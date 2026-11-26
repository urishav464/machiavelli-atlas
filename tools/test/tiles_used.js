// Which map files does the phone actually load? Walks every chapter's overview and every step of every story
// at phone size, and prints the tile/overlay paths that were requested. Use it to find files the artifact can drop
// (the artifact holds at most 511 files; see AGENTS.md, "פרסום").
// usage: node tools/test/tiles_used.js <chapters, comma-separated> > used.txt   (run tools/test/serve.sh first)
const { chromium } = require('playwright');
(async () => {
  const chaps = (process.argv[2] || '0,1,2,19').split(',');
  const b = await chromium.launch();
  const used = new Set();
  for (const chap of chaps) {
    const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
    p.on('request', r => { const m = r.url().match(/localhost:\d+\/((?:t|tl|tf|tv|td|ta|ovl|base)\/[^?#]+)/); if (m) used.add(m[1]); });
    await p.goto('http://localhost:8765/test.html?draft#ch-' + chap); await p.waitForTimeout(2500);
    const n = (await p.$$('[data-open]')).length;
    for (let s = 0; s < n; s++) {
      await p.goto('http://localhost:8765/test.html?draft#ch-' + chap); await p.waitForTimeout(1500);
      await p.click(`[data-open="${s}"]`); await p.waitForTimeout(2600);
      for (let i = 0; i < 12; i++) {
        const prog = await p.$eval('.progress span', e => e.textContent).catch(() => '');
        const m = prog.match(/(\d+)\D+(\d+)/); if (m && +m[1] >= +m[2]) break;
        const nx = await p.$('[data-next]'); if (!nx) break; await nx.click(); await p.waitForTimeout(2600);
      }
    }
    await p.close();
  }
  console.log([...used].sort().join('\n'));
  await b.close();
})();
