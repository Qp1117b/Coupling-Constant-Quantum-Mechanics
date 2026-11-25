# -*- coding: utf-8 -*-
"""
N-7 非均匀多通道刚度组装：把“并联／串联／几何平均”判成不同极限。

只做解析形状与不等式核对；不拟合实验数据。

外部标准：
  Wiener bounds（调和≤有效≤算术）；Keller-Dykhne 2D 对偶
  σ(p)σ(1-p)=σ1σ2，p=1/2 给 √(σ1σ2)；Bruggeman EMA；
  渗流刚度指数 t_U≈1.3（环 19 已用）。
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环10_N7刚度组装.png")
OUT_CSV = os.path.join(HERE, "环10_N7刚度组装.csv")
OUT_SUM = os.path.join(HERE, "环10_N7刚度组装_摘要.csv")

PC = 0.5
T_U = 1.3


def series(g1, g2):
    return g1 * g2 / (g1 + g2)


def arith(p, a, b):
    return p * a + (1 - p) * b


def harm(p, a, b):
    return 1.0 / (p / a + (1 - p) / b)


def bruggeman_2d(p, a, b):
    """2D Bruggeman: p(a-u)/(a+u)+(1-p)(b-u)/(b+u)=0, 数值求根。"""
    if p <= 0.0:
        return b
    if p >= 1.0:
        return a
    lo, hi = min(a, b), max(a, b)
    if b == 0.0:
        # 解析解：u = (2p-1)a (p>1/2)，否则 0
        return max(0.0, (2.0 * p - 1.0) * a)
    for _ in range(200):
        u = 0.5 * (lo + hi)
        f = p * (a - u) / (a + u) + (1 - p) * (b - u) / (b + u)
        if f > 0:
            lo = u
        else:
            hi = u
    return 0.5 * (lo + hi)


def percolation_phi(p, pc=PC, expo=T_U):
    if p <= pc:
        return 0.0
    return ((p - pc) / (1.0 - pc)) ** expo


def main():
    rows = []
    g1, g2 = 1.0, 0.2
    gs = series(g1, g2)
    gp = g1 + g2
    gm = math.sqrt(g1 * g2)

    # A: 两键串联/并联/几何平均
    for name, val in [("series", gs), ("geo", gm), ("arith", (g1 + g2) / 2),
                      ("parallel", gp)]:
        rows.append(("A", name, val))

    # B: 超导相 + 绝缘相，sigma2 = 0
    p_grid = np.linspace(0.0, 1.0, 401)
    for p in p_grid:
        br = bruggeman_2d(p, 1.0, 0.0)
        ph = percolation_phi(p)
        rows.append(("B", p, br, ph, p))

    # C: Dykhne 等比例，两有限电导
    s2_grid = np.geomspace(1e-3, 1.0, 200)
    for s2 in s2_grid:
        rows.append(("C", s2, math.sqrt(1.0 * s2), harm(0.5, 1.0, s2),
                     arith(0.5, 1.0, s2)))

    # D: CQM 刚度读出 vs Bruggeman / Wiener 上界
    for p in np.linspace(0.50, 1.0, 301):
        rows.append(("D", p, percolation_phi(p), bruggeman_2d(p, 1.0, 0.0), p))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["panel", "x", "y1", "y2", "y3"])
        wr.writerows(rows)

    # near-threshold comparison
    delta_list = [1e-1, 1e-2, 1e-3, 1e-4]
    ratios = []
    for d in delta_list:
        br = 2.0 * d
        ph = d ** T_U
        ratios.append(br / ph)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["quantity", "value", "note"])
        wr.writerow(["series(g1,g2)", gs, "g1=1, g2=0.2"])
        wr.writerow(["geometric_mean", gm, "Dykhne at p=1/2"])
        wr.writerow(["arithmetic", (g1 + g2) / 2, "parallel upper"])
        wr.writerow(["parallel", gp, "exact only for common endpoints"])
        for d, r in zip(delta_list, ratios):
            wr.writerow([f"Bruggeman/percolation at delta={d:g}", r, "diverges near threshold"])

    # ---------------------------------------------------------------- figure
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))

    ax[0, 0].bar([0, 1, 2, 3], [gs, gm, (g1 + g2) / 2, gp],
                 color=["tab:blue", "tab:green", "tab:orange", "tab:red"])
    ax[0, 0].set_xticks([0, 1, 2, 3])
    ax[0, 0].set_xticklabels(["串联\n(下界)", "几何平均\n(Dykhne)", "算术平均\n(上界)", "并联\n(共端点)"])
    ax[0, 0].set_ylabel(r"$\Upsilon_{\rm eff}$")
    ax[0, 0].set_title("A  四种读数是不同极限，不是竞争公式")
    ax[0, 0].grid(alpha=0.3, axis="y")

    ax[0, 1].plot(p_grid, [bruggeman_2d(p, 1.0, 0.0) for p in p_grid],
                  lw=1.8, label="Bruggeman 线性解 $(2p-1)_+$")
    ax[0, 1].plot(p_grid, [percolation_phi(p) for p in p_grid],
                  lw=1.8, label=r"CQM $\Phi(p)\sim(p-p_c)^{t_\Upsilon}$")
    ax[0, 1].plot(p_grid, p_grid, ls=":", lw=1.2, label="Wiener 上界")
    ax[0, 1].set_xlabel("$p$")
    ax[0, 1].set_ylabel(r"$\Upsilon_{\rm eff}/\Upsilon_{\rm bond}$")
    ax[0, 1].set_title("B  近阈 Bruggeman 线性律高估 stiffness")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].loglog(s2_grid, [math.sqrt(s2) for s2 in s2_grid],
                    lw=1.8, label=r"Dykhne $\sqrt{\sigma_1\sigma_2}$")
    ax[1, 0].loglog(s2_grid, [harm(0.5, 1.0, s2) for s2 in s2_grid],
                    lw=1.4, ls="--", label="Wiener 下界（调和）")
    ax[1, 0].loglog(s2_grid, [arith(0.5, 1.0, s2) for s2 in s2_grid],
                    lw=1.4, ls="--", label="Wiener 上界（算术）")
    ax[1, 0].set_xlabel(r"$\sigma_2$ ($\sigma_1=1$, $p=1/2$)")
    ax[1, 0].set_ylabel(r"$\sigma_{\rm eff}$")
    ax[1, 0].set_title("C  2D 对偶的精确点夹在 Wiener 界内")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, which="both")

    ax[1, 1].loglog([d for d in delta_list], ratios, "o-", lw=1.8)
    ax[1, 1].set_xlabel(r"$\delta=p-p_c$")
    ax[1, 1].set_ylabel("Bruggeman / 渗流幂律")
    ax[1, 1].set_title("D  比值随阈值发散，线性律不能作近阈标度")
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print(f"series={gs:.6f}, geo={gm:.6f}, arith={(g1+g2)/2:.6f}, parallel={gp:.6f}")
    print(f"sandwich: {gs:.6f} <= {gm:.6f} <= {(g1+g2)/2:.6f} <= {gp:.6f}")
    print("Bruggeman/percolation ratios: " +
          ", ".join(f"{d:g}:{r:.4f}" for d, r in zip(delta_list, ratios)))
    print(f"Dykhne sqrt at sigma2=1e-3: {math.sqrt(1e-3):.6f}")


if __name__ == "__main__":
    main()
