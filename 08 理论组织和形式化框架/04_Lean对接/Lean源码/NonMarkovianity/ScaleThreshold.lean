import NonMarkovianity.Markovization

/-!
# 尺度阈值命题 (ScaleThreshold)

对应研究文档 `04 前沿研究/CQM_前沿研究_分布式不对易关系与非马尔可夫性.md` §5.1。

原文结论“单点共时态不充分”在文档中收紧为阈值命题：

$$\exists\,\ell_*:\quad \ell<\ell_* \text{ 时 } \mathcal{S}_\ell \text{ 充分},
\qquad \ell\ge\ell_* \text{ 时存在反例}.$$

本模块把“$\ell$ 是粗化尺度，越大越粗”作为约定：`statistic ℓ'`（$\ell'\ge\ell$）
由 `statistic ℓ` 复合得到，粗统计量不携带细统计量的额外信息。

- `threshold_of_antitone_sufficiency`：纯序论阈值定理（不依赖模型细节）；
- `scaleSufficiency_antitone`：尺度族上充分性随粗化单调递减；
- `scale_threshold`：把上述两者合成尺度的阈值命题；
- `threshold_instance`：给出满足前提的具体剖面，说明阈值定理不是空转。

阈值 $\ell_*$ 的存在性本身不依赖 CQM；它是否有限、取值多少，
属文档 §9.1 的 T6【待推】，本模块不给出数值。
-/

namespace CQM
namespace NonMarkovianity

/-- 尺度充分性剖面：`S ℓ` 表示“尺度 `ℓ` 的单时刻统计量充分”。 -/
abbrev SufficiencyProfile := ℕ → Prop

/-- 阈值存在定理：若充分性随尺度单调递减（粗尺度充分 ⇒ 细尺度充分），
尺度 0 充分，且存在某个尺度不充分，则存在最小失效尺度 `ℓ* > 0`：

- 所有更细的尺度（`ℓ < ℓ*`）都充分；
- 所有不细于 `ℓ*` 的尺度（`ℓ ≥ ℓ*`）都不充分。

