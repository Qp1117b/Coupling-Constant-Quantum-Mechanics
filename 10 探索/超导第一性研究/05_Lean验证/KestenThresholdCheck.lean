/-
  R64：Kesten 键阈值 pc=1/2 核对的代数核
  ===============================================================================
  2D 方格键渗流 pc=1/2（Kesten 自对偶精确）。MC 核对 L=16/24/32 -> 0.5。
  本文件承载阈值结构（自对偶对合、有限尺寸偏差量级）的代数骨架；
  精确 MC 数值在 Python（标准库并查集）。

  纪律：无 axiom／sorry／admit／native_decide／unsafe。
-/
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.NormNum
import Mathlib.Data.Real.Basic

namespace CQM.KestenCheck

/-- 键阈值精确值 pc = 1/2（Kesten，自对偶）。 -/
def pcBond : ℚ := (1 : ℚ) / 2

theorem pc_bond_value : pcBond = (1 : ℚ) / 2 := rfl

/-- 自对偶：p 与 1-p 对偶，阈值在不动点 p=1/2。截面：f(p)=1-p 的不动点 p=1/2。 -/
def dual (p : ℚ) : ℚ := 1 - p

theorem self_dual_fixed_point : dual pcBond = pcBond := by
  unfold dual pcBond
  norm_num

/-- 座阈值 > 键阈值（0.592746 > 0.5），二者不可混用（审-4）。 -/
def pcSite : ℚ := 592746 / 1000000

theorem site_gt_bond : pcBond < pcSite := by
  unfold pcBond pcSite
  norm_num

/-- 有限尺寸偏差 ~ L^{-3/4}（主链 §0.2 读数层）。截面：偏差单调减。 -/
def finiteSizeDev (L : ℚ) : ℚ := 1 / L  -- 简化截面（真实指数 3/4）

theorem dev_decreases (L1 L2 : ℚ) (hL1 : 0 < L1) (h : L1 < L2) :
    finiteSizeDev L2 < finiteSizeDev L1 := by
  unfold finiteSizeDev
  have hL2 : 0 < L2 := by linarith
  field_simp [hL1.ne', hL2.ne']
  exact h

-- 边界注记（写文档，不构造伪形式化）：
-- Kesten 定理是外部标准数学（已标源），本文件只载阈值/自对偶结构骨架。
-- MC 数值（L=16/24/32 -> 0.5017/0.4997/0.5006）在 Python。
-- 不改缺口、不给 Tc。

end CQM.KestenCheck
