-- Ring15LockWD4.lean（第 200 轮）：形状比与判据比——$S'$ 符号的比值判据（G-188b-2 第二步）
-- 只 import Spec ＋ 上游证明模块；无 sorry／admit／自造 axiom。
import Ring15Spec
import Ring15LockWD
import Ring15LockWD2
import Ring15LockWD3
import Ring15LockIbp

namespace CQM.Ring15.LockWD4

open CQM.Ring15.Spec

noncomputable section

/-- $\tanh\frac{1}{2T}>0$（$T>0$）：端点核值正。 -/
private lemma tanhPos {T : ℝ} (hT : 0 < T) : 0 < Real.tanh (1 / (2 * T)) := by
  have hx : 0 < 1 / (2 * T) := by positivity
  rw [Real.tanh_eq_sinh_div_cosh]
  exact div_pos (Real.sinh_pos_iff.mpr hx) (Real.cosh_pos _)

/-- $\mathrm{sech}^2\frac{1}{2T}>0$。 -/
private lemma sechSqPos (T : ℝ) : 0 < sechSq (1 / (2 * T)) := by
  unfold sechSq
  have h : 0 < Real.cosh (1 / (2 * T)) := Real.cosh_pos _
  positivity

/-- **链内恒等式（本轮核心）**：把"$w\,w''-(w')^2$"整块化成一个正因子乘以一个无量纲差：
$w\,w''-(w')^2=\dfrac{\tanh\frac{1}{2T}\,\mathrm{sech}^2\frac{1}{2T}}{T^3}\bigl(\Phi(1+r)-2r\bigr)$。
来源只有三条已证关系：端点闭式（v26）、分部积分恒等式与端点亏损（v24）、$w'<0$（v23）。 -/
private lemma wSub (T : ℝ) (hT : 0 < T) :
    wGap T * wGapDeriv2 T - wGapDeriv T ^ 2
      = (Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) / T ^ 3)
          * (shapePhi T * (1 + ratioR T) - 2 * ratioR T) := by
  have hAlt := CQM.Ring15.LockWD3.targetPropWGapDeriv2Alt T hT
  have hIbp := CQM.Ring15.LockIbp.targetPropWGapIbp T hT
  have hEnd := CQM.Ring15.LockIbp.targetPropShapeEnd T hT
  have hNeg := CQM.Ring15.LockWD.targetPropWGapDerivNeg T hT
  have hh : Real.tanh (1 / (2 * T)) ≠ 0 := (tanhPos hT).ne'
  have hS : sechSq (1 / (2 * T)) ≠ 0 := (sechSqPos T).ne'
  have hTne : T ≠ 0 := ne_of_gt hT
  set a := |wGapDeriv T| with ha
  -- $a=-w'$
  have hw' : wGapDeriv T = -a := by
    have h1 : a = -wGapDeriv T := by
      rw [ha]
      exact abs_of_neg hNeg
    linarith
  -- $w=h\Phi$
  have hwΦ : wGap T = Real.tanh (1 / (2 * T)) * shapePhi T := by
    unfold shapePhi
    field_simp
  -- $a=2h(1-\Phi)/T$
  have haT : a = 2 * Real.tanh (1 / (2 * T)) * (1 - shapePhi T) / T := by
    have hp : (T / 2) * a = Real.tanh (1 / (2 * T)) * (1 - shapePhi T) := by
      have h0 : (T / 2) * a = Real.tanh (1 / (2 * T)) - wGap T := hEnd
      rw [hwΦ] at h0
      rw [h0]
      ring
    field_simp
    nlinarith [hp]
  -- $r S=T^2a$
  have hrS : ratioR T * sechSq (1 / (2 * T)) = T ^ 2 * a := by
    unfold ratioR
    rw [ha]
    exact div_mul_cancel₀ _ hS
  rw [hAlt]
  unfold wGapDeriv2Alt
  rw [hw', hwΦ, haT]
  unfold ratioR
  rw [← ha]
  rw [haT]
  field_simp
  ring

/-- **G-188b-2d：比值判据**——$S'(T)<0\iff\Phi(T)(1+r(T))<2r(T)$（$T>0$）。 -/
theorem targetPropShapeSignRatio : CQM.Ring15.Spec.TargetPropShapeSignRatio := by
  intro T hT
  have hid := wSub T hT
  have hsign := CQM.Ring15.LockWD3.targetPropShapeDerivSign T hT
  have hpos : 0 < Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) / T ^ 3 := by
    have h1 : 0 < Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) :=
      mul_pos (tanhPos hT) (sechSqPos T)
    exact div_pos h1 (by positivity)
  constructor
  · intro hneg
    have h1 : wGap T * wGapDeriv2 T - wGapDeriv T ^ 2 < 0 := by
      have := hsign.mp hneg
      linarith
    have h2 : (Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) / T ^ 3)
        * (shapePhi T * (1 + ratioR T) - 2 * ratioR T) < 0 := by
      linarith [h1, hid]
    by_contra hc
    push Not at hc
    have h4 : 0 ≤ shapePhi T * (1 + ratioR T) - 2 * ratioR T := by linarith
    have h3 : 0 ≤ (Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) / T ^ 3)
        * (shapePhi T * (1 + ratioR T) - 2 * ratioR T) :=
      mul_nonneg (le_of_lt hpos) h4
    linarith
  · intro hlt
    have h1 : wGap T * wGapDeriv2 T - wGapDeriv T ^ 2 < 0 := by
      have h2 : (Real.tanh (1 / (2 * T)) * sechSq (1 / (2 * T)) / T ^ 3)
          * (shapePhi T * (1 + ratioR T) - 2 * ratioR T) < 0 :=
        mul_neg_of_pos_of_neg hpos (by linarith)
      linarith [h2, hid]
    exact hsign.mpr (by linarith)

/-- **G-188b-2e：$r\ge1$ 段的符号定理**——$1\le r(T)\Rightarrow S'(T)<0$（即 $w''\le0$ 段形状项必降）。 -/
theorem targetPropShapeNegOfRatioGeOne : CQM.Ring15.Spec.TargetPropShapeNegOfRatioGeOne := by
  intro T hT hr
  have hsign := targetPropShapeSignRatio T hT
  apply hsign.mpr
  have hlt1 : shapePhi T < 1 := by
    unfold shapePhi
    rw [div_lt_one (tanhPos hT)]
    exact CQM.Ring15.LockIbp.targetPropShapeEndGt T hT
  have hpos2 : (0 : ℝ) < 1 + ratioR T := by linarith
  have h1 : shapePhi T * (1 + ratioR T) < 1 * (1 + ratioR T) :=
    mul_lt_mul_of_pos_right hlt1 hpos2
  nlinarith

end

end CQM.Ring15.LockWD4
