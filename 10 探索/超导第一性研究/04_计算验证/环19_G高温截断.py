# -*- coding: utf-8 -*-
"""环 19/目标区：G(y) 的高温截断与 t_Upsilon 出口（第 158 轮，R-167）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_G高温截断.py"（本目录）
输出：环19_G高温截断.png / .json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PC0 = 0.592746
NU = 9.0
TU = 1.3
A = np.pi ** 2 / 3.0
TC = 0.3
XC = 4.5
DELTA = 0.0
PCE = PC0 - DELTA
INVP = float(chi2.isf(PCE, NU))


def w(x, n=20001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)


def p_of_y(y, xc=XC):
    return 1.0 - chi2.cdf(xc * WC / y, NU)


def Phi(p):
    return 0.0 if p <= PCE else ((p - PCE) / (1.0 - PCE)) ** TU


def G(y, xc=XC):
    p = p_of_y(y, xc)
    if p <= PCE:
        return 0.0
    p1 = p_of_y(1.0, xc)
    return y * Phi(p) / Phi(p1)


YSTAR = XC * WC / INVP
TSTAR = brentq(lambda t: w(t) - YSTAR, TC, 5.0, xtol=1e-13)


def B(xc):
    h0 = xc * WC
    p0 = 1.0 - chi2.cdf(h0, NU)
    return TU * h0 * chi2.pdf(h0, NU) / (p0 - PCE)


checks = {}

# ---- C1 w 单调减 ----
ts = np.linspace(0.01, 3.0, 60)
wv = np.array([w(float(t)) for t in ts])
checks["C1_w_strict_decrease"] = bool(np.all(np.diff(wv) < 0))
assert np.all(np.diff(wv) < 0)

# ---- C2 y* 公式核对 ----
yroot = brentq(lambda y: p_of_y(y) - PCE, 0.05, 1.0, xtol=1e-13)
checks["C2_ystar_formula"] = YSTAR
checks["C2_ystar_root"] = yroot
assert abs(YSTAR - yroot) < 1e-12

# ---- C3 T* > Tc ----
checks["C3_Tstar"] = TSTAR
checks["C3_Tc"] = TC
assert TSTAR > TC

# ---- C4 G 有限支撑与单调 ----
ys = np.linspace(0.1, 1.0, 100)
gv = np.array([G(float(y)) for y in ys])
checks["C4_G_below_zero"] = bool(G(YSTAR * 0.5) == 0.0)
checks["C4_G_above_pos"] = bool(G(YSTAR * 1.1) > 0.0)
checks["C4_G_monotone_above"] = bool(np.all(np.diff(gv[ys > YSTAR]) > 0))
assert G(YSTAR * 0.5) == 0.0 and G(YSTAR * 1.1) > 0.0
assert np.all(np.diff(gv[ys > YSTAR]) > 0)

# ---- C5 截断局部指数 -> tU ----
slopes = []
for dy in (1e-2, 1e-3, 1e-4):
    y1, y2 = YSTAR + dy, YSTAR + 2 * dy
    slopes.append(np.log(G(y2) / G(y1)) / np.log(2.0))
checks["C5_local_exponents"] = slopes
assert abs(slopes[-1] - TU) < 1e-3

# ---- C6 一阶导趋零（tU>1） ----
ders = []
for dy in (1e-3, 1e-4, 1e-5):
    ders.append((G(YSTAR + 2 * dy) - G(YSTAR + dy)) / dy)
checks["C6_first_derivatives"] = ders
assert abs(ders[-1]) < abs(ders[0])

# ---- C7 两个 x_c 通路一致 ----
xc_low = brentq(lambda x: B(x) - (A * (1 + B(XC)) / A - 1), 1.5, 6.0, xtol=1e-13)
xc_high = YSTAR * INVP / WC
checks["C7_xc_low"] = xc_low
checks["C7_xc_high"] = xc_high
assert abs(xc_low - xc_high) < 1e-10

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ax = axes[0, 0]
ax.plot(ts, wv)
ax.axvline(TC, color="g", ls="--", label="T_c")
ax.axvline(TSTAR, color="r", ls="--", label="T_*")
ax.set(xlabel="T/w_D", ylabel="w", title="(a) Debye 权重与两尺度")
ax.legend(fontsize=8)

ax = axes[0, 1]
ax.plot(ys, gv)
ax.axvline(YSTAR, color="r", ls="--", label="y_*")
ax.set(xlabel="y=w(T)", ylabel="G(y)", title="(b) 有限支撑")

ax = axes[0, 2]
dys = np.logspace(-4, -1.5, 30)
sl = []
for dy in dys:
    y1, y2 = YSTAR + dy, YSTAR + 2 * dy
    sl.append(np.log(G(y2) / G(y1)) / np.log(2.0))
ax.plot(dys, sl, "o-")
ax.axhline(TU, color="r", ls="--", label="t_U=1.3")
ax.set(xlabel="y-y_*", ylabel="局部指数", title="(c) 截断幂律")
ax.legend(fontsize=8)

ax = axes[1, 0]
ax.plot([1e-3, 1e-4, 1e-5], ders, "o-")
ax.set(xlabel="dy", ylabel="G'(y_*+dy)", title="(d) 一阶导趋零")

ax = axes[1, 1]
xcs = np.linspace(3.0, 6.0, 40)
tss = []
for xc in xcs:
    ys0 = xc * WC / INVP
    tss.append(brentq(lambda t: w(t) - ys0, 0.3, 5.0, xtol=1e-10))
ax.plot(xcs, tss, "o-")
ax.set(xlabel="x_c", ylabel="T_*/w_D", title="(e) 截断温度随 x_c")

ax = axes[1, 2]
ax.bar(["低温曲率", "高温截断"], [xc_low, xc_high], color=["tab:blue", "tab:red"])
ax.set(ylabel="x_c", title="(f) 两通路一致")

fig.tight_layout()
fig.savefig("环19_G高温截断.png", dpi=150)
with open("环19_G高温截断.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
