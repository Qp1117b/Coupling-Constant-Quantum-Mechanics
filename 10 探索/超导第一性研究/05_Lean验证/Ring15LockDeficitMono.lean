-- Ring15LockDeficitMono.lean（第 204 轮）：δ 的导数、严格单增与判据右端随 T 的单增（G-188b-2i 前件）
-- 只 import Spec ＋已证模块 ＋基线库子模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockLambda
import Ring15LockWD
import Ring15LockIbp
import Ring15LockW
import Mathlib.Analysis.Calculus.Deriv.MeanValue
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.MeasureTheory.Integral.IntervalIntegral.FundThmCalculus
import Mathlib.Analysis.SpecialFunctions.Trigonometric.DerivHyp

namespace CQM.Ring15.LockDeficitMono

open MeasureTheory
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

private lemma hasDerivAt_tanh (x : ℝ) : HasDerivAt Real.tanh (sechSq x) x := by
  have hdiv : HasDerivAt (fun y : ℝ => Real.sinh y / Real.cosh y)
      ((Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2) x :=
    (Real.hasDerivAt_sinh x).div (Real.hasDerivAt_cosh x) (Real.cosh_pos x).ne'
  have hfun : (fun y : ℝ => Real.sinh y / Real.cosh y) = Real.tanh := by
    funext y; exact (Real.tanh_eq_sinh_div_cosh y).symm
  have hv : (Real.cosh x * Real.cosh x - Real.sinh x * Real.sinh x) / Real.cosh x ^ 2
      = sechSq x := by
    have hc := Real.cosh_sq_sub_sinh_sq x
    unfold sechSq
    field_simp
    nlinarith [hc]
  rw [hfun, hv] at hdiv
  exact hdiv

/-- $\tanh x<x$（$x>0$）：$\tanh x=\int_0^x\mathrm{sech}^2$，$\int_0^x(1-\mathrm{sech}^2)=\int_0^x\tanh^2>0$。 -/
private lemma tanh_lt_self {x : ℝ} (hx : 0 < x) : Real.tanh x < x := by
  have hInt : IntervalIntegrable (fun t : ℝ => sechSq t) volume (0 : ℝ) x :=
    cont_sechSq.intervalIntegrable 0 x
  have htanh : ∫ t in (0 : ℝ)..x, sechSq t = Real.tanh x := by
    have hd : ∀ z ∈ Set.uIcc (0 : ℝ) x, HasDerivAt Real.tanh (sechSq z) z :=
      fun z _ => hasDerivAt_tanh z
    have h := intervalIntegral.integral_eq_sub_of_hasDerivAt hd hInt
    simpa using h
  have hpos : 0 < ∫ t in (0 : ℝ)..x, (1 - sechSq t) := by
    have hcont : Continuous fun t : ℝ => 1 - sechSq t :=
      continuous_const.sub cont_sechSq
    refine intervalIntegral.integral_pos hx hcont.continuousOn (fun t ht => ?_)
      ⟨x / 2, ⟨by linarith [hx], by linarith [hx]⟩, ?_⟩
    · have h1 : sechSq t ≤ 1 := sechSq_le_one t
      linarith
    · have hlt : sechSq (x / 2) < 1 := by
        have hxp : 0 < x / 2 := by linarith [hx]
        have hs : 0 < Real.sinh (x / 2) := Real.sinh_pos_iff.mpr hxp
        unfold sechSq
        rw [div_lt_one (pow_pos (Real.cosh_pos (x / 2)) 2)]
        have hc := Real.cosh_sq (x / 2)
        nlinarith [hs, hc]
      exact sub_pos.mpr hlt
  have hsplit : ∫ t in (0 : ℝ)..x, (1 - sechSq t) = x - ∫ t in (0 : ℝ)..x, sechSq t := by
    rw [intervalIntegral.integral_sub intervalIntegrable_const hInt]
    simp
  nlinarith [hpos, hsplit, htanh]

/-- $\sinh s/s$ 在 $(0,\infty)$ 上严格增（导数 $=\dfrac{s\cosh s-\sinh s}{s^2}>0\iff\tanh s<s$）。 -/
private lemma sinh_ratio_deriv {s : ℝ} (hs : 0 < s) :
    HasDerivAt (fun x : ℝ => Real.sinh x / x)
      ((Real.cosh s * s - Real.sinh s) / s ^ 2) s := by
  have h := (Real.hasDerivAt_sinh s).div (hasDerivAt_id s) (ne_of_gt hs)
  have hfun : (Real.sinh / id) = fun x : ℝ => Real.sinh x / x := by
    funext x; simp
  have hval : (Real.cosh s * id s - Real.sinh s * 1) / id s ^ 2
      = (Real.cosh s * s - Real.sinh s) / s ^ 2 := by
    simp
  rw [hfun, hval] at h
  exact h

private lemma sinh_ratio_strictMono :
    StrictMonoOn (fun x : ℝ => Real.sinh x / x) (Set.Ioi 0) := by
  have hcont : ContinuousOn (fun x : ℝ => Real.sinh x / x) (Set.Ioi 0) :=
    Real.continuous_sinh.continuousOn.div continuous_id.continuousOn
      (fun x hx => (show (0 : ℝ) < x from by simpa using hx).ne')
  refine strictMonoOn_of_hasDerivWithinAt_pos (D := Set.Ioi 0)
    (f := fun x : ℝ => Real.sinh x / x)
    (f' := fun s => (Real.cosh s * s - Real.sinh s) / s ^ 2) (convex_Ioi 0) hcont ?_ ?_
  · intro x hx
    have hx' : (0 : ℝ) < x := by simpa using hx
    exact (sinh_ratio_deriv hx').hasDerivWithinAt
  · intro x hx
    have hx' : (0 : ℝ) < x := by simpa using hx
    have hlt : Real.sinh x < x * Real.cosh x := by
      have ht : Real.tanh x < x := tanh_lt_self hx'
      have h2 : Real.sinh x / Real.cosh x < x := by
        rwa [Real.tanh_eq_sinh_div_cosh] at ht
      exact (div_lt_iff₀ (Real.cosh_pos x)).mp h2
    change 0 < (Real.cosh x * x - Real.sinh x) / x ^ 2
    exact div_pos (by linarith) (by positivity)

/-- 严格版：$s>0$、$0<u<1$ 时 $\sinh(us)<u\sinh s$。 -/
private lemma sinh_smul_lt {s u : ℝ} (hs : 0 < s) (hu0 : 0 < u) (hu1 : u < 1) :
    Real.sinh (u * s) < u * Real.sinh s := by
  have hus : (0 : ℝ) < u * s := mul_pos hu0 hs
  have hlt : u * s < s := by nlinarith [hu1, hs]
  have h := sinh_ratio_strictMono (show u * s ∈ Set.Ioi 0 from hus)
    (show s ∈ Set.Ioi 0 from hs) hlt
  have h2 : Real.sinh (u * s) / (u * s) < Real.sinh s / s := h
  have h3 : Real.sinh (u * s) < (Real.sinh s / s) * (u * s) := (div_lt_iff₀ hus).mp h2
  have h4 : (Real.sinh s / s) * (u * s) = u * Real.sinh s := by
    field_simp
  linarith [h3, h4]

/-- 非严格版：$u\le1$ 时 $\sinh(us)\le u\sinh s$。 -/
private lemma sinh_smul_le {s u : ℝ} (hs : 0 < s) (hu0 : 0 < u) (hu1 : u ≤ 1) :
    Real.sinh (u * s) ≤ u * Real.sinh s := by
  rcases lt_or_eq_of_le hu1 with hlt | heq
  · exact le_of_lt (sinh_smul_lt hs hu0 hlt)
  · rw [heq]
    norm_num

/-- 点位核心（严格）：$2\tanh V\,u^2\mathrm{sech}^2(uV)>2\mathrm{sech}^2V\,u\tanh(uV)$（$0<u<1$）。
两端通分到 $\cosh^2V\cosh^2(uV)$，比较 $u\sinh(2uV)$ 与 $u^2\sinh(2V)$，后者由 `sinh_smul_lt`。 -/
private lemma point_gt_core {V u : ℝ} (hV : 0 < V) (hu0 : 0 < u) (hu1 : u < 1) :
    2 * (1 / Real.cosh V ^ 2) * u * Real.tanh (u * V)
      < 2 * Real.tanh V * u ^ 2 * (1 / Real.cosh (u * V) ^ 2) := by
  have hD : 0 < Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2 :=
    mul_pos (pow_pos (Real.cosh_pos V) 2) (pow_pos (Real.cosh_pos (u * V)) 2)
  have hNA : 2 * (1 / Real.cosh V ^ 2) * u * Real.tanh (u * V)
      = u * Real.sinh (2 * (u * V)) / (Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2) := by
    rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_two_mul (x := u * V)]
    field_simp
    try ring
  have hNB : 2 * Real.tanh V * u ^ 2 * (1 / Real.cosh (u * V) ^ 2)
      = u ^ 2 * Real.sinh (2 * V) / (Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2) := by
    rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_two_mul (x := V)]
    field_simp
    try ring
  have hkey : Real.sinh (2 * (u * V)) < u * Real.sinh (2 * V) := by
    have h2 : 2 * (u * V) = u * (2 * V) := by ring
    rw [h2]
    exact sinh_smul_lt (by linarith : (0 : ℝ) < 2 * V) hu0 hu1
  have hnum : u * Real.sinh (2 * (u * V)) < u ^ 2 * Real.sinh (2 * V) := by
    have h := mul_lt_mul_of_pos_left hkey hu0
    calc u * Real.sinh (2 * (u * V)) < u * (u * Real.sinh (2 * V)) := h
      _ = u ^ 2 * Real.sinh (2 * V) := by ring
  rw [hNA, hNB, div_lt_iff₀ hD, div_mul_cancel₀ _ hD.ne']
  exact hnum

/-- 点位核心（非严格）：$u\le1$ 时 $\ge$。 -/
private lemma point_ge_core {V u : ℝ} (hV : 0 < V) (hu0 : 0 < u) (hu1 : u ≤ 1) :
    2 * (1 / Real.cosh V ^ 2) * u * Real.tanh (u * V)
      ≤ 2 * Real.tanh V * u ^ 2 * (1 / Real.cosh (u * V) ^ 2) := by
  have hD : 0 < Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2 :=
    mul_pos (pow_pos (Real.cosh_pos V) 2) (pow_pos (Real.cosh_pos (u * V)) 2)
  have hNA : 2 * (1 / Real.cosh V ^ 2) * u * Real.tanh (u * V)
      = u * Real.sinh (2 * (u * V)) / (Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2) := by
    rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_two_mul (x := u * V)]
    field_simp
    try ring
  have hNB : 2 * Real.tanh V * u ^ 2 * (1 / Real.cosh (u * V) ^ 2)
      = u ^ 2 * Real.sinh (2 * V) / (Real.cosh V ^ 2 * Real.cosh (u * V) ^ 2) := by
    rw [Real.tanh_eq_sinh_div_cosh, Real.sinh_two_mul (x := V)]
    field_simp
    try ring
  have hkey : Real.sinh (2 * (u * V)) ≤ u * Real.sinh (2 * V) := by
    have h2 : 2 * (u * V) = u * (2 * V) := by ring
    rw [h2]
    exact sinh_smul_le (by linarith : (0 : ℝ) < 2 * V) hu0 hu1
  have hnum : u * Real.sinh (2 * (u * V)) ≤ u ^ 2 * Real.sinh (2 * V) := by
    have h := mul_le_mul_of_nonneg_left hkey hu0.le
    calc u * Real.sinh (2 * (u * V)) ≤ u * (u * Real.sinh (2 * V)) := h
      _ = u ^ 2 * Real.sinh (2 * V) := by ring
  rw [hNA, hNB, div_le_iff₀ hD, div_mul_cancel₀ _ hD.ne']
  exact hnum

private lemma point_gt_T {T u : ℝ} (hT : 0 < T) (hu0 : 0 < u) (hu1 : u < 1) :
    2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T))
      < 2 * shapeH T * u ^ 2 * sechSq (u / (2 * T)) := by
  have hV : (0 : ℝ) < 1 / (2 * T) := by positivity
  have hv : u / (2 * T) = u * (1 / (2 * T)) := by field_simp
  unfold shapeH sechSq
  rw [hv]
  exact point_gt_core hV hu0 hu1

private lemma point_ge_T {T u : ℝ} (hT : 0 < T) (hu0 : 0 < u) (hu1 : u ≤ 1) :
    2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T))
      ≤ 2 * shapeH T * u ^ 2 * sechSq (u / (2 * T)) := by
  have hV : (0 : ℝ) < 1 / (2 * T) := by positivity
  have hv : u / (2 * T) = u * (1 / (2 * T)) := by field_simp
  unfold shapeH sechSq
  rw [hv]
  exact point_ge_core hV hu0 hu1

