import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Pow.Deriv
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

/-!
# `M8`: the percolation phase boundary and its doping slope

The phase-boundary condition is `p_pair(T_c) = p_*(T_c)` with
`p_*(T) = p_c + (1-p_c) R(T)^(1/t_Υ)`, `R(T) = T/w(T)`.  Formalised here:

1. the logarithmic identity `R'/R = 1/T - w'/w`;
2. the chain-rule form of `p_*'`;
3. the implicit-doping slope `T_c' = p_pair' / p_*'` along the boundary.

The exponent `t_Υ ≈ 1.3` remains an external universal number.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.M8PhaseBoundary

/-- The dimensionless ratio R(T) = T/w(T). -/
noncomputable def Rfun (w : ℝ → ℝ) (T : ℝ) : ℝ := T / w T

/-- The phase boundary p_*(T) = p_c + (1-p_c) R^(1/t). -/
noncomputable def pStar (w : ℝ → ℝ) (pc t T : ℝ) : ℝ :=
  pc + (1 - pc) * (Rfun w T) ^ (1 / t)

/-- The logarithmic identity for R = T/w: R'/R = 1/T - w'/w. -/
theorem R_log_deriv (w : ℝ → ℝ) (T : ℝ) (hT : T ≠ 0) (hw : w T ≠ 0)
    (hdw : DifferentiableAt ℝ w T) :
    deriv (Rfun w) T / Rfun w T = 1 / T - deriv w T / w T := by
  unfold Rfun
  have hnum : HasDerivAt (fun y : ℝ => y) 1 T := hasDerivAt_id T
  have hdiv := hnum.div hdw.hasDerivAt hw
  have hRderiv : deriv (fun y : ℝ => y / w y) T = (w T - T * deriv w T) / (w T) ^ 2 := by
    simpa [sub_eq_add_neg, mul_comm, mul_left_comm, mul_assoc, pow_two] using hdiv.deriv
  rw [hRderiv]
  field_simp [hT, hw]

/-- The chain-rule form of the phase-boundary derivative. -/
theorem pStar_deriv (w : ℝ → ℝ) (pc t T : ℝ)
    (hRpos : 0 < Rfun w T) (hdw : DifferentiableAt ℝ w T) (hw : w T ≠ 0) :
    deriv (pStar w pc t) T =
      (1 - pc) * (1 / t) * (Rfun w T) ^ (1 / t - 1) * deriv (Rfun w) T := by
  unfold pStar
  have hRdiff : DifferentiableAt ℝ (Rfun w) T := by
    unfold Rfun
    exact (hasDerivAt_id T).div hdw.hasDerivAt hw |>.differentiableAt
  have hinner : HasDerivAt (Rfun w) (deriv (Rfun w) T) T := hRdiff.hasDerivAt
  have hpow0 : HasDerivAt (fun z : ℝ => z ^ (1 / t))
      ((1 / t) * (Rfun w T) ^ (1 / t - 1)) (Rfun w T) := by
    exact Real.hasDerivAt_rpow_const (Or.inl (ne_of_gt hRpos))
  have hcomp : HasDerivAt (fun y => (Rfun w y) ^ (1 / t))
      ((1 / t) * (Rfun w T) ^ (1 / t - 1) * deriv (Rfun w) T) T :=
    hpow0.comp T hinner
  have hscaled := hcomp.const_mul (1 - pc)
  simpa [mul_assoc] using hscaled.deriv

/-- Along the boundary p_pair(T_c) = p_*(T_c), the doping slope of T_c is
p_pair' / p_*' (provided p_*' ≠ 0). -/
theorem implicit_slope (pair Tc : ℝ → ℝ) (w : ℝ → ℝ) (pc t d : ℝ)
    (hEq : ∀ δ, pair δ = pStar w pc t (Tc δ))
    (hpair : HasDerivAt pair pd d) (hTc : HasDerivAt Tc Td d)
    (hpstar : HasDerivAt (pStar w pc t) ps (Tc d))
    (hps : ps ≠ 0) : Td = pd / ps := by
  have hcomp : HasDerivAt (fun δ => pStar w pc t (Tc δ)) (ps * Td) d := hpstar.comp d hTc
  have hfun : pair = fun δ => pStar w pc t (Tc δ) := by funext δ; exact hEq δ
  have hderiv_eq : deriv pair d = deriv (fun δ => pStar w pc t (Tc δ)) d := by
    rw [hfun]
  rw [hpair.deriv, hcomp.deriv] at hderiv_eq
  field_simp [hps]
  nlinarith

end CQM.M8PhaseBoundary
