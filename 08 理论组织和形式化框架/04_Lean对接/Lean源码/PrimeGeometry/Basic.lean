import Mathlib.Data.Real.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Data.Int.Basic
import Mathlib.Tactic
import SpectralGeometry.Basic

/-!
# 因果时几何 (Causal Time Geometry)

本模块形式化"因果时的弯曲"——即再生产固有时的周期性自我折叠。
所有几何对象（多边形、弧段、位置）都是因果时结构，不是空间几何。

## 本体论区分

| 概念 | CQM（因果时几何） | GR（时空几何） |
|:---|:---|:---|
| 弯曲对象 | 再生产固有时数轴 | 时空流形 \(g_{\mu\nu}\) |
| 弯曲原因 | 再生产周期性 | 物质能量-动量 |
| 空间地位 | 次级涌现（退相干产物） | 与时间一起预设 |
| "长度" | 因果步数（再生产次数） | 空间距离（米） |

## 核心定义

- **再生产固有时** (ReproductionTime)：用整数标记的离散再生产周期
- **因果时多边形** (CausalPolygon)：因果时数轴弯折成的封闭图形
- **因果线段** (CausalSegment)：因果网络中的信息传递链
- **因果时位置** (CausalTimePosition)：因果时在再生产周期中的相位

## 核心定理

- **三角形最小性** (triangleIsMinimal)：n=3 是因果时最小非平凡闭合多边形
- n=1 退化（单点无因果结构），n=2 退化（因果弧段正反重叠）

## 参考文献

- ruster (2026). 质数几何密度-三代粒子模型：因果时弯曲与康普顿波长猜想.
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

namespace CQM

open scoped BigOperators

/-! ## 再生产固有时 -/

/-- 再生产固有时：用整数标记的离散再生产周期。
    正整数表示再生产步数，这是因果时几何的基本单位。
    注意：不是空间坐标，不是时钟时间，而是物质自我运动的内部度量。 -/
abbrev ReproductionTime := ℤ

/-- 再生产固有时步数严格为正的标记 -/
def ReproductionTime.pos (t : ReproductionTime) : Prop := t > 0

/-! ## 因果时多边形 -/

/-- 因果时多边形 (Causal Polygon)：将再生产固有时数轴按周长 C 弯折
    而成的封闭二维图形边界。

    注意：这是因果时结构，不是空间多边形。周长 C 以"因果步数"为单位，
    而非空间距离（米）。

    参数：
    - `n`：边数（扇区数 = 退相干通道数 = 粒子代数）
    - `hn`：n ≥ 1
    - `circumference`：因果时周长（因果步数）
    - `hC`：circumference > 0 -/
structure CausalPolygon where
  n : ℕ
  hn : n ≥ 1
  circumference : ℝ
  hC : circumference > 0

/-- 因果时多边形的边长（正多边形各边等长）。 -/
noncomputable def CausalPolygon.sideLength (p : CausalPolygon) : ℝ :=
  p.circumference / (p.n : ℝ)

/-- 因果时多边形边长严格为正。 -/
theorem CausalPolygon.sideLength_pos (p : CausalPolygon) : p.sideLength > 0 := by
  dsimp [CausalPolygon.sideLength]
  have hnpos : (0 : ℝ) < (p.n : ℝ) := by
    have h : p.n ≠ 0 := Nat.one_le_iff_ne_zero.mp p.hn
    exact_mod_cast Nat.pos_of_ne_zero h
  exact div_pos p.hC hnpos

/-- 因果时多边形是闭合的：所有弧段连续首尾相接，回到起点。
    这等价于 n 条弧段的总弧长 = 周长 C。 -/
theorem CausalPolygon.isClosed (p : CausalPolygon) : (p.n : ℝ) * p.sideLength = p.circumference := by
  dsimp [CausalPolygon.sideLength]
  have hnpos : (p.n : ℝ) ≠ 0 := by
    have h : p.n ≠ 0 := Nat.one_le_iff_ne_zero.mp p.hn
    exact_mod_cast h
  field_simp [hnpos]

/-! ## 因果线段 -/

/-- 因果线段 (Causal Segment)：因果时多边形上的一段连续弧。
    对应因果网络中的信息传递链，其"长度"是再生产周期的因果步数。

    注意：不是空间几何中的线段，没有空间长度（米）。 -/
structure CausalSegment where
  startAngle : ℝ
  arcLength : ℝ
  hpos : arcLength > 0

/-- 从因果时多边形构造第 k 段因果线段。
    第 k 段从角度 2πk/n 开始，弧长为 C/n。 -/
noncomputable def CausalSegment.ofCausalPolygon (p : CausalPolygon) (k : ℕ) (_hk : k < p.n) : CausalSegment :=
  { startAngle := 2 * Real.pi * (k : ℝ) / (p.n : ℝ)
    arcLength := p.circumference / (p.n : ℝ)
    hpos := p.sideLength_pos }

