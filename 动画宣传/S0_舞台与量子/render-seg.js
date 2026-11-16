const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const { spawn } = require('child_process');
const { once } = require('events');
const path = require('path');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/S0_舞台与量子';
const HTML = 'file:///' + ROOT + '/s0.html';
const FFMPEG = 'D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/ffmpeg-static/ffmpeg.exe';
const FPS = 60, TOTAL = 90 * FPS;
const START = parseInt(process.env.START || '0', 10);
const END = Math.min(parseInt(process.env.END || String(TOTAL), 10), TOTAL);
const OUT = process.env.OUT || path.join(ROOT, `seg_${String(START).padStart(4, '0')}.mp4`);

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
    args: ['--disable-gpu', '--force-color-profile=srgb', '--font-render-hinting=none']
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  await page.goto(HTML);
  await page.waitForFunction(() => window.__ready === true, { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  const ff = spawn(FFMPEG, [
    '-y',
    '-loglevel', 'error',
    '-f', 'image2pipe',
    '-framerate', String(FPS),
    '-i', 'pipe:0',
    '-an',
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-profile:v', 'high',
    '-level', '4.2',
    '-g', '60',
    OUT
  ], { stdio: ['pipe', 'inherit', 'inherit'] });

  ff.on('error', e => { console.error('FF ERROR', e.message); process.exit(2); });
  ff.stdin.on('error', e => { console.error('STDIN ERROR', e.message); process.exit(3); });

  const t0 = Date.now();
  for (let i = START; i < END; i++) {
    const t = i / FPS;
    await page.evaluate(t => window.renderAt(t), t);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');
    if ((i - START) % 100 === 0) {
      console.log('frame', i, 'of', END, 't=', t.toFixed(2), 'elapsed', ((Date.now() - t0) / 1000).toFixed(1));
    }
  }
  ff.stdin.end();
  const [code] = await once(ff, 'close');
  console.log('SEG DONE', START, END, 'ffmpeg', code, 'elapsed', ((Date.now() - t0) / 1000).toFixed(1));
  await browser.close();
  process.exit(code === 0 ? 0 : 4);
})();
