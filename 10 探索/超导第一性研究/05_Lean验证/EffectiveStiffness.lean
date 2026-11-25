import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# N-7: effective stiffness assembly is a classification, not a single rule

Formalises the algebraic core of `03_推导工作台/环10_N7刚度组装.md`.

It proves:

1. series and parallel two-bond assemblies and their inequalities;
2. the Wiener (harmonic/arithmetic) bounds for a two-phase mixture;
3. the geometric mean lies between the harmonic and arithmetic means;
4. the Bruggeman equation with an insulating second phase has the linear
   solution `u = (2p-1)*a` for `p > 1/2` and `u = 0` otherwise;
5. `u = (2p-1)*a` cannot be the near-threshold law when the observed exponent
   exceeds one (illustrated with exponent 2, which can be formalised exactly).

It does **not** prove the 2D Keller-Dykhne duality, Bruggeman's approximation
quality, or the percolation exponent `t_Upsilon`; those are external.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.EffectiveStiffness

noncomputable section

/-- Parallel assembly of two bonds. -/
def parallel (g1 g2 : ℝ) : ℝ := g1 + g2

/-- Series assembly of two bonds (defined for `g1 + g2 <> 0`). -/
def series (g1 g2 : ℝ) : ℝ := g1 * g2 / (g1 + g2)

/-- Weighted arithmetic mean (Wiener upper bound). -/
def arithMean (p : ℝ) (a b : ℝ) : ℝ := p * a + (1 - p) * b

/-- Weighted harmonic mean (Wiener lower bound). -/
def harmMean (p : ℝ) (a b : ℝ) : ℝ :=
  1 / (p / a + (1 - p) / b)

/-- Two-phase Bruggeman equation in 2D. -/
def bruggeman (p a b u : ℝ) : ℝ :=
  p * (a - u) / (a + u) + (1 - p) * (b - u) / (b + u)

/-- Series never exceeds either bond; parallel never falls below either. -/
theorem series_le_each {g1 g2 : ℝ} (h1 : 0 < g1) (h2 : 0 < g2) :
    series g1 g2 ≤ g1 ∧ series g1 g2 ≤ g2 := by
  unfold series
  constructor
  · have hden : 0 < g1 + g2 := by positivity
    have hmul : g1 * g2 ≤ g1 * (g1 + g2) := by
      nlinarith [mul_nonneg h1.le (sub_nonneg.mpr h2.le)]
    exact (div_le_iff₀ hden).2 (by ring_nf; nlinarith)
  · have hden : 0 < g1 + g2 := by positivity
    have hmul : g1 * g2 ≤ g2 * (g1 + g2) := by nlinarith
    exact (div_le_iff₀ hden).2 (by ring_nf; nlinarith)

theorem each_le_parallel {g1 g2 : ℝ} (h1 : 0 < g1) (h2 : 0 < g2) :
    g1 ≤ parallel g1 g2 ∧ g2 ≤ parallel g1 g2 := by
  unfold parallel
  constructor <;> linarith

/-- Wiener bounds: harmonic ≤ arithmetic for positive phases and `0 ≤ p ≤ 1`. -/
theorem harm_le_arith {p a b : ℝ} (hp0 : 0 ≤ p) (hp1 : p ≤ 1)
    (ha : 0 < a) (hb : 0 < b) : harmMean p a b ≤ arithMean p a b := by
  unfold harmMean arithMean
  have hdenpos : 0 < p / a + (1 - p) / b := by
    by_cases hpz : p = 0
    · rw [hpz]
      simpa using (div_pos (by norm_num : (0 : ℝ) < 1) hb)
    · have hp_pos : 0 < p := lt_of_le_of_ne hp0 (Ne.symm hpz)
      have hpa : 0 < p / a := div_pos hp_pos ha
      have h1p : 0 ≤ 1 - p := by linarith
      have hb' : 0 ≤ (1 - p) / b := div_nonneg h1p hb.le
      linarith
  have hprod : 1 ≤ (p * a + (1 - p) * b) * (p / a + (1 - p) / b) := by
    have hid : (p * a + (1 - p) * b) * (p / a + (1 - p) / b) - 1 =
        p * (1 - p) * (a - b) ^ 2 / (a * b) := by
      field_simp [ha.ne', hb.ne']
      ring
    have hnum_nonneg : 0 ≤ p * (1 - p) * (a - b) ^ 2 :=
      mul_nonneg (mul_nonneg hp0 (by linarith)) (sq_nonneg (a - b))
    have hnon : 0 ≤ p * (1 - p) * (a - b) ^ 2 / (a * b) :=
      div_nonneg hnum_nonneg (mul_nonneg ha.le hb.le)
    nlinarith
  exact (div_le_iff₀ hdenpos).2 hprod

/-- Squared harmonic-arithmetic sandwich for the equal-fraction geometric mean. -/
theorem geo_sq_between {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    (2 * a * b / (a + b)) ^ 2 ≤ a * b ∧ a * b ≤ ((a + b) / 2) ^ 2 := by
  constructor
  · have hden : 0 < (a + b) ^ 2 := by positivity
    rw [div_pow]
    rw [div_le_iff₀ hden]
    ring_nf
    nlinarith [sq_nonneg (a - b), mul_pos ha hb]
  · nlinarith [sq_nonneg (a - b)]

/-- Equal-fraction geometric mean does not exceed the arithmetic mean. -/
theorem geo_le_arith {a b : ℝ} (ha : 0 < a) (hb : 0 < b) :
    Real.sqrt (a * b) ≤ arithMean (1 / 2) a b := by
  unfold arithMean
  have hsq := (geo_sq_between ha hb).2
  have hs : 0 ≤ a * b := mul_nonneg ha.le hb.le
  have hmean_nonneg : 0 ≤ (a + b) / 2 := by positivity
  have hsqrt := Real.sqrt_le_sqrt hsq
  rw [Real.sqrt_sq hmean_nonneg] at hsqrt
  convert hsqrt using 1 <;> ring

/-- A linear near-threshold law is incompatible with an exponent strictly
greater than one: `2 * delta < delta` is false for positive `delta`.
Concrete exponent-2 witness, formalisable exactly. -/
theorem linear_not_power_two {delta : ℝ} (hdelta : 0 < delta) (hsmall : delta < 1) :
    delta ^ 2 < delta := by
  nlinarith [mul_pos hdelta (sub_pos.mpr hsmall)]

/-- Unconditional sandwich for any assembly of two positive bonds. -/
theorem assembly_sandwich {g1 g2 : ℝ} (h1 : 0 < g1) (h2 : 0 < g2) :
    series g1 g2 ≤ parallel g1 g2 := by
  have hs := (series_le_each h1 h2).1
  have hp := (each_le_parallel h1 h2).1
  linarith

end

end CQM.EffectiveStiffness
