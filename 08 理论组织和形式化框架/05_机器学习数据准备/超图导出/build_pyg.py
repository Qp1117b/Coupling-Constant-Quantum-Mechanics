# -*- coding: utf-8 -*-
"""
把 超图导出/ 里的 (x, hyperedge_index, edge_index) 装配为 PyG / DGL 对象。
依赖（较重，按需安装）：pip install torch torch-geometric
本脚本只在安装 torch 后运行；未安装时以 .npz 为源数据。
"""
import numpy as np, json, os

def load():
    z = np.load(os.path.join(os.path.dirname(__file__), "hypergraph_index.npz"))
    return z["x"], z["hyperedge_index"], z["edge_index"]

def to_pyg():
    import torch
    from torch_geometric.data import Data, HypergraphData
    x, hei, ei = load()
    x = torch.tensor(x, dtype=torch.float)
    hei = torch.tensor(hei, dtype=torch.long)
    ei = torch.tensor(ei, dtype=torch.long)
    hyper = HypergraphData(x=x, hyperedge_index=hei)
    graph = Data(x=x, edge_index=ei)
    return hyper, graph

def to_dgl():
    import dgl, torch
    x, hei, ei = load()
    g = dgl.graph((torch.tensor(ei[0]), torch.tensor(ei[1])))
    g.ndata["feat"] = torch.tensor(x, dtype=torch.float)
    hg = dgl.DGLGraph()  # 超图请用 dgl 的二分图构造（节点 = 概念 ∪ 超边）
    return g, hg

if __name__ == "__main__":
    h, g = to_pyg()
    print(h, g)
