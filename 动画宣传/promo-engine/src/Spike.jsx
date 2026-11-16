import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';

export const Spike = () => {
  const f = useCurrentFrame();
  const x = interpolate(f, [0, 180], [120, 1360], {extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{backgroundColor: '#0B1018', color: '#E8EEF9', fontSize: 76, fontFamily: 'sans-serif'}}>
      <div style={{transform: `translateX(${x}px)`, marginTop: 420, whiteSpace: 'nowrap'}}>
        CQM 引擎重构 · 帧 {f}
      </div>
    </AbsoluteFill>
  );
};
