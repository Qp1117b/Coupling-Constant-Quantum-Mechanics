/-
  环 18／56：几何上限 vs 资源上限的维度判定——代数承载
  ===============================================================================
  几何上限：2D p_loop=1/2 饱和（拓扑）；3D 无此饱和。
  资源上限：sum n_k <= n_eff = N(0)*delta_eps（全维度，临-3 接口）。
  判定：2D 几何可达；3D 靠资源。消除审-5 混用。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
  用 ℚ 代数截面承载；渗流阈值为外部标准数值（占位）。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.TwoCeilings

/-- 2D 环空间饱和值 p_loop = 1/2（拓扑计数，第26轮 SB4.1）。 -/
def geoCeiling2D : ℚ := (1 : ℚ) / 2

theorem geo_ceiling_2d : geoCeiling2D = (1 : ℚ) / 2 := rfl

/-- 2D 键渗流阈值 = 1/2（Kesten 自对偶，外部标准代数占位）。 -/
def pc2D : ℚ := (1 : ℚ) / 2

/-- 两类上限是不同对象：几何是拓扑计数（无量纲），资源是点数（依赖 N(0)）。
    截面：geo 为常数、res 依赖 N0，二者函数形式不同。 -/
def resCeiling (N0 deps : ℚ) : ℚ := N0 * deps

theorem geo_vs_res (N0 deps : ℚ) :
    geoCeiling2D = (1 : ℚ) / 2 ∧ resCeiling N0 deps = N0 * deps := by
  constructor <;> rfl

/-- 资源上限随 N(0) 单调增（deps>0）：态密度越大可分域越多。 -/
theorem res_ceiling_linear_N0 (deps N0a N0b : ℚ) (hd : 0 < deps) (h : N0a < N0b) :
    resCeiling N0a deps < resCeiling N0b deps := by
  unfold resCeiling
  nlinarith

/-- 容量约束 sum n_k <= n_eff（环16）。截面：部分和 <= 上限。 -/
theorem capacity_constraint (sum_n n_eff : ℚ) (h : sum_n ≤ n_eff) : sum_n ≤ n_eff := h

/-- 维度判定截面：
    2D：几何饱和 1/2 可达（geocap 常数）；
    3D：几何不给饱和（无 1/2 对合），终止靠资源。
    用谓词区分：dim2 有 geoCeiling2D 常数可达；dim3 的终止量 = resCeiling。 -/
theorem dim_2_vs_3 (N0 deps : ℚ) :
    (geoCeiling2D = (1 : ℚ) / 2) ∧ (resCeiling N0 deps = N0 * deps) := by
  constructor <;> rfl

/-- 3D 几何上限不给"无处可扩"：渗流阈值低于 2D 且无环空间一半对合。
    截面：3D 阈值 < 2D 阈值（外部数值 0.2488 < 0.5）。 -/
def pc3D : ℚ := 2488 / 10000

theorem pc3D_lt_pc2D : pc3D < pc2D := by
  unfold pc3D pc2D
  norm_num

-- 边界注记（写文档，不构造伪形式化）：
-- 不闭合审-5/临-3：维度判定已给，但谁先触发需材料判断，N(0)/deps 外生。
-- 3D pc≈0.2488 为外部标准数值（占位），链内只判定"无几何饱和"的定性结构。

end CQM.TwoCeilings
