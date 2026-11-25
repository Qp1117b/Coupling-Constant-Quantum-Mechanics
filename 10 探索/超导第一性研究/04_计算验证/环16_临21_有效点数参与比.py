# -*- coding: utf-8 -*-
"""
环 16／临-21 有效点数的参与比数值核对。

1. 指数衰减权重 w_i ∝ exp(-beta*i) 的 n_eff 从 N 降到 1；
2. 等权饱和 n_eff = N 与二维 pi*(xi/a)^2 读数；
3. 细分不减：逐次均分权重，n_eff 单调升；
4. 三候选（空间/能窗/壳层）随选择参数扫描出现交叉——无一般序。

由 (21.1)(21.2) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环16_临21_有效点数参与比.png")
OUT_CSV = os.path.join(HERE, "环16_临21_有效点数参与比.csv")


def n_eff(w):
    """参与比 1/sum p_i^2。"""
    w = np.asarray(w, dtype=float)
    s = w.sum()
    if s <= 0:
        return 0.0
    p = w / s
    return 1.0 / np.sum(p ** 2)


def main():
    rows = []
    rng = np.random.default_rng(20261122)

    # A 集中度扫描：指数衰减权重
    N = 200
    idx = np.arange(N)
    print("A 集中度扫描（指数权重）")
    betas = np.linspace(0, 0.5, 200)
    ne_beta = [n_eff(np.exp(-b * idx)) for b in betas]
    for b, v in zip([0, 0.05, 0.2, 0.5], [n_eff(np.exp(-bb * idx)) for bb in [0, 0.05, 0.2, 0.5]]):
        print(f"  beta={b:.2f}: n_eff={v:.4f}")
        rows.append(("concentration", b, v, N, np.nan))

    # B 等权饱和与二维相干面积
    print("\nB 等权饱和")
    for n in (1, 10, 100, 1000):
        v = n_eff(np.ones(n))
        print(f"  N={n}: n_eff={v:.1f}（应 = N）")
        rows.append(("uniform", n, v, n, np.nan))
    xia = np.linspace(1, 300, 200)
    area = np.pi * xia ** 2  # 二维相干面积读数 pi*(xi/a)^2
    for x in (33, 100, 300):
        rows.append(("coherent_area", x, np.pi * x ** 2, np.nan, np.nan))

    # C 细分不减
    print("\nC 细分不减")
    w0 = np.exp(-0.05 * np.arange(64))
    cur = w0.copy()
    vals = [n_eff(cur)]
    for k in range(1, 5):
        cur = np.repeat(cur / 2, 2)  # 每个权重均分两份
        vals.append(n_eff(cur))
    for k, v in enumerate(vals):
        print(f"  细分 {k} 次: 点数={2**k * 64}, n_eff={v:.4f}")
        rows.append(("split", k, v, 2 ** k * 64, np.nan))

    # D 三候选交叉：同一组随机点，三种权重筛选
    print("\nD 三候选无一般序")
    pts_r = rng.uniform(0, 1, 500)
    pts_e = rng.normal(0, 0.2, 500)
    theta = rng.uniform(0, 2 * np.pi, 500)
    params = np.linspace(0.05, 0.95, 60)  # 选择参数（半径/能量窗/角宽的比例）
    n_space, n_energy, n_shell = [], [], []
    for q in params:
        ws = (pts_r < q).astype(float)                  # 空间圆截止
        we = (np.abs(pts_e) < 0.05 + 0.4 * q).astype(float)  # 能窗
        wk = np.exp(-((theta - np.pi) ** 2) / (2 * (0.2 + 2 * q) ** 2))  # 费米壳层角权重
        n_space.append(n_eff(ws))
        n_energy.append(n_eff(we))
        n_shell.append(n_eff(wk))
    for q, a, b, c in zip(params[::15], n_space[::15], n_energy[::15], n_shell[::15]):
        print(f"  q={q:.2f}: 空间={a:.1f}, 能窗={b:.1f}, 壳层={c:.1f}")
        rows.append(("candidates", q, a, b, c))
    # 是否存在交叉（相对次序改变）
    order = np.argsort(np.argsort(np.array([n_space, n_energy, n_shell]), axis=0), axis=0)
    crossings = int(np.sum(np.abs(np.diff(order, axis=1)) > 0))
    print(f"  三候选相对次序交叉次数: {crossings}（>0 即无一般序）")

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    ax[0, 0].plot(betas, ne_beta, lw=2.4, color="tab:blue")
    ax[0, 0].set_xlabel(r"集中度 $\beta$")
    ax[0, 0].set_ylabel(r"$n_{\rm eff}$")
    ax[0, 0].set_title(r"A  权重越集中，参与比越小（$N\to1$）")
    ax[0, 0].set_ylim(0, N * 1.05)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot([1, 10, 100, 1000], [1, 10, 100, 1000], "o-", lw=2.2,
                  color="tab:green", label=r"等权 $n_{\rm eff}=N$")
    ax[0, 1].plot(xia, area, lw=2.0, color="tab:orange",
                  label=r"$\pi(\xi/a)^2$（二维面积）")
    ax[0, 1].set_xscale("log")
    ax[0, 1].set_yscale("log")
    ax[0, 1].set_xlabel(r"$N$ 或 $\xi/a$")
    ax[0, 1].set_ylabel(r"$n_{\rm eff}$")
    ax[0, 1].set_title("B  等权饱和与相干面积读数")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3, which="both")

    ks = np.arange(len(vals))
    ax[1, 0].plot(ks, vals, "o-", lw=2.2, color="tab:purple")
    ax[1, 0].set_xlabel("均分次数 $k$")
    ax[1, 0].set_ylabel(r"$n_{\rm eff}$")
    ax[1, 0].set_title(r"C  细分不减（点数 $2^k\cdot64$）")
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(params, n_space, lw=2.0, label="空间圆截止")
    ax[1, 1].plot(params, n_energy, lw=2.0, label="能窗")
    ax[1, 1].plot(params, n_shell, lw=2.0, label="费米壳层")
    ax[1, 1].set_xlabel("选择参数 $q$")
    ax[1, 1].set_ylabel(r"$n_{\rm eff}$")
    ax[1, 1].set_title("D  三候选随参数交叉：无一般序")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
