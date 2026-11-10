const {test,expect}=require('@playwright/test');
const fs=require('node:fs');const vm=require('node:vm');
test('fixed chooser renders, filters locally and opens the unchanged chart',async({page},info)=>{
 await page.route('**/_vercel/**',r=>r.abort());
 await page.goto('/reels');
 await expect(page.locator('h1')).toHaveText('எந்த ரீல் பார்த்து வந்தீங்க?');
 await expect(page.locator('.reel-card')).toHaveCount(12);
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.screenshot({path:`/downloads/astro-chooser-${info.project.name}-ta.png`,fullPage:true});
 await page.locator('[data-lang=en]').click();
 await expect(page.locator('h1')).toHaveText('Which reel brought you here?');
 await page.screenshot({path:`/downloads/astro-chooser-${info.project.name}-en.png`,fullPage:true});
 await page.locator('#reel-search').fill('Marriage');
 await expect(page.locator('.reel-card')).toHaveCount(1);
 await expect(page.locator('.reel-card')).toHaveAttribute('href','/from/marriage-timing');
 await page.locator('.reel-card').click();
 await expect(page).toHaveURL(/\/from\/marriage-timing$/);
 await expect(page.locator('#birth-form')).toBeVisible();
 await expect(page.locator('#results')).toBeHidden();
 await page.screenshot({path:`/downloads/astro-chooser-${info.project.name}-chart.png`,fullPage:true});
});
test('all catalog links load chart and unknown and skip remain optional',async({page})=>{
 await page.route('**/_vercel/**',r=>r.abort());
 await page.goto('/reels');
 const links=await page.locator('.reel-card').evaluateAll(es=>es.map(e=>e.getAttribute('href')));
 for(const link of links){await page.goto(link);await expect(page.locator('#birth-form')).toBeVisible();}
 await page.goto('/reels');await page.locator('#reel-search').fill('no-such-reel');
 await expect(page.locator('#no-matches')).toBeVisible();
 await page.locator('.unknown').click();await expect(page).toHaveURL(/\/from\/unknown$/);await expect(page.locator('#birth-form')).toBeVisible();
 await page.goto('/reels');await page.locator('.skip').click();await expect(page).toHaveURL(/\/$/);
});
test('chooser works at 320px, keyboard and without JavaScript',async({page,browser})=>{
 await page.route('**/_vercel/**',r=>r.abort());
 await page.setViewportSize({width:320,height:740});await page.goto('/reels');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 for(const a of await page.locator('.reel-card,.skip,.unknown,[data-lang]').all()){const b=await a.boundingBox();expect(b.height).toBeGreaterThanOrEqual(44);}
 await page.locator('.reel-card').first().focus();await page.keyboard.press('Enter');await expect(page).toHaveURL(/marriage-timing$/);
 const context=await browser.newContext({javaScriptEnabled:false});const p=await context.newPage();await p.goto('http://127.0.0.1:8000/reels');await expect(p.locator('noscript a')).toBeVisible();await context.close();
});
test('analytics only records whitelisted paths, never query/hash or free text',()=>{
 const ctx={window:{},location:{origin:'https://test.invalid'},URL};ctx.window.va=(...a)=>ctx.hook=a[1];vm.createContext(ctx);
 vm.runInContext(fs.readFileSync('app/reels-catalog.js','utf8'),ctx);vm.runInContext(fs.readFileSync('app/analytics.js','utf8'),ctx);
 for(const path of ['/','/reels','/from/marriage-timing','/from/unknown','/weekly','/stats'])expect(ctx.hook({url:'https://test.invalid'+path+'?birth=SECRET#private'}).url).toBe('https://test.invalid'+path);
 for(const path of ['/from/private-person','/from/123-SECRET','/api/calculate','/search?q=SECRET'])expect(ctx.hook({url:'https://test.invalid'+path}).url).toBe('https://test.invalid/other');
 expect(ctx.hook({url:'http://['})).toBeNull();
});
