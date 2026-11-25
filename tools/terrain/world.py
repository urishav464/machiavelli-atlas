"""Low-resolution world base (one Web-Mercator image) for steps that leave the Mediterranean tiles,
e.g. the Atlantic voyages of the preface. Source: NASA Blue Marble texture (public domain) as shipped in the
three.js repository on GitHub (examples/textures/planets/earth_day_4096.jpg, equirectangular 4096x2048).
Its colours are matched to the existing base tiles t/ (per-channel histogram matching on the overlap), so the
seam at the edge of t/ is not obvious. In the page it sits in a pane under the tiles.
usage: python3 tools/terrain/world.py [--bbox lon0,lon1,lat0,lat1] [--out base/world.jpg]"""
import argparse, math, os, glob, urllib.request
import numpy as np
from PIL import Image
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(os.environ.get('ATLAS_CACHE', os.path.expanduser('~/.atlas-cache')), 'world')
SRC = os.path.join(C, 'earth_day_4096.jpg')
URL = 'https://raw.githubusercontent.com/mrdoob/three.js/dev/examples/textures/planets/earth_day_4096.jpg'
ap = argparse.ArgumentParser()
ap.add_argument('--bbox', default='-100,60,-45,66')
ap.add_argument('--out', default=os.path.join(REPO, 'base', 'world.jpg'))
ap.add_argument('--zoom', type=int, default=4, help='display zoom whose scale the image uses (256px tiles)')
a = ap.parse_args()
lon0, lon1, lat0, lat1 = map(float, a.bbox.split(','))
os.makedirs(C, exist_ok=True)
if not os.path.exists(SRC): urllib.request.urlretrieve(URL, SRC)
tex = np.asarray(Image.open(SRC).convert('RGB'), np.float32); TH, TW = tex.shape[:2]
WORLD = 256 * 2 ** a.zoom
mx = lambda lon: (lon + 180) / 360 * WORLD
my = lambda lat: (1 - math.asinh(math.tan(math.radians(lat))) / math.pi) / 2 * WORLD
X0, X1, Y0, Y1 = mx(lon0), mx(lon1), my(lat1), my(lat0)
W, H = int(round(X1 - X0)), int(round(Y1 - Y0))
def sample(xs, ys):
    """texture colour at world-pixel coords (bilinear)"""
    lon = xs / WORLD * 360 - 180; lat = np.degrees(np.arctan(np.sinh(np.pi * (1 - 2 * ys / WORLD))))
    u = (lon + 180) / 360 * TW - .5; v = (90 - lat) / 180 * TH - .5
    u0 = np.floor(u).astype(int); v0 = np.floor(v).astype(int); fu = (u - u0)[..., None]; fv = (v - v0)[..., None]
    g = lambda vv, uu: tex[np.clip(vv, 0, TH - 1), np.mod(uu, TW)]
    return (g(v0, u0) * (1 - fu) + g(v0, u0 + 1) * fu) * (1 - fv) + (g(v0 + 1, u0) * (1 - fu) + g(v0 + 1, u0 + 1) * fu) * fv
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32); out = sample(xx + X0 + .5, yy + Y0 + .5)
# reference: mosaic of the existing base tiles at the same scale (t/ uses 512px tiles with zoomOffset -1)
tz = a.zoom - 1; ref = np.zeros((H, W, 3), np.float32); have = np.zeros((H, W), bool)
for f in glob.glob(os.path.join(REPO, 't', str(tz), '*', '*.jpg')):
    tx, ty = int(f.split(os.sep)[-2]), int(os.path.splitext(os.path.basename(f))[0])
    px, py = tx * 512 - X0, ty * 512 - Y0
    im = np.asarray(Image.open(f).convert('RGB'), np.float32)
    xa, ya = int(round(px)), int(round(py)); xb, yb = xa + 512, ya + 512
    cx0, cy0, cx1, cy1 = max(xa, 0), max(ya, 0), min(xb, W), min(yb, H)
    if cx0 >= cx1 or cy0 >= cy1: continue
    blk = im[cy0 - ya:cy1 - ya, cx0 - xa:cx1 - xa]; ok = blk.sum(2) > 6
    ref[cy0:cy1, cx0:cx1][ok] = blk[ok]; have[cy0:cy1, cx0:cx1] |= ok
print('overlap pixels for colour matching:', int(have.sum()))
for c in range(3):   # histogram matching, channel by channel
    s = np.sort(out[..., c][have]); r = np.sort(ref[..., c][have])
    q = np.linspace(0, 1, 256); sv = np.quantile(s, q); rv = np.quantile(r, q)
    out[..., c] = np.interp(out[..., c], sv, rv)
os.makedirs(os.path.dirname(a.out), exist_ok=True)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(a.out, quality=84, optimize=True, progressive=True)
print(a.out, f'{W}x{H}', os.path.getsize(a.out) // 1024, 'KB; bounds [[%g,%g],[%g,%g]]' % (lat0, lon0, lat1, lon1))
