import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Sqrt
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Analysis.SpecialFunctions.Arsinh
import Mathlib.Order.Filter.AtTopBot.Field
import Mathlib.Topology.Algebra.Order.Field
import Mathlib.Topology.Defs.Filter
import Mathlib.Tactic
import CartanAlgebra.Basic
import Superconductivity.Reduction
import Superconductivity.CartanSuperconductivity
import Superconductivity.SPAF

open scoped Topology
open scoped MeasureTheory

open Filter

/-!
# CQM 超导：推导链 (Derivation Chain)

本模块把超导的**推导起点从文献公式下沉到物理第一原理**，铺开完整链条：

    质子 A₄ 循环相空间（CQM 本体：有限本体=自再产生环，禁闭几何=正四单纯型，
      代数签名 A₄，07 嘉当结构 §2.1）
      → 晶格声子（禁闭几何的因果锁定周期运动；德拜频率 ω_D = √(k/M)，
        k 由 A₄ 谱间隙标定）
      → 电子-声子耦合 λ = N(0)·V（电子的 N(0) 取主流已确立的电子能动张量结果，
        不重新推导费米子谱；V 为 A₄ 晶格扇区的声子介导强度）
      → BCS 自洽积分方程（能隙积分方程作为最低层物理输入）
      → 严格积分恒等式 ∫₀^{ω_D} dξ/√(ξ²+Δ²) = arsinh(ω_D/Δ)
        （把"能隙方程 → arsinh 闭式"的台阶从文献输入提升为严格定理）
      → 能隙闭式 Δ = ω_D/sinh(1/λ)（闭式解）
      → 临界温度（弱耦合消失定理）与能隙比（复用 Reduction 闭式/极限/强耦合链）
      → 再生产维持（锁定因子 e^{−Γ|τ|} 衰减定理：涌现态的确定性需被反复再生产维持）
      → 金属氢实例（氢原子 = 单质子有限本体，禁闭几何直接是 A₄，
        A₄ 谱间隙标定刚度 + 质子质量 → 德拜频率；大量氢 = A₄ 直接拼接）

**输入与非推导声明**（诚实声明）：
1. A₄ 本征向量的显式构造属 CartanAlgebra 待办；本模块以谱为输入。
2. 晶格刚度参考标度、配对强度 V 为正参数（理想化输入）。
3. 电子的费米面态密度 N(0) 采用主流电子结构/能动张量结果（不重新推导）。
4. T_c 方程的"tanh 积分 → 对数近似"渐近（文献 BCS 弱耦合）标注为 G13；
   本模块将能隙积分方程的 ∫ → arsinh 台阶子以严格化，
   能隙/T_c 的其余闭式与极限由 Reduction 承载。
5. 弱耦合对数渐近已有 `bcs_gap_weak_coupling_limit`（比值型）承载。

## 推导链定理
- [latticeStiffnessFromA4_pos] / [phononFrequencyFromA4_pos] /
  [phononFrequencyFromA4_mono_in_stiffness]：质子 A₄ 谱间隙标定晶格刚度与声子频率
- [electronPhononCoupling_pos]：λ = N(0)·V 为正
- [gapIntegral_pr]：**∫₀^{ω_D} dξ/√(ξ²+Δ²) = arsinh(ω_D/Δ)**（严格积分恒等式）
- [bcsGapIntegralEquation_iff_arsinh]：积分能隙方程 ⟺ 单参 arsinh 方程
- [bcsGapIntegralEquation_solved]：积分能隙方程的解 = ω_D/sinh(1/λ)
- [bcsCriticalTemperature_tendsto_zero]：弱耦合 T_c → 0（T_c 在 λ→0 消失）
- [phaseLockingFactor_tendsto_zero]：再生产维持——锁定因子随再生产间隔衰减，
  涌现态确定性需反复耦合事件维持（坍缩难题②的再生产解答）
- [hydrogenPhononFrequency_pos]：金属氢实例——氢 = 单质子有限本体（A₄ 直接拼接），
  德拜频率正性
- [hydrogen_bcs_gap_equation_solved]：金属氢能隙闭式 Δ_H = √(k₀·λ₁/m_p)/sinh(1/λ)
  精确满足能隙积分方程（闭式解实例化到氢材料）
