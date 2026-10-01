const {test,expect} = require('@playwright/test');
test('real calculation, gates, disclosure and layout',async({page},info)=>{
 await page.goto('/');
 await page.screenshot({path:`/downloads/horoscope-${info.project.name}-start.png`,fullPage:true});
 await page.getByRole('button',{name:'Use a synthetic example'}).click();
 await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.locator('#results')).toBeVisible();
 await expect(page.locator('.summary-grid')).toContainText('Aries');
 await expect(page.locator('.summary-grid')).toContainText('Libra');
 await expect(page.locator('.boundary').last()).toContainText('Personal forecast: unavailable');
 await page.screenshot({path:`/downloads/horoscope-${info.project.name}-result.png`,fullPage:true});
 await page.getByText('Planet placements',{exact:true}).click();
 await expect(page.locator('td').first()).toHaveText('Sun');
 await expect(page.locator('table').first()).toContainText('Rahu');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.getByText('Period arithmetic',{exact:true}).click();
 await expect(page.locator('#results')).toContainText('No current-period label');
});
test('invalid timezone hides stale result, safe text rendering',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:'Use a synthetic example'}).click();
 await page.locator('[name=place]').fill('<img src=x onerror=alert(1)>');
 await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.locator('#results h2')).toHaveText('<img src=x onerror=alert(1)>');
 expect(await page.locator('#results img').count()).toBe(0);
 await page.locator('[name=timezone]').fill('bad-zone');await page.getByRole('button',{name:'Calculate chart',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('Invalid IANA timezone');
 await expect(page.locator('#results')).toBeHidden();
 await expect(page.getByRole('button',{name:'Calculate chart',exact:true})).toBeEnabled();
});
