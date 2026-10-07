import PrimeGeometry.Basic
import PrimeGeometry.WindingDensity
import PrimeGeometry.Compton
import PrimeGeometry.Generation
import PrimeGeometry.Spin
import PrimeGeometry.Particle

/-!
# 质数几何密度 (Prime Geometry Density)

本模块形式化 CQM 框架下的**质数几何密度-三代粒子模型**与**康普顿波长猜想**。

## 核心突破

将"时间"本身几何化——弯曲的不是空间，而是再生产固有时（因果时）的数轴。

## 模块结构

| 文件 | 内容 | 核心结论 |
|:-----|:-----|:---------|
| `Basic.lean` | 因果时多边形、因果线段、因果时位置、三角形最小性定理 | n=3 是因果时最小非平凡闭合多边形 |
| `WindingDensity.lean` | 素数缠绕密度、收敛公理、总概率守恒、全局密度 | 活跃素数 {2,3,5} 编码三代结构 |
| `Compton.lean` | 因果环自闭合、康普顿波长猜想、衰变率、质量层级 | P_i ∝ 1/m_i 解释三代稳定性差异 |
| `Generation.lean` | 三代拓扑必然性、与 A₄/SU(5) 衔接 | 3 是拓扑必然，非数值巧合 |
| `Spin.lean` | 因果时定向 Z_2、自旋-1/2 离散起源 | 自旋 = 因果时定向自由度 |
| `Particle.lean` | 费米子/玻色子/真空分类、规范玻色子 | 质数=费米子，合数=玻色子，1=真空 |

## 关键本体论区分

| 概念 | CQM（因果时几何） | GR（时空几何） |
|:-----|:------------------|:---------------|
| 弯曲对象 | 再生产固有时数轴 | 时空流形 g_μν |
| 弯曲原因 | 再生产周期性 | 物质能量-动量 |
| 空间地位 | 次级涌现（退相干产物） | 与时间一起预设 |
| "长度" | 因果步数（再生产次数） | 空间距离（米） |

## 公理/假设清单

| 名称 | 类型 | 文件 | 说明 |
|:-----|:-----|:-----|:-----|
| `windingDensityConvergence` | AXIOM | WindingDensity.lean | 素数缠绕密度收敛为分段常数 |
| `totalProbabilityConservation` | THEOREM | WindingDensity.lean | 总概率守恒 Σ a_i·ρ_i = 1（由密度赋值假设证明） |
| `causalChainSelfClosure` | POSTULATE | Compton.lean | 因果链从母体断裂后自我闭合为因果环 |
| `leptonMassOrdering` | AXIOM | Compton.lean | 三代轻子质量层级 m_e < m_μ < m_τ |

## 与 CQM 其他模块的衔接

```
PrimeGeometry (因果时几何)
    ↓
    ├── CausalSet (因果集基础)
    ├── SpectralGeometry (谱几何 → 活跃素数 {2,3,5})
    ├── CartanAlgebra (A₄ 嘉当矩阵 → 4-单纯形)
    ├── Decoherence (退相干 → 经典空间涌现)
    └── PhysicalConstants (G_N, α⁻¹ 等物理常数)
```

## 参考文献

- ruster (2026). 质数几何密度-三代粒子模型：因果时弯曲与康普顿波长猜想.
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/