// Pull the Ottoman pieces chapter 1 reuses from ch/19.js: Selim's 1516 and 1517 lines, and GEOM/ENT for the given ids.
const fs=require('fs'); let D; global.ATLAS={add:(n,o)=>{D=o}};
eval(fs.readFileSync(process.argv[2],'utf8'));
const ids=process.argv[3].split(',');
let selim=[]; D.STORIES.forEach(st=>st.steps.forEach(s=>{ const m=s.map||{}; if(m.ovl==='ovl/ott-2.webp') selim=(m.lines||[]).filter(l=>l.lbl==='1516'||l.lbl==='1517'); }));
const G={},E={}; ids.forEach(i=>{ if(D.GEOM[i]) G[i]=D.GEOM[i]; if(D.ENT[i]) E[i]=D.ENT[i]; });
console.log(JSON.stringify({SELIM:selim,GEOM:G,ENT:E}));
