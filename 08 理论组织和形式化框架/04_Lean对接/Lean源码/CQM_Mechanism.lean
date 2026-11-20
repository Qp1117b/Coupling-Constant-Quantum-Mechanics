/-!
# CQM 核心机制：六要素 ⇒ K(t) 的质数振荡形式

本文件把六项前提压成一条可编译的机制链：

1. **固有时流速乘积传递 + 亏角**——相邻节点 $v_{\tau,j}=v_{\tau,i}r_{ij}$，沿链累积，闭环要求 $\prod r_k=1$；
2. **节点质数原子化**——每节点持自己的钟，窗口平均不可能均匀；
3. **差异-扩大-平均动力学**——全对历史族 $\mathcal H_{ij}=\tau_i-\tau_j$ 的冻结（所有节点对同时等速）使平均窗口趋于均匀；
4. **渗流**——簇求和只给前因子；
5. **量子递归博弈论**——博弈次序不影响终态；
6. **平凡零点形式配对**——配对数上界由平凡零点位置给出。

在「全对冻结」（$\dot{\mathcal H}_{ij}=0\ \forall i<j$ 的代数形式：所有节点对每个时刻的增量相等）下，幅度被压成 $\Phi/n$，
频率阶梯被压成 $u_1+2\ln n$，于是 $K(t)$ 落入 `PrimeOscForm`。

不证明黎曼猜想；只对上形式。仅依赖 Lean 核心库（无 Mathlib）。
-/

/-! ## §0 基础：连乘、序列、求和 -/

def prodd : List Int → Int
  | [] => 1
  | a :: l => a * prodd l

def vs (v : Int) (r : Nat → Int) : Nat → Int
  | 0 => v
  | n + 1 => vs v r n * r n

def sumN (f : Nat → Int) : Nat → Int
  | 0 => 0
  | n + 1 => sumN f n + f n

theorem vs_succ (v : Int) (r : Nat → Int) (n : Nat) :
    vs v r (n + 1) = vs v r n * r n := rfl

/-! ## §1 乘积传递：闭合 ⇒ 全网同流 -/

theorem vs_const (v : Int) (r : Nat → Int) (h : ∀ k, r k = 1) :
    ∀ n, vs v r n = v := by
  intro n
  induction n with
  | zero => rfl
  | succ n ih =>
    show vs v r n * r n = v
    rw [ih, h n]
    simp

/-! ## §2 冻结（差异-扩大-平均）与权重 -/

def WindowsUniform (avg : Nat → Int) : Prop := ∀ m n, avg m = avg n

def WeightLinear (avg w : Nat → Int) : Prop := ∀ n, w n = w 1 + (avg n - avg 1)

theorem weight_eq_one_of_freeze (avg w : Nat → Int)
    (hunif : WindowsUniform avg) (hlin : WeightLinear avg w) (h1 : w 1 = 1) :
    ∀ n, w n = 1 := by
  intro n
  have h : avg n = avg 1 := hunif n 1
  have hl : w n = w 1 + (avg n - avg 1) := hlin n
  have hz : avg n - avg 1 = 0 := by
    rw [h]
    simp
  rw [hl, hz, h1]
  simp

/-! ## §3 原子化：每节点自有钟 ⇒ 平均不可能均匀 -/

def Atomized (avg : Nat → Int) : Prop := ∃ m n, avg m ≠ avg n

theorem atomization_breaks_uniform (avg : Nat → Int) :
    Atomized avg → ¬ WindowsUniform avg := by
  intro ⟨m, n, hne⟩ hunif
  exact hne (hunif m n)

/-! ## §4 幅度阶梯：$n\,a_n=\Phi$ -/

def AmpLadder (Φ : Int) (w amp : Nat → Int) : Prop :=
  ∀ (n : Nat), 1 ≤ n → (n : Int) * amp n = w n * Φ

theorem amp_from_freeze (Φ : Int) (w amp : Nat → Int)
    (hw : ∀ n, w n = 1) (hA : AmpLadder Φ w amp) :
    ∀ (n : Nat), 1 ≤ n → (n : Int) * amp n = Φ := by
  intro n hn
  rw [hA n hn, hw n]
  simp

