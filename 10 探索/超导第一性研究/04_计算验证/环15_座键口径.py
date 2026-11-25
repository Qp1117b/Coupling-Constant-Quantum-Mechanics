# -*- coding: utf-8 -*-
"""
审-4：座比例 p_pair 与诱导键比例 q = p^2 的口径判定。

核对：
  1. 诱导键的共点正相关 p^3(1-p)；
  2. 正确阈值 p_c(site)=0.592746 vs 朴素 p^2>=1/2 给 p=0.707107；
  3. Monte Carlo 方格座渗流跨越概率（Newman-Ziff 增量并查集），
     看阈值落在哪一边。

只做统计形状与不等式核对，不拟合 CQM 参数。

外部标准：L31（Ziff，p_c(site)=0.59274602(4)）；方格键阈值 1/2（Kesten）。
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
OUT_PNG = os.path.join(HERE, "环15_座键口径.png")
OUT_CSV = os.path.join(HERE, "环15_座键口径.csv")
OUT_SUM = os.path.join(HERE, "环15_座键口径_摘要.csv")

P_SITE = 0.59274605079210
P_BOND = 0.5
P_NAIVE = math.sqrt(P_BOND)


def mc_spanning(L, reps=300, seed=20261122):
    """Newman-Ziff 增量算法：逐 realization 记录首次上下跨越的占据数。"""
    rng = np.random.default_rng(seed + L)
    N = L * L
    cross_counts = []
    for _ in range(reps):
        parent = list(range(N))
        size = [1] * N
        top = [False] * N
        bot = [False] * N
        span = False
        cross_at = None

        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a

        def union(a, b):
            nonlocal span
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]
            top[ra] = top[ra] or top[rb]
            bot[ra] = bot[ra] or bot[rb]
            if top[ra] and bot[ra]:
                span = True

        occ = np.zeros(N, dtype=bool)
        order = rng.permutation(N)
        for step, s in enumerate(order, start=1):
            s = int(s)
            i, j = divmod(s, L)
            occ[s] = True
            top[s] = (i == 0)
            bot[s] = (i == L - 1)
            for t in ([s + 1] if j + 1 < L else []) + ([s - 1] if j - 1 >= 0 else []) + \
                     ([s + L] if i + 1 < L else []) + ([s - L] if i - 1 >= 0 else []):
                if occ[t]:
                    union(s, t)
            if span and cross_at is None:
                cross_at = step
                break
        cross_counts.append(cross_at / N if cross_at else 1.0)
    return np.array(cross_counts)


def main():
    rows = []
    p_grid = np.linspace(0.0, 1.0, 401)

    # A: 共点诱导键协方差
    for p in p_grid:
        cov = p ** 3 * (1.0 - p)
        rows.append(("A", p, cov))

    # B: 诱导键比例与两个阈值
    for p in p_grid:
        rows.append(("B", p, p ** 2))

    # C: MC 跨越概率
    mc = {}
    for L in [16, 24, 32]:
        samples = mc_spanning(L, reps=240, seed=20261122 + L)
        mc[L] = samples
        for p in p_grid:
            frac = float(np.mean(samples <= p))
            rows.append(("C", L, p, frac))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["panel", "x", "y1", "y2"])
        wr.writerows(rows)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["quantity", "value", "note"])
        wr.writerow(["p_c_site", P_SITE, "external, square lattice"])
        wr.writerow(["p_c_bond", P_BOND, "exact, Kesten"])
        wr.writerow(["naive_sqrt_half", P_NAIVE, "p_pair^2 >= 1/2 would require this"])
        wr.writerow(["threshold_error", P_NAIVE - P_SITE, "absolute"])
        wr.writerow(["relative_error", (P_NAIVE - P_SITE) / P_SITE, "relative"])
        wr.writerow(["q_at_site_threshold", P_SITE ** 2, "induced bond fraction"])
        wr.writerow(["q_gap_to_bond_threshold", P_BOND - P_SITE ** 2, "positive"])
        for L, s in mc.items():
            wr.writerow([f"MC_mean_pc_L{L}", float(np.mean(s)), "first top-bottom spanning"])

    # ---------------------------------------------------------------- figure
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))

    ax[0, 0].plot(p_grid, p_grid ** 3 * (1 - p_grid), lw=2.0, color="tab:red")
    peak_p = 3.0 / 4.0
    ax[0, 0].axvline(peak_p, color="k", ls="--", lw=1.0, label=r"峰值 $p=3/4$")
    ax[0, 0].set_xlabel("$p$")
    ax[0, 0].set_ylabel(r"$\mathrm{Cov}(B_e,B_f)$")
    ax[0, 0].set_title("A  共点诱导键正相关 $p^3(1-p)$")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(p_grid, p_grid ** 2, lw=2.0, label=r"诱导键比例 $q=p^2$")
    ax[0, 1].axhline(P_BOND, color="tab:red", ls="--", lw=1.4,
                     label=r"键阈值 $1/2$（错用）")
    ax[0, 1].axhline(P_SITE ** 2, color="tab:green", ls=":", lw=1.6,
                     label=r"正确 $q_c=p_c({\rm site})^2$")
    ax[0, 1].axvline(P_SITE, color="k", ls="-.", lw=1.0, label=r"$p_c({\rm site})$")
    ax[0, 1].axvline(P_NAIVE, color="gray", ls="--", lw=1.0, label=r"$\sqrt{1/2}$（朴素）")
    ax[0, 1].set_xlabel("$p_{\\rm pair}$")
    ax[0, 1].set_ylabel("$q$")
    ax[0, 1].set_title("B  朴素映射把阈值抬高约 19%")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    for L, s in mc.items():
        ax[1, 0].plot(p_grid, [float(np.mean(s <= p)) for p in p_grid],
                      lw=1.6, label=f"L={L}")
    ax[1, 0].axvline(P_SITE, color="k", ls="--", lw=1.2,
                     label=r"$p_c({\rm site})=0.592746$")
    ax[1, 0].axvline(P_NAIVE, color="tab:red", ls=":", lw=1.4,
                     label=r"$\sqrt{1/2}=0.707107$")
    ax[1, 0].set_xlabel("$p$")
    ax[1, 0].set_ylabel("跨越概率")
    ax[1, 0].set_title("C  方格座渗流 Monte Carlo：阈值在 0.593 而非 0.707")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(p_grid, p_grid ** 2, lw=2.0, label=r"$q=p^2$")
    ax[1, 1].plot([0, 1], [P_BOND, P_BOND], "r--", lw=1.4)
    ax[1, 1].plot([0, 1], [P_SITE ** 2, P_SITE ** 2], "g:", lw=1.6)
    ax[1, 1].scatter([P_SITE], [P_SITE ** 2], s=80, color="green", zorder=5,
                     label=r"正确临界点 $(0.5927,\ 0.3513)$")
    ax[1, 1].scatter([P_NAIVE], [P_BOND], s=80, color="red", zorder=5,
                     label=r"朴素临界点 $(0.7071,\ 0.5)$")
    ax[1, 1].set_xlabel("$p_{\\rm pair}$")
    ax[1, 1].set_ylabel("$q$")
    ax[1, 1].set_title("D  两个判定点不在同一条物理曲线上")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print(f"p_c(site)={P_SITE:.9f}, sqrt(1/2)={P_NAIVE:.9f}")
    print(f"threshold error = {P_NAIVE - P_SITE:.6f} (relative {(P_NAIVE-P_SITE)/P_SITE:.4%})")
    print(f"q_c = {P_SITE**2:.6f}, gap to 1/2 = {P_BOND - P_SITE**2:.6f}")
    print("cov peak at p=3/4, value = " + str((3 / 4) ** 3 * (1 / 4)))
    for L, s in mc.items():
        print(f"MC L={L}: mean crossing p = {np.mean(s):.5f}, N={len(s)}")


if __name__ == "__main__":
    main()
