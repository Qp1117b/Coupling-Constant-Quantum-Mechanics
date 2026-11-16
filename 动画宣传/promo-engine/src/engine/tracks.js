// 声明式时间轴：所有时间行为都是数据，没有任何散落的 `if(t>a) setAttribute(...)`。
// 改动画 = 改这张表；evaluate() 是唯一求值器，layer 组件与镜头应用都只消费它的输出。
import {SEGS, OPS, CAPS, SCORE, C, TOTAL} from '../data.js';

const clamp = (x, a, b) => (x < a ? a : x > b ? b : x);

export const EASE = {
  linear: t => t,
  out: t => 1 - Math.pow(1 - clamp(t, 0, 1), 3),
  inOut: t => {
    t = clamp(t, 0, 1);
    return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
  },
};

/** 关键帧采样；keys 必须按 t 递增，v 为标量，可逐段指定缓动。 */
export function sampleKeys(keys, t, defaultEase = 'linear') {
  if (t <= keys[0].t) return keys[0].v;
  for (let i = 0; i < keys.length - 1; i++) {
    const a = keys[i], b = keys[i + 1];
    if (t >= a.t && t <= b.t) {
      const p = (t - a.t) / (b.t - a.t || 1);
      const e = (EASE[b.ease] || EASE[defaultEase])(p);
      return a.v + (b.v - a.v) * e;
    }
  }
  return keys[keys.length - 1].v;
}

/** 连续振荡层：确定性、无累计状态。 */
export function osc(spec, t) {
  return spec.base + spec.amp * Math.sin(2 * Math.PI * spec.freq * t + (spec.phase || 0));
}

/** 窗口内活跃事件；返回带进度 p∈[0,1] 的副本。 */
export function activeEvents(list, t, span) {
  const out = [];
  for (const e of list) {
    const p = (t - e.t) / span;
    if (p >= 0 && p <= 1) out.push({...e, p});
  }
  return out;
}

// ---------- 镜头关键帧：由段表生成，每段三拍推进 + 交替漂移 ----------
function buildCameraKeys() {
  const zoom = [{t: 0, v: 0.986}];
  const dx = [{t: 0, v: 0}];
  const dy = [{t: 0, v: 0}];
  const rot = [{t: 0, v: 0}];
  SEGS.forEach((s, i) => {
    const L = s.b - s.a;
    const dir = i % 2 ? 1 : -1;
    zoom.push({t: s.a + L * 0.45, v: 1.075, ease: 'inOut'});
    zoom.push({t: s.a + L * 0.82, v: 1.128, ease: 'inOut'});
    zoom.push({t: s.b, v: 0.992, ease: 'inOut'});
    dx.push({t: s.a + L * 0.50, v: dir * 13, ease: 'inOut'});
    dx.push({t: s.b, v: 0, ease: 'inOut'});
    dy.push({t: s.a + L * 0.68, v: -dir * 9, ease: 'inOut'});
    dy.push({t: s.b, v: 0, ease: 'inOut'});
    rot.push({t: s.a + L * 0.62, v: dir * 0.32, ease: 'inOut'});
    rot.push({t: s.b, v: 0, ease: 'inOut'});
  });
  return {zoom, dx, dy, rot};
}

const CAM = buildCameraKeys();

export const SEG_COLORS = [C.gold, C.cyan, C.amber, C.cyan, C.amber, C.purple];

/** 事件表：段转场 / 演算脉冲 / 字幕入场 / 声场事件，全部派生自唯一数据源。 */
export const EVENTS = {
  wipes: SEGS.slice(1).map((s, i) => ({t: s.a, seg: i + 1, color: SEG_COLORS[i + 1]})),
  pulses: OPS.map((o, i) => ({t: o, i})),
  captions: CAPS.map((c, i) => ({t: c.a, i})),
  score: SCORE.map((e, i) => ({t: e.t, i, op: e.op})),
};

