# -*- coding: utf-8 -*-
"""成片级自动验收：解码、帧数、时长、运动量、静帧、黑帧、分段死角、抽帧接触表。
用法： C:/Python314/python.exe tools/verify.py [mp4路径]
任何硬门禁不过即 exit 1。"""
import os
import re
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..'))
FF = os.path.join(REPO, '.workbuddy', 'anim-render', 'node_modules', 'ffmpeg-static', 'ffmpeg.exe')
DEFAULT_MP4 = os.path.join(ROOT, 'out', 'promo-v3.mp4')
MP4 = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_MP4
OUT = os.path.join(ROOT, 'out', 'verify')
os.makedirs(OUT, exist_ok=True)

fails = []
def ok(cond, label):
    if not cond:
        fails.append(label)

if not os.path.exists(MP4):
    print('VERIFY_FAIL 成片不存在:', MP4)
    sys.exit(1)

# V1 完整解码
r = subprocess.run([FF, '-hide_banner', '-i', MP4, '-f', 'null', '-'],
                   capture_output=True, text=True, timeout=600)
info = r.stderr
ok(r.returncode == 0, 'V1 全片解码退出码 %d' % r.returncode)
m = re.search(r'frame=\s*(\d+)', info)
frames = int(m.group(1)) if m else -1
ok(frames == 10800, 'V1 帧数 %d ≠ 10800' % frames)
d = re.search(r'Duration:\s*(\d+):(\d+):([\d.]+)', info)
secs = (int(d.group(1)) * 3600 + int(d.group(2)) * 60 + float(d.group(3))) if d else -1
ok(abs(secs - 180.0) < 0.2, 'V1 时长 %.2fs ≠ 180s' % secs)
streams = [ln.strip() for ln in info.splitlines() if 'Stream #' in ln]
ok(any('Video:' in s and '1920x1080' in s for s in streams), 'V1 视频非 1920x1080')
ok(any('Audio:' in s for s in streams), 'V1 缺音轨')

# V2 1fps 帧差 / 静帧 / 黑帧 / 分段死角
W, H = 160, 90
p = subprocess.run([FF, '-v', 'error', '-i', MP4,
                    '-vf', 'fps=1,scale=%d:%d' % (W, H),
                    '-pix_fmt', 'rgb24', '-f', 'rawvideo', '-'],
                   capture_output=True, timeout=600)
a = np.frombuffer(p.stdout, dtype=np.uint8).reshape(-1, H, W, 3).astype(np.int16)
diff = np.abs(np.diff(a, axis=0)).mean(axis=(1, 2, 3))
mean_diff = float(diff.mean())
static_ratio = float((diff < 1.0).mean())
lum = a.mean(axis=(1, 2, 3))
black = int((lum < 3).sum())

ok(len(a) >= 178, 'V2 抽帧仅 %d 帧' % len(a))
ok(mean_diff >= 2.0, 'V2 运动量不足：均值 %.2f < 2.0' % mean_diff)
ok(static_ratio < 0.15, 'V2 静止帧过多：%.0f%%' % (100 * static_ratio))
ok(black == 0, 'V2 黑帧 %d 个' % black)
segmeans = []
for i in range(0, 180, 30):
    seg = diff[i:i + 30]
    segmeans.append(float(seg.mean()))
    ok(seg.mean() >= 1.5, 'V2 第 %d–%d s 运动死角 %.2f' % (i, i + 30, seg.mean()))

# V3 抽 9 帧接触表（供最后一次目视）
TS = [1, 24, 53, 76, 86, 118, 147, 164, 178]
CW, CH = 480, 270
sheet = Image.new('RGB', (3 * CW, 3 * (CH + 22)), (20, 25, 36))
draw = ImageDraw.Draw(sheet)
for i, t in enumerate(TS):
    f = os.path.join(OUT, 'mp4_%03d.png' % t)
    subprocess.run([FF, '-y', '-loglevel', 'error', '-ss', str(t), '-i', MP4,
                    '-frames:v', '1', f], check=True, timeout=90)
    im = Image.open(f).convert('RGB').resize((CW, CH))
    x, y = (i % 3) * CW, (i // 3) * (CH + 22)
    sheet.paste(im, (x, y))
    draw.text((x + 6, y + CH + 4), 'mp4 %ds' % t, fill=(200, 210, 230))
sheet.save(os.path.join(OUT, '_contact.png'))

size_mb = os.path.getsize(MP4) / 1024 / 1024
print('===== CQM 宣传动画 · 成片级验收 =====')
print('  文件        %s (%.2f MB)' % (os.path.basename(MP4), size_mb))
print('  V1 解码     rc=%d, %d 帧, %.2fs, 1920x1080 + 音轨' % (r.returncode, frames, secs))
print('  V2 运动量   均值 %.2f / 中位 %.2f / 最大 %.2f' %
      (mean_diff, float(np.median(diff)), float(diff.max())))
print('  V2 静止帧   %.1f%%   黑帧 %d' % (100 * static_ratio, black))
print('  V2 分段     ' + ' '.join('%.2f' % v for v in segmeans))
print('  V3 接触表   %s' % os.path.join(OUT, '_contact.png'))
if fails:
    for f in fails:
        print('  FAIL  ' + f)
    print('VERIFY_FAIL %d 项' % len(fails))
    sys.exit(1)
print('VERIFY_PASS  0 failures')
