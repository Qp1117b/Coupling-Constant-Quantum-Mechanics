# -*- coding: utf-8 -*-
"""环 15：和乐动力学映射与推 6 终结（第 161 轮，R-170）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环15和乐动力学映射与推6终结.py"（本目录）
输出：环15和乐动力学映射与推6终结.png / .json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from math import erf, erfc, pi, sqrt, exp
from scipy.integrate import quad
from scipy.special import j0, ndtri
from scipy.stats import norm

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PC = 0.592746
Z = ndtri(1.0 - PC)
PHI2 = norm.pdf(Z) ** 2
PC2 = PC ** 2
RHO_MAX = 0.18119175498741524   # 第 157 轮 m=1 最近邻最大值


def rho_nn(m):
    I = quad(lambda u: u ** m * j0(pi * u), 0.0, 1.0, limit=200)[0]
    return (m + 1.0) * I


def lock(sigma):
    x = pi / (sqrt(2.0) * sigma)
    return erf(x), erfc(x)


checks = {}

# ---- C1 方差传递 ----
alpha, kap, sig, rho = 2.0 * pi, 1.0 / (4.0 * pi), 0.03, 0.1
vlam = 2.0 * kap ** 2 * sig ** 2 * (1.0 - rho)
s2 = alpha ** 2 * vlam
checks["C1_v_lambda"] = vlam
checks["C1_sigma_theta_sq"] = s2
assert s2 > 0 and abs(s2 - 2.0 * alpha ** 2 * kap ** 2 * sig ** 2 * (1 - rho)) < 1e-15

# ---- C2 锁相因子 ----
sg = np.linspace(0.1, 1.5, 40)
pl = np.array([lock(float(s))[0] for s in sg])
yv = np.array([lock(float(s))[1] for s in sg])
checks["C2_lock_sum"] = float(np.max(np.abs(pl + yv - 1.0)))
checks["C2_y_monotone"] = bool(np.all(np.diff(yv) > 0))
assert checks["C2_lock_sum"] < 1e-14
assert np.all(np.diff(yv) > 0)

# ---- C3 erfc 渐近 ----
xs = np.array([4.0, 5.0, 6.0, 7.0])
rel = []
for x in xs:
    approx = exp(-x ** 2) / (sqrt(pi) * x)
    rel.append(abs(erfc(float(x)) / approx - 1.0))
checks["C3_erfc_asymptotic_relerr"] = rel
assert rel[-1] < 1e-2

# ---- C4 指数匹配 ----
T, U = 0.3, 0.65
Ec = pi ** 2 * U / 2.0
s2_match = pi ** 2 * T / (2.0 * Ec)
checks["C4_sigma_match"] = s2_match
checks["C4_T_over_U"] = T / U
assert abs(s2_match - T / U) < 1e-14

# ---- C5 K*sigma^2=1 ----
K = U / T
checks["C5_K_sigma_product"] = K * s2_match
assert abs(K * s2_match - 1.0) < 1e-14

# ---- C6 Upsilon_0 结构式 ----
w, sig0 = 1.0, 0.03
D = 4.0 * alpha ** 2 * kap ** 2 * sig0 ** 2 * (1.0 - rho)
U_struct = w / D
lhs = T / U_struct
rhs = D * T / w
checks["C6_Upsilon0_struct"] = U_struct
checks["C6_residual"] = abs(lhs - rhs)
assert abs(lhs - rhs) < 1e-13

# ---- C7 推 6 界 ----
qcs = []
for m in (1, 2, 3):
    r = rho_nn(m)
    qcs.append(PC2 + r * PHI2)
need_cbar = 0.5 - PC2
need_rho = need_cbar / PHI2
checks["C7_qc"] = qcs
checks["C7_all_below_half"] = bool(all(q < 0.5 for q in qcs))
checks["C7_required_rho"] = need_rho
checks["C7_rho_max"] = RHO_MAX
checks["C7_rejected"] = bool(need_rho > RHO_MAX)
assert all(q < 0.5 for q in qcs)
assert need_rho > RHO_MAX

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ax = axes[0, 0]
ax.plot(sg, pl, label="p_lock")
ax.plot(sg, yv, "--", label="y=1-p_lock")
ax.set(xlabel="sigma_theta", ylabel="概率", title="(a) 高斯尾锁相因子")
ax.legend(fontsize=8)

ax = axes[0, 1]
xx = np.linspace(3.0, 6.0, 60)
ax.plot(xx, [erfc(float(x)) for x in xx], label="erfc")
ax.plot(xx, [exp(-x ** 2) / (sqrt(pi) * x) for x in xx], "--", label="渐近")
ax.set(yscale="log", xlabel="x", ylabel="erfc", title="(b) 尾部渐近")
ax.legend(fontsize=8)

ax = axes[0, 2]
ax.plot([T], [s2_match], "o", label="指数匹配")
ax.plot([T], [T / U], "x", label="k_B T / Upsilon_0")
ax.set(xlabel="T", ylabel="sigma_theta^2", title="(c) 指数匹配一致性")
ax.legend(fontsize=8)

ax = axes[1, 0]
ax.bar(["sigma_theta^2", "k_B T / Upsilon_0"], [s2_match, T / U], color=["tab:blue", "tab:red"])
ax.set(title="(d) 两路径比较")

ax = axes[1, 1]
ax.bar(["m=1", "m=2", "m=3"], qcs, color=["tab:blue", "tab:green", "tab:orange"])
ax.axhline(0.5, color="r", ls="--", label="键阈值 1/2")
ax.set(ylabel="q_c", title="(e) 推 6 界")
ax.legend(fontsize=8)

ax = axes[1, 2]
ax.bar(["所需 rho", "Bessel 最大"], [need_rho, RHO_MAX], color=["tab:red", "tab:blue"])
ax.set(ylabel="rho_nn", title="(f) 达到 1/2 不可能")

fig.tight_layout()
fig.savefig("环15和乐动力学映射与推6终结.png", dpi=150)
with open("环15和乐动力学映射与推6终结.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
