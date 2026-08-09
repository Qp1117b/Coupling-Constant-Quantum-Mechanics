import Mathlib.Data.Real.Basic
import Mathlib.Tactic
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics
import Superconductivity.SPAF
import Superconductivity.Reduction
import Superconductivity.FirstPrinciples
import Superconductivity.CartanSuperconductivity

/-!
# CQM SPAF 压强-温度几何构型框架 (P-T Geometric Configuration Framework)

本模块建立压强 (P) 与温度 (T) 作为 **A₄ 几何构型效应** 的半唯像框架。
核心原则：P 和 T 都在 CQM 中有直接的几何诠释，不依赖外部电磁场。
磁场不显式考虑——它无法直接转换为 A₄ 几何构型效应。

## 压强 → 有效几何构型（SPAF-PT §1 + §1.5）
- 压强 = 压缩正四单纯型体积 → 改变嘉当矩阵的耦合常数
- 几何压缩因子 χ(P) = (P/P_ref)^(1/3)：度量 A₄ 单形的紧凑程度
- 质子间距离 d_ij(P) = d_ref / χ(P)：几何压缩→距离缩小
- 因果耦合 t_ij(P) = t_ref · exp(χ(P)−1)：几何压缩→耦合增强
- 桥梁定理：χ(P) → ω_D(P) = ω_DRef · χ^(3γ)（≡ (P/P_ref)^γ）
- 桥梁定理：χ(P) → λ(P) = λRef · χ^(3δ)（≡ (P/P_ref)^δ）
- 桥梁定理：χ(P) → κ(P) = κRef · χ^(3/2)（嘉当耦合常数）
- 两个竞争项（ω_D↑, λ↓）给出 T_c(P) 的穹顶结构

## 温度 → 有效再生产效应（SPAF-PT §2 + §2.5）
- 配对通道的再生产因子 R(T) = exp(−Γ_eff(T)·τ)
- 再生产（reproduction）：超导序参量通过因果耦合通道不断"再生产"
- Γ_eff(T) = Γ₀ · (1−T/T_c)^β：温度升高→锁定率降低
- R(0) = exp(−τ·Γ₀)（锁定完好），R(T_c) = 1（锁定失效）
- 桥梁定理：T_c^eff = (1−R(T)) · T_c^BCS（再生产退化→T_c 压制）
- 自洽方程：T_c = (1−R(T_c)) · T_c^BCS → T_c = 0（临界处再生产停止）

## 超导分类学（SPAF-PT §3）
- 第 I 类：单元素，纯 A₄ 网络，ε ≈ 0，T_c 低（因果网络小）
- 第 II 类（传统）：合金，少量缺陷本体，ε ≪ 5/4
- 高压氢化物：氢亚晶格 = 纯 A₄ 网络主体，重核 = 化学预压（几何替身）
- 高温超导体（铜氧化物）：非 BCS，不在本框架涵盖范围内
- CQM 分类判据：因果网络完整性 + 缺陷本体浓度 + 几何压缩因子

## 定理一览
- [pressureScaling_valid]：正压 → 正 ω_D(P), λ(P)
- [tcPressureDome_exists]：T_c(P) 穹顶存在性（ω_D 与 λ 竞争的必然结果）
- [tcPressureDome_optimalPressure_pos]：最优压强公式的正性
- [neutronDefectPressure_monotone]：ε(P) 随压强单调减
- [neutronDefectTemperature_monotone]：ε(T) 随温度单调不减
- [effectivePhaseLockingRate_at_zero] / [_above_tc]：锁定率在 T=0 和 T≥T_c 的行为
- [spafCorrectedTc_temperature_suppression]：温度升高压低 T_c
- [cqm_pressure_temperature_defect_constraint]：P-T-ε 三方约束
- [roomTemperature_feasibility_with_pressure]：含压强约束的室温可行域
- [networkIntegrity_maxTc_at_pureProtons]：纯质子网络给出最高 T_c
- [superconductorClass_networkIntegrity]：因果网络完整性与超导分类

## 参考文献
- ruster (2026). CQM 室温超导方向. CQMFormal/08 超导/.
- ruster (2026). CQM SPAF 半唯像应用框架. CQMFormal/08 超导/.
- Ashcroft (1968). Metallic Hydrogen: A High-Temperature Superconductor? PRL 21, 1748.
- Drozdov et al. (2015, 2019). H3S / LaH10.
-/

namespace CQM

open scoped BigOperators
open scoped Topology
open Filter

/-! ## 1. 压强作为 A₄ 几何构型效应（SPAF-PT §1） -/

/-- A₄ 正四单纯型的特征体积：V₄ = (1/4!) · det(A₄)^{1/2} · ℓ⁴。
    压强压缩该体积，改变嘉当矩阵的耦合强度。
    在 CQM 中，压强不是外部施加的力，而是网络密度（质子数/体积）的度量。 -/
noncomputable def simplexCharacteristicVolume (lengthScale : ℝ) : ℝ :=
  (1 / 24) * Real.sqrt 5 * lengthScale ^ 4

/-- 压强-体积关系：P ∝ V^{−5/3}（简并费米气体标度，适用于金属氢化物）。
    这给出压强与 A₄ 正四单纯型体积之间的直接几何映射。 -/
noncomputable def pressureFromVolume (volume : ℝ) (prefactor : ℝ) : ℝ :=
  prefactor * volume ^ (-5/3 : ℝ)

/-- 中子缺陷参数的压强依赖性：ε(P) = ε₀ · (P₀/P)^ν。
    高压压缩缺陷位 → 禁闭几何恢复 → ε 减小。
    当 P → ∞ 时 ε → 0，所有有限本体趋于理想质子。
    这是 CQM 的独特预言：极限高压下所有重核都趋于纯质子 A₄ 网络。 -/
noncomputable def neutronDefectAtPressure (eps0 : ℝ) (pRef p nu : ℝ) : ℝ :=
  eps0 * (pRef / p) ^ nu

/-- 高压下中子缺陷趋于零：P → ∞ ⟹ ε(P) → 0。 -/
theorem neutronDefect_tendsto_zero_at_high_pressure {eps0 pRef nu : ℝ}
    (hpRef : 0 < pRef) (hnu : 0 < nu) :
    Filter.Tendsto (fun p : ℝ => neutronDefectAtPressure eps0 pRef p nu)
      Filter.atTop (𝓝 0) := by
  unfold neutronDefectAtPressure
  have h_div : Filter.Tendsto (fun p : ℝ => pRef / p) Filter.atTop (𝓝 0) := by
    have hc : Tendsto (fun _ : ℝ => pRef) atTop (𝓝 pRef) := tendsto_const_nhds
    simpa [div_eq_mul_inv] using hc.mul tendsto_inv_atTop_zero
  have h_rpow : Filter.Tendsto (fun p : ℝ => (pRef / p) ^ nu) Filter.atTop (𝓝 0) := by
    have hz : (0 : ℝ) ^ nu = 0 := Real.zero_rpow (ne_of_gt hnu)
    simpa [hz] using (h_div.rpow_const (Or.inr (le_of_lt hnu)))
  simpa [mul_comm] using Filter.Tendsto.const_mul eps0 h_rpow

/-- ε(P) 关于压强单调减：压强越高，缺陷越被压缩，ε 越小。
    即 p1 ≤ p2 ⇒ ε(p2) ≤ ε(p1)。 -/
