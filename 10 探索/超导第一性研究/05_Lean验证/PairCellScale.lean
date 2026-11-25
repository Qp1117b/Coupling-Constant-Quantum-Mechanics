import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# Ring 15: threshold of an average versus average of a threshold

This file isolates the scale/aggregation distinction behind the ring-15
`p_pair` readout.

For a cell with two local variance readings `x`, `y` and threshold `c`:

* `avgAbove x y c` is the indicator of "the cell average exceeds `c`";
* `fracAbove x y c` is the fraction of local readings that exceed `c`.

They agree when the two readings are equal (the uniform-cell limit `G3`),
but they fail to agree in general.  Thus a chi-square tail for a
coarse-grained sample average cannot be silently identified with the local
pairing fraction of `(15.1)`.

No axiom, `sorry`, `admit`, `native_decide` or `unsafe` is used.
-/

namespace CQM.PairCellScale

noncomputable section

/-- Indicator that the arithmetic mean of two readings exceeds `c`. -/
def avgAbove (x y c : ℝ) : ℝ :=
  if (x + y) / 2 > c then 1 else 0

/-- Fraction of the two readings that exceed `c`. -/
def fracAbove (x y c : ℝ) : ℝ :=
  ((if x > c then (1 : ℝ) else 0) + (if y > c then (1 : ℝ) else 0)) / 2

/-- In the uniform cell `x = y`, the two readouts coincide. -/
theorem avgAbove_self (x c : ℝ) :
    avgAbove x x c = fracAbove x x c := by
  by_cases h : x > c
  · simp [avgAbove, fracAbove, h]
  · simp [avgAbove, fracAbove, h]

/-- Non-uniform cells can make the two readouts differ. -/
theorem avgAbove_ne_fracAbove :
    ∃ x y c : ℝ, avgAbove x y c ≠ fracAbove x y c := by
  refine ⟨0, 2, (1 / 2 : ℝ), ?_⟩
  norm_num [avgAbove, fracAbove]

/-- The same distinction for a cell with an arbitrary finite number of
readings, stated at the level of the two extremal cases: a cell whose mean is
above threshold while not every reading is above it. -/
theorem avg_above_not_all_above
    (x y c : ℝ) (hxy : (x + y) / 2 > c) (hy : ¬ y > c) :
    avgAbove x y c ≠ fracAbove x y c := by
  have hx : x > c := by linarith
  simp [avgAbove, fracAbove, hxy, hx, hy]

end

end CQM.PairCellScale
