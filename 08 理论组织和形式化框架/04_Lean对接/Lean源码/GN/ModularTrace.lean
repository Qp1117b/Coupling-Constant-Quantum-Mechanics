import GN.AdeleJacobian
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# 模流迹路线（ModularTrace）

探索文档 `10 探索/CQM_探索_量纲群论与自守形式.md` §十八 的 Lean 落地。

## 内容与地位

- `jacobianFromTrace tr = exp(-2/tr)`：把 Adele Jacobian 的指数读作
  `Tr Ĥ⁻¹` 的倒数，而不是 `ln det`（路线修正）。
- `jacobianFromTrace_sq`：因子 2 的平方分解
  `exp(-2/tr) = (exp(-1/tr))^2`（**纯实分析定理**）。
- `log_jacobianFromTrace`：对数形式 `ln 𝒥 = -2/tr`（**定理**）。
- `traceHinv_eq_spectralQuantum`：`Tr Ĥ⁻¹ = ☯` 的记录为 `Prop`，
  **不是公理**；它是 §十八 T1 的待证缺口。
- `adeleJacobian_eq_jacobianFromTrace`：在 Tate 自对偶、构造 10.1 与
  `Tr Ĥ⁻¹ = ☯` 三者同时成立时，两条路线给出同一 Jacobian
  （**条件定理**）。

## 诚实边界

- `jacobianFromTrace` 是**定义**，不承担"为何取倒数"的解释；
  该选择在探索文档中标为 CQM 构造假设。
- `traceHinv_eq_spectralQuantum` 只是把缺口写成命题，不宣称成立；
  真正的谱和恒等式在 `SpectralGeometry.RiemannXi` 中登记为待 Hadamard 积
  形式化的开放缺口（条件于 RH），当前不作为公理断言。
- 本模块不新增任何 `axiom`。
-/

open Real

namespace CQM
namespace GN

noncomputable section

/-- CQM 壳层测度 `e^{-u}du` 的模参数：`β = 1`（定义，非定理）。 -/
noncomputable def kmsBeta : ℝ := 1

/-- 模参数为正。 -/
theorem kmsBeta_pos : 0 < kmsBeta := by
  unfold kmsBeta
  norm_num

/-- 由逆谱的迹读出的 Adele Jacobian：`𝒥 = exp(-2 / Tr Ĥ⁻¹)`。 -/
noncomputable def jacobianFromTrace (tr : ℝ) : ℝ := Real.exp (-2 / tr)

/-- 因子 2 的平方分解（纯实分析）：

    `exp(-2/tr) = (exp(-1/tr))^2`

    即 §十八 中 `e^{-2/☯} = (e^{-1/☯})^2` 的一般形式。 -/
theorem jacobianFromTrace_sq (tr : ℝ) :
    jacobianFromTrace tr = (Real.exp (-1 / tr)) ^ 2 := by
  unfold jacobianFromTrace
  have h : (-2 : ℝ) / tr = (-1 : ℝ) / tr + (-1 : ℝ) / tr := by ring
  rw [h, Real.exp_add]
  ring

/-- 正向性：`𝒥 > 0`。 -/
theorem jacobianFromTrace_pos (tr : ℝ) : 0 < jacobianFromTrace tr :=
  Real.exp_pos _

/-- 对数形式：`ln 𝒥 = -2/tr`。 -/
theorem log_jacobianFromTrace (tr : ℝ) :
    Real.log (jacobianFromTrace tr) = -2 / tr := by
  unfold jacobianFromTrace
  rw [Real.log_exp]

/-- 迹路线的缺口（记录，非公理）：`Tr Ĥ⁻¹ = ☯`。

    §十八 T1 的任务是证明此命题；本模块只把它写成可判定的 `Prop`。 -/
def traceHinv_eq_spectralQuantum (tr : ℝ) : Prop := tr = spectralQuantum

/-- 若迹等于 ☯，则迹路线与闭式路线给出同一 Jacobian。 -/
theorem jacobianFromTrace_eq_of_trace_eq_qi (tr : ℝ)
    (htr : traceHinv_eq_spectralQuantum tr) :
    jacobianFromTrace tr = Real.exp (-2 / spectralQuantum) := by
  unfold traceHinv_eq_spectralQuantum at htr
  unfold jacobianFromTrace
  rw [htr]

/-- [条件定理] 在 Tate 自对偶、构造 10.1 与 `Tr Ĥ⁻¹ = ☯` 同时成立时，
    Adele Jacobian 与迹路线一致。 -/
theorem adeleJacobian_eq_jacobianFromTrace
    (hself : detDinf * detDprod = 1) (hpos : 0 < detDprod)
    (hqi : adeleSpectralLog_eq_inv_qi) (tr : ℝ)
    (htr : traceHinv_eq_spectralQuantum tr) :
    adeleJacobian = jacobianFromTrace tr := by
  calc adeleJacobian = Real.exp (-2 / spectralQuantum) :=
        (adeleJacobian_exp_form hself hpos hqi).2
    _ = jacobianFromTrace tr :=
        (jacobianFromTrace_eq_of_trace_eq_qi tr htr).symm

end

end GN
end CQM
