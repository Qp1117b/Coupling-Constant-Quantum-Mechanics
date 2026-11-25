# -*- coding: utf-8 -*-
"""
第 154 轮（R-163）：审-4 诱导键簇恒等与阈值归属。

核对四件事（全部为断言，不拟合 CQM 参数）：
  A. 同一样本上，“座簇划分”与“诱导键簇划分”逐点相同（两种独立实现）。
  B. 方格座/诱导键的跨越曲线重合；独立键渗流的阈值在 1/2，
     而座/诱导键在 0.592746 附近——两者不可互换。
  C. 座阈值处诱导键占比 q_c = p_c^2 = 0.351348 < 1/2；
     把 q=1/2 当诱导键阈值会要求 p=0.707107（已被 B 排除）。
  D. 正关联高斯场（rho_NN≈0.5）的座阈值低于独立对照，方向与 Slepian/
     R-99 一致；R-99 的“平均键密度匹配”给 p_*≈0.522，比 MC 阈值低约 5%，
     故 R-99 是 O(cbar) 近似，不是精确阈值。

外部标准：L31（方格座阈值 0.59274605079210(2)）、Kesten（方格键阈值 1/2）、
arXiv:1305.6941（正关联降低座阈值、升高键阈值）、arXiv:0908.0104（空间关联
对阈值影响小、对分形维数影响大）。

无参数拟合；图与 CSV 只记录核对量。
"""

import csv
import json
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环15_诱导键簇恒等与阈值归属.png")
OUT_CSV = os.path.join(HERE, "环15_诱导键簇恒等与阈值归属.csv")
OUT_JSON = os.path.join(HERE, "环15_诱导键簇恒等与阈值归属_摘要.json")

P_SITE = 0.59274605079210
P_BOND = 0.5
Q_C = P_SITE ** 2
P_NAIVE = math.sqrt(P_BOND)


class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.sz = [1] * n

    def find(self, a):
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        return True

    def union_flags(self, a, b, left, right):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return ra
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        left[ra] = left[ra] or left[rb]
        right[ra] = right[ra] or right[rb]
        return ra


def site_partition(occ):
    """BFS 直接按座相邻关系划分占据格点（实现一）。"""
    L = occ.shape[0]
    seen = -np.ones((L, L), dtype=int)
    comps = []
    for i in range(L):
        for j in range(L):
            if not occ[i, j] or seen[i, j] >= 0:
                continue
            cid = len(comps)
            stack = [(i, j)]
            seen[i, j] = cid
            members = []
            while stack:
                x, y = stack.pop()
                members.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < L and 0 <= ny < L and occ[nx, ny] and seen[nx, ny] < 0:
                        seen[nx, ny] = cid
                        stack.append((nx, ny))
            comps.append(frozenset(members))
    return frozenset(comps)


def induced_bond_partition(occ):
    """先枚举诱导边，再用并查集划分（实现二）。"""
    L = occ.shape[0]
    dsu = DSU(L * L)
    edges = []
    for i in range(L):
        for j in range(L):
            if not occ[i, j]:
                continue
            s = i * L + j
            if i + 1 < L and occ[i + 1, j]:
                edges.append((s, (i + 1) * L + j))
            if j + 1 < L and occ[i, j + 1]:
                edges.append((s, i * L + j + 1))
    for a, b in edges:
        dsu.union(a, b)
    groups = {}
    for i in range(L):
        for j in range(L):
            if occ[i, j]:
                s = i * L + j
                groups.setdefault(dsu.find(s), set()).add((i, j))
    return frozenset(frozenset(g) for g in groups.values())


