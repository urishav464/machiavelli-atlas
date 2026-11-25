"""Look up ancient places in the Pleiades gazetteer (local CSV from get_sources.sh).
usage: python3 tools/sources/pleiades.py Veii Fidenae "Alba Longa"
Prints id, title, lat/lon, location precision, description. "rough" or empty coordinates = location uncertain:
say so on the map (decision of 2026-11-25: unlocated places appear only in text, never as a point)."""
import csv, os, sys, re
P = os.path.join(os.environ.get('ATLAS_CACHE', os.path.expanduser('~/.atlas-cache')), 'src', 'pleiades-places.csv')
rows = list(csv.DictReader(open(P, encoding='utf-8-sig')))
for q in sys.argv[1:]:
    hits = [r for r in rows if re.search(r'\b' + re.escape(q), r['title'], re.I)][:6]
    if not hits: print(f'{q}: not found'); continue
    for r in hits:
        print(f"{q:14}| {r['id']:>10} | {r['title'][:38]:38} | {str(r['representative_latitude'])[:8]:>8},{str(r['representative_longitude'])[:8]:<8} | {r['location_precision'] or '-':7} | {r['description'][:120]}")