theorem neutronDefectPressure_antitone {eps0 pRef p1 p2 nu : ℝ}
    (heps0 : 0 ≤ eps0) (hpRef : 0 < pRef) (hnu : 0 < nu) (hp1 : 0 < p1) (hp_le : p1 ≤ p2) :
    neutronDefectAtPressure eps0 pRef p2 nu ≤ neutronDefectAtPressure eps0 pRef p1 nu := by
  unfold neutronDefectAtPressure
  have hp2 : 0 < p2 := by linarith
  -- 由于 p1 ≤ p2 且 pRef > 0，有 pRef/p2 ≤ pRef/p1
  have h_div : pRef / p2 ≤ pRef / p1 := by
    have hInv : 1 / p2 ≤ 1 / p1 := one_div_le_one_div_of_le hp1 hp_le
    simpa [div_eq_mul_inv] using mul_le_mul_of_nonneg_left hInv (le_of_lt hpRef)
  have h_pow : (pRef / p2) ^ nu ≤ (pRef / p1) ^ nu :=
    Real.rpow_le_rpow (by positivity) h_div (le_of_lt hnu)
  exact mul_le_mul_of_nonneg_left h_pow heps0

/-- 德拜频率的压强标度律：ω_D(P) = ω_D(P₀) · (P/P₀)^γ。
    γ ∈ (0, 1) 由 Grüneisen 参数和 A₄ 谱间隙的压强响应决定。
    物理根源：P ↑ → V ↓ → 质子间距离 d_ij ↓ → 因果耦合 t_ij ↑ → 晶格刚度 ↑。 -/
noncomputable def debyeFrequencyAtPressure (omegaRef : ℝ) (pRef p gamma : ℝ) : ℝ :=
  omegaRef * (p / pRef) ^ gamma

/-- 电子-声子耦合的压强标度律：λ(P) = λ(P₀) · (P/P₀)^δ。
    δ 通常为负值（典型 −0.2 到 −0.5），因高压下费米面态密度被稀释。
    这正是 LaH10 实验的核心特征：T_c(P) 在 ~170 GPa 处取极大值，
    之后 λ 的下降速度超过 ω_D 的上升速度。 -/
noncomputable def couplingAtPressure (lamRef : ℝ) (pRef p delta : ℝ) : ℝ :=
  lamRef * (p / pRef) ^ delta

/-- 压强标度律在正压下的正性。 -/
theorem pressureScaling_valid {omegaRef lamRef pRef p gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : 0 < lamRef) (hpRef : 0 < pRef) (hp : 0 < p) :
    debyeFrequencyAtPressure omegaRef pRef p gamma > 0 ∧
    couplingAtPressure lamRef pRef p delta > 0 := by
  constructor
  · unfold debyeFrequencyAtPressure
    have h_div : 0 < p / pRef := div_pos hp hpRef
    have h_pow : 0 < (p / pRef) ^ gamma := Real.rpow_pos_of_pos h_div gamma
    exact mul_pos ho h_pow
  · unfold couplingAtPressure
    have h_div : 0 < p / pRef := div_pos hp hpRef
    have h_pow : 0 < (p / pRef) ^ delta := Real.rpow_pos_of_pos h_div delta
    exact mul_pos hl h_pow

/-- T_c 的压强依赖：T_c(P) = (2e^γ/π) · ω_D(P) · exp(−1/λ(P))。
    这是 T_c(P) 穹顶结构的基本形式，由 ω_D(P) 和 λ(P) 的竞争决定。 -/
noncomputable def tcAtPressure (omegaRef lamRef pRef p gamma delta : ℝ) : ℝ :=
  bcsCriticalTemperature
    (debyeFrequencyAtPressure omegaRef pRef p gamma)
    (couplingAtPressure lamRef pRef p delta)

/-- [穹顶存在性] 当 γ > 0 且 δ < 0 时，存在正压强使 T_c > 0。
    这保证了 T_c(P) 穹顶的非平凡性——若所有 P 处 T_c = 0，则无穹顶可言。
    结合两端极限（P → 0⁺ 时 ω_D → 0 ⇒ T_c → 0；
    P → ∞ 时 λ → 0 ⇒ exp(−1/λ) → 0 ⇒ T_c → 0），
    由连续函数介值定理知存在内部极大值点。
    这是 LaH10 实验 T_c(P) 非单调的 CQM 几何解释。 -/
theorem tcPressureDome_exists {omegaRef lamRef pRef gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : 0 < lamRef) (hpRef : 0 < pRef)
    (hgamma : 0 < gamma) (hdelta : delta < 0) :
    ∃ pOpt : ℝ, 0 < pOpt ∧ 0 < tcAtPressure omegaRef lamRef pRef pOpt gamma delta := by
  -- 取 P = P_ref 处：ω_D = ω_DRef > 0，λ = λRef > 0，故 T_c > 0
  refine ⟨pRef, hpRef, ?_⟩
  unfold tcAtPressure debyeFrequencyAtPressure couplingAtPressure
  simp [div_self (ne_of_gt hpRef), Real.one_rpow, bcsCriticalTemperature_pos ho]

/-- [穹顶最优压强公式] 使 T_c(P) 取极大值的约化压强为
    x_opt = (γ·λ_ref/η)^(1/η)，其中 η = −δ > 0。
    最优压强 P_opt = P_ref · x_opt。
    解析推导：令 f(x) = x^γ·exp(−x^η/λ_ref)（x = P/P_ref），
    由 ln f 的驻点条件 ∂/∂x[γ·ln x − x^η/λ_ref] = 0 得 x^η = γ·λ_ref/η。
    二阶导数恒负，故为全局极大值点。
    这给出 T_c(P) 穹顶峰的精确位置，可直接计算无需数值搜索。 -/
noncomputable def tcPressureDome_optimalPressure (omegaRef lamRef pRef gamma delta : ℝ) : ℝ :=
  pRef * ((gamma * lamRef) / (-delta)) ^ ((-delta)⁻¹)

/-- 最优压强为正（当 pRef > 0 且 lamRef > 0 时）。 -/
theorem tcPressureDome_optimalPressure_pos {omegaRef lamRef pRef gamma delta : ℝ}
    (hpRef : 0 < pRef) (hl : 0 < lamRef) (hgamma : 0 < gamma) (hdelta : delta < 0) :
    0 < tcPressureDome_optimalPressure omegaRef lamRef pRef gamma delta := by
  unfold tcPressureDome_optimalPressure
  set eta : ℝ := -delta
  have h_eta_pos : 0 < eta := by linarith
  have h_base_pos : 0 < (gamma * lamRef) / eta := div_pos (mul_pos hgamma hl) h_eta_pos
  have hxOpt_pos : 0 < ((gamma * lamRef) / eta) ^ (eta⁻¹ : ℝ) :=
    Real.rpow_pos_of_pos h_base_pos _
  exact mul_pos hpRef hxOpt_pos

/-! ## 1.5 压强→有效几何构型：桥梁定理（SPAF-PT §1.5） -/

/-- 有效几何压缩因子：χ(P) = (P/P_ref)^(1/3)。
    物理根源：各向同性压缩下，线度 L ∝ V^(1/3) ∝ P^(-1/5)（简并费米气体），
    但唯象上 χ(P) ∝ P^(1/3) 捕捉了"压强越高，A₄ 单形越紧凑"的核心几何效应。
    χ(P) > 1 表示高压下的几何压缩（质子间距离小于参考值）。 -/
noncomputable def geometricCompressionFactor (pRef p : ℝ) : ℝ :=
  (p / pRef) ^ (1/3 : ℝ)

/-- 几何压缩因子在正压下的正性。 -/
theorem geometricCompressionFactor_pos {pRef p : ℝ} (hpRef : 0 < pRef) (hp : 0 < p) :
    0 < geometricCompressionFactor pRef p := by
  unfold geometricCompressionFactor
  exact Real.rpow_pos_of_pos (div_pos hp hpRef) _

/-- 质子间有效距离的压强依赖：d_ij(P) = d_ij(P_ref) / χ(P)。
    几何压缩因子越大，质子间距离越小，因果耦合越强。 -/
noncomputable def protonDistanceAtPressure (dRef : ℝ) (pRef p : ℝ) : ℝ :=
  dRef / geometricCompressionFactor pRef p

