/-
  第90轮补（成果登记 R-99）：审-4 关联修正的座→键映射与阈值位移
  ================================================================
  承接 G1-G3 高斯场工作假设与第84轮关联 rho（(9.1)、Bessel 核）。
  本文件用线性近似 cbar(rho)=rho/(2π)（阈值取均值精确式 arcsin(rho)/(2π)
  的 rho→0 首阶，且 arcsin(rho)>=rho 故它是精确 cbar 的下界）承载纯代数骨架：

    * cbar(0)=0、cbar>=0、对 rho 单增；
    * 诱导键密度 q=p²+cbar >= p²（修正独立映射）；
    * 阈值位移 p* = sqrt(pc²-cbar) <= pc，且一阶界 sqrt(pc²-c) <= pc-c/(2pc)；
    * 自平均条件 cbar=o(1/n) 的代数骨架：cbar/n <= cbar。

  外部依据（只作工具，不写成 CQM=渗流模型）：
    Plackett(1954) 恒等式 d(cbar)/d rho = phi_2 > 0；
    arXiv:1305.6941 / 1708.02296：正关联降低 2D 座渗流阈值。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Linarith
import Mathlib.Order.Basic

open scoped BigOperators

namespace CQM.CorrelatedSiteBond

noncomputable section

/-- 小关联首阶：$\bar c(\rho)=\rho/(2\pi)$（精确式为 $\arcsin\rho/(2\pi)\ge$ 此值）。 -/
def cbar (rho : ℝ) : ℝ := rho / (2 * Real.pi)

lemma cbar_zero : cbar 0 = 0 := by
  unfold cbar
  ring

lemma cbar_nonneg {rho : ℝ} (h : 0 ≤ rho) : 0 ≤ cbar rho := by
  unfold cbar
  positivity

lemma cbar_pos {rho : ℝ} (h : 0 < rho) : 0 < cbar rho := by
  unfold cbar
  positivity

lemma cbar_mono {r1 r2 : ℝ} (h : r1 ≤ r2) : cbar r1 ≤ cbar r2 := by
  unfold cbar
  have hden : 0 ≤ 2 * Real.pi := by positivity
  exact div_le_div_of_nonneg_right h hden

/-! ### 一、诱导键密度修正 -/

/-- 诱导键密度 $q=p^2+\bar c\ge p^2$（正关联上移）。 -/
lemma bond_density_ge (p rho : ℝ) (h : 0 ≤ rho) :
    p ^ 2 ≤ p ^ 2 + cbar rho := by
  have hc := cbar_nonneg h
  nlinarith

/-- 严格上移（$\rho>0$ 且 $p>0$ 时 $q>p^2$ 当 $\bar c>0$）。 -/
lemma bond_density_strict (p rho : ℝ) (hr : 0 < rho) :
    p ^ 2 < p ^ 2 + cbar rho := by
  have hc := cbar_pos hr
  linarith

/-! ### 二、阈值位移 -/

/-- 关联下阈值 $p_*=\sqrt{p_c^2-\bar c}\le p_c$。 -/
lemma pstar_le_pc (pc c : ℝ) (hpc : 0 < pc) (hc0 : 0 ≤ c) :
    Real.sqrt (pc ^ 2 - c) ≤ pc := by
  rw [Real.sqrt_le_iff]
  constructor
  · exact hpc.le
  · nlinarith

/-- 阈值非负（被开方数非负时）。 -/
lemma pstar_nonneg (pc c : ℝ) :
    0 ≤ Real.sqrt (pc ^ 2 - c) := Real.sqrt_nonneg _

/-- 一阶位移界：$\sqrt{p_c^2-c}\le p_c-\frac{c}{2p_c}$（凹性）。 -/
lemma pstar_first_order_bound (pc c : ℝ) (hpc : 0 < pc) (hcup : c ≤ pc ^ 2) :
    Real.sqrt (pc ^ 2 - c) ≤ pc - c / (2 * pc) := by
  have hy : 0 ≤ pc - c / (2 * pc) := by
    have hden : 0 < 2 * pc := by positivity
    rw [sub_nonneg]
    rw [div_le_iff₀ hden]
    nlinarith
  rw [Real.sqrt_le_iff]
  constructor
  · exact hy
  · field_simp [hpc.ne']
    nlinarith [sq_nonneg c]

/-- 一阶位移系数严格负（正关联降阈值）。 -/
lemma shift_negative (pc phi : ℝ) (hpc : 0 < pc) (hphi : 0 < phi) :
    -(phi / (2 * pc)) < 0 := by
  have hpos : 0 < phi / (2 * pc) := by positivity
  linarith

/-! ### 三、自平均拉通 -/

/-- 自平均条件 $\bar c=o(1/n)$ 的代数骨架：$c/n\le c$（$n\ge1$）。 -/
lemma cbar_over_n_le (c : ℝ) (hc : 0 ≤ c) {n : ℕ} (hn : 1 ≤ n) :
    c / (n : ℝ) ≤ c := by
  have hnpos : 0 < (n : ℝ) := by exact_mod_cast (lt_of_lt_of_le Nat.zero_lt_one hn)
  rw [div_le_iff₀ hnpos]
  have hn1 : (1 : ℝ) ≤ n := by exact_mod_cast hn
  nlinarith

lemma cbar_over_n_nonneg (c : ℝ) (hc : 0 ≤ c) (n : ℕ) :
    0 ≤ c / (n : ℝ) := by
  have hnnonneg : 0 ≤ (n : ℝ) := by exact_mod_cast Nat.zero_le n
  exact div_nonneg hc hnnonneg

end
end CQM.CorrelatedSiteBond
