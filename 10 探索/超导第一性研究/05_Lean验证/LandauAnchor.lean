import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Bounds
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `审-11`: Landau coefficients of the phase sector, and the anchor

Formalises the algebraic core of `03_推导工作台/环19_审11_Landau系数与锚.md`.

The mean-field expansion of the phase free energy

  F_ph[θ] = - Σ_<ij> J_ij cos(θ_i - θ_j)

gives, with φ = <cos θ> and k_B T₀ = zJ/2,

  f(φ) = a(T) φ² + b(T) φ⁴ + O(φ⁶),

  a(T) = (zJ/2)(1 - T₀/T),   b(T) = (zJ)⁴ / (64 (k_B T)³).

Proved here:

1. `a(T) = 0 ↔ T = T₀`, with the correct signs on both sides (the anchor is the
   mean-field critical point, hence a branch point of `f`);
2. `b > 0` and `b(T₀) = zJ/8`;
3. the specific-heat jump `ΔC = 2 k_B` per site;
4. the dimensional-selectivity statement: the exponent `2 - d` vanishes iff `d = 2`,
   so a criterion of the form `Υ = (pure number) · k_B T` is dimensionally admissible
   only in two dimensions;
5. `T_c = c J / k_B` is homogeneous in `J`, so `T_c/J` and the mean-field ratio are
   `J`-independent;
6. the Ginzburg exponent `2d/(4-d)` is positive for `0 < d < 4`, and `r⁶ < r²`
   for `0 < r < 1` (the 3D critical region is narrower than the 2D one).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.LandauAnchor

/-- Mean-field quadratic coefficient of the phase sector. -/
noncomputable def aMF (zJ T0 T : ℝ) : ℝ := zJ / 2 * (1 - T0 / T)

/-- Mean-field quartic coefficient of the phase sector (per site). -/
noncomputable def bMF (zJ kB T : ℝ) : ℝ := zJ ^ 4 / (64 * (kB * T) ^ 3)

/-! ## 1. The quadratic coefficient and the anchor -/

/-- `a(T) = 0` exactly at the mean-field critical temperature `T₀`. -/
theorem aMF_zero_iff {zJ T0 T : ℝ} (hz : zJ ≠ 0) (hT : T ≠ 0) :
    aMF zJ T0 T = 0 ↔ T = T0 := by
  unfold aMF
  rw [mul_eq_zero]
  have hz2 : zJ / 2 ≠ 0 := div_ne_zero hz (by norm_num)
  constructor
  · rintro (h | h)
    · exact absurd h hz2
    · have h' : T0 / T = 1 := by linarith
      rw [div_eq_one_iff_eq hT] at h'
      exact h'.symm
  · intro h
    right
    subst h
    field_simp
    ring

/-- Below `T₀` the quadratic coefficient is negative (ordered side). -/
theorem aMF_neg {zJ T0 T : ℝ} (hz : 0 < zJ) (hT : 0 < T) (h : T < T0) :
    aMF zJ T0 T < 0 := by
  unfold aMF
  have h1 : 0 < zJ / 2 := by linarith
  have h2 : 1 - T0 / T < 0 := by
    have : 1 < T0 / T := (one_lt_div hT).mpr h
    linarith
  exact mul_neg_of_pos_of_neg h1 h2

/-- Above `T₀` the quadratic coefficient is positive (disordered side). -/
theorem aMF_pos {zJ T0 T : ℝ} (hz : 0 < zJ) (hT : 0 < T) (h : T0 < T) :
    0 < aMF zJ T0 T := by
  unfold aMF
  have h1 : 0 < zJ / 2 := by linarith
  have h2 : 0 < 1 - T0 / T := by
    have : T0 / T < 1 := (div_lt_one hT).mpr h
    linarith
  exact mul_pos h1 h2

/-! ## 2. The quartic coefficient -/

/-- The quartic coefficient is strictly positive. -/
theorem bMF_pos {zJ kB T : ℝ} (hz : zJ ≠ 0) (hkB : 0 < kB) (hT : 0 < T) :
    0 < bMF zJ kB T := by
  unfold bMF
  have hkT : 0 < kB * T := mul_pos hkB hT
  have hden : 0 < 64 * (kB * T) ^ 3 := by
    have : 0 < (kB * T) ^ 3 := pow_pos hkT 3
    linarith
  have hnum : 0 < zJ ^ 4 := by
    have h2 : 0 < zJ ^ 2 := by
      rw [sq]
      exact mul_self_pos.mpr hz
    have h4 : zJ ^ 4 = (zJ ^ 2) ^ 2 := by ring
    rw [h4, sq]
    exact mul_self_pos.mpr (ne_of_gt h2)
  exact div_pos hnum hden

