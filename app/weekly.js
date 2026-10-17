/* Week-by-lagna page: renders engine output as-is; no client-side astrology. */
const SIGNS=['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces'];
const SIGNS_TA={Aries:'மேஷம்',Taurus:'ரிஷபம்',Gemini:'மிதுனம்',Cancer:'கடகம்',Leo:'சிம்மம்',Virgo:'கன்னி',Libra:'துலாம்',Scorpio:'விருச்சிகம்',Sagittarius:'தனுசு',Capricorn:'மகரம்',Aquarius:'கும்பம்',Pisces:'மீனம்'};
const PLANETS=['Sun','Moon','Mars','Mercury','Jupiter','Venus','Saturn','Rahu','Ketu'];
const PLANETS_TA={Sun:'சூரியன்',Moon:'சந்திரன்',Mars:'செவ்வாய்',Mercury:'புதன்',Jupiter:'குரு',Venus:'சுக்கிரன்',Saturn:'சனி',Rahu:'ராகு',Ketu:'கேது'};
const WD=['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
const cache=new Map();
let weekAnchor=istToday(), lagna=null, lastReport=null, lastMoon='';

function istToday(){return new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Kolkata',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());}
function shiftWeek(days){const d=new Date(weekAnchor+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+days);weekAnchor=d.toISOString().slice(0,10);}
function fmtDay(iso){const[y,m,dd]=iso.split('-').map(Number);return `${dd} ${['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][m-1]} ${y}`;}
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}
function esc(s){return String(s);}

function buildControls(){
 const grid=document.querySelector('#lagna-grid');
 SIGNS.forEach(s=>{const b=el('button');b.type='button';b.setAttribute('aria-pressed','false');
  b.textContent=`${s} · ${SIGNS_TA[s]}`;
  b.addEventListener('click',()=>{lagna=s;grid.querySelectorAll('button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));if(lastReport)compute();});
  grid.append(b);});
 const moon=document.querySelector('#moon-sign');
 SIGNS.forEach(s=>{const o=el('option');o.value=s;o.textContent=`${s} · ${SIGNS_TA[s]}`;moon.append(o);});
 moon.addEventListener('change',()=>{if(lastReport)compute();});
 document.querySelector('#prev-week').addEventListener('click',()=>{shiftWeek(-7);compute();});
 document.querySelector('#this-week').addEventListener('click',()=>{weekAnchor=istToday();compute();});
 document.querySelector('#next-week').addEventListener('click',()=>{shiftWeek(7);compute();});
 document.querySelector('#compute').addEventListener('click',compute);
}

async function compute(){
 const err=document.querySelector('#error');err.hidden=true;
 if(!lagna){err.textContent='Choose a lagna first.';err.hidden=false;return;}
 const moon=document.querySelector('#moon-sign').value;lastMoon=moon;
 const body={week_of:weekAnchor,lagna};if(moon)body.moon_sign=moon;
 const key=JSON.stringify(body);
 const ws=document.querySelector('#workspace');ws.setAttribute('aria-busy','true');
 document.querySelector('#compute').disabled=true;
 try{
  if(!cache.has(key)){
   const res=await fetch('/api/weekly',{method:'POST',headers:{'Content-Type':'application/json'},body:key,signal:AbortSignal.timeout(30000)});
   const data=await res.json().catch(()=>({}));
   if(!res.ok)throw new Error(data.error||'Calculation is unavailable. No result has been generated.');
   cache.set(key,data);
  }
  render(cache.get(key));
 }catch(e){err.textContent=e.message||'Calculation is unavailable. No result has been generated.';err.hidden=false;}
 finally{ws.setAttribute('aria-busy','false');document.querySelector('#compute').disabled=false;}
}

function render(r){
 lastReport=r;
 document.querySelector('#empty').hidden=true;
 const out=document.querySelector('#results');out.hidden=false;out.textContent='';
 document.querySelector('#week-label').textContent=`Weeks run Monday to Sunday, India time. Showing ${fmtDay(r.week_start_ist)} to ${fmtDay(addDays(r.week_end_ist_exclusive,-1))}.`;

 const head=el('div','result-head week-card');
 head.append(el('h2',null,`Week: ${fmtDay(r.week_start_ist)} – ${fmtDay(addDays(r.week_end_ist_exclusive,-1))}`));
 head.append(el('p',null,`Lagna: ${r.lagna} (${SIGNS_TA[r.lagna]})`+(r.moon_sign?` · Moon sign: ${r.moon_sign} (${SIGNS_TA[r.moon_sign]})`:'')));
 head.append(el('p',null,`${r.model}. ${r.sampling}`));
 out.append(head);

 if(r.events.length){
  const card=el('div','week-card');card.append(el('h3',null,'Sky events inside this week'));
  const ul=el('ul','event-list');
  for(const e of r.events){
   const li=el('li');
   if(e.kind==='sign_ingress')li.append(el('span',null,`${e.planet} moves ${e.from_sign} (${SIGNS_TA[e.from_sign]}) to ${e.to_sign} (${SIGNS_TA[e.to_sign]})`));
   else li.append(el('span',null,`${e.planet} ${e.kind==='station_retrograde'?'turns retrograde':'turns direct'}`));
   li.append(el('time',null,`${e.at_ist} (${e.precision})`));ul.append(li);
  }
  card.append(ul);out.append(card);
 }

 const planets=el('div','week-card');planets.append(el('h3',null,'Planets through the week, houses from your lagna'));
 for(const p of PLANETS){
  const v=r.placements[p];if(!v)continue;
  const row=el('div','planet-row');
  const headRow=el('div','head');
  const firstChange=v.signs_by_day.findIndex(s=>s!==v.signs_by_day[0]);
  let movement='';
  if(firstChange>0)movement=` ${v.signs_by_day[0]} (${SIGNS_TA[v.signs_by_day[0]]}) → ${v.signs_by_day[firstChange]} (${SIGNS_TA[v.signs_by_day[firstChange]]}) from ${fmtDay(r.day_dates_ist[Math.min(firstChange,6)])}`;
  else movement=` ${v.signs_by_day[0]} (${SIGNS_TA[v.signs_by_day[0]]}) all week`;
  const retroDays=v.retrograde_by_day.filter(Boolean).length;
  const retroText=retroDays===8?' · retrograde all week':retroDays>0?' · retrograde part of the week':'';
  headRow.append(el('strong',null,`${p}`));
  headRow.append(el('span',null,movement+retroText+(v.derived?' · derived from Rahu':'')));
  row.append(headRow);
  const strip=el('div','day-strip');
  for(let k=0;k<7;k++){
   const cell=el('div','day'+(k>0&&v.houses_from_lagna_by_day[k]!==v.houses_from_lagna_by_day[k-1]?' changed':''));
   cell.append(el('span',null,WD[k]));cell.append(el('strong',null,String(v.houses_from_lagna_by_day[k])));
   cell.title=`${r.day_dates_ist[k]}: ${v.signs_by_day[k]} ${v.degrees_in_sign_by_day[k]}°, house ${v.houses_from_lagna_by_day[k]} from ${r.lagna}`;
   strip.append(cell);
  }
  row.append(strip);planets.append(row);
 }
 planets.append(el('p','src-note','A house count is structure, not a verdict. Numbers count whole signs from the lagna you picked.'));
 out.append(planets);

 if(r.moon_sign){
  const card=el('div','week-card');card.append(el('h3',null,'Cited readings switched on by your Moon sign'));
  if(r.moon_findings&&r.moon_findings.length){
   for(const f of r.moon_findings){
    const d=el('div','finding');
    d.append(el('div','topic',f.topic.replaceAll('_',' ')));
    d.append(el('div',null,`${f.planet} ${f.house_from_moon}${ordinal(f.house_from_moon)} from your Moon: ${f.outcome}`));
    const days=f.active_days.length===7?'Active all 7 days':`Active ${f.active_days.length} of 7 days: ${f.active_days.map(a=>`${a.weekday.slice(0,3)} ${a.date.slice(8)}`).join(', ')}`;
    d.append(el('div','days',days));
    d.append(el('div','src',`Phaladeepika 1937, chapter ${f.source.chapter}, verse ${f.source.sloka}, PDF page ${f.source.pdf_page}, checked against the page image.`));
    card.append(d);
   }
  }else card.append(el('p','muted','No enabled cited transit rule matches this Moon sign in this week. Only four Phaladeepika chapter 26 rules are verified so far; an empty list is the honest answer, not a neutral week.'));
  card.append(el('p','src-note',r.moon_findings_notice||''));
  out.append(card);
 }else{
  const card=el('div','week-card');card.append(el('h3',null,'Cited readings stay off'));
  card.append(el('p','muted','Pick your Moon rasi above to switch on the four verified Phaladeepika chapter 26 transit readings. Without it this page shows structure only, on purpose.'));
  out.append(card);
 }

 const det=el('details','evidence week-card');det.append(el('summary',null,'Structure behind this page (lordship, aspects, timing conditions)'));
 const s=r.structural_factors_from_lagna;
 const tbl=el('table','houses');
 tbl.innerHTML='<thead><tr><th>House</th><th>Sign</th><th>Lord</th></tr></thead>';
 const tb=el('tbody');
 for(const h of s.lordships.houses){const tr=el('tr');tr.append(el('td',null,String(h.house)),el('td',null,`${h.sign} (${SIGNS_TA[h.sign]})`),el('td',null,`${h.lord}`));tb.append(tr);}
 tbl.append(tb);det.append(tbl);
 det.append(el('p','src-note','Sign ownership per Phaladeepika 1937, chapter I, verse 6, checked against the page image. Ownership and aspect are not strength or effect.'));
 const asp=el('div');
 for(const pf of s.planet_factors){
  const targets=pf.aspects.filter(t=>t.target_house_from_reference!==pf.house_from_reference);
  const txt=targets.length?`${pf.planet} in house ${pf.house_from_reference} aspects house${targets.length>1?'s':''} ${targets.map(t=>t.target_house_from_reference).join(', ')}.`:`${pf.planet} in house ${pf.house_from_reference}: ${pf.planet==='Rahu'?'node aspects are not enabled by the checked verse':'no aspect targets'}.`;
  asp.append(el('p','src-note',txt));
 }
 det.append(asp);
 const tp=el('div');
 for(const p of PLANETS){
  const ev=r.placements[p]&&r.placements[p].transit_phase_evidence;if(!ev)continue;
  let state;
  if(ev.status==='not_covered')state='not covered by the cited passage';
  else if(ev.throughout_passage)state='the cited timing condition applies throughout the passage';
  else if(ev.boundary_unresolved)state='sits on a third boundary; the cited timing condition is unresolved';
  else state=`the cited timing condition is ${ev.active_condition?'active':'not active'} (third ${ev.third_1_based} of the sign; the verse names third ${ev.specified_third_1_based})`;
  tp.append(el('p','src-note',`${p}: ${state}. Phaladeepika 1937, chapter XXVI, verse 25, PDF page 333.`));
 }
 det.append(tp);
 out.append(det);

 out.append(el('p','src-note',r.notice));
}

function ordinal(n){return n===1?'st':n===2?'nd':n===3?'rd':'th';}
function addDays(iso,n){const d=new Date(iso+'T00:00:00Z');d.setUTCDate(d.getUTCDate()+n);return d.toISOString().slice(0,10);}
function setTitle(){const ta=(document.documentElement.lang==='ta');document.title=ta?'வார ராசி நிலை | ஜாதகம்':'Weekly sky by lagna | Horoscope';}
document.addEventListener('languagechange',()=>setTimeout(setTitle,0));
setTitle();
buildControls();
