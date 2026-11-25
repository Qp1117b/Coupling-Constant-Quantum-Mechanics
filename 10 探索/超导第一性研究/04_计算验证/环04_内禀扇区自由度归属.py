# -*- coding: utf-8 -*-
r"""
第 136 轮：环 4 内禀扇区的自由度归属判定——非仿射子空间与谱正交性
=====================================================================
问题：R96 把亏角载体定为 "ker H 的正交补（曲率激发模）"，R97 把它的谱
对接**余切拉普拉斯**（顶点图）的非零模。本脚本用纯计数与线性代数判定。

三个层次：

  (1) 计数：V, E, 顶点自由度 3V-6, 可嵌入方向 rank(B)=3V-6,
      非仿射（内禀）子空间 N_I = E - (3V-6)。
  (2) 正交性（决定性）：设 A[e,e']=d eps_e/d(delta_e')、Ã=A·diag(1/l)、
      B[e,3i+a]=d l_e/d x_{i,a}。R73 的位移盲性等价于 **Ã·B^T = 0**，
      即 A 的值域完全落在 N_I 上、在全部顶点位移扇区（含所有声子模）
      上恒为零。故任何顶点基算子（余切拉普拉斯、动力矩阵）的谱
      ——其本征矢都在 im(B^T) 内——都**不承载** eps。
  (3) 尺寸外推：N_I/(3V-6) 随样品增大，极限 E/V = z/2 = 7（BCC 配位数 14）。

外加 (4) 向错构型的线性响应（R73 斜率的物理身份＝Frank 角响应）。

只用链内量（(3.1) 亏角）与外部标准工具（Delaunay、四面体重建、线性代数）；不拟合。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_内禀扇区自由度归属.py"
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
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# ---------------------------------------------------------------- 几何
def dihedral(p, tet, edge):
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
    d = {PAIRS[i]: L[i] for i in range(6)}
    a, b = edge
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


def bcc_complex(n):
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
    faces = set()
    for t in tets:
        for e in itertools.combinations(t, 2):
            edges.add(tuple(sorted(e)))
        for f in itertools.combinations(t, 3):
            faces.add(tuple(sorted(f)))
    return P, tets, sorted(edges), sorted(faces)


def incidence(P, edges):
    """B: (E x 3V)，d l_e / d x_{i,a} = +-u_e（单位向量）。"""
    B = np.zeros((len(edges), 3 * len(P)))
    for ei, (i, j) in enumerate(edges):
        u = (P[j] - P[i]) / np.linalg.norm(P[j] - P[i])
        B[ei, 3 * i:3 * i + 3] = -u
        B[ei, 3 * j:3 * j + 3] = +u
    return B


def deficit_jacobian(P, tets, edges, h=1e-6):
    """A[e,e'] = d eps_e / d(delta_{e'})，delta 为边长相对偏差（中心差分）。
    eps_e 只依赖邻接 e 的四面体 ⇒ 只重建这些四面体（局部性，提速）。"""
    E = len(edges)
    A = np.zeros((E, E))
    lens = np.array([np.linalg.norm(P[a] - P[b]) for (a, b) in edges])
    # 预计算：每条边邻接的四面体；每个四面体的基准边长
    adj = [[] for _ in range(E)]
    eidx = {e: i for i, e in enumerate(edges)}
    for ei, e in enumerate(edges):
        adj[ei] = [t for t in tets if e[0] in t and e[1] in t]
    tet_base = []
    for t in tets:
        idx = list(t)
        L0 = [float(np.linalg.norm(P[idx[a]] - P[idx[b]])) for (a, b) in PAIRS]
        tet_base.append(L0)

    def eps_of_edge(ei, smap):
        e = edges[ei]
        tot = 0.0
        for t in adj[ei]:
            ti = tet_index[id(t)]
            idx = list(t)
            L = list(tet_base[ti])
            for k, (a, b) in enumerate(PAIRS):
                key = tuple(sorted((idx[a], idx[b])))
                if key in smap:
                    L[k] *= smap[key]
            ia, ib = idx.index(e[0]), idx.index(e[1])
            q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
            tot += dihedral(q, [0, 1, 2, 3], ee)
        return 2 * math.pi - tot

    tet_index = {id(t): i for i, t in enumerate(tets)}
    # 只有邻接 e2 的边会受 e2 长度变化影响
    e2_adj = [[] for _ in range(E)]
    for ei in range(E):
        s = set(edges[ei])
        e2_adj[ei] = [ej for ej in range(E)
                      if any(s <= set(t) and set(edges[ej]) <= set(t) for t in adj[ei])]
    for ej, e2 in enumerate(edges):
        smap_p = {e2: 1.0 + h}
        smap_m = {e2: 1.0 - h}
        for ei in e2_adj[ej]:
            A[ei, ej] = (eps_of_edge(ei, smap_p) - eps_of_edge(ei, smap_m)) / (2 * h)
    return A, lens


def main():
    # ----------------------------------------------------------------
    print("=" * 78)
    print("A. 自由度计数与尺寸外推")
    print("=" * 78)
    rows = []
    cache = {}
    for n in (2, 3, 4, 5):
        P, tets, edges, faces = bcc_complex(n)
        V, E, T, F = len(P), len(edges), len(tets), len(faces)
        B = incidence(P, edges)
        rankB = int(np.linalg.matrix_rank(B, tol=1e-9))
        NI = E - rankB
        rows.append(dict(n=n, V=V, E=E, F=F, T=T, rankB=rankB, NI=NI,
                         dof=3 * V - 6, ratio=NI / (3 * V - 6), EV=E / V,
                         euler=V - E + F - T))
        cache[n] = (P, tets, edges, B)
        print(f"  n={n}: V={V:4d} E={E:5d}  V-E+F-T={V-E+F-T}   "
              f"rank(B)={rankB:4d}=3V-6   N_I={NI:5d}   "
              f"N_I/(3V-6)={NI/(3*V-6):.4f}   E/V={E/V:.4f}")

    for r in rows:
        assert r["rankB"] == r["dof"], "rank(B) 必须等于 3V-6"
        assert r["euler"] == 1, "3D 球复形欧拉示性数应为 1"
        assert r["NI"] > 0

    # 线性外推 E/V = A - B/n
    ns = np.array([r["n"] for r in rows], float)
    ev = np.array([r["EV"] for r in rows])
    coef = np.polyfit(1.0 / ns, ev, 1)
    Bslope, Ainf = float(coef[0]), float(coef[1])
    print(f"\n  E/V = {Ainf:.4f} + ({Bslope:.4f})/n  ⇒ 极限 E/V = {Ainf:.3f}"
          f"（= z/2，z = {2*Ainf:.2f}，BCC Delaunay 配位数 14）")
    print(f"  ⇒ N_I/(3V-6) 的极限 = (E/V-3)/3 = {(Ainf-3)/3:.4f}")
    print(f"  ⇒ 热力学极限 N_I ≈ {(Ainf-3):.2f}V > 3V-6（判据在无限体成立）")
    extrap = dict(Ainf=Ainf, Bslope=Bslope, limit_ratio=(Ainf - 3) / 3)

    # ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print("B. 谱正交性（决定性）：Ã·B^T = 0  ⇒ 顶点位移扇区不承载 eps")
    print("=" * 78)
    orth = []
    for n in (2, 3):
        P, tets, edges, B = cache[n]
        E = len(edges)
        # 内部铰链：绕边四面体数 >= 3（凸包边只邻 1-2 个，属读数层，R82）
        n_adj = np.array([len([t for t in tets if set(e) <= set(t)]) for e in edges])
        mask = n_adj >= 4
        A, lens = deficit_jacobian(P, tets, edges)
        At = A / lens[None, :]                     # Ã = d eps / d l
        if n == 3:
            cache["A3"] = (A, lens, At, mask)
        ABx = At[mask] @ B                         # (E_int x 3V) = d eps_int / d x
        sc = np.abs(At[mask]).max() * np.abs(B).max()
        rel = np.abs(ABx).max() / sc
        BtB = B.T @ B
        PrE = B @ np.linalg.pinv(BtB, rcond=1e-10) @ B.T   # (E,E) 投到 im(B)
        PrN = np.eye(E) - PrE
        frac = np.linalg.norm(At[mask] @ PrN) / np.linalg.norm(At[mask])
        print(f"  n={n}: E={E}（内部 {int(mask.sum())}）  max|Ã|={np.abs(At[mask]).max():.4f}")
        print(f"        max|d eps_int/d x| = {np.abs(ABx).max():.3e}  相对={rel:.2e}")
        print(f"        ‖Ã_int·P_N‖/‖Ã_int‖ = {frac:.6f}  (→1 ⇒ 值域全在非仿射方向)")
        orth.append(dict(n=n, rel=rel, frac=frac, E=E, Eint=int(mask.sum()),
                         V=len(P), NI=E - int(np.linalg.matrix_rank(B, tol=1e-9))))
        assert rel < 1e-4, "内部铰链上 d eps/d x 必须为零"
        assert frac > 0.999, "Ã 必须完全作用在非仿射子空间上"

    # ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print("C. 向错构型：单键长非仿射偏差 → Frank 角线性响应")
    print("=" * 78)
    P, tets, edges, B = cache[4]
    inner = [e for e in edges
             if np.all(P[list(e)] >= 1 - 1e-9) and np.all(P[list(e)] <= 2 + 1e-9)]
    e0 = min(inner, key=lambda e: np.linalg.norm(P[e[0]] - P[e[1]]))
    print(f"  内部键 {len(inner)} 条，取最短键 |e|={np.linalg.norm(P[e0[0]]-P[e0[1]]):.6f}")

    def eps_of(e, delta):
        tot = 0.0
        for t in [t for t in tets if set(e) <= set(t)]:
            idx = list(t)
            L = []
            for (a, b) in PAIRS:
                v = float(np.linalg.norm(P[idx[a]] - P[idx[b]]))
                if set((idx[a], idx[b])) == set(e):
                    v *= (1.0 + delta)
                L.append(v)
            ia, ib = idx.index(e[0]), idx.index(e[1])
            q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
            tot += dihedral(q, [0, 1, 2, 3], ee)
        return 2 * math.pi - tot

    ds = np.array([-0.02, -0.01, -0.005, -0.0025, 0.0, 0.0025, 0.005, 0.01, 0.02])
    es = np.array([eps_of(e0, d) for d in ds])
    small = np.abs(ds) <= 0.0101
    slope = float(np.polyfit(ds[small], es[small], 1)[0])
    resid = float(np.max(np.abs(es[small] - slope * ds[small])))
    print(f"  斜率 d eps/d(delta) = {slope:.6f} rad，残差 {resid:.2e}"
          f"（|δ|≤1%）")
    print(f"  1% 键长非仿射偏差 ⇒ Frank 角 {abs(slope)*0.01:.5f} rad"
          f"（= {abs(slope)*0.01/(2*math.pi)*100:.3f}% 的 2π）")
    assert abs(es[4]) < 1e-12 and abs(slope) > 1e-3 and resid < 1e-3

    # ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print("D. 载体对比：同一 Ã，非仿射扰动 vs 顶点位移")
    print("=" * 78)
    n = 3
    P3, tets3, edges3, B3 = cache[n]
    E3 = len(edges3)
    A3, lens3, At3, mask3 = cache["A3"]
    PrE3 = B3 @ np.linalg.pinv(B3.T @ B3, rcond=1e-10) @ B3.T
    PrN3 = np.eye(E3) - PrE3
    rng = np.random.default_rng(11)
    rms_non, rms_ver = [], []
    for _ in range(12):
        v = PrN3 @ rng.standard_normal(E3)
        v /= np.linalg.norm(v)
        rms_non.append(float(np.sqrt(np.mean((A3[mask3] @ v) ** 2))))
        x = rng.standard_normal(3 * len(P3))
        d = (B3 @ x) / lens3          # 相对偏差 delta = d l / l
        rms_ver.append(float(np.sqrt(np.mean((A3[mask3] @ d) ** 2))))
    rms_non = np.array(rms_non); rms_ver = np.array(rms_ver)
    print(f"  n={n}，内部铰链 {int(mask3.sum())}，12 次随机扰动：")
    print(f"    非仿射扰动（投影到 $N_I$）: <eps^2>^(1/2) = {rms_non.mean():.4e} rad"
          f"  (min {rms_non.min():.2e})")
    print(f"    顶点位移（任意声子模）    : <eps^2>^(1/2) = {rms_ver.mean():.4e} rad"
          f"  (max {rms_ver.max():.2e})")
    ratio = rms_non.mean() / rms_ver.mean()
    print(f"    比值 = {ratio:.3e}  ⇒ 顶点扇区的 ε 响应是数值零")
    assert rms_ver.max() < 1e-6 and rms_non.min() > 1e-3

    # ----------------------------------------------------------------
    # 图
    # ----------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2))

    ax = axes[0, 0]
    nn = np.array([r["n"] for r in rows])
    ax.plot(nn, [r["EV"] for r in rows], "o-", label="$E/V$ 数值")
    xx = np.linspace(0, 0.55, 100)
    xf = np.linspace(1.5, 8, 120)
    ax.plot(xf, Ainf + Bslope / xf, "--",
            label=f"外推 $E/V\\to{Ainf:.2f}$（$z={2*Ainf:.1f}$）")
    ax.axhline(7.0, color="gray", ls=":", label="极限 $z/2=7$（配位数 14）")
    ax.set_xlabel("样品尺寸 $n$")
    ax.set_ylabel("$E/V$")
    ax.set_title("A. 边数密度外推到 BCC Delaunay 极限")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[0, 1]
    ax.plot(nn, [r["ratio"] for r in rows], "o-", label="$N_I/(3V-6)$")
    ax.axhline(1.0, color="r", ls="--", label="判据线 =1")
    ax.axhline(extrap["limit_ratio"], color="green", ls=":",
               label=f"极限 {(Ainf-3)/3:.2f}")
    ax.set_xlabel("样品尺寸 $n$")
    ax.set_ylabel("$N_I/(3V-6)$")
    ax.set_title("B. 非仿射维数 / 顶点谱上限（递增，外推穿线）")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[1, 0]
    ax.plot(ds, es, "o", label="数值（逐四面体重建）")
    ax.plot(ds, slope * ds, "-", label=f"线性斜率 {slope:.3f} rad")
    ax.set_xlabel(r"单键长相对偏差 $\delta$")
    ax.set_ylabel(r"Frank 角 $\varepsilon_e$ (rad)")
    ax.set_title("C. 非仿射键长偏差 → 亏角（=向错弗兰克角）")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[1, 1]
    lab = [r"非仿射 $\delta\ell\in N_I$", r"顶点位移 $\delta x$"]
    data = [rms_non, rms_ver]
    bp = ax.boxplot(data, tick_labels=lab, widths=.5, patch_artist=True)
    for patch, c in zip(bp["boxes"], ("#4C9F70", "#C0504D")):
        patch.set_facecolor(c); patch.set_alpha(.45)
    ax.set_yscale("log")
    ax.set_ylabel(r"$\langle(\Delta\varepsilon)^2\rangle^{1/2}$ (rad)")
    ax.set_title("D. 同一传递矩阵下的两种载体（n=3，12 次随机）")
    ax.grid(alpha=.3, which="both", axis="y")
    ax.annotate(f"数值零：max {rms_ver.max():.1e}", xy=(2, rms_ver.mean()),
                xytext=(1.55, rms_ver.max() * 30), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="#C0504D"))

    fig.tight_layout()
    png = os.path.join(OUT, "环04_内禀扇区自由度归属.png")
    fig.savefig(png, dpi=150)
    print(f"\n图：{png}")

    csvp = os.path.join(OUT, "环04_内禀扇区自由度归属.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "V", "E", "F", "T", "rankB", "NI", "3V-6",
                    "NI/(3V-6)", "E/V", "euler"])
        for r in rows:
            w.writerow([r["n"], r["V"], r["E"], r["F"], r["T"], r["rankB"],
                        r["NI"], r["dof"], f"{r['ratio']:.6f}",
                        f"{r['EV']:.6f}", r["euler"]])
    print(f"表：{csvp}")

    sump = os.path.join(OUT, "环04_内禀扇区自由度归属_摘要.csv")
    with open(sump, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["项目", "数值", "判据"])
        w.writerow(["E/V 极限", f"{Ainf:.4f}", "= z/2，z=14 为 BCC Delaunay 配位数"])
        w.writerow(["NI/(3V-6) 极限", f"{(Ainf-3)/3:.4f}", ">1 ⇒ 无限体判据成立"])
        for o in orth:
            w.writerow([f"max|d eps_int/d x| 相对（n={o['n']}）", f"{o['rel']:.3e}", "<1e-4"])
            w.writerow([f"‖Ã_int·P_N‖/‖Ã_int‖（n={o['n']}）", f"{o['frac']:.6f}", ">0.999"])
            w.writerow([f"内部铰链数（n={o['n']}）", o["Eint"], f"E={o['E']}, V={o['V']}, N_I={o['NI']}"])
        w.writerow(["单键长 → Frank 角斜率", f"{slope:.6f}", "rad per unit delta"])
        w.writerow(["非仿射扰动 ε 响应 (n=3)", f"{rms_non.mean():.3e}", "rad, 有物理量级"])
        w.writerow(["顶点位移 ε 响应 (n=3)", f"{rms_ver.mean():.3e}", "rad, 数值零"])
        w.writerow(["两者比值", f"{ratio:.3e}", ">1e6 ⇒ 载体判定"])
    print(f"摘要：{sump}")
    print("\n全部断言通过。")


if __name__ == "__main__":
    main()
