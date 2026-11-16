const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const path = require('path');
const fs = require('fs');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/S0_舞台与量子';
const HTML = 'file:///' + ROOT + '/s0.html';
const OUT = path.join(ROOT, 'preview');

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
    args: ['--disable-gpu', '--force-color-profile=srgb', '--font-render-hinting=none']
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('console', m => console.log('CONSOLE', m.type(), m.text()));
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  await page.goto(HTML);
  await page.waitForFunction(() => window.__ready === true, { timeout: 20000 });
  await page.evaluate(() => document.fonts.ready);
  const times = [0, 3, 8, 15, 21, 26, 31, 36, 41, 48, 54, 60, 68, 72, 78, 86, 89.9];
  for (const t of times) {
    await page.evaluate(t => window.renderAt(t), t);
    const name = 't' + String(t).replace('.', '_') + '.png';
    await page.screenshot({ path: path.join(OUT, name) });
    console.log('frame', t, name);
  }
  await browser.close();
})();