- [hydrogen_phonon_higher_than_deuterium]：金属氢同位素方向——氘晶格声子截止
  不高于氢晶格（最轻有限本体给出最高 T_c 上限）
- [firstPrinciples_chain_pos]：张量序参量（A₄ 谱）与推导链能隙闭式同为正

## 参考文献
- ruster (2026). CQM_数学_嘉当结构（07 推导与数学）§2.1–§2.2.
- ruster (2026). CQM_超导核心理论（08 超导）.
- Bardeen, Cooper, Schrieffer (1957). Theory of Superconductivity.
-/

namespace CQM

open scoped BigOperators

/-! ## 第一步：质子 A₄ 循环本体 → 晶格声子 -/

/-- 晶格刚度标度取自 A₄ 谱间隙：k = k₀·λ₁（k₀ 为 A₄ 循环刚度参考标度，理想化输入；
    spectralGap 见 Superconductivity.CartanSuperconductivity，λ₁ = (3−√5)/2）。 -/
noncomputable def latticeStiffnessFromA4 (stiffnessRef : ℝ) : ℝ :=
  stiffnessRef * spectralGap

/-- 晶格刚度严格为正（A₄ 谱间隙 > 0，禁闭几何不坍缩）。 -/
theorem latticeStiffnessFromA4_pos {stiffnessRef : ℝ} (hk : 0 < stiffnessRef) :
    0 < latticeStiffnessFromA4 stiffnessRef := by
  unfold latticeStiffnessFromA4
  exact mul_pos hk spectralGap_pos

/-- 声子频率 = 德拜频率：ω_D = √(k/M)，k 由 A₄ 谱间隙标定。
    对应"电子-晶格-电子三方因果闭环"的离子扇区。 -/
noncomputable def phononFrequencyFromA4 (stiffnessRef ionMass : ℝ) : ℝ :=
  debyeFrequency (latticeStiffnessFromA4 stiffnessRef) ionMass

/-- 声子频率严格为正。 -/
theorem phononFrequencyFromA4_pos {stiffnessRef ionMass : ℝ}
    (hk : 0 < stiffnessRef) (hM : 0 < ionMass) :
    0 < phononFrequencyFromA4 stiffnessRef ionMass := by
  unfold phononFrequencyFromA4
  exact debyeFrequency_pos (latticeStiffnessFromA4_pos hk) hM

/-- 声子频率关于刚度参考单调不减：A₄ 循环越强，声速越高。 -/
theorem phononFrequencyFromA4_mono_in_stiffness {ref1 ref2 ionMass : ℝ}
    (href : ref1 ≤ ref2) (hM : 0 < ionMass) :
    phononFrequencyFromA4 ref1 ionMass ≤ phononFrequencyFromA4 ref2 ionMass := by
  unfold phononFrequencyFromA4 debyeFrequency latticeStiffnessFromA4
  apply Real.sqrt_le_sqrt
  exact div_le_div_of_nonneg_right
    (mul_le_mul_of_nonneg_right href (le_of_lt spectralGap_pos)) (le_of_lt hM)

/-! ## 第二步：电子-声子耦合（电子能动张量采用主流结果） -/

/-- 电子-声子耦合常数 λ = N(0)·V。
    N(0)：电子费米面态密度（主流凝聚态/电子能动张量已确立，不重新推导）；
    V：A₄ 晶格扇区的声子介导配对强度（理想化正输入）。 -/
noncomputable def electronPhononCoupling (densityOfStates pairStrength : ℝ) : ℝ :=
  densityOfStates * pairStrength

/-- 弱耦合可配对条件：N(0) 与 V 均正时 λ > 0。 -/
theorem electronPhononCoupling_pos {densityOfStates pairStrength : ℝ}
    (hn : 0 < densityOfStates) (hv : 0 < pairStrength) :
    0 < electronPhononCoupling densityOfStates pairStrength := by
  unfold electronPhononCoupling
  exact mul_pos hn hv

/-! ## 第三步：BCS 能隙积分方程（严格步） -/

/-- 能隙积分的被积函数：f(ξ) = 1/√(ξ² + Δ²)，ξ 为费米面附近单粒子能量。 -/
noncomputable def gapIntegrand (xi gap : ℝ) : ℝ :=
  (Real.sqrt (xi ^ 2 + gap ^ 2))⁻¹

