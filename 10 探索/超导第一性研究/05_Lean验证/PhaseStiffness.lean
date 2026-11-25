import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Real.Pi.Bounds
import Mathlib.Order.Monotone.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Phase stiffness: spin-wave energy, BKT renormalisation, percolation readout

This file formalises the algebraic and monotonicity core of
`03_推导工作台/环19_相位自由能与渗流刚度.md`.

It does **not** prove:

* that the CQM phase sector is the XY model;
* the Mermin–Wagner theorem;
* the Kosterlitz recursion relations or the universal jump;
* the percolation stiffness exponent `t_Upsilon`;
* the power-law shape of `Phi`.

It proves only:

1. the single-bond spin-wave energy is nonnegative and vanishes only at zero
   phase difference (positive coupling);
2. a uniform rescaling of the aggregate bond sum rescales the stiffness;
3. if the renormalised stiffness is bounded by the bare one, then the bare
   crossing temperature is an upper bound for the BKT temperature;
4. the percolation readout never exceeds the bare stiffness when `0 <= Phi <= 1`;
5. the BKT equation with the percolation readout gives `T <= pi * Upsilon / 2`;
6. if `Phi` vanishes below `p_c`, a solution forces `p > p_c`;
7. `p > p_c` is not sufficient (explicit numerical counterexample);
8. a strictly decreasing and a strictly increasing function cross at most once.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.PhaseStiffness

noncomputable section

/-- Harmonic (spin-wave) energy of one bond:
`(J/2) * (Delta theta)^2`.  This is the quadratic term of
`-J cos(Delta theta)`. -/
def bondSpinWave (J dθ : ℝ) : ℝ :=
  (J / 2) * dθ ^ 2

/-- The single-bond spin-wave energy is nonnegative for a positive coupling. -/
theorem bondSpinWave_nonneg {J dθ : ℝ} (hJ : 0 ≤ J) :
    0 ≤ bondSpinWave J dθ := by
  unfold bondSpinWave
  have hJ2 : 0 ≤ J / 2 := by linarith
  exact mul_nonneg hJ2 (sq_nonneg dθ)

/-- For a strictly positive coupling the spin-wave energy vanishes exactly at
zero phase difference. -/
theorem bondSpinWave_eq_zero_iff {J dθ : ℝ} (hJ : 0 < J) :
    bondSpinWave J dθ = 0 ↔ dθ = 0 := by
  unfold bondSpinWave
  constructor
  · intro h
    have hJ2 : (J / 2) ≠ 0 := by positivity
    have h2 : dθ ^ 2 = 0 := (mul_eq_zero.mp h).resolve_left hJ2
    exact sq_eq_zero_iff.mp h2
  · intro h
    simp [h]

/-- Phase stiffness read from an aggregate bond sum,
`(1/(2A)) * sum_ij J_ij r_ij^2`. -/
def phaseStiffness (A bondSum : ℝ) : ℝ :=
  (1 / (2 * A)) * bondSum

/-- A uniform rescaling of the bond sum rescales the stiffness. -/
theorem phaseStiffness_rescale (A w bondSum : ℝ) :
    phaseStiffness A (w * bondSum) = w * phaseStiffness A bondSum := by
  unfold phaseStiffness
  ring

/-- Dimensionless stiffness `K = Upsilon / (k_B T)`. -/
def reducedStiffness (kB T U : ℝ) : ℝ :=
  U / (kB * T)

/-- If the renormalised stiffness never exceeds the bare stiffness, and the
bare stiffness is antitone, then the bare crossing temperature is an upper
bound for the BKT temperature.  This is the formal content of
`T_BKT <= T_bare`. -/
theorem bkt_bare_crossing_ge {KR K0 : ℝ → ℝ} {Tb Tbare : ℝ}
    (hKR : ∀ T, KR T ≤ K0 T)
    (hmono : StrictAnti K0)
    (hR : KR Tb = 2 / Real.pi)
    (h0 : K0 Tbare = 2 / Real.pi) : Tb ≤ Tbare := by
  have hc : 2 / Real.pi ≤ K0 Tb := by
    rw [← hR]
    exact hKR Tb
  by_contra h
  have hlt : Tbare < Tb := lt_of_not_ge h
  have hle : K0 Tb < K0 Tbare := hmono hlt
  linarith

/-- Percolation readout of the phase stiffness:
`Upsilon_bond * w * Phi(p)`. -/
def percolationStiffness (Ubond w : ℝ) (Phi : ℝ → ℝ) (p : ℝ) : ℝ :=
  Ubond * w * Phi p

