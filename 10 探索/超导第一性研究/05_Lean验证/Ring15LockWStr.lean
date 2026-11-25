-- Ring15LockWStr.lean（第 192 轮）：$w$ 的严格单调——$0<T_1<T_2\Rightarrow w(T_2)<w(T_1)$。
-- 路线：逐点单调（`integral_mono_on`）给 $\le$；再把差值照 `integral_pos` 判正，
-- 从而由 `integral_sub` 得严格不等。只 import Ring15Spec，不 import 任何证明模块。
import Ring15Spec
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockWStr

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

private lemma continuous_tanh : Continuous Real.tanh := by
  have h : Continuous fun y : ℝ => Real.sinh y / Real.cosh y :=
    Real.continuous_sinh.div Real.continuous_cosh (fun y => (Real.cosh_pos y).ne')
  exact h.congr (fun y => (Real.tanh_eq_sinh_div_cosh y).symm)

private lemma hasDerivAt_tanh (x : ℝ) : HasDerivAt Real.tanh (1 / Real.cosh x ^ 2) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = 1 / Real.cosh x ^ 2 := by
    have hc : Real.cosh x ^ 2 = Real.sinh x ^ 2 + 1 := Real.cosh_sq x
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

private lemma tanh_strictMono : StrictMono Real.tanh := by
  refine strictMono_of_deriv_pos (fun x => ?_)
  rw [(hasDerivAt_tanh x).deriv]
  exact one_div_pos.mpr (pow_pos (Real.cosh_pos x) 2)

private lemma cont_integrand (T : ℝ) :
    Continuous fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)) := by
  refine (continuous_const.mul continuous_id).mul ?_
  exact continuous_tanh.comp (continuous_id.div_const (2 * T))

theorem targetPropWGapStrictAnti : CQM.Ring15.Spec.TargetPropWGapStrictAnti := by
  intro T1 T2 h1 h12
  have h2 : 0 < T2 := lt_trans h1 h12
  -- 逐点：$g\le f$ 于 $[0,1]$（$g$ 用 $T_2$、$f$ 用 $T_1$）
  have hpt : ∀ x ∈ Set.Icc (0 : ℝ) 1,
      2 * x * Real.tanh (x / (2 * T2)) ≤ 2 * x * Real.tanh (x / (2 * T1)) := by
    intro x hx
    have hx0 : 0 ≤ x := hx.1
    have harg : x / (2 * T2) ≤ x / (2 * T1) :=
      div_le_div_of_nonneg_left hx0 (by linarith) (by linarith)
    have htanh : Real.tanh (x / (2 * T2)) ≤ Real.tanh (x / (2 * T1)) :=
      tanh_strictMono.monotone harg
    have h2x : 0 ≤ 2 * x := by linarith
    exact mul_le_mul_of_nonneg_left htanh h2x
  -- 差值连续
  have hdiff_cont : Continuous fun u : ℝ =>
      2 * u * Real.tanh (u / (2 * T1)) - 2 * u * Real.tanh (u / (2 * T2)) :=
    (cont_integrand T1).sub (cont_integrand T2)
  -- 差值严格正：非负 + 在 $u=1$ 处为正
  have hpos : 0 < ∫ u in (0 : ℝ)..1,
      (2 * u * Real.tanh (u / (2 * T1)) - 2 * u * Real.tanh (u / (2 * T2))) := by
    refine intervalIntegral.integral_pos (a := (0 : ℝ)) (b := 1) (by norm_num)
      hdiff_cont.continuousOn ?_ ?_
    · intro x hx
      have hxI : x ∈ Set.Icc (0 : ℝ) 1 := ⟨hx.1.le, hx.2⟩
      exact sub_nonneg.mpr (hpt x hxI)
    · refine ⟨1, ⟨by norm_num, le_rfl⟩, ?_⟩
      have harg : (1 : ℝ) / (2 * T2) < (1 : ℝ) / (2 * T1) :=
        div_lt_div_of_pos_left one_pos (by linarith) (by linarith)
      have htanh : Real.tanh ((1 : ℝ) / (2 * T2)) < Real.tanh ((1 : ℝ) / (2 * T1)) :=
        tanh_strictMono harg
      have h2n : (0 : ℝ) < 2 * 1 := by norm_num
      have hlt : 2 * (1 : ℝ) * Real.tanh ((1 : ℝ) / (2 * T2))
          < 2 * (1 : ℝ) * Real.tanh ((1 : ℝ) / (2 * T1)) :=
        mul_lt_mul_of_pos_left htanh h2n
      exact sub_pos.mpr hlt
  -- `integral_sub` 把差值积分拆开（显式给 f、g，使求积的被积函数与目标全部对齐）
  have hsub : (∫ u in (0 : ℝ)..1, (2 * u * Real.tanh (u / (2 * T1)) - 2 * u * Real.tanh (u / (2 * T2)))) = ((∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T1))) - (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T2)))) := by
    exact intervalIntegral.integral_sub (f := fun u : ℝ => 2 * u * Real.tanh (u / (2 * T1)))
      (g := fun u : ℝ => 2 * u * Real.tanh (u / (2 * T2))) (μ := volume)
      ((cont_integrand T1).intervalIntegrable 0 1)
      ((cont_integrand T2).intervalIntegrable 0 1)
  show (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T2))) < (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T1)))
  simp only [sub_eq_add_neg] at hpos hsub ⊢
  linarith

end CQM.Ring15.LockWStr
