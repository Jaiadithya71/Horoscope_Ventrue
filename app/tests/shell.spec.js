const {test,expect} = require('@playwright/test');
const chennai = {candidates:[{display_name:'Chennai, Tamil Nadu, India',latitude:13.0827,longitude:80.2707,category:'place',type:'city'}]};
const multi = {candidates:[
 {display_name:'Salem, Tamil Nadu, India',latitude:11.6643,longitude:78.146,category:'place',type:'city'},
 {display_name:'Salem, Oregon, United States',latitude:44.9429,longitude:-123.0351,category:'place',type:'city'}]};
test('place lookup resolves one match and calculates',async({page},info)=>{
 await page.route('**/api/geocode**',route=>route.fulfill({json:chennai}));
 await page.goto('/');
 await page.screenshot({path:`/downloads/horoscope-${info.project.name}-start.png`,fullPage:true});
 await page.locator('[name=date]').fill('2000-01-01');
 await page.locator('[name=time]').fill('14:30');
 await page.locator('[name=place]').fill('Chennai');
 await page.locator('[name=timezone]').fill('Asia/Kolkata');
 await page.getByRole('button',{name:'Find coordinates'}).click();
 await expect(page.locator('#resolved')).toContainText('13.0827, 80.2707');
 await expect(page.locator('#resolved')).toContainText('Chennai, Tamil Nadu, India');
 await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.locator('#results')).toBeVisible();
 await expect(page.locator('.summary-grid')).toContainText('Aries');
 await expect(page.locator('.summary-grid')).toContainText('Libra');
 await expect(page.locator('.result-head')).toContainText('coordinates from place lookup');
 await expect(page.locator('.boundary').last()).toContainText('Personal forecast: unavailable');
 await page.screenshot({path:`/downloads/horoscope-${info.project.name}-result.png`,fullPage:true});
 await page.getByText('Planet placements',{exact:true}).click();
 await expect(page.locator('td').first()).toHaveText('Sun');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
test('ambiguous place asks the user to pick',async({page})=>{
 await page.route('**/api/geocode**',route=>route.fulfill({json:multi}));
 await page.goto('/');
 await page.locator('[name=place]').fill('Salem');
 await page.getByRole('button',{name:'Find coordinates'}).click();
 await expect(page.getByRole('alert')).toContainText('More than one place matches');
 await page.getByText('Salem, Tamil Nadu, India').click();
 await expect(page.locator('#resolved')).toContainText('11.6643, 78.1460');
 await expect(page.locator('#candidates')).toBeHidden();
});
test('no match and manual fallback',async({page})=>{
 await page.route('**/api/geocode**',route=>route.fulfill({json:{candidates:[]}}));
 await page.goto('/');
 await page.locator('[name=place]').fill('Nowhereplace');
 await page.getByRole('button',{name:'Find coordinates'}).click();
 await expect(page.getByRole('alert')).toContainText('No match');
 await page.locator('details.manual summary').click();
 await expect(page.locator('[name=latitude]')).toBeVisible();
});
test('manual coordinates still work without lookup, safe text, timezone errors',async({page})=>{
 let geocodeCalls = 0;
 await page.route('**/api/geocode**',route=>{geocodeCalls++;route.fulfill({json:chennai});});
 await page.goto('/');await page.getByRole('button',{name:'Use a synthetic example'}).click();
 await page.locator('[name=place]').fill('<img src=x onerror=alert(1)>');
 await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.locator('#results h2')).toHaveText('<img src=x onerror=alert(1)>');
 expect(await page.locator('#results img').count()).toBe(0);
 expect(geocodeCalls).toBe(0);
 await page.locator('[name=timezone]').fill('bad-zone');await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('Invalid IANA timezone');
 await expect(page.locator('#results')).toBeHidden();
 await expect(page.getByRole('button',{name:'Calculate chart',exact:true})).toBeEnabled();
});
