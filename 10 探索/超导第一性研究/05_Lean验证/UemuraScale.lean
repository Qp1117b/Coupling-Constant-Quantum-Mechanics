import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith

/-!
# Uemura scale from the BKT jump and the percolation stiffness

Formalises the algebraic core of `03_推导工作台/目标区_Uemura标度.md`.

It does **not** prove:

* the Nelson–Kosterlitz universal jump itself;
* the identification `rho_s ~ Upsilon_bare` (external London relation);
* the Uemura / Homes experimental laws;
* the Kosterlitz RG, `Phi`, or the chi-square tail.

It proves only the algebra once those inputs are granted:

1. `uemura_identity`: the jump plus `Upsilon_R = g * Upsilon_bare` and
   `Upsilon_bare(T) = r * Upsilon_bare(0)` gives `Tc = pi * U0 * r * g / (2 kB)`;
2. `uemura_upper`: `r <= 1` and `g <= 1` give `Tc <= pi * U0 / (2 kB)`;
3. `uemura_linear_of_const_Q`, `uemura_strictMono_in_U0`: the linear branch;
4. `uemura_Q_le_one`, `uemura_Q_eq_one_iff`: the损耗因子 bounds and equality case;
5. `uemura_breakdown_witness`: two materials with different `Q` break global linearity;
6. `uemura_bounds_combine`: combine with the ring-19 upper bound.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.UemuraScale

noncomputable section

/-- The损耗 (loss) factor `Q = r * g`. -/
def lossFactor (r g : ℝ) : ℝ := r * g

/-- The Uemura temperature predicted by the identity, with `kB` kept explicit. -/
def uemuraTc (kB U0 r g : ℝ) : ℝ :=
  Real.pi * U0 * r * g / (2 * kB)

/-- The identity (U.1): granting the jump and the two factorisations, the critical
temperature equals the zero-temperature bare stiffness times the loss factor. -/
theorem uemura_identity {kB Tc U0 r g : ℝ} (hkB : kB ≠ 0)
    (hjump : 2 * kB * Tc = Real.pi * (g * (r * U0))) :
    Tc = Real.pi * U0 * r * g / (2 * kB) := by
  have h2 : 2 * kB ≠ 0 := mul_ne_zero (by norm_num) hkB
  field_simp [h2]
  ring_nf at hjump ⊢
  exact hjump

/-- `uemuraTc` is exactly the right-hand side of the identity. -/
theorem uemuraTc_eq (kB U0 r g : ℝ) :
    uemuraTc kB U0 r g = Real.pi * U0 * r * g / (2 * kB) := rfl

/-- The unconditional upper bound (U.3), first half: `r <= 1` and `g <= 1`. -/
theorem uemura_upper {kB Tc U0 r g : ℝ} (hkB : 0 < kB) (hU0 : 0 ≤ U0)
    (hr1 : r ≤ 1) (hg0 : 0 ≤ g) (hg1 : g ≤ 1)
    (hid : Tc = Real.pi * U0 * r * g / (2 * kB)) :
    Tc ≤ Real.pi * U0 / (2 * kB) := by
  have hrg : r * g ≤ 1 := by
    have h := mul_le_mul hr1 hg1 hg0 (by norm_num : (0 : ℝ) ≤ 1)
    simpa using h
  have hmul : Real.pi * U0 * (r * g) ≤ Real.pi * U0 * 1 :=
    mul_le_mul_of_nonneg_left hrg (mul_nonneg (le_of_lt Real.pi_pos) hU0)
  have hden : 0 < 2 * kB := by positivity
  rw [hid]
  have hdiv := div_le_div_of_nonneg_right hmul hden.le
  simpa [mul_assoc] using hdiv

/-- The loss factor never exceeds one. -/
theorem uemura_Q_le_one {r g : ℝ} (hr1 : r ≤ 1) (hg0 : 0 ≤ g) (hg1 : g ≤ 1) :
    lossFactor r g ≤ 1 := by
  have h := mul_le_mul hr1 hg1 hg0 (by norm_num : (0 : ℝ) ≤ 1)
  simpa [lossFactor] using h

/-- Equality of the loss factor to one forces both factors to one. -/
theorem uemura_Q_eq_one_iff {r g : ℝ} (hr0 : 0 ≤ r) (hr1 : r ≤ 1)
    (hg1 : g ≤ 1) :
    lossFactor r g = 1 ↔ r = 1 ∧ g = 1 := by
  constructor
  · intro h
    rw [lossFactor] at h
    have hr_eq : r = 1 := by
      by_contra hne
      have hrlt : r < 1 := lt_of_le_of_ne hr1 hne
      have hle : r * g ≤ r * 1 := mul_le_mul_of_nonneg_left hg1 hr0
      nlinarith [hle]
    have hg_eq : g = 1 := by
      rw [hr_eq] at h
      nlinarith
    exact ⟨hr_eq, hg_eq⟩
  · intro h
    rw [h.1, h.2]
    norm_num [lossFactor]

/-- The Uemura line: a constant loss factor gives exact linearity in `U0`. -/
theorem uemura_linear_of_const_Q (kB U0 Q : ℝ) :
    uemuraTc kB U0 1 Q = (Real.pi * Q / (2 * kB)) * U0 := by
  unfold uemuraTc
  ring

/-- With a fixed positive loss factor, the predicted `Tc` is strictly increasing
in the zero-temperature stiffness. -/
theorem uemura_strictMono_in_U0 {kB Q : ℝ} (hkB : 0 < kB) (hQ : 0 < Q) :
    StrictMono (fun U0 : ℝ => uemuraTc kB U0 1 Q) := by
  intro a b hab
  change uemuraTc kB a 1 Q < uemuraTc kB b 1 Q
  have hcoef : 0 < Real.pi * Q / (2 * kB) := by positivity
  have hrw : ∀ x : ℝ, uemuraTc kB x 1 Q = (Real.pi * Q / (2 * kB)) * x := by
    intro x
    unfold uemuraTc
    ring
  rw [hrw a, hrw b]
  exact mul_lt_mul_of_pos_left hab hcoef

/-- Global linearity fails: two materials with different loss factors have
different slopes `Tc / U0`.  Concrete witness: `Q = 1` versus `Q = 1/2`. -/
theorem uemura_breakdown_witness :
    ∃ U0a U0b Qa Qb : ℝ,
      U0a ≠ U0b ∧ 0 < Qa ∧ Qa ≤ 1 ∧ 0 < Qb ∧ Qb ≤ 1 ∧ Qa ≠ Qb ∧
      uemuraTc (1 : ℝ) U0a 1 Qa / U0a ≠ uemuraTc (1 : ℝ) U0b 1 Qb / U0b := by
  refine ⟨1, 2, 1, 1 / 2, by norm_num, by norm_num, by norm_num,
    by norm_num, by norm_num, by norm_num, ?_⟩
  unfold uemuraTc
  norm_num
  nlinarith [Real.pi_pos]

/-- Combine the stiffness upper bound with the ring-19 upper bound. -/
theorem uemura_bounds_combine {Tc Tstiff TBpair TBpure : ℝ}
    (hstiff : Tc ≤ Tstiff) (hB : Tc ≤ min TBpair TBpure) :
    Tc ≤ min Tstiff (min TBpair TBpure) :=
  le_min hstiff hB

/-- The slope of the linear branch is `pi / (2 kB)`. -/
theorem uemura_linear_slope {kB : ℝ} :
    Real.pi * 1 / (2 * kB) = Real.pi / (2 * kB) := by ring

end

end CQM.UemuraScale
