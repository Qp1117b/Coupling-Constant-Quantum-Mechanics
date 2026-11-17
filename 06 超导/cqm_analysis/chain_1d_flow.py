# -*- coding: utf-8 -*-
"""
一维节点链固有时流速序列（局域比值递推）——可复核
==========================================================

权威口径 + 用户纠正:
  - 亏角都是【节点之间(铰链)】的, 没有"节点自身亏角"; 每条相邻边 (k,k+1)
    有唯一亏角 eps_{k,k+1} = 2pi - sum_{T⊃e} theta。
  - LQG 铰链亏角-固有时流速关系(FG_核心理论 §3.1): 相邻节点流速【比值】
        v_{k+1} / v_k = sqrt(1 - eps_{k,k+1}/2pi)      (曲率载体 = 两节点间边亏角)
  - 这是【局域递推】: 下一步流速只由【前一个节点流速】+【当前边亏角】决定,
    不是前面节点的"加和", 也不是什么全局累积/全局同步。
  - 参考节点(第1个)流速记为 v_o (origin/reference node), 是变量符号, 非数值1。
  - 一维开链无环 => 无反馈, 不存在全局固有时流速同步 => 不引入全局集体量/加和叙事。

模型(纯局域递推):
    v1 = v_o (参考节点)
    v_{k+1} = v_k * sqrt(1 - eps_{k,k+1}/2pi)     (逐节点, 只用前一步 + 当前边亏角)

验证: 相邻比值由边亏角给出; 递推自洽; 一维开链无反馈/无全局同步(不引入集体加和)。

边界: FG接口假设; 参考节点 v_o 是自由变量; u与p_u共轭, 不从 v 臆造 alpha;
      u_i 量子化待 W-3。
"""
import sys, math
import numpy as np
sys.stdout.reconfigure(encoding="utf-8")

HERE = __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0]
sys.path.insert(0, HERE)
from lattice_regge_model import bcc_lattice, fcc_lattice, hcp_lattice, build_cot_laplacian

XIS = 0.02309570897  # README 权威值（仅 DNR 对照用，不参与链递推）


def extract_chain(hinges, N, start=0):
    """从邻接图(边亏角为权重)提取一维开链(贪心走未访问邻居)"""
    adj = {i: [] for i in range(N)}
    for (i, j), angs in hinges.items():
        e = 2 * math.pi - sum(angs)
        adj[i].append((j, e)); adj[j].append((i, e))
    chain = [start]; visited = {start}; cur = start
    while True:
        nxt = [(j, e) for j, e in adj[cur] if j not in visited]
        if not nxt:
            break
        j, e = max(nxt, key=lambda x: abs(x[1]))
        chain.append(j); visited.add(j); cur = j
    return chain, adj


def main():
    for name, pts in [("BCC-Nb", bcc_lattice(n=2)), ("FCC-Al", fcc_lattice(n=2))]:
        _, n_tet, hinges, _ = build_cot_laplacian(pts)
        N = len(pts)
        chain, adj = extract_chain(hinges, N, start=0)

        # 局域递推: v_{k+1} = v_k * r_k, r_k 只由当前边亏角定; 起点 v_1 = v_o (符号变量)
        v_sym = "v_o"  # 参考节点流速符号(变量, 非数值)
        ratios = []
        v = [v_sym]  # 符号序列
        v_num = [1.0]  # 数值仅作比值显示(v_k/v_o), 不代表 v_o=1
        for a, b in zip(chain[:-1], chain[1:]):
            e = next(e for j, e in adj[a] if j == b)          # 两节点间边亏角
            r = math.sqrt(max(1 - e / (2 * math.pi), 0))      # LQG 接口给相邻流速比
            ratios.append(r)
            v_num.append(v_num[-1] * r)                        # 局域递推一步
        ratios = np.array(ratios); v_num = np.array(v_num)

        print("=" * 70)
        print(f"{name}: 一维开链长={len(chain)}; 亏角都是节点间边亏角")
        print(f"  递推 v_(k+1) = v_k * sqrt(1 - eps_(k,k+1)/2pi), 起点 v_1 = {v_sym}(变量)")
        print(f"  相邻流速比 r_k 范围[{ratios.min():.4f},{ratios.max():.4f}] (当前边亏角定)")
        print(f"  序列 v_k / v_o (前8)={[round(x,4) for x in v_num[:8]]}  <- 仅为比值显示")
        print(f"  验证相邻比值 v_(k+1)/v_k = r_k: {np.allclose(v_num[1:]/v_num[:-1], ratios)}")
        print(f"  一维开链无环 => 无反馈 => 不存在全局固有时流速同步(不引入集体加和)")

    print("\n" + "=" * 70)
    print("链: 节点间边亏角 -> LQG接口给相邻流速比 -> 乘积关系 v_k = v_o * prod(r_j)")
    print("  v_(k+1)=v_k*r_k: 每一步由前一步+当前边亏角定; 是【乘积关系】, 不是加和。")
    print("  参考节点流速 v_o 是变量符号, 非数值1; 一维开链无反馈, 无全局同步。")
    print("  不臆造 alpha; u 与 p_u 共轭, 耦合常数待同步方程锁定(W-3)。")


if __name__ == "__main__":
    main()
