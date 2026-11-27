-- Ring15LockDeficitSq.lean（第 219 轮）：$\delta\le\frac13-\frac{9}{500T^2}$（$T\ge1$）。
-- 输入：217 的三阶界（$x-\frac{x^3}{3}\le\tanh x$）、218 的五阶界（$0\le s\le1$）。
-- 输出：$w$ 的多项式下界、$h$ 的多项式上界、比值下界、$\delta$ 的减平方界。
import Ring15Spec
import Ring15LockTanhTools
import Ring15LockTanhQuintic
import Ring15LockW
import Mathlib.Analysis.SpecialFunctions.Integrals.Basic

namespace CQM.Ring15.LockDeficitSq

open MeasureTheory
open scoped Interval
open CQM.Ring15.Spec
open CQM.Ring15.LockTanhTools
open CQM.Ring15.LockTanhQuintic

/-- $w$ 的多项式下界：$T>0$ 时 $\frac{1}{3T}-\frac{1}{60T^3}\le w(T)$。
路线：三阶界逐点 $x-\frac{x^3}{3}\le\tanh x$（$x=\frac{u}{2T}\ge0$），乘 $2u\ge0$ 后积分保序。 -/
theorem wGapLowerPoly (T : ℝ) (hT : 0 < T) :
    1 / (3 * T) - 1 / (60 * T ^ 3) ≤ wGap T := by
  have hcont : Continuous fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)) :=
    (continuous_const.mul continuous_id).mul
      (continuous_tanh.comp (continuous_id.div_const (2 * T)))
  have hcontP : Continuous fun u : ℝ => u ^ 2 / T - u ^ 4 / (12 * T ^ 3) :=
    ((continuous_id.pow 2).div_const T).sub ((continuous_id.pow 4).div_const (12 * T ^ 3))
  have hIntA : IntervalIntegrable (fun u : ℝ => u ^ 2 / T - u ^ 4 / (12 * T ^ 3))
      volume (0 : ℝ) 1 := hcontP.intervalIntegrable 0 1
  have hIntB : IntervalIntegrable (fun u : ℝ => 2 * u * Real.tanh (u / (2 * T)))
      volume (0 : ℝ) 1 := hcont.intervalIntegrable 0 1
  have hTne : T ≠ 0 := ne_of_gt hT
  have hmono : (∫ u in (0 : ℝ)..1, u ^ 2 / T - u ^ 4 / (12 * T ^ 3))
      ≤ ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T)) := by
    refine intervalIntegral.integral_mono_on zero_le_one hIntA hIntB ?_
    intro u hu
    have hu0 : 0 ≤ u := hu.1
    have hx0 : 0 ≤ u / (2 * T) := by positivity
    have hcub := targetPropTanhCubic (u / (2 * T)) hx0
    have hmul := mul_le_mul_of_nonneg_left hcub (by positivity : (0 : ℝ) ≤ 2 * u)
    have hpoly : 2 * u * (u / (2 * T) - (u / (2 * T)) ^ 3 / 3)
        = u ^ 2 / T - u ^ 4 / (12 * T ^ 3) := by
      field_simp
      ring
    rw [← hpoly]
    exact hmul
  have hint : (∫ u in (0 : ℝ)..1, u ^ 2 / T - u ^ 4 / (12 * T ^ 3))
      = 1 / (3 * T) - 1 / (60 * T ^ 3) := by
    have h2 : IntervalIntegrable (fun u : ℝ => u ^ 2 / T) volume (0 : ℝ) 1 :=
      ((continuous_id.pow 2).div_const T).intervalIntegrable 0 1
    have h4 : IntervalIntegrable (fun u : ℝ => u ^ 4 / (12 * T ^ 3)) volume (0 : ℝ) 1 :=
      ((continuous_id.pow 4).div_const (12 * T ^ 3)).intervalIntegrable 0 1
    rw [intervalIntegral.integral_sub h2 h4]
    have hq2 : (∫ u in (0 : ℝ)..1, u ^ 2 / T) = 1 / 3 / T := by
      rw [intervalIntegral.integral_div]
      have hq : (∫ u in (0 : ℝ)..1, u ^ 2) = 1 / 3 := by
        rw [integral_pow]; norm_num
      rw [hq]
    have hq4 : (∫ u in (0 : ℝ)..1, u ^ 4 / (12 * T ^ 3)) = 1 / 5 / (12 * T ^ 3) := by
      rw [intervalIntegral.integral_div]
      have hq : (∫ u in (0 : ℝ)..1, u ^ 4) = 1 / 5 := by
        rw [integral_pow]; norm_num
      rw [hq]
    rw [hq2, hq4]
    field_simp
    ring
  rw [hint] at hmono
  simpa [wGap] using hmono

/-- $h$ 的多项式上界：$T\ge1$ 时 $h(T)\le\frac{1}{2T}-\frac{1}{24T^3}+\frac{1}{240T^5}$。
由 218 的五阶界取 $s=\frac{1}{2T}$（$0\le s\le1$ 由 $T\ge1$ 给）。 -/
theorem shapeHUpperPoly (T : ℝ) (hT : 1 ≤ T) :
    shapeH T ≤ 1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5) := by
  have hT0 : 0 < T := by linarith
  have hTne : T ≠ 0 := ne_of_gt hT0
  have hs0 : 0 ≤ 1 / (2 * T) := by positivity
  have hs1 : 1 / (2 * T) ≤ 1 := by
    rw [div_le_iff₀ (by positivity : (0 : ℝ) < 2 * T)]
    nlinarith
  have hq := targetPropTanhQuintic (1 / (2 * T)) hs0 hs1
  have heq : 1 / (2 * T) - (1 / (2 * T)) ^ 3 / 3 + 2 * (1 / (2 * T)) ^ 5 / 15
      = 1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5) := by
    field_simp
    ring
  have hshape : shapeH T = Real.tanh (1 / (2 * T)) := rfl
  rw [hshape]
  exact le_trans hq (le_of_eq heq)

