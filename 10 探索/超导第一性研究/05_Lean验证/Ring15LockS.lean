-- Ring15LockS.lean（第 191 轮）：$s$ 的同名判否——可解性因子 $s_{\rm sol}=2/[C(a\lambda-r)]$
-- 正向取遍 $(0,\infty)$、在另一分支取负，故不是 $\frac12\mathbb Z$ 的表示权。
-- 只 import Ring15Spec（＋基线除法），不 import 任何证明模块。
import Ring15Spec

namespace CQM.Ring15.LockS

open CQM.Ring15.Spec

theorem targetPropSolSurj : CQM.Ring15.Spec.TargetPropSolSurj := by
  intro y hy
  have hyne : y ≠ 0 := ne_of_gt hy
  refine ⟨1, 2 / y, 0, one_pos, ?_, ?_, ?_⟩
  · exact div_pos two_pos hy
  · exact div_pos two_pos hy
  · show sOfLock 1 (2 / y) 0 = y
    unfold sOfLock
    field_simp
    ring

theorem targetPropSolNeg : CQM.Ring15.Spec.TargetPropSolNeg := by
  refine ⟨1, 0, 1, one_pos, by norm_num, ?_⟩
  show sOfLock 1 0 1 < 0
  unfold sOfLock
  norm_num

end CQM.Ring15.LockS
