// 出片前静态门禁。任何一项失败即 exit 1，禁止渲染。
// 检查对象：唯一数据源 vs v2 内容内核、字幕措辞、限定语、时长、母带、声画表对齐。
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve(import.meta.dirname, '..');
const REPO = path.resolve(ROOT, '..', '..');
const V2 = path.join(ROOT, 'reference', 'CQM_宣传动画_v2.html');
const DATA_FILE = path.join(ROOT, 'src', 'data.js');
const KERNEL_FILE = path.join(ROOT, 'src', 'legacy', 'kernel.js');
const WAV = path.join(ROOT, 'public', 'master.wav');

const v2 = fs.readFileSync(V2, 'utf8');
const data = fs.readFileSync(DATA_FILE, 'utf8');
const kernel = fs.readFileSync(KERNEL_FILE, 'utf8');

const fails = [];
const notes = [];
const ok = (cond, label) => { if (!cond) fails.push(label); };

/** 按括号平衡抽取 `const NAME = <value>;` 的值文本（含开闭括号）。 */
function constValue(src, name) {
  const re = new RegExp('(?:export\\s+)?const\\s+' + name + '\\s*=\\s*');
  const m = re.exec(src);
  if (!m) throw new Error('找不到常量 ' + name);
  const i = m.index + m[0].length;
  const open = src[i];
  if (open !== '[' && open !== '{') {
    const end = src.indexOf(';', i);
    return src.slice(i, end).trim();
  }
  const close = open === '[' ? ']' : '}';
  let depth = 0, inStr = false, quote = '', j = i;
  for (; j < src.length; j++) {
    const ch = src[j];
    if (inStr) {
      if (ch === '\\') { j++; continue; }
      if (ch === quote) inStr = false;
      continue;
    }
    if (ch === '"' || ch === "'" || ch === '`') { inStr = true; quote = ch; continue; }
    if (ch === open) depth++;
    else if (ch === close) { depth--; if (depth === 0) return src.slice(i, j + 1); }
  }
  throw new Error('常量 ' + name + ' 括号不平衡');
}

// G1 数据源逐字一致：v2 → data.js
for (const name of ['C', 'MATH', 'MONO', 'ZH', 'SYM', 'TOTAL', 'RAIL', 'OPS', 'SEGS', 'B', 'CAPS', 'SCORE']) {
  const a = constValue(v2, name);
  const b = constValue(data, name);
  ok(a === b, 'G1 数据源漂移: ' + name);
}
notes.push('G1 v2 ↔ data.js：12 个常量逐字一致');

// G2 内容内核的场景几何逐字保留（v2 的 S1..S6 原样出现在 kernel.js）
const v2Lines = v2.split('\n');
const scenes = v2Lines.slice(327, 760).join('\n');
ok(kernel.includes(scenes), 'G2 场景几何被改动');
const kit = v2Lines.slice(103, 151).join('\n');
ok(kernel.includes(kit), 'G2 SVG 工具集被改动');
notes.push('G2 场景几何 / SVG 工具集：逐字保留');

// G3 运动层确实被剥离
for (const banned of ['motionAt(', 'typeAt(', 'cameraAt(', 'fieldAt(', 'transitionAt(', 'localAt(', 'OfflineAudioContext']) {
  ok(!kernel.includes(banned), 'G3 旧运动/音画残留: ' + banned);
}
notes.push('G3 旧运动引擎与双管线：已剥离');