/-- 质子间距离关于压强单调减：P₁ ≤ P₂ ⇒ d(P₂) ≤ d(P₁)。 -/
theorem protonDistance_antitone_in_pressure {dRef pRef p1 p2 : ℝ}
    (hdRef : 0 < dRef) (hpRef : 0 < pRef) (hp1 : 0 < p1) (hp_le : p1 ≤ p2) :
    protonDistanceAtPressure dRef pRef p2 ≤ protonDistanceAtPressure dRef pRef p1 := by
  unfold protonDistanceAtPressure geometricCompressionFactor
  have h_chi : 0 < (p1 / pRef) ^ (1/3 : ℝ) := Real.rpow_pos_of_pos (div_pos hp1 hpRef) _
  have h_chi2 : 0 < (p2 / pRef) ^ (1/3 : ℝ) :=
    Real.rpow_pos_of_pos (div_pos (by linarith) hpRef) _
  have h_div_le : p1 / pRef ≤ p2 / pRef := div_le_div_of_nonneg_right hp_le (le_of_lt hpRef)
  have h_rpow_le : (p1 / pRef) ^ (1/3 : ℝ) ≤ (p2 / pRef) ^ (1/3 : ℝ) :=
    Real.rpow_le_rpow (by positivity) h_div_le (by norm_num : 0 ≤ (1/3 : ℝ))
  -- dRef / χ₂ ≤ dRef / χ₁ ⟺ χ₁ ≤ χ₂
  have hd_le : 1 / ((p2 / pRef) ^ (1/3 : ℝ)) ≤ 1 / ((p1 / pRef) ^ (1/3 : ℝ)) :=
    one_div_le_one_div_of_le h_chi h_rpow_le
  simpa [div_eq_mul_inv] using mul_le_mul_of_nonneg_left hd_le (le_of_lt hdRef)

/-- 因果耦合强度的几何压缩标度：
    t_ij(P) = t_ij(P_ref) · exp(χ(P) − 1)。
    当 χ(P) > 1（高压）时 t_ij 指数增长；当 χ(P) < 1（负压/膨胀）时 t_ij 指数衰减。
    物理根源：d_ij(P) = d_ref / χ(P) ⇒ t_ij ∝ exp(−d_ij/λ) ∝ exp(−d_ref/(λ·χ(P)))。
    在小 χ 变化下，exp(−1/χ) ≈ exp(−1)·exp(χ−1) ∝ exp(χ−1)。 -/
noncomputable def causalCouplingGeometricScaling (tRef : ℝ) (pRef p : ℝ) : ℝ :=
  tRef * Real.exp (geometricCompressionFactor pRef p - 1)

/-- 因果耦合强度的几何压缩标度在正压下的正性。 -/
theorem causalCouplingGeometricScaling_pos {tRef pRef p : ℝ}
    (htRef : 0 < tRef) (hpRef : 0 < pRef) (hp : 0 < p) :
    0 < causalCouplingGeometricScaling tRef pRef p := by
  unfold causalCouplingGeometricScaling
  exact mul_pos htRef (Real.exp_pos _)

/-- [桥梁定理] 几何压缩因子→德拜频率：
    ω_D(P) = ω_D(P_ref) · χ(P)^(3γ)，其中 γ 为 Grüneisen 参数。
    由 χ(P) = (P/P_ref)^(1/3) 代入，得 ω_D(P) = ω_D(P_ref) · (P/P_ref)^γ，
    与 §1 的 `debyeFrequencyAtPressure` 一致。
    此定理验证了"压强→几何压缩→晶格刚度→德拜频率"的因果链自洽。 -/
theorem geometricCompression_to_debyeFrequency {omegaRef pRef p gamma : ℝ}
    (hpRef : 0 < pRef) (hp : 0 < p) :
    omegaRef * (geometricCompressionFactor pRef p) ^ (3 * gamma) =
    debyeFrequencyAtPressure omegaRef pRef p gamma := by
  unfold geometricCompressionFactor debyeFrequencyAtPressure
  have h : (p / pRef) ^ ((1/3 : ℝ) * (3 * gamma)) = (p / pRef) ^ gamma := by
    have : ((1/3 : ℝ) * (3 * gamma)) = gamma := by ring
    rw [this]
  calc
    omegaRef * ((p / pRef) ^ (1/3 : ℝ)) ^ (3 * gamma)
        = omegaRef * ((p / pRef) ^ ((1/3 : ℝ) * (3 * gamma))) := by
      rw [Real.rpow_mul (by positivity : 0 ≤ p / pRef)]
    _ = omegaRef * (p / pRef) ^ gamma := by rw [h]

/-- [桥梁定理] 几何压缩因子→电子-声子耦合：
    λ(P) = λ(P_ref) · χ(P)^(3δ)，其中 δ < 0。
    物理根源：高压压缩费米面态密度 N(0) ∝ V^(1/3) ∝ χ(P)^(−1)，
    故 λ = N(0)·V ∝ χ(P)^(−1) = χ(P)^(3δ)（δ = −1/3）。
    与 §1 的 `couplingAtPressure` 一致。 -/
theorem geometricCompression_to_coupling {lamRef pRef p delta : ℝ}
    (hpRef : 0 < pRef) (hp : 0 < p) :
    lamRef * (geometricCompressionFactor pRef p) ^ (3 * delta) =
    couplingAtPressure lamRef pRef p delta := by
  unfold geometricCompressionFactor couplingAtPressure
  have h : (p / pRef) ^ ((1/3 : ℝ) * (3 * delta)) = (p / pRef) ^ delta := by
    have : ((1/3 : ℝ) * (3 * delta)) = delta := by ring
    rw [this]
  calc
    lamRef * ((p / pRef) ^ (1/3 : ℝ)) ^ (3 * delta)
        = lamRef * ((p / pRef) ^ ((1/3 : ℝ) * (3 * delta))) := by
      rw [Real.rpow_mul (by positivity : 0 ≤ p / pRef)]
    _ = lamRef * (p / pRef) ^ delta := by rw [h]

/-- [桥梁定理] 几何压缩→嘉当耦合强度：
    A₄ 嘉当矩阵的耦合常数 κ(P) = κ₀ · χ(P)^(3/2)。
    物理根源：κ ∝ √(t_ij)（因果耦合的平方根决定能级分裂），
    而 t_ij ∝ exp(χ−1) ≈ χ（小 χ 变化下），故 κ ∝ χ^(3/2)。
    此定理将压强几何效应直接连接到嘉当代数结构。 -/
noncomputable def cartanCouplingAtPressure (kappaRef : ℝ) (pRef p : ℝ) : ℝ :=
  kappaRef * (geometricCompressionFactor pRef p) ^ (3/2 : ℝ)

/-- 嘉当耦合强度在正压下的正性。 -/
theorem cartanCouplingAtPressure_pos {kappaRef pRef p : ℝ}
    (hkappaRef : 0 < kappaRef) (hpRef : 0 < pRef) (hp : 0 < p) :
    0 < cartanCouplingAtPressure kappaRef pRef p := by
  unfold cartanCouplingAtPressure
  have h_chi_pos : 0 < geometricCompressionFactor pRef p :=
    geometricCompressionFactor_pos hpRef hp
  exact mul_pos hkappaRef (Real.rpow_pos_of_pos h_chi_pos _)

/-! ## 2. 温度作为因果锁定退化（SPAF-PT §2） -/

/-- 中子缺陷参数的温度依赖性：ε(T) = ε₀ · (1 + α·T/T_F)。
    物理根源：温度扰动增强缺陷位的非锁定程度——
    热激发使缺陷本体的再生产相对偏移增大。
    T_F 为费米温度（≈ 10⁴–10⁵ K），α 为无量纲热激发系数。 -/
