"""Assemble ch/01.js from the four story fragments (s0..s3), geo.py and the Ottoman pieces of ch/19.js.
usage (from the repo root):
  node tools/build/ch01/ott_from_ch19.js ch/19.js ott12,g_seana,g_mamluk,dulkadir,ramazan,v_cyprus,rhodes > tools/build/ch01/ott.json
  python3 tools/build/ch01/build.py ch/01.js
Every fact in the fragments comes from the checked fact sheets (facts/ch01-*.md)."""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); OUT = sys.argv[1]
ns = []
for i in range(4):
    g = {}; exec(open(os.path.join(D, f's{i}.py'), encoding='utf-8').read(), g); ns.append(g)
geo = {}; exec(open(os.path.join(D, 'geo.py'), encoding='utf-8').read(), geo)
ott = json.load(open(os.path.join(D, 'ott.json'), encoding='utf-8'))
special = {'SELIM': ott['SELIM'], 'GEO_EGYPT': geo['GEO_EGYPT'], 'GEO_ALEX': geo['GEO_ALEX']}
STORIES, PLACES, PINFO, PEOPLE = [], {}, {}, []
for si, g in enumerate(ns):
    S = g['S']
    for k, st in enumerate(S['steps']):
        m = st['map']; L = m.get('lines', [])
        if isinstance(L, str): L = g[L] if L in g else special[L]
        L = list(L) + geo['EXTRA'].get((si, k), [])
        m['lines'] = L
        for key in [x for x, v in list(m.items()) if v in ([], {}) and x not in ('show', 'lg')]: del m[key]
    STORIES.append(S)
    for pid, p in g['PLACES'].items():
        assert pid not in PLACES, pid; PLACES[pid] = p
    for pid, (n, d, src) in g['P'].items():
        if pid in PINFO and (PINFO[pid]['n'], PINFO[pid]['d']) != (n, d): raise SystemExit(f'PINFO id clash: {pid}')
        PINFO[pid] = {'n': n, 'd': d, 'src': src}
    PEOPLE.append({'g': S['title'], 's': si, 'list': [{'n': n, 'y': y, 'tag': [t, ''], 'nt': nt, 'also': '', 'at': at} for (n, y, t, nt, at) in g['PEOPLE']]})
