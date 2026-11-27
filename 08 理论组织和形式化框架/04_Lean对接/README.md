# 04 · 形式化验证（Lean 对接）

> 维度 3。旧的 55 个 Lean 源文件 / 1003 条声明不在当前工作树；当前只对接从零重建的 `SuperconductivityChain` 单库（12 模块 / 124 声明 / 60 定理）。

| 文件 | 内容 |
|:---|:---|
| `lean代码路径.yaml` | 项目路径、Lean v4.29.1、单库模块清单、声明直方图（`build_lean.py` 生成） |
| `Lean结构提取/declarations.csv` / `.json` | 新库全部声明（数量以实际抽取为准） |
| `Lean结构提取/模块清单.csv` | 逐模块声明计数 |
| `Lean结构提取/导入依赖.csv` / `.dot` | 模块导入依赖图 |
| `Lean↔概念映射.csv` | 只映射新库真实符号；旧映射无值 |
| `蓝图/蓝图.md` | 阶段—概念—缺口对照 + 缺口登记 + 声明统计 |
| `蓝图/index.html` | 交互式蓝图网页（离线自包含） |

**权威状态**：以 `04_Lean对接/Lean源码/README.md` 为准。本目录只做自动抽取，不把旧库的“已闭合”结论带入新库。

覆盖：27/27 环有专用 Lean 声明，且 27/27 至少一条定理；`r23` 只到 `ZMod` 标签基数，`r27` 到统一阻尼率的符号后果与 RH 显式桥，二者都不升级为物理结论。RH 与 Goldbach 以显式前提接入（`hRH : RiemannHypothesis`、`h : Goldbach`），不新增 `axiom`。

构建：`_build/build_lean.py`。
