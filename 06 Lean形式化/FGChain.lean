import FGChain.Basic
import FGChain.QuantumOscillation
import FGChain.CurvatureOperator
import FGChain.ReggeBase
import FGChain.FiberBundle
import FGChain.Synchronization
import FGChain.Observable
import FGChain.CartanToShell
import FGChain.CurvatureDerivation
import FGChain.SyncOperator
import FGChain.BundleEOM
import FGChain.Hierarchy

/-!
# CQM FG 链路形式化 (FGChain) — 严格化版

FG 纤维丛理论链路的完整 Lean 4 形式化：从嘉当矩阵与晶胞分布到全局同步
相变的全部环节，以及实验可观测结果的第一性推导。

## 链路环节 ↔ 模块映射

| 环节 | 模块 | 核心内容 |
|:---|:---|:---|
| 链A/链B 两链结构 | `FGChain.Basic` | 几何生成链 ∥ 谱约束链，发生学分离定理 |
| 3–5 | `FGChain.QuantumOscillation` | 晶胞量子振荡、晶胞波函数（声子占据态）、谐振子谱 E_n = ħω(n+1/2) |
| 6–8 | `FGChain.CurvatureOperator` | 曲率算符 δ̂_v、CQM 海森堡对 [û,p̂_u]=i、不确定性通道 |
| 9（前置） | `FGChain.ReggeBase` | 晶胞分布 → Regge 底空间，两链交汇定理 |
| 10–14 | `FGChain.FiberBundle` | 离散主丛、和乐平庸化、结构群涨落、重组实现 F=G⇒R=G⇒Ĥ（子群重组）、表示、物质场 |
| 15–19 | `FGChain.Synchronization` | 同步算符（零点谱经紧化约束进入 𝔠_n=1/4+γ_n²）、本征值交叉（IVT）、CFT 幂律、全局同步=和乐平庸化 |
| 验收 | `FGChain.Observable` | 氢原子能级/巴尔末系、壳层容量/周期长度、跃迁耦级谱、BCS T_c 正性 |

## 严格化模块（新增）

| 模块 | 严格化内容 |
|:---|:---|
| `FGChain.CartanToShell` | A₄ 嘉当矩阵 → SU(5) Dynkin 图深度 → 壳层标签 l_k=k-1 → Casimir C_k=l_k(l_k+1)+3/4 → 壳层容量 2(2l+1)=2,6,10,14 → 周期长度 2,8,18,32 |
| `FGChain.CurvatureDerivation` | 曲率算符严格推导：[X,P]=iħ → 声子代数 → δ̂_v^(1)=Σ(ħω_k/E_bind)|v_k(v)|²(N_k+1/2) → δ̂_v=δ̄_v+δ̂_v^(1) |
| `FGChain.SyncOperator` | 同步算符完整形式 Ŝ_k=(L_u/2π☯)√(1-βδ̂_v)+Ĉ₂(G_k)、约束方程锁定 N_k、耦合常数层级 g_k=α·exp(-(n_k-n_1)/n_1)、Aufbau 顺序 |
| `FGChain.BundleEOM` | U(1) 和乐严格化、伴丛曲率 F=dA+A∧A、运动方程 D*F=*J_Φ、Bianchi 恒等式 DF=0、谱分解 |
| `FGChain.Hierarchy` | 四层 FG（电子→元素→分子→晶胞）、层级嵌套 P_el↪P_mol↪P_cell、谱传递规则 |

## 发生学修正（详见 `FGChain.Basic` 文档头）

1. 底空间构造前置（链A 生成 ∥ 链B 约束）。
2. "拉格朗日量L函数"环节修正为：同步算符 + 零点谱经紧化约束进入 +
   本征值交叉（L 函数是 QG 算术层对象）。
3. "F 充当后主丛结构群"修正为：实现群 R（重组产物）充当有序态空间，
   子群重组 Spec(R), Spec(Ĥ) ⊆ Spec(G)，母群 G 本身不变。
-/