-- Ring15LockTStrict.lean（第 193 轮）：$w$ 的严格减沿 $T\to K\to y\to t$ 链传下去
-- 本环三定理：K 严格减、y 严格增、t 严格增（p 固定）。
-- 只 import Spec；$w$ 的严格性在本模块内私有重证（不 import 任何证明模块），故链是自足的。
import Ring15Spec
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockTStrict

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec

noncomputable section

/- ===== 私有：$w$ 的严格单调（与 192 轮同形，本模块内自足重证） ===== -/

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

/-- $0<T_1<T_2\Rightarrow w(T_2)<w(T_1)$（`integral_mono_on`＋`integral_pos`＋`integral_sub`）。 -/
private lemma wGap_strictAnti {T1 T2 : ℝ} (h1 : 0 < T1) (h12 : T1 < T2) : wGap T2 < wGap T1 := by
  have h2 : 0 < T2 := lt_trans h1 h12
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
  have hdiff_cont : Continuous fun u : ℝ =>
      2 * u * Real.tanh (u / (2 * T1)) - 2 * u * Real.tanh (u / (2 * T2)) :=
    (cont_integrand T1).sub (cont_integrand T2)
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
  have hsub : (∫ u in (0 : ℝ)..1,
        (2 * u * Real.tanh (u / (2 * T1)) - 2 * u * Real.tanh (u / (2 * T2)))) = ((∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T1))) - (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T2)))) := by
    exact intervalIntegral.integral_sub (f := fun u : ℝ => 2 * u * Real.tanh (u / (2 * T1)))
      (g := fun u : ℝ => 2 * u * Real.tanh (u / (2 * T2))) (μ := volume)
      ((cont_integrand T1).intervalIntegrable 0 1)
      ((cont_integrand T2).intervalIntegrable 0 1)
  show (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T2))) < (∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T1)))
  simp only [sub_eq_add_neg] at hpos hsub ⊢
  linarith

/- ===== 私有：$y$ 的严格反单调与正性 ===== -/

private lemma fugOfK_strictAnti {K1 K2 : ℝ} (h : K1 < K2) : fugOfK K2 < fugOfK K1 := by
  have hpi2 : (0 : ℝ) < Real.pi ^ 2 / 2 := div_pos (pow_pos Real.pi_pos 2) (by norm_num)
  have hmid : Real.pi ^ 2 * K1 / 2 < Real.pi ^ 2 * K2 / 2 := by
    have hm := mul_lt_mul_of_pos_left h hpi2
    calc Real.pi ^ 2 * K1 / 2 = Real.pi ^ 2 / 2 * K1 := by ring
      _ < Real.pi ^ 2 / 2 * K2 := hm
      _ = Real.pi ^ 2 * K2 / 2 := by ring
  have harg : -(Real.pi ^ 2 * K2 / 2) < -(Real.pi ^ 2 * K1 / 2) := by linarith
  have hexp : Real.exp (-(Real.pi ^ 2 * K2 / 2)) < Real.exp (-(Real.pi ^ 2 * K1 / 2)) :=
    Real.exp_lt_exp.mpr harg
  have h2pi : (0 : ℝ) < 2 * Real.pi := by linarith [Real.pi_pos]
  unfold fugOfK
  exact mul_lt_mul_of_pos_left hexp h2pi

private lemma fugOfK_pos (K : ℝ) : 0 < fugOfK K := by
  unfold fugOfK
  have h2pi : (0 : ℝ) < 2 * Real.pi := by linarith [Real.pi_pos]
  exact mul_pos h2pi (Real.exp_pos _)

/- ===== 本环三条 ===== -/

theorem targetPropKStrictAnti : TargetPropKStrictAnti := by
  intro ups0 T1 T2 h0 h1 h12 hw1
  have h2 : 0 < T2 := lt_trans h1 h12
  have hw : wGap T2 < wGap T1 := wGap_strictAnti h1 h12
  have hA : wGap T2 / T2 < wGap T1 / T2 := div_lt_div_of_pos_right hw h2
  have hB : wGap T1 / T2 < wGap T1 / T1 := div_lt_div_of_pos_left hw1 h1 h12
  have hC : wGap T2 / T2 < wGap T1 / T1 := lt_trans hA hB
  have hD : ups0 * (wGap T2 / T2) < ups0 * (wGap T1 / T1) :=
    mul_lt_mul_of_pos_left hC h0
  calc (ups0 * wGap T2) / T2 = ups0 * (wGap T2 / T2) := by ring
    _ < ups0 * (wGap T1 / T1) := hD
    _ = (ups0 * wGap T1) / T1 := by ring

theorem targetPropYStrictMono : TargetPropYStrictMono := by
  intro ups0 T1 T2 h0 h1 h12 hw1 hw2
  have h2 : 0 < T2 := lt_trans h1 h12
  have hK : (ups0 * wGap T2) / T2 < (ups0 * wGap T1) / T1 :=
    targetPropKStrictAnti (ups0 := ups0) (T1 := T1) (T2 := T2) h0 h1 h12 hw1
  unfold yOfT
  exact fugOfK_strictAnti hK

/-- 差商写法（与 186 轮同形）：$t(y_2)-t(y_1)=m\cdot[\ln(1-y_2)-\ln(1-y_1)]/\ln p$。 -/
private lemma tEffM_sub (p y1 y2 : ℝ) (m : ℕ) :
    tEffM p y2 m - tEffM p y1 m
      = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) / Real.log p) := by
  unfold tEffM
  field_simp
  ring

theorem targetPropTStrictMono : TargetPropTStrictMono := by
  intro ups0 T1 T2 p m h0 h1 h12 hw1 hw2 hp0 hp1 hm hy1 hy2
  have hy : yOfT ups0 T1 < yOfT ups0 T2 :=
    targetPropYStrictMono (ups0 := ups0) (T1 := T1) (T2 := T2) h0 h1 h12 hw1 hw2
  have hy1pos : (0 : ℝ) < 1 - yOfT ups0 T1 := by linarith
  have hy2pos : (0 : ℝ) < 1 - yOfT ups0 T2 := by linarith
  have hlog : Real.log (1 - yOfT ups0 T2) < Real.log (1 - yOfT ups0 T1) :=
    Real.log_lt_log hy2pos (by linarith)
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hnum : Real.log (1 - yOfT ups0 T2) - Real.log (1 - yOfT ups0 T1) < 0 := by linarith
  have hquot : 0 < (Real.log (1 - yOfT ups0 T2) - Real.log (1 - yOfT ups0 T1)) / Real.log p :=
    (div_pos_iff).mpr (Or.inr ⟨hnum, hlogp⟩)
  have hm0 : 0 < m := lt_of_lt_of_le Nat.zero_lt_one hm
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm0
  have hdiff : tEffM p (yOfT ups0 T2) m - tEffM p (yOfT ups0 T1) m
      = (m : ℝ) * ((Real.log (1 - yOfT ups0 T2) - Real.log (1 - yOfT ups0 T1))
          / Real.log p) :=
    tEffM_sub p (yOfT ups0 T1) (yOfT ups0 T2) m
  have hpos : 0 < tEffM p (yOfT ups0 T2) m - tEffM p (yOfT ups0 T1) m := by
    rw [hdiff]
    exact mul_pos hmpos hquot
  linarith

end

end CQM.Ring15.LockTStrict
