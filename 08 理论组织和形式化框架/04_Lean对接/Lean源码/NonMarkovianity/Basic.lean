import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# 非马尔可夫性的分布式关系载体：基础定义 (Basic)

对应研究文档：`04 前沿研究/CQM_前沿研究_非马尔可夫性的分布式关系载体.md`。

本模块把该文的四个基础概念写成类型与谓词：

- 历史沉淀 `D : V → α`（§2.1）：历史演化在节点上沉淀的局域关系数据；
- 单点共时投影 `π : α → β`（§2.2）：把局域关系数据压成单点共时观测量；
- 未来法则 `law : (V → α) → Ω`（§2.3）：由历史决定的未来统计对象；
- 充分性 `Sufficient π law`（§2.3）：投影相同的两个历史给出相同的未来法则。

## 检验结论（对应原文 §3.2）

原文由“`π` 非单射”推出“单点共时态不充分”。本模块给出：

- `sufficient_of_injective`：单射投影必充分；
- `insufficient_imp_not_injective`：不充分必蕴含投影非单射；
- `noninjectivity_not_implying_insufficiency`：存在投影非单射却仍然充分的模型。

因此非单射只是不充分的**必要**条件，不是充分条件；原文这一推理步骤不成立，
其正确内容只有“投影有损”。真正的判据是投影纤维内未来法则不同
（`Insufficient` 的定义，亦即原文命题 C）。

## 与阈值命题的关系

`sufficient_of_factor`：充分性可以从粗统计量传递到细统计量。
这是文档 §3.6 尺度阈值命题的单调性来源（见 `NonMarkovianity.ScaleThreshold`）。
-/

namespace CQM
namespace NonMarkovianity

/-- 历史沉淀：把每个节点 $v$ 映到其历史演化沉淀下的局域关系数据 $D(v)$。 -/
abbrev Sedimentation (V α : Type) := V → α

/-- 未来法则：历史到未来统计对象的映射。`Ω` 可以是概率分布、可观测量的
期望值等；本定义只使用其相等关系，不预设统计结构。 -/
abbrev FutureLaw (V α Ω : Type) := (V → α) → Ω

/-- 单点共时投影 $\pi:\{D(v)\}\mapsto\{\varphi(v)\}$：逐点作用。 -/
def project {V α β : Type} (π : α → β) (D : V → α) : V → β :=
  fun v => π (D v)

/-- 充分性：凡单点共时投影相同的历史，未来法则相同，
即未来法则经由投影 `π` 分解。 -/
def Sufficient {V α β Ω : Type} (π : α → β) (law : FutureLaw V α Ω) : Prop :=
  ∀ D D' : V → α, (∀ v : V, π (D v) = π (D' v)) → law D = law D'

/-- 不充分：投影的纤维内存在未来法则不同的两个历史。
这是原文命题 C 的形式，也是“非马尔可夫性”的判据。 -/
def Insufficient {V α β Ω : Type} (π : α → β) (law : FutureLaw V α Ω) : Prop :=
  ∃ D D' : V → α, (∀ v : V, π (D v) = π (D' v)) ∧ law D ≠ law D'

/-- 单射投影必充分：若 `π` 单射，则投影相同的两个历史逐点相同，
未来法则自然相同。等价地（逆否）：不充分 ⇒ 非单射。 -/
theorem sufficient_of_injective {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) (hinj : Function.Injective π) : Sufficient π law := by
  intro D D' h
  have hD : D = D' := funext fun v => hinj (h v)
  rw [hD]

/-- 不充分蕴含投影非单射：这是原文命题 B 唯一成立的方向。
证明：若 `π` 单射，则与不充分矛盾。 -/
theorem insufficient_imp_not_injective {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) (h : Insufficient π law) : ¬ Function.Injective π := by
  intro hinj
  obtain ⟨D, D', hproj, hlaw⟩ := h
  exact hlaw (sufficient_of_injective π law hinj D D' hproj)

/-- 不充分性与纤维判据等价：`Insufficient` 就是 `¬ Sufficient` 的展开形式。 -/
theorem insufficient_iff_fiber {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) : Insufficient π law ↔ ¬ Sufficient π law := by
  classical
  constructor
  · rintro ⟨D, D', hproj, hlaw⟩ hsuf
    exact hlaw (hsuf D D' hproj)
  · intro h
    by_contra hcon
    apply h
    intro D D' hproj
    by_contra hne
    exact hcon ⟨D, D', hproj, hne⟩

/-- 充分性从粗统计量传递到细统计量：若 `φ = g ∘ ψ`（`φ` 比 `ψ` 粗）
且粗统计量 `φ` 充分，则细统计量 `ψ` 也充分。

反向不成立：细统计量充分不能保证粗统计量充分（粗化会丢信息）。
这一单向传递给出尺度阈值命题所需的单调性。 -/
theorem sufficient_of_factor {V α β γ Ω : Type} (φ : α → γ) (ψ : α → β)
    (g : β → γ) (law : FutureLaw V α Ω)
    (hfactor : ∀ a : α, φ a = g (ψ a)) (hφ : Sufficient φ law) :
    Sufficient ψ law := by
  intro D D' hψ
  apply hφ D D'
  intro v
  rw [hfactor (D v), hfactor (D' v), hψ v]

/-- 反例：投影非单射，却仍是充分统计量。

取 `V = Unit`，`α = Bool × Bool`（局域关系数据的两个分量），
`β = Bool`（只读取第一分量），`π = Prod.fst`；未来法则只依赖第一分量。

`π` 显然非单射（`(true, false)` 与 `(true, true)` 同像），
但投影相同 ⇒ 第一分量相同 ⇒ 未来法则相同，故充分。

结论：非单射不能推出不充分。原文 §3.2 的推理步骤不成立，
判据只能是纤维条件（`insufficient_iff_fiber`）。 -/
theorem noninjectivity_not_implying_insufficiency :
    ∃ (π : Bool × Bool → Bool) (law : FutureLaw Unit (Bool × Bool) Bool),
      ¬ Function.Injective π ∧ Sufficient π law := by
  refine ⟨Prod.fst, fun D => (D ()).1, ?_, ?_⟩
  · intro hinj
    have h : ((true, false) : Bool × Bool) = (true, true) := hinj rfl
    exact Bool.false_ne_true (congrArg Prod.snd h)
  · intro D D' h
    exact h ()

end NonMarkovianity
end CQM
