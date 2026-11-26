# 环15_判据一元化_数值核对.py（第 201 轮，约束层旁证，不入建模层）
# 只做三件事：
#   1) 核对 r 的 Phi 闭式：r = 2 T h (1-Phi)/(1-h^2)（相对残差）
#   2) 核对判据一元化：sign(S') 与 G 的符号一致（S'<0 <-> G>0）
#   3) 给出 Phi、r、G、S' 的分点表与 S' 的变号括号
# 只用标准库。
import math

def tanh(x):
    return math.tanh(x)

def sech2(x):
    c = math.cosh(x)
    return 1.0 / (c * c)

def simpson(f, a, b, n=2000):
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    s = f(a) + f(b)
    for i in range(1, n):
        s += (4.0 if i % 2 == 1 else 2.0) * f(a + i * h)
    return s * h / 3.0

def wGap(T):
    return 2.0 * simpson(lambda u: u * tanh(u / (2.0 * T)), 0.0, 1.0)

def wGapDeriv(T):
    return -(1.0 / T**2) * simpson(lambda u: u * u * sech2(u / (2.0 * T)), 0.0, 1.0)

def h(T):
    return tanh(1.0 / (2.0 * T))

def Phi(T):
    return wGap(T) / h(T)

def ratioR(T):
    return T**2 * abs(wGapDeriv(T)) / sech2(1.0 / (2.0 * T))

def ratioR_phi(T):
    ht = h(T)
    return 2.0 * T * ht * (1.0 - Phi(T)) / (1.0 - ht * ht)

def G(T):
    ht = h(T)
    ph = Phi(T)
    return 2.0 * T * ht * (1.0 - ph) * (2.0 - ph) - ph * (1.0 - ht * ht)

def wGapDeriv2(T, eps=1e-5):
    return (wGapDeriv(T + eps) - wGapDeriv(T - eps)) / (2.0 * eps)

def shapeDeriv(T):
    w = wGap(T)
    w1 = wGapDeriv(T)
    w2 = wGapDeriv2(T)
    return (w * w2 - w1 * w1) / (w1 * w1)

Ts = [0.05 + 0.001 * i for i in range(1150)]  # 0.05 .. 1.199

# --- 1) r 的 Phi 闭式 ---
maxres = 0.0
for T in Ts:
    a = ratioR(T)
    b = ratioR_phi(T)
    den = max(abs(a), abs(b), 1e-30)
    maxres = max(maxres, abs(a - b) / den)

# --- 2) 判据一元化：S'<0 <-> G>0 ---
mism = 0
mism_list = []
for T in Ts:
    s = shapeDeriv(T)
    g = G(T)
    # 只在 |S'| 足够大、|G| 足够大处比较，避开零点数值噪声
    if abs(s) > 1e-6 and abs(g) > 1e-9:
        if (s < 0.0) != (g > 0.0):
            mism += 1
            mism_list.append((T, s, g))

# --- 3) S' 的变号括号 ---
bracket = None
prev = None
for T in Ts:
    s = shapeDeriv(T)
    if prev is not None and prev[1] * s < 0.0:
        bracket = (prev[0], T)
        break
    prev = (T, s)

print("points:", len(Ts), " T in [%.3f, %.3f]" % (Ts[0], Ts[-1]))
print("1) max relative residual |r - 2Th(1-Phi)/(1-h^2)| = %.3e" % maxres)
print("2) sign mismatches (S'<0 vs G>0) = %d" % mism)
if mism_list:
    for row in mism_list[:8]:
        print("   T=%.6f  S'=%.3e  G=%.3e" % row)
print("3) S' sign-change bracket = %s" % (str(bracket),))

for T in (0.15, 0.25, 0.30, 0.3435, 0.40, 0.50, 0.70, 0.90, 1.20):
    print("T=%.4f  Phi=%.6f  r=%.6f  G=%+.6e  S'=%+.6e  h=%.6f"
          % (T, Phi(T), ratioR(T), G(T), shapeDeriv(T), h(T)))
