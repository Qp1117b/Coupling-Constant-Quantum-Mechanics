// 抽帧验证：Edge headless + 确定性 renderAt(t)
const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const path = require('path');
const fs = require('fs');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/宣传片';
const HTML = 'file:///' + ROOT + '/' + (process.env.HTML_NAME || 'CQM_宣传动画_v2.html') + '?shot=1';
const OUT = path.join(ROOT, process.env.OUT_DIR || 'preview_v2');
const TIMES = (process.env.TIMES || '2,10,18,30,48,53,63,76,86,100,118,140,147,164,172,178')
  .split(',').map(Number);

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
    args: ['--disable-gpu', '--force-color-profile=srgb', '--font-render-hinting=none']
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE ' + m.text()); });
  await page.goto(HTML);
  await page.waitForFunction(() => window.__ready === true, { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  const checks = await page.evaluate(() => window.__checks);
  console.log('CHECKS', JSON.stringify(checks));
  for (const t of TIMES) {
    await page.evaluate(t => window.renderAt(t), t);
    const name = 't' + String(Math.round(t)).padStart(3, '0') + '.png';
    await page.screenshot({ path: path.join(OUT, name), type: 'png' });
    console.log('frame', t, name);
  }
  console.log('ERRORS', errors.length, errors.slice(0, 12).join(' | '));
  await browser.close();
  process.exit(errors.length ? 2 : 0);
})();
