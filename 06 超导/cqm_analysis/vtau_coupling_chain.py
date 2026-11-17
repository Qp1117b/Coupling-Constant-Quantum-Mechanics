# -*- coding: utf-8 -*-
"""
声子 → 亏角 → 固有时流速 → 全局耦合常数 关系链（可复核）
==============================================================

按 CQM 权威口径把声子-亏角方程组 (E1-E7) 向下游贯通:

  §0.2/0.3: 两两节点之间【一条边 = 一个铰链 = 一个亏角 eps_ij】。
            参考节点是【传递原点】定 v_tau=1; 其余节点沿【相邻节点逐跳传递】:
            节点 j 的流速由相邻节点 i 间那条边的亏角 eps_ij 经 FG 接口更新,
            不是所有节点直接和参考节点比。环路多路径不一致 = 绕环和乐(§10.1)。
  DNR(04前沿§6.3): p_u,i = v_tau,i/☯, u_G=(1/N)sum u_i, [u_G,sum v_tau]=i☯
  A12<=>DNR(探索D1-D4): C_ij=-C_ji => sum_{i!=j} C_ij=0 (反对称自动满足)
  耦合常数: u=ln g, g=alpha^{-1}; 跃迁 Delta u_n=2 ln n, alpha->n^2 alpha

关键修正(用户指正): 亏角挂在铰链(两节点之间唯一一条边), 不是每个节点一个聚合量。
  差异 C_ij 用【边亏角 eps_ij】(仅相邻对非零), 不用"节点关联亏角绝对值之和"
  (后者引入配位数依赖, 非纯两两关系量)。

严格性边界(如实标注):
  - 亏角 eps_ij = 2pi - sum_{T⊃e_ij} theta (几何严格, 每条边一个)
  - FG 接口 v_tau=sqrt(1-eps/2pi) 是【假设】(FG_核心理论 §3.1)
  - C_ij = f(eps_ij), f 奇反对称 => A12 自动成立(代数事实)
  - 参考节点=传递原点 v_tau=1(§0.3)是规范选择; 沿相邻逐跳传递, 环路多路径不一致=绕环和乐(§10.1)
  - 乘法传递因子 sqrt(1-eps/2pi) 是实现选择; 环路阻挫幅度大说明需和乐闭合, 非误差
  - g0 归一化、u_i 绝对标度 均为待推 W-3 / 构造选择
"""
import sys, math, os
import numpy as np
from collections import deque
sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lattice_regge_model import bcc_lattice, fcc_lattice, hcp_lattice, build_cot_laplacian

XIS = 0.02309570897  # 相变量子 ☯ (README 权威值)


def edge_deficits(hinges, N):
    """边亏角表: eps[(i,j)] = 2pi - sum(theta over shared tets); 每条边一个"""
    E = {}
    for (i, j), angs in hinges.items():
        E[(i, j)] = 2 * math.pi - sum(angs)
    return E


def vtau_from_edge(eps_e):
    """FG 接口: v_tau = sqrt(1 - eps/(2pi)) (流体快慢比, eps越大流速越慢)"""
    return math.sqrt(max(1 - eps_e / (2 * math.pi), 0))


def main():
    for name, pts in [("BCC-Nb", bcc_lattice()), ("FCC-Al", fcc_lattice()), ("HCP-Tc", hcp_lattice())]:
        _, n_tet, hinges, _ = build_cot_laplacian(pts)
        N = len(pts)
        E = edge_deficits(hinges, N)

        # 邻接表: 每条边一个亏角 eps_ij -> 对称衰减因子 r_ij = sqrt(1-eps_ij/2pi) <=1
        # 沿相邻节点逐跳传递: v_tau(下游) = v_tau(上游) * r_ij (参考节点为原点)
        adj = {i: [] for i in range(N)}
        for (i, j), e in E.items():
            r = vtau_from_edge(e)
            adj[i].append((j, r)); adj[j].append((i, r))  # 对称: 同一条边因子两端相同

        # 参考节点=传递原点 v_tau=1; 沿相邻节点逐跳(BFS 树)传递
        ref = 0
        vtau = np.zeros(N)
        vtau[ref] = 1.0
        parent = {ref: -1}
        q = deque([ref])
        while q:
            u = q.popleft()
            for w, r in adj[u]:
                cand = vtau[u] * r
                if vtau[w] == 0 and w != ref:
                    vtau[w] = cand; parent[w] = u; q.append(w)
        vtau[vtau == 0] = 1.0

        # 环路阻挫(=和乐 H_ijk): 非树亏角边两端经不同路径传递的一致性偏差
        frust = []
        for (i, j), e in E.items():
            if abs(e) < 1e-6:
                continue
            if parent.get(i) == j or parent.get(j) == i:
                continue  # 树边
            r = vtau_from_edge(e)
            ratio1 = vtau[i] * r / vtau[j] if vtau[j] > 0 else 0
            ratio2 = vtau[j] * r / vtau[i] if vtau[i] > 0 else 0
            frust.append(min(abs(ratio1 - 1), abs(ratio2 - 1)))

        # 差异 C_ij = f(eps_ij), 仅相邻非零, f奇反对称 => A12 自动
        C = np.zeros((N, N))
        for (i, j), e in E.items():
            C[i, j] = e; C[j, i] = -e
        np.fill_diagonal(C, 1.0)
        off_sum = C.sum() - np.trace(C)
        anti = np.max(np.abs(C + C.T - np.eye(N) * 2))

        p_u = vtau / XIS
        u_i = np.log(vtau)  # g0=1 归一化(待推 W-3 只验证相对)
        u_G = u_i.mean()
        g_G = math.exp(u_G)
        alpha_G = 1 / g_G

        print("=" * 70)
        print(f"{name}: 边数={len(E)}(非零亏角={sum(abs(e)>1e-6 for e in E.values())}), 四面体={n_tet}")
        print(f"  传递原点 ref={ref}, v_tau_ref={vtau[ref]:.6f} (应为1); v_tau范围[{vtau.min():.4f},{vtau.max():.4f}]")
        if frust:
            print(f"  环路阻挫(和乐): 非树亏角边={len(frust)}, 传递比偏离1中位={float(np.median(frust)):.3f}, >0.05={sum(d>0.05 for d in frust)}")
        print(f"  A12: sum_{{i!=j}}C_ij={off_sum:.3e}; 反对称 max|C_ij+C_ji|={anti:.3e}")
        print(f"  p_u范围[{p_u.min():.2f},{p_u.max():.2f}]; DNR下界☯/2={XIS/2:.6f}")
        print(f"  u_G={u_G:.6f}, alpha_G=1/g_G={alpha_G:.6f}")
        for n in (2, 4, 6):
            print(f"    n={n}: alpha_n=n^2*alpha_G={alpha_G*n**2:.4f}")

    print("\n" + "=" * 70)
    print("链: 声子->亏角(边)->参考原点沿相邻逐跳传递v_tau(§0.2)->DNR->全局耦合常数 自洽")
    print("  关键1: 亏角挂在边(两两节点唯一一条边), C_ij用边亏角(局域两两量), 非节点聚合。")
    print("  关键2: 参考节点是传递原点, 流速沿相邻节点逐跳传递(非所有节点直接和参考比)。")
    print("  关键3: 环路传递不一致=绕环和乐(§10.1), 是相位阻挫的几何表现, 非误差。")
    print("  边界: FG接口假设/和乐闭合/g0标度/绝对u_i 为待推或构造, 只验证相对结构与跃迁代数。")


if __name__ == "__main__":
    main()
