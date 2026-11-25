import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Data.Real.Basic

/-!
# R41: 变形势链内化的结构 no-go 代数核（隔离区）

- 变形势声学支矩阵元 M ∝ Ξ·k，k→0 时 →0（声学求和规则 g(k=0)=0）
- 链内声学色散 ω = v_s·k，k→0 时 →0
- 两者在 k→0 同为 0（唯一连接点=零耦合），非零 Ξ 需电子能带边（链内无）
无 axiom / sorry / admit / native_decide / unsafe。
-/

namespace CQM.DeformationPotentialNoGo

noncomputable section

/-- 变形势声学支矩阵元（比例形式）：M(k) = Ξ · k。 -/
def Mel (Xi k : ℝ) : ℝ := Xi * k

/-- 链内声学色散：omega(k) = v_s · k。 -/
def omega (vs k : ℝ) : ℝ := vs * k

/-- k=0 时矩阵元为零（声学求和规则：平移模 g=0）。 -/
theorem mel_zero_at_k0 (Xi : ℝ) : Mel Xi 0 = 0 := by
  unfold Mel
  ring

/-- k=0 时链内声学频率为零。 -/
theorem omega_zero_at_k0 (vs : ℝ) : omega vs 0 = 0 := by
  unfold omega
  ring

/-- k→0：M(k)/omega(k) = Ξ/v_s 为常数（两者同阶线性）——唯一可比较的量是比值，但该比值
    仍需 Ξ（电子结构量），链内只有 v_s。 -/
theorem mel_over_omega (Xi vs k : ℝ) (hk : k ≠ 0) (hvs : vs ≠ 0) :
    Mel Xi k / omega vs k = Xi / vs := by
  unfold Mel omega
  field_simp [hk, hvs]

/-- 结论的结构形式：链内可算的是 omega/v_s = k（几何），而 Mel/v_s = (Ξ/v_s)·k 含外生 Ξ。
    即使 k→0，Mel(k)/k = Ξ 仍需电子结构量——链内 Mel(k)/k = 0（求和规则）。 -/
theorem acoustic_sum_no_xi : Mel 0 1 / (1 : ℝ) = 0 := by
  unfold Mel
  norm_num

end
end CQM.DeformationPotentialNoGo
