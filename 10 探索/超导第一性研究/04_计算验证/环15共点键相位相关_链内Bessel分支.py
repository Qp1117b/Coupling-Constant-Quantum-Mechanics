"""环 15 / 审-6 第六段（第 177 轮）：把 ρ=-1/2 换成链内 Bessel 核的一般支。

前件：
  (9.1)  Var(λ_ij) = 2 κ_f^2 σ^2 (1-ρ_ij)  ⇒ 差场形态 ⇒ ρ_ij 是**顶点**相关
  第 84/157 轮  ρ_nn(m) = (m+1) ∫_0^1 u^m J_0(π u) du （Bessel 核，唯一几何归一）
  第 85 轮      06 的 3D Regge 体给 m_eff = 2n+1-s，n=1、s=1 ⇒ m_eff = 2

输出：ρ_XY(ρ_v) = (2ρ_v-1)/(2(1-ρ_v))，以及各支下的 C_lock(a)、C_unlock(a)。
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.special import j0
from scipy.stats import norm

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def rho_nn(m):
    """Bessel 核在最近邻归一 r=a（Qa=π）：ρ_nn(m) = (m+1)∫_0^1 u^m J0(πu) du。"""
    return (m + 1.0) * quad(lambda u: u ** m * j0(np.pi * u), 0.0, 1.0)[0]


def rho_xy(rv):
    return (2.0 * rv - 1.0) / (2.0 * (1.0 - rv))


def box(a, r):
    """P(|X|<a,|Y|<a)，ρ=r；对 X 一维积分（无二维 cdf 抵消）。"""
    s = np.sqrt(1.0 - r ** 2)
    f = lambda x: norm.pdf(x) * (norm.cdf((a - r * x) / s) - norm.cdf((-a - r * x) / s))
    return quad(f, -a, a, limit=200)[0]


def both_out(a, r):
    """P(|X|>a,|Y|>a)。"""
    s = np.sqrt(1.0 - r ** 2)
    f1 = lambda x: norm.pdf(x) * norm.cdf((-a - r * x) / s)
    f2 = lambda x: norm.pdf(x) * (1.0 - norm.cdf((a - r * x) / s))
    return 2.0 * quad(f1, a, np.inf, limit=200)[0] + 2.0 * quad(f2, a, np.inf, limit=200)[0]


Y_WP = 1.4298e-4
A_WP = float(norm.isf(Y_WP / 2.0))          # 由 y 反解的工作点 a

branches = []
for m in (1, 2, 3):
    rv = rho_nn(m)
    r = rho_xy(rv)
    pin = 2 * norm.cdf(A_WP) - 1
    branches.append({
        "m_eff": m,
        "rho_v": rv,
        "rho_XY": r,
        "C_lock_at_workpoint": box(A_WP, r) / pin ** 2,
        "C_lock_a1": box(1.0, r) / (2 * norm.cdf(1.0) - 1) ** 2,
        "C_unlock_a1": both_out(1.0, r) / (1 - (2 * norm.cdf(1.0) - 1)) ** 2,
    })
# ρ_v = 0 的理想化支（第 176 轮的 -1/2）
branches.append({
    "m_eff": 0,
    "rho_v": 0.0,
    "rho_XY": -0.5,
    "C_lock_at_workpoint": box(A_WP, -0.5) / (2 * norm.cdf(A_WP) - 1) ** 2,
    "C_lock_a1": box(1.0, -0.5) / (2 * norm.cdf(1.0) - 1) ** 2,
    "C_unlock_a1": both_out(1.0, -0.5) / (1 - (2 * norm.cdf(1.0) - 1)) ** 2,
})

rv_grid = np.linspace(-0.2, 0.45, 300)


# ---- v7（第 177 轮补）：不假设距离 2 相关为零 ----
def rho_mr(m, r_over_a):
    """距离 r（以最近邻 a 为单位）的顶点相关：ρ_m(r)=(m+1)∫_0^1 u^m J0(π u r/a) du。"""
    return (m + 1.0) * quad(lambda u: u ** m * j0(np.pi * u * r_over_a), 0.0, 1.0)[0]


def rho_xy_full(r1, r2):
    """Cov(X,Y)=v(2ρ₁-1-ρ₂)、Var=2v(1-ρ₁) ⇒ ρ_XY=(2ρ₁-1-ρ₂)/(2(1-ρ₁))。"""
    return (2.0 * r1 - 1.0 - r2) / (2.0 * (1.0 - r1))


m_eff = 2
R1 = rho_mr(m_eff, 1.0)
R2 = rho_mr(m_eff, 2.0)          # θ_i 与 θ_k（对顶点）之间的距离 2 相关
r_full = rho_xy_full(R1, R2)
v7 = {
    "m_eff": m_eff,
    "rho1": R1,
    "rho2_distance2": R2,
    "rho_XY_full": r_full,
    "rho_XY_with_rho2_zero": rho_xy_full(R1, 0.0),
    "C_lock_at_workpoint": box(A_WP, r_full) / (2 * norm.cdf(A_WP) - 1) ** 2,
}

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(rv_grid, rho_xy(rv_grid), "-", color="#1f77b4", lw=2, label="rho_XY(rho_v)")
ax[0].axhline(-0.5, color="k", ls=":", lw=1.2, label="rho_v=0 理想化 -1/2")
for b in branches[:3]:
    ax[0].plot([b["rho_v"]], [b["rho_XY"]], "o", ms=6,
               label="m_eff=%d: %.4f" % (b["m_eff"], b["rho_XY"]))
ax[0].set(xlabel=r"$\rho_v$", ylabel=r"$\rho_{XY}$",
          title="(a) v6 式（仅相邻相关，ρ₂=0 近似）")
ax[0].legend(fontsize=7); ax[0].grid(alpha=0.25)

ax[1].plot(rv_grid, [box(A_WP, rho_xy(r)) / (2 * norm.cdf(A_WP) - 1) ** 2 for r in rv_grid],
           "-", color="#d62728", lw=2, label="C_lock(a=3.80)")
ax[1].plot(rv_grid, [box(1.0, rho_xy(r)) / (2 * norm.cdf(1.0) - 1) ** 2 for r in rv_grid],
           "--", color="#2ca02c", lw=1.6, label="C_lock(a=1)")
ax[1].axhline(1.0, color="k", ls=":", lw=1.2, label="独立基线 1")
ax[1].set(yscale="log", xlabel=r"$\rho_v$", ylabel="C_lock",
          title="(b) 锁定聚集比：工作点几乎贴 1")
ax[1].legend(fontsize=7); ax[1].grid(alpha=0.25)

fig.suptitle("(9.1) 的 ρ 是顶点相关：v6 ρ_XY=(2ρ₁-1)/[2(1-ρ₁)]；v7 加 ρ₂ 项 ⇒ -0.424938", fontsize=11)
fig.tight_layout()
out_png = os.path.join(HERE, "环15共点键相位相关_链内Bessel分支.png")
fig.savefig(out_png, dpi=150)
plt.close(fig)

data = {
    "round": 177,
    "formula": "rho_XY = (2 rho_v - 1) / (2 (1 - rho_v))",
    "a_workpoint": A_WP,
    "rho_nn_1_to_5": [rho_nn(m) for m in (1, 2, 3, 4, 5)],
    "m_eff_committed": 2,
    "branches": branches,
    "v7_full": v7,
    "verdict": ("(9.1) 的 (1-rho) 是差场形态 ⇒ rho 是顶点相关；第 85 轮定 m_eff=2 ⇒ "
                "rho_v=rho_nn(2)=0.048930 ⇒ rho_XY=-0.474276（而非 -1/2）。"
                "三支给出的相位差相关落在 [-0.515, -0.389]，-1/2 只是 rho_v=0 的理想化边界；"
                "工作点 C_lock-1 仍在 1e-6 量级 ⇒ 独立假设在工作域的数值结论不变，但'顶点相位独立'本身被链内否定。"
                "补：v6 隐含 ρ₂=0，实际 ρ₂(距离2)=-0.093848 ⇒ 完整式 ρ_XY=-0.424938（v7）。"),
}
with open(os.path.join(HERE, "环15共点键相位相关_链内Bessel分支.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))
print("图片:", out_png)
