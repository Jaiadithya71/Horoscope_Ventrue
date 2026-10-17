/* Content studio: renders engine cards as-is; no client-side astrology. */
let INDEX=null, tool='weekday', choice=null;
const cache=new Map();
function el(tag,cls,text){const e=document.createElement(tag);if(cls)e.className=cls;if(text!=null)e.textContent=text;return e;}

async function loadIndex(){
 const res=await fetch('/api/studio',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({tool:'index'})});
 INDEX=await res.json(); buildTools(); pick('weekday',null);
}

function buildTools(){
 const tabs=document.querySelector('#tool-tabs');tabs.textContent='';
 for(const t of INDEX.tools){
  const b=el('button','secondary inline');b.type='button';b.setAttribute('role','tab');
  b.setAttribute('aria-pressed',String(t.id===tool));
  b.textContent=`${t.title_ta} · ${t.title_en}`;
  b.addEventListener('click',()=>pick(t.id,null));
  tabs.append(b);
 }
}

function pick(t,c){
 tool=t;choice=c;
 buildTools();
 const meta=INDEX.tools.find(x=>x.id===t);
 document.querySelector('#choice-legend').textContent=`${meta.title_ta} · ${meta.title_en}`;
 const grid=document.querySelector('#choice-grid');grid.textContent='';
 for(const ch of meta.choices){
  const b=el('button');b.type='button';b.setAttribute('aria-pressed',String(ch.id===choice));
  b.innerHTML='';b.append(document.createTextNode(`${ch.ta} · ${ch.en}`));
  b.addEventListener('click',()=>pick(t,ch.id));
  grid.append(b);
 }
 if(c)compute();
}

async function compute(){
 const err=document.querySelector('#error');err.hidden=true;
 const key=JSON.stringify({tool,choice});
 const ws=document.querySelector('#workspace');ws.setAttribute('aria-busy','true');
 try{
  if(!cache.has(key)){
   const res=await fetch('/api/studio',{method:'POST',headers:{'Content-Type':'application/json'},body:key,signal:AbortSignal.timeout(15000)});
   const data=await res.json().catch(()=>({}));
   if(!res.ok)throw new Error(data.error||'Unavailable.');
   cache.set(key,data);
  }
  render(cache.get(key));
 }catch(e){err.textContent=e.message||'Unavailable.';err.hidden=false;}
 finally{ws.setAttribute('aria-busy','false');}
}

function render(r){
 document.querySelector('#empty').hidden=true;
 const out=document.querySelector('#results');out.hidden=false;out.textContent='';
 const head=el('div','result-head week-card');
 head.append(el('h2',null,`${r.title_ta} · ${r.title_en}`));
 out.append(head);

 const card=el('div','week-card');card.append(el('h3',null,'Card lines · அட்டை வாசகங்கள்'));
 for(const b of r.bullets){
  const d=el('div','finding');
  const topic=el('div','topic',b.kind==='derived'?'derived · தொகுப்பு':'cited · நூல் குறிப்பு');
  if(b.kind==='derived')topic.style.color='#a51522';
  d.append(topic);
  d.append(el('div',null,b.ta));
  d.append(el('div','days',b.en));
  if(b.source)d.append(el('div','src',b.source));
  card.append(d);
 }
 out.append(card);

 for(const n of r.notices){
  const nc=el('div','week-card');nc.append(el('h3',null,'What the sources do and do not say · நேர்மைக் குறிப்பு'));
  nc.append(el('p',null,n.ta));nc.append(el('p','muted',n.en));
  out.append(nc);
 }

 const cap=el('div','week-card');cap.append(el('h3',null,'Ready caption · தயார் வாசகம்'));
 const pre=el('pre',null,r.caption_text);cap.append(pre);
 const btn=el('button','secondary inline','Copy caption');
 btn.addEventListener('click',async()=>{try{await navigator.clipboard.writeText(r.caption_text);btn.textContent='Copied';}catch(_){btn.textContent='Select and copy above';}});
 cap.append(btn);
 cap.append(el('p','src-note',r.general_notice));
 out.append(cap);
}
loadIndex();
