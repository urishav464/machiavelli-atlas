"""Worked example: the four kings of Rome (Discourses I.19, story 1). Re-creates ovl/rome-0..3.webp and the tap geometry.
Facts behind every shape: facts/ch19-rome.md (verified twice, approved by Uri 2026-11-25).
usage: python3 tools/overlays/rome_kings.py   (needs tools/terrain/get_dem.sh srtm_39_04 N41E012 N42E012)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
C = os.path.join(os.environ.get('ATLAS_CACHE', os.path.expanduser('~/.atlas-cache')), 'dem')
BB = (11.85, 13.15, 41.42, 42.42)
F = Frame(BB, os.path.join(C, 'srtm_39_04.tif'), os.path.join(C, 'wbd'))
RV = json.load(open(os.path.join(REPO, 'tools/terrain/latium-rivers.json')))
left, right = banks(RV['tiber'], (12.60, 41.80), BB)
MI = 1.48  # Roman mile, km
G = {}
G['rome_r'] = ell(12.486, 41.889, 5.5 * MI).intersection(left)                       # Strabo 5.3.2: old boundary 5-6 miles
jan = along(RV['tiber'], 41.912, 41.862, 1.6, right)                                 # Janiculum (Livy 1.33.6)
G['rome_a'] = unary_union([G['rome_r'], along(RV['tiber'], 41.90, 41.70, 5.0, left), jan])  # Ancus: "to the sea" (1.33.9)
G['col_fid'] = ell(12.5154, 41.9821, 1.8); G['col_cru'] = ell(12.5501, 42.0151, 1.8)
G['septem'] = along(RV['tiber'], 41.905, 41.80, 3.0, right).difference(jan)        # Septem Pagi: right bank, location unknown
G['maesia'] = along(RV['tiber'], 41.862, 41.70, 4.0, right)                         # Silva Maesia: right bank, location unknown
G['alban'] = chaikin([(12.55, 41.80), (12.68, 41.80), (12.735, 41.745), (12.71, 41.68), (12.60, 41.655), (12.535, 41.71)], 3)
G['albagone'] = ell(12.650, 41.747, 1.4); G['polit'] = ell(12.430, 41.728, 2.0); G['lavin'] = ell(12.4807, 41.6645, 1.8)
G['veii'] = chaikin([(12.18, 41.86), (12.30, 41.80), (12.44, 41.86), (12.50, 41.95), (12.53, 42.05), (12.52, 42.15), (12.40, 42.20), (12.25, 42.15), (12.18, 42.02)], 3).intersection(right)
G['etruria'] = right.intersection(box(BB[0], BB[2], BB[1], BB[3])).difference(G['veii'])
G['sabines'] = chaikin([(12.50, 42.06), (12.70, 42.04), (12.85, 42.09), (13.0, 42.13), (13.3, 42.15), (13.3, 42.6), (12.40, 42.6)], 2).intersection(left)
G['aequi'] = chaikin([(12.86, 41.98), (13.05, 41.90), (13.3, 41.88), (13.3, 42.14), (12.98, 42.11), (12.86, 42.05)], 2).intersection(left).difference(G['sabines'])
G['volsci'] = chaikin([(12.74, 41.62), (12.95, 41.69), (13.3, 41.66), (13.3, 41.3), (12.70, 41.3), (12.66, 41.52)], 2).intersection(left)
G['latins'] = left.intersection(box(BB[0], BB[2], BB[1], BB[3])).difference(unary_union([G['sabines'], G['aequi'], G['volsci']]))
Z = lambda k, r: (G[k], r, 20, 0)           # neighbour zone, soft
S = lambda k, r, soft=0: (G[k], r, soft, 1)  # state / place, crisp
STEPS = [
 [Z('etruria','neutral'),Z('veii','enemy'),Z('sabines','ally'),Z('latins','neutral'),Z('aequi','neutral'),Z('volsci','neutral'),S('lavin','ally'),S('septem','trad'),S('col_fid','trad'),S('col_cru','trad'),(G['rome_r'],'core',9,0)],
 [Z('etruria','neutral'),Z('veii','ally'),Z('sabines','ally'),Z('latins','ally'),Z('aequi','neutral'),Z('volsci','neutral'),S('septem','trad'),S('col_fid','trad'),S('col_cru','trad'),S('rome_r','core')],
 [Z('etruria','neutral'),Z('veii','enemy'),Z('sabines','enemy'),Z('latins','ally'),Z('aequi','neutral'),Z('volsci','neutral'),S('alban','trad'),S('albagone','gone'),S('septem','trad'),S('col_fid','enemy'),S('col_cru','trad'),S('rome_r','core')],
 [Z('etruria','neutral'),Z('veii','enemy'),Z('sabines','neutral'),Z('latins','enemy'),Z('aequi','neutral'),Z('volsci','neutral'),S('alban','trad'),S('albagone','gone'),S('polit','gone'),S('septem','trad'),S('maesia','trad'),S('col_fid','trad'),S('col_cru','trad'),S('rome_a','core')],
]
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'ovl')
for i, st in enumerate(STEPS): F.render(st, os.path.join(out, f'rome-{i}.webp'))
F.export_geo(G, os.path.join(out, 'rome-geo.json'))
