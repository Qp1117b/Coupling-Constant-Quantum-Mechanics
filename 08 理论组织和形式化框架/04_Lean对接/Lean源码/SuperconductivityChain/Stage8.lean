import SuperconductivityChain.Basic
import SuperconductivityChain.Stage2
import Mathlib.Data.ZMod.Basic
import Mathlib.NumberTheory.Real.Irrational
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
# 阶段 8：危机与锚（环 19–24）

形式化危机三条件、全对速度冻结、锚开关的算术核、锚区等速、离散相位标签 `Z_n`。
锚的几何判据、起点截距、`c_ij` 分布、`A_τ` 与 `K^SC` 的数值同一均不证。

缺口：`审-8`、`审-11`、`审-12`、`审-13`、`M9`、`临-9`、`临-16`、`临-17`、`G22`。
-/

namespace CQM.SuperconductivityChain

variable {V : Type*} [Fintype V] [DecidableEq V]

/-- 环 19：危机三条件；仅为形式定义，不声称可解或可算。 -/
def Crisis (Vbar Mdot B : ℝ) : Prop :=
  0 < Vbar ∧ Mdot = 0 ∧ 0 ≤ B

/-- 危机条件给出 `Vbar > 0`。 -/
theorem crisis_Vbar_pos {Vbar Mdot B : ℝ} (h : Crisis Vbar Mdot B) :
    0 < Vbar := h.1

/-- 危机条件给出 `Mdot = 0`。 -/
theorem crisis_Mdot_eq_zero {Vbar Mdot B : ℝ} (h : Crisis Vbar Mdot B) :
    Mdot = 0 := h.2.1

/-- 危机条件给出 `B ≥ 0`。 -/
theorem crisis_B_nonneg {Vbar Mdot B : ℝ} (h : Crisis Vbar Mdot B) :
    0 ≤ B := h.2.2

/-- 环 20：全对速度冻结，`Ḣ_ij = 0` 对所有节点对。 -/
def AllPairsFreeze (v : V → ℝ) : Prop := ∀ i j, historyRate v i j = 0

/-- 环 20：全对冻结等价于所有节点速度相等。 -/
theorem allPairsFreeze_iff (v : V → ℝ) :
    AllPairsFreeze v ↔ ∀ i j, v i = v j := by
  unfold AllPairsFreeze
  constructor
  · intro h i j
    exact (historyRate_eq_zero_iff v i j).mp (h i j)
  · intro h i j
    exact (historyRate_eq_zero_iff v i j).mpr (h i j)

/-- 环 21：锚开关的算术核。若相位条件 `γ_n H ∈ 2πℤ` 对所有 `n` 成立，
且存在一对 `γ_n/γ_n'` 无理，则 `H=0`。 -/
theorem anchorSwitch_zero {H : ℝ} {γ : ℕ → ℝ}
    (hγ : ∃ n n', Irrational (γ n / γ n'))
    (hphase : ∀ n, ∃ m : ℤ, H * γ n = 2 * Real.pi * m) : H = 0 := by
  obtain ⟨n, n', hI⟩ := hγ
  by_contra hH
  obtain ⟨m, hm⟩ := hphase n
  obtain ⟨m', hm'⟩ := hphase n'
  have hratio_ne_zero : γ n / γ n' ≠ 0 := by
    simpa using hI.ne_rational 0 1
  have hγn : γ n ≠ 0 := by
    intro h0
    apply hratio_ne_zero
    rw [h0]
    simp
  have hγn' : γ n' ≠ 0 := by
    intro h0
    apply hratio_ne_zero
    rw [h0]
    simp
  have hm0 : m ≠ 0 := by
    intro hmz
    have hzero : H * γ n = 0 := by simpa [hmz] using hm
    exact hH ((mul_eq_zero.mp hzero).resolve_right hγn)
  have hm0' : m' ≠ 0 := by
    intro hmz
    have hzero : H * γ n' = 0 := by simpa [hmz] using hm'
    exact hH ((mul_eq_zero.mp hzero).resolve_right hγn')
  have hpi : (2 * Real.pi : ℝ) ≠ 0 := by positivity
  have hratio_eq : γ n / γ n' = (m : ℝ) / (m' : ℝ) := by
    calc
      γ n / γ n' = (H * γ n) / (H * γ n') := by
        field_simp [hH]
      _ = (2 * Real.pi * (m : ℝ)) / (2 * Real.pi * (m' : ℝ)) := by
        rw [hm, hm']
      _ = (m : ℝ) / (m' : ℝ) := by
        field_simp [hpi, hm0, hm0']
  exact hI.ne_rational m m' hratio_eq

/-- 环 22：锚区结构容器。`constant_on` 表示 `ℓ_e=0` 区域内速度相等；
从 `ℓ_e=0` 到该字段的几何推导仍归 `临-16`/`审-8`。 -/
structure AnchorRegion where
  carrier : Finset V
  speed : V → ℝ
  constant_on : ∀ i ∈ carrier, ∀ j ∈ carrier, speed i = speed j

/-- 环 22：锚区内任一节点对的历史变化率为零。 -/
theorem AnchorRegion.historyRate_zero (A : AnchorRegion (V := V))
    {i j : V} (hi : i ∈ A.carrier) (hj : j ∈ A.carrier) :
    historyRate A.speed i j = 0 := by
  rw [historyRate_eq_zero_iff]
  exact A.constant_on i hi j hj

/-- 环 23：离散相位标签 `Z_n`；`n=2` 是第一档，不是唯一档。 -/
abbrev CyclicPhase (n : ℕ) := ZMod n

/-- 环 23：`n` 档循环相位标签的基数；只证明标签集有限，不证明 `U(1)//Z_n` 商。 -/
theorem cyclicPhase_card {n : ℕ} [NeZero n] :
    Fintype.card (CyclicPhase n) = n := by
  simp [CyclicPhase]

end CQM.SuperconductivityChain