/-- **核不等式**：$\mathrm{sech}^2\frac1{2T}\,w<2T^2\tanh\frac1{2T}\,|w'|$。
两端即积分 $\int_0^1(2h\,u^2\mathrm{sech}^2\frac{u}{2T}-2S\,u\tanh\frac{u}{2T})$ 的展开，
被积函数在 $u\in(0,1)$ 上非负、在 $u=1/2$ 上严格正，故积分严格正。 -/
private lemma key_integral (T : ℝ) (hT : 0 < T) :
    0 < 2 * T ^ 2 * shapeH T * (-wGapDeriv T) - sechSq (1 / (2 * T)) * wGap T := by
  have hcontA : Continuous fun u : ℝ => 2 * shapeH T * u ^ 2 * sechSq (u / (2 * T)) :=
    ((continuous_const.mul (continuous_id.pow 2)).mul
      (cont_sechSq.comp (continuous_id.div_const (2 * T))))
  have hcontB : Continuous fun u : ℝ =>
      2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T)) :=
    ((continuous_const.mul continuous_id).mul
      (continuous_tanh.comp (continuous_id.div_const (2 * T))))
  have hpos : 0 < ∫ u in (0 : ℝ)..1,
      (2 * shapeH T * u ^ 2 * sechSq (u / (2 * T))
        - 2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T))) := by
    refine intervalIntegral.integral_pos (a := (0 : ℝ)) (b := 1) (by norm_num)
      (hcontA.sub hcontB).continuousOn
      (fun x hx => sub_nonneg.mpr (point_ge_T hT hx.1 hx.2))
      ⟨1 / 2, ⟨by norm_num, by norm_num⟩,
        sub_pos.mpr (point_gt_T hT (by norm_num) (by norm_num))⟩
  have hI : ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T)) = -T ^ 2 * wGapDeriv T := by
    unfold wGapDeriv
    field_simp
  have hA : ∫ u in (0 : ℝ)..1, 2 * shapeH T * u ^ 2 * sechSq (u / (2 * T))
      = 2 * shapeH T * (-T ^ 2 * wGapDeriv T) := by
    rw [show (fun u : ℝ => 2 * shapeH T * u ^ 2 * sechSq (u / (2 * T)))
        = fun u : ℝ => 2 * shapeH T * (u ^ 2 * sechSq (u / (2 * T))) from by
      funext u; ring]
    rw [intervalIntegral.integral_const_mul, hI]
  have hB : ∫ u in (0 : ℝ)..1, 2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T))
      = sechSq (1 / (2 * T)) * wGap T := by
    rw [show (fun u : ℝ => 2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T)))
        = fun u : ℝ => sechSq (1 / (2 * T)) * (2 * u * Real.tanh (u / (2 * T))) from by
      funext u; ring]
    rw [intervalIntegral.integral_const_mul]
    simp only [wGap]
  have hsub : ∫ u in (0 : ℝ)..1,
      (2 * shapeH T * u ^ 2 * sechSq (u / (2 * T))
        - 2 * sechSq (1 / (2 * T)) * u * Real.tanh (u / (2 * T)))
      = 2 * shapeH T * (-T ^ 2 * wGapDeriv T) - sechSq (1 / (2 * T)) * wGap T := by
    rw [intervalIntegral.integral_sub (hcontA.intervalIntegrable 0 1)
      (hcontB.intervalIntegrable 0 1), hA, hB]
  have hval : 2 * shapeH T * (-T ^ 2 * wGapDeriv T) - sechSq (1 / (2 * T)) * wGap T
      = 2 * T ^ 2 * shapeH T * (-wGapDeriv T) - sechSq (1 / (2 * T)) * wGap T := by ring
  rw [hsub, hval] at hpos
  exact hpos

