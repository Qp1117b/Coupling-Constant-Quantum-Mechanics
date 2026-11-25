import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `临-9`: weakening the premise of Lemma A

Lemma A (main chain (21.1)): e^{i gamma_n H}=1 for all n implies H=0, provided
some pair gamma_n/gamma_n' is irrational.  We weaken the premise: it suffices
that the (reduced) denominators q_n of gamma_n/gamma_1 are unbounded, proved by
pure integer divisibility.  Bounded denominators force a lattice structure,
whose linear capacity contradicts the superlinear Riemann-von Mangoldt count
(conditional on bounded multiplicity per ordinate).

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.LemmaAPremise

/-- Original Lemma A: an irrational ratio kills c. -/
theorem pair_ratio_irrational_zero {c gamma gamma' : ℝ} {m m' : ℤ}
    (hg' : gamma' ≠ 0)
    (hm : c * gamma = (m : ℝ)) (hm' : c * gamma' = (m' : ℝ))
    (hirr : gamma / gamma' ∉ Set.range (fun q : ℚ => (q : ℝ))) : c = 0 := by
  by_contra hc
  have hm_ne : m' ≠ 0 := by
    intro hz
    have hzero : c * gamma' = 0 := by simpa [hz] using hm'
    have hcg : c = 0 ∨ gamma' = 0 := mul_eq_zero.mp hzero
    rcases hcg with hc0 | hg0
    · exact hc hc0
    · exact hg' hg0
  have hdiv : (c * gamma) / (c * gamma') = (m : ℝ) / (m' : ℝ) := by rw [hm, hm']
  have hcancel : (c * gamma) / (c * gamma') = gamma / gamma' := by
    field_simp [hc, hg']
  have hratio : gamma / gamma' = (m : ℝ) / (m' : ℝ) := by rw [← hcancel, hdiv]
  apply hirr
  refine ⟨(m : ℚ) / (m' : ℚ), ?_⟩
  rw [hratio]
  norm_num

/-- Unbounded divisors of a natural number force it to be zero. -/
theorem unbounded_dvd_only_zero_nat (K : ℕ)
    (h : ∀ Q : ℕ, ∃ q : ℕ, Q < q ∧ q ∣ K) : K = 0 := by
  by_contra hK
  obtain ⟨q, hq, hdiv⟩ := h K
  have hKpos : 0 < K := Nat.pos_of_ne_zero hK
  have hqle : q ≤ K := Nat.le_of_dvd hKpos hdiv
  exact (not_lt_of_ge hqle hq).elim

/-- Weakened Lemma A: unbounded denominators q_n | k force k = 0. -/
theorem denom_unbounded_zero (k : ℤ)
    (h : ∀ Q : ℕ, ∃ q : ℕ, Q < q ∧ (q : ℤ) ∣ k) : k = 0 := by
  have hnat : ∀ Q : ℕ, ∃ q : ℕ, Q < q ∧ q ∣ k.natAbs := by
    intro Q
    obtain ⟨q, hq, hdiv⟩ := h Q
    refine ⟨q, hq, ?_⟩
    have hn : (q : ℤ).natAbs ∣ k.natAbs := Int.natAbs_dvd_natAbs.mpr hdiv
    simpa using hn
  have hkabs : k.natAbs = 0 := unbounded_dvd_only_zero_nat k.natAbs hnat
  exact Int.natAbs_eq_zero.mp hkabs

/-- Bounded denominators give a lattice structure: gamma in (gamma1/Q) Z. -/
theorem bounded_denom_lattice (gamma gamma1 : ℝ) (Q : ℕ) (hQ : 0 < Q)
    (p : ℤ) (hp : (Q : ℝ) * gamma = (p : ℝ) * gamma1) :
    ∃ z : ℤ, gamma = (z : ℝ) * (gamma1 / Q) := by
  refine ⟨p, ?_⟩
  have hQr : (Q : ℝ) ≠ 0 := by exact_mod_cast (ne_of_gt hQ)
  rw [show (p : ℝ) * (gamma1 / Q) = ((p : ℝ) * gamma1) / Q by ring]
  rw [← hp]
  field_simp [hQr]

end CQM.LemmaAPremise
