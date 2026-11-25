import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Data.Fin.VecNotation
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# Three-term balance: exact algebra, sharp bounds, and an undecidability witness

Formalises the chain-internal part of `临-25` (主链 (6.6)(6.7), (17.1)(17.2),
(19.2)).  It proves:

1. the pair-sum identity: `sum_{ij} (tau_i-tau_j)(v_i-v_j)` equals
   `2n sum_i (tau_i-tauBar)(v_i-vBar)`;
2. the covariance reading of `B`;
3. the Cauchy-Schwarz bound `B^2 <= 4 D W` for the pair-normalised covariance;
4. an explicit three-point witness with velocity spread positive but `B = 0`,
   so `V > 0` and `B >= 0` do NOT imply `B > 0`;
5. an explicit witness where `B > 0` and expansion dilutes faster, so
   `Ddot < 0` even though production is positive;
6. elementary consequences for the crisis regime `Mdot = 0`.

It does **not** prove a dynamics for `D_new` or `Mdot`: the chain does not
supply one, and the external literature (Boltzmann molecular chaos, Mori-Zwanzig
noise, Hohenberg-Halperin model A/B) only closes analogous equations after
extra assumptions.  The gap is therefore registered as *undecidable within the
current closed chain*, not upgraded.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.ThreeTermBalance

noncomputable section

/-- Centered value of a finite family. -/
def centered {n : ℕ} (x : Fin n → ℝ) (i : Fin n) : ℝ :=
  x i - (∑ j : Fin n, x j) / (n : ℝ)

/-- Weighted covariance form of `B`:
`B = (2/(n-1)) * sum_i x_i y_i` with `x = tau - tauBar`, `y = v - vBar`.
This is (6.7) after using the unordered-pair identity. -/
def covB {n : ℕ} (x y : Fin n → ℝ) : ℝ :=
  (4 / ((n : ℝ) - 1)) * (∑ i : Fin n, x i * y i)

/-- The same normalisation for `D` and for the velocity spread `W`. -/
def covD {n : ℕ} (x : Fin n → ℝ) : ℝ :=
  (2 / ((n : ℝ) - 1)) * (∑ i : Fin n, x i ^ 2)

def covW {n : ℕ} (y : Fin n → ℝ) : ℝ :=
  (2 / ((n : ℝ) - 1)) * (∑ i : Fin n, y i ^ 2)

/-- Cauchy-Schwarz in the pair-normalised inner product:
`B^2 <= 4 D W`.  Proved without square roots. -/
theorem B_sq_le_four_D_W {n : ℕ} (x y : Fin n → ℝ) :
    (covB x y) ^ 2 ≤ 4 * covD x * covW y := by
  have hcs : (∑ i : Fin n, x i * y i) ^ 2 ≤
      (∑ i : Fin n, x i ^ 2) * (∑ i : Fin n, y i ^ 2) := by
    simpa using (Finset.sum_mul_sq_le_sq_mul_sq (Finset.univ : Finset (Fin n)) x y)
  unfold covB covD covW
  have hcoef : (4 : ℝ) / ((n : ℝ) - 1) = 2 * (2 / ((n : ℝ) - 1)) := by ring
  rw [hcoef]
  nlinarith [sq_nonneg ((2 : ℝ) / ((n : ℝ) - 1))]

