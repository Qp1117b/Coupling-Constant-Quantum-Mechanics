# 06 · 动态机制

> 维度 5。把论证表建模为**重写系统**，做前向派生仿真，刻画理论结构的动态展开。

| 目录 | 文件 | 内容 |
|:---|:---|:---|
| `演化模型/` | `理论状态模型.md` | 状态向量 $s_t=(\mathcal K_t,\mathcal P_t,\mathcal G_t,\mathcal L_t)$ 与转移算子 |
| | `初始状态.json` | 种子概念（44 个） |
| `重写规则/` | `重写规则.json` | 61 条规则（`lhs ⊆ 已有 ⇒ 派生 rhs`） |
| | `重写规则.md` | 规则格式与统计 |
| `仿真/` | `simulate.py` | 前向派生复算与轨迹校验 |
| | `derivation_trace.csv` | 每步触发规则 |
| | `derivation_order.csv` | 节点派生顺序与深度 |
| | `dynamic_hypergraph.json` | 超图 + `derive_depth` 标注 |
| | `README.md` | 算法与结果 |

**结果**：种子 44 → 4 轮 → 触发 49 条 → 可达 **81/82**；不可达 1 概念（C074 共形固定点），如实登记。构建：`_build/build_dynamics.py`。