private lemma shapeH_pos {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  have hV : (0 : ℝ) < 1 / (2 * T) := by positivity
  unfold shapeH
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hV) (Real.cosh_pos (1 / (2 * T)))

private lemma deficit_eq {T : ℝ} : deficitFrac T = 1 - wGap T / shapeH T := by
  unfold deficitFrac shapePhi shapeH
  rfl

private lemma deficit_pos {T : ℝ} (hT : 0 < T) : 0 < deficitFrac T := by
  have hlt : wGap T < shapeH T := CQM.Ring15.LockIbp.targetPropShapeEndGt T hT
  have hh : 0 < shapeH T := shapeH_pos hT
  have hq : wGap T / shapeH T < 1 := (div_lt_one hh).mpr hlt
  rw [deficit_eq]
  linarith

private lemma deficit_lt_one {T : ℝ} (hT : 0 < T) : deficitFrac T < 1 := by
  have hw : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT
  have hh : 0 < shapeH T := shapeH_pos hT
  have hq : 0 < wGap T / shapeH T := div_pos hw hh
  rw [deficit_eq]
  linarith

/-- $\tanh\frac1{2T}$ 对 $T$ 的导数：$\mathrm{sech}^2\frac1{2T}\cdot(-\frac1{2T^2})$。 -/
private lemma hasDerivAt_shapeH {T : ℝ} (hT : T ≠ 0) :
    HasDerivAt shapeH (-(sechSq (1 / (2 * T)) / (2 * T ^ 2))) T := by
  have hinv : HasDerivAt (fun T : ℝ => T⁻¹) (-(T ^ 2)⁻¹) T := hasDerivAt_inv hT
  have hmul := HasDerivAt.const_mul (1 / 2 : ℝ) hinv
  have hfun : (fun T : ℝ => (1 / 2) * T⁻¹) = fun T : ℝ => 1 / (2 * T) := by
    funext T; ring
  have hval : (1 / 2) * (-(T ^ 2)⁻¹) = -(1 / (2 * T ^ 2)) := by
    field_simp
  rw [hfun, hval] at hmul
  have hcomp := (hasDerivAt_tanh (1 / (2 * T))).comp T hmul
  have hval2 : sechSq (1 / (2 * T)) * (-(1 / (2 * T ^ 2)))
      = -(sechSq (1 / (2 * T)) / (2 * T ^ 2)) := by
    field_simp
  rw [hval2] at hcomp
  have hfun2 : (Real.tanh ∘ fun x : ℝ => 1 / (2 * x)) = shapeH := by
    funext x
    unfold shapeH
    rfl
  rw [hfun2] at hcomp
  exact hcomp

