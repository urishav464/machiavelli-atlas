// Cross-check every chapter's data: each id a step uses exists (ENT, GEOM, PINFO, LINE, KIND, ROLE, PLACES), every line has a card.
// usage: node tools/test/check_data.js            (checks index.html + all ch/NN.js listed in AVAIL)
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '../..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const i = html.indexOf('<script>\nconst RIVERS'), j = html.indexOf('</script>', i);
if (i < 0) throw new Error('page script not found');
const src = html.slice(i + 8, j);
const head = src.slice(0, src.indexOf('/* ---------- map ---------- */'));
const k0 = src.indexOf('const KIND = {'), k1 = src.indexOf('function smoothPts');
const S = new Function('location', head + src.slice(k0, k1) + ';return {CH,ATLAS,AVAIL,ROLE,KIND,LINE,CHAPTERS};')({search:'?draft'});
let bad = 0;
for (const n of S.AVAIL) {
  const f = path.join(root, 'ch', String(n).padStart(2, '0') + '.js');
  vm.runInNewContext(fs.readFileSync(f, 'utf8'), { ATLAS: S.ATLAS }, { filename: f });
  const D = S.CH[n], miss = [];
  if (!D) { console.log('ch', n, 'did not register'); bad++; continue; }
  for (const key of ['eyebrow', 'title', 'full', 'oneline', 'intro']) if (!D[key]) miss.push(['header', key]);
  D.STORIES.forEach((s, si) => s.steps.forEach((st, k) => { const m = st.map || {};
    Object.entries(m.ents || {}).forEach(([id, r]) => { if (!D.ENT[id]) miss.push(['ENT', si, k, id]); if (!D.GEOM[id]) miss.push(['GEOM', si, k, id]); if (!S.ROLE[r]) miss.push(['ROLE', r]); });
    Object.keys(m.say || {}).forEach(id => { if (!(m.ents || {})[id]) miss.push(['say-not-in-ents', si, k, id]); });
    (m.pins || []).forEach(p => { if (p[3] && !D.PINFO[p[3]]) miss.push(['PINFO', si, k, p[3]]); });
    (m.zones || []).forEach(z => { if (z[4] && !D.PINFO[z[4]]) miss.push(['PINFO', si, k, z[4]]); });
    (m.lines || []).forEach(l => { if (!S.LINE[l.k]) miss.push(['LINE', l.k]); if (!l.info) miss.push(['line-without-card', si, k, l.lbl || '']); });
    (m.lg || []).forEach(x => { if (!S.KIND[x]) miss.push(['KIND', x]); });
    (m.show || []).forEach(id => { if (!D.PLACES[id]) miss.push(['PLACE', id]); });
    (m.tl || []).forEach(t => { if (!S.KIND[t[3]]) miss.push(['label-role', si, k, t[3]]); });
  }));
  Object.values(D.PLACES).forEach(p => { if (!D.STORIES[p.s]) miss.push(['PLACE.s', p.n]); });
  (D.overview || []).forEach(id => { if (!D.PLACES[id]) miss.push(['overview', id]); });
  D.PEOPLE.forEach(g => g.list.forEach(p => { const [s, k] = p.at; if (!D.STORIES[s] || !D.STORIES[s].steps[k]) miss.push(['PEOPLE.at', p.n]); }));
  D.LADDER.forEach(r => { if (r.at && !(D.STORIES[r.at[0]] && D.STORIES[r.at[0]].steps[r.at[1]])) miss.push(['LADDER.at', r.h]); });
  console.log(miss.length ? `ch ${n} MISSING ${JSON.stringify(miss)}` : `ch ${n} OK: ${D.STORIES.map(s => s.steps.length).join('+')} steps`);
  bad += miss.length;
}
process.exit(bad ? 1 : 0);