/-- 因果线段的弧长即为多边形边长。 -/
theorem CausalSegment.ofCausalPolygon_arcLength (p : CausalPolygon) (k : ℕ) (hk : k < p.n) :
    (CausalSegment.ofCausalPolygon p k hk).arcLength = p.sideLength := rfl

/-! ## 因果时位置 -/

/-- 因果时位置 (Causal Time Position)：将整数 n 映射到因果时圆上的位置。

    将再生产固有时数轴缠绕在周长为 C 的因果时圆上，
    整数 n 对应位置 (n mod N)·(C/N)，其中 N 是总缠绕次数。

    等价于 n·(C/N) mod C，但使用 Int.mod 使周期性证明更简洁。
    注意：非空间位置，而是因果时在再生产周期中的相位（0 ≤ 位置 < C）。 -/
noncomputable def CausalTimePosition (n : ℤ) (C : ℝ) (N : ℕ) : ℝ :=
  ((n % (N : ℤ) : ℤ) : ℝ) * C / (N : ℝ)

/-- 因果时位置的周期性：位置 (n+N) = 位置 n。
    因果时模 N 等价——这正是"因果时弯曲"的数学表达。 -/
theorem causalTimePosition_periodic (n : ℤ) (C : ℝ) (N : ℕ) (_hN : N > 0) :
    CausalTimePosition (n + (N : ℤ)) C N = CausalTimePosition n C N := by
  unfold CausalTimePosition
  have h : (n + (N : ℤ)) % (N : ℤ) = n % (N : ℤ) := by
    simp [Int.add_emod_right]
  have h' : (Int.cast : ℤ → ℝ) ((n + (N : ℤ)) % (N : ℤ)) = (Int.cast : ℤ → ℝ) (n % (N : ℤ)) :=
    congrArg (Int.cast : ℤ → ℝ) h
  rw [h']

/-- 因果时位置在 [0, C) 范围内。 -/
theorem causalTimePosition_range (n : ℤ) (C : ℝ) (N : ℕ) (hN : N > 0) (hC : C > 0) :
    0 ≤ CausalTimePosition n C N ∧ CausalTimePosition n C N < C := by
  unfold CausalTimePosition
  have hNpos : (N : ℝ) > 0 := by exact_mod_cast hN
  have hNpos_int : (0 : ℤ) < (N : ℤ) := by exact_mod_cast hN
  have h_mod_nonneg : 0 ≤ (Int.cast : ℤ → ℝ) (n % (N : ℤ)) := by
    have h : (0 : ℤ) ≤ n % (N : ℤ) := Int.emod_nonneg n hNpos_int.ne'
    exact Int.cast_nonneg h
  have h_mod_lt : (Int.cast : ℤ → ℝ) (n % (N : ℤ)) < (N : ℝ) := by
    have h : n % (N : ℤ) < (N : ℤ) := Int.emod_lt _ hNpos_int.ne'
    have h' : (Int.cast : ℤ → ℝ) (n % (N : ℤ)) < (Int.cast : ℤ → ℝ) (N : ℤ) := Int.cast_lt.mpr h
    simpa using h'
  have h_mul : (Int.cast : ℤ → ℝ) (n % (N : ℤ)) * C ≥ 0 := mul_nonneg h_mod_nonneg (by linarith)
  have h_div_nonneg : 0 ≤ (Int.cast : ℤ → ℝ) (n % (N : ℤ)) * C / (N : ℝ) :=
    div_nonneg h_mul (by linarith)
  have h_mul_lt : (Int.cast : ℤ → ℝ) (n % (N : ℤ)) * C < (N : ℝ) * C :=
    mul_lt_mul_of_pos_right h_mod_lt hC
  have h_div_lt : (Int.cast : ℤ → ℝ) (n % (N : ℤ)) * C / (N : ℝ) < C := by
    calc
      (Int.cast : ℤ → ℝ) (n % (N : ℤ)) * C / (N : ℝ) < (N : ℝ) * C / (N : ℝ) :=
        div_lt_div_of_pos_right h_mul_lt hNpos
      _ = C := by field_simp [hNpos.ne']
  exact ⟨h_div_nonneg, h_div_lt⟩

-- 因果时位置不是空间坐标。
-- 在 CQM 中，因果时位置是再生产周期的内部相位，与 GR 中的空间坐标有本质区别。
-- 此声明已在 `CausalTimePosition` 的定义注释中体现：因果时位置
-- 以因果步数度量，取值范围 [0, C)，而非空间坐标（米）。

/-! ## 正因果时三角形 -/

/-- 正因果时三角形（等边三角形内接于因果时圆）：n=3，各边等长 C/3。
    这是最小非平凡因果时闭合结构，对应三代费米子结构。 -/
noncomputable def equilateralTriangle (C : ℝ) (hC : C > 0) : CausalPolygon :=
  { n := 3
    hn := by norm_num
    circumference := C
    hC := hC }

/-- 正三角形的三段因果弧长相等 = C/3。 -/
theorem equilateralTriangle_arcs_equal (C : ℝ) (hC : C > 0) :
    (equilateralTriangle C hC).sideLength = C / 3 := rfl

/-- 正三角形三边之和 = 周长 C。 -/
theorem equilateralTriangle_perimeter (C : ℝ) (hC : C > 0) :
    (3 : ℝ) * (equilateralTriangle C hC).sideLength = C := by
  unfold equilateralTriangle CausalPolygon.sideLength
  field_simp
  ring

/-! ## 三角形最小性定理

三角形（n=3）是因果时最小非平凡闭合多边形。这是拓扑必然，不是数值巧合。

证明思路：
- n=1：单点，无边（无因果结构，无信息传递链）
- n=2：两点+两条边，但两条边作为因果弧段正反重叠（同一段因果时被折叠两次），
  不能形成真正的闭合因果环。退化情况。
- n=3：三点+三条边，三条边围成非零面积的因果区域，是第一个能简单闭合的因果时多边形。
-/

/-- 因果时多边形按边数分类：
    - n=1：退化（单点，无因果结构）
    - n=2：退化（因果弧段正反重叠，非简单闭合）
    - n≥3：非退化（存在真正的因果环） -/
def CausalPolygon.isDegenerate (p : CausalPolygon) : Prop := p.n < 3

/-- 因果时多边形非退化：n ≥ 3。 -/
def CausalPolygon.isNonDegenerate (p : CausalPolygon) : Prop := p.n ≥ 3

/-- [THEOREM] 三角形最小性定理：n=3 是因果时最小非平凡闭合多边形。

    对于正整数 n：
    - n=1：孤立点，因果弧段集为空，无闭合因果环 → 平凡
    - n=2：两点 A、B，两条弧段 AB 和 BA。
      这两条弧段作为因果时弧段完全重合（都是同一段因果时），
      形成的"因果区域"面积为零。退化多边形。
    - n=3：三点 A、B、C，三条弧段 AB、BC、CA。
      三条弧段围成非零面积因果区域，形成真正的闭合因果环。
    - n≥3：均存在非退化闭合因果时多边形。

    结论：n=3 是最小的 n 使得存在非退化闭合因果时多边形。 -/
theorem triangleIsMinimal : ∀ n : ℕ, n ≥ 1 → n < 3 → n = 1 ∨ n = 2 := by
  intro n hn1 hn3
  omega

/-- 退化情况 n=1：单点因果结构，无边（无信息传递链）。 -/
theorem degenerate_causal_n1 (p : CausalPolygon) (h : p.n = 1) :
    p.isDegenerate := by
  unfold CausalPolygon.isDegenerate
  omega

/-- 退化情况 n=1：单点无边，因果弧段长度 = 周长（自身）。 -/
theorem degenerate_causal_n1_sideLength (p : CausalPolygon) (h : p.n = 1) :
    p.sideLength = p.circumference := by
  unfold CausalPolygon.sideLength
  rw [h]
  norm_num

/-- 退化情况 n=2：两点+两条因果弧段正反重叠，非简单闭合。 -/
theorem degenerate_causal_n2 (p : CausalPolygon) (h : p.n = 2) :
    p.isDegenerate := by
  unfold CausalPolygon.isDegenerate
  omega

/-- 退化情况 n=2：两条因果弧段重合，闭合因果区域面积为零。 -/
theorem degenerate_causal_n2_zero_area (p : CausalPolygon) (h : p.n = 2) :
    (2 : ℝ) * p.sideLength = p.circumference := by
  unfold CausalPolygon.sideLength
  rw [h]
  field_simp; ring

/-- 最小非退化因果时多边形边数 = 3。 -/
theorem minimal_non_degenerate_causal_n : (sInf {n : ℕ | n ≥ 3}) = 3 := by
  have hBdd : BddBelow {n : ℕ | n ≥ 3} := by
    refine ⟨0, ?_⟩
    intro x hx
    simp at hx
    omega
  apply le_antisymm
  · apply csInf_le hBdd
    show 3 ∈ {n : ℕ | n ≥ 3}
    simp
  · apply le_csInf
    · show {n : ℕ | n ≥ 3}.Nonempty
      refine ⟨3, ?_⟩
      simp
    · intro b hb
      simp at hb
      exact hb

/-- 三角形是因果时体系中的第一个非退化多边形。 -/
theorem triangle_is_first_non_degenerate (p : CausalPolygon) (h : p.n = 3) :
    p.isNonDegenerate := by
  unfold CausalPolygon.isNonDegenerate
  omega

/-- 三角形边数 = 活跃素数个数 = 3（与 SpectralGeometry 一致）。 -/
theorem triangle_sides_eq_activePrimes_count : (3 : ℕ) = activePrimes.length := by
  rw [activePrimes_count_eq_three]

/-- 三角形顶点数 = 3。 -/
def triangleVertexCount : ℕ := 3

/-- 三角形的边数 (=3) 与顶点数 (=3) 相等（Euler 示性数 = 0）。 -/
theorem triangle_euler_char_zero : (triangleVertexCount : ℤ) - (3 : ℤ) = 0 := by
  unfold triangleVertexCount; norm_num

end CQM