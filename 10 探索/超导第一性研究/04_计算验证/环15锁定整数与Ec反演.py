# -*- coding: utf-8 -*-
"""环 15：`审-6` 锁定整数与 E_c/gamma 反演（第 159 轮，R-168）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环15锁定整数与Ec反演.py"（本目录）
输出：环15锁定整数与Ec反演.png / .json
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

PC = 0.592746
NU = 9.0
TU = 1.3
TC = 0.3
XC = 4.5
G = 0.622281
BETA_K = 0.89294
YBOUND = 2.0 * np.pi * np.exp(-np.pi ** 2 / (2.0 * BETA_K))


def w(x, n=20001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
Phi = lambda p: ((p - PC) / (1 - PC)) ** TU
phic = 1.0 - chi2.cdf(XC, NU)
PHIC = Phi(phic)
PHI0 = Phi(1.0 - chi2.cdf(XC * WC, NU))
KAP = G * PHIC
UPS0 = 2.0 * TC / (np.pi * WC * KAP)      # Upsilon_0 = Upsilon_bond
U0 = UPS0 * PHI0
EC = np.pi ** 2 * UPS0 / 2.0
GAMMA = UPS0                              # omega_D = 1


def y_of(t, ec=EC):
    if t <= 0:
        return 0.0
    return 2.0 * np.pi * np.exp(-ec / t)


def p_pair(t):
    return 1.0 - chi2.cdf(XC * WC / w(t), NU)


def p_sync(t):
    return p_pair(t) * (1.0 - y_of(t))


checks = {}

# ---- C1 锁定分解 ----
ts = np.linspace(0.05, 1.2, 60)
ps = np.array([p_sync(float(t)) for t in ts])
pp = np.array([p_pair(float(t)) for t in ts])
checks["C1_sync_le_pair"] = bool(np.all(ps <= pp))
assert np.all(ps <= pp)

# ---- C2 逸度单调 ----
ys = np.array([y_of(float(t)) for t in ts])
checks["C2_y_monotone"] = bool(np.all(np.diff(ys) > 0))
assert np.all(np.diff(ys) > 0)

# ---- C3 两阈值抬升与 T_sync<T_* ----
YTC = y_of(TC)
thr_sync = PC / (1.0 - YTC)
checks["C3_threshold_uplift"] = thr_sync - PC
assert thr_sync > PC
TSTAR = brentq(lambda t: p_pair(t) - PC, TC, 2.0, xtol=1e-12)
TSYNC = brentq(lambda t: p_pair(t) - PC / (1.0 - y_of(t)), TC, TSTAR, xtol=1e-12)
checks["C3_Tsync"] = TSYNC
checks["C3_Tstar"] = TSTAR
checks["C3_Tc"] = TC
assert TC < TSYNC < TSTAR

# ---- C4 m=1 分支 t(T_c) 上界 ----
t_TC = 1.0 + np.log(1.0 - YTC) / np.log(phic)
checks["C4_t_Tc_m1"] = t_TC
checks["C4_bound_m1"] = 1.0509
checks["C4_bound_m2"] = 1.1072
assert 1.0 < t_TC < 1.0509

# ---- C5 E_c 与 gamma 反演 ----
checks["C5_Upsilon0"] = UPS0
checks["C5_Ec"] = EC
checks["C5_gamma"] = GAMMA
checks["C5_Phi0"] = PHI0
assert abs(EC - np.pi ** 2 * U0 / (2.0 * PHI0)) < 1e-12

# ---- C6 裸 vs 重整化 ----
EC_REN = np.pi ** 2 * (2.0 * TC / np.pi) / 2.0
y_ren = 2.0 * np.pi * np.exp(-EC_REN / TC)
checks["C6_y_bare_Tc"] = YTC
checks["C6_y_ren_Tc"] = y_ren
checks["C6_bound"] = YBOUND
assert YTC < YBOUND < y_ren

# ---- C7 E_c 随 x_c 的反演单调 ----
xcs = np.linspace(3.0, 6.0, 30)
ecs = []
for xc in xcs:
    ph = Phi(1.0 - chi2.cdf(xc, NU))
    ph0 = Phi(1.0 - chi2.cdf(xc * WC, NU))
    kap = G * ph
    ub = 2.0 * TC / (np.pi * WC * kap)
    ecs.append(np.pi ** 2 * ub / 2.0)
checks["C7_Ec_monotone"] = bool(np.all(np.diff(ecs) > 0))
checks["C7_Ec_range"] = [float(min(ecs)), float(max(ecs))]
assert np.all(np.diff(ecs) > 0)

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ax = axes[0, 0]
ax.plot(ts, ys, label="bare E_c")
ax.axhline(YBOUND, color="r", ls="--", label="BKT bound")
ax.set(xlabel="T/w_D", ylabel="y", title="(a) 逸度")
ax.legend(fontsize=8)

ax = axes[0, 1]
ax.plot(ts, pp, label="p_pair")
ax.plot(ts, ps, "--", label="p_sync")
ax.axhline(PC, color="k", ls=":", label="p_c")
ax.set(xlabel="T/w_D", ylabel="占据率", title="(b) 锁定分解")
ax.legend(fontsize=8)

ax = axes[0, 2]
ax.plot([TC, TSYNC, TSTAR], [1, 1, 1], "o-")
ax.set(xlabel="温度点", ylabel="", title="(c) T_c <= T_sync < T_*")
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["T_c", "T_sync", "T_*"])

ax = axes[1, 0]
tt = np.linspace(TC, TSYNC, 40)
tv = [1.0 + np.log(1.0 - y_of(float(t))) / np.log(p_pair(float(t))) for t in tt]
ax.plot(tt, tv, "o-", label="t(T)")
ax.axhline(1.0509, color="r", ls="--", label="m=1 bound")
ax.axhline(1.1072, color="g", ls=":", label="m=2 (excluded)")
ax.set(xlabel="T/w_D", ylabel="t", title="(d) 粗粒化指数上界")
ax.legend(fontsize=8)

ax = axes[1, 1]
ax.plot(xcs, ecs, "o-", label="E_c")
ax.set(xlabel="x_c", ylabel="E_c", title="(e) 核能反演")

ax = axes[1, 2]
ax.bar(["bare", "renorm"], [YTC, y_ren], color=["tab:blue", "tab:red"])
ax.axhline(YBOUND, color="k", ls="--", label="bound")
ax.set(ylabel="y(T_c)", title="(f) 裸/重整化判否")
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig("环15锁定整数与Ec反演.png", dpi=150)
with open("环15锁定整数与Ec反演.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