/-- At the mean-field critical temperature the quartic coefficient equals `zJ/8`. -/
theorem bMF_at_T0 {zJ kB T0 : ℝ} (hz : zJ ≠ 0) (hkT0 : kB * T0 = zJ / 2) :
    bMF zJ kB T0 = zJ / 8 := by
  unfold bMF
  rw [hkT0]
  have h2 : zJ / 2 ≠ 0 := div_ne_zero hz (by norm_num)
  have h3 : (zJ / 2) ^ 3 ≠ 0 := pow_ne_zero 3 h2
  field_simp
  norm_num

/-- The mean-field critical temperature in terms of `zJ` and `k_B`. -/
theorem mf_tc {zJ kB T0 : ℝ} (hkB : kB ≠ 0) (hkT0 : kB * T0 = zJ / 2) :
    T0 = zJ / (2 * kB) := by
  have h : T0 = (zJ / 2) / kB := by
    rw [← hkT0]
    field_simp
  rw [h]
  field_simp

/-- The mean-field specific-heat jump is `2 k_B` per site (`a₀ = k_B`). -/
theorem deltaC_MF {zJ kB T0 : ℝ} (hz : zJ ≠ 0) (hkB : 0 < kB)
    (hkT0 : kB * T0 = zJ / 2) :
    T0 * kB ^ 2 / (2 * bMF zJ kB T0) = 2 * kB := by
  rw [bMF_at_T0 hz hkT0]
  have h2 : zJ / 8 ≠ 0 := div_ne_zero hz (by norm_num)
  field_simp
  nlinarith [hkT0]

/-! ## 3. Dimensional selectivity -/

/-- The stiffness exponent `2 - d` vanishes exactly in two dimensions, so only there
does `Υ/(k_B T)` carry no length scale. -/
theorem dim_selective (d : ℤ) : (2 - d = 0) ↔ d = 2 := by
  constructor <;> intro h <;> linarith

/-- In two dimensions the universal jump `Υ = (2/π) k_B T` is a pure number. -/
theorem bkt_ratio {ups kB T : ℝ} (hT : kB * T ≠ 0)
    (h : ups = 2 / Real.pi * (kB * T)) : ups / (kB * T) = 2 / Real.pi := by
  rw [h, mul_div_assoc, div_self hT, mul_one]

/-! ## 4. Energy-scale independence -/

/-- `T_c = c J / k_B` is homogeneous in `J`: a rescaling of `J` rescales `T_c`. -/
theorem tc_scale (c kB J lam : ℝ) (hkB : kB ≠ 0) :
    c * (lam * J) / kB = lam * (c * J / kB) := by
  field_simp

/-- The mean-field-to-exact ratio of `T_c` does not depend on `J`. -/
theorem ratio_J_indep {cMF cEx J kB : ℝ} (hJ : J ≠ 0) (hEx : cEx ≠ 0)
    (hkB : kB ≠ 0) : (cMF * J / kB) / (cEx * J / kB) = cMF / cEx := by
  have h : cEx * J ≠ 0 := mul_ne_zero hEx hJ
  field_simp

/-! ## 5. Ginzburg -/

/-- For `0 < d < 4` the Ginzburg exponent `2d/(4-d)` is positive. -/
theorem ginzburg_exp_pos {d : ℝ} (h0 : 0 < d) (h4 : d < 4) :
    0 < 2 * d / (4 - d) := by
  have h : 0 < 4 - d := by linarith
  positivity

/-- With `r = a/ξ₀ ∈ (0,1)`, the 3D Ginzburg region `r⁶` is narrower than the 2D one `r²`. -/
theorem ginzburg_d3_lt_d2 {r : ℝ} (h0 : 0 < r) (h1 : r < 1) : r ^ 6 < r ^ 2 := by
  have hr2 : r ^ 2 < 1 := by
    have h : 0 < (1 - r) * (1 + r) := mul_pos (by linarith) (by linarith)
    nlinarith
  have hr4 : r ^ 4 < 1 := by
    have h2 : 0 < r ^ 2 := pow_pos h0 2
    have h : 0 < (1 - r ^ 2) * (1 + r ^ 2) := mul_pos (by linarith) (by linarith)
    nlinarith
  have hm := mul_lt_mul_of_pos_left hr4 (pow_pos h0 2)
  nlinarith [hm]

end CQM.LandauAnchor
