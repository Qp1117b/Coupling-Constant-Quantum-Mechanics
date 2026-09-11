import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Module.LinearMap.Basic

/-!
# 再生产算符 (Reproduction Operator)

CQM 的第二公理：有限本体通过再生产维持自身存在。

## 公理
- 再生产算符 `μ̂` 是线性算子，满足 `μ̂² = μ̂`（幂等性）
- 再生产是投影：将状态投影到"存在"子空间

## 物理意义
`μ̂` 的形式化表达了"有限本体维持自身存在"的操作。
幂等性 `μ̂² = μ̂` 意味着：再生产一次与再生产多次的效果相同——
存在一旦被维持，不需要二次维持。

## 参考文献
- ruster (2026). CNT 完整研究. Zenodo. DOI: 10.5281/zenodo.20804380.
-/

/-- 再生产算符：作用于 Hilbert 空间 H 上的幂等线性算子。
    `muHat² = muHat` 表示"再生产一次 = 再生产多次"。
    使用 `ℝ` 作为标量域（CQM 中耦合强度为实数值）。 -/
class ReproductionOperator (H : Type*) [AddCommGroup H] [Module ℝ H] where
  /-- 再生产算符 μ̂ : H → H -/
  muHat : H →ₗ[ℝ] H
  /-- 幂等性：μ̂² = μ̂ -/
  idempotent : ∀ x, muHat (muHat x) = muHat x

namespace ReproductionOperator

variable {H : Type*} [AddCommGroup H] [Module ℝ H] [ReproductionOperator H]

/-- 已再生产态：满足 muHat ψ = ψ 的状态（再生产的不动点） -/
def isReproduced (ψ : H) : Prop := muHat ψ = ψ

/-- 存在子空间：所有已再生产态的集合 -/
def existenceSubspace : Set H := {ψ | isReproduced ψ}

/-- 幂等性定理 -/
theorem muHat_idempotent (x : H) : muHat (muHat x) = muHat x :=
  ReproductionOperator.idempotent x

/-- 零向量是已再生产态 -/
theorem zero_isReproduced : isReproduced (0 : H) := by
  dsimp [isReproduced]
  rw [map_zero]

/-- 已再生产态的和仍是已再生产态（存在子空间是加法子群） -/
theorem add_isReproduced {x y : H} (hx : isReproduced x) (hy : isReproduced y) : isReproduced (x + y) := by
  dsimp [isReproduced] at hx hy ⊢
  rw [map_add, hx, hy]

/-- 已再生产态的标量倍仍是已再生产态 -/
theorem smul_isReproduced {ψ : H} (h : isReproduced ψ) (c : ℝ) : isReproduced (c • ψ) := by
  dsimp [isReproduced] at h ⊢
  rw [map_smul, h]

/-- 再生产算符的像 = 存在子空间 -/
theorem image_eq_existenceSubspace : Set.range (muHat (H := H)) = existenceSubspace := by
  ext x
  constructor
  · rintro ⟨y, rfl⟩
    dsimp [existenceSubspace, Set.mem_setOf_eq, isReproduced]
    rw [muHat_idempotent]
  · intro h
    dsimp [existenceSubspace, Set.mem_setOf_eq, isReproduced] at h
    exact ⟨x, h⟩

end ReproductionOperator