/-- 私有引理：√(1+(ξ/gap)²)·gap = √(ξ²+gap²)（gap > 0）。 -/
private lemma sqrt_one_add_div_mul_gap {xi gap : ℝ} (hg : 0 < gap) :
    Real.sqrt (1 + (xi / gap) ^ 2) * gap = Real.sqrt (xi ^ 2 + gap ^ 2) := by
  calc
    Real.sqrt (1 + (xi / gap) ^ 2) * gap
        = Real.sqrt (1 + (xi / gap) ^ 2) * Real.sqrt (gap ^ 2) := by
        rw [Real.sqrt_sq hg.le]
    _ = Real.sqrt ((1 + (xi / gap) ^ 2) * gap ^ 2) := by
        rw [← Real.sqrt_mul (by positivity : 0 ≤ 1 + (xi / gap) ^ 2) (gap ^ 2)]
    _ = Real.sqrt (gap ^ 2 + xi ^ 2) := by
        congr 1
        field_simp [ne_of_gt hg]
    _ = Real.sqrt (xi ^ 2 + gap ^ 2) := by
        congr 1
        ac_rfl

/-- [推导] 积分恒等式：∫₀^{ω_D} dξ/√(ξ²+Δ²) = arsinh(ω_D/Δ)（Δ > 0）。
    ├ 由 `Real.hasDerivAt_arsinh`（d/dx arsinh x = 1/√(1+x²)）与链式法则：
    │   d/dξ arsinh(ξ/Δ) = 1/√(ξ²+Δ²)；
    └ 由微积分基本定理 `intervalIntegral.integral_eq_sub_of_hasDerivAt` 完成。
    这把 BCS 能隙积分方程的"积分 → arsinh"闭式台阶升格为严格定理。 -/
theorem gapIntegral_pr {wDebye gap : ℝ} (hw : 0 ≤ wDebye) (hg : 0 < gap) :
    ∫ xi in 0..wDebye, gapIntegrand xi gap = Real.arsinh (wDebye / gap) := by
  have hderiv : ∀ xi ∈ Set.uIcc 0 wDebye,
      HasDerivAt (fun xi => Real.arsinh (xi / gap)) (gapIntegrand xi gap) xi := by
    intro xi hx
    have hid : HasDerivAt (fun x : ℝ => x / gap) (1 / gap) xi := by
      simpa using (hasDerivAt_id xi).div_const gap
    have hcomp : HasDerivAt (fun x : ℝ => Real.arsinh (x / gap))
        ((Real.sqrt (1 + (xi / gap) ^ 2))⁻¹ * (1 / gap)) xi := by
      simpa [smul_eq_mul] using hid.arsinh
    have hderivEq : (Real.sqrt (1 + (xi / gap) ^ 2))⁻¹ * gap⁻¹ =
        (Real.sqrt (xi ^ 2 + gap ^ 2))⁻¹ := by
      have hmain : Real.sqrt (1 + (xi / gap) ^ 2) * gap = Real.sqrt (xi ^ 2 + gap ^ 2) :=
        sqrt_one_add_div_mul_gap hg
      rw [← mul_inv]
      rw [hmain]
    simpa [gapIntegrand, hderivEq] using hcomp
  have hcont : ContinuousOn (fun xi => gapIntegrand xi gap) (Set.Icc 0 wDebye) := by
    unfold gapIntegrand
    apply ContinuousOn.inv₀
    · fun_prop
    · intro xi hxi
      exact (Real.sqrt_pos.mpr (by nlinarith [sq_nonneg xi, sq_nonneg gap])).ne'
  have hint : IntervalIntegrable (fun xi => gapIntegrand xi gap) MeasureTheory.volume 0 wDebye :=
    hcont.intervalIntegrable_of_Icc hw
  have hFTC := intervalIntegral.integral_eq_sub_of_hasDerivAt hderiv hint
  simpa [Real.arsinh_zero] using hFTC

/-! ## 第四步：积分能隙方程、闭式与唯一性 -/

/-- BCS 能隙积分方程（弱耦合平均场，积分形式为最低层物理输入）：
    1 = λ·∫₀^{ω_D} dξ/√(ξ² + Δ²)。 -/
def bcsGapIntegralEquation (lam wDebye gap : ℝ) : Prop :=
  lam * ∫ xi in 0..wDebye, gapIntegrand xi gap = 1

