-- Ring15LockDeficitUb.lean（第 215 轮）：δ′ 去 |w′| 的闭式与严格上界
-- 只 import Spec ＋已证模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockIbp
import Ring15LockW
import Ring15LockSecant
import Ring15LockDeficitMono

namespace CQM.Ring15.LockDeficitUb

open CQM.Ring15.Spec

noncomputable section

private lemma tanh_pos_of_pos {x : ℝ} (hx : 0 < x) : 0 < Real.tanh x := by
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos x)

private lemma sechSq_pos' (x : ℝ) : 0 < sechSq x := by
  unfold sechSq
  exact div_pos one_pos (pow_pos (Real.cosh_pos x) 2)

/-- $h=\tanh\frac1{2T}>0$。 -/
private lemma shapeH_pos' {T : ℝ} (hT : 0 < T) : 0 < shapeH T := by
  unfold shapeH
  exact tanh_pos_of_pos (by positivity)

/-- 归一形态下 $\tanh\frac1{2T}\ne 0$（供 `field_simp` 使用）。 -/
private lemma tanh_norm_ne {T : ℝ} (hT : 0 < T) : Real.tanh (T⁻¹ * (1 / 2)) ≠ 0 := by
  have h1 : T⁻¹ * (1 / 2 : ℝ) = 1 / (2 * T) := by field_simp
  rw [h1]
  exact (shapeH_pos' hT).ne'

/-- 由 197 的 $w=h+\frac T2w'$ 解出 $w'=\dfrac{2(w-h)}{T}$（$h=\tanh\frac1{2T}$）。 -/
private lemma wderiv_eq {T : ℝ} (hT : 0 < T) :
    wGapDeriv T = 2 * (wGap T - Real.tanh (1 / (2 * T))) / T := by
  have hIBP := CQM.Ring15.LockIbp.targetPropWGapIbp T hT
  rw [eq_div_iff hT.ne']
  nlinarith [hIBP]

/-- 闭式对齐：$\delta'=\dfrac{2(h-w)}{Th}-\dfrac{w\,\mathrm{sech}^2}{2T^2h^2}$。 -/
theorem targetPropDeficitDerivAlt : TargetPropDeficitDerivAlt := by
  intro T hT
  have hw' := wderiv_eq hT
  have htn := tanh_norm_ne hT
  have hTne : T ≠ 0 := hT.ne'
  unfold deficitDeriv deficitDerivAlt shapeH
  rw [hw']
  field_simp [htn, hTne]
  ring

/-- $2\delta/T$ 的分式形态与闭式首项一致。 -/
private lemma twoDelta_eq {T : ℝ} (hT : 0 < T) :
    2 * deficitFrac T / T = 2 * (shapeH T - wGap T) / (T * shapeH T) := by
  have hh : shapeH T ≠ 0 := (shapeH_pos' hT).ne'
  have hTne : T ≠ 0 := hT.ne'
  have htn := tanh_norm_ne hT
  have hkey : deficitFrac T = (shapeH T - wGap T) / shapeH T := by
    change 1 - wGap T / shapeH T = (shapeH T - wGap T) / shapeH T
    rw [one_sub_div hh]
  rw [hkey]
  field_simp [hh, hTne]

/-- $\delta'$ 的严格上界（一）：减项严格正 ⇒ $\delta'<\dfrac{2\delta}{T}$。 -/
theorem targetPropDeficitDerivLtTwoDelta : TargetPropDeficitDerivLtTwoDelta := by
  intro T hT
  have hh : 0 < shapeH T := shapeH_pos' hT
  have hw : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT
  have hsech : 0 < sechSq (1 / (2 * T)) := sechSq_pos' _
  have hden : 0 < 2 * T ^ 2 * shapeH T ^ 2 := by positivity
  have hpos : 0 < wGap T * sechSq (1 / (2 * T)) / (2 * T ^ 2 * shapeH T ^ 2) :=
    div_pos (mul_pos hw hsech) hden
  have hEq := targetPropDeficitDerivAlt T hT
  have hRHS := twoDelta_eq hT
  rw [hEq, hRHS]
  unfold deficitDerivAlt
  linarith

/-- $\delta'$ 的严格上界（二）：$\delta\le\frac13\Rightarrow\delta'<\dfrac{2}{3T}$。 -/
theorem targetPropDeficitDerivLtTwoThird : TargetPropDeficitDerivLtTwoThird := by
  intro T hT
  have hlt := targetPropDeficitDerivLtTwoDelta T hT
  have h3 := CQM.Ring15.LockSecant.targetPropDeficitLeThird T hT
  have hle : 2 * deficitFrac T / T ≤ 2 / (3 * T) := by
    rw [div_le_div_iff₀ hT (by positivity)]
    nlinarith [h3, hT]
  exact lt_of_lt_of_le hlt hle

end

end CQM.Ring15.LockDeficitUb
