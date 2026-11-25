# -*- coding: utf-8 -*-
"""
R72：BCC Delaunay 复形上 cot 拉普拉斯的实数核实
================================================
第 72 轮。四件事：
  (1) 用 Delaunay 直接数出 BCC 两类铰链的绕边四面体数 k 与内二面角 theta，
      核对"绕铰链角和 = 2*pi"（平直判据）与亏角 eps = 0；
  (2) 由 (1) 定出 cot 权：最近邻（长边）W = k*cot(theta)，次近邻（短边）W = 0；
  (3) 验证 06 (3.2) 的四性质（对称、零行和、半正定、单零模）在 BCC 上成立；
  (4) 定出三维纯数 K：lambda_q = K * Omega^{2/3} * q^2，Omega = a^3/2。

只用链内已登记的量与外部标准工具（Delaunay 三角化、cot 公式）；不拟合。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环02_环03_BCC的cot拉普拉斯与K.py"
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
A_ = 1.0                        # 晶格常数 a = 1
L_NN = math.sqrt(3) / 2         # 最近邻（长边）
L_NNN = 1.0                     # 次近邻（短边，立方棱）


# ----------------------------------------------------------------------
# 几何
# ----------------------------------------------------------------------
def bcc_points(n=4):
    pts, lab = [], []
    for i, j, k in itertools.product(range(n), repeat=3):
        pts.append([i, j, k]); lab.append(("c", (i, j, k)))
        pts.append([i + .5, j + .5, k + .5]); lab.append(("m", (i, j, k)))
    return np.array(pts, float), lab


def dihedral(p, tet, edge):
    """四面体在 edge 上的**内二面角**：两法向取朝外后 theta = pi - phi。"""
    i, j = edge
    k, l = [x for x in tet if x not in edge]
    n1 = np.cross(p[j] - p[i], p[k] - p[i])
    n2 = np.cross(p[j] - p[i], p[l] - p[i])
    if np.dot(n1, p[l] - p[i]) > 0:
        n1 = -n1
    if np.dot(n2, p[k] - p[i]) > 0:
        n2 = -n2
    n1 /= np.linalg.norm(n1); n2 /= np.linalg.norm(n2)
    return math.pi - math.acos(float(np.clip(np.dot(n1, n2), -1.0, 1.0)))


def hinge_stats():
    p, lab = bcc_points(4)

    def tetvol(t):
        a, b, c, d = [p[i] for i in t]
        return abs(float(np.linalg.det(np.array([b - a, c - a, d - a])))) / 6.0

    simp = [tuple(int(x) for x in s) for s in Delaunay(p).simplices]
    # drop degenerate (zero-volume) simplices produced by cospherical points
    simp = [t for t in simp if tetvol(t) > 1e-9]
    ic = lab.index(("c", (1, 1, 1)))
    im = lab.index(("m", (1, 1, 1)))
    ic2 = lab.index(("c", (2, 1, 1)))

    def around(e):
        ts = [s for s in simp if set(e) <= set(s)]
        return ts, [dihedral(p, s, e) for s in ts]

    ts_nn, ang_nn = around((min(ic, im), max(ic, im)))
    ts_nnn, ang_nnn = around((min(ic, ic2), max(ic, ic2)))

    stats = {round(L_NN, 6): [], round(L_NNN, 6): []}
    seen = set()
    for s in simp:
        for e in itertools.combinations(s, 2):
            key = tuple(sorted(e))
            if key in seen:
                continue
            seen.add(key)
            # interior edges of the central cell only (both endpoints inside [1,2]^3)
            if not (np.all(p[list(e)] >= 1.0 - 1e-9) and np.all(p[list(e)] <= 2.0 + 1e-9)):
                continue
            L = round(float(np.linalg.norm(p[e[0]] - p[e[1]])), 6)
            if L in stats:
                ts = [t for t in simp if set(e) <= set(t)]
                stats[L].append((len(ts), dihedral(p, ts[0], e)))
    return dict(k_nn=len(ts_nn), th_nn=ang_nn, k_nnn=len(ts_nnn),
                th_nnn=ang_nnn, stats=stats, n_tet=len(simp))


# ----------------------------------------------------------------------
# L 与谱
# ----------------------------------------------------------------------
def bcc_L(n=2):
    """周期 n×n×n 常规胞的 L（节点图）。L_ij = -(1/2) k cot(theta) = -sqrt3（最近邻）。"""
    idx = {}
    for i, j, k in itertools.product(range(n), repeat=3):
        idx[(i, j, k)] = len(idx)
        idx[(i + .5, j + .5, k + .5)] = len(idx)
    N = len(idx)
    W = 6.0 / math.sqrt(3.0)          # = 2 sqrt3
    Lm = np.zeros((N, N))
    for (x, y, z), i1 in idx.items():
        for dx, dy, dz in itertools.product((-.5, .5), repeat=3):
            key = ((x + dx) % n, (y + dy) % n, (z + dz) % n)
            if key in idx:
                Lm[i1, idx[key]] += 0.5 * W
    Lm = -Lm
    np.fill_diagonal(Lm, 0.0)
    np.fill_diagonal(Lm, -Lm.sum(axis=1))
    return Lm


def lam_plane_wave(qvec):
    """无限 BCC：lambda(q) = sum_delta (W/2)(1 - cos q.delta)，8 个最近邻。"""
    W = 6.0 / math.sqrt(3.0)
    s = 0.0
    for dx, dy, dz in itertools.product((-.5, .5), repeat=3):
        s += 0.5 * W * (1.0 - math.cos(float(np.dot(qvec, [dx, dy, dz]))))
    return s


def main():
    g = hinge_stats()
    print("=== BCC Delaunay 铰链实数 ===")
    print("样品四面体总数:", g["n_tet"])
    print("最近邻长边 sqrt3/2：绕边 %d 个四面体，内二面角 %s 度，和 %.3f 度"
          % (g["k_nn"], sorted(set(round(math.degrees(t), 3) for t in g["th_nn"])),
             math.degrees(sum(g["th_nn"]))))
    print("次近邻短边 a      ：绕边 %d 个四面体，内二面角 %s 度，和 %.3f 度"
          % (g["k_nnn"], sorted(set(round(math.degrees(t), 3) for t in g["th_nnn"])),
             math.degrees(sum(g["th_nnn"]))))
    for L, rows in sorted(g["stats"].items()):
        ks = sorted(set(r[0] for r in rows))
        ths = sorted(set(round(math.degrees(r[1]), 3) for r in rows))
        print("  边长 %.6f：样本 %4d 条，k ∈ %s，二面角 ∈ %s" % (L, len(rows), ks, ths))

    assert g["k_nn"] == 6 and abs(g["th_nn"][0] - math.pi / 3) < 1e-9
    assert g["k_nnn"] == 4 and abs(g["th_nnn"][0] - math.pi / 2) < 1e-9
    assert abs(math.degrees(sum(g["th_nn"])) - 360.0) < 1e-6
    assert abs(math.degrees(sum(g["th_nnn"])) - 360.0) < 1e-6
    assert set(r[0] for r in g["stats"][round(L_NN, 6)]) == {6}
    assert set(r[0] for r in g["stats"][round(L_NNN, 6)]) == {4}

    W_nn = 6.0 * (1.0 / math.tan(math.pi / 3))
    W_nnn = 4.0 * (1.0 / math.tan(math.pi / 2))
    print("\n=== cot 权 ===")
    print("最近邻：W = 6*cot(60°) = %.6f = 2*sqrt3  (>0，无需 |cot|)" % W_nn)
    print("次近邻：W = 4*cot(90°) = %.6f" % W_nnn)
    assert abs(W_nn - 2 * math.sqrt(3)) < 1e-12
    assert abs(W_nnn) < 1e-12

    Lm = bcc_L(2)
    ev = np.linalg.eigvalsh(Lm)
    print("\n=== L 的四性质（16 原子周期超胞）===")
    print("对称：max|L-L^T| = %.2e" % np.abs(Lm - Lm.T).max())
    print("零行和：max|rowsum| = %.2e" % np.abs(Lm.sum(axis=1)).max())
    print("本征值：min %.6f  max %.6f  零模个数 %d"
          % (ev.min(), ev.max(), int(np.sum(np.abs(ev) < 1e-9))))
    assert np.abs(Lm - Lm.T).max() < 1e-14
    assert np.abs(Lm.sum(axis=1)).max() < 1e-12
    assert ev.min() > -1e-9
    assert int(np.sum(np.abs(ev) < 1e-9)) == 1

    om23 = 1.0 / (2.0 ** (2.0 / 3.0))
    Ks = {}
    print("\n=== 三维纯数 K ===")
    for name, qh in (("[100]", np.array([1.0, 0, 0])),
                     ("[110]", np.array([1, 1, 0]) / math.sqrt(2)),
                     ("[111]", np.array([1, 1, 1]) / math.sqrt(3))):
        qs = [1e-3 * 2 ** m for m in range(4)]
        rs = [lam_plane_wave(q * qh) / (om23 * q * q) for q in qs]
        Ks[name] = rs[0]                      # smallest q = closest to q -> 0
        print("  q∥%-5s lambda/(Omega^{2/3}q^2) = %s" % (name, ["%.6f" % r for r in rs]))
    K = Ks["[100]"]
    assert max(abs(K - Ks[n]) for n in Ks) < 1e-4      # isotropy at q^2 order
    assert abs(K - 2 ** (2 / 3) * math.sqrt(3)) < 1e-4
    print("  K = 2^{2/3}*sqrt3 = %.6f（q^2 阶各向同性）" % K)

    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.3))

    ax = axes[0]
    ax.plot(np.arange(len(ev)), np.sort(ev), "o-", ms=3.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("模式序号")
    ax.set_ylabel(r"$L$ 本征值（$a=1$）")
    ax.set_title(r"BCC 的 $L$：半正定、单零模（四性质成立）")
    ax.grid(alpha=0.3)

    ax = axes[1]
    qs = np.linspace(1e-3, 1.2, 300)
    for name, qh in (("[100]", np.array([1.0, 0, 0])),
                     ("[111]", np.array([1, 1, 1]) / math.sqrt(3))):
        r = np.array([lam_plane_wave(q * qh) / (om23 * q * q) for q in qs])
        ax.plot(qs, r, lw=1.8, label="q∥" + name)
    ax.axhline(K, color="k", ls="--", lw=1.0, label=r"$K=2^{2/3}\sqrt{3}=%.4f$" % K)
    ax.set_xlabel(r"$qa$")
    ax.set_ylabel(r"$\lambda_q/(\Omega^{2/3}q^2)$")
    ax.set_title("声学标度收敛到 $K$")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[2]
    labels = ["NN 长边\n$\\sqrt{3}a/2$", "NNN 短边\n$a$"]
    kvals = [g["k_nn"], g["k_nnn"]]
    thvals = [math.degrees(g["th_nn"][0]), math.degrees(g["th_nnn"][0])]
    x = np.arange(2)
    ax.bar(x - 0.2, kvals, width=0.4, label="绕边四面体数 $k$")
    ax.bar(x + 0.2, [t / 60 for t in thvals], width=0.4, label="二面角$/60^\\circ$")
    for xi, (kk, tt) in enumerate(zip(kvals, thvals)):
        ax.text(xi - 0.2, kk + 0.1, str(kk), ha="center", fontsize=10)
        ax.text(xi + 0.2, tt / 60 + 0.1, "%.0f°" % tt, ha="center", fontsize=10)
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0, 7.5)
    ax.set_title(r"$k\theta=2\pi$（平直判据）⇒ $\varepsilon_e=0$")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "环02_环03_BCC的cot拉普拉斯.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)

    csv_path = os.path.join(OUT, "环02_环03_BCC的cot拉普拉斯.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["量", "值", "说明"])
        w.writerow(["NN 长边/a", "%.6f" % L_NN, "最近邻；k=6；二面角 60°；cot=+1/sqrt3"])
        w.writerow(["NNN 短边/a", "%.6f" % L_NNN, "次近邻；k=4；二面角 90°；cot=0"])
        w.writerow(["NN 权 W", "%.6f" % W_nn, "6*cot60 = 2sqrt3 > 0（正权，无需 |cot|）"])
        w.writerow(["NNN 权 W", "%.6f" % W_nnn, "4*cot90 = 0"])
        w.writerow(["每原子体积/a^3", "0.5", "BCC 两原子/常规胞"])
        w.writerow(["K", "%.6f" % K, "lambda_q = K Omega^{2/3} q^2"])
        w.writerow(["L min 本征值", "%.3e" % ev.min(), ">=0 半正定"])
        w.writerow(["零模个数", "1", "常数模"])
    print("\n图：", os.path.basename(png))
    print("表：", os.path.basename(csv_path))


if __name__ == "__main__":
    main()