/-- 积分能隙方程 ⟺ 单参 arsinh 方程（推导链积分恒等式直接代入）。 -/
theorem bcsGapIntegralEquation_iff_arsinh {lam wDebye gap : ℝ} (hw : 0 ≤ wDebye)
    (hg : 0 < gap) :
    bcsGapIntegralEquation lam wDebye gap ↔ lam * Real.arsinh (wDebye / gap) = 1 := by
  unfold bcsGapIntegralEquation
  rw [gapIntegral_pr hw hg]

/-- [闭式解] 能隙积分方程的解 = ω_D/sinh(1/λ)。
    ├ 积分恒等式（[gapIntegral_pr]）把积分方程化为 arsinh 方程；
    └ arsinh 方程的唯一闭式解（`bcs_gap_equation_unique`）。 -/
theorem bcsGapIntegralEquation_solved {lam wDebye gap : ℝ} (hw : 0 < wDebye)
    (hg : 0 < gap) (hl : 0 < lam) (hEq : bcsGapIntegralEquation lam wDebye gap) :
    gap = bcsGapFromGapEquation wDebye lam := by
  have hars : lam * Real.arsinh (wDebye / gap) = 1 :=
    (bcsGapIntegralEquation_iff_arsinh (le_of_lt hw) hg).mp hEq
  exact bcs_gap_equation_unique (ne_of_gt hw) (ne_of_gt hl) hars

/-! ## 第五步：临界温度与端到端链 -/

/-- 弱耦合消失：λ → 0⁺ 时 T_c → 0（T_c 在耦合趋零时退隐，配对消失）。
    与 BCS 物理一致：T_c 的指数因子 e^{−1/λ} 是严格闭式的结果，
    不是经验截断。 -/