/-- 五阶上界式的正性（$T\ge1$）：$1.2\times10^2T^4-10T^2+1>0$。 -/
theorem hubNumPos (T : ℝ) (hT : 1 ≤ T) : 0 < 120 * T ^ 4 - 10 * T ^ 2 + 1 := by
  have h1 : 1 ≤ T ^ 2 := by nlinarith [hT]
  have h2 : T ^ 2 ≤ T ^ 4 := by nlinarith [h1, sq_nonneg T]
  nlinarith [h1, h2]

/-- 五阶上界式为正（$T\ge1$）：$h$ 的上界可作分母。 -/
theorem hubPos (T : ℝ) (hT : 1 ≤ T) :
    0 < 1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5) := by
  have hT0 : 0 < T := by linarith
  have hTne : T ≠ 0 := ne_of_gt hT0
  have heq : 1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5)
      = (120 * T ^ 4 - 10 * T ^ 2 + 1) / (240 * T ^ 5) := by
    field_simp
    ring
  rw [heq]
  exact div_pos (hubNumPos T hT) (by positivity)

/-- $w$ 的多项式下界为正（$T\ge1$）。 -/
theorem wlbPos (T : ℝ) (hT : 1 ≤ T) : 0 < 1 / (3 * T) - 1 / (60 * T ^ 3) := by
  have hT0 : 0 < T := by linarith
  have hTne : T ≠ 0 := ne_of_gt hT0
  have h1 : 1 ≤ T ^ 2 := by nlinarith [hT]
  have heq : 1 / (3 * T) - 1 / (60 * T ^ 3) = (20 * T ^ 2 - 1) / (60 * T ^ 3) := by
    field_simp
    ring
  rw [heq]
  exact div_pos (by nlinarith [h1]) (by positivity)

/-- **关键代数**：$T\ge1$ 时
$\frac{w_{\rm lb}}{h_{\rm ub}}\ge\frac23+\frac{9}{500T^2}$。
交叉相乘后即 $1.52T^4-1.46T^2-0.054\ge0$（$T=1$ 处余量 $0.006$）。 -/
theorem ratioLower (T : ℝ) (hT : 1 ≤ T) :
    2 / 3 + (9 : ℝ) / 500 / T ^ 2
      ≤ (1 / (3 * T) - 1 / (60 * T ^ 3)) / (1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5)) := by
  have hT0 : 0 < T := by linarith
  have hTne : T ≠ 0 := ne_of_gt hT0
  have h1 : 1 ≤ T ^ 2 := by nlinarith [hT]
  have h2 : 1 ≤ T ^ 4 := by nlinarith [h1, sq_nonneg (T ^ 2)]
  have hd := hubPos T hT
  have heqH : 1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5)
      = (120 * T ^ 4 - 10 * T ^ 2 + 1) / (240 * T ^ 5) := by
    field_simp
    ring
  have heqW : 1 / (3 * T) - 1 / (60 * T ^ 3) = (20 * T ^ 2 - 1) / (60 * T ^ 3) := by
    field_simp
    ring
  rw [le_div_iff₀ hd, heqH, heqW]
  rw [le_div_iff₀ (by positivity : (0 : ℝ) < 60 * T ^ 3)]
  field_simp
  nlinarith [h1, h2, hT]

/-- **本环主不等式**：$T\ge1$ 时 $\delta(T)\le\frac13-\frac{9}{500T^2}$。 -/
theorem deficitLeThirdSubSq (T : ℝ) (hT : 1 ≤ T) :
    deficitFrac T ≤ 1 / 3 - (9 : ℝ) / 500 / T ^ 2 := by
  have hT0 : 0 < T := by linarith
  have hw := wGapLowerPoly T hT0
  have hh := shapeHUpperPoly T hT
  have hhub := hubPos T hT
  have hwpos : 0 < wGap T := CQM.Ring15.LockW.targetPropWGapPos T hT0
  have hhpos : 0 < shapeH T := tanh_pos_of_pos (by positivity : (0 : ℝ) < 1 / (2 * T))
  have hratio : (1 / (3 * T) - 1 / (60 * T ^ 3)) / (1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5))
      ≤ wGap T / shapeH T := by
    rw [div_le_div_iff₀ hhub hhpos]
    have h1 : (1 / (3 * T) - 1 / (60 * T ^ 3)) * shapeH T ≤ wGap T * shapeH T :=
      mul_le_mul_of_nonneg_right hw (le_of_lt hhpos)
    have h2 : wGap T * shapeH T ≤ wGap T * (1 / (2 * T) - 1 / (24 * T ^ 3) + 1 / (240 * T ^ 5)) :=
      mul_le_mul_of_nonneg_left hh (le_of_lt hwpos)
    linarith
  have halg := ratioLower T hT
  have hphi : 2 / 3 + (9 : ℝ) / 500 / T ^ 2 ≤ shapePhi T := le_trans halg hratio
  unfold deficitFrac
  linarith

/-- **Spec 对齐版**（主定理名按目录规范）：`deficitLeThirdSubSq` 的命题形态。 -/
theorem targetPropDeficitLeThirdSubSq : CQM.Ring15.Spec.TargetPropDeficitLeThirdSubSq := by
  intro T hT
  exact deficitLeThirdSubSq T hT
