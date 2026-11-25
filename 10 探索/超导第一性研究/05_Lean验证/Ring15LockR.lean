-- Ring15LockR.lean（第 188 轮）：epsilon_nu -> r 的反比结构与失效面判据
-- 只 import Spec（v15）；无 sorry／admit／自造 axiom。
import Ring15Spec

namespace CQM.Ring15.LockR

open CQM.Ring15.Spec

noncomputable section

/-- $r=\dfrac{k}{\epsilon_\nu}$，$k=\dfrac{2\alpha_Vw}{3|w'|}$。 -/
private lemma rOfW_eq (aV w w' e : ℝ) (hw' : w' ≠ 0) (he : e ≠ 0) :
    rOfW aV w w' e = (2 * aV * w / (3 * |w'|)) / e := by
  unfold rOfW
  field_simp

theorem targetPropROfEps : TargetPropROfEps := by
  intro aV w w' e1 e2 hA hw hw' h1 h12
  have habs : (0 : ℝ) < |w'| := abs_pos.mpr hw'
  have hk : (0 : ℝ) < 2 * aV * w / (3 * |w'|) := by
    apply div_pos
    · nlinarith
    · nlinarith
  have he2 : (0 : ℝ) < e2 := lt_trans h1 h12
  have he1ne : e1 ≠ 0 := ne_of_gt h1
  have he2ne : e2 ≠ 0 := ne_of_gt he2
  have hkey : (2 * aV * w / (3 * |w'|)) / e2 < (2 * aV * w / (3 * |w'|)) / e1 := by
    rw [div_lt_div_iff₀ he2 h1]
    exact mul_lt_mul_of_pos_left h12 hk
  rw [rOfW_eq aV w w' e2 hw' he2ne, rOfW_eq aV w w' e1 hw' he1ne]
  exact hkey

theorem targetPropSFail : TargetPropSFail := by
  intro C1 aLam r hC
  have hnum : (0 : ℝ) < 2 := by norm_num
  constructor
  · intro h
    have hprod : (0 : ℝ) < C1 * (aLam - r) := by
      rcases (div_pos_iff).mp h with hp | hp
      · exact hp.2
      · linarith [hp.1]
    have hd : (0 : ℝ) < aLam - r := by
      by_contra hle
      have hle' : aLam - r ≤ 0 := not_lt.mp hle
      have : C1 * (aLam - r) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos (le_of_lt hC) hle'
      linarith
    linarith
  · intro h
    have hd : (0 : ℝ) < aLam - r := by linarith
    exact (div_pos_iff).mpr (Or.inl ⟨hnum, mul_pos hC hd⟩)

end

end CQM.Ring15.LockR
