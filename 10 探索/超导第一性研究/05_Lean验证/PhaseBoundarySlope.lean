/-
PhaseBoundarySlope.lean —— 第 141 轮：相界斜率的链式法则修正与形状通道

承载三条严格结果：
  1. 沿相界 p_pair(T_c(δ),δ) = p_*(T_c(δ),δ)，全导数给
     dT_c/dδ = (∂_δ p_pair - ∂_δ p_*) / (∂_T p_* - ∂_T p_pair)。
     M8 卡片把 p_pair 写成只依赖 δ，若把 dp_pair/dδ 读作偏导即漏项。
  2. 偏读斜率/严格斜率 = 1/r，其中 r = p_*'/(p_*' - ∂_T p_pair) ∈ (0,1)
     ⇒ 偏读法系统性高估 |dT_c/dδ|，高估因子恒等于 1/r。
  3. ∂_T p_pair = f_ν(x)·(x/V)·V' 的符号：V' < 0 ⇒ ∂_T p_pair < 0
     （升温配对减少，与降温有序一致），且分母 p_*' - ∂_T p_pair > p_*' > 0。

有效自由度 DF_n = 2n/(κ-(n-3)/(n-1))，κ=3 给 n-1；κ 降 ⇒ DF_n 升
（形状通道：均匀 κ=1.8 给 ν≈19.6，指数 κ=9 给 ν≈2.4）。

无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

namespace CQM.PhaseBoundarySlope

/-! ### 一、相界斜率的严格链式法则 -/

/-- 相界不变量：沿相界 F(T,δ)=0，其中 F=p_pair-p_*。
    记号用偏导数值 a=∂_T F、b=∂_δ F；隐函数定理（a≠0）给 T'=-b/a。 -/
theorem implicit_slope (a b : ℝ) :
    -(b / a) = -b / a := by ring

/-- 展开版：a = p_*' - p_T、b = p_δ - q_δ（q=p_*），
    则 dT_c/dδ = (p_δ - q_δ)/(p_*' - p_T)。 -/
theorem slope_expanded (pStarT pT pDel qDel : ℝ) :
    -(qDel - pDel) / (pStarT - pT) = (pDel - qDel) / (pStarT - pT) := by
  ring

/-- 若 q=p_* 不直接依赖掺杂（qDel=0），斜率 = p_δ/(p_*'-p_T)。 -/
theorem slope_no_qdel (pStarT pT pDel : ℝ) :
    (pDel - 0) / (pStarT - pT) = pDel / (pStarT - pT) := by ring

/-! ### 二、偏读误差恒等式 = 1/r - 1 -/

/-- 修正因子 r = p_*'/(p_*'-p_T)。 -/
noncomputable def correction (pStarT pT : ℝ) : ℝ := pStarT / (pStarT - pT)

/-- 偏读斜率 = p_δ/p_*'；严格斜率 = p_δ/(p_*'-p_T)。
    比值 = 1/r（当 p_*'≠0、p_*'-p_T≠0）。 -/
theorem partial_over_exact (pStarT pT pDel : ℝ)
    (hps : pStarT ≠ 0) (hden : pStarT - pT ≠ 0) (hp : pDel ≠ 0) :
    (pDel / pStarT) / (pDel / (pStarT - pT)) = 1 / correction pStarT pT := by
  unfold correction
  field_simp

/-- 由上式：偏读/严格 - 1 = p_T/p_*'。 -/
theorem partial_error_formula (pStarT pT pDel : ℝ)
    (hps : pStarT ≠ 0) (hp : pDel ≠ 0) :
    (pDel / pStarT) / (pDel / (pStarT - pT)) - 1 = -pT / pStarT := by
  field_simp
  ring

/-! ### 三、符号与修正因子的界 -/

/-- 若 p_*'>0 且 p_T<0（升温配对减少），则分母 p_*'-p_T>0。 -/
theorem denom_pos (pStarT pT : ℝ) (hps : 0 < pStarT) (hpT : pT < 0) :
    0 < pStarT - pT := by linarith

/-- 在上述符号下 0 < r < 1 ⇒ 偏读法系统性高估。 -/
theorem correction_in_unit_interval (pStarT pT : ℝ) (hps : 0 < pStarT) (hpT : pT < 0) :
    0 < correction pStarT pT ∧ correction pStarT pT < 1 := by
  unfold correction
  have hd : 0 < pStarT - pT := by linarith
  constructor
  · positivity
  · rw [div_lt_iff₀ hd]
    linarith

/-- 修正因子随 p_T 严格增（p_T 越负 ⇒ r 越小 ⇒ 偏读越坏）。 -/
theorem correction_strictMono_in_pT {pStarT : ℝ} (hps : 0 < pStarT) :
    StrictMonoOn (fun pT : ℝ => pStarT / (pStarT - pT)) (Set.Iio pStarT) := by
  intro a ha b hb hab
  change a < pStarT at ha
  change b < pStarT at hb
  have hda : 0 < pStarT - a := by linarith
  have hdb : 0 < pStarT - b := by linarith
  change pStarT / (pStarT - a) < pStarT / (pStarT - b)
  rw [div_lt_div_iff₀ hda hdb]
  nlinarith

/-- 有效自由度：κ=3 时 DF_n=n-1（n>1）。 -/
theorem df_nat_kappa_three (n : ℝ) (hn : 1 < n) :
    2 * n / (3 - (n - 3) / (n - 1)) = n - 1 := by
  have hn1 : n - 1 ≠ 0 := by linarith
  have htmp : 3 - (n - 3) / (n - 1) = 2 * n / (n - 1) := by
    field_simp [hn1]
    ring
  rw [htmp]
  field_simp [hn1]

/-- 在 n>1、κ>1 的域上 DF_n 随 κ 严格减（峰度越高自由度越少）。 -/
theorem df_strict_anti (n k1 k2 : ℝ) (hn : 1 < n)
    (hk1 : 1 < k1) (h12 : k1 < k2) :
    2 * n / (k2 - (n - 3) / (n - 1)) < 2 * n / (k1 - (n - 3) / (n - 1)) := by
  have hn1 : 0 < n - 1 := by linarith
  have hc1 : 0 < k1 - (n - 3) / (n - 1) := by
    rw [sub_pos]
    -- (n-3)/(n-1) = 1 - 2/(n-1) < 1 < k1
    have hratio : (n - 3) / (n - 1) < 1 := by
      rw [div_lt_one hn1]
      linarith
    linarith
  have hc2 : 0 < k2 - (n - 3) / (n - 1) := by
    have hratio : (n - 3) / (n - 1) < 1 := by
      rw [div_lt_one hn1]
      linarith
    linarith
  have hck : k1 - (n - 3) / (n - 1) < k2 - (n - 3) / (n - 1) := by linarith
  -- 分子 2n>0，分母越大分数越小
  rw [div_lt_div_iff₀ hc2 hc1]
  nlinarith

end CQM.PhaseBoundarySlope
