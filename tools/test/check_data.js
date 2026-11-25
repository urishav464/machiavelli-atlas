// Cross-check the page data: every id used in a step exists (ENT, GEOM, ROLE, PINFO, LINE, KIND, PLACES).
// usage: node tools/test/check_data.js [index.html]
const fs = require('fs');
const html = fs.readFileSync(process.argv[2] || require('path').join(__dirname, '../../index.html'), 'utf8');
const i = html.indexOf('<script>\nconst PLACES'), j = html.indexOf('</script>', i);
const src = html.slice(i + 8, j), cut = src.indexOf('/* ---------- map ---------- */');
const k0 = src.indexOf('const KIND = {'), k1 = src.indexOf('function smoothPts');   // KIND and LINE live after the map code
const D = new Function(src.slice(0, cut) + src.slice(k0, k1) + ';return {PLACES,STORIES,PEOPLE,ENT,PINFO,GEOM,ROLE,KIND,LINE};')();
const miss = [];
D.STORIES.forEach((s, si) => s.steps.forEach((st, k) => { const m = st.map || {};
  Object.entries(m.ents || {}).forEach(([id, r]) => { if (!D.ENT[id]) miss.push(['ENT', si, k, id]); if (!D.GEOM[id]) miss.push(['GEOM', si, k, id]); if (!D.ROLE[r]) miss.push(['ROLE', r]); });
  Object.keys(m.say || {}).forEach(id => { if (!(m.ents || {})[id]) miss.push(['say-not-in-ents', si, k, id]); });
  (m.pins || []).forEach(p => { if (p[3] && !D.PINFO[p[3]]) miss.push(['PINFO', si, k, p[3]]); });
  (m.lines || []).forEach(l => { if (!D.LINE[l.k]) miss.push(['LINE', l.k]); if (!l.info) miss.push(['line-without-card', si, k, l.lbl || '']); });
  (m.lg || []).forEach(x => { if (!D.KIND[x]) miss.push(['KIND', x]); });
  (m.show || []).forEach(id => { if (!D.PLACES[id]) miss.push(['PLACE', id]); });
  (m.tl || []).forEach(t => { if (!D.KIND[t[3]]) miss.push(['label-role', si, k, t[3]]); });
}));
D.PEOPLE.forEach(g => g.list.forEach(p => { const [s, k] = p.at; if (!D.STORIES[s] || !D.STORIES[s].steps[k]) miss.push(['PEOPLE.at', p.n]); }));
console.log(miss.length ? 'MISSING ' + JSON.stringify(miss) : 'data OK: ' + D.STORIES.map(s => s.steps.length).join('+') + ' steps');
process.exit(miss.length ? 1 : 0);