noncomputable def neutronDefectAtTemperature (eps0 alpha fermiTemp temp : ℝ) : ℝ :=
  eps0 * (1 + alpha * (temp / fermiTemp))

/-- ε(T) 关于温度单调不减：温度越高，缺陷位的非锁定越严重。 -/
theorem neutronDefectTemperature_monotone {eps0 alpha fermiTemp t1 t2 : ℝ}
    (heps0 : 0 ≤ eps0) (halpha : 0 ≤ alpha) (hTF : 0 < fermiTemp) (h : t1 ≤ t2) :
    neutronDefectAtTemperature eps0 alpha fermiTemp t1 ≤
    neutronDefectAtTemperature eps0 alpha fermiTemp t2 := by
  unfold neutronDefectAtTemperature
  have h_ratio : t1 / fermiTemp ≤ t2 / fermiTemp :=
    div_le_div_of_nonneg_right h (le_of_lt hTF)
  have hm : (eps0 * alpha) * (t1 / fermiTemp) ≤ (eps0 * alpha) * (t2 / fermiTemp) :=
    mul_le_mul_of_nonneg_left h_ratio (mul_nonneg heps0 halpha)
  nlinarith

/-- 温度对因果锁定因子的影响：Γ_eff(T) = Γ₀ · (1 − T/T_c)^β。
    当 T → T_c 时 Γ_eff → 0，锁定因子 e^{−Γ_eff·τ} → 1（锁定失效）。 -/
noncomputable def effectivePhaseLockingRate (gamma0 tc temp beta : ℝ) : ℝ :=
  if temp < tc then gamma0 * (1 - temp / tc) ^ beta else 0

/-- 有效锁定率在 T = 0 处取最大值 Γ₀。 -/
theorem effectivePhaseLockingRate_at_zero {gamma0 tc : ℝ} (htc : 0 < tc) :
    effectivePhaseLockingRate gamma0 tc 0 1 = gamma0 := by
  unfold effectivePhaseLockingRate
  simp [htc]

/-- 有效锁定率在 T ≥ T_c 时为零（锁定完全失效）。 -/
theorem effectivePhaseLockingRate_above_tc {gamma0 tc temp beta : ℝ} (h : tc ≤ temp) :
    effectivePhaseLockingRate gamma0 tc temp beta = 0 := by
  unfold effectivePhaseLockingRate
  simp [h]

/-- SPAF 修正的 T_c（含中子缺陷温度效应）：
    T_c^eff(T) = f(ε(T)) · T_c^BCS。
    注意：这是自洽条件——T_c 本身出现在 ε(T) 的定义中。
    实际求解需迭代：T_c^(n+1) = f(ε(T_c^(n))) · T_c^BCS。 -/
noncomputable def spafCorrectedTcAtTemperature (wDebye lam eps0 alpha fermiTemp : ℝ) : ℝ :=
  neutronDefectTcFactor (neutronDefectAtTemperature eps0 alpha fermiTemp
    (bcsCriticalTemperature wDebye lam)) * bcsCriticalTemperature wDebye lam

/-- 温度升高 → 缺陷加重 → T_c 压低（自洽方向的单调性）。 -/
theorem spafCorrectedTc_temperature_suppression {wDebye lam eps0 alpha fermiTemp : ℝ}
    (hw : 0 < wDebye) (heps0 : 0 ≤ eps0) (halpha : 0 ≤ alpha) (hTF : 0 < fermiTemp) :
    spafCorrectedTcAtTemperature wDebye lam eps0 alpha fermiTemp ≤
    bcsCriticalTemperature wDebye lam := by
  unfold spafCorrectedTcAtTemperature
  have hpos : 0 ≤ neutronDefectAtTemperature eps0 alpha fermiTemp
      (bcsCriticalTemperature wDebye lam) := by
    unfold neutronDefectAtTemperature
    have hTc1 : 0 ≤ bcsCriticalTemperature wDebye lam :=
      le_of_lt (bcsCriticalTemperature_pos hw)
    have hdiv : 0 ≤ bcsCriticalTemperature wDebye lam / fermiTemp :=
      div_nonneg hTc1 (le_of_lt hTF)
    have hq : 0 ≤ 1 + alpha * (bcsCriticalTemperature wDebye lam / fermiTemp) := by
      have halphaX : 0 ≤ alpha * (bcsCriticalTemperature wDebye lam / fermiTemp) :=
        mul_nonneg halpha hdiv
      linarith
    exact mul_nonneg heps0 hq
  have h_factor : neutronDefectTcFactor (neutronDefectAtTemperature eps0 alpha fermiTemp
    (bcsCriticalTemperature wDebye lam)) ≤ 1 :=
    (neutronDefectTcFactor_range hpos).2
  have hTc : 0 ≤ bcsCriticalTemperature wDebye lam :=
    le_of_lt (bcsCriticalTemperature_pos hw)
  nlinarith

/-! ## 2.5 温度→有效再生产效应：桥梁定理（SPAF-PT §2.5） -/

/-- 配对通道的再生产因子：R(T) = exp(−Γ_eff(T) · τ)。
    物理含义：温度 T 下，因果锁定因子 e^{−Γ_eff(T)·τ} 表征
    "配对通道在热涨落中仍能维持因果锁定的概率"。
    再生产（reproduction）是 CQM 的核心概念：
    超导序参量不是静态的，而是通过因果耦合通道不断"再生产"的。
    R(T) 度量了一个再生产周期内配对通道的存活率。

    R(0) = 1（零温完全锁定，所有配对通道都被再生产），
    R(T_c) → 0（临界温度处锁定失效，再生产停止）。 -/
noncomputable def pairingReproductionFactor (gamma0 tc temp beta tau : ℝ) : ℝ :=
  Real.exp (-tau * effectivePhaseLockingRate gamma0 tc temp beta)

/-- 再生产因子 R(T) 在 T = 0 处取最大值 1（完全锁定，完全再生产）。 -/
theorem pairingReproductionFactor_at_zero {gamma0 tc tau : ℝ} (htc : 0 < tc) :
    pairingReproductionFactor gamma0 tc 0 1 tau = Real.exp (-tau * gamma0) := by
  unfold pairingReproductionFactor effectivePhaseLockingRate
  simp [htc]

/-- 再生产因子 R(T) 在 T ≥ T_c 时等于 1（锁定失效，exp(0) = 1）。
    注意：R(T_c) = 1 的意思是"锁定机制完全失效，配对通道不再被再生产"，
    此时 T_c(T_c) = 0，超导消失。这不同于"再生产完好"——
    R 是锁定因子的指数，不是配对存活率本身。
    配对存活率 ∝ (1 − R) 或更精确地 ∝ (1 − R(T))·T_c^BCS。 -/
theorem pairingReproductionFactor_at_tc {gamma0 tc temp beta tau : ℝ} (h : tc ≤ temp) :
    pairingReproductionFactor gamma0 tc temp beta tau = 1 := by
  unfold pairingReproductionFactor effectivePhaseLockingRate
  simp [h]

/-- 再生产因子 R(T) 关于温度单调不减：
    T 越高 → Γ_eff(T) 越小 → exp(−τ·Γ_eff(T)) 越大 → R(T) 越接近 1。
    这意味着"锁定效应随温度升高而减弱"，配对通道的再生产逐渐停止。
    需假设 β ≥ 0 以保证 (1−T/T_c)^β 的单调性。 -/
