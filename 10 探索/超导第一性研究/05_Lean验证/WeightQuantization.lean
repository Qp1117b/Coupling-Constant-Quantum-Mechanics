import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# `G19`: quantization of the representation weight s

Single-valuedness of ρ(R(2π)) = exp(i 2π s) gives s ∈ ℤ (bosonic) or, allowing
the SU(2) double cover, s ∈ ℤ + 1/2.  Together 2s ∈ ℤ and the phase-connection
coefficient α_lin = -4πs = -2π(2s) lies in 2πℤ.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.WeightQuantization

/-- Bosonic single-valuedness: cos(2πs) = 1 forces s ∈ ℤ. -/
theorem integer_weight_of_single_valued (s : ℝ) (h : Real.cos (2 * Real.pi * s) = 1) :
    ∃ n : ℤ, s = n := by
  rcases (Real.cos_eq_one_iff (2 * Real.pi * s)).mp h with ⟨n, hn⟩
  refine ⟨n, ?_⟩
  have hpi : 0 < Real.pi := Real.pi_pos
  nlinarith [hn]

/-- Spinorial double cover: cos(2πs) = -1 forces s ∈ ℤ - 1/2. -/
theorem half_integer_weight_of_double_cover (s : ℝ) (h : Real.cos (2 * Real.pi * s) = -1) :
    ∃ n : ℤ, 2 * s = 2 * n - 1 := by
  have hplus : Real.cos (2 * Real.pi * s + Real.pi) = 1 := by
    rw [Real.cos_add_pi, h]
    norm_num
  rcases (Real.cos_eq_one_iff (2 * Real.pi * s + Real.pi)).mp hplus with ⟨n, hn⟩
  refine ⟨n, ?_⟩
  have hpi : 0 < Real.pi := Real.pi_pos
  nlinarith [hn]

/-- Both cases give 2s ∈ ℤ. -/
theorem weight_quantized (s : ℝ) (h : Real.cos (2 * Real.pi * s) = 1 ∨
    Real.cos (2 * Real.pi * s) = -1) : ∃ k : ℤ, 2 * s = k := by
  rcases h with h | h
  · obtain ⟨n, hn⟩ := integer_weight_of_single_valued s h
    refine ⟨2 * n, ?_⟩
    rw [hn]
    norm_num [mul_comm]
  · obtain ⟨n, hn⟩ := half_integer_weight_of_double_cover s h
    refine ⟨2 * n - 1, ?_⟩
    rw [hn]
    norm_num

/-- The linear phase-connection coefficient is quantized in units of 2π. -/
theorem alpha_quantized (s : ℝ) (k : ℤ) (hk : 2 * s = k) :
    -4 * Real.pi * s = -2 * Real.pi * (k : ℝ) := by
  have hs : s = (k : ℝ) / 2 := by linarith
  rw [hs]
  ring

end CQM.WeightQuantization
