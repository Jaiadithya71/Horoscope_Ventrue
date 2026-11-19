const {chromium}=require('playwright');
(async()=>{
 const browser=await chromium.launch();const page=await browser.newPage({viewport:{width:390,height:844}});
 const variants=JSON.parse(require('child_process').execFileSync('.venv/bin/python',['app/tests/ui_variants.py'],{maxBuffer:20*1024*1024}));
 await page.goto('http://127.0.0.1:8000/chart');
 for(const [i,v] of variants.entries()){
  await page.evaluate(v=>render(v.report,v.birth,false),v);await page.waitForTimeout(80);
  const ta=await page.evaluate(()=>{const w=document.createTreeWalker(document.querySelector('#results'),NodeFilter.SHOW_TEXT),a=[];while(w.nextNode()){const n=w.currentNode;if(n.parentElement&&!n.parentElement.closest('pre,[data-private]')&&/[a-zA-Z]{3,}/.test(n.textContent)&&!/(PDF|UTC|Swiss|Asia\/|Synthetic test|null|Nominatim|OpenStreetMap|Vercel|Lahiri|Moshier|Jaiadithya|cookies)/.test(n.textContent))a.push(n.textContent.trim());}return [...new Set(a)].filter(Boolean);});
  if(ta.length)console.log('variant',i,'TA-LATIN:',ta.slice(0,10));
  await page.locator('[data-language=en]').click();
  const en=await page.evaluate(()=>{const w=document.createTreeWalker(document.querySelector('#results'),NodeFilter.SHOW_TEXT),a=[];while(w.nextNode()){const n=w.currentNode;if(n.parentElement&&!n.parentElement.closest('pre,[data-private]')&&/[\u0B80-\u0BFF]/.test(n.textContent))a.push(n.parentElement.tagName+'.'+n.parentElement.className+' :: '+n.textContent.trim().slice(0,70));}return [...new Set(a)];});
  if(en.length)console.log('variant',i,'EN-RESIDUE:',en.slice(0,8));
  await page.locator('[data-language=ta]').click();
 }
 await browser.close();
})();
