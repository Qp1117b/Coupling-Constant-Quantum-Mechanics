"""环 15 / 审-6 第七段（第 178 轮）：把相位聚集修正接进 m=2 锁定概率。

前件（全部链内，无新参数）：
  第 161 轮 (161.2)：失锁 ⇔ |θ| ≥ π（主值支边界）⇒ θ_c = π，y = erfc(π/(√2 σ_θ))
  第 177 轮 v7：ρ_XY = (2ρ₁-1-ρ₂)/[2(1-ρ₁)]，ρ₁=0.048930、ρ₂=-0.093848 ⇒ ρ=-0.424938
  由此 a = θ_c/σ_θ 不是外生量：y = P(|X|>a) ⇒ a = Φ⁻¹(1-y/2)，随 T 由 y(T)=2πe^{-E_c/T} 决定。

输出：C_lock(T)、m=2 修正前后 p_lock 与 T_sync（m=2）。
"""
import json
import os
import runpy

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
from scipy.integrate import quad
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = runpy.run_path(os.path.join(HERE, "环15锁定概率复合_两分支核对.py"))

PC = BASE["PC"]
y_of = BASE["y_of"]
p_pair = BASE["p_pair"]
EC = BASE["EC"]

RHO = -0.424938                                 # v7：ρ_1=0.048930、ρ_2=-0.093848


def a_of(t):
    """θ_c=π ⇒ a=π/σ_θ；又 y=erfc(a/√2)=P(|X|>a) ⇒ a=Φ⁻¹(1-y/2)。"""
    y = y_of(t)
    if y <= 0.0 or y >= 1.0:
        return np.inf
    return float(norm.isf(y / 2.0))


def box(a, r=RHO):
    s = np.sqrt(1.0 - r ** 2)
    f = lambda x: norm.pdf(x) * (norm.cdf((a - r * x) / s) - norm.cdf((-a - r * x) / s))
    return quad(f, -a, a, limit=200)[0]


def c_lock(a, r=RHO):
    pin = 2.0 * norm.cdf(a) - 1.0
    return box(a, r) / pin ** 2


def p_lock2_plain(t):
    return (1.0 - y_of(t)) ** 2


def p_lock2_corr(t):
    a = a_of(t)
    if not np.isfinite(a):
        return p_lock2_plain(t)
    return c_lock(a) * p_lock2_plain(t)


def p_sync2(t, corr):
    return p_pair(t) * (p_lock2_corr(t) if corr else p_lock2_plain(t))


def solve(corr):
    f = lambda t: p_sync2(t, corr) - PC
    lo, hi = 0.30, 0.75
    return float(brentq(f, lo, hi, xtol=1e-12))


T_plain = solve(False)
T_corr = solve(True)

Ts = np.linspace(0.30, 0.72, 300)
A_T = np.array([a_of(t) for t in Ts])
C_T = np.array([c_lock(a) for a in A_T])
Y_T = np.array([y_of(t) for t in Ts])

data = {
    "round": 178,
    "rho_v7": RHO,
    "theta_c": "pi (第 161 轮 (161.2)：失锁 ⇔ |θ|≥π)",
    "a_at_Tc": a_of(BASE["TC"]),
    "y_at_Tc": y_of(BASE["TC"]),
    "C_lock_at_Tc": c_lock(a_of(BASE["TC"])),
    "C_lock_max_over_range": [float(C_T.min()), float(C_T.max())],
    "a_range": [float(A_T.min()), float(A_T.max())],
    "T_sync_m2_plain": T_plain,
    "T_sync_m2_corr": T_corr,
    "dT_sync": T_corr - T_plain,
    "p_lock2_ratio_at_Tsync_corr": p_lock2_corr(T_corr) / p_lock2_plain(T_corr),
    "verdict": ("θ_c=π 使 a=Φ^{-1}(1-y/2) 成为 y(T) 的函数，聚集修正是链内可算量。"
                "m=2 的 p_lock 被 (1-y)^2 低估，最大相对修正出现在高温端（y 大、a 小）；"
                "故 T_sync 略上移（+0.00149，+0.24%），m=1 不受影响。"),
}

fig, ax = plt.subplots(1, 3, figsize=(14, 4.0))
ax[0].plot(Ts, Y_T, "-", color="#1f77b4", label="y(T)")
ax[0].set(yscale="log", xlabel="T", ylabel="y", title="(a) 逸度随 T")
ax[0].grid(alpha=0.25); ax[0].legend(fontsize=8)

ax[1].plot(Ts, C_T - 1.0, "-", color="#d62728", label="C_lock(T)-1")
ax[1].axhline(0.0, color="k", ls=":", lw=1.0)
ax[1].set(xlabel="T", ylabel="C_lock minus 1", title="(b) 锁定聚集修正（v7, ρ=-0.4249）")
ax[1].grid(alpha=0.25); ax[1].legend(fontsize=8)

ax[2].plot(Ts, [p_sync2(t, False) for t in Ts], "--", color="#2ca02c", label="m=2 未修正")
ax[2].plot(Ts, [p_sync2(t, True) for t in Ts], "-", color="#9467bd", label="m=2 聚集修正")
ax[2].axhline(PC, color="k", ls=":", lw=1.2, label="p_c")
ax[2].axvline(T_plain, color="#2ca02c", ls=":", lw=1.0)
ax[2].axvline(T_corr, color="#9467bd", ls=":", lw=1.0)
ax[2].set(xlabel="T", ylabel="p_sync", title="(c) T_sync(m=2)：%.5f → %.5f" % (T_plain, T_corr))
ax[2].grid(alpha=0.25); ax[2].legend(fontsize=8)

fig.suptitle("环 15：θ_c=π → a(T)=Phi^-1(1-y/2)；共点相位聚集对 m=2 锁定概率的修正", fontsize=11)
fig.tight_layout()
out_png = os.path.join(HERE, "环15锁定概率_相位聚集修正.png")
fig.savefig(out_png, dpi=150)
plt.close(fig)

with open(os.path.join(HERE, "环15锁定概率_相位聚集修正.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))
print("图片:", out_png)

