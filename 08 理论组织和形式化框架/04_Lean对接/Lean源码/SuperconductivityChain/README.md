# SuperconductivityChain — 27 环发生学的 Lean 骨架

本目录是**从零重建**的超导理论形式化，只承载《`10 探索/CQM_探索_推导链.md`》的 27 环发生学。
旧 `Superconductivity/`、`FGChain/` 及全部旧 Lean 源文件不在工作树；本库不引用任何旧定义。

## 原则

| 原则 | 落实 |
|:---|:---|
| 不虚构 | 不引入推导链之外的术语、数值、机制 |
| 不绕过 | 不用 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe` |
| 不定义式绕过 | 物理同一、数值、热力学身份不写成 `def`；只登记为缺口 |
| 缺口明确 | 62 条链层缺口在 `Gaps.lean` 全登记，`gaps_length` 校验数量 |
| 精悍 | 每个阶段只保留可定义对象与可证代数命题；不重复既有结论 |

## 模块与环

| 模块 | 环 | 形式化内容 |
|:---|:---|:---|
| `Basic.lean` | 索引 | 27 环索引、阶段、状态、缺口性质 |
| `Gaps.lean` | 全链 | 62 条缺口编号与所属环 |
| `Stage1.lean` | 1–4 | 基态方差、声子幅度、Bose 占据数、亏角方差、固有时流速几何定义、Regge 刚度结构 |
| `Stage2.lean` | 5–7 | `H_ij` 反对称/上闭链、冻结判据、方差非负 |
| `Stage3.lean` | 8–10 | `C_ij` 反对称、配对势负性、`λ` 非负 |
| `Stage4.lean` | 11–12 | 配对荷单位、配对算符骨架、`2/n` 模式权重、`2 ln n` 阶梯 |
| `Stage5.lean` | 13 / 13.A | 局域域、配对算符的节点质数化实现、`2 ln n` 阶梯谓词与单调性、Goldbach 显式假设供给、2 配对基准概率归一与单点上界、高模式数学重标度、DFT 四项容器与参考节点 |
| `Stage6.lean` | 14 / 14.A | 相位核与固定平移 |
| `Stage7.lean` | 15–18 | 渗流/容量/扩大数据结构、资源饱和终止 |
| `Stage8.lean` | 19–24 | 危机三条件、全对冻结、锚开关算术核、锚区等速、`Z_n` 相位标签与基数 |
| `Stage9.lean` | 25–27 | `I_K` 区间积分骨架、退相干率、相位相干模界、阻尼率统一命题与非负性、RH 显式假设接口与 `DampingReading` 零点实部→统一阻尼桥 |
| `../SuperconductivityChain.lean` | 根 | 汇总导入 |

13.A、14.A、25.A、26.B 是环内补充，不另设环号；`Gaps.lean` 的 `ring` 字段仍归其母环。

27/27 环有专用 Lean 声明且至少一条定理；`r23` 只到 `ZMod` 标签基数，`r27` 到统一阻尼率的符号后果与 RH 显式桥。

## 明确不形式化的部分

- BCS 延迟配对的物理同一与同刻度（`审-15`、`临-8`）；
- 相变等效的读数/抽样等效（`临-10`、`临-11`）；
- Goldbach 本身（按外部假设使用）与配对算符→节点质数化的实现次序（`临-26`）；
- DFT 四项分解的均匀极限还原（`链外-D`）；
- 相变锚 `A_τ` 与 `K^SC` 的数值同一（`M9`）；
- 自守形式–`L` 的函数方程与表示论（`G22`）；
- 黎曼猜想与阻尼率统一（`临-22`）；
- `T_c` 数值与自由能身份（`审-11`、`审-14`）。

这些不是“待补的定理”，而是当前没有载体、没有方程或没有证明的缺口；形式化只给条件命题或结构定义。

## 构建

```powershell
Set-Location 'D:\WorkSpace\物理\CQMFormal\08 理论组织和形式化框架\04_Lean对接\Lean源码'
& 'D:\DevTools\.elan\toolchains\leanprover--lean4---v4.29.1\bin\lake.exe' build
```

审计：`rg -n 'sorry|admit|native_decide|unsafe|axiom' SuperconductivityChain SuperconductivityChain.lean`
（`axiom` 命中只允许为零；本库目标为零）。
