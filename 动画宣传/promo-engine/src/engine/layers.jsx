// 声明式运动图层：只消费 evaluate(t) 的输出，不含任何时间判断。
// 流场位于内容层之下，扫描／转场／脉冲位于内容层之上，两者都不触碰公式 DOM。
import React from 'react';
import {C} from '../data.js';
import {evaluate, TRACKS} from './tracks.js';

const hsh = (i, k) => {
  const x = Math.sin(i * 127.1 + k * 311.7) * 43758.5453;
  return x - Math.floor(x);
};

const SVG_STYLE = {position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, pointerEvents: 'none'};

/** 持续流场：96 个确定性粒子 + 6 条形变波纹 + 呼吸光晕。 */
export const FlowField = ({t}) => {
  const s = evaluate(t);
  const energy = s.flow.energy;
  const nodes = [];

  for (let k = 0; k < 6; k++) {
    const amp = 26 + 17 * Math.sin(t * 0.4 + k * 1.1) + energy * 12;
    const yb = 170 + k * 152 + 42 * Math.sin(t * 0.23 + k);
    let d = '';
    for (let j = 0; j <= 40; j++) {
      const x = j * 48;
      const y = yb + amp * Math.sin(x / 150 + k + t * 0.8) + 6 * Math.sin(x / 70 + k * 2 + t * 0.5);
      d += (j ? 'L' : 'M') + x.toFixed(0) + ' ' + y.toFixed(1) + ' ';
    }
    nodes.push(
      <path key={'w' + k} d={d} fill="none" stroke={C.cyan} strokeWidth="1.1"
        strokeOpacity={(0.032 + 0.036 * (0.5 + 0.5 * Math.sin(t * 0.7 + k))).toFixed(3)} />
    );
  }

  for (let i = 0; i < 96; i++) {
    const raw = hsh(i, 1) * 1920 + t * (14 + hsh(i, 2) * 26) * (1 + energy * 0.9);
    const x = ((raw % 2400) + 2400) % 2400 - 240;
    const y = hsh(i, 3) * 1080 + 18 * Math.sin(t * 0.6 + i);
    const dx = 8 + hsh(i, 4) * 22;
    const dy = (hsh(i, 5) - 0.5) * 8;
    const col = [C.cyan, C.gold, C.purple, C.white][i % 4];
    nodes.push(
      <g key={'p' + i} opacity={(0.45 + 0.5 * hsh(i, 6)).toFixed(2)}>
        <line x1={x - dx} y1={y - dy} x2={x} y2={y} stroke={col} strokeOpacity="0.22" strokeWidth="1" />
        <circle cx={x} cy={y} r={(0.8 + hsh(i, 7) * 1.6).toFixed(2)} fill={col} fillOpacity="0.5" />
      </g>
    );
  }

  return (
    <svg viewBox="0 0 1920 1080" width="1920" height="1080" style={SVG_STYLE}>
      <defs>
        <radialGradient id="engineHalo" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={C.cyan} stopOpacity="0.145" />
          <stop offset="48%" stopColor={C.cyan} stopOpacity="0.042" />
          <stop offset="100%" stopColor={C.cyan} stopOpacity="0" />
        </radialGradient>
      </defs>
      <ellipse
        cx={(960 + 74 * Math.sin(t * 0.17)).toFixed(1)}
        cy={(520 + 40 * Math.sin(t * 0.13)).toFixed(1)}
        rx={(720 + 95 * Math.sin(t * 0.33)).toFixed(1)}
        ry={(440 + 64 * Math.sin(t * 0.29 + 1)).toFixed(1)}
        fill="url(#engineHalo)" opacity="0.85" />
      {nodes}
    </svg>
  );
};

/** 上层：常驻扫描带 + 段间光帘 + 每个演算刻度一次扩散脉冲。 */
export const Overlay = ({t}) => {
  const s = evaluate(t);
  const scanX = -500 + s.scanProgress * (1920 + 1000);

  const wipes = s.wipes.map(w => (
    <rect key={'w' + w.seg}
      x={(-700 + w.p * (1920 + 1400)).toFixed(1)} y="0" width="540" height="1080"
      fill="url(#engineWipe)" opacity={(Math.sin(w.p * Math.PI) * 0.8).toFixed(3)} />
  ));

  const pulses = s.pulses.map(p => (
    <circle key={'u' + p.i} cx="960" cy="540"
      r={(20 + p.p * 520).toFixed(1)} fill="none" stroke={C.cyan}
      strokeOpacity={((1 - p.p) * 0.30).toFixed(3)}
      strokeWidth={(2.2 * (1 - p.p) + 0.4).toFixed(2)} />
  ));

  return (
    <svg viewBox="0 0 1920 1080" width="1920" height="1080" style={SVG_STYLE}>
      <defs>
        <linearGradient id="engineScan" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor={C.cyan} stopOpacity="0" />
          <stop offset="38%" stopColor={C.cyan} stopOpacity="0.095" />
          <stop offset="50%" stopColor="#E8EEF9" stopOpacity="0.175" />
          <stop offset="62%" stopColor={C.cyan} stopOpacity="0.095" />
          <stop offset="100%" stopColor={C.cyan} stopOpacity="0" />
        </linearGradient>
        <linearGradient id="engineWipe" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0%" stopColor={C.cyan} stopOpacity="0" />
          <stop offset="40%" stopColor={C.cyan} stopOpacity="0.10" />
          <stop offset="50%" stopColor="#FFFFFF" stopOpacity="0.21" />
          <stop offset="60%" stopColor={C.gold} stopOpacity="0.10" />
          <stop offset="100%" stopColor={C.gold} stopOpacity="0" />
        </linearGradient>
      </defs>
      <rect x={scanX.toFixed(1)} y="0" width={TRACKS.scan.width} height="1080"
        fill="url(#engineScan)" opacity="0.8" />
      {wipes}
      {pulses}
    </svg>
  );
};
