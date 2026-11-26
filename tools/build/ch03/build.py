"""Assemble ch/03.js from the story fragments (s0..s3), geo.py (lines from the checked supplementary sheet)
and head.py (chapter header and LADDER).
usage (from the repo root): python3 tools/build/ch03/build.py ch/03.js
Every fact in the fragments comes from the checked fact sheets (facts/ch03-*.md)."""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
def load(name):
    g = {}; exec(open(os.path.join(D, name), encoding='utf-8').read(), g); return g
NSTORIES = 2
ns = [load(f's{i}.py') for i in range(NSTORIES)]
geo, head = load('geo.py'), load('head.py')
STORIES, PLACES, PINFO, PEOPLE = [], {}, {}, []
for si, g in enumerate(ns):
    S = g['S']
    for k, st in enumerate(S['steps']):
        m = st['map']; L = m.get('lines', [])
        if isinstance(L, str): L = g[L] if L in g else geo[L]
        m['lines'] = list(L) + geo['EXTRA'].get((si, k), [])
        for key in [x for x, v in list(m.items()) if v in ([], {}) and x not in ('show', 'lg')]: del m[key]
    STORIES.append(S)
    for pid, p in g['PLACES'].items():
        assert pid not in PLACES, pid; PLACES[pid] = p
    for pid, (n, d, src) in g['P'].items():
        if pid in PINFO and (PINFO[pid]['n'], PINFO[pid]['d']) != (n, d): raise SystemExit(f'PINFO id clash: {pid}')
        PINFO[pid] = {'n': n, 'd': d, 'src': src}
    PEOPLE.append({'g': S['title'], 's': si, 'list': [{'n': n, 'y': y, 'tag': [t, ''], 'nt': nt, 'also': '', 'at': at} for (n, y, t, nt, at) in g['PEOPLE']]})
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
src = ['/* אטלס הדיונים · ספר ראשון, פרק 3: נתוני הפרק. נבנה עם tools/build/ch03/build.py מתוך הקטעים שבתיקייה.',
 '   תיקי העובדות: facts/ch03-tarquins.md, facts/ch03-secession.md, facts/ch03-geo.md (כל אחד עם דוח בודק בנספח).',
 '   העמודים לפי האפיון בפרויקט. ציטוט בעברית רק מנוסח שלם שמופיע בסיכומי הפרויקט; כל השאר "תרגום חופשי" מהאיטלקית. */',
 'ATLAS.add(3, (function(){',
 'const PLACES = ' + J(PLACES) + ';',
 'const STORIES = ' + json.dumps(STORIES, ensure_ascii=False, indent=1) + ';',
 'const PEOPLE = ' + json.dumps(PEOPLE, ensure_ascii=False, indent=1) + ';',
 'const LADDER = ' + json.dumps(head['LADDER'], ensure_ascii=False, indent=1) + ';',
 'const GEOM = {};',
 'const ENT = {};',
 'const PINFO = ' + json.dumps(PINFO, ensure_ascii=False, indent=1) + ';',
 'return Object.assign(' + J(head['H']) + ', {PLACES, STORIES, PEOPLE, LADDER, GEOM, ENT, PINFO});',
 '})());', '']
open(OUT, 'w', encoding='utf-8').write('\n'.join(src))
print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB;', sum(len(s['steps']) for s in STORIES), 'steps;', len(PINFO), 'places')