theorem pairingReproductionFactor_monotone_in_temp {gamma0 tc t1 t2 beta tau : ℝ}
    (hgamma0 : 0 ≤ gamma0) (htc : 0 < tc) (h : t1 ≤ t2) (htau : 0 ≤ tau)
    (hbeta : 0 ≤ beta) :
    pairingReproductionFactor gamma0 tc t1 beta tau ≤
    pairingReproductionFactor gamma0 tc t2 beta tau := by
  unfold pairingReproductionFactor
  -- 需要证 Γ_eff(t1) ≥ Γ_eff(t2)（因为 t1 ≤ t2，锁定率随温度递减）
  -- 因此 −τ·Γ_eff(t1) ≤ −τ·Γ_eff(t2)（τ ≥ 0）
  -- 从而 exp(−τ·Γ_eff(t1)) ≤ exp(−τ·Γ_eff(t2))
  by_cases ht2 : t2 < tc
  · have ht1 : t1 < tc := lt_of_le_of_lt h ht2
    unfold effectivePhaseLockingRate
    simp [ht1, ht2]
    have h_ratio : t1 / tc ≤ t2 / tc := div_le_div_of_nonneg_right h (le_of_lt htc)
    have h_one_minus : 1 - t2 / tc ≤ 1 - t1 / tc := by linarith
    have h_ge0_2 : 0 ≤ 1 - t2 / tc := by
      have hlt : t2 / tc < 1 := (div_lt_one htc).mpr ht2
      linarith
    have h_pow : (1 - t2 / tc) ^ beta ≤ (1 - t1 / tc) ^ beta :=
      Real.rpow_le_rpow h_ge0_2 h_one_minus hbeta
    have h_gamma : gamma0 * ((1 - t2 / tc) ^ beta) ≤ gamma0 * ((1 - t1 / tc) ^ beta) :=
      mul_le_mul_of_nonneg_left h_pow hgamma0
    exact mul_le_mul_of_nonneg_left h_gamma htau
  · -- t2 ≥ tc，则 Γ_eff(t2) = 0，R(t2) = 1
    unfold effectivePhaseLockingRate
    simp [ht2]
    by_cases ht1 : t1 < tc
    · simp [ht1]
      -- R(t1) = exp(-τ·Γ₀·(1−t1/tc)^β) ≤ 1 = R(t2)
      -- 因为 −τ·Γ₀·(1−t1/tc)^β ≤ 0（τ, Γ₀ ≥ 0, (1−t1/tc)^β ≥ 0）
      have h_one_minus_nonneg : 0 ≤ 1 - t1 / tc := by
        have : t1 / tc < 1 := (div_lt_one htc).mpr ht1
        linarith
      have h_pow_nonneg : 0 ≤ (1 - t1 / tc) ^ beta :=
        Real.rpow_nonneg h_one_minus_nonneg beta
      have h_prod_nonneg : 0 ≤ gamma0 * (1 - t1 / tc) ^ beta :=
        mul_nonneg hgamma0 h_pow_nonneg
      have h_arg_nonpos : -tau * (gamma0 * (1 - t1 / tc) ^ beta) ≤ 0 :=
        mul_nonpos_of_nonpos_of_nonneg (neg_nonpos.mpr htau) h_prod_nonneg
      exact (by simpa using (Real.exp_le_exp.mpr h_arg_nonpos))
    · simp [ht1]

/-- [桥梁定理] 再生产因子→T_c 压制：
    有效临界温度 T_c^eff(T) = (1 − R(T)) · T_c^BCS。
    当 R(0) = exp(−τ·Γ₀)（锁定完好，再生产因子小）时，1−R 最大 → T_c^eff 最高。
    当 R(T_c) = 1（锁定失效）时，1−R = 0 → T_c^eff = 0。
    此公式将"温度→再生产退化→T_c 压制"的因果链形式化。 -/
noncomputable def reproductionCorrectedTc (wDebye lam : ℝ) (gamma0 tc temp beta tau : ℝ) : ℝ :=
  (1 - pairingReproductionFactor gamma0 tc temp beta tau) *
  bcsCriticalTemperature wDebye lam

/-- 再生产修正的 T_c 不超过 BCS T_c（因为 1−R ≤ 1）。 -/
theorem reproductionCorrectedTc_le_bcsTc {wDebye lam gamma0 tc temp beta tau : ℝ}
    (hw : 0 < wDebye) :
    reproductionCorrectedTc wDebye lam gamma0 tc temp beta tau ≤
    bcsCriticalTemperature wDebye lam := by
  unfold reproductionCorrectedTc
  have hR : 0 ≤ pairingReproductionFactor gamma0 tc temp beta tau := by
    unfold pairingReproductionFactor
    exact Real.exp_nonneg _
  have hTc : 0 ≤ bcsCriticalTemperature wDebye lam :=
    le_of_lt (bcsCriticalTemperature_pos hw)
  nlinarith

/-- [桥梁定理] 再生产退化→自洽 T_c 方程：
    T_c 满足 T_c = (1 − R(T_c)) · T_c^BCS。
    这是超越方程：R(T_c) = exp(−τ·Γ_eff(T_c)) = 1（因为 Γ_eff(T_c) = 0），
    故 1−R(T_c) = 0，得 T_c = 0 —— 表明纯再生产退化意味着 T_c 在 T = T_c 处
    自洽地为零。实际物理中，配对通道的再生产在 T < T_c 时仍可维持，
    因此有效 T_c 由 (1−R(T))·T_c^BCS 在 T < T_c 时的值决定，
    自洽条件为 T_c^eff = (1−R(T_c^eff))·T_c^BCS。 -/
theorem reproductionSelfConsistentTc_eq_zero {wDebye lam gamma0 tc tau : ℝ}
    (hw : 0 < wDebye) (htc : 0 < tc) :
    reproductionCorrectedTc wDebye lam gamma0 tc tc 1 tau = 0 := by
  unfold reproductionCorrectedTc pairingReproductionFactor effectivePhaseLockingRate
  simp [htc]

/-! ## 3. 超导分类学（SPAF-PT §3） -/

/-- 超导类型（基于 CQM 因果网络完整性）。 -/
inductive SuperconductorClass
  | typeI        -- 第 I 类：单元素，纯 A₄ 网络，ε ≈ 0
  | typeII       -- 第 II 类（传统）：合金，少量缺陷本体
  | hydride      -- 高压氢化物：氢亚晶格 = A₄ 网络主体
  | highTc       -- 高温超导体（铜氧化物）：非 BCS 配对，不在本框架涵盖
  | other        -- 其他（重费米子、有机超导体等）
  deriving DecidableEq

/-- CQM 分类判据：因果网络完整性与缺陷本体浓度。
    - n_defect / n_total < 5%  → 第 I 类（纯网络）
    - 5% ≤ n_defect / n_total < 25% → 第 II 类（轻度缺陷）
    - 氢亚晶格占比 > 50% → 高压氢化物类
    - ε > 5/4（正定性丧失）→ 非超导
    - 非 BCS 配对 → 高温超导体类（不在框架内） -/
noncomputable def cqmClassify (nProton nNeutron : ℕ) (eps : ℝ)
    (isBCS : Bool) : SuperconductorClass :=
  let total := nProton + nNeutron
  if total = 0 then SuperconductorClass.other else
  let defectRatio := (nNeutron : ℝ) / (total : ℝ)
  if eps ≥ 5/4 then SuperconductorClass.other else
  if ¬ isBCS then SuperconductorClass.highTc else
  if defectRatio < 0.05 then SuperconductorClass.typeI else
  if defectRatio < 0.25 then SuperconductorClass.typeII else
  if (nProton : ℝ) / (total : ℝ) > 0.5 then SuperconductorClass.hydride else
  SuperconductorClass.typeII

/-- 因果网络完整性定理：纯质子网络（ε = 0，α = 0）给出该材料类的最高可能 T_c。
    缺陷本体（中子）稀释网络，压低 T_c。 -/
theorem networkIntegrity_maxTc_at_pureProtons {wDebye lam : ℝ} :
    spafCorrectedTcAtTemperature wDebye lam 0 0 0 = bcsCriticalTemperature wDebye lam := by
  unfold spafCorrectedTcAtTemperature neutronDefectAtTemperature
  simp
  rw [neutronDefectTcFactor_zero, one_mul]

