"""Atlas-style territory overlays (one transparent WebP per story step) + simplified polygons for tap-to-read.
The overlay is a Web-Mercator raster of a bbox; in the page it is an L.imageOverlay with the same bbox
(step field  map.ovb:[[lat0,lon0],[lat1,lon1]]  plus  map.ovl:'ovl/<name>.webp').
Roles and colours are shared by all stories (see ROLE/KIND in index.html):
  core = the state of the story (navy), trad = held "according to the tradition", extent estimated (navy hatch),
  vassal (navy hatch), ally (gold), enemy (dark red), rival (red), crack (orange hatch), neutral (grey-brown),
  gone / razed (grey hatch).
Neighbour peoples whose borders are not known are drawn as soft zones (soft >= 15 px blur, no edge);
the state itself gets a crisp edge band. See rome_kings.py for a complete worked example."""
import math, os, glob, re, json
import numpy as np, tifffile
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from shapely.geometry import Polygon, Point, LineString, box
from shapely.ops import split, unary_union
STY = {'core': ((30, 62, 122), .58), 'trad': ((35, 67, 119), .14), 'vassal': ((35, 67, 119), .14), 'ally': ((201, 151, 31), .24),
       'enemy': ((142, 27, 20), .24), 'rival': ((179, 56, 43), .30), 'crack': ((224, 102, 43), .16), 'neutral': ((92, 84, 70), .10),
       'gone': ((110, 110, 110), .20), 'razed': ((110, 110, 110), .20)}
EDGE = {'core': (24, 50, 92), 'trad': (35, 67, 119), 'vassal': (35, 67, 119), 'ally': (150, 108, 16), 'enemy': (112, 18, 12),
        'rival': (140, 40, 30), 'crack': (200, 80, 30), 'gone': (90, 90, 90), 'razed': (90, 90, 90)}
