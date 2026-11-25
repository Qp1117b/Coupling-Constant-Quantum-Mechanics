/-
  R38：M2 谱形同形——Eliashberg 积分核的代数结构
  ============================================================
  外部标准：lambda=2∫alpha^2F/omega，ln omega_log 按 (alpha^2F/omega) 加权。
  链内 R38 取 alpha^2F=A*omega^s (0<omega<omega_D)。
  本文件只承载被积函数的代数恒等式与幅度 A 的可消性；
  连续积分结果由数值与 B 类标准承担。

  不证明：M2 识别、g/N(0) 的链内来源、任何缺口闭合。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

namespace CQM.PairingModeShape

noncomputable section

/-- (1) 声学幂律谱的 lambda 被积函数：$A\\omega^s/\\omega=A\\omega^{s-1}$（$s\\ge1$）。 -/
theorem integrand_power (A w : ℝ) (s : ℕ) (hw : w ≠ 0) :
    A * w ^ (s + 1) / w = A * w ^ s := by
  field_simp
  rw [pow_succ]
  ring

/-- (2) 对数矩的权重与幅度无关：$(A w)/(A W)=w/W$。 -/
theorem log_weight_amplitude_free (A w W : ℝ) (hA : A ≠ 0) (hW : W ≠ 0) :
    (A * w) / (A * W) = w / W := by
  field_simp

/-- (3) 幅度标度：谱乘 c 时 lambda 被积函数线性放大 c。 -/
theorem integrand_scale (A c w : ℝ) (s : ℕ) (hw : w ≠ 0) :
    (c * A) * w ^ (s + 1) / w = c * (A * w ^ (s + 1) / w) := by
  field_simp

end
end CQM.PairingModeShape
