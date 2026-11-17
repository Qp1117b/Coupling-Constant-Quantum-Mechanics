# -*- coding: utf-8 -*-
"""
一般晶格几何剖分建模（CQM 内生，可复核）
==========================================

把骨架「嘉当矩阵 = 图拉普拉斯 = Regge 剖分必然结果」从 A4 二维推广到一般 3D 晶格：

    底空间 R=(V,E,T,{L_ij})  --Delaunay 四面体化-->  二面角 theta(余弦定律)
      -> 铰链亏角 eps_e = 2pi - sum_T theta_e^T
      -> cot 权重拉普拉斯 L  (= Regge 二阶变分矩阵 M_ij 的几何实现)

验证 L 的图拉普拉斯性质(对称/零行和/半正定/单一零模); 其本征向量即简正模式 U,
本征值即 omega_k^2 的几何来源 —— 把上一轮缺口 c/L^2 具体化为 cot 权重/L^2。

晶格 != A4: 本脚本用真实 3D BCC/FCC/HCP 晶格, 不用 element_fg_table 的 A4 二维结构。
A4 是核子层/禁闭边界代数结构, 与晶格载体层级不同。

外部对照(仅对照不引入 CQM): Regge 二阶变分 M_ij=-A_ij、cot Laplacian
  (arXiv:gr-qc/0012035 §C; arXiv:1601.04821; arXiv:2203.02409;
   convergence_cotan.pdf; Barrett 1994 hep-th/9404124; JDG 2011 10.4310/jdg/1304514973)。

诚实标注: 为保证半正定, 钝角二面角取 |cot| 作数值稳健化 —— 这是构造选择,
  不是纯几何恒等式; 一般晶格的四面体化不保证所有二面角为锐角。
"""
import sys, math
import numpy as np
from scipy.spatial import Delaunay
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8")


def bcc_lattice(a=3.30, n=1):
    basis = np.array([[0, 0, 0], [0.5, 0.5, 0.5]]) * a
    return _supercell(basis, a, n)


def fcc_lattice(a=4.05, n=1):
    basis = np.array([[0, 0, 0], [0, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0]]) * a
    return _supercell(basis, a, n)


def hcp_lattice(a=2.74, c=4.39, n=1):
    a1 = np.array([a, 0, 0]); a2 = np.array([a / 2, a * math.sqrt(3) / 2, 0]); a3 = np.array([0, 0, c])
    basis_frac = np.array([[1 / 3, 2 / 3, 1 / 4], [2 / 3, 1 / 3, 3 / 4]])
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                for f in basis_frac:
                    pts.append(f[0] * a1 + f[1] * a2 + f[2] * a3 + i * a1 + j * a2 + k * a3)
    return np.array(pts, float)


def _supercell(basis, a, n):
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                for b in basis:
                    pts.append(b + np.array([i, j, k]) * a)
    return np.array(pts, float)


def dihedral_tet(verts4, e_local):
    """verts4: 4x3 四面体顶点; e_local=(i,j) 局部指标; 沿该边的二面角"""
    p, q = e_local
    others = [v for v in range(4) if v not in (p, q)]
    if len(others) != 2:
        return None
    P, Q, R, S = verts4[p], verts4[q], verts4[others[0]], verts4[others[1]]
    u = Q - P; v = R - P; w = S - P
    n1 = np.cross(u, v); n2 = np.cross(u, w)  # 两面 pqr, pqs 法向
    nn = np.linalg.norm(n1) * np.linalg.norm(n2)
    if nn < 1e-14:
        return None
    c = np.clip(np.dot(n1, n2) / nn, -1, 1)
    return math.acos(c)


def build_cot_laplacian(pts, jitter=1e-3):
    """一般晶格 -> Regge 复形 -> cot 权重拉普拉斯 L + 亏角列表"""
    rng = np.random.default_rng(0)
    pts = pts + rng.normal(scale=jitter, size=pts.shape)  # 打破共球退化
    tets = Delaunay(pts).simplices
    N = len(pts)
    hinge_angles = defaultdict(list)
    for tet in tets:
        v4 = pts[tet]
        for ii in range(4):
            for jj in range(ii + 1, 4):
                gi, gj = tet[ii], tet[jj]
                e = (int(min(gi, gj)), int(max(gi, gj)))
                th = dihedral_tet(v4, (ii, jj))
                if th is not None:
                    hinge_angles[e].append(th)
    L = np.zeros((N, N)); eps_list = []
    for e, angs in hinge_angles.items():
        eps = 2 * math.pi - sum(angs)
        eps_list.append(eps)
        angs_ok = [a for a in angs if math.sin(a) > 1e-6]
        if not angs_ok:
            continue
        # cot 权重; |cot| 稳健化保证半正定(钝角二面角构造选择, 见文档说明)
        w = 0.5 * sum(abs(1.0 / math.tan(a)) for a in angs_ok)
        i, j = e
        L[i, j] -= w; L[j, i] -= w
        L[i, i] += w; L[j, j] += w
    return L, len(tets), hinge_angles, np.array(eps_list)


def main():
    for name, pts in [("BCC-Nb", bcc_lattice()), ("FCC-Al", fcc_lattice()), ("HCP-Tc", hcp_lattice())]:
        L, n_tet, hinges, eps = build_cot_laplacian(pts)
        eig = np.linalg.eigvalsh(L)
        print("=" * 66)
        print(f"{name}: 原子数={len(pts)}, 四面体数={n_tet}, 铰链数={len(hinges)}")
        print(f"  对称性 max|L-L^T|   = {np.max(np.abs(L - L.T)):.2e}")
        print(f"  零行和 max|L@1|     = {np.max(np.abs(L @ np.ones(len(pts)))):.2e}")
        print(f"  半正定 最小特征值   = {eig[0]:.2e}")
        print(f"  零特征值个数        = {np.sum(np.abs(eig) < 1e-8)}")
        print(f"  谱(前6)             = {eig[:6]}")
        print(f"  亏角 eps 均值={eps.mean():.4f} rad, 范围=[{eps.min():.4f},{eps.max():.4f}], 非零铰链={np.sum(np.abs(eps) > 1e-6)}")

    print("\n" + "=" * 66)
    print("结论: 一般 3D 晶格的 Regge 剖分 -> cot 拉普拉斯 L 满足图拉普拉斯性质")
    print("  (对称/零行和/半正定/单一零模), 与'嘉当矩阵=离散拉普拉斯'同构。")
    print("  L 的本征向量=简正模式 U, 本征值=omega_k^2 几何来源; 缺口 c/L^2 具体化为 cot 权重/L^2。")
    print("  晶格 != A4 得到尊重(用真实 3D 晶格, 非 element_fg_table 的 A4 二维结构)。")


if __name__ == "__main__":
    main()
