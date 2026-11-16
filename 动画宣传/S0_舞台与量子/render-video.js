const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const { spawn } = require('child_process');
const { once } = require('events');
const path = require('path');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/S0_舞台与量子';
const HTML = 'file:///' + ROOT + '/s0.html';
const FFMPEG = 'D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/ffmpeg-static/ffmpeg.exe';
const OUT = path.join(ROOT, 'S0_舞台与量子_1080p60.mp4');
const FPS = 60, TOTAL = 90 * FPS;

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
    '-i', path.join(ROOT, 'master.wav'),
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '18',
    '-pix_fmt', 'yuv420p',
    '-profile:v', 'high',
    '-level', '4.2',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    '-movflags', '+faststart',
    OUT
  ], { stdio: ['pipe', 'inherit', 'inherit'] });

  const t0 = Date.now();
  for (let i = 0; i < TOTAL; i++) {
    const t = i / FPS;
    await page.evaluate(t => window.renderAt(t), t);
    const buf = await page.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');
    if (i % 300 === 0) {
      const sec = ((Date.now() - t0) / 1000).toFixed(1);
      console.log('frame', i, '/', TOTAL, 't=', t.toFixed(2), 'elapsed', sec);
    }
  }
  ff.stdin.end();
  const [code] = await once(ff, 'close');
  console.log('ffmpeg exit', code, 'elapsed', ((Date.now() - t0) / 1000).toFixed(1));
  await browser.close();
})();