// G4 字幕措辞
const capRe = /\{a:([\d.]+),b:([\d.]+),m:"(.*?)",s:"(.*?)",g:/g;
const caps = [...data.matchAll(capRe)].map(m => ({a: +m[1], b: +m[2], m: m[3], s: m[4]}));
ok(caps.length === 46, 'G4 字幕条数不是 46（实得 ' + caps.length + '）');
const bannedWords = ['证明', '已证', '确定', '彻底解决', '零参数', '室温超导', '已闭合', '已统一', '已验证'];
const bad = caps.filter(c => bannedWords.some(w => c.m.includes(w) && !c.m.includes('不等于')));
ok(bad.length === 0, 'G4 禁用措辞命中 ' + bad.length + ' 条');
const qualifiers = ['构造后验', '待推', '框架内构造', '示意', '启发式', '设定', '假设', '机制形状', '不是', '坐标'];
// 只有「构造后验 / 与实验比对」类数字才强制限定语；纯推导数值不在此列。
const needsQualifier = /ppm|Gₙ|137\.|与实验|偏差|10⁻³⁸|16384/;
const unqualified = caps.filter(c => needsQualifier.test(c.m) && !qualifiers.some(q => c.m.includes(q) || c.s.includes(q)));
ok(unqualified.length === 0, 'G4 数值字幕缺限定语 ' + unqualified.length + ' 条');
notes.push('G4 字幕 46 条：禁用词 0、数值限定语齐备');

// G5 限定语同屏常驻
const gn = data.split('构造后验数字校验，待独立复现').length - 1;
ok(gn >= 3, 'G5 G_N 限定语不足（' + gn + '）');
for (const key of ['FG 的因果假设', '框架设定 · 无推导', '启发式近似，非从谱导出', '示意值，不是理论预言']) {
  ok(data.includes(key), 'G5 缺失限定语: ' + key);
}
notes.push('G5 关键限定语：全部在表');

// G6 时长 / 帧数 / 母带
ok(/export const TOTAL=180;/.test(data), 'G6 TOTAL 不是 180');
ok(/export const FPS = 60;/.test(data), 'G6 FPS 不是 60');
ok(/durationInFrames=\{10800\}/.test(fs.readFileSync(path.join(ROOT, 'src', 'Root.jsx'), 'utf8')), 'G6 Composition 帧数不是 10800');
const wav = fs.readFileSync(WAV);
ok(wav.toString('ascii', 0, 4) === 'RIFF', 'G6 母带不是 RIFF');
const channels = wav.readUInt16LE(22);
const sampleRate = wav.readUInt32LE(24);
const bits = wav.readUInt16LE(34);
let dataOff = 12, dataSize = 0;
while (dataOff + 8 <= wav.length) {
  const id = wav.toString('ascii', dataOff, dataOff + 4);
  const sz = wav.readUInt32LE(dataOff + 4);
  if (id === 'data') { dataSize = sz; break; }
  dataOff += 8 + sz + (sz % 2);
}
const dur = dataSize / (sampleRate * channels * bits / 8);
ok(Math.abs(dur - 180) < 0.05, 'G6 母带时长 ' + dur.toFixed(3) + 's ≠ 180s');
notes.push('G6 180s / 60fps / 10800 帧 / 母带 ' + dur.toFixed(3) + 's @ ' + sampleRate + 'Hz');

// G7 声画表对齐：演算刻度与声场事件同源
const ops = [...constValue(data, 'OPS').matchAll(/[\d.]+/g)].map(m => +m[0]);
const scoreTs = [...constValue(data, 'SCORE').matchAll(/t:([\d.]+)/g)].map(m => +m[1]);
ok(ops.length === 24, 'G7 演算刻度不是 24');
ok(scoreTs.length >= 60, 'G7 声场事件过少');
const matched = ops.filter(o => scoreTs.some(s => Math.abs(s - o) < 1.2)).length;
ok(matched >= 14, 'G7 刻度与声场对齐仅 ' + matched + '/24');
notes.push('G7 演算刻度 24 / 声场事件 ' + scoreTs.length + ' / 对齐 ' + matched);

console.log('===== CQM 宣传动画 · 出片前门禁 =====');
notes.forEach(n => console.log('  PASS  ' + n));
if (fails.length) {
  fails.forEach(f => console.log('  FAIL  ' + f));
  console.log('GATE_FAILED ' + fails.length + ' 项，禁止渲染');
  process.exit(1);
}
console.log('GATE_PASS  0 failures');