LADDER = [
 {'role':['פתיחה',''], 'pg':'עמ׳ 5', 'h':'ילידים או זרים', 'q':'"o dagli uomini natii del luogo... o dai forestieri": או בידי ילידי המקום, או בידי זרים', 'tr':True, 'at':[0,0]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 5', 'h':'ילידים מתאחדים: אתונה וונציה', 'q':'"sotto l\'autorità di Teseo": תחת סמכותו של תזאוס', 'tr':True, 'at':[0,1]},
 {'role':['הבחנה','rule'], 'pg':'עמ׳ 6', 'h':'זרים: חופשיים או תלויים', 'q':'"o da uomini liberi o che dependono da altri": מאנשים חופשיים, או מאנשים שתלויים באחרים', 'tr':True, 'at':[1,1]},
 {'role':['הכלל','rule'], 'pg':'עמ׳ 6', 'h':'לעיר תלויה אין עתיד גדול', 'q':'"rade volte occorre che le facciano processi grandi": רק לעתים רחוקות הן מתקדמות הרבה', 'tr':True, 'at':[1,2]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 6', 'h':'וגם פירנצה', 'q':'"Simile a queste fu l\'edificazione di Firenze": דומה לאלה היה ייסודה של פירנצה', 'tr':True, 'at':[1,3]},
 {'role':['הניגוד','rule'], 'pg':'עמ׳ 6', 'h':'החופשיים: משה ואינאס', 'q':'"si conosce la virtù dello edificatore, e la fortuna dello edificato": ניכרת המידה הטובה של המייסד והפורטונה של המיוסד', 'tr':True, 'at':[2,0]},
 {'role':['השאלה','rule'], 'pg':'עמ׳ 7', 'h':'מקום עקר או מקום פורה', 'q':'"porsi in luogo fertile, quando quella fertilità con le leggi infra i debiti termini si ristringa": מקום פורה, כשהחוקים מגבילים את הפוריות בגבולות הראויים', 'tr':True, 'at':[3,1]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 7', 'h':'מצרים והממלוכים', 'q':'הסדר של הממלוכים ושל צבאם, לפני שחוסלו בידי סלים התורכי הגדול', 'at':[3,3]},
 {'role':['ראיה','evid'], 'pg':'עמ׳ 7–8', 'h':'אלכסנדר עוזב את אתוס', 'q':'"domandandolo Alessandro di quello che quelli abitatori viverebbero": אלכסנדר שאל ממה יחיו התושבים', 'tr':True, 'at':[1,0]},
 {'role':['חזרה לרומא',''], 'pg':'עמ׳ 8', 'h':'ורומא?', 'q':'"la vedrà avere principio libero, sanza dependere da alcuno": יראה שהייתה לה ראשית חופשית, בלי תלות באיש', 'tr':True, 'at':[2,4]},
]
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
H = {'n':1, 'eyebrow':'ספר ראשון, פרק 1 · עמ׳ 5–8', 'title':'כיצד נוצרו ערים',
 'full':'"מה היו, באופן כללי, הראשית של כל עיר, ומה הייתה הראשית של רומא" (תרגום חופשי)',
 'oneline':'מקיאוולי ממיין ערים לפי מי שבנה אותן: ילידים או זרים, חופשיים או תלויים. ובכל ייסוד הוא בודק שני דברים: את בחירת המקום ואת סידור החוקים.',
 'intro':'ארבעה סיפורים מהפרק, כולם על המפה. בחרו סיפור כדי ללכת בו צעד אחר צעד.',
 'question':'מקיאוולי אומר שלעיר בלי ראשית חופשית רק לעתים רחוקות יש עתיד גדול. אבל אלכסנדריה נעשתה "ראשונה בעולם", ופירנצה שלו הייתה מושבה. האם הכלל עומד במבחן המפה? ולמה חשוב לו כל כך שלרומא הייתה ראשית חופשית?',
 'next':'ממשיך בפרק 2: סוגי הרפובליקות.',
 'overviewBounds':[[28.5,10.5],[46.5,36.5]], 'hideOther':True}
src = ['/* אטלס הדיונים · ספר ראשון, פרק 1: נתוני הפרק. נבנה עם tools/build/ch01/build.py מתוך הקטעים שבתיקייה.',
 '   תיקי העובדות: facts/ch01-athens-venice.md, facts/ch01-alexandria-florence.md, facts/ch01-moses-aeneas.md, facts/ch01-ragusa-egypt.md, facts/ch01-geo.md (כל אחד עם דוח בודק בנספח).',
 '   העמודים לפי האפיון בפרויקט. ציטוט בעברית רק מנוסח שלם שמופיע בסיכומי הפרויקט; כל השאר "תרגום חופשי" מהאיטלקית. */',
 'ATLAS.add(1, (function(){',
 'const PLACES = ' + J(PLACES) + ';',
 'const STORIES = ' + json.dumps(STORIES, ensure_ascii=False, indent=1) + ';',
 'const PEOPLE = ' + json.dumps(PEOPLE, ensure_ascii=False, indent=1) + ';',
 'const LADDER = ' + json.dumps(LADDER, ensure_ascii=False, indent=1) + ';',
 'const GEOM = {};',
 'Object.assign(GEOM, /*ott*/' + J(ott['GEOM']) + ');',
 'const ENT = ' + json.dumps(ott['ENT'], ensure_ascii=False, indent=1) + ';',
 'const PINFO = ' + json.dumps(PINFO, ensure_ascii=False, indent=1) + ';',
 'return Object.assign(' + J(H) + ', {PLACES, STORIES, PEOPLE, LADDER, GEOM, ENT, PINFO});',
 '})());', '']
open(OUT, 'w', encoding='utf-8').write('\n'.join(src))
print('wrote', OUT, os.path.getsize(OUT) // 1024, 'KB;', sum(len(s['steps']) for s in STORIES), 'steps;', len(PINFO), 'places')
