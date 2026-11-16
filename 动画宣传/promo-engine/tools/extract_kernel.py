# -*- coding: utf-8 -*-
"""
一次性迁移工具：把 v2 手写片源的「内容层」逐字抽进 Remotion 工程。

产出：
  src/data.js          —— 四表 + 颜色/字体常量，作为新引擎唯一数据源
  src/legacy/kernel.js —— 场景几何 + 演算逐步呈现（内容内核），不含任何运动层

刻意不迁移的部分（由新引擎接管）：
  v2 的 158–327 行 MOTION ENGINE（流场/镜头/转场/动态排版/局部形变）
  renderAt 内的 motionAt(t) / typeAt(t,c) / 进度 UI
  1021 行之后的 OfflineAudioContext 与播放控制

运行：在仓库根目录执行  C:/Python314/python.exe 动画宣传/promo-engine/tools/extract_kernel.py
"""
import io
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SOURCE = os.path.join(ROOT, '动画宣传', 'promo-engine', 'reference', 'CQM_宣传动画_v2.html')
ENGINE = os.path.join(ROOT, '动画宣传', 'promo-engine')

lines = io.open(SOURCE, encoding='utf-8').read().split('\n')


def seg(a, b):
    """1-indexed inclusive"""
    return '\n'.join(lines[a - 1:b])


# ---------- 前置断言：行号若漂移，立即中止 ----------
assert lines[20].strip().startswith('<svg id="stage"'), 'skeleton 起点漂移'
assert lines[68].strip() == '</svg>', 'skeleton 终点漂移'
assert lines[77].strip() == '(function(){', '脚本起点漂移'
assert lines[90].strip().startswith('const C='), '配色常量漂移'
assert lines[103].strip() == 'function E(tag,attrs,parent){', 'SVG 工具集漂移'
assert lines[327].strip().startswith('const S1='), '场景层起点漂移'
assert seg(328, 760).count('=(function(){') == 6, '场景函数数量漂移'
assert seg(328, 760).count('})();') == 6, '场景闭包数量漂移'
assert lines[771].strip().startswith('const OPS='), '演算刻度漂移'
assert lines[775].strip().startswith('const SEGS='), '段表漂移'
assert lines[784].strip().startswith('const CAPS='), '字幕表漂移'
assert lines[856].strip() == 'function renderAt(t){', 'renderAt 起点漂移'
assert lines[1016].strip() == '}', 'wedgesShift 终点漂移'
assert lines[1023].strip().startswith('const SCORE='), '声场表漂移'
assert lines[1056].strip() == '];', '声场表终点漂移'

# 背景板改为透明，让新引擎的流场层位于内容层之下
skeleton = seg(21, 69)
assert skeleton.count('<rect width="1920" height="1080" fill="url(#bg)"/>') == 1
skeleton = skeleton.replace(
    '<rect width="1920" height="1080" fill="url(#bg)"/>',
    '<rect width="1920" height="1080" fill="none"/>')
# UI 常驻标记不属于镜头层：移出 #camera，避免推拉时被放大裁到画面外。
carry_inside = '''    <g id="s4"></g><g id="s5"></g><g id="s6"></g>
    <g id="carry"></g>
  </g>
  <g id="rail"></g>'''
carry_outside = '''    <g id="s4"></g><g id="s5"></g><g id="s6"></g>
  </g>
  <g id="carry"></g>
  <g id="rail"></g>'''
assert skeleton.count(carry_inside) == 1, 'carry 层结构漂移'
skeleton = skeleton.replace(carry_inside, carry_outside)

# ---------- data.js：唯一数据源 ----------
DATA_BLOCKS = [
    ('C', seg(91, 92)),
    ('MATH', seg(93, 97)),
    ('RAIL', seg(766, 766)),
    ('OPS', seg(772, 773)),
    ('SEGS', seg(776, 783)),
    ('B', seg(784, 784)),
    ('CAPS', seg(785, 832)),
    ('SCORE', seg(1024, 1057)),
]
data_parts = [
    '// 由 tools/extract_kernel.py 从 v2 片源逐字提取。勿手改：口径门禁以此为准。',
    '// 内容内核与新引擎共用这一份数据，不存在第二份字幕/刻度/声场表。',
    '',
]
for name, block in DATA_BLOCKS:
    head = 'const %s' % name
    assert block.startswith(head), '%s 抽取起点不符' % name
    if name == 'MATH':
        # 这一块含 MATH / MONO / ZH / SYM / TOTAL 五个常量，逐行导出
        for ln in block.split('\n'):
            assert ln.startswith('const '), 'MATH 块内出现非常量行'
            data_parts.append('export ' + ln)
    else:
        data_parts.append('export ' + block)
    data_parts.append('')