/-- With `0 <= Phi <= 1` the percolation readout never exceeds the bare
stiffness. -/
theorem percolationStiffness_le_bare {Ubond w : ℝ} {Phi : ℝ → ℝ} {p : ℝ}
    (hPhi : Phi p ≤ 1) (hUw : 0 ≤ Ubond * w) :
    percolationStiffness Ubond w Phi p ≤ Ubond * w := by
  unfold percolationStiffness
  calc
    Ubond * w * Phi p ≤ Ubond * w * 1 :=
      mul_le_mul_of_nonneg_left hPhi hUw
    _ = Ubond * w := by ring

/-- The bare BKT condition written without division:
`2 T = pi * Upsilon`. -/
def bktCondition (T U : ℝ) : Prop :=
  2 * T = Real.pi * U

/-- The percolation readout plus `Phi <= 1` gives the upper bound
`T <= pi * Upsilon_bond * w / 2`. -/
theorem bkt_upper_bound {Ubond w T : ℝ} {Phi : ℝ → ℝ} {p : ℝ}
    (hPhi : Phi p ≤ 1) (hUw : 0 ≤ Ubond * w)
    (h : bktCondition T (percolationStiffness Ubond w Phi p)) :
    T ≤ Real.pi * (Ubond * w) / 2 := by
  unfold bktCondition percolationStiffness at h
  have hle : Ubond * w * Phi p ≤ Ubond * w := by
    calc
      Ubond * w * Phi p ≤ Ubond * w * 1 :=
        mul_le_mul_of_nonneg_left hPhi hUw
      _ = Ubond * w := by ring
  have hpi : 0 < Real.pi := Real.pi_pos
  have h2 : 2 * T ≤ Real.pi * (Ubond * w) := by
    rw [h]
    exact mul_le_mul_of_nonneg_left hle hpi.le
  linarith

/-- If `Phi` vanishes at and below `p_c`, then any positive-temperature
solution of the BKT equation must have `p > p_c`.  This is the precise sense in
which `p_c` is necessary. -/
theorem pc_necessary {Ubond w T pc : ℝ} {Phi : ℝ → ℝ} {p : ℝ}
    (hzero : ∀ q, q ≤ pc → Phi q = 0)
    (hT : 0 < T)
    (h : bktCondition T (percolationStiffness Ubond w Phi p)) : pc < p := by
  by_contra hnot
  have hle : p ≤ pc := le_of_not_gt hnot
  have hp0 : Phi p = 0 := hzero p hle
  unfold bktCondition percolationStiffness at h
  rw [hp0] at h
  ring_nf at h
  linarith

/-- An explicit `Phi` with `Phi = 0` below `1/2` and `Phi = 1/10` above it. -/
def examplePhi (p : ℝ) : ℝ :=
  if p ≤ 1 / 2 then 0 else 1 / 10

/-- `p > p_c` is not sufficient: at `p = 3/4`, `Upsilon_bond = 1`, `w = 1` and
`T = 1`, the readout is `1/10`, far below `2T/pi`. -/
theorem pc_not_sufficient :
    ∃ p T : ℝ, (1 / 2 : ℝ) < p ∧
      ¬ bktCondition T (percolationStiffness 1 1 examplePhi p) := by
  refine ⟨3 / 4, 1, by norm_num, ?_⟩
  unfold bktCondition percolationStiffness examplePhi
  norm_num
  intro h
  have hpi : Real.pi < 4 := Real.pi_lt_four
  nlinarith

/-- A strictly decreasing function and a strictly increasing function cross at
most once.  This is the uniqueness half of `p_pair(T) = p_*(T)`; existence is a
continuity statement and is not formalised here. -/
theorem crossing_unique {f g : ℝ → ℝ} (hf : StrictAnti f) (hg : StrictMono g)
    {T₁ T₂ : ℝ} (h₁ : f T₁ = g T₁) (h₂ : f T₂ = g T₂) : T₁ = T₂ := by
  rcases lt_trichotomy T₁ T₂ with h | h | h
  · have hf' : f T₂ < f T₁ := hf h
    have hg' : g T₁ < g T₂ := hg h
    linarith
  · exact h
  · have hf' : f T₁ < f T₂ := hf h
    have hg' : g T₂ < g T₁ := hg h
    linarith

/-- The percolation readout is antitone in temperature when `w` is antitone and
`Phi(p) >= 0`. -/
theorem percolationStiffness_antitone_in_T {Ubond : ℝ} (hU : 0 ≤ Ubond)
    {Phi : ℝ → ℝ} {p : ℝ} (hPhi0 : 0 ≤ Phi p)
    {w : ℝ → ℝ} (hw : Antitone w) :
    Antitone (fun T => percolationStiffness Ubond (w T) Phi p) := by
  intro T₁ T₂ hT
  unfold percolationStiffness
  have hw' : w T₂ ≤ w T₁ := hw hT
  have h1 : Ubond * w T₂ ≤ Ubond * w T₁ :=
    mul_le_mul_of_nonneg_left hw' hU
  exact mul_le_mul_of_nonneg_right h1 hPhi0

end

end CQM.PhaseStiffness
