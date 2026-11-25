"""Discourses I.19, story 3: Mehmed II, Bayezid II, Selim I. Re-creates ovl/ott-0..2.webp and the tap geometry.
Borders are hand-drawn approximations (rivers, ridges, known towns) of the verified claims in facts/ch19-ottoman-france*.md;
the page says so ("גבולות משוערים"). Islands are taken from Natural Earth and assigned explicitly.
usage: python3 tools/overlays/ottomans.py [outdir]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from lib import *
LARGE = {'core': .30, 'gain': .26}   # zoom 4-6 on the satellite base: lighter fills, the crisp edge carries the border
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BB = (12.0, 48.0, 27.5, 48.0)
LAND = land_from_ne(BB)
F = Frame(BB, land=LAND, W=1800, alpha=LARGE)
P = lambda pts, n=2: chaikin(pts, n)
_parts = sorted(getattr(LAND, 'geoms', [LAND]), key=lambda p: -p.area)
ISL = lambda lo, la: island(LAND, lo, la)
NONMAIN = unary_union(_parts[1:])   # every island (the first part is the mainland)
# ---------------- building blocks (lon, lat)
DANUBE_S = [(22.40, 44.68), (22.66, 44.60), (22.86, 44.00), (23.24, 43.80), (23.96, 43.71), (24.90, 43.67), (25.35, 43.59), (25.97, 43.82), (26.62, 44.02), (27.26, 44.09), (27.92, 44.33), (27.92, 44.69), (27.94, 45.24), (28.05, 45.38), (28.46, 45.24), (28.80, 45.15), (29.62, 44.86)]
rum51 = Polygon([(22.40, 44.68), (22.15, 43.9), (21.95, 43.3), (21.75, 42.75), (21.4, 42.3), (20.75, 42.0), (20.45, 41.6), (20.1, 41.1), (19.75, 40.7), (19.2, 40.45), (19.5, 39.9), (20.3, 39.2), (20.7, 38.9), (21.3, 38.6), (22.3, 38.5), (22.8, 38.55), (23.1, 38.65), (24.5, 39.2), (25.5, 40.2), (26.2, 40.3), (27.5, 40.7), (28.5, 40.85), (29.9, 41.4), (29.9, 43.0), (30.2, 44.8)] + DANUBE_S[::-1])
cpl = Polygon([(28.5, 40.9), (29.12, 40.95), (29.2, 41.3), (28.6, 41.35), (28.45, 41.1)])
ana_big = Polygon([(26.15, 39.9), (26.62, 40.4), (27.6, 40.45), (29.0, 40.95), (29.25, 41.3), (31.0, 41.5), (32.6, 42.1), (35.6, 42.4), (37.6, 41.5), (38.0, 41.1), (38.2, 40.5), (38.1, 40.0), (38.3, 39.6), (37.9, 39.0), (37.6, 38.75), (36.2, 38.62), (35.6, 38.3), (34.95, 37.55), (34.6, 36.9), (34.0, 36.0), (31.0, 36.45), (29.2, 36.5), (28.2, 36.75), (27.35, 36.95), (27.1, 37.6), (26.35, 38.2), (26.65, 38.9), (26.55, 39.5)])
karaman = P([(31.6, 38.5), (33.0, 39.2), (34.8, 38.9), (35.3, 38.0), (34.6, 37.0), (34.0, 36.15), (32.4, 36.05), (31.6, 36.7), (31.3, 37.6)])
candar = P([(32.6, 41.9), (32.4, 41.2), (33.3, 40.6), (34.6, 40.8), (35.5, 41.5), (35.7, 42.4), (33.0, 42.3)])
trebiz = P([(37.95, 41.06), (38.4, 40.82), (39.5, 40.66), (40.8, 40.88), (41.55, 41.3), (41.8, 41.9), (37.5, 41.8)])
ott51 = unary_union([rum51.difference(cpl), ana_big.difference(unary_union([karaman, candar, trebiz]))])
serbia = Polygon([(19.4, 44.86), (20.3, 44.78), (20.9, 44.70), (21.6, 44.70), (22.40, 44.68), (22.15, 43.9), (21.95, 43.3), (21.75, 42.75), (21.4, 42.3), (20.75, 42.0), (20.0, 42.4), (19.6, 43.0), (19.3, 43.6), (19.25, 44.3), (19.1, 44.9)])
herzeg = P([(17.2, 43.6), (18.1, 43.4), (19.0, 43.2), (19.2, 43.25), (18.9, 42.6), (18.2, 42.5), (17.5, 42.95), (17.1, 43.3)], 1).difference(serbia)
jajce = ell(17.27, 44.34, 38)
bosnia = P([(15.8, 45.2), (16.9, 45.25), (18.0, 45.15), (19.1, 44.95), (19.7, 44.9), (19.7, 43.3), (19.0, 43.2), (18.1, 43.4), (17.2, 43.6), (16.4, 44.2), (15.9, 44.7)], 1).difference(serbia).difference(herzeg).difference(jajce)
albania = P([(19.3, 42.25), (19.95, 42.6), (20.5, 42.5), (21.2, 42.1), (20.9, 41.3), (20.1, 41.0), (19.6, 40.5), (19.2, 40.9), (19.35, 41.8)], 1).difference(serbia).difference(rum51)
morea_all = P([(21.0, 38.45), (22.9, 38.2), (23.5, 37.6), (23.3, 36.3), (22.4, 36.25), (21.6, 36.6), (21.0, 37.6)], 1)
vforts = {'modon': ell(21.705, 36.819, 9), 'coron': ell(21.957, 36.796, 9), 'nauplia': ell(22.80, 37.57, 9), 'monemv': ell(23.06, 36.69, 8)}
attica = P([(22.3, 38.55), (23.1, 38.68), (24.3, 38.3), (24.0, 37.5), (23.0, 37.85), (22.4, 38.15)], 1)   # Duchy of Athens: 1456-1460 (geo3-check 1)
vcoast = {'kotor': ell(18.77, 42.42, 8), 'bar': ell(19.136, 42.097, 7), 'ulcinj': ell(19.21, 41.93, 7), 'durazzo': ell(19.45, 41.32, 9)}   # Venetian (geo3 3)
VC = unary_union(list(vcoast.values()))
albania = albania.difference(VC); herzeg = herzeg.difference(VC)
zeta = P([(18.75, 42.75), (19.3, 42.95), (19.75, 42.75), (19.95, 42.5), (19.6, 42.2), (19.35, 42.05), (19.1, 42.15), (18.85, 42.35)], 1).difference(herzeg).difference(albania).difference(serbia).difference(VC)   # Zeta: mostly Ottoman 1477-78 (geo3 2)
ragusa = ell(18.09, 42.65, 12)   # Republic of Ragusa, tributary (geo3 5)
euboea, lesbos = ISL(23.6, 38.6), ISL(26.3, 39.2)
crimea_s = P([(33.45, 44.38), (33.7, 44.72), (34.4, 44.92), (35.4, 45.17), (36.55, 45.5), (36.65, 45.3), (35.45, 44.97), (34.3, 44.52), (33.6, 44.35)], 1)
gains1 = {'g_cpl': cpl, 'g_serbia': serbia.difference(ell(20.457, 44.817, 10)), 'g_bosnia': bosnia, 'g_albania': albania,
          'g_morea': morea_all.difference(unary_union(list(vforts.values()))), 'g_attica': attica.difference(morea_all).difference(euboea), 'g_zeta': zeta,
          'g_karaman': karaman, 'g_candar': candar, 'g_trebiz': trebiz, 'g_euboea': euboea, 'g_lesbos': lesbos, 'g_crimeas': crimea_s}
CLOSE = lambda g: g.buffer(0.06).buffer(-0.06)
ott81 = CLOSE(unary_union([ott51] + list(gains1.values())))
gains2 = {'g_kilia': ell(29.27, 45.43, 22), 'g_akkerman': ell(30.35, 46.19, 22), 'g_herzeg': herzeg,
          'g_lepanto': ell(21.828, 38.392, 12), 'g_modon': vforts['modon'], 'g_coron': vforts['coron'], 'g_durazzo': vcoast['durazzo']}
ott12 = CLOSE(unary_union([ott81] + list(gains2.values())))
mamluk = Polygon([(25.0, 27.0), (25.0, 31.8), (32.0, 31.9), (34.0, 31.7), (34.75, 32.9), (35.55, 35.4), (35.85, 36.6), (34.6, 36.55), (34.6, 36.9), (34.95, 37.55), (35.8, 37.85), (36.45, 37.45), (37.3, 37.25), (37.4, 37.6), (37.9, 38.5), (38.6, 38.6), (38.9, 38.2), (38.3, 37.4), (38.3, 36.9), (38.6, 36.2), (39.0, 35.95), (40.1, 35.3), (40.6, 34.6), (39.0, 33.0), (37.8, 31.0), (37.2, 29.8), (35.2, 27.8), (34.6, 27.0)])
dulkadir = P([(35.8, 37.85), (36.45, 37.45), (37.3, 37.25), (37.4, 37.6), (37.9, 38.5), (37.2, 38.75), (36.2, 38.6), (35.6, 38.3)], 1)
ramazan = P([(35.05, 36.75), (35.0, 37.3), (35.4, 37.6), (35.9, 37.4), (35.85, 36.85), (35.5, 36.6)], 1)   # Adana: Ramadanid buffer state
mamluk = mamluk.difference(ramazan)
se_ana = Polygon([(37.5, 41.0), (40.9, 41.0), (41.3, 40.4), (41.8, 39.6), (42.6, 38.8), (43.0, 37.6), (42.2, 37.15), (41.0, 36.9), (40.6, 36.4), (39.0, 35.95), (38.6, 36.2), (38.3, 36.9), (38.3, 37.4), (37.6, 38.0), (37.4, 38.6)]).difference(ott12).difference(mamluk).difference(dulkadir)
gains3 = {'g_seana': se_ana, 'g_mamluk': mamluk}
ott20 = unary_union([ott12] + list(gains3.values())).difference(dulkadir)
# islands: Ottoman only where stated (Euboea 1470, Lesbos 1462); every other island is removed from the Ottoman shapes
keep = lambda g, isl: g.difference(NONMAIN).union(unary_union(isl).intersection(g.buffer(0.01)) if isl else Polygon())
ott51 = ott51.difference(NONMAIN)
ott81 = keep(ott81, [euboea, lesbos]); ott12 = keep(ott12, [euboea, lesbos]); ott20 = keep(ott20, [euboea, lesbos, ISL(33.2, 35.1).intersection(Polygon())])
for d in (gains1, gains2, gains3):
    for k in list(d):
        if k not in ('g_euboea', 'g_lesbos'): d[k] = d[k].difference(NONMAIN)
# ---------------- neighbours
CARP = [(22.6, 45.1), (23.5, 45.45), (24.5, 45.6), (25.3, 45.45), (26.0, 45.55), (26.6, 45.78)]
wallachia = Polygon([(22.43, 44.72), (22.70, 44.64), (22.90, 44.03), (23.24, 43.86), (23.96, 43.76), (24.90, 43.72), (25.35, 43.65), (25.97, 43.88), (26.62, 44.08), (27.26, 44.15), (27.85, 44.4), (27.86, 44.7), (27.88, 45.24), (27.6, 45.5), (27.2, 45.72), (26.6, 45.78)] + CARP[::-1] + [(22.45, 44.85)])
moldavia = Polygon([(26.6, 45.78), (27.2, 45.72), (27.6, 45.5), (27.95, 45.42), (28.8, 45.32), (29.7, 45.25), (30.6, 46.1), (30.1, 46.9), (29.6, 47.8), (28.2, 48.4), (26.6, 48.4), (25.2, 47.95), (25.6, 47.0), (26.3, 46.2)])
crimea_k = Polygon([(32.5, 45.4), (33.5, 46.2), (34.5, 47.2), (36.0, 47.35), (37.5, 46.9), (36.9, 45.45), (35.5, 45.25), (33.6, 44.55), (32.5, 45.2)]).difference(crimea_s)
hungary = Polygon([(13.6, 46.6), (14.2, 45.55), (15.0, 45.05), (15.6, 44.55), (15.9, 44.7), (16.9, 45.27), (18.0, 45.17), (19.1, 44.97), (19.4, 44.88), (20.3, 44.80), (20.9, 44.73), (21.6, 44.73), (22.43, 44.72), (22.45, 44.85)] + CARP + [(26.3, 46.2), (25.6, 47.0), (25.2, 47.95), (24.0, 48.3), (17.0, 48.3), (16.5, 47.5), (16.1, 46.8)]).union(jajce)
venice = {'v_dalmatia': P([(14.9, 44.62), (15.6, 44.0), (16.3, 43.5), (17.0, 43.22), (17.12, 43.42), (16.5, 43.68), (15.9, 44.08), (15.3, 44.48)], 1),
          'v_crete': ISL(24.9, 35.25), 'v_corfu': ISL(19.85, 39.6), 'v_cyprus': ISL(33.2, 35.1), 'v_lepanto': ell(21.828, 38.392, 12)} | {('v_' + k): v for k, v in vforts.items()} | {('v_' + k): v for k, v in vcoast.items()}
rhodes = ISL(28.0, 36.2)
akkoy = P([(38.4, 40.82), (40.5, 40.6), (43.5, 40.3), (48.6, 39.6), (48.6, 33.3), (42.0, 33.3), (40.6, 34.6), (40.1, 35.3), (39.0, 35.95), (38.6, 36.2), (38.3, 36.9), (38.3, 37.4), (38.9, 38.2), (38.6, 38.6), (38.3, 39.0), (38.3, 39.6), (38.1, 40.0), (38.2, 40.5)], 1)
safav12 = akkoy
safav20 = P([(41.8, 39.6), (43.5, 40.3), (48.6, 39.6), (48.6, 33.3), (44.5, 33.3), (43.6, 35.5), (43.0, 37.6), (42.6, 38.8)], 1)
byz = unary_union([cpl, morea_all.difference(unary_union(list(vforts.values())))]).difference(NONMAIN)
G = {'ott51': ott51, 'ott81': ott81, 'ott12': ott12, 'ott20': ott20, 'wallachia': wallachia, 'moldavia': moldavia, 'crimeak': crimea_k,
     'hungary': hungary, 'rhodes': rhodes, 'akkoy': akkoy, 'safav12': safav12, 'safav20': safav20, 'byz': byz,
     'mamluk': mamluk, 'dulkadir': dulkadir, 'ramazan': ramazan, 'jajce': jajce, 'ragusa': ragusa, 'teke': P([(29.5, 36.4), (29.4, 37.4), (30.6, 37.85), (31.8, 37.4), (31.6, 36.5)], 1)} | gains1 | gains2 | gains3 | venice
Z = lambda k, r: (G[k], r, 20, 0)
S = lambda k, r: (G[k], r, 0, 1)
VEN = lambda r, skip=(): [S(k, r) for k in venice if k not in ('v_cyprus',) + tuple(skip)]
STEPS = [
 [Z('akkoy', 'enemy'), Z('mamluk', 'neutral'), Z('ramazan', 'neutral'), Z('dulkadir', 'neutral'), Z('moldavia', 'neutral'), Z('hungary', 'enemy'), S('jajce', 'enemy'), S('wallachia', 'vassal'), S('crimeak', 'vassal'), S('rhodes', 'enemy'), S('ragusa', 'neutral')] + VEN('enemy') +
 [S(k, 'gain') for k in gains1] + [S('ott51', 'core')],
 [Z('safav12', 'rival'), Z('mamluk', 'enemy'), Z('ramazan', 'neutral'), Z('dulkadir', 'neutral'), Z('moldavia', 'enemy'), Z('hungary', 'neutral'), S('jajce', 'neutral'), S('wallachia', 'vassal'), S('crimeak', 'vassal'), S('rhodes', 'neutral'), S('ragusa', 'neutral'), S('v_cyprus', 'enemy')] + VEN('enemy', ('v_lepanto', 'v_modon', 'v_coron', 'v_durazzo')) +
 [S(k, 'gain') for k in gains2] + [S('ott81', 'core'), S('teke', 'crack')],
 [Z('safav20', 'enemy'), Z('moldavia', 'neutral'), Z('hungary', 'neutral'), S('jajce', 'neutral'), S('wallachia', 'vassal'), S('crimeak', 'vassal'), S('dulkadir', 'vassal'), S('ramazan', 'vassal'), S('rhodes', 'neutral'), S('ragusa', 'neutral'), S('v_cyprus', 'neutral')] + VEN('neutral', ('v_lepanto', 'v_modon', 'v_coron', 'v_durazzo')) +
 [S(k, 'gain') for k in gains3] + [S('ott12', 'core')],
]
out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, 'ovl')
for i, st in enumerate(STEPS): F.render(st, os.path.join(out, f'ott-{i}.webp'))
F.export_geo(G, os.path.join(out, 'ott-geo.json'), tol=0.03)
