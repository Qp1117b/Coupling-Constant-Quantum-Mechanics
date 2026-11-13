import NonMarkovianity.Basic
import NonMarkovianity.Markovization
import NonMarkovianity.ScaleThreshold
import NonMarkovianity.ProperTimeRelaxation

/-!
# 分布式不对易关系与非马尔可夫性 (NonMarkovianity)

对应研究文档 `04 前沿研究/CQM_前沿研究_分布式不对易关系与非马尔可夫性.md`。

## 模块结构

| 模块 | 内容 |
|:---|:---|
| `NonMarkovianity.Basic` | 历史沉淀、单点共时投影、充分性判据；非单射不蕴含不充分的反例 |
| `NonMarkovianity.Markovization` | 单点本体论马尔可夫化与单时刻有界状态类（`LocalAt`） |
| `NonMarkovianity.ScaleThreshold` | 尺度阈值命题：存在最小失效尺度 `ℓ*` |
| `NonMarkovianity.ProperTimeRelaxation` | N1 接口：角亏—固有时流速—弛豫时标 |

## 状态标注

- 定义与定理均不含 `sorry`、`admit`、`native_decide`、`unsafe`、新增 `axiom`；
- N1 的系数来源未确定，属文档 §9【待推】，本库只形式化接口结构与
  由定义直接可得的不等式；
- 阈值 `ℓ*` 的存在性已证，具体值与是否存在有限上界属【待推】T6。
-/
