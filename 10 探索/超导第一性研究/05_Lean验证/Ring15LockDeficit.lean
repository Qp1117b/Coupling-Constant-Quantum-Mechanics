-- Ring15LockDeficit.lean（第 202 轮）：判据的 δ／λ 形式与判据比 r 的双侧夹逼（G-188b-2g）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockW
import Ring15LockWD
import Ring15LockIbp
import Ring15LockUnary
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockDeficit

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma cont_sechSq : Continuous sechSq := by
  unfold sechSq
  exact continuous_const.div (Real.continuous_cosh.pow 2)
    (fun x => pow_ne_zero 2 (Real.cosh_pos x).ne')

private lemma sechSq_pos (x : ℝ) : 0 < sechSq x := by
  unfold sechSq
  exact div_pos one_pos (pow_pos (Real.cosh_pos x) 2)

private lemma sechSq_le_one (x : ℝ) : sechSq x ≤ 1 := by
  unfold sechSq
  have hc : 1 ≤ Real.cosh x ^ 2 := by
    have h1 := Real.one_le_cosh x
    have hp := Real.cosh_pos x
    nlinarith [h1, hp]
  rw [div_le_iff₀ (pow_pos (Real.cosh_pos x) 2)]
  nlinarith [hc]

private lemma sechSq_anti {x y : ℝ} (h : |x| ≤ |y|) : sechSq y ≤ sechSq x := by
  have hc : Real.cosh x ≤ Real.cosh y := Real.cosh_le_cosh.mpr h
  have hx := Real.cosh_pos x
  have hy := Real.cosh_pos y
  have hsq : Real.cosh x ^ 2 ≤ Real.cosh y ^ 2 := by
    nlinarith [hc, hx, hy]
  unfold sechSq
  exact one_div_le_one_div_of_le (pow_pos hx 2) hsq

private lemma tanhPos {T : ℝ} (hT : 0 < T) : 0 < Real.tanh (1 / (2 * T)) := by
  have hx : 0 < 1 / (2 * T) := by positivity
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos _)

private lemma sechSq_eq_one_sub_tanh_sq (x : ℝ) : sechSq x = 1 - Real.tanh x ^ 2 := by
  unfold sechSq
  rw [Real.tanh_eq_sinh_div_cosh, div_pow]
  have hcs := Real.cosh_sq_sub_sinh_sq x
  have hc : Real.cosh x ^ 2 ≠ 0 := pow_ne_zero 2 (Real.cosh_pos x).ne'
  field_simp
  linarith

/-- $\int_0^1u^2\,du=1/3$（FTC：原函数 $u^3/3$）。 -/
private lemma int_u_sq : ∫ u in (0 : ℝ)..1, u ^ 2 = 1 / 3 := by
  have hd : ∀ x ∈ Set.uIcc (0 : ℝ) 1, HasDerivAt (fun y : ℝ => y ^ 3 / 3) (x ^ 2) x := by
    intro x _
    have h := (hasDerivAt_pow 3 x).div_const 3
    have hv : (3 : ℝ) * x ^ (3 - 1) / 3 = x ^ 2 := by
      rw [show x ^ (3 - 1) = x ^ 2 from rfl]
      ring
    simpa [hv] using h
  have hInt : IntervalIntegrable (fun u : ℝ => u ^ 2) volume (0 : ℝ) 1 :=
    (continuous_id.pow 2).intervalIntegrable 0 1
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hInt
  simpa using h

/-- $|w'(T)|$ 的积分式（照定义展开，$T>0$）：$|w'|=\frac{1}{T^2}\int_0^1u^2\mathrm{sech}^2\frac{u}{2T}$。 -/
private lemma abs_deriv (T : ℝ) (hT : 0 < T) :
    |wGapDeriv T| = (1 / T ^ 2) * ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
  have hcont : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
    (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * T)))
  have hBpos : 0 < ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    refine intervalIntegral.integral_pos (a := (0 : ℝ)) (b := 1) (by norm_num)
      hcont.continuousOn (fun x hx => ?_) ⟨1 / 2, ⟨by norm_num, by norm_num⟩, ?_⟩
    · exact mul_nonneg (sq_nonneg x) (le_of_lt (sechSq_pos _))
    · exact mul_pos (by norm_num) (sechSq_pos _)
  have hT2 : (0 : ℝ) < T ^ 2 := pow_pos hT 2
  have h1 : (0 : ℝ) < 1 / T ^ 2 := one_div_pos.mpr hT2
  have hneg : -(1 / T ^ 2) * (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))) < 0 := by
    nlinarith [hBpos, h1]
  rw [wGapDeriv, abs_of_neg hneg]
  ring