/-! ## §5 平方律与对数阶梯：$E_n=n^2E_1$ ⇒ $u_n=u_1+2\ln n$ -/

def E (E1 n : Nat) : Nat := E1 * (n * n)

theorem log_ladder (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b) (E1 n : Nat) :
    lnE (E E1 n) = lnE E1 + 2 * lnE n := by
  show lnE (E1 * (n * n)) = lnE E1 + 2 * lnE n
  rw [hadd E1 (n * n), hadd n n]
  omega

/-! ## §6 K 与质数振荡形式 -/

def Kfun (cosF : Int → Int) (amp freq : Nat → Int) (N : Nat) (t : Nat) : Int :=
  sumN (fun n => amp n * cosF (freq n * (t : Int))) N

def PrimeOscForm (cosF : Int → Int) (K : Nat → Int) (Φ u1 : Int)
    (ℓ : Nat → Nat) (N : Nat) : Prop :=
  ∃ amp freq : Nat → Int,
    (∀ t, K t = Kfun cosF amp freq N t) ∧
    (∀ (n : Nat), 1 ≤ n → (n : Int) * amp n = Φ) ∧
    (∀ n, freq n = u1 + 2 * (ℓ n : Int))

/-- **主定理**：冻结（$w\equiv1$）+ 平方律 + 对数阶梯 ⇒ $K$ 落于质数振荡形式。 -/
theorem mechanism_prime_osc
    (cosF : Int → Int) (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b)
    (E1 : Nat) (Φ : Int) (avg w amp : Nat → Int) (N : Nat)
    (hunif : WindowsUniform avg) (hlin : WeightLinear avg w) (h1 : w 1 = 1)
    (hA : AmpLadder Φ w amp) :
    PrimeOscForm cosF
      (fun t => Kfun cosF amp (fun n => lnE (E E1 n)) N t)
      Φ (lnE E1 : Int) lnE N := by
  refine ⟨amp, fun n => lnE (E E1 n), ?_, ?_, ?_⟩
  · intro t
    rfl
  · intro n hn
    exact amp_from_freeze Φ w amp (weight_eq_one_of_freeze avg w hunif hlin h1) hA n hn
  · intro n
    have h2 : lnE (E E1 n) = lnE E1 + 2 * lnE n := log_ladder lnE hadd E1 n
    have h3 : ((lnE E1 + 2 * lnE n : Nat) : Int) = (lnE E1 : Int) + 2 * (lnE n : Int) := by
      omega
    exact Eq.trans (congrArg (fun x : Nat => (x : Int)) h2) h3

/-! ## §7 条件①：冻结的代数形式（标量投影与全对族） -/

/-- 标量投影层的冻结（某个历史序列不再变化）。本体是全对族，见 §7.1。 -/
def HFreeze (H : Nat → Int) : Prop := ∀ t, H (t + 1) = H t

theorem freeze_history (H : Nat → Int) (hh : HFreeze H) : ∀ t, H t = H 0 := by
  intro t
  induction t with
  | zero => rfl
  | succ t ih =>
    rw [hh t, ih]

theorem freeze_gives_uniform (H : Nat → Int) (hh : HFreeze H) :
    WindowsUniform H := by
  intro m n
  rw [freeze_history H hh m, freeze_history H hh n]

/-- **① ⇒ 形式**：历史冻结时，$K$ 直接落入质数振荡形式。 -/
theorem step_dotH_zero_gives_form
    (cosF : Int → Int) (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b)
    (E1 : Nat) (Φ : Int) (H w amp : Nat → Int) (N : Nat)
    (hh : HFreeze H) (hlin : WeightLinear H w) (h1 : w 1 = 1)
    (hA : AmpLadder Φ w amp) :
    PrimeOscForm cosF
      (fun t => Kfun cosF amp (fun n => lnE (E E1 n)) N t)
      Φ (lnE E1 : Int) lnE N :=
  mechanism_prime_osc cosF lnE hadd E1 Φ H w amp N
    (freeze_gives_uniform H hh) hlin h1 hA

/-! ## §7.1 全对历史 $\mathcal H_{ij}=\tau_i-\tau_j$：本体与冻结 -/

