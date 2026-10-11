const {test,expect}=require('@playwright/test');
test.beforeEach(async({page})=>{await page.addInitScript(()=>localStorage.setItem('horoscope-language','en'));});
async function notebook(page){await page.goto('/');await page.getByRole('button',{name:'Use a synthetic example'}).click();await page.locator('#clients-title').click();}
async function save(page,name='Test client'){await page.locator('#client-name').fill(name);await page.getByRole('button',{name:'Save birth details to this browser'}).click();await expect(page.locator('#client-status')).toContainText('saved in this browser');}
test('opt-in client save, consultation, reload and deletion',async({page},info)=>{
 let notesSent=false;page.on('request',r=>{if(r.postData()?.includes('private note'))notesSent=true;});
 await notebook(page);expect(await page.evaluate(()=>localStorage.getItem('horoscope-client-notebook-v1'))).toBe(null);await save(page,'Test <img src=x>');
 await page.locator('#consult-reading').fill('Reader expects a career change');await page.locator('#consult-observed').fill('Client reports no change yet');await page.locator('#consult-notes').fill('private note <script>alert(1)</script>');await page.getByRole('button',{name:'Save consultation',exact:true}).click();
 await expect(page.locator('.consult-item')).toContainText('no change yet');await page.getByRole('button',{name:'Edit consultation',exact:true}).click();await page.locator('#consult-observed').fill('Corrected: no change yet');await page.getByRole('button',{name:'Update consultation',exact:true}).click();await expect(page.locator('.consult-item')).toHaveCount(1);await expect(page.locator('.consult-item')).toContainText('Corrected: no change yet');expect(await page.locator('.client-panel script,.client-panel img').count()).toBe(0);
 await page.screenshot({path:`/downloads/notebook-${info.project.name}.png`,fullPage:true});
 await page.reload();await page.locator('#clients-title').click();await page.locator('.client-item').click();await expect(page.locator('.consult-item')).toContainText('private note');
 page.on('dialog',d=>d.accept());await page.getByRole('button',{name:'Load birth details'}).click();await expect(page.locator('[name=time]')).toHaveValue('14:30');await expect(page.locator('[name=latitude]')).toHaveValue('13');
 await page.getByRole('button',{name:'Calculate chart',exact:true}).click();await expect(page.locator('#results')).toBeVisible();expect(notesSent).toBe(false);
 await page.getByRole('button',{name:'Delete client',exact:true}).click();await expect(page.locator('.client-item')).toHaveCount(0);await expect(page.locator('#client-detail')).toBeHidden();
});
test('uncertain time survives saving and loading without an invented precise time',async({page})=>{
 await notebook(page);await page.locator('[name=timemode][value=window]').check();await save(page);page.on('dialog',d=>d.accept());await page.locator('#client-load').click();await expect(page.locator('[name=timemode][value=window]')).toBeChecked();await expect(page.locator('[name=win_start]')).toHaveValue('06:00');await expect(page.locator('#client-birth')).toContainText('uncertain');expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
});
test('corrupt or blocked storage does not falsely report success',async({page})=>{
 await page.addInitScript(()=>localStorage.setItem('horoscope-client-notebook-v1','broken'));await notebook(page);await page.locator('#client-name').fill('Test');await page.locator('#client-form button').click();await expect(page.locator('#client-status')).toContainText('No records were changed');expect(await page.evaluate(()=>localStorage.getItem('horoscope-client-notebook-v1'))).toBe('broken');
});
test('backup download, import adds rather than overwrites; invalid backup rejected',async({page})=>{
 await notebook(page);await save(page);const promise=page.waitForEvent('download');await page.locator('.client-panel details details summary').click();await page.locator('#clients-export').click();const dl=await promise;const path=await dl.path();page.on('dialog',d=>d.accept());await page.locator('#clients-import').setInputFiles(path);await expect(page.locator('.client-item')).toHaveCount(2);
 await page.locator('#clients-import').setInputFiles({name:'bad.json',mimeType:'application/json',buffer:Buffer.from('{"version":1,"records":[{}]}')});await expect(page.locator('#client-status')).toContainText('Invalid client');await expect(page.locator('.client-item')).toHaveCount(2);
});
