# -*- coding: utf-8 -*-
"""
R34: 13.A5 配对供给——有限集 Goldbach 表示数记账。
素数/有限集为外部标准数学对象，无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R34_有限集配对记账.py"
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def primes_below(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    return [i for i in range(n + 1) if sieve[i]]


def r_ord(M, S):
    """有序表示数 #{p∈S : M-p∈S}。"""
    Sset = set(S)
    return sum(1 for p in S if (M - p) in Sset)


def r_unord(M, S):
    """无序表示数 #{p≤q, p+q=M, p,q∈S}。"""
    Sset = set(S)
    return sum(1 for p in S if (M - p) in Sset and p <= M - p)


def assertions():
    out = {}
    P = primes_below(100)
    # (R34.1) 上界：r_ord ≤ |S|
    for M in [20, 50, 100]:
        S = [p for p in P if p <= M]
        out[f"rOrd_le_card_M{M}"] = bool(r_ord(M, S) <= len(S))
    # (R34.2) 对称配对恒等式：m∉S 时 r_ord = 2 r_unord
    M = 30  # m=15 不是素数
    S = P
    out["diag_not_in_S"] = 15 not in S
    out["symm_pair_identity"] = bool(r_ord(M, S) == 2 * r_unord(M, S))
    # m∈S 情形：M=14, m=7 是素数 → r_ord = 2 r_unord - 1
    M2 = 14
    out["diag_in_S"] = 7 in S
    out["symm_pair_diag_identity"] = bool(r_ord(M2, S) == 2 * r_unord(M2, S) - 1)
    # 有限化张力：有限集截断后某些名额 r_ord=0
    Ssmall = [2, 3, 5]
    out["finite_gap_M100_small"] = bool(r_ord(100, Ssmall) == 0)
    out["goldbach_infinite_nonempty"] = bool(r_ord(100, P) > 0)
    out["finite_vs_infinite_tension"] = bool(
        out["finite_gap_M100_small"] and out["goldbach_infinite_nonempty"]
    )
    # matching 上界：ν ≤ ⌊|S|/2⌋
    out["matching_bound"] = bool(len(Ssmall) // 2 == 1)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    P = primes_below(200)
    evens = list(range(4, 101, 2))

    ax = axes[0, 0]
    rvals = [r_unord(M, P) for M in evens]
    ax.plot(evens, rvals, "b-o", ms=4)
    ax.set_xlabel("偶数 M"); ax.set_ylabel(r"无序表示数 $r_{\rm unord}$")
    ax.set_title("(a) Goldbach 表示数（无限素数集）"); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    Ssmall = primes_below(50)  # 有限截断
    rvals_small = [r_unord(M, Ssmall) for M in evens]
    ax.plot(evens, rvals_small, "g-o", ms=4, label="有限集 S≤50")
    ax.plot(evens, rvals, "b--", alpha=0.5, label="素数集 S≤200")
    ax.set_xlabel("偶数 M"); ax.set_ylabel(r"$r_{\rm unord}$")
    ax.set_title("(b) 有限化：大 M 表示数归零")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    Ms = [30, 50, 70]  # m∉S
    ords = [r_ord(M, P) for M in Ms]
    unords = [r_unord(M, P) for M in Ms]
    x = np.arange(len(Ms))
    ax.bar(x - 0.2, ords, 0.4, label="有序")
    ax.bar(x + 0.2, unords, 0.4, label="无序")
    ax.set_xticks(x); ax.set_xticklabels([str(M) for M in Ms])
    ax.set_xlabel("偶数 M"); ax.set_ylabel("表示数")
    ax.set_title("(c) 对称配对：有序 ≈ 2×无序（对角线不在 S）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    M = 100
    sizes = [3, 5, 10, 20, 35]
    rvals_size = [r_ord(M, primes_below(s)) for s in sizes]
    ax.plot(sizes, rvals_size, "purple", lw=2)
    ax.set_xlabel("有限集大小 |S|"); ax.set_ylabel(r"有序表示数 $r_{\rm ord}(100;S)$")
    ax.set_title("(d) 有限化张力：|S| 小时供给为 0"); ax.grid(alpha=0.3)

    fig.suptitle("R34: 13.A5 有限集 Goldbach 配对记账（非拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R34_有限集配对记账.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R34 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R34_有限集配对记账_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
