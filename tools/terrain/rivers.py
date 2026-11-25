"""Trace rivers from the elevation model (no hand-drawn rivers).
  1. fill pits/depressions, D8 flow directions and flow accumulation (pysheds);
  2. follow the flow downstream from a seed point (snapped to the strongest channel nearby) until the sea
     or until it joins an already traced river;
  3. refine inside a corridor along that path with a least-cost route that hugs the lowest ground (the channel);
  4. optional --via waypoints force the route (needed in deltas/flat plains, where D8 may follow a MODERN canal:
     at the Tiber mouth it followed the Fiumicino canal, so the lower Tiber was routed via Ostia to the natural mouth);
  5. --check prints the distance from the traced line to known points (bridges, confluences). Report these numbers.
Latium example (result already saved in tools/terrain/latium-rivers.json; Tiber within 40-150 m of Rome's bridges):
  python3 tools/terrain/rivers.py --dem ~/.atlas-cache/dem/srtm_39_04.tif --area 11.55 13.45 41.25 43.0 \
    --river tiber 42.46,12.39 --via 41.802,12.335 --via 41.7588,12.2896 --via 41.7405,12.2335 \
    --river anio 41.93,13.08 --join \
    --check "Ponte Milvio" 41.9357,12.4667 --check "Tiber Island" 41.8906,12.4775 --out latium-rivers.json
"""
import argparse, json, math, os
import numpy as np, tifffile
if not hasattr(np, 'in1d'): np.in1d = lambda a, b, **k: np.isin(a, b, **k)
from scipy import ndimage as ndi
from skimage.graph import route_through_array
ap = argparse.ArgumentParser()
ap.add_argument('--dem', required=True); ap.add_argument('--area', nargs=4, type=float, required=True, metavar=('LON0', 'LON1', 'LAT0', 'LAT1'))
ap.add_argument('--river', nargs=2, action='append', default=[], metavar=('NAME', 'LAT,LON'))
ap.add_argument('--via', action='append', default=[], help='waypoint LAT,LON for the most recent --river (repeatable)')
ap.add_argument('--join', action='store_true', help='stop the most recent --river where it meets an earlier one')
ap.add_argument('--check', nargs=2, action='append', default=[], metavar=('LABEL', 'LAT,LON'))
ap.add_argument('--out', default='rivers.json'); ap.add_argument('--simplify', type=float, default=0.00035)
import sys
# attach --via/--join to the preceding --river
order = []; cur = None
argv = sys.argv[1:]; i = 0
while i < len(argv):
    if argv[i] == '--river': cur = {'name': argv[i + 1], 'seed': argv[i + 2], 'via': [], 'join': False}; order.append(cur); i += 3; continue
    if argv[i] == '--via' and cur: cur['via'].append(argv[i + 1]); i += 2; continue
    if argv[i] == '--join' and cur: cur['join'] = True; i += 1; continue
    i += 1
a = ap.parse_args()
from pysheds.sview import Raster, ViewFinder
from pysheds.grid import Grid
from affine import Affine
import pyproj
tfw = [float(x) for x in open(os.path.splitext(a.dem)[0] + '.tfw').read().split()]
res = tfw[0]; X0 = tfw[4] - res / 2; Y0 = tfw[5] + res / 2
d = tifffile.imread(a.dem).astype(np.float64)
L0, L1, B0, B1 = a.area
c0 = int((L0 - X0) / res); c1 = int((L1 - X0) / res); r0 = int((Y0 - B1) / res); r1 = int((Y0 - B0) / res)
z = d[r0:r1, c0:c1].copy(); z[z < -1000] = -5
GX, GY = X0 + c0 * res, Y0 - r0 * res
vf = ViewFinder(affine=Affine(res, 0, GX, 0, -res, GY), shape=z.shape, nodata=-9999.0, crs=pyproj.Proj('EPSG:4326'))
g = Grid(viewfinder=vf); dem = Raster(z, viewfinder=vf)
f = g.resolve_flats(g.fill_depressions(g.fill_pits(dem)))
fd = np.asarray(g.flowdir(f)); acc = np.asarray(g.accumulation(g.flowdir(f)))
H, W = z.shape
step = {64: (-1, 0), 128: (-1, 1), 1: (0, 1), 2: (1, 1), 4: (1, 0), 8: (1, -1), 16: (0, -1), 32: (-1, -1)}
rc = lambda la, lo: (int((GY - la) / res), int((lo - GX) / res))
ll = lambda r, c: (GY - (r + .5) * res, GX + (c + .5) * res)
km = lambda p, q: math.hypot((p[0] - q[0]) * 111.0, (p[1] - q[1]) * 111.0 * math.cos(math.radians(p[0])))
def snap(la, lo, rad=15):
    r, c = rc(la, lo); s = acc[r - rad:r + rad + 1, c - rad:c + rad + 1]; i_ = np.unravel_index(np.argmax(s), s.shape); return r - rad + i_[0], c - rad + i_[1]