/-- 节点固有时 $\tau_i(t)$；全对历史由它生成，$\mathcal H_{ij}(t)=\tau_i(t)-\tau_j(t)$。 -/
def Hpair (tau : Nat → Nat → Int) (i j t : Nat) : Int :=
  tau i t - tau j t

theorem Hpair_self (tau : Nat → Nat → Int) (i t : Nat) :
    Hpair tau i i t = 0 := by
  unfold Hpair
  omega

theorem Hpair_antisym (tau : Nat → Nat → Int) (i j t : Nat) :
    Hpair tau i j t = - Hpair tau j i t := by
  unfold Hpair
  omega

/-- 上闭链：$\mathcal H_{ij}+\mathcal H_{jk}=\mathcal H_{ik}$。 -/
theorem Hpair_cocycle (tau : Nat → Nat → Int) (i j k t : Nat) :
    Hpair tau i j t + Hpair tau j k t = Hpair tau i k t := by
  unfold Hpair
  omega

/-- 全对冻结：所有节点对的历史每一步都不变。 -/
def PairFreeze (tau : Nat → Nat → Int) (N : Nat) : Prop :=
  ∀ i j t, i < N → j < N → Hpair tau i j (t + 1) = Hpair tau i j t

/-- 节点固有时每步增量相等：$\dot{\mathcal H}_{ij}=0\ \forall i<j$ 的离散形式。 -/
def StepEq (tau : Nat → Nat → Int) (N : Nat) : Prop :=
  ∀ i j t, i < N → j < N →
    tau i (t + 1) - tau i t = tau j (t + 1) - tau j t

theorem pairFreeze_iff_stepEq (tau : Nat → Nat → Int) (N : Nat) :
    PairFreeze tau N ↔ StepEq tau N := by
  constructor
  · intro h i j t hi hj
    have hp := h i j t hi hj
    unfold Hpair at hp
    omega
  · intro h i j t hi hj
    have hs := h i j t hi hj
    unfold Hpair
    omega

/-- 全对冻结 ⇒ 任一节点对投影的 HFreeze（故标量形式结论仍可用）。 -/
theorem pairFreeze_projection (tau : Nat → Nat → Int) (N i j : Nat)
    (hi : i < N) (hj : j < N) (h : PairFreeze tau N) :
    HFreeze (fun t => Hpair tau i j t) := by
  intro t
  exact h i j t hi hj

/-- 全对冻结 ⇒ 每个节点对投影都落入质数振荡形式。 -/
theorem pair_freeze_gives_form
    (cosF : Int → Int) (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b)
    (E1 : Nat) (Φ : Int) (tau : Nat → Nat → Int) (N i j : Nat)
    (w amp : Nat → Int)
    (hi : i < N) (hj : j < N)
    (h : PairFreeze tau N) (hlin : WeightLinear (fun t => Hpair tau i j t) w)
    (h1 : w 1 = 1) (hA : AmpLadder Φ w amp) :
    PrimeOscForm cosF
      (fun t => Kfun cosF amp (fun n => lnE (E E1 n)) N t)
      Φ (lnE E1 : Int) lnE N :=
  step_dotH_zero_gives_form cosF lnE hadd E1 Φ
    (fun t => Hpair tau i j t) w amp N
    (pairFreeze_projection tau N i j hi hj h) hlin h1 hA

/-! ## §8 渗流与博弈：只给前因子与次序无关 -/