/-- $r(T)=T^2|w'|/\mathrm{sech}^2\frac{1}{2T}$ 的积分商写法（$T>0$）。 -/
private lemma ratio_integral (T : ℝ) (hT : 0 < T) :
    ratioR T = (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)))
      / sechSq (1 / (2 * T)) := by
  have hSpos : 0 < sechSq (1 / (2 * T)) := sechSq_pos _
  unfold ratioR
  rw [abs_deriv T hT]
  have hTne : T ^ 2 ≠ 0 := (pow_pos hT 2).ne'
  have hSne : sechSq (1 / (2 * T)) ≠ 0 := hSpos.ne'
  field_simp

/-- **G-188b-2g-1 落地：$1/3\le r(T)$**。
$\mathrm{sech}^2\frac{u}{2T}\ge\mathrm{sech}^2\frac{1}{2T}$（$u\in[0,1]$，$\cosh$ 单增），
逐点乘 $u^2\ge0$ 后积分给 $T^2|w'|\ge\frac13\mathrm{sech}^2\frac{1}{2T}$，除以正量即得。 -/
theorem targetPropRatioBracketLow : CQM.Ring15.Spec.TargetPropRatioBracketLow := by
  intro T hT
  have hcont : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
    (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * T)))
  have hSpos : 0 < sechSq (1 / (2 * T)) := sechSq_pos _
  have hmono : ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (1 / (2 * T))
      ≤ ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_on (a := (0 : ℝ)) (b := 1) (by norm_num)
      (((continuous_id.pow 2).mul continuous_const).intervalIntegrable 0 1) ?_ ?_
    · exact hcont.intervalIntegrable 0 1
    · intro x hx
      have hx1 : x / (2 * T) ≤ 1 / (2 * T) := by
        rw [div_le_div_iff₀ (by positivity : (0 : ℝ) < 2 * T) (by positivity : (0 : ℝ) < 2 * T)]
        nlinarith [hx.2]
      have harg : |x / (2 * T)| ≤ |1 / (2 * T)| := by
        rw [abs_of_nonneg (div_nonneg hx.1 (by positivity)),
          abs_of_nonneg (by positivity)]
        exact hx1
      exact mul_le_mul_of_nonneg_left (sechSq_anti harg) (sq_nonneg x)
  have hc : ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (1 / (2 * T))
      = sechSq (1 / (2 * T)) * (1 / 3) := by
    rw [show (fun u : ℝ => u ^ 2 * sechSq (1 / (2 * T)))
        = (fun u : ℝ => sechSq (1 / (2 * T)) * u ^ 2) from funext fun u => mul_comm _ _]
    rw [intervalIntegral.integral_const_mul, int_u_sq]
  rw [ratio_integral T hT, le_div_iff₀ hSpos]
  have h3 : sechSq (1 / (2 * T)) * (1 / 3)
      ≤ ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) := by
    rw [← hc]
    exact hmono
  nlinarith [h3]

/-- **G-188b-2g-2 落地：$r(T)\le 1/(3\,\mathrm{sech}^2\frac{1}{2T})$**。
$\mathrm{sech}^2\le1$ 逐点乘 $u^2$ 后积分给 $T^2|w'|\le\int_0^1u^2=\frac13$。 -/
theorem targetPropRatioBracketHigh : CQM.Ring15.Spec.TargetPropRatioBracketHigh := by
  intro T hT
  have hcont : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
    (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * T)))
  have hSpos : 0 < sechSq (1 / (2 * T)) := sechSq_pos _
  have hmono : ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))
      ≤ ∫ u in (0 : ℝ)..1, u ^ 2 * (1 : ℝ) := by
    refine intervalIntegral.integral_mono_on (a := (0 : ℝ)) (b := 1) (by norm_num)
      (hcont.intervalIntegrable 0 1) ?_ ?_
    · exact ((continuous_id.pow 2).mul continuous_const).intervalIntegrable 0 1
    · intro x _
      simpa using mul_le_mul_of_nonneg_left (sechSq_le_one (x / (2 * T))) (sq_nonneg x)
  have hB3 : ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) ≤ 1 / 3 := by
    have h : ∫ u in (0 : ℝ)..1, u ^ 2 * (1 : ℝ) = 1 / 3 := by
      rw [← int_u_sq]
      simp
    rw [← h]
    exact hmono
  rw [ratio_integral T hT, div_le_iff₀ hSpos]
  have hX : 1 / (3 * sechSq (1 / (2 * T))) * sechSq (1 / (2 * T)) = 1 / 3 := by
    field_simp
  rw [hX]
  exact hB3