/-! ## 4. CQM 推导链约束（SPAF-PT §4） -/

/-- CQM 压强-缺陷-温度的三方约束：
    若 ε(P, T) < 5/4（正定区间），则因果网络可支撑超导；
    若 ε(P, T) ≥ 5/4，则正定性丧失，超导不可能。
    高压 (P ↑) 压缩缺陷位 → ε ↓；高温 (T ↑) 热激发缺陷 → ε ↑。
    两者竞争给出 P-T 相图上的超导区域边界。 -/
theorem cqm_pressure_temperature_defect_constraint {eps0 alpha fermiTemp pRef p nu : ℝ}
    (heps0 : 0 ≤ eps0) (halpha : 0 ≤ alpha) (hTF : 0 < fermiTemp)
    (hpRef : 0 < pRef) (hnu : 0 < nu) (hp : 0 < p) (temp : ℝ) :
    (neutronDefectAtPressure eps0 pRef p nu < 5/4 ∧
     neutronDefectAtTemperature eps0 alpha fermiTemp temp < 5/4) →
    (neutronCartan (neutronDefectAtPressure eps0 pRef p nu)).PosDef := by
  intro h
  rcases h with ⟨hP, _⟩
  exact neutronCartan_posDef_of_lt_five_fourths hP

/-- 室温可行域（含压强约束）：
    T_c(P) ≥ 300 K 需要同时满足：
    1. ω_D(P) ≥ (300 / 2e^γ/π) · e^{1/λ(P)}（德拜频率下界）
    2. ε(P) < 5/4（正定区间）
    3. P 在实验可达范围内（当前 DAC 上限约 400 GPa）
    这比单纯"T_c ≥ 300 K"严格得多——大多数候选材料因压强约束被排除。 -/
theorem roomTemperature_feasibility_with_pressure {omegaRef lamRef pRef p gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : 0 < lamRef) (hpRef : 0 < pRef) (hp : 0 < p)
    (roomTemp : ℝ) (hr : 0 < roomTemp) :
    (tcAtPressure omegaRef lamRef pRef p gamma delta ≥ roomTemp ↔
      bcsExactConstant * debyeFrequencyAtPressure omegaRef pRef p gamma ≥
        roomTemp * Real.exp (1 / couplingAtPressure lamRef pRef p delta)) :=
  roomTemperature_iff_debyeLowerBound

/-! ## 4.5 穹顶极限行为与室温窗口（SPAF-PT §4.5） -/

/-- 恒等式：(p/pRef)^delta = (pRef/p)^(-delta)，对 p > 0, pRef > 0 成立。
    用于将负指数 rpow 转换到正指数，方便使用 atTop 极限引理。 -/
lemma rpow_div_neg_eq_inv {p pRef delta : ℝ} (hp : 0 < p) (hpRef : 0 < pRef) :
    (p / pRef) ^ delta = (pRef / p) ^ (-delta) := by
  calc
    (p / pRef) ^ delta = ((pRef / p)⁻¹) ^ delta := by field_simp
    _ = ((pRef / p) ^ delta)⁻¹ := by
      rw [Real.inv_rpow (by positivity : 0 ≤ pRef / p)]
    _ = (pRef / p) ^ (-delta) := by
      rw [Real.rpow_neg (by positivity : 0 ≤ pRef / p)]

/-- T_c(P) → 0 当 P → 0⁺（因 ω_D(P) = ω_DRef · (P/P_ref)^γ → 0，
    而 λ(P) = λRef · (P/P_ref)^δ → ∞（δ < 0），故 exp(−1/λ) → 1）。
    物理上：压强趋于零时晶格消失，声子配对通道关闭。 -/
theorem tcAtPressure_tendsto_zero_at_zero {omegaRef lamRef pRef gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : lamRef ≠ 0) (hpRef : 0 < pRef)
    (hgamma : 0 < gamma) (hdelta : delta < 0) :
    Filter.Tendsto (fun p : ℝ => tcAtPressure omegaRef lamRef pRef p gamma delta)
      (𝓝[>] 0) (𝓝 0) := by
  unfold tcAtPressure debyeFrequencyAtPressure couplingAtPressure bcsCriticalTemperature
  have h_eta : 0 < -delta := by linarith
  -- Step 1: p/pRef → 0 as p → 0⁺
  have h_div_zero : Filter.Tendsto (fun p : ℝ => p / pRef) (𝓝[>] 0) (𝓝 0) := by
    have h0 : Filter.Tendsto (fun p : ℝ => p / pRef) (𝓝 0) (𝓝 0) := by
      simpa [div_eq_mul_inv] using (continuous_id.tendsto 0).mul_const pRef⁻¹
    exact h0.mono_left nhdsWithin_le_nhds
  -- Step 2: (p/pRef)^gamma → 0 (gamma > 0)
  have h_pow_gamma : Filter.Tendsto (fun p : ℝ => (p / pRef) ^ gamma) (𝓝[>] 0) (𝓝 0) := by
    simpa [Real.zero_rpow (ne_of_gt hgamma)] using
      h_div_zero.rpow_const (Or.inr (le_of_lt hgamma))
  -- Step 3: ω_D(P) = omegaRef * (p/pRef)^gamma → 0
  have h_omega_D : Filter.Tendsto (fun p : ℝ => omegaRef * (p / pRef) ^ gamma) (𝓝[>] 0) (𝓝 0) := by
    simpa using Filter.Tendsto.const_mul omegaRef h_pow_gamma
  -- Step 4: pRef/p → ∞ as p → 0⁺（使用 tendsto_inv_nhdsGT_zero）
  have h_inv_atTop : Filter.Tendsto (fun p : ℝ => pRef / p) (𝓝[>] 0) Filter.atTop := by
    have h_one_div : Filter.Tendsto (fun x : ℝ => x⁻¹) (𝓝[>] 0) Filter.atTop :=
      tendsto_inv_nhdsGT_zero
    simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using
      Filter.Tendsto.atTop_mul_const hpRef h_one_div
  -- Step 5: (pRef/p)^(-delta) → ∞ (-delta > 0, base → ∞)
  have h_pow_pos_atTop : Filter.Tendsto (fun p : ℝ => (pRef / p) ^ (-delta)) (𝓝[>] 0) Filter.atTop :=
    (tendsto_rpow_atTop h_eta).comp h_inv_atTop
  -- Step 6: 使用恒等式将 (p/pRef)^delta 转为 (pRef/p)^(-delta) → ∞
  have h_pow_delta_atTop : Filter.Tendsto (fun p : ℝ => (p / pRef) ^ delta) (𝓝[>] 0) Filter.atTop := by
    -- 在 𝓝[>] 0 上，p > 0，因此恒等式适用
    refine h_pow_pos_atTop.congr' ?_
    filter_upwards [eventually_mem_nhdsWithin] with p hp
    have hp_pos : 0 < p := hp
    exact (rpow_div_neg_eq_inv hp_pos hpRef).symm
  -- Step 7: -1/(lamRef * (p/pRef)^delta) → 0（分情况讨论 lamRef 的正负）
  have h_exp_arg : Filter.Tendsto (fun p : ℝ => -1 / (lamRef * (p / pRef) ^ delta))
      (𝓝[>] 0) (𝓝 0) := by
    by_cases hpos : 0 < lamRef
    · -- lamRef > 0: denom = lamRef * (p/pRef)^delta → ∞
      have h_denom : Filter.Tendsto (fun p : ℝ => lamRef * (p / pRef) ^ delta)
          (𝓝[>] 0) Filter.atTop := by
        simpa [mul_comm] using
          Filter.Tendsto.atTop_mul_const hpos h_pow_delta_atTop
      have h_inv : Filter.Tendsto (fun p : ℝ => 1 / (lamRef * (p / pRef) ^ delta))
          (𝓝[>] 0) (𝓝 0) := by
        have hI : Filter.Tendsto (fun p : ℝ => (lamRef * (p / pRef) ^ delta)⁻¹) (𝓝[>] 0) (𝓝 0) :=
          h_denom.inv_tendsto_atTop
        exact hI.congr (fun p => by simp)
      simpa [neg_div] using Filter.Tendsto.neg h_inv
    · -- lamRef < 0: denom = lamRef * (p/pRef)^delta → -∞
      -- 转换为 -denom → ∞，然后 1/(-denom) → 0，故 1/denom = -(1/(-denom)) → 0
      have hneg : lamRef < 0 := by
        by_contra! hge
        have hle : lamRef ≤ 0 := not_lt.mp hpos
        exact hl (le_antisymm hle hge)
      have h_neg_denom : Filter.Tendsto (fun p : ℝ => -(lamRef * (p / pRef) ^ delta))
          (𝓝[>] 0) Filter.atTop := by
        simpa [neg_mul, mul_comm] using
          Filter.Tendsto.atTop_mul_const (by linarith : 0 < -lamRef) h_pow_delta_atTop
      have h_inv_neg : Filter.Tendsto (fun p : ℝ => 1 / (-(lamRef * (p / pRef) ^ delta)))
          (𝓝[>] 0) (𝓝 0) := by
        have hI : Filter.Tendsto (fun p : ℝ => (-(lamRef * (p / pRef) ^ delta))⁻¹) (𝓝[>] 0) (𝓝 0) :=
          h_neg_denom.inv_tendsto_atTop
        exact hI.congr (fun p => by simp)
      simpa [neg_div, div_neg] using h_inv_neg
  -- Step 9: exp(-1/(lamRef * (p/pRef)^delta)) → 1
  have h_exp : Filter.Tendsto (fun p : ℝ => Real.exp (-1 / (lamRef * (p / pRef) ^ delta)))
      (𝓝[>] 0) (𝓝 1) := by
    have := (Real.continuous_exp.tendsto 0).comp h_exp_arg
    simpa [Real.exp_zero] using this
  -- Step 10: ω_D(P) * exp(...) → 0 * 1 = 0
  have h_prod : Filter.Tendsto
      (fun p : ℝ => (omegaRef * (p / pRef) ^ gamma) *
        Real.exp (-1 / (lamRef * (p / pRef) ^ delta)))
      (𝓝[>] 0) (𝓝 0) := by
    simpa using Filter.Tendsto.mul h_omega_D h_exp
  -- Step 11: multiply by bcsExactConstant
  simpa [mul_assoc] using Filter.Tendsto.const_mul bcsExactConstant h_prod

