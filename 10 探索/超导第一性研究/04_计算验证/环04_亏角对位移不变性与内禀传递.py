# -*- coding: utf-8 -*-
"""
R73：环 4 的 epsilon 究竟由谁承载——亏角对位移场恒为零，对内禀度规线性响应
==========================================================================
第 73 轮。四组数值：

  A. 位移不变性：随机位移（三档振幅）与平面波（两个 q）下，所有内部铰链的
     eps_e = 2*pi - sum_T theta 是否仍为零？（定理：同组合复形嵌入 R^3 时恒为 2*pi）
  B. 非可嵌入扰动：把一条铰链的边长乘以 (1+delta)，用**逐四面体重建**（只由 6 条
     边长定形）算二面角，看 eps 是否线性出现。
  C. 仿射一致扰动：整体按同一应变改变所有边长（仍可嵌入）⇒ eps 应仍为零。
  D. 结论量化：eps 对 delta 的斜率（= 该铰链的传递系数），与"应变方向落在核里"对照。

只用链内量（(3.1) 的亏角定义）与外部标准工具（Delaunay、四面体重建）；不拟合。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_亏角对位移不变性与内禀传递.py"
"""
import csv
import itertools
import math
import os

import numpy as np
from scipy.spatial import Delaunay
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------
# 几何工具
# ----------------------------------------------------------------------
def dihedral(p, tet, edge):
    """内二面角：两法向取朝外后 theta = pi - phi。"""
    i, j = edge
    k, l = [x for x in tet if x not in edge]
    n1 = np.cross(p[j] - p[i], p[k] - p[i])
    n2 = np.cross(p[j] - p[i], p[l] - p[i])
    if np.dot(n1, p[l] - p[i]) > 0:
        n1 = -n1
    if np.dot(n2, p[k] - p[i]) > 0:
        n2 = -n2
    n1 /= np.linalg.norm(n1)
    n2 /= np.linalg.norm(n2)
    return math.pi - math.acos(float(np.clip(np.dot(n1, n2), -1.0, 1.0)))


def embed_tet(L, edge=(0, 1)):
    """由 6 条边长（PAIRS 顺序）重建四面体；按最长边重排以避免退化面。
    返回 (4 个顶点, 目标边在新编号下的下标对)。"""
    d = {PAIRS[i]: L[i] for i in range(6)}
    a, b = edge
    # 找最长边做新 (0,1)
    amax = max(d, key=lambda k: d[k])
    perm = [amax[0], amax[1]] + [v for v in range(4) if v not in amax]
    Lp = []
    for (u, v) in PAIRS:
        key = (perm[u], perm[v])
        Lp.append(d[key] if key in d else d[(key[1], key[0])])
    l01, l02, l03, l12, l13, l23 = Lp
    p0 = np.zeros(3)
    p1 = np.array([l01, 0.0, 0.0])
    x2 = (l02 ** 2 + l01 ** 2 - l12 ** 2) / (2 * l01)
    y2 = math.sqrt(max(l02 ** 2 - x2 ** 2, 1e-30))
    p2 = np.array([x2, y2, 0.0])
    x3 = (l03 ** 2 + l01 ** 2 - l13 ** 2) / (2 * l01)
    y3 = (l03 ** 2 - l23 ** 2 - 2 * x3 * x2 + x2 ** 2 + y2 ** 2) / (2 * y2)
    z3 = math.sqrt(max(l03 ** 2 - x3 ** 2 - y3 ** 2, 0.0))
    p3 = np.array([x3, y3, z3])
    ia, ib = perm.index(a), perm.index(b)
    return np.array([p0, p1, p2, p3]), (min(ia, ib), max(ia, ib))


PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


def bcc_complex(n=4):
    pts = []
    for i, j, k in itertools.product(range(n), repeat=3):
        pts.append([i, j, k])
        pts.append([i + .5, j + .5, k + .5])
    P = np.array(pts, float)

    def vol(s):
        a, b, c, d = [P[i] for i in s]
        return abs(np.linalg.det(np.array([b - a, c - a, d - a]))) / 6.0

    tets = [tuple(int(x) for x in s) for s in Delaunay(P).simplices if vol(s) > 1e-9]
    edges = set()
    for t in tets:
        for e in itertools.combinations(t, 2):
            if np.all(P[list(e)] >= 1 - 1e-9) and np.all(P[list(e)] <= 2 + 1e-9):
                edges.add(tuple(sorted(e)))
    return P, tets, sorted(edges)