/-- **G-188b-2i-1 落地**：$\delta'$ 的闭式。 -/
private lemma hasDerivAt_deficit {T : ℝ} (hT : 0 < T) :
    HasDerivAt (fun T : ℝ => deficitFrac T) (deficitDeriv T) T := by
  have hTne : T ≠ 0 := ne_of_gt hT
  have hw : HasDerivAt wGap (wGapDeriv T) T :=
    CQM.Ring15.LockWD.targetPropWGapDeriv T hT
  have hh : HasDerivAt shapeH (-(sechSq (1 / (2 * T)) / (2 * T ^ 2))) T :=
    hasDerivAt_shapeH hTne
  have hhne : shapeH T ≠ 0 := (shapeH_pos hT).ne'
  have hq : HasDerivAt (fun T : ℝ => wGap T / shapeH T)
      ((wGapDeriv T * shapeH T
        - wGap T * (-(sechSq (1 / (2 * T)) / (2 * T ^ 2)))) / shapeH T ^ 2) T :=
    hw.div hh hhne
  have hraw := (hasDerivAt_const T (1 : ℝ)).add hq.neg
  have hfun : (fun T : ℝ => 1 + -(wGap T / shapeH T))
      =ᶠ[nhds T] (fun T : ℝ => deficitFrac T) :=
    Filter.Eventually.of_forall fun x => by
      change 1 + -(wGap x / shapeH x) = deficitFrac x
      rw [deficit_eq (T := x)]
      ring
  have hfin := hraw.congr_of_eventuallyEq hfun
  have hval : (0 + -((wGapDeriv T * shapeH T
        - wGap T * (-(sechSq (1 / (2 * T)) / (2 * T ^ 2)))) / shapeH T ^ 2))
      = deficitDeriv T := by
    have hh2 : shapeH T ^ 2 ≠ 0 := pow_ne_zero 2 hhne
    unfold deficitDeriv
    field_simp
    try ring
  rw [hval] at hfin
  exact hfin

