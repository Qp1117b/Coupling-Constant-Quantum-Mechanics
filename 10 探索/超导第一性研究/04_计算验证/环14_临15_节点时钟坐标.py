# -*- coding: utf-8 -*-
"""
环 14／临-15 节点时钟坐标的排除性论证数值核对。

1. 全局坐标 K(t) 单曲线 vs 节点坐标 {K_i(tau_i)} 多曲线；
2. 读数差 Delta K 随 c_ij：全局恒 0、节点坐标一般非零；
3. 信息保持度：节点坐标保留 N 条、全局压缩为 1 条；
4. 例外：c_ij -> 0 时两类坐标重合（临-16 不可达）。

由 (15.1)-(15.3) 直接计算，无拟合。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环14_临15_节点时钟坐标.png")
OUT_CSV = os.path.join(HERE, "环14_临15_节点时钟坐标.csv")

GAMMAS = np.array([14.1347, 21.0220, 25.0109, 30.4249])
RHOS = 0.5 + 1j * GAMMAS
OFFSETS = np.array([0.0, 0.004, 0.008, 0.012])  # 起点未齐 a_i


def K(tau, offset=0.0):
    return -np.sum(np.exp(1j * GAMMAS * (tau + offset)) / RHOS)


def main():
    rows = []
    taus = np.linspace(0, 0.5, 400)

    # A 两类坐标的读数曲线
    print("A 全局坐标 vs 节点坐标")
    global_curve = np.array([K(t) for t in taus])
    node_curves = np.array([[K(t, a) for a in OFFSETS] for t in taus])
    print(f"  全局坐标: 1 条曲线; 节点坐标: {len(OFFSETS)} 条曲线")
    print(f"  t=0.25 时节点读数实部: {np.real(node_curves[200]).round(4).tolist()}")
    for t in taus[::100]:
        rows.append(("curves", t, global_curve[int(t / 0.5 * 399)].real,
                     node_curves[int(t / 0.5 * 399), 3].real, np.nan))

    # B 读数差随 c_ij
    print("\nB 读数差 Delta K 随偏移 c")
    cs = np.linspace(0, 0.02, 200)
    d_global = np.zeros_like(cs)
    d_node = np.array([abs(K(0.3, c) - K(0.3, 0)) for c in cs])
    print(f"  c=0.02: 全局差={d_global[-1]:.6f}, 节点差={d_node[-1]:.6f}")
    for c, dn in zip(cs[::40], d_node[::40]):
        rows.append(("reading_diff", c, dn, 0.0, np.nan))

    # C 信息保持度
    print("\nC 信息保持度")
    N = len(OFFSETS)
    print(f"  节点坐标保留 {N} 条独立读数; 全局坐标压缩为 1 条")
    rows.append(("info", N, N, 1, np.nan))

    # D 例外 c -> 0
    print("\nD 例外 c->0 两坐标重合")
    small = np.logspace(-6, 0, 200)
    d_small = np.array([abs(K(0.3, c) - K(0.3, 0)) for c in small])
    print(f"  c=1e-6: 节点差={d_small[0]:.3e}（->0，但 c=0 不可达）")
    for c, d in zip(small[::40], d_small[::40]):
        rows.append(("exception", c, d, 0.0, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(taus, global_curve.real, lw=2.6, color="tab:red",
                  label="全局坐标（1 条）")
    for i, a in enumerate(OFFSETS[1:], start=1):
        ax[0, 0].plot(taus, node_curves[:, i].real, lw=1.4, alpha=0.8,
                      label=rf"节点 $i={i}$, $a_i={a}$")
    ax[0, 0].set_xlabel(r"$t$ 或 $\tau_i$")
    ax[0, 0].set_ylabel(r"$\mathrm{Re}\,K$")
    ax[0, 0].set_title("A  全局坐标压成一条；节点坐标保留多条")
    ax[0, 0].legend(fontsize=7)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(cs, d_global, lw=2.2, color="tab:red", label="全局：恒 0")
    ax[0, 1].plot(cs, d_node, lw=2.2, color="tab:blue", label="节点：一般非零")
    ax[0, 1].set_xlabel(r"偏移 $c_{ij}$")
    ax[0, 1].set_ylabel(r"$|K_i-K_j|$")
    ax[0, 1].set_title("B  读数差排除全局坐标")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].bar(["全局坐标", "节点坐标"], [1, N],
                 color=["tab:red", "tab:blue"], alpha=0.85)
    for i, v in enumerate([1, N]):
        ax[1, 0].text(i, v + 0.1, str(v), ha="center", fontsize=10)
    ax[1, 0].set_ylabel("独立读数曲线数")
    ax[1, 0].set_title("C  信息压缩 vs 保持")
    ax[1, 0].grid(alpha=0.3, axis="y")

    ax[1, 1].loglog(small, d_small, lw=2.2, color="tab:green")
    ax[1, 1].set_xlabel(r"偏移 $c_{ij}$")
    ax[1, 1].set_ylabel(r"$|K_i-K_j|$")
    ax[1, 1].set_title(r"D  $c_{ij}\to0$ 时重合（$c_{ij}=0$ 不可达）")
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