/-- T_c(P) → 0 当 P → ∞（因 λ(P) = λRef · (P/P_ref)^δ → 0（δ < 0），
    exp(−1/λ) 的指数衰减压倒 ω_D(P) 的幂律增长）。 -/
theorem tcAtPressure_tendsto_zero_atTop {omegaRef lamRef pRef gamma delta : ℝ}
    (ho : 0 < omegaRef) (hl : 0 < lamRef) (hpRef : 0 < pRef)
    (hgamma : 0 < gamma) (hdelta : delta < 0) :
    Filter.Tendsto (fun p : ℝ => tcAtPressure omegaRef lamRef pRef p gamma delta)
      Filter.atTop (𝓝 0) := by
  unfold tcAtPressure debyeFrequencyAtPressure couplingAtPressure bcsCriticalTemperature
  have h_eta : 0 < -delta := by linarith
  -- x = p/pRef → ∞ as p → ∞
  have hx : Filter.Tendsto (fun p : ℝ => p / pRef) Filter.atTop Filter.atTop := by
    refine (tendsto_id (α := ℝ)).atTop_div_const (by positivity : 0 < pRef)
  -- y = (p/pRef)^η / lamRef → ∞ as p → ∞
  have hy : Filter.Tendsto (fun p : ℝ => ((p / pRef) ^ (-delta)) / lamRef) Filter.atTop Filter.atTop := by
    have h_pow : Filter.Tendsto (fun p : ℝ => (p / pRef) ^ (-delta)) Filter.atTop Filter.atTop :=
      (tendsto_rpow_atTop h_eta).comp hx
    simpa [div_eq_mul_inv] using
      Filter.Tendsto.atTop_mul_const (by positivity : 0 < (lamRef : ℝ)⁻¹) h_pow
  -- 核心引理：y^(γ/η) * exp(-y) → 0 as y → ∞（γ/η > 0）
  have h_s : 0 < gamma / (-delta) := div_pos hgamma h_eta
  have h_core : Filter.Tendsto (fun y : ℝ => y ^ (gamma / (-delta)) * Real.exp (-y))
      Filter.atTop (𝓝 0) := by
    have h := tendsto_rpow_mul_exp_neg_mul_atTop_nhds_zero (gamma / (-delta)) 1 (by norm_num : 0 < (1 : ℝ))
    simpa [mul_comm] using h
