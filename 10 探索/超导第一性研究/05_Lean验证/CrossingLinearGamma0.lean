/-
  R28：真交叉 → 线性劈裂 → Γ₀ 的线性形状（系数外生）
  ============================================================
  链内已登记前提（06 L1332/L1336/L1350）：
    * 本征值交叉 λ2(Tc)=λ1(Tc)，拍频消失、相干时间发散；
    * 拍频 = λ_m - λ_n 决定退相干速率；
    * τ_dec ~ ħ/|λ_m-λ_n|（严格证明未闭合，按前提使用）；
    * Tc 以下退相干到最低分量 → 单一本征态 → 无拍频。
  外部（PRB 57 R11093）：Γ0(T)=a(T-Tc)，Γ0(Tc)=0。

  本文件承载：
    (1) 真交叉（两模可微、斜率不同）给劈裂严格线性于 T-Tc；
    (2) Tc 处劈裂为 0（与外部 Γ0(Tc)=0 相容）；
    (3) 避免交叉在 Tc 留有限间隙 2W>0，与 Γ0(Tc)=0 矛盾；
    (4) 斜率（比例系数）不由链内确定：不同斜率给不同系数。

  不证明：τ_dec 关系的严格证明（06 L1350 开放）；
          λ_n(T) 热修正显式（06 L1691 开放）；8/π 的链内来源（无）。
  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith

namespace CQM.CrossingLinearGamma0

noncomputable section

/-- (1) 两模在 $T_c$ 真交叉（同截距、不同斜率）⇒ 劈裂严格线性。 -/
theorem crossing_split_linear (c a1 a2 T Tc : ℝ) :
    (c + a2 * (T - Tc)) - (c + a1 * (T - Tc)) = (a2 - a1) * (T - Tc) := by
  ring

/-- (2) $T=T_c$ 处劈裂为零（拍频消失、相干时间发散）。 -/
theorem crossing_zero (c a1 a2 Tc : ℝ) :
    (c + a2 * (Tc - Tc)) - (c + a1 * (Tc - Tc)) = 0 := by ring

/-- (3) 避免交叉在 $T_c$ 处留有限间隙 $2W$。 -/
theorem avoided_gap_positive (c W : ℝ) (hW : 0 < W) :
    0 < (c + W) - (c - W) := by
  linarith

/-- (3′) no-go：若外部要求 $\\Gamma_0(T_c)=0$，避免交叉的有限间隙与之矛盾。 -/
theorem no_avoided_crossing (c W gamma0Tc : ℝ) (hW : 0 < W)
    (hgap : (c + W) - (c - W) = gamma0Tc) (hext : gamma0Tc = 0) : False := by
  have hpos : 0 < (c + W) - (c - W) := avoided_gap_positive c W hW
  linarith

/-- (4) 斜率外生：不同斜率给不同劈裂系数，链内无约束选哪一个。 -/
theorem slope_freedom (a1 a2 b1 b2 T Tc : ℝ) (h : a2 - a1 ≠ b2 - b1) (hT : T ≠ Tc) :
    (a2 - a1) * (T - Tc) ≠ (b2 - b1) * (T - Tc) := by
  intro heq
  have hdiff : T - Tc ≠ 0 := sub_ne_zero.mpr hT
  apply h
  exact mul_right_cancel₀ hdiff heq

end
end CQM.CrossingLinearGamma0
