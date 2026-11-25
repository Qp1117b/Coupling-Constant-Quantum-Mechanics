-- Ring15LockIbp.lean（第 197 轮）：$w$ 的分部积分恒等式与形状项分解（G-188a）
-- 只 import Spec ＋ 三角导数基线；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockWD
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus

namespace CQM.Ring15.LockIbp

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma hasDerivAt_tanh' (x : ℝ) : HasDerivAt Real.tanh (1 / Real.cosh x ^ 2) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = 1 / Real.cosh x ^ 2 := by
    have hc := Real.cosh_sq x
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

private lemma cont_sechSq : Continuous sechSq := by
  unfold sechSq
  exact continuous_const.div (Real.continuous_cosh.pow 2)
    (fun x => pow_ne_zero 2 (Real.cosh_pos x).ne')

private lemma cont_A (T : ℝ) : Continuous fun u : ℝ => u * Real.tanh (u / (2 * T)) :=
  continuous_id.mul (continuous_tanh.comp (continuous_id.div_const (2 * T)))

private lemma cont_B (T : ℝ) : Continuous fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)) :=
  (continuous_id.pow 2).mul (cont_sechSq.comp (continuous_id.div_const (2 * T)))

/-- 分部积分恒等式（G-188a 主定理）。 -/
theorem targetPropWGapIbp : CQM.Ring15.Spec.TargetPropWGapIbp := by
  intro T hT
  -- (A) ∫ u tanh(u/2T) = w/2
  have hA : (∫ u in (0 : ℝ)..1, u * Real.tanh (u / (2 * T))) = wGap T / 2 := by
    have h2 : wGap T = 2 * ∫ u in (0 : ℝ)..1, u * Real.tanh (u / (2 * T)) := by
      rw [wGap]
      have h := intervalIntegral.integral_const_mul (μ := (volume : Measure ℝ)) (a := (0 : ℝ)) (b := 1) (r := (2 : ℝ))
        (f := fun u : ℝ => u * Real.tanh (u / (2 * T)))
      have hf : (fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)))
          = fun u : ℝ => 2 * (u * Real.tanh (u / (2 * T))) := by
        funext u; ring
      rw [← hf] at h
      exact h
    linarith
  -- (B) ∫ u^2 sech^2(u/2T) = -(T^2) * w'
  have hB : (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))) = -(T ^ 2) * wGapDeriv T := by
    rw [wGapDeriv]
    field_simp
    try ring
  -- F 与 G 命名，避免 beta-未归约
  set F : ℝ → ℝ := fun u => u ^ 2 / 2 * Real.tanh (u / (2 * T)) with hF
  set G : ℝ → ℝ := fun u => u * Real.tanh (u / (2 * T))
      + (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T))) with hG
  -- 逐点导数
  have hderiv : ∀ u ∈ Set.uIcc (0 : ℝ) 1, HasDerivAt F (G u) u := by
    intro u hu
    have hinner : HasDerivAt (fun u : ℝ => u / (2 * T)) (1 / (2 * T)) u := by
      have h := (hasDerivAt_id u).div_const (2 * T)
      simpa using h
    have htanh : HasDerivAt Real.tanh (sechSq (u / (2 * T))) (u / (2 * T)) :=
      hasDerivAt_tanh' (u / (2 * T))
    have hcomp : HasDerivAt (fun u : ℝ => Real.tanh (u / (2 * T)))
        (sechSq (u / (2 * T)) * (1 / (2 * T))) u := by
      simpa [Function.comp] using htanh.comp u hinner
    have hsq : HasDerivAt (fun u : ℝ => u ^ 2 / 2) u u := by
      have h1 : HasDerivAt (fun u : ℝ => u ^ 2) (2 * u) u := by
        simpa using (hasDerivAt_id u).pow 2
      simpa using h1.div_const 2
    have hmul := hsq.mul hcomp
    have hval : u * Real.tanh (u / (2 * T)) + u ^ 2 / 2 * (sechSq (u / (2 * T)) * (1 / (2 * T)))
        = u * Real.tanh (u / (2 * T)) + (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T))) := by
      field_simp
      try ring
    rw [hval] at hmul
    exact hmul
  -- 可积性
  have hcontG : Continuous G := by
    have h : Continuous fun u : ℝ => u * Real.tanh (u / (2 * T))
        + (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T))) :=
      (cont_A T).add (continuous_const.mul (cont_B T))
    simpa [hG] using h
  have hint : IntervalIntegrable G volume (0 : ℝ) 1 := hcontG.intervalIntegrable 0 1
  -- FTC
  have hFTC : (∫ u in (0 : ℝ)..1, G u) = F 1 - F 0 :=
    intervalIntegral.integral_eq_sub_of_hasDerivAt (a := (0 : ℝ)) (b := 1) hderiv hint
  have hF10 : F 1 - F 0 = (1 / 2) * Real.tanh (1 / (2 * T)) := by
    rw [hF]
    simp [Real.tanh_zero]
    try ring
  -- 拆分 ∫G = ∫A + ∫(const * B)
  have hsplit : (∫ u in (0 : ℝ)..1, G u)
      = (∫ u in (0 : ℝ)..1, u * Real.tanh (u / (2 * T)))
        + (∫ u in (0 : ℝ)..1, (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T)))) := by
    have h1 : IntervalIntegrable (fun u : ℝ => u * Real.tanh (u / (2 * T))) volume (0 : ℝ) 1 :=
      (cont_A T).intervalIntegrable 0 1
    have h2 : IntervalIntegrable (fun u : ℝ => (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T))))
        volume (0 : ℝ) 1 :=
      (continuous_const.mul (cont_B T)).intervalIntegrable 0 1
    have hadd := intervalIntegral.integral_add (μ := (volume : Measure ℝ)) (a := (0 : ℝ)) (b := 1) h1 h2
    simpa [hG] using hadd
  -- 常数提出
  have hconst : (∫ u in (0 : ℝ)..1, (1 / (4 * T)) * (u ^ 2 * sechSq (u / (2 * T))))
      = (1 / (4 * T)) * (∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))) :=
    intervalIntegral.integral_const_mul (μ := (volume : Measure ℝ)) (a := (0 : ℝ)) (b := 1) (r := (1 / (4 * T)))
      (f := fun u : ℝ => u ^ 2 * sechSq (u / (2 * T)))
  -- 合成：(1/2)tanh = w/2 + (1/(4T))*(-(T^2)w')
  have hchain : (1 / 2) * Real.tanh (1 / (2 * T))
      = wGap T / 2 + (1 / (4 * T)) * (-(T ^ 2) * wGapDeriv T) := by
    have h1 := hFTC
    rw [hF10] at h1
    rw [hsplit] at h1
    rw [hconst] at h1
    rw [hA] at h1
    rw [hB] at h1
    exact h1.symm
  have hval : (1 / (4 * T)) * (-(T ^ 2) * wGapDeriv T) = -(T / 4) * wGapDeriv T := by
    field_simp
    try ring
  rw [hval] at hchain
  linarith

/-- 形状项分解。 -/
theorem targetPropShapeSplit : CQM.Ring15.Spec.TargetPropShapeSplit := by
  intro T hT
  have hneg := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have habs : |wGapDeriv T| = -(wGapDeriv T) := abs_of_neg hneg
  have hibp := targetPropWGapIbp T hT
  have hne : wGapDeriv T ≠ 0 := ne_of_lt hneg
  rw [habs, hibp]
  field_simp [hne]
  ring

/-- 端点亏损恒等式。 -/
theorem targetPropShapeEnd : CQM.Ring15.Spec.TargetPropShapeEnd := by
  intro T hT
  have hneg := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have habs : |wGapDeriv T| = -(wGapDeriv T) := abs_of_neg hneg
  have hibp := targetPropWGapIbp T hT
  rw [habs, hibp]
  ring

/-- 端点严格高于窗口平均。 -/
theorem targetPropShapeEndGt : CQM.Ring15.Spec.TargetPropShapeEndGt := by
  intro T hT
  have hneg := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have hend := targetPropShapeEnd T hT
  have hpos : 0 < (T / 2) * |wGapDeriv T| :=
    mul_pos (by linarith) (abs_pos.mpr (ne_of_lt hneg))
  linarith

end

end CQM.Ring15.LockIbp