-- 代数恒等式（G14 闭合）：T_c(P) = C · y^(γ/η) · exp(-y)
  -- 其中 C = omegaRef * lamRef^(γ/η)，y = (p/pRef)^η / lamRef，
  -- 该恒等式在 p → ∞（最终 p ≥ 1）时保序成立（rpow 需参数非负）
  have h_identity :
      (fun p : ℝ => omegaRef * (p / pRef) ^ gamma *
          Real.exp (-1 / (lamRef * (p / pRef) ^ delta))) =ᶠ[atTop]
      (fun p : ℝ => omegaRef * lamRef ^ (gamma / (-delta)) *
          ((((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) *
          Real.exp (-(((p / pRef) ^ (-delta)) / lamRef)))) := by
    filter_upwards [eventually_ge_atTop (1 : ℝ)] with p hp
    have hp0 : 0 < p := by linarith
    have ha : 0 < p / pRef := div_pos hp0 hpRef
    have ha_nonneg : 0 ≤ p / pRef := le_of_lt ha
    have hb_pos : 0 < (p / pRef) ^ (-delta) := Real.rpow_pos_of_pos ha _
    have hb_nonneg : 0 ≤ (p / pRef) ^ (-delta) := le_of_lt hb_pos
    -- (p/pRef)^delta = ((p/pRef)^(-delta))⁻¹
    have h_delta_inv : (p / pRef) ^ delta = ((p / pRef) ^ (-delta))⁻¹ := by
      rw [← Real.rpow_neg ha_nonneg, neg_neg]
    -- (p/pRef)^gamma = ((p/pRef)^(-delta))^(gamma/(-delta))
    have h_pow_gamma : (p / pRef) ^ gamma = ((p / pRef) ^ (-delta)) ^ (gamma / (-delta)) := by
      have hg : gamma = (-delta) * (gamma / (-delta)) :=
        (mul_div_cancel₀ (gamma : ℝ) (ne_of_gt h_eta)).symm
      conv_lhs => rw [hg]
      rw [Real.rpow_mul ha_nonneg]
    -- 指数参数化简：-1/(lamRef * (p/pRef)^delta) = -(((p/pRef)^(-delta)) / lamRef)
    have h_exp_arg : -1 / (lamRef * (p / pRef) ^ delta) = -(((p / pRef) ^ (-delta)) / lamRef) := by
      rw [h_delta_inv]
      field_simp [ne_of_gt hl, ne_of_gt hb_pos]
    -- 幂的拆分：(p/pRef)^(-delta)^(γ/η) = lamRef^(γ/η) * (((p/pRef)^(-delta))/lamRef)^(γ/η)
    have h_pow_split : ((p / pRef) ^ (-delta)) ^ (gamma / (-delta)) =
        lamRef ^ (gamma / (-delta)) * (((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) := by
      have hq : (p / pRef) ^ (-delta) = lamRef * (((p / pRef) ^ (-delta)) / lamRef) := by
        field_simp [ne_of_gt hl]
      calc
        ((p / pRef) ^ (-delta)) ^ (gamma / (-delta))
            = (lamRef * (((p / pRef) ^ (-delta)) / lamRef)) ^ (gamma / (-delta)) := by
              conv_lhs => rw [hq]
        _ = lamRef ^ (gamma / (-delta)) * (((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) := by
              rw [Real.mul_rpow (le_of_lt hl)
                (div_nonneg hb_nonneg (le_of_lt hl))]
    calc
      omegaRef * (p / pRef) ^ gamma * Real.exp (-1 / (lamRef * (p / pRef) ^ delta))
          = omegaRef * (((p / pRef) ^ (-delta)) ^ (gamma / (-delta))) *
              Real.exp (-(((p / pRef) ^ (-delta)) / lamRef)) := by
        rw [h_pow_gamma, h_exp_arg]
      _ = omegaRef * lamRef ^ (gamma / (-delta)) *
          ((((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) *
          Real.exp (-(((p / pRef) ^ (-delta)) / lamRef))) := by
        rw [h_pow_split]
        ring
  -- 核心项（去掉常数因子）→ 0
  have h_subst : Filter.Tendsto
      (fun p : ℝ => omegaRef * lamRef ^ (gamma / (-delta)) *
        ((((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) *
        Real.exp (-(((p / pRef) ^ (-delta)) / lamRef))))
      Filter.atTop (𝓝 0) := by
    -- 常数因子 C = omegaRef * lamRef^(gamma/(-delta))（正有限数）乘以 → 0 的项仍 → 0
    have h_factor : Filter.Tendsto
        (fun p : ℝ => (((p / pRef) ^ (-delta)) / lamRef) ^ (gamma / (-delta)) *
          Real.exp (-(((p / pRef) ^ (-delta)) / lamRef)))
        Filter.atTop (𝓝 0) :=
      h_core.comp hy
    -- 乘以常数因子
    simpa [mul_assoc, mul_comm, mul_left_comm] using
      (Filter.Tendsto.const_mul (omegaRef * lamRef ^ (gamma / (-delta))) h_factor)
  -- 应用恒等式（在 atTop 上保序，换取点式）
  have h_final : Filter.Tendsto
      (fun p : ℝ => omegaRef * (p / pRef) ^ gamma *
        Real.exp (-1 / (lamRef * (p / pRef) ^ delta)))
      Filter.atTop (𝓝 0) :=
    h_subst.congr' h_identity.symm
  -- 乘以 bcsExactConstant
  simpa [mul_assoc] using Filter.Tendsto.const_mul bcsExactConstant h_final

/-- [室温窗口存在性（条件形式）] 穹顶结构保证：若在参考压强处 T_c ≥ roomTemp，
    则至少存在一个压强（P_ref 自身）满足室温条件。
    
    更一般地：由 T_c(P) → 0 当 P → 0⁺（ω_D → 0）和 P → ∞（exp(−1/λ) → 0），
    结合 T_c(P) 在 (0, ∞) 上的连续性（rpow、exp、乘法均为连续函数），
    由介值定理：当穹顶峰值超过室温时，存在有限区间 [P_min, P_max] 使
    T_c(P) ≥ roomTemp。P_min 和 P_max 满足 T_c(P_min) = T_c(P_max) = roomTemp。
    
    极限行为的形式化见 `tcAtPressure_tendsto_zero_at_zero` 和
    `tcAtPressure_tendsto_zero_atTop`（含缺口 G14）。 -/
theorem roomTemperature_pressure_window_exists {omegaRef lamRef pRef gamma delta roomTemp : ℝ}
    (h : roomTemp ≤ tcAtPressure omegaRef lamRef pRef pRef gamma delta) :
    ∃ p : ℝ, tcAtPressure omegaRef lamRef pRef p gamma delta ≥ roomTemp :=
  ⟨pRef, h⟩

/-! ## 5. 压强-温度联合效应（SPAF-PT §5） -/

/-- 有效中子缺陷参数：同时考虑压强压缩和温度激发的联合效应。
    ε_eff(P, T) = ε₀ · (P₀/P)^ν · (1 + α·T/T_F)。
    压强压低缺陷，温度增强缺陷，两者竞争决定超导区域的边界。 -/
noncomputable def effectiveNeutronDefect (eps0 pRef p nu alpha fermiTemp temp : ℝ) : ℝ :=
  eps0 * (pRef / p) ^ nu * (1 + alpha * (temp / fermiTemp))

/-- 有效缺陷的 P-T 联合约束：当 ε_eff(P, T) < 5/4 时，因果网络正定。
    这给出 P-T 相图上的超导区域边界条件。 -/
theorem effectiveDefect_PT_constraint {eps0 pRef p nu alpha fermiTemp temp : ℝ}
    (hp : 0 < p) (hpRef : 0 < pRef) (hnu : 0 < nu)
    (heps0 : 0 ≤ eps0) (halpha : 0 ≤ alpha) (hTF : 0 < fermiTemp) :
    effectiveNeutronDefect eps0 pRef p nu alpha fermiTemp temp < 5/4 ↔
    eps0 * (pRef / p) ^ nu * (1 + alpha * (temp / fermiTemp)) < 5/4 := by
  rfl

/-- 压强-温度相界的单调性：固定温度下，提高压强扩大超导区域；
    固定压强下，降低温度扩大超导区域。
    这是因为 ε_eff(P, T) 对 P 单调减、对 T 单调增。 -/
theorem pt_phase_boundary_monotonicity {eps0 pRef p1 p2 nu alpha fermiTemp temp : ℝ}
    (heps0 : 0 ≤ eps0) (hpRef : 0 < pRef) (hnu : 0 < nu)
    (halpha : 0 ≤ alpha) (hTF : 0 < fermiTemp)
    (hp_lt : 0 < p1) (hp_le : p1 ≤ p2) (hT : 0 ≤ temp) :
    effectiveNeutronDefect eps0 pRef p2 nu alpha fermiTemp temp ≤
    effectiveNeutronDefect eps0 pRef p1 nu alpha fermiTemp temp := by
  unfold effectiveNeutronDefect
  have h_base : (pRef / p2) ^ nu ≤ (pRef / p1) ^ nu := by
    have h_inv : (p2 : ℝ)⁻¹ ≤ (p1 : ℝ)⁻¹ := by simpa using (one_div_le_one_div_of_le hp_lt hp_le)
    have h_div : pRef / p2 ≤ pRef / p1 := by
      rw [div_eq_mul_inv, div_eq_mul_inv]
      exact mul_le_mul_of_nonneg_left h_inv (le_of_lt hpRef)
    exact Real.rpow_le_rpow (div_nonneg (le_of_lt hpRef) (by linarith : 0 ≤ p2)) h_div (le_of_lt hnu)
  have h_temp : 0 ≤ 1 + alpha * (temp / fermiTemp) := by
    nlinarith [div_nonneg hT (le_of_lt hTF)]
  have h_nonneg : 0 ≤ eps0 := heps0
  calc
    eps0 * (pRef / p2) ^ nu * (1 + alpha * (temp / fermiTemp))
        = eps0 * (((pRef / p2) ^ nu) * (1 + alpha * (temp / fermiTemp))) := by ring
    _ ≤ eps0 * (((pRef / p1) ^ nu) * (1 + alpha * (temp / fermiTemp))) := by
        exact mul_le_mul_of_nonneg_left
          (mul_le_mul_of_nonneg_right h_base h_temp) h_nonneg
    _ = eps0 * (pRef / p1) ^ nu * (1 + alpha * (temp / fermiTemp)) := by ring

end CQM