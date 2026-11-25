# -*- coding: utf-8 -*-
"""
R37: 全链 R1-R37 可审计结构地图——依赖 DAG 可视化（拓扑图，非数据拟合）。
节点=推导块，边=前件依赖，颜色=层级状态。无拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/R37_全链结构地图DAG.py"
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

# (节点, 层级) 层级：landed=落地主链, alg=代数严格, judge=判据比值, void=作废, struct=结构/核对
NODES = {
    "环4-10-9-M6-FE01": "base",
    "R1 λ几何": "alg",
    "FE10 η几何": "landed",
    "R30审计": "struct",
    "R29质量无关": "judge",
    "R22预言精确": "landed",
    "R23判别实验": "judge",
    "12.A3 w=1/k": "base",
    "临21 n_eff": "base",
    "R2作废": "void",
    "R3作废": "void",
    "R15最大Tc": "judge",
    "R4模和no-go": "alg",
    "R5 DOS": "alg",
    "R7温度no-go": "alg",
    "R8不可能性": "alg",
    "FE09旧作废": "void",
    "R10核修正": "alg",
    "R11证伪状态": "alg",
    "HM§2.3回溯必然": "base",
    "R16 ≤min": "landed",
    "R17赝能隙": "landed",
    "R18必要条件": "landed",
    "临19磁场": "base",
    "R19方向判据": "landed",
    "R24 μ*=0极限": "judge",
    "R25 εF/ωD比值": "judge",
    "审-14": "base",
    "R27假闭合": "judge",
    "R28量纲no-go": "judge",
    "R31权重比复核": "judge",
    "R32分档结构": "judge",
    "R34配对记账": "judge",
    "R33间距判别": "judge",
    "R35几何权重": "judge",
    "R36跨块核对": "struct",
}

EDGES = [
    ("环4-10-9-M6-FE01", "R1 λ几何"),
    ("R1 λ几何", "FE10 η几何"),
    ("R1 λ几何", "R29质量无关"),
    ("R1 λ几何", "R22预言精确"),
    ("FE10 η几何", "R22预言精确"),
    ("FE10 η几何", "R30审计"),
    ("R22预言精确", "R23判别实验"),
    ("12.A3 w=1/k", "R2作废"),
    ("12.A3 w=1/k", "R4模和no-go"),
    ("临21 n_eff", "R2作废"),
    ("R2作废", "R3作废"),
    ("R3作废", "R15最大Tc"),
    ("R4模和no-go", "R8不可能性"),
    ("R5 DOS", "R8不可能性"),
    ("R7温度no-go", "R8不可能性"),
    ("12.A3 w=1/k", "R5 DOS"),
    ("R4模和no-go", "FE09旧作废"),
    ("FE09旧作废", "R10核修正"),
    ("R10核修正", "R11证伪状态"),
    ("HM§2.3回溯必然", "R16 ≤min"),
    ("R16 ≤min", "R17赝能隙"),
    ("R17赝能隙", "R18必要条件"),
    ("临19磁场", "R19方向判据"),
    ("R24 μ*=0极限", "审-14"),
    ("R25 εF/ωD比值", "审-14"),
    ("R27假闭合", "R28量纲no-go"),
    ("R28量纲no-go", "R30审计"),
    ("12.A3 w=1/k", "R31权重比复核"),
    ("R31权重比复核", "R36跨块核对"),
    ("R35几何权重", "R36跨块核对"),
]

COLOR = {
    "landed": "#2ca02c",
    "alg": "#1f77b4",
    "judge": "#ff7f0e",
    "void": "#d62728",
    "struct": "#9467bd",
    "base": "#8c8c8c",
}
LABEL = {
    "landed": "已落地主链", "alg": "代数严格", "judge": "判据/比值",
    "void": "作废", "struct": "审计/核对", "base": "链内前件",
}


def assertions():
    out = {}
    out["n_nodes"] = len(NODES)
    out["n_edges"] = len(EDGES)
    G = nx.DiGraph(); G.add_nodes_from(NODES); G.add_edges_from(EDGES)
    out["is_dag"] = bool(nx.is_directed_acyclic_graph(G))
    out["n_components"] = nx.number_weakly_connected_components(G)
    # 落地主链节点数
    out["n_landed"] = sum(1 for v in NODES.values() if v == "landed")
    out["n_void"] = sum(1 for v in NODES.values() if v == "void")
    return out


def plots(a):
    G = nx.DiGraph(); G.add_nodes_from(NODES); G.add_edges_from(EDGES)
    fig, ax = plt.subplots(figsize=(20, 13))
    # 分层布局：按链手动设 y 层
    layers = {
        "环4-10-9-M6-FE01": 0, "12.A3 w=1/k": 0, "临21 n_eff": 0,
        "HM§2.3回溯必然": 0, "临19磁场": 0,
        "R1 λ几何": 1, "R2作废": 1, "R4模和no-go": 1, "R16 ≤min": 1,
        "R24 μ*=0极限": 1, "R25 εF/ωD比值": 1, "R27假闭合": 1,
        "R15最大Tc": 2,
        "FE10 η几何": 2, "R3作废": 2, "R5 DOS": 2, "FE09旧作废": 2,
        "R17赝能隙": 2, "审-14": 2, "R31权重比复核": 2,
        "R30审计": 3, "R29质量无关": 3, "R22预言精确": 3, "R7温度no-go": 3,
        "R10核修正": 3, "R18必要条件": 3, "R28量纲no-go": 3,
        "R35几何权重": 3, "R32分档结构": 3, "R34配对记账": 3, "R33间距判别": 3,
        "R8不可能性": 4, "R23判别实验": 4, "R19方向判据": 4, "R11证伪状态": 4, "R36跨块核对": 4,
    }
    pos = {}
    per_layer = {}
    for n, y in layers.items():
        per_layer.setdefault(y, []).append(n)
    for y, ns in per_layer.items():
        for i, n in enumerate(ns):
            pos[n] = ((i - (len(ns) - 1) / 2) * 2.6, -y * 2.2)
    colors = [COLOR[NODES[n]] for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=1500,
                           edgecolors="white", linewidths=1.5, alpha=0.95)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=14, edge_color="#999",
                           alpha=0.6, connectionstyle="arc3,rad=0.05")
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="white", font_weight="bold")
    handles = [plt.Line2D([0], [0], marker="o", color="w", markerfacecolor=c,
                          markersize=12, label=LABEL[k]) for k, c in COLOR.items()]
    ax.legend(handles=handles, loc="upper left", fontsize=10)
    ax.set_title("全链 R1–R37 可审计结构地图：依赖 DAG（六条串联链，拓扑可视化，非拟合）", fontsize=14)
    ax.axis("off")
    png = os.path.join(HERE, "R37_全链结构地图DAG.png")
    fig.savefig(png, dpi=130, bbox_inches="tight"); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R37 结构地图断言 ===")
    for k, v in a.items():
        print(f"{k:20s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R37_全链结构地图DAG_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
