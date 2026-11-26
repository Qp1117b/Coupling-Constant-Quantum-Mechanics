-- Ring15LockUnary.lean（第 201 轮）：$r$ 的 $\Phi$ 闭式与 $S'$ 判据的一元化（G-188b-2f）
-- 只 import Spec ＋ 上游证明模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockWD
import Ring15LockWD2
import Ring15LockWD3
import Ring15LockWD4
import Ring15LockIbp

namespace CQM.Ring15.LockUnary

open CQM.Ring15.Spec

noncomputable section

/-- $\tanh\frac{1}{2T}>0$（$T>0$）：端点核值正。 -/
private lemma tanhPos {T : ℝ} (hT : 0 < T) : 0 < Real.tanh (1 / (2 * T)) := by
  have hx : 0 < 1 / (2 * T) := by positivity
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos _)

/-- 勾股恒等式：$\mathrm{sech}^2x=1-\tanh^2x$。 -/
private lemma sechSq_eq_one_sub_tanh_sq (x : ℝ) : sechSq x = 1 - Real.tanh x ^ 2 := by
  unfold sechSq
  rw [Real.tanh_eq_sinh_div_cosh, div_pow]
  have hcs := Real.cosh_sq_sub_sinh_sq x
  have hc : Real.cosh x ^ 2 ≠ 0 := pow_ne_zero 2 (Real.cosh_pos x).ne'
  field_simp
  linarith

/-- 纯代数引理：$D>0$ 时 $\Phi\left(1+\frac ND\right)<2\frac ND\iff 0<N(2-\Phi)-\Phi D$
——两边同乘 $D$ 后整块移项，不改变任何量的语义。 -/
private lemma ratioCriterion {Φ N D : ℝ} (hD : 0 < D) :
    (Φ * (1 + N / D) < 2 * (N / D) ↔ 0 < N * (2 - Φ) - Φ * D) := by
  have hDne : D ≠ 0 := ne_of_gt hD
  have h₁ : Φ * (1 + N / D) * D = Φ * (D + N) := by
    field_simp
  have h₂ : 2 * (N / D) * D = 2 * N := by
    field_simp
  rw [← mul_lt_mul_iff_of_pos_right hD, h₁, h₂]
  constructor <;> intro h <;> nlinarith

/-- **G-188b-2f-1：$r$ 的 $\Phi$ 闭式**——$r=\dfrac{2Th(1-\Phi)}{1-h^2}$。
链内只用端点亏损（v24）与勾股恒等式，不引入新量。 -/
theorem targetPropRatioPhiForm : CQM.Ring15.Spec.TargetPropRatioPhiForm := by
  intro T hT
  have hEnd := CQM.Ring15.LockIbp.targetPropShapeEnd T hT
  have hhne : Real.tanh (1 / (2 * T)) ≠ 0 := (tanhPos hT).ne'
  -- $w=h\Phi$
  have hwΦ : wGap T = shapeH T * shapePhi T := by
    unfold shapeH shapePhi
    field_simp
  -- $\frac T2|w'|=h(1-\Phi)$
  have hp : (T / 2) * |wGapDeriv T| = shapeH T * (1 - shapePhi T) := by
    have h0 : (T / 2) * |wGapDeriv T| = shapeH T - wGap T := by
      unfold shapeH
      exact hEnd
    rw [hwΦ] at h0
    rw [h0]
    ring
  -- $T^2|w'|=2Th(1-\Phi)$
  have hT2 : T ^ 2 * |wGapDeriv T| = 2 * T * shapeH T * (1 - shapePhi T) := by
    nlinarith [hp]
  -- $\mathrm{sech}^2\frac{1}{2T}=1-h^2$
  have hS : sechSq (1 / (2 * T)) = 1 - shapeH T ^ 2 := by
    unfold shapeH
    exact sechSq_eq_one_sub_tanh_sq _
  unfold ratioR
  rw [hT2, hS]

/-- **G-188b-2f-2：判据一元化**——$S'(T)<0\iff 0<G(T)$，$G$ 只含 $\Phi$ 与 $h$。 -/
theorem targetPropShapeSignUnary : CQM.Ring15.Spec.TargetPropShapeSignUnary := by
  intro T hT
  have hratio := CQM.Ring15.LockWD4.targetPropShapeSignRatio T hT
  have hrPhi := targetPropRatioPhiForm T hT
  have hh : 0 < shapeH T := tanhPos hT
  have hh1 : shapeH T < 1 := by
    unfold shapeH
    exact Real.tanh_lt_one _
  have hD : 0 < 1 - shapeH T ^ 2 := by nlinarith
  rw [hratio, hrPhi]
  unfold shapeG
  exact ratioCriterion hD

end

end CQM.Ring15.LockUnary
