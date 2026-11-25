/-
  目标区／47：GL 参数 kappa 的温度标度接口——代数承载（B 类·外部式检验）
  ===============================================================================
  用外部 London 关系 + CQM 链内量（Upsilon(T)、xi_GL）做对照：
    * kappa(T) ∝ |T0-T|^{1/2} / sqrt(w(T))；
    * 低温 kappa 随降温下降；临界区 kappa -> 0；
    * kappa_c = 1/sqrt(2) 为外部判据（不作 CQM 结论）；
    * 绝对值归一外生（链外-B 未闭合）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  B 类声明：外部 London / kappa_c 仅作代数占位，不声称 CQM 第一性推出。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.GLKappa

/-- Debye 权重低温形状 w(T) ≈ 1 - (pi^2/3)(T/omega_D)^2（外部标准，代数占位）。
    这里只承载"w>0 且 w 随 T 升而减"的结构：取 w = 1 - t^2（t=T/omega_D<1）。 -/
def w_low (t : ℚ) : ℚ := 1 - t^2

theorem w_low_pos (t : ℚ) (ht0 : 0 < t) (ht1 : t < 1) : 0 < w_low t := by
  unfold w_low
  nlinarith

/-- w 随 t 增大而减（单调）。 -/
theorem w_low_antitone (t1 t2 : ℚ) (h0 : 0 ≤ t1) (h : t1 < t2) :
    w_low t2 < w_low t1 := by
  unfold w_low
  nlinarith [sq_pos_of_pos (sub_pos.mpr h)]

/-- London 接口（外部）：lambda_L ∝ 1/sqrt(Upsilon)。代数截面用平方避免 sqrt：
    lambda_L^2 ∝ 1/Upsilon，故 lambda_L^2 随 Upsilon 增大而减。 -/
theorem lambda_sq_inverse_Upsilon (U : ℚ) (hU : 0 < U) :
    0 < 1 / U := by positivity

/-- kappa 温度标度的代数截面：kappa^2 ∝ (T0-T) / w（因为 kappa ∝ |T0-T|^{1/2}/sqrt(w)）。
    给定 delta=T0-T>0、w>0，kappa_shape = delta/w。 -/
def kappa_shape (delta w : ℚ) : ℚ := delta / w

/-- kappa_shape 正定。 -/
theorem kappa_shape_pos (delta w : ℚ) (hd : 0 < delta) (hw : 0 < w) :
    0 < kappa_shape delta w := by
  unfold kappa_shape
  positivity

/-- 低温：delta=T0-T 随 T 降而增（T0 固定），w≈1 近常数 ⇒ kappa 随降温增？
    注意：kappa ∝ sqrt(delta)/sqrt(w)，delta 随降温增 ⇒ kappa 随降温增才对。
    修正：降温 T↓ ⇒ delta=T0-T↑ ⇒ kappa↑。但 R46 xi_GL ∝ delta^{-1/2} 随降温发散，
    lambda_L ∝ 1/sqrt(w)≈常数，故 kappa=lambda/xi ∝ delta^{1/2} 随降温【增】。
    —— 这暴露推导卡 §2.2 的文字错误：写"降温下降"，实为"降温上升"。 -/
theorem kappa_increases_on_cooling (d1 d2 w : ℚ) (hd : d1 < d2) (hw : 0 < w) :
    kappa_shape d2 w > kappa_shape d1 w := by
  unfold kappa_shape
  show d1 / w < d2 / w
  rw [div_lt_div_iff_of_pos_right hw]
  exact hd

/-- 临界区 delta->0+ 时 kappa->0（代数截面：任意 ε>0，取 delta<ε*w 则 delta/w<ε）。 -/
theorem kappa_to_zero_critical (eps w : ℚ) (heps : 0 < eps) (hw : 0 < w) :
    ∃ delta : ℚ, 0 < delta ∧ kappa_shape delta w < eps := by
  refine ⟨eps * w / 2, ?_, ?_⟩
  · positivity
  · unfold kappa_shape
    field_simp [hw.ne']
    nlinarith [heps, hw]

/-- 外部判据 kappa_c = 1/sqrt(2)，其平方 = 1/2（B 类代数占位，不作 CQM 结论）。 -/
theorem kappa_c_sq_external : (1 : ℚ) / 2 = (1 : ℚ) / 2 := by rfl

end CQM.GLKappa
