-- Ring15LockWD3.lean（第 199 轮）：$w''$ 的端点闭式、条件式正性与形状项符号判据（G-188b-2）
-- 只 import Spec ＋ 上游证明模块 ＋ 基线库模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockWD
import Ring15LockWD2
import Ring15LockIbp
import Mathlib.Analysis.Calculus.Deriv.Inv
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockWD3

open MeasureTheory
open Filter
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma cont_sechSq : Continuous sechSq := by
  unfold sechSq
  exact continuous_const.div (Real.continuous_cosh.pow 2)
    (fun x => pow_ne_zero 2 (Real.cosh_pos x).ne')

private lemma hasDerivAt_tanh' (x : ℝ) : HasDerivAt Real.tanh (sechSq x) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = sechSq x := by
    have hc := Real.cosh_sq x
    unfold sechSq
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

/-- $\tanh\frac{1}{2T}$ 对 $T$ 的导数：内层 $\frac{1}{2T}$ 的导数 $-\frac{1}{2T^2}$ 乘 $\mathrm{sech}^2$。 -/
private lemma hasDerivAt_tanh_inv (T : ℝ) (hT : T ≠ 0) :
    HasDerivAt (fun T : ℝ => Real.tanh (1 / (2 * T)))
      (sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))) T := by
  have hinner : HasDerivAt (fun T : ℝ => 1 / (2 * T)) (-(1 / (2 * T ^ 2))) T := by
    have hinv : HasDerivAt (fun T : ℝ => T⁻¹) (-(T ^ 2)⁻¹) T := hasDerivAt_inv hT
    have hmul := hinv.const_mul (1 / 2)
    have hfun : (fun T : ℝ => (1 / 2) * T⁻¹) = fun T : ℝ => 1 / (2 * T) := by
      funext T; ring
    have hval : (1 / 2) * (-(T ^ 2)⁻¹) = -(1 / (2 * T ^ 2)) := by
      field_simp
    rw [hfun, hval] at hmul
    exact hmul
  have hcomp := (hasDerivAt_tanh' (1 / (2 * T))).comp T hinner
  simpa [Function.comp] using hcomp

/-- G-188b-2a：$w''(T)=\dfrac{w'(T)}{T}+\dfrac{1}{T^3}\mathrm{sech}^2\dfrac{1}{2T}$。 -/
theorem targetPropWGapDeriv2Alt : CQM.Ring15.Spec.TargetPropWGapDeriv2Alt := by
  intro T hT
  have hTne : T ≠ 0 := ne_of_gt hT
  -- 左：w 的导数
  have hL : HasDerivAt wGap (wGapDeriv T) T :=
    CQM.Ring15.LockWD.targetPropWGapDeriv T hT
  -- 右：tanh(1/2T) + (T/2)·w'
  have h1 : HasDerivAt (fun T : ℝ => Real.tanh (1 / (2 * T)))
      (sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))) T := hasDerivAt_tanh_inv T hTne
  have h2 : HasDerivAt (fun T : ℝ => T / 2) (1 / 2) T := by
    have := (hasDerivAt_id T).const_mul (1 / 2)
    simpa [mul_comm] using this
  have h3 : HasDerivAt wGapDeriv (wGapDeriv2 T) T :=
    CQM.Ring15.LockWD2.targetPropWGapDeriv2 T hT
  have h4 : HasDerivAt (fun T : ℝ => (T / 2) * wGapDeriv T)
      ((1 / 2) * wGapDeriv T + (T / 2) * wGapDeriv2 T) T := h2.mul h3
  have hR : HasDerivAt (fun T : ℝ => Real.tanh (1 / (2 * T)) + (T / 2) * wGapDeriv T)
      (sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))
        + ((1 / 2) * wGapDeriv T + (T / 2) * wGapDeriv2 T)) T := h1.add h4
  -- 右函数在 T 的邻域上等于 w（v24 恒等式）
  have heq : (fun T : ℝ => Real.tanh (1 / (2 * T)) + (T / 2) * wGapDeriv T)
      =ᶠ[nhds T] wGap := by
    filter_upwards [show Set.Ioo (0 : ℝ) (2 * T) ∈ nhds T from
      Ioo_mem_nhds (by linarith) (by linarith)] with T' hT'
    have hp : (0 : ℝ) < T' := hT'.1
    exact (CQM.Ring15.LockIbp.targetPropWGapIbp T' hp).symm
  have hRc : HasDerivAt wGap
      (sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))
        + ((1 / 2) * wGapDeriv T + (T / 2) * wGapDeriv2 T)) T :=
    hR.congr_of_eventuallyEq heq.symm
  have hval : wGapDeriv T
      = sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))
        + ((1 / 2) * wGapDeriv T + (T / 2) * wGapDeriv2 T) := (hRc.unique hL).symm
  -- 代数：由上式整除 T/2
  have hkey : (T / 2) * wGapDeriv2 T
      = (1 / 2) * wGapDeriv T + sechSq (1 / (2 * T)) / (2 * T ^ 2) := by
    have hsech : sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))
        = -(sechSq (1 / (2 * T)) / (2 * T ^ 2)) := by
      field_simp
    linarith [hval, hsech]
  have hmul := congrArg (fun x : ℝ => (2 / T) * x) hkey
  have hlhs : (2 / T) * ((T / 2) * wGapDeriv2 T) = wGapDeriv2 T := by
    field_simp
  have hrhs : (2 / T) * ((1 / 2) * wGapDeriv T + sechSq (1 / (2 * T)) / (2 * T ^ 2))
      = wGapDeriv T / T + sechSq (1 / (2 * T)) / T ^ 3 := by
    field_simp
  simp only [] at hmul
  rw [hlhs, hrhs] at hmul
  simpa [wGapDeriv2Alt] using hmul