def deficits_from_positions(X, tets, edges):
    out = []
    for e in edges:
        ts = [t for t in tets if set(e) <= set(t)]
        out.append(2 * math.pi - sum(dihedral(X, t, e) for t in ts))
    return np.array(out)


def hinge_eps_from_lengths(P, tets, e, scale):
    """只由边长定形：把铰链 e 的长度乘以 scale，逐四面体重建后求该铰链的 eps。"""
    ts = [t for t in tets if set(e) <= set(t)]
    tot = 0.0
    for t in ts:
        idx = list(t)
        L = []
        for (a, b) in PAIRS:
            v = float(np.linalg.norm(P[idx[a]] - P[idx[b]]))
            if set((idx[a], idx[b])) == set(e):
                v *= scale
            L.append(v)
        ia, ib = idx.index(e[0]), idx.index(e[1])
        q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
        tot += dihedral(q, [0, 1, 2, 3], ee)
    return 2 * math.pi - tot


def hinge_eps_from_lengths_one(P, tets, e, e2, scale):
    """把边 e2 的长度乘以 scale（其余不动），逐四面体重建后求铰链 e 的 eps。"""
    ts = [t for t in tets if set(e) <= set(t)]
    tot = 0.0
    for t in ts:
        idx = list(t)
        L = []
        for (a, b) in PAIRS:
            v = float(np.linalg.norm(P[idx[a]] - P[idx[b]]))
            if set((idx[a], idx[b])) == set(e2):
                v *= scale
            L.append(v)
        ia, ib = idx.index(e[0]), idx.index(e[1])
        q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
        tot += dihedral(q, [0, 1, 2, 3], ee)
    return 2 * math.pi - tot


def hinge_eps_scaled(P, tets, e, scales):
    """按字典 scales: edge -> 长度缩放，逐四面体重建后求铰链 e 的 eps。"""
    ts = [t for t in tets if set(e) <= set(t)]
    tot = 0.0
    for t in ts:
        idx = list(t)
        L = []
        for (a, b) in PAIRS:
            v = float(np.linalg.norm(P[idx[a]] - P[idx[b]]))
            ee = tuple(sorted((idx[a], idx[b])))
            if ee in scales:
                v *= scales[ee]
            L.append(v)
        ia, ib = idx.index(e[0]), idx.index(e[1])
        q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
        tot += dihedral(q, [0, 1, 2, 3], ee)
    return 2 * math.pi - tot


