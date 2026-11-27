import SuperconductivityChain.Basic

/-!
# 阶段 6：记忆核起点（环 14 / 14.A）

形式化相位核 `K_i(t)=f(τ_i+t)` 与固定平移关系：
`τ_i = τ_j + c` 时 `K_i(t)=K_j(t+c)`。这是 (14.3)/(24.2) 的代数骨架。
BCS 延迟配对的同刻度、物理 `K` 与质数形式的焊接不证。

缺口：`M9`、`审-9`、`审-15`、`临-8`、`临-12`、`临-14`、`临-15`、`M1`。
-/

namespace CQM.SuperconductivityChain

variable {V : Type*}

/-- 记忆核的抽象类型：时间到复振幅。 -/
abbrev MemoryKernel := ℝ → ℂ

/-- 环 14：单相位核，`K_i(t) = f(τ_i + t)`；`f` 是共享的谱函数。 -/
noncomputable def phaseKernel (f : ℝ → ℂ) (τ : V → ℝ) (i : V) (t : ℝ) : ℂ :=
  f (τ i + t)

/-- 环 14.3/24.2：冻结给出固定平移，`τ_i = τ_j + c → K_i(t)=K_j(t+c)`。 -/
theorem phaseKernel_shift {f : ℝ → ℂ} {τ : V → ℝ} {i j : V} {c t : ℝ}
    (h : τ i = τ j + c) :
    phaseKernel f τ i t = phaseKernel f τ j (t + c) := by
  unfold phaseKernel
  have harg : τ i + t = τ j + (t + c) := by linarith
  rw [harg]

/-- 特例：`τ_i = τ_j` 时两核逐点相等；这对应 `c_ij=0`，不能由锚推出。 -/
theorem phaseKernel_eq_of_eq {f : ℝ → ℂ} {τ : V → ℝ} {i j : V}
    (h : τ i = τ j) (t : ℝ) :
    phaseKernel f τ i t = phaseKernel f τ j t := by
  simpa using phaseKernel_shift (f := f) (τ := τ) (i := i) (j := j)
    (c := 0) (t := t) (by simpa using h)

end CQM.SuperconductivityChain
