import wave, array, math

p = r'D:\WorkSpace\物理\CQMFormal\动画宣传\S0_舞台与量子\master.wav'
w = wave.open(p, 'rb')
sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
raw = array.array('h'); raw.frombytes(w.readframes(n)); w.close()
L = raw[0::2]; R = raw[1::2]
peak = max(max(L), max(R)) / 32768.0
mean = sum(L) / len(L) / 32768.0
win = int(sr * 0.05)
rms = []
for i in range(0, n - win + 1, win):
    seg = L[i:i+win]
    s = sum(x*x for x in seg) / len(seg)
    rms.append((i / sr, math.sqrt(s) / 32768.0))

def db(x): return 20 * math.log10(x) if x > 0 else -120
print('sr', sr, 'frames', n, 'dur', n/sr, 'ch', ch)
print('peak', round(peak, 4), 'peak_dbfs', round(db(peak), 2), 'dc', round(mean, 5))
print('rms_dbfs', round(db(sum(x for _, x in rms)/len(rms)), 2))
top = sorted(rms, key=lambda t: t[1], reverse=True)[:18]
print('TOP RMS')
for t, v in sorted(top): print(f'  {t:6.2f}s {db(v):7.2f} dB')
# silence runs > 0.25 s below -40 dBFS
runs = []; start = None
for t, v in rms:
    if v < 0.01 and db(v) < -40:
        if start is None: start = t
    else:
        if start is not None and t - start >= 0.25: runs.append((start, t))
        start = None
if start is not None and n/sr - start >= 0.25: runs.append((start, n/sr))
print('SILENCE >0.25s')
for a, b in runs: print(f'  {a:6.2f} - {b:6.2f}  ({b-a:.2f}s)')
# report level around key ops
print('OPS LEVELS')
for t in [0, 7, 12, 14.2, 20, 24.5, 32, 38, 45, 52.6, 57.5, 66.2, 74, 78.6, 84, 88]:
    idx = min(range(len(rms)), key=lambda i: abs(rms[i][0] - t))
    print(f'  {t:5.1f}s {db(rms[idx][1]):7.2f} dB')