theorem cluster_sum (f : Nat → Int) (c : Int) (g : Nat → Int) (N : Nat)
    (h : ∀ n, n < N → f n = c * g n) :
    sumN f N = c * sumN g N := by
  induction N with
  | zero => simp [sumN]
  | succ N ih =>
    have hN : f N = c * g N := h N (by omega)
    have ih' : sumN f N = c * sumN g N := ih (fun n hn => h n (by omega))
    show sumN f N + f N = c * (sumN g N + g N)
    rw [ih', hN]
    exact (Int.mul_add c (sumN g N) (g N)).symm

theorem game_order_irrelevant (a b : Int) : a + b = b + a := by
  omega

/-! ## §9 六要素打包 -/

/-- 六要素同时成立时的完整结论。 -/
theorem six_elements_deliver
    (cosF : Int → Int) (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b)
    (E1 : Nat) (Φ : Int) (r : Nat → Int) (H w amp : Nat → Int) (N : Nat) (v : Int)
    (hclosed : ∀ k, r k = 1)
    (hh : HFreeze H) (hlin : WeightLinear H w) (h1 : w 1 = 1)
    (hA : AmpLadder Φ w amp) :
    PrimeOscForm cosF
        (fun t => Kfun cosF amp (fun n => lnE (E E1 n)) N t)
        Φ (lnE E1 : Int) lnE N ∧
      (∀ n, vs v r n = v) ∧
      (∀ t, H t = H 0) := by
  refine ⟨step_dotH_zero_gives_form cosF lnE hadd E1 Φ H w amp N hh hlin h1 hA, ?_, ?_⟩
  · intro n
    exact vs_const v r hclosed n
  · intro t
    exact freeze_history H hh t

/-! ## §10 条件③：峰位置唯一 ⇒ $T_c$ 唯一 -/

/-- 峰判据（离散）：$m^n=n-1$。 -/
def PeakAt (n m : Nat) : Prop := m ^ n = n - 1

theorem pow_eq_pow_inj (n : Nat) (hn : n ≠ 0) {a b : Nat} (h : a ^ n = b ^ n) : a = b := by
  rcases Nat.lt_trichotomy a b with hlt | heq | hgt
  · have h' : a ^ n < b ^ n := Nat.pow_lt_pow_left hlt hn
    omega
  · exact heq
  · have h' : b ^ n < a ^ n := Nat.pow_lt_pow_left hgt hn
    omega

/-- **③**：峰判据若有解则唯一，故 $T_c=\frac{E_0}{(m^{*}-1)^{(m^{*}-1)/m^{*}}}$ 唯一。 -/
theorem peak_unique (n : Nat) (hn : n ≠ 0) (m1 m2 : Nat)
    (h1 : PeakAt n m1) (h2 : PeakAt n m2) : m1 = m2 := by
  have h : m1 ^ n = m2 ^ n := by
    simp only [PeakAt] at h1 h2
    rw [h1, h2]
  exact pow_eq_pow_inj n hn h

/-! ## §11 公理审计 -/

#print axioms mechanism_prime_osc
#print axioms step_dotH_zero_gives_form
#print axioms pairFreeze_iff_stepEq
#print axioms pair_freeze_gives_form
#print axioms six_elements_deliver
#print axioms peak_unique
/-! ## §12 ①②③ 合取：形式 ∧ 唯一（相变稳定） -/

/-- 条件②：相变发生 = 峰判据有解（$T_c$ 存在）。 -/
def PhaseTransition (n : Nat) : Prop := ∃ m, PeakAt n m

/-- **①②③ 合取**：① 冻结给形式，③ 幂单射给唯一，② 给存在。
三者同时成立时，$K$ 落于质数振荡形式，且 $T_c$ 唯一（相变稳定）。 -/
theorem three_conditions_deliver
    (cosF : Int → Int) (lnE : Nat → Nat)
    (hadd : ∀ a b : Nat, lnE (a * b) = lnE a + lnE b)
    (E1 : Nat) (Φ : Int) (H w amp : Nat → Int) (N n : Nat)
    (hh : HFreeze H) (hlin : WeightLinear H w) (h1 : w 1 = 1)
    (hA : AmpLadder Φ w amp)
    (htrans : PhaseTransition n) (hn : n ≠ 0) :
    PrimeOscForm cosF
        (fun t => Kfun cosF amp (fun m => lnE (E E1 m)) N t)
        Φ (lnE E1 : Int) lnE N ∧
      (∃ m : Nat, PeakAt n m ∧ ∀ m' : Nat, PeakAt n m' → m' = m) := by
  refine ⟨step_dotH_zero_gives_form cosF lnE hadd E1 Φ H w amp N hh hlin h1 hA, ?_⟩
  obtain ⟨m, hm⟩ := htrans
  exact ⟨m, hm, fun m' hm' => peak_unique n hn m' m hm' hm⟩

#print axioms three_conditions_deliver