data_parts.append('export const FPS = 60;')
data_parts.append('export const DURATION_IN_FRAMES = TOTAL * FPS;')
data_parts.append('')
io.open(os.path.join(ENGINE, 'src', 'data.js'), 'w', encoding='utf-8', newline='\n').write('\n'.join(data_parts))

# ---------- renderAt 改写：剥离运动层调用 ----------
render = seg(857, 1017)
assert render.count('const seg=motionAt(t);') == 1
render = render.replace('const seg=motionAt(t);', 'const seg=segIndex(t);')
assert render.count('  typeAt(t,c);') == 1
render = render.replace('  typeAt(t,c);', '')
ui_block = '''  if(!RAW){fill.style.width=(t/TOTAL*100).toFixed(3)+"%";
    const mm=Math.floor(t/60),ss=t-mm*60;
    clockEl.textContent=mm+":"+(ss<10?"0":"")+ss.toFixed(1)+" / 3:00";}'''
assert render.count(ui_block) == 1
render = render.replace(ui_block, '')
assert 'motionAt' not in render and 'typeAt' not in render and 'RAW' not in render

# ---------- kernel.js ----------
kit = seg(104, 151)
scenes = seg(328, 760)
carry_and_ticks = seg(761, 771)
badge_and_segop = seg(833, 856)

body = '\n'.join([
    'function createKernel(container, DATA){',
    '  const q = id => container.querySelector("#"+id);',
    '  container.innerHTML = SKELETON;',
    '  const NS="http://www.w3.org/2000/svg";',
    '  const svg=q("stage");',
    '  const G=[1,2,3,4,5,6].map(i=>q("s"+i));',
    '  const carryG=q("carry"), railG=q("rail"), badgeG=q("badge");',
    '  const capMain=q("capMain"), capSub=q("capSub"), segLabel=q("segLabel");',
    '  const cameraG=q("camera"), fieldG=q("field"), overlayG=q("overlay");',
    '  const {C,MATH,MONO,ZH,SYM,TOTAL,OPS,SEGS,B,CAPS}=DATA;',
    '',
    seg(99, 102),          # clamp / lerp / easeOut / easeIO
    '',
    kit,                   # E / T / FT / vis / group / smallLabel
    '',
    scenes,                # S1..S6：场景几何，逐字不动
    '',
    carry_and_ticks,       # ☯ 常驻标记 + 刻度尺刻度
    '',
    badge_and_segop,       # 徽章绘制 + 段淡入淡出
    '',
    '  function segIndex(t){let k=0;for(let i=0;i<6;i++)if(t>=SEGS[i].a)k=i;return k;}',
    '',
    render,                # 演算逐步呈现（已剥离运动层）
    '',
    '  return {render:renderAt, svg, G, cameraG, fieldG, overlayG,',
    '    capMain, capSub, badgeG, segLabel, carryG, railG,',
    '    CAPS, SEGS, OPS, B, C, TOTAL, S1, S2, S3, S4, S5, S6};',
    '}',
    '',
    'export {createKernel};',
    '',
])

header = '\n'.join([
    '// 内容内核：由 tools/extract_kernel.py 从 v2 片源逐字提取。',
    '// 只负责「场景几何 + 演算逐步呈现」；镜头、流场、转场、字幕入场、',
    '// 音画同步、渲染与验收一概不在这里，全部由 src/engine 承担。',
    '// 请勿手改本文件；改动内容口径请回到上屏白名单并重新抽取。',
    '',
])
skel_literal = 'export const SKELETON = ' + json.dumps(skeleton, ensure_ascii=False) + ';\n\n'
io.open(os.path.join(ENGINE, 'src', 'legacy', 'kernel.js'), 'w', encoding='utf-8', newline='\n').write(
    header + skel_literal + body)

print('data.js      ', os.path.getsize(os.path.join(ENGINE, 'src', 'data.js')), 'bytes')
print('legacy/kernel.js', os.path.getsize(os.path.join(ENGINE, 'src', 'legacy', 'kernel.js')), 'bytes')
print('skeleton chars', len(skeleton))
print('MIGRATION_OK')
