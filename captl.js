const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  const base = 'https://horoscope-ventrue.vercel.app/chart';
  await page.goto(base, { waitUntil: 'networkidle', timeout: 60000 });
  await page.evaluate(() => localStorage.setItem('horoscope-language','en'));
  await page.reload({ waitUntil: 'networkidle' });
  await page.click('#example'); await page.waitForTimeout(400);
  await page.click('#calculate');
  await page.waitForSelector('#scr-app:not([hidden])', { timeout: 90000 });
  await page.waitForTimeout(2000);
  // Home: now card
  await page.evaluate(() => document.querySelector('.now-card')?.scrollIntoView({block:'center'}));
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/tmp/tl-now-en.png' });
  // Timeline tab EN
  await page.click('[data-tab=timeline]'); await page.waitForTimeout(1200);
  await page.evaluate(() => window.scrollTo(0,0)); await page.waitForTimeout(400);
  await page.screenshot({ path: '/tmp/tl-tab-en.png' });
  // Opened current stretch lower on page
  await page.evaluate(() => document.querySelector('.tln.now')?.scrollIntoView({block:'start'}));
  await page.waitForTimeout(800);
  await page.screenshot({ path: '/tmp/tl-open-en.png' });
  // Tamil
  await page.click('[data-language=ta]'); await page.waitForTimeout(1500);
  await page.evaluate(() => window.scrollTo(0,0)); await page.waitForTimeout(400);
  await page.screenshot({ path: '/tmp/tl-tab-ta.png' });
  await page.evaluate(() => document.querySelector('.tln.now')?.scrollIntoView({block:'start'}));
  await page.waitForTimeout(800);
  await page.screenshot({ path: '/tmp/tl-open-ta.png' });
  await page.click('[data-tab=home]'); await page.waitForTimeout(800);
  await page.evaluate(() => document.querySelector('.now-card')?.scrollIntoView({block:'center'}));
  await page.waitForTimeout(1000);
  await page.screenshot({ path: '/tmp/tl-now-ta.png' });
  await browser.close(); console.log('done');
})().catch(e => { console.error(e.message); process.exit(1); });
