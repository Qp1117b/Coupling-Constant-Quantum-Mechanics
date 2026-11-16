import React from 'react';
import {Composition} from 'remotion';
import {Spike} from './Spike';
import {CQMPromo} from './CQMPromo';

export const RemotionRoot = () => (
  <>
    <Composition
      id="CQMSpike"
      component={Spike}
      durationInFrames={180}
      fps={60}
      width={1920}
      height={1080}
    />
    <Composition
      id="CQMPromo"
      component={CQMPromo}
      durationInFrames={10800}
      fps={60}
      width={1920}
      height={1080}
    />
  </>
);
