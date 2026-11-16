import wave, array, math, sys

path = r'D:\WorkSpace\物理\CQMFormal\动画宣传\S0_舞台与量子\master.wav'
w = wave.open(path, 'rb')
sr = w.getframerate(); n = w.getnframes(); ch = w.getnchannels()
raw = w.readframes(n); w.close()
a = array.array('h'); a.frombytes(raw)
mono = array.array('f', [0.0]) * n
for i in range(n):
    mono[i] = (a[2*i] + a[2*i+1]) / 65536.0

def rms(t0, dur):
    i0 = max(0, int(t0*sr)); i1 = min(n, int((t0+dur)*sr))
    if i1 <= i0: return 0.0
    s = 0.0
    for i in range(i0, i1):
        v = mono[i]; s += v*v
    return math.sqrt(s/(i1-i0))

peak = max(abs(x) for x in mono)
dc = sum(mono)/n
print('sr', sr, 'frames', n, 'peak', round(peak,4), 'dc', round(dc,5))
keys = [0,3,7,12,14.2,20,24.5,31.5,32,33,38,45,52.6,57.5,60,66.2,70,74,78,84,86,88,89.5]
for t in keys:
    print(f'{t:5.1f}  rms={rms(t,0.5):.4f}')

# 0.5s grid summary: quiet and loud windows
vals = [(t, rms(t,0.5)) for t in [i*0.5 for i in range(180)]]
quiet = [t for t,v in vals if v < 0.01]
loud = sorted(vals, key=lambda x: -x[1])[:12]
print('quiet windows (<0.01):', len(quiet), quiet[:40])
print('loudest:', [(round(t,1), round(v,3)) for t,v in loud])

# stereo difference energy (width)
diff = 0.0; tot = 0.0
for i in range(n):
    l = a[2*i]/32768.0; r = a[2*i+1]/32768.0
    diff += (l-r)*(l-r); tot += (l*l+r*r)/2
print('stereo diff ratio', round(math.sqrt(diff/max(tot,1e-12)),3))

# 1/3-octave-ish band energy via simple Goertzel at key freqs
def goertzel(f, t0, dur):
    i0=int(t0*sr); i1=min(n,int((t0+dur)*sr))
    if i1<=i0: return 0
    wf=2*math.pi*f/sr; c=2*math.cos(wf); s0=s1=0.0
    for i in range(i0,i1):
        s0=mono[i]+c*s1-s0*0; s1=s0
    # crude: not used
    return 0
print('done')
