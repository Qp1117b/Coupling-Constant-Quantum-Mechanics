"""环 15 / 审-6 第八段（第 179 轮）：ρ 的载体核分支审计。

问题：ρ_nn(m)=(m+1)∫_0^1 u^m J0(πu) du 用的是 **2D Bessel 核**（J0）；
而 06 的 ε 载体是 **3D Regge 体**（README 第 865 行）。若载体是 3D，
核应为球 Bessel j0(πu)=sin(πu)/(πu)。两者给出的 ρ_1 差一个量级，
故本轮把四支都算出来，看结论是否依赖分支。

谱指数：σ² ∝ ∫ q^{d-1}|G_q|²/ω_q dq ∝ Q^{2n+(d-1)-s+1}
⇒ m_eff = 2n + (d-1) - s（链内用 1/ω 形式，见 (161.5) 的 [1+2n_B]）。
d=2 ⇒ m_eff=2（第 85 轮写法 2n+1-s 是 d=2 特例）；d=3 ⇒ m_eff=3。
"""
import json
import os
import runpy

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad
from scipy.special import j0
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = runpy.run_path(os.path.join(HERE, "环15锁定概率复合_两分支核对.py"))
PC = BASE["PC"]
y_of, p_pair, EC = BASE["y_of"], BASE["p_pair"], BASE["EC"]


def kernel(r_type):
    if r_type == "2D":
        return lambda z: float(j0(z))
    def s(z):
        z = float(z)
        return 1.0 if abs(z) < 1e-12 else np.sin(z) / z
    return s


def rho(kind, m, r_over_a):
    k = kernel(kind)
    return (m + 1.0) * quad(lambda u: u ** m * k(np.pi * u * r_over_a), 0.0, 1.0)[0]


def rho_xy(r1, r2):
    return (2.0 * r1 - 1.0 - r2) / (2.0 * (1.0 - r1))


def box(a, r):
    s = np.sqrt(1.0 - r ** 2)
    f = lambda x: norm.pdf(x) * (norm.cdf((a - r * x) / s) - norm.cdf((-a - r * x) / s))
    return quad(f, -a, a, limit=200)[0]


def c_lock(a, r):
    return box(a, r) / (2.0 * norm.cdf(a) - 1.0) ** 2


def a_of(t):
    y = y_of(t)
    return np.inf if y <= 0 or y >= 1 else float(norm.isf(y / 2.0))


BRANCHES = [("2D", 2), ("2D", 3), ("3D", 2), ("3D", 3)]
WP = a_of(BASE["TC"])
Ts = np.linspace(0.30, 0.72, 120)

rows = []
for kind, m in BRANCHES:
    r1, r2 = rho(kind, m, 1.0), rho(kind, m, 2.0)
    r = rho_xy(r1, r2)
    cmax = max(c_lock(a_of(t), r) for t in Ts)
    # m=2 支的 T_sync（乘入 C_lock）
    f = lambda t: p_pair(t) * c_lock(a_of(t), r) * (1.0 - y_of(t)) ** 2 - PC
    tsync = float(brentq(f, 0.30, 0.75, xtol=1e-12))
    rows.append({"kernel": kind, "m_eff": m, "rho1": r1, "rho2": r2, "rho_XY": r,
                 "C_lock_wp": c_lock(WP, r), "C_lock_max": cmax,
                 "T_sync_m2": tsync})

base = [r for r in rows if r["kernel"] == "2D" and r["m_eff"] == 2][0]

data = {
    "round": 179,
    "a_workpoint": WP,
    "m_eff_rule": "m_eff = 2n + (d-1) - s（1/ω 形式）；d=2 ⇒ 2，d=3 ⇒ 3",
    "branches": rows,
    "rho1_range": [min(r["rho1"] for r in rows), max(r["rho1"] for r in rows)],
    "rhoXY_range": [min(r["rho_XY"] for r in rows), max(r["rho_XY"] for r in rows)],
    "C_lock_wp_range": [min(r["C_lock_wp"] for r in rows), max(r["C_lock_wp"] for r in rows)],
    "T_sync_range": [min(r["T_sync_m2"] for r in rows), max(r["T_sync_m2"] for r in rows)],
    "verdict": ("ρ_nn 的 J0 核属 2D；06 的 ε 载体是 3D Regge ⇒ 核与载体维数不匹配。"
                "四支的 ρ_1 跨 [-0.031, 0.304]、ρ_XY 跨 [-0.478, -0.227]，"
                "但工作点 C_lock-1 ≤ 2.5e-6、T_sync(m=2) 变化 ≤ 0.3% ⇒ 结论对分支不敏感；"
                "ρ_1 的定值仍不成立，须先钉载体层与核。"),
}

fig, ax = plt.subplots(1, 2, figsize=(11, 4.0))
labels = ["%s m=%d" % (r["kernel"], r["m_eff"]) for r in rows]
ax[0].bar(range(len(rows)), [r["rho_XY"] for r in rows], color="#1f77b4")
ax[0].axhline(-0.5, color="k", ls=":", lw=1.2, label="rho_v=0 理想化 -1/2")
ax[0].set_xticks(range(len(rows))); ax[0].set_xticklabels(labels, fontsize=8)
ax[0].set(ylabel="rho_XY", title="(a) 四支的相位差相关")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.25, axis="y")

ax[1].bar(range(len(rows)), [r["T_sync_m2"] for r in rows], color="#d62728")
ax[1].axhline(base["T_sync_m2"], color="k", ls=":", lw=1.0)
ax[1].set_xticks(range(len(rows))); ax[1].set_xticklabels(labels, fontsize=8)
ax[1].set(ylabel="T_sync(m=2)", title="(b) 修正后的 T_sync：分支间 <0.3%")
ts = [r["T_sync_m2"] for r in rows]
ax[1].set_ylim(min(ts) - 0.004, max(ts) + 0.004)
ax[1].grid(alpha=0.25, axis="y")

fig.suptitle("环 15：ρ 的载体核分支（2D J0 vs 3D j0）×（m_eff=2,3）", fontsize=11)
fig.tight_layout()
out_png = os.path.join(HERE, "环15锁定概率_载体核分支.png")
fig.savefig(out_png, dpi=150)
plt.close(fig)

with open(os.path.join(HERE, "环15锁定概率_载体核分支.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))
print("图片:", out_png)

