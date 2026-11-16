// 确定性逐帧渲染 → ffmpeg image2pipe → 1080p60 MP4（中间 PNG 不落盘）
const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const { spawn } = require('child_process');
const { once } = require('events');
const path = require('path');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/宣传片';
const HTML = 'file:///' + ROOT + '/' + (process.env.HTML_NAME || 'CQM_宣传动画_v2.html') + '?shot=1';
const FFMPEG = 'D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/ffmpeg-static/ffmpeg.exe';
const OUT = process.env.OUT || 'D:/WorkSpace/物理/CQMFormal/动画宣传/输出/CQM_宣传动画_1080p60_v2.mp4';
const FPS = 60, TOTAL = 180 * FPS;
const START = parseInt(process.env.START || '0', 10);
const END = Math.min(parseInt(process.env.END || String(TOTAL), 10), TOTAL);

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
    args: ['--disable-gpu', '--force-color-profile=srgb', '--font-render-hinting=none']
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(HTML);
  await page.waitForFunction(() => window.__ready === true, { timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);

  const args = [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-vcodec', 'mjpeg', '-i', 'pipe:0',
    '-i', path.join(ROOT, 'master.wav'),
    '-c:v', 'libx264', '-preset', 'medium',
    '-b:v', '11M', '-maxrate', '14M', '-bufsize', '22M',
    '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-level', '4.2',
    '-g', '120', '-keyint_min', '120', '-sc_threshold', '0',
    '-color_primaries', 'bt709', '-color_trc', 'bt709', '-colorspace', 'bt709',
    '-c:a', 'aac', '-b:a', '192k', '-ar', '48000', '-ac', '2',
    '-shortest', '-movflags', '+faststart',
    OUT
  ];
  const ff = spawn(FFMPEG, args, { stdio: ['pipe', 'inherit', 'inherit'] });
  ff.on('error', e => { console.error('FF ERROR', e.message); process.exit(2); });
  ff.stdin.on('error', e => { console.error('STDIN ERROR', e.message); process.exit(3); });

  const t0 = Date.now();
  for (let i = START; i < END; i++) {
    await page.evaluate(t => window.renderAt(t), i / FPS);
    // MJPEG 中间帧：q98 相对 PNG 平均像素差 0.74/255，逐帧速度约 5 倍
    const buf = await page.screenshot({ type: 'jpeg', quality: 98 });
    if (!ff.stdin.write(buf)) await once(ff.stdin, 'drain');
    if ((i - START) % 300 === 0) {
      const sec = ((Date.now() - t0) / 1000).toFixed(1);
      console.log('frame', i, '/', END, 't=', (i / FPS).toFixed(2), 'elapsed', sec);
    }
  }
  ff.stdin.end();
  const [code] = await once(ff, 'close');
  console.log('FFMPEG_EXIT', code, 'elapsed', ((Date.now() - t0) / 1000).toFixed(1),
    'errors', errors.length, errors.slice(0, 5).join(' | '));
  await browser.close();
  process.exit(code === 0 && errors.length === 0 ? 0 : 4);
})();