theorem targetPropDeficitDeriv : CQM.Ring15.Spec.TargetPropDeficitDeriv := by
  intro T hT
  exact hasDerivAt_deficit hT

theorem targetPropDeficitDerivPos : CQM.Ring15.Spec.TargetPropDeficitDerivPos := by
  intro T hT
  have hkey := key_integral T hT
  have h2T : (0 : ℝ) < 2 * T ^ 2 := by positivity
  have hpos1 : wGap T * sechSq (1 / (2 * T)) / (2 * T ^ 2)
      < (-wGapDeriv T) * shapeH T := by
    rw [div_lt_iff₀ h2T]
    have hEq : (-wGapDeriv T) * shapeH T * (2 * T ^ 2)
        = 2 * T ^ 2 * shapeH T * (-wGapDeriv T) := by ring
    rw [hEq]
    linarith [hkey]
  have hnum : wGapDeriv T * shapeH T + wGap T * sechSq (1 / (2 * T)) / (2 * T ^ 2) < 0 := by
    linarith
  have hh : 0 < shapeH T ^ 2 := pow_pos (shapeH_pos hT) 2
  have hval : 0 < (-(wGapDeriv T * shapeH T
        + wGap T * sechSq (1 / (2 * T)) / (2 * T ^ 2))) / shapeH T ^ 2 :=
    div_pos (neg_pos.mpr hnum) hh
  unfold deficitDeriv
  exact hval