/** 局部形变：数据表指定「哪一段、哪个节点、多大振幅、多快」，由引擎统一施加。 */
export const LOCAL_MOTION = [
  {seg: 0, node: 'S1.grid', amp: 0.010, freq: 0.42, phase: 0.0},
  {seg: 2, node: 'S3.slots', amp: 0.008, freq: 0.37, phase: 1.1},
  {seg: 5, node: 'S6.layers', amp: 0.009, freq: 0.28, phase: 2.3},
];

export const TRACKS = {
  cameraZoom: CAM.zoom,
  driftX: CAM.dx,
  driftY: CAM.dy,
  rotation: CAM.rot,
  breath: {base: 0, amp: 0.0055, freq: 0.33, phase: 0},
  flowEnergy: {base: 0.55, amp: 0.32, freq: 0.21, phase: 0.4},
  scan: {period: 9, width: 440},
  wipeSpan: 0.9,
  pulseSpan: 1.15,
  captionSpan: 0.42,
};

function indexOfSeg(t) {
  let k = 0;
  for (let i = 0; i < SEGS.length; i++) if (t >= SEGS[i].a) k = i;
  return k;
}

function captionAt(t) {
  for (let i = 0; i < CAPS.length; i++) if (t >= CAPS[i].a && t < CAPS[i].b) return CAPS[i];
  return CAPS[CAPS.length - 1];
}

/** 唯一求值入口：纯函数，t 决定一切，可任意跳帧。 */
export function evaluate(t) {
  t = clamp(t, 0, TOTAL);
  const cap = captionAt(t);
  const captionEnter = clamp((t - cap.a) / TRACKS.captionSpan, 0, 1);
  const zoom = sampleKeys(TRACKS.cameraZoom, t, 'inOut');
  const scale = zoom * (1 + osc(TRACKS.breath, t));
  return {
    t,
    camera: {
      scale,
      dx: sampleKeys(TRACKS.driftX, t, 'inOut'),
      dy: sampleKeys(TRACKS.driftY, t, 'inOut'),
      rot: sampleKeys(TRACKS.rotation, t, 'inOut'),
    },
    flow: {energy: osc(TRACKS.flowEnergy, t), phase: t},
    scanProgress: (t / TRACKS.scan.period) % 1,
    wipes: activeEvents(EVENTS.wipes, t, TRACKS.wipeSpan),
    pulses: activeEvents(EVENTS.pulses, t, TRACKS.pulseSpan),
    caption: cap,
    captionEnter,
    seg: indexOfSeg(t),
  };
}

/** 把求值结果写进内容内核的 DOM。这是引擎的输出端，不含任何业务时间判断。 */
export function applyToKernel(kernel, s) {
  const {scale, dx, dy, rot} = s.camera;
  kernel.cameraG.setAttribute('transform',
    `translate(${(960 + dx).toFixed(2)} ${(540 + dy).toFixed(2)}) ` +
    `rotate(${rot.toFixed(3)}) scale(${scale.toFixed(5)}) translate(-960 -540)`);

  const e = EASE.out(s.captionEnter);
  const se = EASE.out(clamp((s.captionEnter - 0.18) / 0.82, 0, 1));
  kernel.capMain.setAttribute('transform', `translate(${((1 - e) * -38).toFixed(1)} 0)`);
  kernel.capMain.setAttribute('opacity', e.toFixed(3));
  kernel.capSub.setAttribute('transform', `translate(${((1 - se) * -30).toFixed(1)} 0)`);
  kernel.badgeG.setAttribute('transform', `translate(${((1 - e) * 22).toFixed(1)} 0)`);
  kernel.badgeG.setAttribute('opacity', e.toFixed(3));

  for (const m of LOCAL_MOTION) {
    const [sk, key] = m.node.split('.');
    const node = kernel[sk] && kernel[sk][key];
    if (!node) continue;
    const on = s.seg === m.seg ? 1 : 0;
    const v = on * osc({base: 0, amp: m.amp, freq: m.freq, phase: m.phase}, s.t);
    node.setAttribute('transform',
      `translate(${(v * 900).toFixed(2)} ${(v * -420).toFixed(2)})`);
  }
}