def spans_site(occ):
    """开边界左右跨越（座模型）。"""
    L = occ.shape[0]
    dsu = DSU(L * L)
    left = [(k % L == 0) for k in range(L * L)]
    right = [(k % L == L - 1) for k in range(L * L)]
    for i in range(L):
        for j in range(L):
            if not occ[i, j]:
                continue
            s = i * L + j
            if i + 1 < L and occ[i + 1, j]:
                dsu.union_flags(s, (i + 1) * L + j, left, right)
            if j + 1 < L and occ[i, j + 1]:
                dsu.union_flags(s, i * L + j + 1, left, right)
    return any(dsu.find(k) == k and left[k] and right[k] and occ[k // L, k % L] for k in range(L * L))


def spans_induced(occ):
    """同一占据集，用诱导边构造（实现二）判定跨越。"""
    L = occ.shape[0]
    dsu = DSU(L * L)
    left = [(k % L == 0) for k in range(L * L)]
    right = [(k % L == L - 1) for k in range(L * L)]
    for i in range(L):
        for j in range(L):
            if not occ[i, j]:
                continue
            s = i * L + j
            for ni, nj in ((i + 1, j), (i, j + 1)):
                if ni < L and nj < L and occ[ni, nj]:
                    dsu.union_flags(s, ni * L + nj, left, right)
    return any(dsu.find(k) == k and left[k] and right[k] and occ[k // L, k % L] for k in range(L * L))


def spans_bond(L, bonds_h, bonds_v):
    """独立键渗流：每条边独立占据，判左右跨越。"""
    dsu = DSU(L * L)
    left = [(k % L == 0) for k in range(L * L)]
    right = [(k % L == L - 1) for k in range(L * L)]
    for (i, j), on in np.ndenumerate(bonds_h):
        if on and j + 1 < L:
            dsu.union_flags(i * L + j, i * L + j + 1, left, right)
    for (i, j), on in np.ndenumerate(bonds_v):
        if on and i + 1 < L:
            dsu.union_flags(i * L + j, (i + 1) * L + j, left, right)
    for k in range(L * L):
        if dsu.find(k) == k and left[k] and right[k]:
            return True
    return False


def crossing_point(xs, ys):
    ys = np.asarray(ys, float)
    for i in range(len(xs)):
        if ys[i] >= 0.5:
            if i == 0:
                return float(xs[0])
            return float(xs[i - 1] + (0.5 - ys[i - 1]) * (xs[i] - xs[i - 1]) / (ys[i] - ys[i - 1]))
    return float("nan")


def mc_crossing(L, mode, grid, reps, seed):
    rng = np.random.default_rng(seed)
    curves = []
    for _ in range(reps):
        if mode == "site":
            u = rng.random((L, L))
            curves.append([spans_site(u < p) for p in grid])
        elif mode == "bond":
            curves.append([])
            for q in grid:
                bh = rng.random((L, L)) < q
                bv = rng.random((L, L)) < q
                curves[-1].append(spans_bond(L, bh, bv))
        else:
            raise ValueError(mode)
    return np.array(curves, float).mean(axis=0)


def field_corr(L, xi, rng):
    r = np.arange(L)
    dx = np.minimum(r, L - r)
    X, Y = np.meshgrid(dx, dx, indexing="ij")
    C = np.exp(-(X ** 2 + Y ** 2) / (2 * xi ** 2))
    Chat = np.maximum(np.real(np.fft.fft2(C)), 0.0)
    w = rng.standard_normal((L, L))
    f = np.real(np.fft.ifft2(np.fft.fft2(w) * np.sqrt(Chat)))
    return (f - f.mean()) / f.std()


def mc_corr(L, xi, grid, reps, seed):
    rng = np.random.default_rng(seed)
    curves = []
    rhos = []
    for _ in range(reps):
        f = field_corr(L, xi, rng)
        rhos.append(float(np.mean(f * np.roll(f, 1, axis=1))))
        curves.append([spans_site(f > norm.ppf(1 - p)) for p in grid])
    return np.array(curves, float).mean(axis=0), float(np.mean(rhos))


def solve_r99(rho, pc0):
    def gap(p):
        z = norm.ppf(1 - p)
        return p * p + rho * norm.pdf(z) ** 2 - pc0 ** 2
    return float(brentq(gap, 0.2, 0.59))


def main():
    summary = {}
    rows = []

    # ---------------- A: 同一样本簇划分恒等 ----------------
    L = 24
    rng = np.random.default_rng(20261125)
    mismatch = 0
    trials = 300
    for _ in range(trials):
        occ = rng.random((L, L)) < 0.55
        if site_partition(occ) != induced_bond_partition(occ):
            mismatch += 1
    summary["cluster_partition_mismatch"] = mismatch
    summary["cluster_partition_trials"] = trials
    assert mismatch == 0, "座簇与诱导键簇划分必须逐样本相同"

    # ---------------- B: 跨越曲线，座/诱导/独立键 ----------------
    Lb = 40
    grid_site = np.linspace(0.50, 0.68, 37)
    grid_bond = np.linspace(0.42, 0.58, 33)
    site_curve = mc_crossing(Lb, "site", grid_site, reps=220, seed=11)
    bond_curve = mc_crossing(Lb, "bond", grid_bond, reps=220, seed=12)
    pc_site_mc = crossing_point(grid_site, site_curve)
    pc_bond_mc = crossing_point(grid_bond, bond_curve)
    summary["pc_site_mc_L40"] = pc_site_mc
    summary["pc_bond_mc_L40"] = pc_bond_mc
    assert abs(pc_site_mc - P_SITE) < 0.02, "座/诱导键阈值应落在 0.593 附近"
    assert abs(pc_bond_mc - P_BOND) < 0.02, "独立键阈值应落在 1/2 附近"
    assert abs(pc_site_mc - P_NAIVE) > 0.05, "座阈值不应在 sqrt(1/2)=0.707"

    # 同一样本、同一占据集上，座跨越与诱导键跨越逐样本一致
    span_mismatch = 0
    for _ in range(400):
        occ = rng.random((Lb, Lb)) < 0.56
        if spans_site(occ) != spans_induced(occ):
            span_mismatch += 1
    summary["span_mismatch"] = span_mismatch
    assert span_mismatch == 0

    # 诱导键占比
    summary["q_c_induced"] = Q_C
    summary["q_gap_to_half"] = P_BOND - Q_C
    summary["p_naive_sqrt_half"] = P_NAIVE
    summary["threshold_shift_naive_rel"] = (P_NAIVE - P_SITE) / P_SITE
    assert Q_C < P_BOND - 0.14

    # ---------------- C: 正关联高斯场的阈值 ----------------
    Lc = 48
    grid_c = np.linspace(0.46, 0.68, 45)
    xi_corr = 1.0 / math.sqrt(2.0 * math.log(2.0))  # rho_NN = 1/2
    corr_curve, rho_nn = mc_corr(Lc, xi_corr, grid_c, reps=140, seed=21)
    ctrl_curve, rho_ctrl = mc_corr(Lc, 0.02, grid_c, reps=140, seed=22)
    pc_corr = crossing_point(grid_c, corr_curve)
    pc_ctrl = crossing_point(grid_c, ctrl_curve)
    bias = pc_ctrl - P_SITE  # 开边界有限尺寸偏移
    pc_corr_adj = pc_corr - bias
    p_r99 = solve_r99(rho_nn, P_SITE)
    summary.update({
        "rho_nn_corr": rho_nn,
        "rho_nn_control": rho_ctrl,
        "pc_corr_raw": pc_corr,
        "pc_control_raw": pc_ctrl,
        "open_boundary_bias": bias,
        "pc_corr_bias_adjusted": pc_corr_adj,
        "p_r99": p_r99,
        "r99_relative_error_vs_mc": (p_r99 - pc_corr_adj) / pc_corr_adj,
        "pc_corr_minus_pc": pc_corr_adj - P_SITE,
    })
    assert rho_nn > 0.4 and abs(rho_ctrl) < 0.05
    assert pc_corr < pc_ctrl - 0.02, "正关联必须降低座阈值"
    assert 0.50 < pc_corr_adj < 0.59
    assert p_r99 < pc_corr_adj, "R-99 平均密度匹配应低于真实相关阈值"
    assert -0.10 < (p_r99 - pc_corr_adj) / pc_corr_adj < -0.01

    # ---------------- 输出 ----------------
    for p, s in zip(grid_site, site_curve):
        rows.append(("site_induced", p, s, ""))
    for q, s in zip(grid_bond, bond_curve):
        rows.append(("bond", q, s, ""))
    for p, s in zip(grid_c, corr_curve):
        rows.append(("corr", p, s, rho_nn))
    for p, s in zip(grid_c, ctrl_curve):
        rows.append(("control", p, s, rho_ctrl))
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["panel", "x", "spanning_prob", "extra"])
        wr.writerows(rows)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # ---------------- 图 ----------------
    fig, ax = plt.subplots(2, 2, figsize=(12.8, 10.2))

    ax[0, 0].plot(grid_site, site_curve, lw=2.0, color="tab:blue",
                  label="座 / 诱导键（同一样本）")
    ax[0, 0].plot(grid_bond, bond_curve, lw=2.0, color="tab:orange", label="独立键")
    ax[0, 0].axvline(P_SITE, color="tab:blue", ls="--", lw=1.0)
    ax[0, 0].axvline(P_BOND, color="tab:orange", ls="--", lw=1.0)
    ax[0, 0].axhline(0.5, color="k", ls=":", lw=0.8)
    ax[0, 0].set_xlabel("占据率")
    ax[0, 0].set_ylabel("跨越概率")
    ax[0, 0].set_title(f"B  阈值归属：座/诱导 {pc_site_mc:.3f}，独立键 {pc_bond_mc:.3f}")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    pgrid = np.linspace(0, 1, 401)
    ax[0, 1].plot(pgrid, pgrid ** 2, lw=2.0, color="tab:green", label=r"$q=p^2$")
    ax[0, 1].axhline(P_BOND, color="tab:red", ls="--", lw=1.4, label=r"键阈值 $1/2$")
    ax[0, 1].axhline(Q_C, color="tab:green", ls=":", lw=1.6, label=r"$q_c=p_c^2$")
    ax[0, 1].axvline(P_SITE, color="k", ls="-.", lw=1.0, label=r"$p_c$")
    ax[0, 1].axvline(P_NAIVE, color="gray", ls="--", lw=1.0, label=r"$\sqrt{1/2}$")
    ax[0, 1].scatter([P_SITE], [Q_C], color="tab:green", zorder=5)
    ax[0, 1].set_xlabel(r"$p_{\rm pair}$")
    ax[0, 1].set_ylabel("诱导键占比")
    ax[0, 1].set_title("C  座阈值处的键占比 0.3513，不是 1/2")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(grid_c, corr_curve, lw=2.0, color="tab:red",
                  label=fr"正关联 $\rho_{{NN}}\approx{rho_nn:.2f}$")
    ax[1, 0].plot(grid_c, ctrl_curve, lw=2.0, color="tab:blue",
                  label=fr"近独立对照 $\rho_{{NN}}\approx{rho_ctrl:.2f}$")
    ax[1, 0].axvline(P_SITE, color="k", ls="--", lw=1.0, label=r"$p_c({\rm indep})$")
    ax[1, 0].axvline(pc_corr, color="tab:red", ls=":", lw=1.2)
    ax[1, 0].axhline(0.5, color="k", ls=":", lw=0.8)
    ax[1, 0].set_xlabel("占据率 $p$")
    ax[1, 0].set_ylabel("跨越概率")
    ax[1, 0].set_title("D  正关联降低座阈值（方向判定）")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    names = [r"$p_c$ 独立", "MC 相关\n(偏置校正)", "R-99 平均\n密度匹配"]
    vals = [P_SITE, pc_corr_adj, p_r99]
    cols = ["tab:blue", "tab:red", "tab:purple"]
    ax[1, 1].bar(names, vals, color=cols, alpha=0.85)
    for k, v in enumerate(vals):
        ax[1, 1].text(k, v + 0.004, f"{v:.4f}", ha="center", fontsize=9)
    ax[1, 1].set_ylim(0.45, 0.63)
    ax[1, 1].set_ylabel("阈值")
    ax[1, 1].set_title("E  R-99 是 O(cbar) 近似，低估约 5%")
    ax[1, 1].grid(alpha=0.3, axis="y")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=160)
    plt.close(fig)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("ALL ASSERTIONS PASSED")


if __name__ == "__main__":
    main()
