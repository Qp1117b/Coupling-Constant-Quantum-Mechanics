// 一次打包、多帧定格。用于门禁前的画面与运行时验证。
import path from 'node:path';
import fs from 'node:fs';
import crypto from 'node:crypto';
import {bundle} from '@remotion/bundler';
import {getCompositions, renderStill} from '@remotion/renderer';

const ROOT = path.resolve(import.meta.dirname, '..');
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const OUT = path.join(ROOT, 'out', 'probe');
const TIMES = (process.env.TIMES || '1,10,24,53,86,118,147,178')
  .split(',').map(s => Number(s.trim())).filter(n => !Number.isNaN(n));

fs.mkdirSync(OUT, {recursive: true});

const serveUrl = await bundle({
  entryPoint: path.join(ROOT, 'src', 'index.js'),
  outDir: path.join(ROOT, 'out', '.bundle'),
  onProgress: p => { if (p === 100) console.log('bundle 100%'); },
});
console.log('bundled at', serveUrl);

const comps = await getCompositions(serveUrl, {browserExecutable: EDGE});
const comp = comps.find(c => c.id === 'CQMPromo');
if (!comp) throw new Error('CQMPromo composition not found');
console.log('composition', comp.id, comp.durationInFrames, 'frames', comp.width + 'x' + comp.height, comp.fps + 'fps');

for (const t of TIMES) {
  const file = path.join(OUT, 't' + String(t).padStart(3, '0') + '.png');
  await renderStill({
    composition: comp,
    serveUrl,
    output: file,
    frame: t * 60,
    imageFormat: 'png',
    browserExecutable: EDGE,
    overwrite: true,
    logLevel: 'error',
  });
  console.log('t=' + t, fs.statSync(file).size, 'bytes');
}
// 跳帧确定性：t=86 → t=10 → t=86，两次 86 必须逐像素一致
if (process.env.DET) {
  const hashes = [];
  for (const [i, sec] of [86, 10, 86].entries()) {
    const file = path.join(OUT, 'det_' + i + '.png');
    await renderStill({
      composition: comp, serveUrl, output: file, frame: sec * 60,
      imageFormat: 'png', browserExecutable: EDGE, overwrite: true, logLevel: 'error',
    });
    hashes.push(crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'));
  }
  const same = hashes[0] === hashes[2];
  console.log('DETERMINISM 86→10→86:', same ? 'IDENTICAL' : 'DIFFERENT');
  if (!same) process.exitCode = 1;
}
console.log('PROBE_OK');
