# -*- coding: utf-8 -*-
"""环 15 / 审-6 第二段：锁定概率的键级复合与指数单调（第 163 轮）

只做解析式在工作点的数值核对与函数图像，不做拟合。
运行：python "环15锁定概率复合_两分支核对.py"（本目录）
输出：环15锁定概率复合_两分支核对.json / .png
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
KAP = G * Phi(phic)
UPS0 = 2.0 * TC / (np.pi * WC * KAP)
EC = np.pi ** 2 * UPS0 / 2.0

y_of = lambda t: 0.0 if t <= 0 else 2.0 * np.pi * np.exp(-EC / t)
p_pair = lambda t: 1.0 - chi2.cdf(XC * WC / w(t), NU)
t_m = lambda t, m: 1.0 + m * np.log(1.0 - y_of(t)) / np.log(phic)
p_sync_m = lambda t, m: p_pair(t) * (1.0 - y_of(t)) ** m

out = {}
YTC = y_of(TC)
out["p_at_Tc"] = phic
out["y_at_Tc"] = YTC
out["t_m1_at_Tc"] = t_m(TC, 1)
out["t_m2_at_Tc"] = t_m(TC, 2)
out["ratio_excess"] = (t_m(TC, 2) - 1.0) / (t_m(TC, 1) - 1.0)   # 应为 2
out["p_sync_m1_at_Tc"] = p_sync_m(TC, 1)
out["p_sync_m2_at_Tc"] = p_sync_m(TC, 2)
out["p_sync_drop"] = p_sync_m(TC, 1) - p_sync_m(TC, 2)
out["thr_m1"] = PC / (1.0 - YTC)
out["thr_m2"] = PC / (1.0 - YTC) ** 2

# 已登记两界 1.0509 / 1.1072 的反解 p：若二者是同一点的两支，应互为 2 倍
# 这两个界对应的是 BKT 界 y <= 0.025007 处的上限（不是工作点 y(T_c)=1.4e-4）
def p_for_bound(bound, y=YBOUND):
    return float(np.exp(np.log(1.0 - y) / (bound - 1.0)))


out["p_reverse_from_1p0509"] = p_for_bound(1.0509)
out["p_reverse_from_1p1072"] = p_for_bound(1.1072)
out["bound_m1"] = 1.0509
out["bound_m2"] = 1.1072
out["two_times_m1_excess"] = 1.0 + 2.0 * (1.0509 - 1.0)   # = 1.1018 ≠ 1.1072

# 两界的正确构造：y 取 BKT 界，p 取被抬升到 p_c 的配对阈值（m 支各自抬升 m 次）
p_raise1 = PC / (1.0 - YBOUND)
p_raise2 = PC / (1.0 - YBOUND) ** 2
out["p_raise_m1"] = p_raise1
out["p_raise_m2"] = p_raise2
out["t_bound_recompute_m1"] = 1.0 + np.log(1.0 - YBOUND) / np.log(p_raise1)
out["t_bound_recompute_m2"] = 1.0 + 2.0 * np.log(1.0 - YBOUND) / np.log(p_raise2)
out["bound_m1_matches"] = bool(abs(out["t_bound_recompute_m1"] - 1.0509) < 2e-3)
out["bound_m2_matches"] = bool(abs(out["t_bound_recompute_m2"] - 1.1072) < 2e-3)

# 单调性：扫描 T（只取 y 未下溢的区间，T->0 时 y 在双精度下精确为 0），
# 验证 t(m=2) > t(m=1) 且 p_sync(m=2) < p_sync(m=1)
ts = np.linspace(0.15, 1.1, 80)
ys = np.array([y_of(float(t)) for t in ts])
out["frac_y_underflow_to_zero"] = float(np.mean(ys == 0.0))
t1 = np.array([t_m(float(t), 1) for t in ts])
t2 = np.array([t_m(float(t), 2) for t in ts])
s1 = np.array([p_sync_m(float(t), 1) for t in ts])
s2 = np.array([p_sync_m(float(t), 2) for t in ts])
out["t_monotone_strict"] = bool(np.all(t2 > t1))
out["psync_m2_lt_m1"] = bool(np.all(s2 < s1))
out["t_m1_minus_1_at_scan"] = [float(t1.min() - 1.0), float(t1.max() - 1.0)]

# 由 p_sync(m) > p_c 反解 T_sync(m)，m=2 应严格更低温
def solve_tsync(m):
    f = lambda t: p_sync_m(t, m) - PC
    return brentq(f, TC, 1.5, xtol=1e-12)
out["T_sync_m1"] = solve_tsync(1)
out["T_sync_m2"] = solve_tsync(2)
out["T_star"] = brentq(lambda t: p_pair(t) - PC, TC, 2.0, xtol=1e-12)
out["Tsync_m2_lt_m1"] = bool(out["T_sync_m2"] < out["T_sync_m1"])

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ax.plot(ts, [y_of(float(t)) for t in ts], label="y(T)")
ax.plot(ts, s1, label="p_sync, m=1")
ax.plot(ts, s2, "--", label="p_sync, m=2")
ax.axhline(PC, color="k", ls=":", label="p_c")
ax.set(xlabel="T/w_D", ylabel="概率", title="(a) 两分支的同步比例")
ax.legend(fontsize=8)

ax = axes[1]
ax.plot(ts, t1, label="t, m=1")
ax.plot(ts, t2, "--", label="t, m=2")
ax.axhline(1.0509, color="r", ls=":", lw=1)
ax.axhline(1.1072, color="g", ls=":", lw=1)
ax.set(xlabel="T/w_D", ylabel="t", title="(b) 粗粒化指数（同点严格单调）")
ax.legend(fontsize=8)

ax = axes[2]
vals = [out["T_sync_m2"], out["T_sync_m1"], out["T_star"]]
ax.plot([0, 1, 2], vals, "o-")
ax.set_xticks([0, 1, 2])
ax.set_xticklabels(["T_sync(m=2)", "T_sync(m=1)", "T_*"])
ax.set_ylim(min(vals) - 0.02, max(vals) + 0.02)
ax.set(title="(c) 星级读法把同步温度压得更低")
for xi, v in zip([0, 1, 2], vals):
    ax.annotate(f"{v:.4f}", (xi, v), textcoords="offset points", xytext=(0, 6), ha="center", fontsize=8)

fig.tight_layout()
fig.savefig("环15锁定概率复合_两分支核对.png", dpi=150)
with open("环15锁定概率复合_两分支核对.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