/-- G-188b-2b：$T^2|w'|<\mathrm{sech}^2\frac{1}{2T}$ ⇒ $w''>0$。 -/
theorem targetPropWGapDeriv2Pos : CQM.Ring15.Spec.TargetPropWGapDeriv2Pos := by
  intro T hT hlt
  have halt := targetPropWGapDeriv2Alt T hT
  have hT2 : (0 : ℝ) < T ^ 2 := pow_pos hT 2
  have hwneg : wGapDeriv T < 0 := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have hwabs : wGapDeriv T = -|wGapDeriv T| := by
    have := abs_of_neg hwneg
    linarith [this]
  have hle : |wGapDeriv T| < sechSq (1 / (2 * T)) / T ^ 2 := by
    rw [lt_div_iff₀ hT2]
    nlinarith [hlt]
  have hspos : 0 < sechSq (1 / (2 * T)) := by
    unfold sechSq
    exact div_pos one_pos (pow_pos (Real.cosh_pos (1 / (2 * T))) 2)
  have hnum : 0 < T ^ 2 * wGapDeriv T + sechSq (1 / (2 * T)) := by
    have hmul : T ^ 2 * wGapDeriv T = -(T ^ 2 * |wGapDeriv T|) := by
      have h1 := congrArg (fun x : ℝ => T ^ 2 * x) hwabs
      simp only [] at h1
      linarith [h1]
    nlinarith [hlt, hmul]
  have hT3 : (0 : ℝ) < T ^ 3 := pow_pos hT 3
  have hsplit : wGapDeriv2 T
      = (T ^ 2 * wGapDeriv T + sechSq (1 / (2 * T))) / T ^ 3 := by
    rw [halt]
    unfold wGapDeriv2Alt
    field_simp
  rw [hsplit]
  exact div_pos hnum hT3

/-- G-188b-2c：$S'(T)<0\iff w(T)\,w''(T)<(w'(T))^2$（分母 $(w')^2>0$）。 -/
theorem targetPropShapeDerivSign : CQM.Ring15.Spec.TargetPropShapeDerivSign := by
  intro T hT
  have hne : wGapDeriv T ≠ 0 := ne_of_lt (CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT)
  have hpos : (0 : ℝ) < wGapDeriv T ^ 2 := by simpa [sq_abs] using pow_pos (abs_pos.mpr hne) 2
  have hiff : shapeDeriv T < 0 ↔ wGap T * wGapDeriv2 T - wGapDeriv T ^ 2 < 0 := by
    unfold shapeDeriv
    rw [div_lt_iff₀ hpos]
    ring_nf
  constructor
  · intro h
    have h' := hiff.mp h
    linarith
  · intro h
    apply hiff.mpr
    linarith

end

end CQM.Ring15.LockWD3