def main():
    P, tets, edges = bcc_complex(4)
    print("原子数 %d，非退化四面体 %d，内部铰链 %d" % (len(P), len(tets), len(edges)))

    eps0 = deficits_from_positions(P, tets, edges)
    print("\n=== A. 位移不变性 ===")
    print("平坦参考：max|eps| = %.3e" % np.abs(eps0).max())
    assert np.abs(eps0).max() < 1e-12

    rng = np.random.default_rng(7)
    rows = []
    for amp in (1e-4, 1e-3, 1e-2, 1e-1):
        X = P.copy()
        X[1:-1] += amp * rng.standard_normal(X[1:-1].shape)
        m = np.abs(deficits_from_positions(X, tets, edges)).max()
        rows.append(("随机位移 amp=%.0e" % amp, m))
        print("  随机位移 amp=%.0e -> max|eps| = %.3e" % (amp, m))
    for q in (0.3, 1.0, 2.0):
        X = P.copy()
        X[:, 0] += 0.01 * np.sin(q * P[:, 0])
        m = np.abs(deficits_from_positions(X, tets, edges)).max()
        rows.append(("平面波 q=%.1f" % q, m))
        print("  平面波 q=%.1f, amp=0.01 -> max|eps| = %.3e" % (q, m))

    # 均匀应变（仿射，仍可嵌入）
    F = np.array([[1.02, 0.01, 0.0], [0.0, 0.98, 0.005], [0.0, 0.0, 1.01]])
    X = P @ F.T
    m = np.abs(deficits_from_positions(X, tets, edges)).max()
    rows.append(("均匀应变", m))
    print("  均匀应变 F=1.02/0.98/1.01 -> max|eps| = %.3e" % m)

    assert max(r[1] for r in rows) < 1e-12

    print("\n=== B/C/D. 非可嵌入扰动 ===")
    # 选中心 NN 铰链
    i1 = int(np.argmin(np.linalg.norm(P - [1.5, 1.5, 1.5], axis=1)))
    i2 = int(np.argmin(np.linalg.norm(P - [1.0, 1.0, 1.0], axis=1)))
    e = (min(i1, i2), max(i1, i2))
    print("铰链 %s：|e| = %.6f，绕边四面体 %d 个"
          % (e, np.linalg.norm(P[e[0]] - P[e[1]]), len([t for t in tets if set(e) <= set(t)])))

    deltas, epss = [], []
    for d in (-4e-2, -2e-2, -1e-2, -5e-3, 0.0, 5e-3, 1e-2, 2e-2, 4e-2):
        eps = hinge_eps_from_lengths(P, tets, e, 1.0 + d)
        deltas.append(d)
        epss.append(eps)
        print("  边长 x(1%+.3f) -> eps = %+.6e" % (d, eps))
    deltas = np.array(deltas)
    epss = np.array(epss)
    assert abs(epss[np.argmin(np.abs(deltas))]) < 1e-12        # delta=0 给 0
    nz = np.abs(deltas) > 1e-9
    small = np.abs(deltas) <= 0.021
    slope = float(np.polyfit(deltas[small], epss[small], 1)[0])
    resid = float(np.max(np.abs(epss[small] - slope * deltas[small])))
    print("  线性斜率 d eps / d(delta) = %.6f（|delta|<=2%% 拟合），残差 %.2e" % (slope, resid))
    assert abs(slope) > 1e-3 and resid < 1e-3   # 线性 + O(delta^2)（二次系数约 1）

    # C：整体均匀缩放所有边长（仿射）⇒ 仍为零（用一条铰链的边缘四面体验证）
    print("\n=== C. 均匀缩放全部边长（仿射，可嵌入）===")
    for s in (1.01, 1.05):
        # 均匀缩放等价于把整个结构放大，逐四面体重建后二面角不变
        ts = [t for t in tets if set(e) <= set(t)]
        tot = 0.0
        for t in ts:
            idx = list(t)
            L = [float(np.linalg.norm(P[idx[a]] - P[idx[b]])) * s for (a, b) in PAIRS]
            ia, ib = idx.index(e[0]), idx.index(e[1])
            q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
            tot += dihedral(q, [0, 1, 2, 3], ee)
        print("  全部边长 x%.2f -> eps = %+.3e" % (s, 2 * math.pi - tot))
        assert abs(2 * math.pi - tot) < 1e-12

    # --------------------------------------------------------------
    # D. 传递矩阵 A 与应变核
    # --------------------------------------------------------------
    print("\n=== D. 传递矩阵与应变核 ===")
    allE = sorted({tuple(sorted((t[a], t[b])))
                   for t in tets for (a, b) in PAIRS})
    eidx = {e_: i for i, e_ in enumerate(allE)}
    # 只对内部铰链求行
    rowsA, eps_list = [], []
    Dl = 1e-4
    for e in edges:
        row = np.zeros(len(allE))
        for e2 in allE:
            # 只对影响该铰链的边求差分（其余为 0，省时且精确）
            if not any((set(e2) <= set(t)) for t in tets if set(e) <= set(t)):
                continue
            L0 = hinge_eps_from_lengths(P, tets, e, 1.0)
            Lp = hinge_eps_from_lengths_one(P, tets, e, e2, 1.0 + Dl)
            row[eidx[e2]] = (Lp - L0) / Dl
        rowsA.append(row)
    A = np.array(rowsA)
    print("  A 形状 %s，Frobenius 范数 %.4f，最大元 %.4f" % (A.shape, np.linalg.norm(A), np.abs(A).max()))

    # 应变方向：delta l / l = e_hat . eps . e_hat（精确边长变化，不走差分）
    S0 = 0.02          # 小应变，保证 I+eps 非奇异
    strains = {
        "exx": S0 * np.array([[1, 0, 0], [0, 0, 0], [0, 0, 0.]]),
        "eyy": S0 * np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0.]]),
        "ezz": S0 * np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1.]]),
        "exy": S0 * np.array([[0, .5, 0], [.5, 0, 0], [0, 0, 0.]]),
        "eyz": S0 * np.array([[0, 0, 0], [0, 0, .5], [0, .5, 0.]]),
        "ezx": S0 * np.array([[0, 0, .5], [0, 0, 0], [.5, 0, 0.]]),
    }
    eps_strain = {}
    for nm, eps in strains.items():
        X = P + P @ np.asarray(eps).T
        eps_strain[nm] = float(np.abs(deficits_from_positions(X, tets, edges)).max())
    print("  应变响应 max|eps|（位置，精确）：" +
          "  ".join("%s=%.2e" % (k, x) for k, x in eps_strain.items()))

    rng2 = np.random.default_rng(11)
    sc = {e2: 1.0 + 1e-4 * rng2.standard_normal() for e2 in allE}
    m_rand = max(abs(hinge_eps_scaled(P, tets, e2, sc)) for e2 in edges)
    print("  随机度规扰动（相对 1e-4）max|eps| = %.3e" % m_rand)
    assert np.all(np.isfinite(list(eps_strain.values())))
    assert max(eps_strain.values()) < 1e-12
    assert m_rand > 1e-8

    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.2))

    ax = axes[0]
    labels = [r[0] for r in rows]
    vals = [max(r[1], 1e-18) for r in rows]
    ax.barh(range(len(vals)), vals, color="#4a90d9")
    ax.set_yticks(range(len(vals)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xscale("log")
    ax.axvline(1e-12, color="k", ls="--", lw=1, label="零判据 $10^{-12}$")
    ax.set_xlabel(r"$\max_e|\varepsilon_e|$")
    ax.set_title("A：任何位移场都不产生亏角")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.3, axis="x")

    ax = axes[1]
    ax.plot(deltas * 100, epss, "o-", ms=4, label=r"逐四面体重建")
    ax.plot(deltas * 100, slope * deltas, "k--", lw=1, label=r"斜率 %.3f" % slope)
    ax.axhline(0, color="gray", lw=0.8)
    ax.axvline(0, color="gray", lw=0.8)
    ax.set_xlabel(r"铰链边长相对改变 $\delta$ (%)")
    ax.set_ylabel(r"$\varepsilon_e$（rad）")
    ax.set_title("B：非可嵌入度规扰动 → 亏角线性出现")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[2]
    ax.axis("off")
    ax.text(0.5, 0.86, r"$\delta\ell\;=\;\delta\ell^{\,\mathrm{strain}}\;\oplus\;\delta\ell^{\,\mathrm{intr}}$",
            ha="center", fontsize=17)
    ax.text(0.5, 0.62, "可嵌入部分（位移/应变）", ha="center", fontsize=11, color="#2c7fb8")
    ax.text(0.5, 0.50, r"$\Rightarrow\ \varepsilon\equiv0$（A 与 C 面板）", ha="center", fontsize=11)
    ax.text(0.5, 0.30, "内禀部分（非可嵌入度规，FG 接口）", ha="center", fontsize=11, color="#d95f0e")
    ax.text(0.5, 0.18, r"$\Rightarrow\ \varepsilon\ne0$，且 $\delta\varepsilon=A\,\delta\ell^{\,\mathrm{intr}}$（B 面板）",
            ha="center", fontsize=11)
    ax.set_title("亏角只承载内禀扇区")

    fig.tight_layout()
    png = os.path.join(OUT, "环04_亏角对位移不变性.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)

    csv_path = os.path.join(OUT, "环04_亏角对位移不变性.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["检验", "量", "值"])
        for lab, v in rows:
            w.writerow(["A 位移不变性", lab, "%.3e" % v])
        for d, s_ in zip(deltas, epss):
            w.writerow(["B 非可嵌入扰动", "delta=%.4f" % d, "%.6e" % s_])
        w.writerow(["B 斜率", "d eps/d delta", "%.6f" % slope])
    print("\n图：", os.path.basename(png))
    print("表：", os.path.basename(csv_path))


if __name__ == "__main__":
    main()
