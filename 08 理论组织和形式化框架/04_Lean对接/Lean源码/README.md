# CQMFormal — 超导发生学的 Lean 4 重建

**作者**：ruster

本目录按“从零重建”只保留新库源文件，现只有一个库：

```
SuperconductivityChain
```

它只承载 `10 探索/CQM_探索_推导链.md` 的 **27 环发生学**，不引用旧 `Superconductivity/`、`FGChain/` 或任何旧定义。

## 编译状态

- Lean 4.29.1（`lean-toolchain` 固定 `v4.29.1`）
- 构建命令：`lake build`
- 目标：零 `sorry`、零 `admit`、零 `native_decide`、零 `unsafe`、零 `axiom`

> 构建通过后，本节的计数以实际 `lake build` 与 `build_lean.py` 抽取为准；不预填“已通过”。
>
> 当前实测（2026-11-21）：`lake build` 全量通过（2902 jobs）；12 模块 / 124 声明 / 60 定理；零 `axiom`、零 `sorry`、零 `admit`、零 `native_decide`、零 `unsafe`。
>
> 覆盖：27/27 环有专用声明且至少一条定理；`r23` 只到 `ZMod` 标签基数，`r27` 到统一阻尼率的符号后果与 RH 显式桥。RH 与 Goldbach 以显式前提接入（`hRH`、`h`），不新增 `axiom`。

## 目录

| 文件 | 内容 |
|:---|:---|
| `SuperconductivityChain.lean` | 库根，汇总导入 |
| `SuperconductivityChain/Basic.lean` | 27 环索引、阶段、状态、缺口性质 |
| `SuperconductivityChain/Gaps.lean` | 62 条链层缺口登记与数量校验 |
| `SuperconductivityChain/Stage1.lean` | 环 1–4：基态方差、声子幅度、Bose 占据数、亏角方差、固有时流速、Regge 刚度结构 |
| `SuperconductivityChain/Stage2.lean` | 环 5–7：`H_ij` 反对称/上闭链、冻结、方差 |
| `SuperconductivityChain/Stage3.lean` | 环 8–10：`C_ij` 反对称、配对势、`λ` |
| `SuperconductivityChain/Stage4.lean` | 环 11–12：配对荷、配对算符骨架、`2/n` 模式权重、`2 ln n` |
| `SuperconductivityChain/Stage5.lean` | 环 13／13.A：域、配对算符的节点质数化实现、`2 ln n` 阶梯谓词与单调性、Goldbach 显式假设供给、2 配对基准概率归一与单点上界、高模式重标度、DFT 四项容器与参考节点 |
| `SuperconductivityChain/Stage6.lean` | 环 14／14.A：相位核与固定平移 |
| `SuperconductivityChain/Stage7.lean` | 环 15–18：渗流/容量/扩大结构、资源饱和终止 |
| `SuperconductivityChain/Stage8.lean` | 环 19–24：危机三条件、全对冻结、锚开关算术核、锚区等速、`Z_n` 相位标签与基数 |
| `SuperconductivityChain/Stage9.lean` | 环 25–27：`I_K` 区间积分骨架、退相干率、相位相干模界、阻尼率统一命题与非负性、RH 显式假设接口与 `DampingReading` 零点实部→统一阻尼桥 |

## 形式化边界

- **只定义**：对象、结构、命题形式（如局域域、配对算符骨架、质数实现、Goldbach 条件、资源约束）。
- **只证明**：代数恒等式、定义层不等式、固定平移关系（如 `H_ij` 上闭链、`C_ij` 反对称、`deficitSpeed` 平方恒等式）。
- **不证明**：BCS 物理同一、相变等效的读数/抽样、Goldbach（按外部假设使用）、DFT 还原、`M9` 数值同一、自守形式函数方程、RH（按外部假设使用）、`T_c` 数值与自由能身份。
- **缺口**：62 条链层缺口全部登记在 `Gaps.lean`；`gaps_length` 只校验“登记完整”，不校验“已解决”。

## 构建与审计

```powershell
Set-Location 'D:\WorkSpace\物理\CQMFormal\08 理论组织和形式化框架\04_Lean对接\Lean源码'
& 'D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe' build

rg -n 'sorry|admit|native_decide|unsafe|axiom' SuperconductivityChain SuperconductivityChain.lean
```

`rg` 命中 `axiom` 必须为零；命中注释中的缺口名不算声明。

## 相关文档

- 推导链：`10 探索/CQM_探索_推导链.md`
- 缺口台账：`08 理论组织和形式化框架/附录/缺口台账.md`
- 目录说明：`SuperconductivityChain/README.md`
