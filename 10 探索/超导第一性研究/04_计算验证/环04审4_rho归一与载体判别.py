# -*- coding: utf-8 -*-
"""环 4/15：`rho` 链内归一与载体维数判别（第 157 轮，R-166）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环04审4_rho归一与载体判别.py"（本目录）
输出：环04审4_rho归一与载体判别.png / .json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import j0, ndtri
from scipy.stats import norm
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PC = 0.592746
K_BIAS = 7.7                 # 第 156 轮工作点斜率 Delta g/g ~= 7.7 delta
ROUNDING = abs((2.0 / np.pi) / 1.023 - 0.622281) / 0.622281

Z = ndtri(1.0 - PC)
PHI2 = norm.pdf(Z) ** 2


def rho_nn(m, qa=np.pi):
    """(8G.3) 在最近邻 r=a、Q=pi/a： (m+1)∫_0^1 u^m J_0(qa*u) du"""
    I = quad(lambda u: u ** m * j0(qa * u), 0.0, 1.0, limit=200)[0]
    return (m + 1.0) * I


def delta_of(m):
    r = rho_nn(m)
    cbar = r * PHI2
    return r, cbar, cbar / (2.0 * PC)


checks = {}

# ---- C1 归一化 rho_m(0)=1 ----
norm_err = []
for m in (1, 2, 3, 4):
    I = quad(lambda u: u ** m, 0.0, 1.0)[0]
    norm_err.append(abs((m + 1) * I - 1.0))
checks["C1_normalization_maxerr"] = max(norm_err)
assert max(norm_err) < 1e-12

# ---- C2 最近邻 rho 数值与变号 ----
rows = {m: delta_of(m) for m in (1, 2, 3, 4)}
checks["C2_rho_table"] = {str(m): rows[m][0] for m in rows}
assert rows[1][0] > rows[2][0] > 0 > rows[3][0] > rows[4][0]
assert abs(rows[2][0] - 0.048930) < 1e-5
assert abs(rows[3][0] + 0.031094) < 1e-5

# ---- C3 cbar 与 delta ----
checks["C3_delta_table"] = {str(m): rows[m][2] for m in rows}
assert abs(rows[1][2] - 0.023023) < 1e-5
assert abs(rows[3][2] + 0.003951) < 1e-5

# ---- C4 偏差幅度超过舍入残差 ----
detect = {}
for m in (1, 2, 3, 4):
    bias = K_BIAS * rows[m][2]
    detect[str(m)] = bool(abs(bias) > ROUNDING)
checks["C4_rounding"] = ROUNDING
checks["C4_detectable"] = detect
assert all(detect.values())

# ---- C5 符号对应 ----
signs_ok = all(np.sign(K_BIAS * rows[m][2]) == np.sign(rows[m][0]) for m in rows)
checks["C5_sign_correspondence"] = bool(signs_ok)
assert signs_ok

# ---- C6 零穿越 m* ----
mstar = brentq(lambda m: rho_nn(m), 2.0, 3.0, xtol=1e-12)
checks["C6_mstar"] = mstar
assert 2.0 < mstar < 3.0

# ---- C7 截止敏感性：m=2 在不同 Qa 下变号 ----
qa_vals = np.linspace(2.0, 5.0, 60)
rho_qa = np.array([rho_nn(2, float(qa)) for qa in qa_vals])
checks["C7_qa_zero_cross"] = bool(np.any(np.diff(np.sign(rho_qa)) != 0))
checks["C7_rho_qa_pi"] = rho_nn(2, np.pi)
assert np.any(np.diff(np.sign(rho_qa)) != 0)

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ms = np.linspace(1.0, 4.0, 100)
rhos = np.array([rho_nn(float(m)) for m in ms])
dels = np.array([K_BIAS * delta_of(float(m))[2] for m in ms])

ax = axes[0, 0]
ax.plot(ms, rhos, "o-")
ax.axhline(0, color="r", ls="--")
ax.set(xlabel="m", ylabel="rho_nn", title="(a) 最近邻关联随载体变号")

ax = axes[0, 1]
ax.plot(ms, [delta_of(float(m))[2] for m in ms], "o-")
ax.axhline(0, color="r", ls="--")
ax.set(xlabel="m", ylabel="delta", title="(b) 阈值位移")

ax = axes[0, 2]
ax.plot(ms, dels, "o-", label="bias")
ax.axhline(ROUNDING * 100, color="g", ls=":", label="舍入残差%")
ax.axhline(-ROUNDING * 100, color="g", ls=":")
ax.set(xlabel="m", ylabel="Delta g/g (%)", title="(c) 可测偏差")
ax.legend(fontsize=8)

ax = axes[1, 0]
u = np.linspace(0, 1, 400)
ax.plot(u, j0(np.pi * u))
ax.axvline(2.4048 / np.pi, color="r", ls="--")
ax.set(xlabel="u", ylabel="J_0(pi u)", title="(d) Bessel 核过零")

ax = axes[1, 1]
ax.plot(qa_vals, rho_qa, "o-")
ax.axhline(0, color="r", ls="--")
ax.set(xlabel="Q a", ylabel="rho_nn(m=2)", title="(e) 截止敏感性")

ax = axes[1, 2]
ax.bar([str(m) for m in (1, 2, 3, 4)],
       [abs(K_BIAS * rows[m][2]) * 100 for m in (1, 2, 3, 4)])
ax.set(ylabel="|bias| (%)", title="(f) 各分支幅度")

fig.tight_layout()
fig.savefig("环04审4_rho归一与载体判别.png", dpi=150)
with open("环04审4_rho归一与载体判别.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