/-- **G-188b-2g-3 落地：$\lambda(T)=1/(T\sinh\frac1T)$**。
$\mathrm{sech}^2=\frac{1}{\cosh^2}$、$\tanh=\frac{\sinh}{\cosh}$，再用二倍角
$\sinh\frac1T=\sinh\left(2\cdot\frac{1}{2T}\right)=2\sinh\frac{1}{2T}\cosh\frac{1}{2T}$ 约分。 -/
theorem targetPropLambdaForm : CQM.Ring15.Spec.TargetPropLambdaForm := by
  intro T hT
  have hx : 0 < 1 / (2 * T) := by positivity
  have hTne : T ≠ 0 := hT.ne'
  have hc : Real.cosh (1 / (2 * T)) ≠ 0 := (Real.cosh_pos _).ne'
  have hs : Real.sinh (1 / (2 * T)) ≠ 0 := (Real.sinh_pos_iff.mpr hx).ne'
  have h2 : (1 : ℝ) / T = 2 * (1 / (2 * T)) := by
    field_simp
  have hsinh : Real.sinh (1 / T) = 2 * Real.sinh (1 / (2 * T)) * Real.cosh (1 / (2 * T)) := by
    rw [h2]
    exact Real.sinh_two_mul _
  unfold endpointLambda shapeH sechSq
  rw [Real.tanh_eq_sinh_div_cosh, hsinh]
  field_simp

/-- 纯代数：$0<2Th\delta(1+\delta)-(1-\delta)(1-h^2)\iff(1-h^2)/(2Th)<\delta(1+\delta)/(1-\delta)$
（$\delta=1-\Phi$；两边同除以正量 $2Th\delta$，不改语义）。 -/
private lemma criterionPhi {T h Φ : ℝ} (hT : 0 < T) (hh : 0 < h)
    (h0 : 0 < Φ) (_h1 : Φ < 1) :
    (0 < 2 * T * h * (1 - Φ) * (2 - Φ) - Φ * (1 - h ^ 2)) ↔
      ((1 - h ^ 2) / (2 * T * h) < (1 - Φ) * (2 - Φ) / Φ) := by
  have h2T : (0 : ℝ) < 2 * T * h := by positivity
  constructor
  · intro hpos
    rw [div_lt_div_iff₀ h2T h0]
    nlinarith [hpos]
  · intro hlt
    rw [div_lt_div_iff₀ h2T h0] at hlt
    nlinarith [hlt]

/-- **G-188b-2g-4 落地：判据的 δ／λ 形式**。
由 201 的一元化 $S'<0\iff0<G$，把 $G>0$ 整块除以 $(2Th)\delta>0$：
$0<G\iff\lambda<\dfrac{\delta(1+\delta)}{1-\delta}$，$\delta=1-\Phi$、$\lambda$ 取 G-188b-2g-3 的闭式。
判据不再需要 $r$，也不再需要对 $\Phi$ 的单调性下判断；只比 $\lambda(T)$ 与 $\delta$ 的显式阈值。 -/
theorem targetPropShapeSignDeficit : CQM.Ring15.Spec.TargetPropShapeSignDeficit := by
  intro T hT
  have hunary := CQM.Ring15.LockUnary.targetPropShapeSignUnary T hT
  rw [hunary]
  have hh0 : 0 < shapeH T := by
    unfold shapeH
    exact tanhPos hT
  have hw0 : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT
  have hwh : wGap T < shapeH T := CQM.Ring15.LockIbp.targetPropShapeEndGt T hT
  have hΦeq : shapePhi T = wGap T / shapeH T := rfl
  have h0 : 0 < shapePhi T := by
    rw [hΦeq]
    exact div_pos hw0 hh0
  have h1 : shapePhi T < 1 := by
    rw [hΦeq, div_lt_one hh0]
    exact hwh
  have hPne : shapePhi T ≠ 0 := h0.ne'
  have hS : sechSq (1 / (2 * T)) = 1 - shapeH T ^ 2 := by
    unfold shapeH
    exact sechSq_eq_one_sub_tanh_sq _
  have hlam : endpointLambda T = (1 - shapeH T ^ 2) / (2 * T * shapeH T) := by
    unfold endpointLambda
    rw [hS]
  have hred : deficitFrac T * (1 + deficitFrac T) / (1 - deficitFrac T)
      = (1 - shapePhi T) * (2 - shapePhi T) / shapePhi T := by
    unfold deficitFrac
    congr 1
    · ring
    · ring
  have hG : shapeG T = 2 * T * shapeH T * (1 - shapePhi T) * (2 - shapePhi T)
      - shapePhi T * (1 - shapeH T ^ 2) := rfl
  rw [hlam, hred, hG]
  exact criterionPhi hT hh0 h0 h1

end

end CQM.Ring15.LockDeficit