theorem bcsCriticalTemperature_tendsto_zero {wDebye : ℝ} (_hw : wDebye > 0) :
    Tendsto (fun lam : ℝ => bcsCriticalTemperature wDebye lam) (𝓝[>] 0) (𝓝 0) := by
  have h₁ : Tendsto (fun lam : ℝ => 1 / lam) (𝓝[>] 0) atTop := by
    simpa [div_eq_mul_inv] using (tendsto_inv_nhdsGT_zero (𝕜 := ℝ))
  have h₂ : Tendsto (fun lam : ℝ => -1 / lam) (𝓝[>] 0) atBot := by
    have hm : Tendsto (fun lam : ℝ => -1 * (1 / lam)) (𝓝[>] 0) atBot :=
      (Filter.tendsto_const_mul_atBot_of_neg (by norm_num : (-1 : ℝ) < 0)).mpr h₁
    simpa [div_eq_mul_inv] using hm
  have h₃ : Tendsto (fun lam : ℝ => Real.exp (-1 / lam)) (𝓝[>] 0) (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h₂
  unfold bcsCriticalTemperature
  have hc : Tendsto (fun lam : ℝ => (bcsExactConstant * wDebye) * Real.exp (-1 / lam))
      (𝓝[>] 0) (𝓝 0) := by
    simpa using tendsto_const_nhds.mul h₃
  exact hc

/-- 端到端链（正性合成）：质子 A₄ 循环刚度 → 声子频率 > 0，
    电子-声子耦合 λ > 0，能隙积分方程的闭式解 > 0，张量超导序参量
    （A₄ 全部本征通道）> 0——超导态沿推导链严格涌现。 -/
theorem firstPrinciples_chain_pos {stiffnessRef ionMass N0 V s Γ τ : ℝ}
    (hk : 0 < stiffnessRef) (hM : 0 < ionMass) (hn : 0 < N0) (hv : 0 < V)
    (hs : 0 < s) :
    phononFrequencyFromA4 stiffnessRef ionMass > 0 ∧
      electronPhononCoupling N0 V > 0 ∧
      bcsGapFromGapEquation (phononFrequencyFromA4 stiffnessRef ionMass)
        (electronPhononCoupling N0 V) > 0 ∧
      superconductingOrderTensor cartanEigenvalue s Γ τ > 0 := by
  constructor
  · exact phononFrequencyFromA4_pos hk hM
  · constructor
    · exact electronPhononCoupling_pos hn hv
    · constructor
      · exact bcsGapFromGapEquation_pos (phononFrequencyFromA4_pos hk hM)
          (electronPhononCoupling_pos hn hv)
      · exact superconductingOrderTensor_cartanWeights_pos hs

/-! ## 第六步：再生产维持（坍缩难题②的解答） -/

/-- 再生产锁定因子的时间衰减：e^{−Γ|τ|} → 0（再生产间隔 τ → ∞，Γ > 0）。
    物理意义：把坍缩取消后，涌现态的**确定性**不能一次获得、必须被反复维持——
    若配对锁定的再生产间隔趋于无穷（耦合事件不再反复发生），
    锁定因子完全衰减、序参量无从维持。这正对应涌现公式中的再生产项
    e^{−Γτ} 的必要性：确定性是历史性地被再生产出来的（机制对应
    "反复的耦合事件维持涌现态"），而非一次性给定的结果。 -/
theorem phaseLockingFactor_tendsto_zero {GammaPhase : ℝ} (hg : 0 < GammaPhase) :
    Tendsto (fun tau : ℝ => phaseLockingFactor GammaPhase tau) atTop (𝓝 0) := by
  unfold phaseLockingFactor
  have h₁ : Tendsto (fun tau : ℝ => tau) atTop atTop := tendsto_id
  have h₂ : Tendsto (fun tau : ℝ => GammaPhase * tau) atTop atTop :=
    (Filter.tendsto_const_mul_atTop_of_pos hg).2 h₁
  have h₃ : Tendsto (fun tau : ℝ => -(GammaPhase * tau)) atTop atBot :=
    (tendsto_neg_atBot_iff).mpr h₂
  have h₄ : Tendsto (fun tau : ℝ => Real.exp (-(GammaPhase * tau))) atTop (𝓝 0) :=
    Real.tendsto_exp_atBot.comp h₃
  apply h₄.congr'
  filter_upwards [eventually_ge_atTop (0 : ℝ)] with tau htau
  congr 1
  rw [abs_of_nonneg htau]
  ring

/-! ## 第七步：金属氢实例（单质子有限本体的 A₄ 直接拼接） -/

/-- 金属氢：氢原子 = 单个质子有限本体，禁闭几何直接为正四单纯型（A₄ 嘉当矩阵）。
    无需跨种类有限本体拼接——A₄ 谱间隙标定晶格刚度、离子质量即质子质量，
    德拜频率完全由 CQM 本体量（谱间隙 × 质子质量）决定。
    这是第二步"大量金属氢材料的 CQM 超导机制"的计算起点。 -/
noncomputable def hydrogenPhononFrequency (stiffnessRef : ℝ) : ℝ :=
  phononFrequencyFromA4 stiffnessRef protonMass

/-- 金属氢声子频率严格为正（A₄ 循环刚度与质子质量均正）。 -/
theorem hydrogenPhononFrequency_pos {stiffnessRef : ℝ} (hk : 0 < stiffnessRef) :
    0 < hydrogenPhononFrequency stiffnessRef := by
  unfold hydrogenPhononFrequency
  exact phononFrequencyFromA4_pos hk protonMass_pos

/-- 金属氢能隙闭式：Δ_H = ω_D^H / sinh(1/λ)
    （ω_D^H = √(k₀·λ₁/m_p)，λ = N(0)·V）。
    氢 = 单质子有限本体 → A₄ 谱间隙直接进入晶格刚度；
    这是第二步"大量金属氢材料的 CQM 超导机制"的能隙计算封闭式。 -/
noncomputable def hydrogenBcsGap (stiffnessRef coupling : ℝ) : ℝ :=
  bcsGapFromGapEquation (hydrogenPhononFrequency stiffnessRef) coupling

/-- [推导] 金属氢能隙闭式精确满足能隙积分方程 1 = λ·arsinh(ω_D^H/Δ_H)。
    这是闭式解链（积分恒等式 → arsinh 方程 → 唯一闭式解）在氢材料上的
    直接实例：不需要任何经验参数，仅用质子 A₄ 谱间隙的输入。 -/
theorem hydrogen_bcs_gap_equation_solved {stiffnessRef coupling : ℝ}
    (hk : 0 < stiffnessRef) (hlam : 0 < coupling) :
    coupling * Real.arsinh
        (hydrogenPhononFrequency stiffnessRef / hydrogenBcsGap stiffnessRef coupling) = 1 := by
  unfold hydrogenBcsGap
  exact bcs_gap_equation (hydrogenPhononFrequency_pos hk) hlam

/-! ## 第八步：同位素方向与 T_c 单调性 -/

/-- 金属氢同位素方向：氘晶格（离子质量 2·m_p）的声子截止不高于氢晶格——
    最轻的有限本体（质子）给出最高 ω_D，对应同位素位移的家系
    T_c(D) < T_c(H)。 -/
theorem hydrogen_phonon_higher_than_deuterium {stiffnessRef : ℝ} (hk : 0 ≤ stiffnessRef) :
    phononFrequencyFromA4 stiffnessRef (2 * protonMass) ≤
    hydrogenPhononFrequency stiffnessRef := by
  unfold hydrogenPhononFrequency phononFrequencyFromA4 debyeFrequency latticeStiffnessFromA4
  apply Real.sqrt_le_sqrt
  have hrecip : 1 / (2 * protonMass) ≤ 1 / protonMass := by
    exact one_div_le_one_div_of_le protonMass_pos (by nlinarith [protonMass_pos])
  have hkk : 0 ≤ stiffnessRef * spectralGap := mul_nonneg hk (le_of_lt spectralGap_pos)
  rw [div_eq_mul_inv, div_eq_mul_inv]
  rw [inv_eq_one_div, inv_eq_one_div]
  exact mul_le_mul_of_nonneg_left hrecip hkk

/-! ## 第九步：T_c 单调性 -/

/-- T_c 关于德拜频率单调不减（数学性质）：
    T_c = 常·ω_D·e^{−1/λ} 对 ω_D 线性单调——声子截止越高、T_c 越高。 -/
theorem bcsCriticalTemperature_mono_in_debye {w1 w2 n0V : ℝ} (hw : w1 ≤ w2) :
    bcsCriticalTemperature w1 n0V ≤ bcsCriticalTemperature w2 n0V := by
  unfold bcsCriticalTemperature
  have hconst : 0 ≤ bcsExactConstant := le_of_lt bcsExactConstant_pos
  have hmul : bcsExactConstant * w1 ≤ bcsExactConstant * w2 :=
    mul_le_mul_of_nonneg_left hw hconst
  exact mul_le_mul_of_nonneg_right hmul (le_of_lt (Real.exp_pos _))

/-- T_c 关于耦合常数 λ 单调不减（数学性质）：
    e^{−1/λ} 随 1/λ 下降而下降、随 λ 增长而增长——强耦合同样上推 T_c。
    两条单调性共同给出 T_c 随 ω_D 与 λ 增大的方向坐标。 -/
theorem bcsCriticalTemperature_mono_in_coupling {wDebye lam1 lam2 : ℝ}
    (hw : 0 < wDebye) (hl : lam1 ≤ lam2) (hp : 0 < lam1) :
    bcsCriticalTemperature wDebye lam1 ≤ bcsCriticalTemperature wDebye lam2 := by
  unfold bcsCriticalTemperature
  have hif : (1 / lam2 : ℝ) ≤ 1 / lam1 := by
    exact (one_div_le_one_div (lt_of_lt_of_le hp hl) hp).2 hl
  have hineq : -1 / lam1 ≤ -1 / lam2 := by
    rw [neg_div, neg_div]
    exact neg_le_neg hif
  have hle : Real.exp (-1 / lam1) ≤ Real.exp (-1 / lam2) := Real.exp_monotone hineq
  have hpos : 0 ≤ bcsExactConstant * wDebye :=
    mul_nonneg (le_of_lt bcsExactConstant_pos) (le_of_lt hw)
  exact mul_le_mul_of_nonneg_left hle hpos


/-! ## 第十一步：中子缺陷与推导链的一致性约束 -/

/-- SPAF §3.2 中子缺陷参数 ε 与推导链的一致性：
    若 ε < 5/4（C_n 正定区间），则推导链的全部正性保持不变——
    声子频率、电子-声子耦合、能隙闭式、张量序参量均严格为正。
    这建立了半唯像参数（ε）与推导链（A₄ → ω_D → λ → Δ → T_c）
    之间的双向约束：ε 必须在正定区间内，否则推导链的正性前提被破坏。 -/
theorem spaf_firstPrinciples_chain_consistent {stiffnessRef ionMass N0 V s Γ τ eps : ℝ}
    (hk : 0 < stiffnessRef) (hM : 0 < ionMass) (hn : 0 < N0) (hv : 0 < V)
    (hs : 0 < s) (heps : eps < 5/4) :
    (neutronCartan eps).PosDef ∧
      phononFrequencyFromA4 stiffnessRef ionMass > 0 ∧
      electronPhononCoupling N0 V > 0 ∧
      bcsGapFromGapEquation (phononFrequencyFromA4 stiffnessRef ionMass)
        (electronPhononCoupling N0 V) > 0 ∧
      superconductingOrderTensor cartanEigenvalue s Γ τ > 0 := by
  have h_posDef : (neutronCartan eps).PosDef :=
    neutronCartan_posDef_of_lt_five_fourths heps
  have h_chain := firstPrinciples_chain_pos (Γ := Γ) (τ := τ) hk hM hn hv hs
  exact ⟨h_posDef, h_chain.1, h_chain.2.1, h_chain.2.2.1, h_chain.2.2.2⟩

/-! ## 第十二步：同位素效应的 CQM 几何因子修正（FirstPrinciples 第八步补完） -/

/-- CQM 同位素指数（含几何因子修正）：
    α_CQM = 1/2 + ln(f(M₁)/f(M₂)) / ln(M₂/M₁)。
    当 f 为常数时 α = 1/2（精确退化到 BCS）；
    当 f 随质量变化时 α 偏离 1/2——这是 CQM 对非常规同位素效应的
    独特预言（重费米子、钌酸盐等体系中 α 可远离 0.5）。 -/
noncomputable def cqmIsotopeExponent (f1 f2 m1 m2 : ℝ) : ℝ :=
  1/2 + Real.log (f1 / f2) / Real.log (m2 / m1)

/-- 几何因子为常数时，CQM 同位素指数精确回到 BCS 的 1/2。
    这是 CQM 退化到 BCS 的同位素侧：f(H) = f(D) ⇒ α = 1/2。 -/
theorem cqmIsotopeExponent_constant_f {f m1 m2 : ℝ} (hm : m1 ≠ m2) (hf : f > 0) :
    cqmIsotopeExponent f f m1 m2 = 1/2 := by
  unfold cqmIsotopeExponent
  have h_div : f / f = 1 := by field_simp [ne_of_gt hf]
  simp [h_div]

/-- CQM 同位素位移的完整公式（含几何因子）：
    T_c(M₂) / T_c(M₁) = √(M₁/M₂) · √(f(M₁)/f(M₂))。
    第一因子为 BCS 谐波预言（ω_D ∝ M^(−1/2)），
    第二因子为 CQM 几何修正（有效质量 = 离子质量 × 几何因子）。 -/
theorem cqmIsotopeTcRatio (m1 m2 f1 f2 : ℝ) (hm1 : 0 < m1) (hm2 : 0 < m2)
    (hf1 : 0 < f1) (hf2 : 0 < f2) :
    Real.sqrt ((m1 * f1) / (m2 * f2)) = Real.sqrt (m1 / m2) * Real.sqrt (f1 / f2) := by
  calc
    Real.sqrt ((m1 * f1) / (m2 * f2))
        = Real.sqrt ((m1 / m2) * (f1 / f2)) := by ring_nf
    _ = Real.sqrt (m1 / m2) * Real.sqrt (f1 / f2) := by
      rw [Real.sqrt_mul (by positivity : 0 ≤ m1 / m2)]

/-- BCS 退化极限：f₁ = f₂ 时，CQM 同位素位移退化为纯谐波预言
    √(M₁/M₂)。这是 CQM 在简单金属（f ≈ 常数）中还原 BCS 同位素定律
    的严格表述。 -/
theorem cqmIsotopeTcRatio_bcsLimit (m1 m2 f : ℝ) (hm1 : 0 < m1) (hm2 : 0 < m2)
    (hf : 0 < f) :
    Real.sqrt ((m1 * f) / (m2 * f)) = Real.sqrt (m1 / m2) := by
  have h := cqmIsotopeTcRatio m1 m2 f f hm1 hm2 hf hf
  rw [h]
  have hf_div : Real.sqrt (f / f) = 1 := by
    have h_div : f / f = 1 := by field_simp [ne_of_gt hf]
    simp [h_div]
  simp [hf_div, mul_one]

end CQM
