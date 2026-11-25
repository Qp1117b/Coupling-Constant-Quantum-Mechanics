# -*- coding: utf-8 -*-
"""环 15/19：`审-4` 关联修正阈值接入相界与反演（第 156 轮，R-165）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环15_审4关联阈值接入相界.py"（本目录）
输出：环15_审4关联阈值接入相界.png / .json
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
G_TRUE = 0.622281
X_TRUE = 4.5


def w_debye(x, n=20001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w_debye(TC)


def Phi(p, pc=PC0):
    return 0.0 if p <= pc else ((p - pc) / (1.0 - pc)) ** TU


def p_at(xc, fac=1.0):
    return 1.0 - chi2.cdf(xc * fac, NU)


def B(xc, pc):
    h0 = xc * WC
    p0 = p_at(xc, WC)
    return TU * h0 * chi2.pdf(h0, NU) / (p0 - pc)


def csb(pc):
    return (2.0 * pc / (1.0 + pc)) ** TU


def pceff_of_delta(delta):
    return PC0 - delta


def invert(U0, c2, pc_assumed):
    Bt = c2 / A - 1.0
    xr = brentq(lambda x: B(x, pc_assumed) - Bt, 1.5, 6.0, xtol=1e-13)
    phi0r = Phi(p_at(xr, WC), pc_assumed)
    Ubr = U0 / phi0r
    kapr = 2.0 * TC * phi0r / (np.pi * U0 * WC)
    phicr = Phi(p_at(xr), pc_assumed)
    return xr, kapr / phicr, Ubr


def synth(delta):
    pc = pceff_of_delta(delta)
    phic = Phi(p_at(X_TRUE), pc)
    kap = G_TRUE * phic
    phi0 = Phi(p_at(X_TRUE, WC), pc)
    Ub = 2.0 * TC / (np.pi * WC * kap)
    U0 = Ub * phi0
    c2 = A * (1.0 + B(X_TRUE, pc))
    return pc, U0, c2, phi0, Ub, kap


checks = {}

# ---- C1 座/键近阈比收敛到 C_sb ----
deltas = np.array([1e-2, 1e-3, 1e-4, 1e-5])
ratios = []
for dp in deltas:
    p = PC0 + dp
    q = p ** 2
    qc = PC0 ** 2
    ratios.append(Phi(q, qc) / Phi(p, PC0))
checks["C1_ratio_converges_to"] = csb(PC0)
checks["C1_last_ratio"] = ratios[-1]
assert abs(ratios[-1] - csb(PC0)) < 1e-3

# ---- C2 C_sb 独立极限闭式 ----
checks["C2_csb"] = csb(PC0)
checks["C2_qc"] = PC0 ** 2
assert abs(csb(PC0) - 0.6812048570778535) < 1e-12

# ---- C3 阈值位移单调 ----
cbs = np.linspace(0.0, 0.06, 40)
pceffs = np.array([PC0 - cb / (2 * PC0) for cb in cbs])
checks["C3_pceff_range"] = [float(pceffs.min()), float(pceffs.max())]
assert np.all(np.diff(pceffs) < 0)
assert abs(pceffs[0] - PC0) < 1e-14

# ---- C4 pstar 随 pceff 单调增、xc 随之下移而上移 ----
s = (G_TRUE * Phi(p_at(X_TRUE))) ** (1 / TU)
ps = np.array([pc + (1 - pc) * s for pc in pceffs])
xcs = np.array([chi2.isf(p, NU) for p in ps])
checks["C4_s"] = s
checks["C4_pstar_monotone"] = bool(np.all(np.diff(ps) < 0))
checks["C4_xc_antitone"] = bool(np.all(np.diff(xcs) > 0))
assert s < 1 and s >= 0
assert np.all(np.diff(ps) < 0) and np.all(np.diff(xcs) > 0)

# ---- C5 反演偏差表 ----
rows = []
for d in (0.0, 0.01, 0.02, 0.05):
    pc, U0, c2, phi0, Ub, kap = synth(d)
    xr_ig, g_ig, Ub_ig = invert(U0, c2, PC0)
    xr_co, g_co, Ub_co = invert(U0, c2, pc)
    rows.append((d, g_ig, (g_ig - G_TRUE) / G_TRUE, g_co, xr_ig))
checks["C5_bias_002"] = rows[2][2]
checks["C5_correct_recover"] = rows[2][3]
checks["C5_bias_monotone"] = bool(rows[1][1] < rows[2][1] < rows[3][1])
assert abs(rows[0][1] - G_TRUE) < 1e-12
assert rows[1][1] < rows[2][1] < rows[3][1]
assert abs(rows[2][3] - G_TRUE) < 1e-10

# ---- C6 可测判据 ----
rounding = abs((2.0 / np.pi) / 1.023 - G_TRUE) / G_TRUE
bias_001 = None
pc, U0, c2, _, _, _ = synth(0.001)
_, g_001, _ = invert(U0, c2, PC0)
bias_001 = (g_001 - G_TRUE) / G_TRUE
checks["C6_rounding"] = rounding
checks["C6_bias_delta0001"] = bias_001
checks["C6_detectable"] = bool(bias_001 > rounding)
assert bias_001 > rounding

# ---- C7 自平均条件等价 ----
nvals = np.array([9.0, 100.0, 1000.0])
cb_over_n = np.array([0.02 / n for n in nvals])
deltas_sa = np.array([cb / (2 * PC0) for cb in cb_over_n])
checks["C7_delta_selfavg"] = deltas_sa.tolist()
assert np.all(deltas_sa < 0.002)

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ax = axes[0, 0]
pp = np.linspace(PC0 + 1e-6, PC0 + 0.05, 100)
ax.plot(pp, [Phi(p) for p in pp], label="Phi_site")
ax.plot(pp, [Phi(p ** 2, PC0 ** 2) for p in pp], "--", label="Phi_bond")
ax.set(xlabel="p", ylabel="Phi", title="(a) 座/键两种写法")
ax.legend(fontsize=8)

ax = axes[0, 1]
ax.semilogy(deltas, ratios, "o-", label="实测比")
ax.axhline(csb(PC0), color="r", ls="--", label="C_sb")
ax.set(xlabel="p-pc", ylabel="比", title="(b) 近阈收敛到常数")
ax.legend(fontsize=8)

ax = axes[0, 2]
ax.plot(cbs, pceffs, "o-")
ax.set(xlabel="cbar", ylabel="p_c_eff", title="(c) 阈值位移")

ax = axes[1, 0]
ax.plot(pceffs, xcs, "o-")
ax.set(xlabel="p_c_eff", ylabel="x_c", title="(d) 反解阈值上移")

ax = axes[1, 1]
ds = np.linspace(0.0, 0.05, 20)
biases = []
for d in ds:
    pc, U0, c2, _, _, _ = synth(float(d))
    _, gg, _ = invert(U0, c2, PC0)
    biases.append((gg - G_TRUE) / G_TRUE)
ax.plot(ds, biases, "o-", label="忽略关联")
ax.axhline(0, color="g", ls="--")
ax.axhline(rounding, color="r", ls=":", label="舍入残差")
ax.set(xlabel="delta", ylabel="相对偏差", title="(e) 反演偏差")
ax.legend(fontsize=8)

ax = axes[1, 2]
ax.bar(["舍入", "delta=1e-3"], [rounding, bias_001], color=["tab:blue", "tab:red"])
ax.set(ylabel="相对偏差", title="(f) 可测性")

fig.tight_layout()
fig.savefig("环15_审4关联阈值接入相界.png", dpi=150)
with open("环15_审4关联阈值接入相界.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