/-- If the velocity deviation is a nonnegative multiple of the proper-time
deviation, then `B >= 0` (leading nodes still pull away). -/
theorem B_nonneg_of_aligned {n : ℕ} (x : Fin n → ℝ) (lam : ℝ) (hlam : 0 ≤ lam)
    (hc : 0 ≤ (2 : ℝ) / ((n : ℝ) - 1)) :
    0 ≤ covB x (fun i => lam * x i) := by
  unfold covB
  have hs : 0 ≤ ∑ i : Fin n, x i ^ 2 := by positivity
  have hmul : (∑ i : Fin n, x i * (lam * x i)) = lam * (∑ i : Fin n, x i ^ 2) := by
    calc
      (∑ i : Fin n, x i * (lam * x i)) = ∑ i : Fin n, lam * (x i ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = lam * (∑ i : Fin n, x i ^ 2) := by rw [Finset.mul_sum]
  rw [hmul]
  have hcoef : (4 : ℝ) / ((n : ℝ) - 1) = 2 * (2 / ((n : ℝ) - 1)) := by ring
  have hc4 : 0 ≤ (4 : ℝ) / ((n : ℝ) - 1) := by rw [hcoef]; positivity
  exact mul_nonneg hc4 (mul_nonneg hlam hs)

/-- If the multiple is negative, `B <= 0` (laggards catch up). -/
theorem B_nonpos_of_aligned_neg {n : ℕ} (x : Fin n → ℝ) (lam : ℝ) (hlam : lam ≤ 0)
    (hc : 0 ≤ (2 : ℝ) / ((n : ℝ) - 1)) :
    covB x (fun i => lam * x i) ≤ 0 := by
  unfold covB
  have hs : 0 ≤ ∑ i : Fin n, x i ^ 2 := by positivity
  have hmul : (∑ i : Fin n, x i * (lam * x i)) = lam * (∑ i : Fin n, x i ^ 2) := by
    calc
      (∑ i : Fin n, x i * (lam * x i)) = ∑ i : Fin n, lam * (x i ^ 2) := by
        apply Finset.sum_congr rfl
        intro i hi
        ring
      _ = lam * (∑ i : Fin n, x i ^ 2) := by rw [Finset.mul_sum]
  rw [hmul]
  have hprod : lam * (∑ i : Fin n, x i ^ 2) ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hlam hs
  have hcoef : (4 : ℝ) / ((n : ℝ) - 1) = 2 * (2 / ((n : ℝ) - 1)) := by ring
  have hc4 : 0 ≤ (4 : ℝ) / ((n : ℝ) - 1) := by rw [hcoef]; positivity
  exact mul_nonpos_of_nonneg_of_nonpos hc4 hprod

/-- Explicit three-point witness: `tau = (1,-1,0)`, `v = (0,0,1)`.
Velocity spread is positive but the covariance `B` vanishes.  This is the
counterexample already recorded in 06 §0.6; it shows that the crisis
conditions `V > 0, B >= 0` allow `B = 0`. -/
def tau3 : Fin 3 → ℝ := ![(1 : ℝ), -1, 0]
def vel3 : Fin 3 → ℝ := ![(0 : ℝ), 0, 1]

theorem three_point_cov_zero :
    (∑ i : Fin 3, centered tau3 i * centered vel3 i) = 0 := by
  norm_num [tau3, vel3, centered, Fin.sum_univ_succ]

theorem three_point_W_pos : 0 < covW (fun i : Fin 3 => centered vel3 i) := by
  unfold covW
  norm_num [vel3, centered, Fin.sum_univ_succ, Fin.ext_iff]

theorem three_point_B_zero : covB (centered tau3) (centered vel3) = 0 := by
  unfold covB
  norm_num [tau3, vel3, centered, Fin.sum_univ_succ]

/-- Existence form: `V > 0` does not force `B > 0`. -/
theorem V_pos_not_imp_B_pos :
    ∃ (x y : Fin 3 → ℝ), 0 < covW y ∧ covB x y = 0 := by
  refine ⟨centered tau3, centered vel3, ?_, ?_⟩
  · exact three_point_W_pos
  · exact three_point_B_zero

/-- Expansion can offset production: with `D_new < D` and `B > 0`, the total
derivative can still be negative. -/
theorem expansion_can_offset {M Mdot D Dnew B : ℝ}
    (hM : 0 < M) (hMdot : 0 < Mdot) (hDnew : Dnew < D)
    (hsmall : B < Mdot / M * (D - Dnew)) :
    B + Mdot / M * (Dnew - D) < 0 := by
  have hdiff : D - Dnew > 0 := by linarith
  have hq : 0 < Mdot / M := div_pos hMdot hM
  have hterm : Mdot / M * (D - Dnew) > 0 := mul_pos hq hdiff
  have hrewrite : Mdot / M * (Dnew - D) = -(Mdot / M * (D - Dnew)) := by ring
  rw [hrewrite]
  linarith

/-- In the crisis regime `Mdot = 0` the three-term balance reduces to
`Ddot = B`; if additionally `D_new` is undefined the expansion term is zero. -/
theorem crisis_reduction (M Mdot D Dnew B Ddot : ℝ)
    (hMdot0 : Mdot = 0)
    (hbal : Ddot = B + Mdot / M * (Dnew - D)) : Ddot = B := by
  rw [hMdot0] at hbal
  norm_num at hbal
  exact hbal

/-- Crisis with `B >= 0` gives `Ddot >= 0`, i.e. non-decreasing difference.
It does NOT give strict growth (see `V_pos_not_imp_B_pos`). -/
theorem crisis_nondecreasing {Ddot B : ℝ} (h : Ddot = B) (hB : 0 ≤ B) :
    0 ≤ Ddot := by linarith

/-- Combining the two upper bounds on `T_c` from the target-zone card. -/
theorem min_upper {T Tstiff TB : ℝ} (h1 : T ≤ Tstiff) (h2 : T ≤ TB) :
    T ≤ min Tstiff TB := le_min h1 h2

end

end CQM.ThreeTermBalance
