const { chromium } = require('D:/WorkSpace/物理/CQMFormal/.workbuddy/anim-render/node_modules/playwright-core');
const fs = require('fs');
const path = require('path');

const ROOT = 'D:/WorkSpace/物理/CQMFormal/动画宣传/S0_舞台与量子';
const HTML = 'file:///' + ROOT + '/s0.html';

(async () => {
  const browser = await chromium.launch({
    executablePath: 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
    headless: true,
    args: ['--disable-gpu']
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', m => console.log('CONSOLE', m.type(), m.text()));
  page.on('pageerror', e => console.log('PAGEERROR', e.message));
  await page.goto(HTML);
  await page.waitForFunction(() => window.__ready === true, { timeout: 30000 });
  const info = await page.evaluate(() => window.__renderAudio());
  console.log('audio', JSON.stringify(info));

  const dataBytes = info.len * 4;
  const header = Buffer.alloc(44);
  header.write('RIFF', 0, 'ascii');
  header.writeUInt32LE(36 + dataBytes, 4);
  header.write('WAVE', 8, 'ascii');
  header.write('fmt ', 12, 'ascii');
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(2, 22);
  header.writeUInt32LE(info.sr, 24);
  header.writeUInt32LE(info.sr * 4, 28);
  header.writeUInt16LE(4, 32);
  header.writeUInt16LE(16, 34);
  header.write('data', 36, 'ascii');
  header.writeUInt32LE(dataBytes, 40);

  const outPath = path.join(ROOT, 'master.wav');
  const out = fs.createWriteStream(outPath);
  out.write(header);
  const chunks = await page.evaluate(() => window.__wavChunkCount);
  for (let i = 0; i < chunks; i++) {
    const b64 = await page.evaluate(i => window.__wavChunk(i), i);
    out.write(Buffer.from(b64, 'base64'));
    if (i % 10 === 0) console.log('chunk', i);
  }
  await new Promise(r => out.end(r));
  const size = fs.statSync(outPath).size;
  console.log('wrote', outPath, size, 'expected', 44 + dataBytes);
  await browser.close();
})();
