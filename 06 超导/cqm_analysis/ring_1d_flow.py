# -*- coding: utf-8 -*-
"""
一维闭环节点链: 乘积递推放到首尾相接的节点环(可复核)
============================================================

按用户要求: 只建闭环几何结构, 性质后面按前面的理论(位置-动量->声子->亏角->固有时流速
的乘积递推)自然推出, 不预设闭合判据。

结构: 一维闭环 = 首尾相接节点环, 每条边(节点间)一个亏角 eps_{k,k+1}。
递推(前面理论): v_{k+1} = v_k * sqrt(1 - eps_{k,k+1}/2pi)  (LQG接口, 乘积关系)
绕环一周: v_o' = (prod r) * v_o,  r=sqrt(1-eps/2pi) 逐边比值。

性质(自然推出, 非预设):
  - 开链: 无反馈, v_o 自由; 闭环: 首尾同一节点, 单值性要求 v_o'=v_o => prod r=1 (反馈约束)。
  - Delaunay 剖分 eps>=0 => prod r<=1 => 绕环衰减; 严格单值需 eps 正负抵消(鞍形)。

边界: G10闭环条件动力学形式未闭合, G19和乐容差未闭合(权威源 06超导 §13);
      本脚本仅建结构+推乘积递推, 不预设闭合判据、不臆造 alpha。
"""
import sys, math
sys.stdout.reconfigure(encoding="utf-8")

HERE = __file__.rsplit("\\", 1)[0].rsplit("/", 1)[0]
sys.path.insert(0, HERE)
from lattice_regge_model import bcc_lattice, build_cot_laplacian


def find_triangle_rings(hinges, max_rings=4):
    """邻接图中找 3-环(闭合节点链)作为一维闭环样例"""
    adj = {}
    for (i, j), angs in hinges.items():
        e = 2 * math.pi - sum(angs)
        adj.setdefault(i, {})[j] = e; adj.setdefault(j, {})[i] = e
    rings = []; seen = set()
    for a in adj:
        for b, eab in adj[a].items():
            if b <= a: continue
            for c, ebc in adj[b].items():
                if c <= b: continue
                if c in adj[a]:
                    key = tuple(sorted((a, b, c)))
                    if key not in seen:
                        seen.add(key); rings.append(([a, b, c], [eab, ebc, adj[a][c]]))
        if len(rings) >= max_rings: break
    return rings


def main():
    pts = bcc_lattice(n=1)
    _, n_tet, hinges, _ = build_cot_laplacian(pts)
    rings = find_triangle_rings(hinges)

    print("=" * 70)
    print("[闭环结构] 一维闭环 = 首尾相接节点环; 每条边一个亏角 eps")
    print("[前面理论] 乘积递推 v_{k+1}=v_k*sqrt(1-eps_{k,k+1}/2pi); 绕一周 v_o'=prod(r)*v_o")
    print()
    for nodes, es in rings:
        rs = [math.sqrt(max(1 - e / (2 * math.pi), 0)) for e in es]
        P = math.prod(rs)
        print(f"  环{nodes}: eps=[{', '.join('%.3f' % e for e in es)}]")
        print(f"    r=[{', '.join('%.3f' % r for r in rs)}], prod r={P:.4f}, v_o'={P:.4f}*v_o")

    print("\n" + "=" * 70)
    print("性质(由闭环拓扑+前面乘积递推自然推出, 非预设):")
    print("  开链无反馈 v_o 自由; 闭环首尾同一节点, 单值性 v_o'=v_o => prod r=1 (反馈约束)。")
    print("  Delaunay eps>=0 => prod r<=1 => 绕环衰减; 严格单值需 eps 正负抵消(鞍形)。")
    print("  边界: G10闭环条件动力学形式/G19和乐容差未闭合; 不预设判据、不臆造 alpha。")


if __name__ == "__main__":
    main()
