import React, {useLayoutEffect, useRef, useState} from 'react';
import {AbsoluteFill, Audio, staticFile, useCurrentFrame} from 'remotion';
import * as DATA from './data.js';
import {createKernel} from './legacy/kernel.js';
import {evaluate, applyToKernel} from './engine/tracks.js';
import {FlowField, Overlay} from './engine/layers.jsx';

/**
 * 组装层。三条职责严格分离：
 *   kernel.render(t)  —— 内容内核：场景几何与演算逐步呈现（逐字迁移，口径零改动）
 *   evaluate(t)       —— 新引擎：镜头/流场/转场/字幕/脉冲，全部来自声明式 Track 表
 *   <Audio>           —— 同一条时间轴上的母带，不再有第二条音画对齐管线
 */
export const CQMPromo = () => {
  const frame = useCurrentFrame();
  const t = frame / DATA.FPS;
  const hostRef = useRef(null);
  const kernelRef = useRef(null);
  const [, bump] = useState(0);

  useLayoutEffect(() => {
    if (!kernelRef.current && hostRef.current) {
      kernelRef.current = createKernel(hostRef.current, DATA);
      bump(x => x + 1);
    }
  }, []);

  useLayoutEffect(() => {
    if (!kernelRef.current) return;
    kernelRef.current.render(t);
    applyToKernel(kernelRef.current, evaluate(t));
  }, [t]);

  return (
    <AbsoluteFill style={{backgroundColor: '#070A12', overflow: 'hidden'}}>
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 46% 40%, #0A0F1A 0%, #070A12 100%)',
      }} />
      <FlowField t={t} />
      <div ref={hostRef} style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}} />
      <Overlay t={t} />
      <Audio src={staticFile('master.wav')} />
    </AbsoluteFill>
  );
};