HATCHED = {'trad', 'vassal', 'crack', 'gone', 'razed'}
def merc(lat): return (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2
class Frame:
    """bbox = (lon0, lon1, lat0, lat1). Land mask from an SRTM tile (sea = void) and optional ASTER WBD lakes."""
    def __init__(self, bbox, dem, wbd=None, W=1600, SS=2):
        self.BB, self.W, self.SS = bbox, W, SS
        self.mx0, self.mx1 = (bbox[0] + 180) / 360, (bbox[1] + 180) / 360; self.my0, self.my1 = merc(bbox[3]), merc(bbox[2])
        self.H = int(round(W * (self.my1 - self.my0) / (self.mx1 - self.mx0)))
        tfw = [float(x) for x in open(os.path.splitext(dem)[0] + '.tfw').read().split()]
        res = tfw[0]; X0 = tfw[4] - res / 2; Y0 = tfw[5] + res / 2
        d = tifffile.imread(dem)
        ii = np.arange(self.H * SS) + .5; jj = np.arange(W * SS) + .5
        lon = bbox[0] + jj / (W * SS) * (bbox[1] - bbox[0])
        my = self.my0 + ii / (self.H * SS) * (self.my1 - self.my0); lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * my))))
        gr = ((Y0 - lat) / res - .5).astype(int).clip(0, d.shape[0] - 1); gc = ((lon - X0) / res - .5).astype(int).clip(0, d.shape[1] - 1)
        land = d[gr[:, None], gc[None, :]] > -1000
        if wbd:
            LA = lat[:, None] + 0 * lon[None, :]; LO = lon[None, :] + 0 * lat[:, None]
            for f in glob.glob(os.path.join(wbd, '*_att.tif')):
                m_ = re.search(r'([NS])(\d+)([EW])(\d+)', os.path.basename(f))
                la0 = (int(m_.group(2)) if m_.group(1) == 'N' else -int(m_.group(2))) + 1; lo0 = int(m_.group(4)) if m_.group(3) == 'E' else -int(m_.group(4))
                m = (LA <= la0) & (LA > la0 - 1) & (LO >= lo0) & (LO < lo0 + 1)
                if not m.any(): continue
                a = tifffile.imread(f); v = np.zeros(m.shape, np.uint8)
                v[m] = a[((la0 - LA[m]) * 3600).astype(int).clip(0, 3600), ((LO[m] - lo0) * 3600).astype(int).clip(0, 3600)]
                land &= ~(v == 3)
        self.land = ndi.binary_opening(land, iterations=1).astype(np.float32)
        self.yy, self.xx = np.mgrid[0:self.H * SS, 0:W * SS]
    def px(self, lon, lat):
        return ((lon + 180) / 360 - self.mx0) / (self.mx1 - self.mx0) * self.W * self.SS, (merc(lat) - self.my0) / (self.my1 - self.my0) * self.H * self.SS
    def rast(self, geom):
        im = Image.new('L', (self.W * self.SS, self.H * self.SS), 0); dr = ImageDraw.Draw(im)
        for g in ([geom] if geom.geom_type == 'Polygon' else list(getattr(geom, 'geoms', []))):
            if g.is_empty or g.geom_type != 'Polygon': continue
            dr.polygon([self.px(*c) for c in g.exterior.coords], fill=255)
            for h in g.interiors: dr.polygon([self.px(*c) for c in h.coords], fill=0)
        return np.asarray(im, np.float32) / 255
    def hatch(self, sp, ang): return (((self.xx + ang * self.yy) % (sp * self.SS)) < (2.2 * self.SS)).astype(np.float32)
    def edgeband(self, m, wpx): inside = m > 0.5; return np.clip(1 - ndi.distance_transform_edt(inside) / (wpx * self.SS), 0, 1) * inside
    def render(self, layers, out):
        """layers: list of (geometry, role, soft, crisp). soft>=15 -> neighbour zone (blurred, kept off land held by others);
        0<soft<15 -> soft-edged state (e.g. Romulus: no measured border); crisp=1 -> edge band/line."""
        SS = self.SS; rgb = np.zeros((self.H * SS, self.W * SS, 3), np.float32); A = np.zeros((self.H * SS, self.W * SS), np.float32)
        def over(col, a):
            nonlocal rgb, A; a = np.clip(a, 0, 1); rgb = rgb * (1 - a[..., None]) + np.array(col, np.float32) * a[..., None]; A = A + a * (1 - A)
        held = np.zeros_like(self.land)
        for g, role, soft, crisp in layers:
            if soft < 15: held = np.maximum(held, self.rast(g))
        held = ndi.gaussian_filter(held, 2 * SS)
        for g, role, soft, crisp in layers:
            m = self.rast(g) * self.land
            if soft >= 15: m = ndi.gaussian_filter(m, soft * SS) * self.land * (1 - held)
            elif soft: m = ndi.gaussian_filter(m, soft * SS) * self.land
            col, al = STY[role]
            if role in HATCHED:
                over(col, m * al); over(EDGE[role], m * self.hatch(12 if role in ('trad', 'vassal') else 9, 1 if role in ('trad', 'vassal') else -1) * 0.55)
                if crisp: over(EDGE[role], self.edgeband((m > 0.5).astype(np.float32), 1.6) * 0.85)
            else:
                over(col, m * al)
                if crisp:
                    over(EDGE.get(role, col), self.edgeband((m > 0.5).astype(np.float32), 7) ** 2 * 0.35)
                    over(EDGE.get(role, col), self.edgeband((m > 0.5).astype(np.float32), 1.5) * 0.9)
        col = np.where(A[..., None] > 1e-4, rgb / np.maximum(A[..., None], 1e-4), 0)
        im = Image.fromarray(np.dstack([np.clip(col, 0, 255), np.clip(A * 255, 0, 255)]).astype(np.uint8), 'RGBA').resize((self.W, self.H), Image.LANCZOS)
        im.save(out, 'WEBP', quality=82, method=6); print(out, os.path.getsize(out) // 1024, 'KB', im.size)
    def export_geo(self, G, out, tol=0.004):
        """Simplified [lat,lon] rings for tap hit-testing; merge into GEOM in index.html (Object.assign(GEOM, {...}))."""
        geo = {}
        for k, g in G.items():
            gg = g.intersection(box(self.BB[0], self.BB[2], self.BB[1], self.BB[3])).simplify(tol)
            polys = [gg] if gg.geom_type == 'Polygon' else [p for p in getattr(gg, 'geoms', []) if p.geom_type == 'Polygon']
            geo[k] = [[[round(y, 3), round(x, 3)] for x, y in p.exterior.coords] for p in polys if p.area > 1e-5]
        json.dump(geo, open(out, 'w'), separators=(',', ':')); print('geo ->', out)
KM_LAT = 1 / 111.0
def ell(lon, lat, km):
    """Circle of radius km (use for 'about N miles around the city' or a town's estimated area)."""
    kl = 1 / (111.32 * math.cos(math.radians(lat)))
    return Polygon([(lon + km * kl * math.cos(t), lat + km * KM_LAT * math.sin(t)) for t in np.linspace(0, 2 * math.pi, 96)])
def chaikin(coords, n=3):
    """Smooth a hand-made polygon (lon,lat list) so estimated zones don't look like boxes."""
    p = list(coords)
    for _ in range(n):
        q = []
        for a, b in zip(p, p[1:] + p[:1]): q += [(0.75 * a[0] + 0.25 * b[0], 0.75 * a[1] + 0.25 * b[1]), (0.25 * a[0] + 0.75 * b[0], 0.25 * a[1] + 0.75 * b[1])]
        p = q
    return Polygon(p)
def banks(river_latlon, probe_left, bbox):
    """Split the world in two along a river ([[lat,lon],...]). probe_left=(lon,lat) of a point known to be on the
    'left' side. The line is extended far past the bbox so the split always succeeds."""
    tib = [(p[1], p[0]) for p in river_latlon]
    ext = [(tib[0][0], bbox[3] + 0.7)] + tib + [(tib[-1][0] - 0.25, tib[-1][1] - 0.15), (tib[-1][0] - 0.9, tib[-1][1] - 0.7)]
    BOX = box(bbox[0] - .5, bbox[2] - .5, bbox[1] + .5, bbox[3] + .5)
    parts = list(split(BOX, LineString(ext)).geoms)
    left = [p for p in parts if p.contains(Point(probe_left))][0]
    right = unary_union([p for p in parts if p is not left])
    return left, right
def along(river_latlon, lat_hi, lat_lo, km, side):
    """Strip of width km along the river between two latitudes, on one bank."""
    seg = [(p[1], p[0]) for p in river_latlon if lat_lo <= p[0] <= lat_hi]
    return LineString(seg).buffer(km / (111.32 * math.cos(math.radians(seg[0][1]))), cap_style=2).intersection(side)
