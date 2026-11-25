# -*- coding: utf-8 -*-
"""
环 22／临-16 全对归零测度零的数值核对。

1. 离散全相等概率 M/M^N = 1/M^(N-1) 随 N 指数衰减（不同 M）；
2. 连续样本 a_i ~ N(0, sigma_a^2) 的 max|c_ij| 分布（恒正，全对归零频率 0）；
3. 核内平移 a_i -> a_i + c 不改变 c_ij（规范平凡，数值验证）；
4. 三态分类中态3（全齐）的测度零示意。

由 (16.1)-(16.4) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环22_临16_全对归零测度零.png")
OUT_CSV = os.path.join(HERE, "环22_临16_全对归零测度零.csv")


def main():
    rows = []
    rng = np.random.default_rng(20261122)

    # A 离散全相等概率
    print("A 离散全相等概率 M/M^N")
    Ns = np.arange(2, 21)
    for M in (2, 5, 10):
        probs = np.array([M / M ** N for N in Ns])
        print(f"  M={M}: N=2 时 {probs[0]:.3e}, N=20 时 {probs[-1]:.3e}")
        for N, p in zip(Ns[::4], probs[::4]):
            rows.append(("discrete", N, p, M, np.nan))

    # B 连续样本 max|c_ij| 分布
    print("\nB 连续样本 max|c_ij|（恒正）")
    N = 30
    n_samples = 2000
    sigma_a = 0.5
    maxcs = []
    allzero_count = 0
    for _ in range(n_samples):
        a = rng.normal(0, sigma_a, N)
        c = a[:, None] - a[None, :]
        mc = np.max(np.abs(c - np.diag(np.diag(c))))
        maxcs.append(mc)
        if mc < 1e-12:
            allzero_count += 1
    maxcs = np.array(maxcs)
    print(f"  样本数={n_samples}: max|c_ij| 最小值={maxcs.min():.4f}, "
          f"全对归零样本数={allzero_count}")
    rows.append(("continuous", sigma_a, maxcs.min(), allzero_count, np.nan))
    for i in range(6):
        rows.append(("sample", i, maxcs[i], np.nan, np.nan))

    # C 核内平移不改变 c_ij
    print("\nC 核内平移 a_i -> a_i + c 不改变 c_ij")
    a = rng.normal(0, sigma_a, 6)
    cshift = 3.7
    c_before = a[:, None] - a[None, :]
    a_shift = a + cshift
    c_after = a_shift[:, None] - a_shift[None, :]
    diff = np.max(np.abs(c_after - c_before))
    print(f"  平移 {cshift}: max|c_after - c_before|={diff:.3e}")
    rows.append(("gauge", cshift, diff, np.nan, np.nan))

    # D 三态分类示意（态3 测度零）
    print("\nD 三态分类（态3 全齐 = 测度零）")
    print("  态1 场未公有化 / 态2 冻结未齐（测度正）/ 态3 全齐（测度零）")
    rows.append(("states", 1, 0.0, 1.0, np.nan))  # 态1/态2 测度正
    rows.append(("states", 2, 1.0, 1.0, np.nan))
    rows.append(("states", 3, 0.0, 0.0, np.nan))  # 态3 测度零

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    for M, col in [(2, "tab:blue"), (5, "tab:orange"), (10, "tab:green")]:
        probs = [M / M ** N for N in Ns]
        ax[0, 0].semilogy(Ns, probs, "o-", ms=3, lw=1.8, color=col,
                          label=f"M={M}")
    ax[0, 0].set_xlabel(r"节点数 $N$")
    ax[0, 0].set_ylabel(r"全相等概率 $M/M^N$")
    ax[0, 0].set_title("A  离散全相等概率指数衰减")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3, which="both")

    ax[0, 1].hist(maxcs, bins=50, color="tab:purple", alpha=0.85)
    ax[0, 1].axvline(0, color="tab:red", ls="--", lw=1.4)
    ax[0, 1].set_xlabel(r"$\max_{i<j}|c_{ij}|$")
    ax[0, 1].set_ylabel("样本数")
    ax[0, 1].set_title(f"B  连续样本恒正（归零频率 {allzero_count}/{n_samples}）")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(a, "o-", color="tab:blue", label=r"$a_i$")
    ax[1, 0].plot(a_shift, "s--", color="tab:orange", alpha=0.8,
                  label=r"$a_i+c$")
    ax[1, 0].set_xlabel("节点")
    ax[1, 0].set_ylabel("固有时")
    ax[1, 0].set_title(f"C  核内平移 $c={cshift}$：$c_{{ij}}$ 不变")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].bar(["态1 未公有化", "态2 冻结未齐", "态3 全齐"], [1, 1, 0],
                 color=["tab:red", "tab:blue", "tab:green"], alpha=0.85)
    ax[1, 1].set_ylabel("测度（示意：正 / 零）")
    ax[1, 1].set_title("D  态3 全齐为测度零事件")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