theorem targetPropDeficitStrictMono : CQM.Ring15.Spec.TargetPropDeficitStrictMono := by
  intro T₁ T₂ h1 h2
  have hdiff : DifferentiableOn ℝ (fun T : ℝ => deficitFrac T) (Set.Ioi 0) :=
    fun x hx => ((hasDerivAt_deficit (by simpa using hx)).differentiableAt).differentiableWithinAt
  have hcont : ContinuousOn (fun T : ℝ => deficitFrac T) (Set.Ioi 0) := hdiff.continuousOn
  have hderiv : ∀ x ∈ interior (Set.Ioi 0), 0 < deriv (fun T : ℝ => deficitFrac T) x := by
    intro x hx
    have hx' : (0 : ℝ) < x := by simpa using hx
    rw [(hasDerivAt_deficit hx').deriv]
    exact targetPropDeficitDerivPos x hx'
  have hmono := strictMonoOn_of_deriv_pos (f := fun T : ℝ => deficitFrac T)
    (convex_Ioi 0) hcont hderiv
  exact @hmono T₁ (show T₁ ∈ Set.Ioi (0 : ℝ) from by simpa using h1) T₂
    (show T₂ ∈ Set.Ioi (0 : ℝ) from by simpa using lt_trans h1 h2) h2

theorem targetPropDeficitRatioStrictMonoT :
    CQM.Ring15.Spec.TargetPropDeficitRatioStrictMonoT := by
  intro T₁ T₂ h1 h2
  have hm : deficitFrac T₁ < deficitFrac T₂ := targetPropDeficitStrictMono T₁ T₂ h1 h2
  have hp : 0 < deficitFrac T₁ := deficit_pos h1
  have hu : deficitFrac T₂ < 1 := deficit_lt_one (lt_trans h1 h2)
  exact CQM.Ring15.LockLambda.targetPropDeficitRatioMono _ _ hp hm hu

end

end CQM.Ring15.LockDeficitMono
