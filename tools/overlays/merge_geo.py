"""Merge a tap-geometry JSON (from Frame.export_geo) into index.html as one line:
    Object.assign(GEOM, /*<tag>*/{...});
Re-running replaces the line with the same tag, so overlays can be re-rendered freely.
usage: python3 tools/overlays/merge_geo.py <tag> <geo.json> <ch/NN.js>   (the chapter data file that owns the story)"""
import sys, os, json
tag, src = sys.argv[1], sys.argv[2]
page = sys.argv[3]
geo = json.load(open(src))
line = 'Object.assign(GEOM, /*%s*/%s);' % (tag, json.dumps(geo, separators=(',', ':'), ensure_ascii=False))
L = open(page, encoding='utf-8').read().split('\n')
hit = [i for i, l in enumerate(L) if l.startswith('Object.assign(GEOM, /*%s*/' % tag)]
if hit: L[hit[0]] = line
else:
    at = max(i for i, l in enumerate(L) if l.startswith('const GEOM = ') or l.startswith('Object.assign(GEOM,'))
    L.insert(at + 1, line)
open(page, 'w', encoding='utf-8').write('\n'.join(L))
print(tag, len(geo), 'shapes,', len(line) // 1024, 'KB ->', page)