证明用 `Nat.find` 取最小失效尺度。 -/
theorem threshold_of_antitone_sufficiency (S : SufficiencyProfile)
    (hanti : ∀ ℓ ℓ' : ℕ, ℓ ≤ ℓ' → S ℓ' → S ℓ)
    (h0 : S 0) (hN : ∃ N : ℕ, ¬ S N) :
    ∃ ℓstar : ℕ, 0 < ℓstar ∧ (∀ ℓ : ℕ, ℓ < ℓstar → S ℓ) ∧
      (∀ ℓ : ℕ, ℓstar ≤ ℓ → ¬ S ℓ) := by
  classical
  have hex : ∃ n : ℕ, ¬ S n := hN
  refine ⟨Nat.find hex, ?_, ?_, ?_⟩
  · exact (Nat.find_pos hex).mpr (fun h => h h0)
  · intro ℓ hℓ
    by_contra h
    exact absurd (Nat.find_min' hex h) (Nat.not_le.mpr hℓ)
  · intro ℓ hℓ hS
    exact (Nat.find_spec hex) (hanti (Nat.find hex) ℓ hℓ hS)

/-- 尺度族：每个尺度给出一个满足支撑半径约束的单时刻统计量，
且更大尺度（更粗）的统计量由更小尺度（更细）的统计量复合得到。 -/
structure ScaleFamily (V α β : Type) where
  /-- 节点图距离 -/
  dist : GraphDistance V
  /-- 每个尺度的单时刻统计量 -/
  statistic : ℕ → SingleTimeStatistic V α β
  /-- 每个尺度的统计量满足相应半径的局域性 -/
  locality : ∀ ℓ : ℕ, LocalAt dist ℓ (statistic ℓ)
  /-- 粗化相容性：`ℓ ≤ ℓ'` 时，粗统计量 `ℓ'` 经由细统计量 `ℓ` 因子化 -/
  coarser : ∀ (ℓ ℓ' : ℕ), ℓ ≤ ℓ' → ∃ g : β → β,
    ∀ (D : V → α) (v : V), statistic ℓ' D v = g (statistic ℓ D v)

/-- 一般统计量的充分性：统计量取值相同的历史给出相同的未来法则。 -/
def SufficientStat {H β Ω : Type} (stat : H → β) (law : H → Ω) : Prop :=
  ∀ a a' : H, stat a = stat a' → law a = law a'

/-- 充分性从粗统计量传递到细统计量（一般形式）。 -/
theorem sufficientStat_of_factor {H β γ Ω : Type} (φ : H → γ) (ψ : H → β)
    (g : β → γ) (law : H → Ω) (hfactor : ∀ a : H, φ a = g (ψ a))
    (hφ : SufficientStat φ law) : SufficientStat ψ law := by
  intro a a' hψ
  apply hφ a a'
  rw [hfactor a, hfactor a', hψ]

/-- 尺度族的充分性剖面。 -/
def scaleSufficiency {V α β Ω : Type} (F : ScaleFamily V α β)
    (law : FutureLaw V α Ω) (ℓ : ℕ) : Prop :=
  SufficientStat (fun D => fun v => F.statistic ℓ D v) law

/-- 充分性随粗化单调递减：粗尺度充分则细尺度充分。
由 `sufficient_of_factor` 与 `ScaleFamily.coarser` 得到。 -/
theorem scaleSufficiency_antitone {V α β Ω : Type} (F : ScaleFamily V α β)
    (law : FutureLaw V α Ω) :
    ∀ ℓ ℓ' : ℕ, ℓ ≤ ℓ' → scaleSufficiency F law ℓ' → scaleSufficiency F law ℓ := by
  intro ℓ ℓ' hle hcoarse
  obtain ⟨g, hg⟩ := F.coarser ℓ ℓ' hle
  let fine : (V → α) → V → β := fun D v => F.statistic ℓ D v
  let coarse : (V → α) → V → β := fun D v => F.statistic ℓ' D v
  let G : (V → β) → V → β := fun b v => g (b v)
  have hfactor : ∀ a : V → α, coarse a = G (fine a) := by
    intro a
    funext v
    exact hg a v
  change SufficientStat fine law
  exact sufficientStat_of_factor coarse fine G law hfactor hcoarse

/-- 尺度阈值：若细端（尺度 0）充分、某个粗端失效，则存在失效阈值 `ℓ*`。
这就是文档 §3.3 的阈值命题。 -/
theorem scale_threshold {V α β Ω : Type} (F : ScaleFamily V α β)
    (law : FutureLaw V α Ω) (h0 : scaleSufficiency F law 0)
    (hN : ∃ N : ℕ, ¬ scaleSufficiency F law N) :
    ∃ ℓstar : ℕ, 0 < ℓstar ∧
      (∀ ℓ : ℕ, ℓ < ℓstar → scaleSufficiency F law ℓ) ∧
      (∀ ℓ : ℕ, ℓstar ≤ ℓ → ¬ scaleSufficiency F law ℓ) :=
  threshold_of_antitone_sufficiency (scaleSufficiency F law)
    (scaleSufficiency_antitone F law) h0 hN

/-- 阈值的具体实例：取 `S ℓ` 为 `ℓ = 0`。
`S 0` 成立、`S 1` 不成立、且 `S` 对粗化单调，满足阈值定理的全部前提，
得到 `ℓ* = 1`。这说明阈值定理的前提可同时满足，不是空转。 -/
theorem threshold_instance :
    ∃ ℓstar : ℕ, 0 < ℓstar ∧
      (∀ ℓ : ℕ, ℓ < ℓstar → ℓ = 0) ∧
      (∀ ℓ : ℕ, ℓstar ≤ ℓ → ℓ ≠ 0) := by
  have hanti : ∀ ℓ ℓ' : ℕ, ℓ ≤ ℓ' → ℓ' = 0 → ℓ = 0 := by
    intro ℓ ℓ' hle h
    omega
  have h0 : (0 : ℕ) = 0 := rfl
  have hN : ∃ N : ℕ, N ≠ 0 := ⟨1, by norm_num⟩
  exact threshold_of_antitone_sufficiency (fun ℓ => ℓ = 0) hanti h0 hN

end NonMarkovianity
end CQM
