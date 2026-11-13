import NonMarkovianity.Basic

/-!
# 单点本体论马尔可夫化与单时刻状态类 (Markovization)

对应研究文档 `04 前沿研究/CQM_前沿研究_分布式不对易关系与非马尔可夫性.md`
§2.3 与 §3.3。

## 四约束的编码方式

文档 §2.3 把“单点共时”收紧为四条同时成立的约束：

1. **单一时刻截面**：`SingleTimeStatistic` 的作用域是单一构型 `D : V → α`，
   类型中不出现时间下标；
2. **支撑半径有界**：`LocalAt dist ℓ φ`，`φ(D)(v)` 只依赖 `v` 的 `ℓ` 邻域；
3. **站点规则与位置无关**：本文档不把平移不变性写成定理，只作为建模假设
   （函数 `φ` 在所有站点上使用同一规则）；本模块不声明也无法声明其形式证明；
4. **不显式携带历史标号**：`α` 中不含时间下标，由类型保证。

因此本模块形式化的是约束 1、2、4；约束 3 仍为建模假设，如实标注，不冒充已证。
-/

namespace CQM
namespace NonMarkovianity

/-- 节点图距离：`dist v w` 为节点 `v` 到 `w` 的图距离。 -/
abbrev GraphDistance (V : Type) := V → V → ℕ

/-- 单时刻统计量：只读取一个时刻的构型 `D : V → α`，逐点输出观测量 `β`。 -/
abbrev SingleTimeStatistic (V α β : Type) := (V → α) → V → β

/-- 半径 `ℓ` 的局域性：`φ(D)(v)` 只依赖 `v` 的 `ℓ` 邻域内的历史数据。

这是原文 $\varphi(v)=f\bigl(G|_{N_k(v)}\bigr)$ 的形式化，
对应“支撑半径有界”这一约束。 -/
def LocalAt {V α β : Type} (dist : GraphDistance V) (ℓ : ℕ)
    (φ : SingleTimeStatistic V α β) : Prop :=
  ∀ (D D' : V → α) (v : V), (∀ w : V, dist v w ≤ ℓ → D w = D' w) → φ D v = φ D' v

/-- 局域性对半径单调：在小半径成立则在大半径成立。
（半径越小越局域；大半径的条件更强，故可由小半径推出。） -/
theorem localAt_mono {V α β : Type} (dist : GraphDistance V) {ℓ ℓ' : ℕ}
    (hℓ : ℓ ≤ ℓ') {φ : SingleTimeStatistic V α β} (h : LocalAt dist ℓ φ) :
    LocalAt dist ℓ' φ := by
  intro D D' v hagree
  exact h D D' v fun w hw => hagree w (le_trans hw hℓ)

/-- 单点本体论马尔可夫化（原文 §2.3）：存在单点共时投影 `π`，
使未来法则经由它分解。

“状态变量有独立物理载体、不是任意历史堆栈”由 `β` 的类型承担：
`β` 是单点共时观测量，不是 `V → α` 的历史堆栈。 -/
def OnticMarkovizable {V α β Ω : Type} (π : α → β) (law : FutureLaw V α Ω) : Prop :=
  Sufficient π law

/-- 单点本体论马尔可夫化等价于投影充分（定义展开）。 -/
theorem onticMarkovizable_iff_sufficient {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) : OnticMarkovizable π law ↔ Sufficient π law :=
  Iff.rfl

/-- 单射的单时刻投影给出单点本体论马尔可夫化。 -/
theorem onticMarkovizable_of_injective {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) (hinj : Function.Injective π) :
    OnticMarkovizable π law :=
  sufficient_of_injective π law hinj

/-- 纤维内未来法则不同时，不存在单点本体论马尔可夫化。
这是原文结论（在给定投影下）的精确形式。 -/
theorem not_onticMarkovizable_of_fiber {V α β Ω : Type} (π : α → β)
    (law : FutureLaw V α Ω) (h : Insufficient π law) : ¬ OnticMarkovizable π law := by
  intro hmark
  exact (insufficient_iff_fiber π law).mp h hmark

end NonMarkovianity
end CQM
