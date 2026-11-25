#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""全链 R1-R60 结构地图 DAG 可视化（非数据拟合，只表发生学串联）"""
import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
try:
    import networkx as nx
    HAS_NX = True
except ImportError:
    HAS_NX = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "全链结构地图_R1R60.png")
SUM = os.path.join(HERE, "全链结构地图_R1R60_摘要.txt")

log = []
def emit(s=""):
    print(s); log.append(s)

# 11 条链的串联边（R43-R60 新增 5 条链）
chains = {
    "L7 关联核→GL": [("R43","R44"),("R44","R45"),("R45","R46"),("R46","R48"),("R48","R49"),("R46","R47")],
    "L8 记忆核谱": [("R50","R51"),("R51","R52"),("R52","R53")],
    "L9 GL磁场/上界": [("R46","R54"),("R16","R57"),("Uemura","R57")],
    "L10 上限/积分": [("R43","R56"),("R50","R58")],
    "L11 数值核对": [("README_Xi","R59"),("main634","R60")],
}

emit("=" * 60)
emit("全链 R1-R60 结构地图：新增 5 条串联链（R43-R60）")
emit("=" * 60)
total_edges = 0
for name, edges in chains.items():
    emit(f"  {name}: {len(edges)} edges, {len(set([n for e in edges for n in e]))} nodes")
    total_edges += len(edges)
emit(f"  总边数 = {total_edges}")
emit("  层级：14 链内结构 + 1 B类 + 2 综合检验 + 2 数值核对 + 4 回改")
emit("  边界：绝对 Tc 缺口位置不变（Z2/R8/临-5/6/G22）")

if HAS_NX:
    G = nx.DiGraph()
    for name, edges in chains.items():
        for a, b in edges:
            G.add_edge(a, b, chain=name)
    emit(f"  DAG check: is_dag={nx.is_directed_acyclic_graph(G)}, nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")
    fig, ax = plt.subplots(figsize=(13, 9))
    pos = nx.spring_layout(G, seed=42, k=0.6)
    colors = {"L7 关联核→GL":"steelblue","L8 记忆核谱":"darkorange","L9 GL磁场/上界":"seagreen",
              "L10 上限/积分":"purple","L11 数值核对":"crimson"}
    for name, col in colors.items():
        es = [(a,b) for a,b,d in G.edges(data=True) if d.get("chain")==name]
        ns = list(set([n for e in es for n in e]))
        nx.draw_networkx_nodes(G, pos, nodelist=ns, node_color=col, node_size=400, alpha=0.8, ax=ax, label=name if ns else None)
        nx.draw_networkx_edges(G, pos, edgelist=es, edge_color=col, alpha=0.6, ax=ax, arrows=True, arrowsize=12)
    nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
    ax.set_title("Full-chain structure map v2: R43-R60 new chains (DAG, non-fit)")
    ax.axis("off")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT, dpi=120)
else:
    emit("  networkx unavailable; skip DAG draw")

with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE edges={total_edges} is_dag={HAS_NX and nx.is_directed_acyclic_graph(G)}")