locmin = ndi.minimum_filter(z, size=31)
def lowroute(path, buf=18, T=3.0, ends=None):
    m = np.zeros(z.shape, bool)
    for p in path: r, c = rc(*p); m[max(r - 1, 0):r + 2, max(c - 1, 0):c + 2] = True
    m = ndi.binary_dilation(m, iterations=buf)
    cost = np.exp(np.clip((z - locmin) / T, 0, 12)); cost[~m] = 1e9; cost[z <= -5] = 1e6
    a_, b_ = ends or (rc(*path[0]), rc(*path[-1]))
    rr = np.where(m.any(1))[0]; cc = np.where(m.any(0))[0]; R0, R1, C0, C1 = rr[0], rr[-1] + 1, cc[0], cc[-1] + 1
    p2, _ = route_through_array(cost[R0:R1, C0:C1], (a_[0] - R0, a_[1] - C0), (b_[0] - R0, b_[1] - C0), fully_connected=True, geometric=True)
    return [ll(p[0] + R0, p[1] + C0) for p in p2]
done = {}
for rv in order:
    la, lo = map(float, rv['seed'].split(',')); r, c = snap(la, lo)
    pts = []
    for _ in range(40000):
        pts.append(ll(r, c))
        if z[r, c] <= -5: break
        if rv['join'] and done and any(km(pts[-1], q) < 0.15 for P in done.values() for q in P[::3]): break
        dd = int(fd[r, c])
        if dd not in step: break
        r += step[dd][0]; c += step[dd][1]
        if not (0 <= r < H and 0 <= c < W): break
    if rv['via']:
        vias = [tuple(map(float, v.split(','))) for v in rv['via']]
        k = min(range(len(pts)), key=lambda i_: km(pts[i_], vias[0]))
        head = lowroute(pts[:k + 1]); tail = []
        prev = vias[0]
        for v in vias[1:]:
            seg = [prev, v]; mid = [(prev[0] + (v[0] - prev[0]) * t, prev[1] + (v[1] - prev[1]) * t) for t in np.linspace(0, 1, 30)]
            tail += lowroute(mid, buf=60)[1:]; prev = v
        out = head + tail
    else:
        out = lowroute(pts)
    done[rv['name']] = out
    print(rv['name'], 'points', len(out), 'from', tuple(round(x, 4) for x in out[0]), 'to', tuple(round(x, 4) for x in out[-1]))
for lab, p in a.check:
    q = tuple(map(float, p.split(',')))
    best = min(((km(q, x), n) for n, P in done.items() for x in P), key=lambda t: t[0])
    print(f'check {lab:22} {best[0] * 1000:6.0f} m from {best[1]}')
from shapely.geometry import LineString
res_ = {n: [[round(y, 4), round(x, 4)] for x, y in LineString([(p[1], p[0]) for p in P]).simplify(a.simplify).coords] for n, P in done.items()}
json.dump(res_, open(a.out, 'w'), separators=(',', ':')); print('saved', a.out)
