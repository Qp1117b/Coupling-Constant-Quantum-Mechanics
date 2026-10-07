# 动态机制 · 仿真

> 以 `../重写规则/重写规则.json` 为规则库，做前向派生（forward chaining）仿真。

## 一、运行

```bash
python simulate.py            # 复算派生轨迹并校验与已生成 CSV 一致
```

## 二、算法

1. 种子 $S_0$：论证表中不作为任何规则后件的概念（基元/接口概念）（44 个）。
2. 迭代：若规则 `lhs ⊆ available` 且 `rhs ∉ available`，则派生 `rhs`，记 `depth = max(depth(lhs)) + 1`。
3. 至不动点终止。

## 三、结果

- 派生轮数 4；触发规则 49 条；可达概念 81/82。
- 不可达概念（需理论外输入或为终端/接口概念）：见 `dynamic_hypergraph.json` → `dynamics.unreachable_concepts`。

## 四、产物

| 文件 | 内容 |
|:---|:---|
| `derivation_trace.csv` | 每步触发的规则、前件、后件、深度 |
| `derivation_order.csv` | 节点派生顺序与深度 |
| `dynamic_hypergraph.json` | 超图 + `derive_depth` 标注 |
