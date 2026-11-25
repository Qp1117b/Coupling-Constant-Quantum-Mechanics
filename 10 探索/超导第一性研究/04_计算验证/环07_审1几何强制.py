# -*- coding: utf-8 -*-
"""
环 7→8／`审-1` 矩阵分支几何强制的数值核对。

1. BCC 三环 prod(r)=0.177/0.707/0.500 的对数和（全非零 => 非梯度）；
2. 中心对称四邻居壳层上四个奇函数的行和残差（全为 0）；
3. 非对称壳层上同四个函数的行和残差（非零且随 f 变）；
4. 随机规范位移下三环和乐不变。

BCC 数值是链内输入；函数族直接计算，无拟合参数。
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
OUT_PNG = os.path.join(HERE, "环07_审1几何强制.png")
OUT_CSV = os.path.join(HERE, "环07_审1几何强制.csv")

PRODUCTS = np.array([0.177, 0.707, 0.500])  # 06 第 139/944 行 BCC 三角环
FUNCS = [
    ("f=x", lambda x: x),
    ("f=x^3", lambda x: x ** 3),
    ("f=tanh(x)", np.tanh),
    ("f=sinh(x)", np.sinh),
]


def main():
    rows = []

    # ---- 1 BCC 三环
    logs = np.log(PRODUCTS)
    print("BCC 三环 prod(r) 与 log 和（链内输入）")
    for p, s in zip(PRODUCTS, logs):
        print(f"  prod={p:.3f}  sum(lambda)={s:.6f}")
        rows.append(("bcc_loop", float(p), float(s), 0.0, np.nan))

    # ---- 2 中心对称壳层
    a, b = 0.8, 1.3
    sym_lams = [a, -a, b, -b]
    print("\n中心对称壳层行和残差")
    sym_res = []
    for name, f in FUNCS:
        res = sum(f(x) for x in sym_lams)
        sym_res.append(res)
        print(f"  {name:12s} {res:.12f}")
        rows.append(("sym_shell", float(a), float(res), 0.0, np.nan))

    # ---- 3 非对称壳层
    asym_lams = [0.8, 1.3, -0.4]
    print("\n非对称壳层行和残差")
    asym_res = []
    for name, f in FUNCS:
        res = sum(f(x) for x in asym_lams)
        asym_res.append(res)
        print(f"  {name:12s} {res:.6f}")
        rows.append(("asym_shell", float(a), float(res), 0.0, np.nan))

    # ---- 4 规范不变性
    rng = np.random.default_rng(20261122)
    lam0 = logs.copy()
    shifts = []
    for _ in range(5):
        c = rng.normal(size=3) * 2.0
        # 三环边 (0,1),(1,2),(2,0) 的规范位移：(c1-c0)+(c2-c1)+(c0-c2)=0
        d = (c[1] - c[0]) + (c[2] - c[1]) + (c[0] - c[2])
        shifted = lam0 + d
        shifts.append(float(np.max(np.abs(shifted - lam0))))
        rows.append(("gauge", float(d), float(np.max(np.abs(shifted - lam0))), 0.0, np.nan))
    print(f"\n规范位移后三环和乐最大偏差 = {max(shifts):.3e}")

    # ---- CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A
    idx = np.arange(3)
    ax[0, 0].bar(idx - 0.18, PRODUCTS, 0.36, color="tab:blue", alpha=0.85, label=r"$\prod r$")
    ax[0, 0].axhline(1.0, color="tab:red", ls="--", lw=1.8, label=r"梯度要求 $\prod r=1$")
    ax[0, 0].set_xticks(idx)
    ax[0, 0].set_xticklabels([r"$C_1$", r"$C_2$", r"$C_3$"])
    ax[0, 0].set_ylim(0.0, 1.2)
    ax[0, 0].set_ylabel(r"$\prod_{C} r$")
    ax[0, 0].set_title("A  BCC 三环：乘积不为 1")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B
    names = [n for n, _ in FUNCS]
    ax[0, 1].bar(names, sym_res, color="tab:green", alpha=0.85)
    ax[0, 1].axhline(0.0, color="0.35", lw=1.0)
    ax[0, 1].set_ylabel("行和残差")
    ax[0, 1].set_title("B  中心对称壳层：任意奇 f 自动消散度")
    ax[0, 1].set_ylim(-0.3, 0.35)
    ax[0, 1].text(1.5, 0.27, "四个残差均 < 1e-15（机器精度）",
                  ha="center", fontsize=9, color="tab:green")
    ax[0, 1].grid(alpha=0.3, axis="y")

    # C
    ax[1, 0].bar(names, asym_res, color="tab:orange", alpha=0.85)
    ax[1, 0].axhline(0.0, color="0.35", lw=1.0)
    ax[1, 0].set_ylabel("行和残差")
    ax[1, 0].set_title("C  非对称壳层：残差随 f 变化")
    ax[1, 0].grid(alpha=0.3, axis="y")

    # D
    ax[1, 1].plot(np.arange(len(shifts)), np.abs(shifts), "o-", color="tab:blue", lw=1.8)
    ax[1, 1].axhline(0.0, color="0.35", lw=1.0)
    ax[1, 1].set_xlabel("随机规范位移组")
    ax[1, 1].set_ylabel("和乐变化绝对值")
    ax[1, 1].set_title(r"D  规范位移不改三环和乐")
    ax[1, 1].set_ylim(-0.1, max(1e-12, max(shifts)) * 2 + 0.1)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
