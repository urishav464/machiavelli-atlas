"""Discourses I.19, story 4: the kingdom of France and its "ancient orders". Re-creates ovl/fra-0.webp and the tap geometry.
The 1515 border is built from modern départements (Natural Earth admin-1) minus the lands that were not French then
(facts/ch19-ottoman-france-geo.md 1-9, facts/ch19-france-geo2.md); départements only serve as building blocks.
Neighbours are soft zones; small sovereign enclaves (Calais, Avignon, Orange, Béarn) are crisp.
usage: python3 tools/overlays/france.py [outdir]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
LARGE = {'core': .30, 'gain': .26}   # zoom 4-6 on the satellite base: lighter fills, the crisp edge carries the border
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BB = (-5.5, 11.5, 41.2, 51.5)
LAND = land_from_ne(BB)
F = Frame(BB, land=LAND, W=1500, alpha=LARGE)
D = {k: v for k, v in ne_admin1('FRA').items() if box(-6, 41, 10, 52).contains(v.representative_point())}
U = lambda *ks: unary_union([D[k] for k in ks])
P = lambda pts, n=2: chaikin(pts, n)
metro = unary_union(list(D.values()))
corsica = U('Corse-du-Sud', 'Haute-Corse')
# not French in 1515
roussillon = D['Pyrénées-Orientales'].difference(box(1.95, 42.70, 2.85, 43.0))              # Fenouillèdes (north) stays French
VAR = [(7.20, 43.55), (7.19, 43.80), (7.13, 43.87), (6.95, 43.95), (6.85, 44.05), (6.72, 44.20), (6.65, 44.45)]
nice = D['Alpes-Maritimes'].intersection(Polygon(VAR + [(8.2, 44.45), (8.2, 43.5)]))
ubaye = D['Alpes-de-Haute-Provence'].intersection(P([(6.40, 44.42), (6.55, 44.56), (6.90, 44.56), (6.98, 44.40), (6.75, 44.29), (6.50, 44.31)], 1))   # Barcelonnette valley: Savoyard 1388-1713
savoy_fr = unary_union([U('Savoie', 'Haute-Savoie', 'Ain'), nice, ubaye])   # the Var line is only approximate (geo2-check 5)
fcomte = U('Doubs', 'Jura', 'Haute-Saône')
lorraine = U('Moselle', 'Meurthe-et-Moselle', 'Vosges', 'Meuse')
alsace = U('Bas-Rhin', 'Haute-Rhin', 'Territoire de Belfort')
pdc_fr = D['Pas-de-Calais'].intersection(Polygon([(1.3, 50.25), (2.08, 50.25), (2.02, 50.6), (1.97, 50.85), (1.3, 51.1)]))   # Boulonnais, Montreuil
calais = D['Pas-de-Calais'].intersection(Polygon([(1.72, 50.93), (1.80, 50.85), (1.90, 50.845), (1.95, 50.875), (2.12, 50.92), (2.12, 51.05), (1.70, 51.05)]))   # Guînes inside, Ardres (French) outside; extent estimated
artois = unary_union([D['Nord'], D['Pas-de-Calais'].difference(pdc_fr)]).difference(calais)
orange = ell(4.81, 44.14, 9).intersection(D['Vaucluse'])
comtat = D['Vaucluse'].intersection(box(4.6, 43.6, 5.30, 44.5)).difference(orange)
soule = P([(-1.06, 43.31), (-0.80, 43.30), (-0.74, 43.05), (-0.85, 42.90), (-1.08, 42.96)], 2)
albret = D['Pyrénées-Atlantiques'].intersection(P([(-1.48, 42.95), (-1.40, 43.45), (-1.20, 43.55), (-0.8, 43.75), (0.3, 43.75), (0.3, 42.6), (-1.3, 42.6)], 2)).difference(soule)    # Béarn + Lower Navarre
lnav = D['Pyrénées-Atlantiques'].intersection(P([(-1.48, 42.95), (-1.40, 43.38), (-1.15, 43.45), (-0.93, 43.42), (-0.96, 43.2), (-1.06, 43.0)], 1)).difference(soule)   # Lower Navarre: disputed after 1512
bearn = albret.difference(lnav)
brittany = U("Finistère", "Côtes-d'Armor", 'Morbihan', 'Ille-et-Vilaine', 'Loire-Atlantique')
notfr = unary_union([corsica, roussillon, savoy_fr, fcomte, lorraine, alsace, artois, calais, orange, comtat, albret])
france = metro.difference(notfr).difference(brittany).buffer(0.002).buffer(-0.002)
# neighbours (rough, soft)
milan = P([(8.45, 45.20), (8.55, 45.75), (8.75, 46.05), (9.10, 45.95), (9.45, 45.88), (9.52, 45.45), (9.70, 45.25), (10.20, 45.12), (10.05, 45.10), (9.70, 45.08), (9.45, 45.12), (9.20, 44.75), (8.85, 44.75), (8.50, 44.90)], 1)   # core only; south of the Po (Parma, Piacenza) left out: unverified
piedmont = P([(6.62, 44.45), (6.90, 44.98), (6.95, 45.60), (7.85, 45.95), (8.40, 45.55), (8.40, 45.0), (8.20, 44.55), (7.70, 44.15), (7.0, 44.15)], 1).difference(milan)
savoy = unary_union([savoy_fr, piedmont])
swiss = P([(6.9, 47.5), (7.6, 47.6), (8.6, 47.8), (9.6, 47.55), (9.5, 47.05), (9.2, 46.6), (9.05, 46.15), (8.55, 46.35), (7.9, 46.3), (7.1, 46.6), (6.9, 46.95)], 1)
hab_nl = unary_union([artois, P([(2.4, 51.1), (3.6, 51.5), (4.3, 52.4), (5.6, 53.4), (7.1, 53.3), (6.2, 51.8), (6.1, 50.7), (5.8, 49.6), (4.9, 49.8), (4.2, 50.2), (3.3, 50.4), (2.6, 50.75)], 1)])
empire = unary_union([alsace, P([(7.0, 49.2), (8.2, 51.5), (11.5, 51.5), (11.5, 47.6), (9.6, 47.55), (8.6, 47.8), (7.6, 47.6), (7.5, 48.6)], 1)]).difference(swiss)
spain = unary_union([roussillon, Polygon([(-5.6, 43.7), (-1.8, 43.38), (-1.45, 43.05), (-0.75, 42.85), (0.0, 42.68), (1.4, 42.55), (1.75, 42.45), (2.2, 42.35), (3.3, 42.35), (3.6, 41.2), (-5.6, 41.2)])])
england = P([(-5.6, 50.0), (-5.6, 51.6), (1.6, 51.6), (1.6, 50.7), (-3.0, 50.2)], 1)
G = {'fr1515': france, 'brittany': brittany, 'milan': milan, 'savoy': savoy, 'fcomte': fcomte, 'lorraine': lorraine, 'empire': empire,
     'hab_nl': hab_nl, 'swiss': swiss, 'spain': spain, 'england': england, 'calais': calais, 'comtat': comtat, 'orange': orange,
     'bearn': bearn, 'lnav': lnav, 'corsica': corsica}
Z = lambda k, r='neutral': (G[k], r, 18, 0)
S = lambda k, r: (G[k], r, 0, 1)
STEP = [Z('england'), Z('hab_nl'), Z('empire'), Z('lorraine'), Z('fcomte'), Z('swiss'), Z('savoy'), Z('spain'),
        S('calais', 'neutral'), S('comtat', 'neutral'), S('orange', 'neutral'), S('bearn', 'neutral'), S('lnav', 'disp'), S('corsica', 'neutral'),
        S('milan', 'gain'), S('brittany', 'pu'), S('fr1515', 'core')]
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'ovl')
F.render(STEP, os.path.join(out, 'fra-0.webp'))
F.export_geo(G, os.path.join(out, 'fra-geo.json'), tol=0.02)
