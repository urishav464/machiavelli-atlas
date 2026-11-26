"""Least-cost path over SRTM between named stations, to get terrain-following waypoints for a route
whose stations are documented but whose road is not. Output: simplified [lat, lon] waypoints + profile.
usage: python3 tools/terrain/lcpath.py <dem.tif> lat,lon lat,lon [lat,lon ...]   (stations in order)"""
import sys, numpy as np, tifffile, os
from skimage.graph import route_through_array
dem_path = sys.argv[1]; st = [tuple(map(float, a.split(','))) for a in sys.argv[2:]]
tfw = [float(x) for x in open(dem_path[:-4] + '.tfw').read().split()]
res, x0, y0 = tfw[0], tfw[4], tfw[5]
Z = tifffile.imread(dem_path).astype(float); Z[Z < -1000] = np.nan
lat0, lat1 = min(p[0] for p in st) - .08, max(p[0] for p in st) + .08
lon0, lon1 = min(p[1] for p in st) - .08, max(p[1] for p in st) + .08
r0, r1 = int((y0 - lat1) / res), int((y0 - lat0) / res); c0, c1 = int((lon0 - x0) / res), int((lon1 - x0) / res)
z = Z[r0:r1, c0:c1]; z = np.where(np.isnan(z), np.nanmax(z), z)
dy = res * 111320; dx = dy * np.cos(np.radians((lat0 + lat1) / 2))
gy, gx = np.gradient(z, dy, dx); slope = np.hypot(gx, gy)
cost = 1 + (slope * 25) ** 2 + np.clip(z - np.percentile(z, 20), 0, None) / 150.0
def rc(p): return int((y0 - p[0]) / res) - r0, int((p[1] - x0) / res) - c0
segs = []
for a, b in zip(st, st[1:]):
    idx, _ = route_through_array(cost, rc(a), rc(b), fully_connected=True, geometric=True)
    segs.append([(y0 - (r + r0 + .5) * res, x0 + (c + c0 + .5) * res, z[r, c]) for r, c in idx])
ll = [p for s_ in segs for p in s_]
# Douglas-Peucker in degrees (~0.004 deg ~ 350 m), keeping the stations
def dp(pts, eps):
    if len(pts) < 3: return pts
    a, b = np.array(pts[0][:2]), np.array(pts[-1][:2]); d = b - a; n = np.hypot(*d) or 1
    dist = [abs(d[0] * (p[1] - a[1]) - d[1] * (p[0] - a[0])) / n for p in pts[1:-1]]
    i = int(np.argmax(dist)) + 1
    return dp(pts[:i + 1], eps)[:-1] + dp(pts[i:], eps) if dist[i - 1] > eps else [pts[0], pts[-1]]
eps = float(os.environ.get('EPS', '0.006')); out = []
for s_ in segs: out += dp(s_, eps) if not out else dp(s_, eps)[1:]
for la, lo, h in out: print(f'[{la:.4f},{lo:.4f}],  # {h:.0f} m')
print('max elevation on path:', int(max(p[2] for p in ll)), 'm; points:', len(out))
