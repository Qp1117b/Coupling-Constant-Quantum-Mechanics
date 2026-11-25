-- Ring15LockThr.lean（第 187 轮）：配对阈值与粗粒化指数的两条写法等价
-- 只 import Spec（v14）；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockThr

open CQM.Ring15.Spec

noncomputable section

/-- $\ln p_{\rm pair}^{\rm thr}=\ln p_c-m\ln(1-y)$（$p_c>0$、$1-y>0$）。 -/
private lemma log_pPairThr (p y : ℝ) (m : ℕ) (hp : 0 < p) (hy : 0 < 1 - y) :
    Real.log (pPairThr p y m)
      = Real.log p - (m : ℝ) * Real.log (1 - y) := by
  unfold pPairThr
  have hpow : (0 : ℝ) < (1 - y) ^ m := pow_pos hy m
  rw [Real.log_div (ne_of_gt hp) (ne_of_gt hpow), Real.log_pow (1 - y) m]

/-- 等价（一）：$1+m\ln(1-y)/\ln p_{\rm pair}^{\rm thr}=\ln p_c/\ln p_{\rm pair}^{\rm thr}$。 -/
theorem targetPropThrLog : TargetPropThrLog := by
  intro p y m hp0 hp1 hy0 hy1 hm hceil
  have hy : (0 : ℝ) < 1 - y := by linarith
  have hpow : (0 : ℝ) < (1 - y) ^ m := pow_pos hy m
  have hpT : (0 : ℝ) < pPairThr p y m := div_pos hp0 hpow
  have hpT1 : pPairThr p y m < 1 := by
    unfold pPairThr
    rw [div_lt_one hpow]
    exact hceil
  have hlogT : Real.log (pPairThr p y m) < 0 := Real.log_neg hpT hpT1
  have hsub := log_pPairThr p y m hp0 hy
  have hden : Real.log p - (m : ℝ) * Real.log (1 - y) ≠ 0 := by
    rw [← hsub]
    exact ne_of_lt hlogT
  have hrewrite : tEffM (pPairThr p y m) y m
      = 1 + (m : ℝ) * Real.log (1 - y)
          / (Real.log p - (m : ℝ) * Real.log (1 - y)) := by
    unfold tEffM
    rw [hsub]
  rw [hrewrite, hsub]
  field_simp
  ring

/-- 等价（二）：$p_c^{1/t}=p_{\rm pair}^{\rm thr}$。 -/
theorem targetPropThrRpow : TargetPropThrRpow := by
  intro p y m hp0 hp1 hy0 hy1 hm hceil
  have hy : (0 : ℝ) < 1 - y := by linarith
  have hpow : (0 : ℝ) < (1 - y) ^ m := pow_pos hy m
  have hpT : (0 : ℝ) < pPairThr p y m := div_pos hp0 hpow
  have hpT1 : pPairThr p y m < 1 := by
    unfold pPairThr
    rw [div_lt_one hpow]
    exact hceil
  have hlogp : Real.log p < 0 := Real.log_neg hp0 hp1
  have hlogpne : Real.log p ≠ 0 := ne_of_lt hlogp
  have ht := targetPropThrLog p y m hp0 hp1 hy0 hy1 hm hceil
  have hlogT : Real.log (pPairThr p y m) < 0 := Real.log_neg hpT hpT1
  have htpos : (0 : ℝ) < tEffM (pPairThr p y m) y m := by
    have hneg : Real.log p / Real.log (pPairThr p y m)
        = (-Real.log p) / (-Real.log (pPairThr p y m)) := (neg_div_neg_eq _ _).symm
    rw [ht, hneg]
    exact div_pos (neg_pos.mpr hlogp) (neg_pos.mpr hlogT)
  have hinv : 1 / tEffM (pPairThr p y m) y m
      = Real.log (pPairThr p y m) / Real.log p := by
    rw [ht]
    field_simp
  calc p ^ (1 / tEffM (pPairThr p y m) y m)
      = Real.exp (Real.log p * (1 / tEffM (pPairThr p y m) y m)) :=
        Real.rpow_def_of_pos hp0 _
    _ = Real.exp (Real.log p * (Real.log (pPairThr p y m) / Real.log p)) := by rw [hinv]
    _ = Real.exp (Real.log (pPairThr p y m)) := by
        field_simp
    _ = pPairThr p y m := Real.exp_log hpT

end

end CQM.Ring15.LockThr
