// Phone screenshots (390x844) of every step of one story, plus tap tests.
// usage: node tools/test/shots.js <storyIndex> [outDir]     (run tools/test/serve.sh first; re-run serve.sh after editing index.html)
// Prints JS errors (a failed Google-Fonts request is normal in the container). Then LOOK at every image:
// labels overlapping, arrows pointing the right way, territories on the correct bank/side, cards readable.
const { chromium } = require('playwright');
(async () => {
  const story = process.argv[2] || '0', out = process.argv[3] || '.';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 1, isMobile: true, hasTouch: true });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error' && !/ERR_TUNNEL|fonts/.test(m.text())) errs.push(m.text()); });
  await p.goto('http://localhost:8765/test.html'); await p.waitForTimeout(1200);
  await p.click(`[data-open="${story}"]`); await p.waitForTimeout(2600);
  for (let i = 0; i < 12; i++) {
    await p.screenshot({ path: `${out}/s${story}-step${i}.png` });
    // tap every line label, one card per screenshot
    const labels = await p.$$('.llabel.tapl');
    for (let k = 0; k < labels.length; k++) {
      await labels[k].click({ force: true }); await p.waitForTimeout(250);
      await p.screenshot({ path: `${out}/s${story}-step${i}-line${k}.png` });
      await p.click('.ic-x').catch(() => {});
    }
    const n = await p.$('[data-next]'); if (!n) break; await n.click(); await p.waitForTimeout(2600);
  }
  console.log('errors:', JSON.stringify(errs)); await b.close();
})();
