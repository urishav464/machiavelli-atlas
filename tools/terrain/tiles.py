"""Detailed terrain tiles for a region (SRTM hillshade blended with the Blue Marble colors of the base map).
Output: <repo>/<out>/{u}/{x}/{y}.webp, 1024-px tiles. In Leaflet: tileSize:1024, zoomOffset:-2, so URL level u
is shown at map zoom u+2. Levels 7,8,9,10 -> map zooms 9-12 (set maxNativeZoom:12, maxZoom:13).
Edges fade to transparent (~0.06 deg) so the tiles blend into the base map. Example (Latium, already built in tl/):
  python3 tools/terrain/tiles.py --bbox 11.85 13.15 41.42 42.42 --dem ~/.atlas-cache/dem/srtm_39_04.tif \
      --wbd ~/.atlas-cache/dem/wbd --out tl --levels 7,8,9,10
A new region needs its own folder (e.g. tl2/) and its own L.tileLayer with matching bounds."""
import argparse, math, os, glob, re
import numpy as np, tifffile
from PIL import Image
from scipy import ndimage as ndi
ap = argparse.ArgumentParser()
ap.add_argument('--bbox', nargs=4, type=float, required=True, metavar=('LON0', 'LON1', 'LAT0', 'LAT1'))
ap.add_argument('--dem', required=True); ap.add_argument('--wbd', default=None)
ap.add_argument('--repo', default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
ap.add_argument('--out', default='tl'); ap.add_argument('--levels', default='7,8,9,10')
a = ap.parse_args(); BB = a.bbox
# --- DEM georeference from the .tfw world file
tfw = [float(x) for x in open(os.path.splitext(a.dem)[0] + '.tfw').read().split()]
res = tfw[0]; X0 = tfw[4] - res / 2; Y0 = tfw[5] + res / 2
d = tifffile.imread(a.dem).astype(np.float32)
pad = 0.08
c0 = int((BB[0] - pad - X0) / res); c1 = int((BB[1] + pad - X0) / res); r0 = int((Y0 - BB[3] - pad) / res); r1 = int((Y0 - BB[2] + pad) / res)
z = d[r0:r1, c0:c1].copy(); sea = z < -1000; z[sea] = 0; z = np.maximum(z, 0)
gx0 = X0 + c0 * res; gy0 = Y0 - r0 * res
H, W = z.shape; lat = gy0 - (np.arange(H) + .5) * res; lon = gx0 + (np.arange(W) + .5) * res
LA, LO = np.meshgrid(lat, lon, indexing='ij')
lake = np.zeros_like(sea)
if a.wbd:
    for f in glob.glob(os.path.join(a.wbd, '*_att.tif')):
        m_ = re.search(r'([NS])(\d+)([EW])(\d+)', os.path.basename(f))
        la0 = (int(m_.group(2)) if m_.group(1) == 'N' else -int(m_.group(2))) + 1
        lo0 = int(m_.group(4)) if m_.group(3) == 'E' else -int(m_.group(4))
        m = (LA <= la0) & (LA > la0 - 1) & (LO >= lo0) & (LO < lo0 + 1)
        if not m.any(): continue
        att = tifffile.imread(f)
        v = att[((la0 - LA[m]) * 3600).astype(int).clip(0, 3600), ((LO[m] - lo0) * 3600).astype(int).clip(0, 3600)]
        lk = np.zeros_like(sea); lk[m] = (v == 3); lake |= lk
# --- hillshade (multi-directional)
dx = res * 111320 * math.cos(math.radians((BB[2] + BB[3]) / 2)); dy = res * 110950
gy, gx = np.gradient(ndi.gaussian_filter(z, 0.6), dy, dx)
def shade(azd, alt, ex=2.2):
    az, al = math.radians(azd), math.radians(alt); sl = np.arctan(np.hypot(gx, gy) * ex); asp = np.arctan2(-gx, gy)
    return np.clip(np.sin(al) * np.cos(sl) + np.cos(al) * np.sin(sl) * np.cos(az - asp), 0, 1)
hs = (0.55 * shade(315, 42) + 0.25 * shade(270, 48) + 0.20 * shade(350, 55)) / (0.55 * math.sin(math.radians(42)) + 0.25 * math.sin(math.radians(48)) + 0.2 * math.sin(math.radians(55)))
def hyps(e):
    stops = [(0, (196, 206, 168)), (60, (206, 208, 170)), (200, (214, 206, 165)), (500, (196, 180, 140)), (900, (176, 160, 128)), (1500, (160, 150, 135)), (2200, (200, 196, 190))]
    out = np.zeros(e.shape + (3,), np.float32)
    for (e0, k0), (e1, k1) in zip(stops[:-1], stops[1:]):
        m = (e >= e0) & (e < e1); t = ((e[m] - e0) / (e1 - e0))[:, None]; out[m] = np.array(k0) * (1 - t) + np.array(k1) * t
    out[e >= stops[-1][0]] = stops[-1][1]; return out
# --- Blue Marble colors from the base tiles t/7/x/y.jpg (512 px = one z7 tile)
def merc(la): return (1 - np.arcsinh(np.tan(np.radians(la))) / np.pi) / 2
tx0, tx1 = int((BB[0] - .2 + 180) / 360 * 128), int((BB[1] + .2 + 180) / 360 * 128)
ty0, ty1 = int(merc(BB[3] + .2) * 128), int(merc(BB[2] - .2) * 128)
BM = np.zeros(((ty1 - ty0 + 1) * 512, (tx1 - tx0 + 1) * 512, 3), np.float32)
for x in range(tx0, tx1 + 1):
    for y in range(ty0, ty1 + 1):
        p = os.path.join(a.repo, 't', '7', str(x), f'{y}.jpg')
        if os.path.exists(p): BM[(y - ty0) * 512:(y - ty0 + 1) * 512, (x - tx0) * 512:(x - tx0 + 1) * 512] = np.asarray(Image.open(p).convert('RGB'))
BMb = np.stack([ndi.gaussian_filter(BM[..., k], 1.6) for k in range(3)], -1)
SEA = np.array([26, 67, 127], np.float32); LAKE = np.array([74, 118, 160], np.float32)
seaf = ndi.gaussian_filter(sea.astype(np.float32), 0.8); lakef = ndi.gaussian_filter(lake.astype(np.float32), 0.7)
def tile(u, x, y, N=1024):
    Z = 256 * 2 ** (u + 2); i = np.arange(N) + .5
    lo = (x * N + i) / Z * 360 - 180; la = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * (y * N + i) / Z))))
    A, O = np.meshgrid(la, lo, indexing='ij')
    gr = (gy0 - A) / res - .5; gc = (O - gx0) / res - .5
    smp = lambda arr: ndi.map_coordinates(arr, [gr, gc], order=1, mode='nearest')
    e, h, sf, lf = smp(z), smp(hs), smp(seaf), smp(lakef)
    bx = ((O + 180) / 360 * 128 - tx0) * 512; by = (merc(A) * 128 - ty0) * 512
    bmc = np.stack([ndi.map_coordinates(BMb[..., k], [by, bx], order=1, mode='nearest') for k in range(3)], -1)
    land = np.clip((0.12 * hyps(e) * 0.55 + 0.88 * bmc) * (0.40 + 0.72 * h[..., None]) * 1.06, 0, 255)
    rgb = land * (1 - sf[..., None]) + SEA * sf[..., None]; rgb = rgb * (1 - lf[..., None]) + LAKE * lf[..., None]
    fe = 0.06; ax = np.clip(np.minimum(O - BB[0], BB[1] - O) / fe, 0, 1); ay = np.clip(np.minimum(A - BB[2], BB[3] - A) / fe, 0, 1)
    al = ax * ay; al = al * al * (3 - 2 * al)
    return np.dstack([np.clip(rgb, 0, 255), al[..., None] * 255]).astype(np.uint8), al.max()
tot = 0
for u in [int(v) for v in a.levels.split(',')]:
    n = 2 ** u
    xs = range(int((BB[0] + 180) / 360 * n), int((BB[1] + 180) / 360 * n) + 1); ys = range(int(merc(BB[3]) * n), int(merc(BB[2]) * n) + 1)
    for x in xs:
        for y in ys:
            img, amax = tile(u, x, y)
            if amax <= 0: continue
            d_ = os.path.join(a.repo, a.out, str(u), str(x)); os.makedirs(d_, exist_ok=True)
            p = os.path.join(d_, f'{y}.webp'); Image.fromarray(img, 'RGBA').save(p, 'WEBP', quality=80, method=5); tot += os.path.getsize(p)
print('tiles written, total', tot // 1024, 'KB')
