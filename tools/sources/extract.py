"""Extract a Perseus TEI text into one line per section: "book.chapter.section text".
usage: python3 tools/sources/extract.py <file.xml> [book] > out.txt
  - Livy / Dionysius: give the book number.  Plutarch lives: omit it.
Footnotes are dropped without losing the text that follows them (lxml .tail trap)."""
import sys, re
from lxml import etree
ns = {'t': 'http://www.tei-c.org/ns/1.0'}
f = sys.argv[1]; book = sys.argv[2] if len(sys.argv) > 2 else None
t = etree.parse(f)
for n in t.xpath('//t:note', namespaces=ns):
    p = n.getparent(); tail = n.tail or ''; prev = n.getprevious()
    if prev is not None: prev.tail = (prev.tail or '') + tail
    else: p.text = (p.text or '') + tail
    p.remove(n)
root = t.xpath(f"//t:div[@subtype='book' and @n='{book}']", namespaces=ns)[0] if book else t.getroot()
for ch in root.xpath(".//t:div[@subtype='chapter']", namespaces=ns):
    secs = ch.xpath("t:div[@subtype='section']", namespaces=ns) or [ch]
    for s in secs:
        txt = re.sub(r'\s+', ' ', ''.join(s.itertext())).strip()
        ref = '.'.join(x for x in (book, ch.get('n'), s.get('n') if s is not ch else None) if x)
        print(ref, txt)
