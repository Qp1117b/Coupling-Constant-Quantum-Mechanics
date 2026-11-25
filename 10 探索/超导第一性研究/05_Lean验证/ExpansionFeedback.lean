/-
ExpansionFeedback.lean —— 第 142 轮：环 17 扩大动力学的三重链式漏项

承载以下严格结果（外部统计工具只作为前提输入，不声称 CQM 推出它们）：
  1. M(N)=C(N,2) 的精确中心导数是 N-1/2；(17.1) 用 N-1，相对误差 1/(2N-1)。
  2. 合并两组样本时方差增量的精确分解（Welford 型）：
     s^2-s0^2 = (m1/m)(s1^2-s0^2) + (m0*m1/m^2)(mu1-mu0)^2。
     故变化域上的矩导数含边界通量 K = s_new^2-s^2+(mu_new-mu)^2，
     零均值对差 (6.6) 的 D_new-D 缺均值漂移平方，不能照搬到非零均值的 ell。
  3. 截断正态前提（B 类）给 K/s^2 = a*lambda(a)，a 为门槛标准化位置。
  4. 自洽方程 g*(2s-C*K)=C*A，A>0、C>0、0<eta<1 时
     g = C*A/(2s-C*K) 且严格解大于偏读解；eta=1 时无解（隐函数失效面）。

无 axiom / sorry / admit / native_decide / unsafe。
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Order.Basic

namespace CQM.ExpansionFeedback

/-! ### 一、组合数离散—连续混用 -/

/-- 对二次函数取任意步长的中心差分，精确等于 N-1/2（h≠0）。 -/
theorem choose2_central_diff (N h : ℝ) (hh : h ≠ 0) :
    ((N + h) * (N + h - 1) - (N - h) * (N - h - 1)) / (4 * h) = N - 1 / 2 := by
  field_simp [hh]
  ring

/-- (17.1) 用 N-1 替代 N-1/2，相对误差恒为 1/(2N-1)。 -/
theorem choose2_old_error (N : ℝ) (hN : 2 * N - 1 ≠ 0) :
    ((N - 1 / 2) - (N - 1)) / (N - 1 / 2) = 1 / (2 * N - 1) := by
  have hN2 : N - 1 / 2 ≠ 0 := by
    intro h
    apply hN
    linarith
  field_simp [hN, hN2]
  ring

/-- N_t = p*N_eff 的链式法则：dM/dt = (N-1/2)*N_eff*p_dot。 -/
theorem mdot_chain (p Neff pdot : ℝ) :
    (p * Neff - 1 / 2) * Neff * pdot
      = ((2 * (p * Neff) - 1) / 2) * Neff * pdot := by
  ring

/-! ### 二、变化样本集上的方差通量 -/

/-- 二阶原始矩 m*(s^2+mu^2)。 -/
noncomputable def rawSecond (m mu s2 : ℝ) : ℝ := m * (s2 + mu ^ 2)

/-- 合并两批样本的方差精确分解：不存在"矩只随内部演化"的写法。 -/
theorem merge_variance (m0 m1 mu0 mu1 s0 s1 : ℝ) (hm : m0 + m1 ≠ 0) :
    (rawSecond m0 mu0 s0 + rawSecond m1 mu1 s1) / (m0 + m1)
        - ((m0 * mu0 + m1 * mu1) / (m0 + m1)) ^ 2
      = (m0 * s0 + m1 * s1) / (m0 + m1)
        + (m0 * m1 / (m0 + m1) ^ 2) * (mu1 - mu0) ^ 2 := by
  unfold rawSecond
  field_simp [hm]
  ring

/-- 通量括号的恒等变形：m2_new-mu^2-s^2-2mu*(mu_new-mu)
    = (s_new^2-s^2)+(mu_new-mu)^2。零均值对差时第二项消失，ell 不然。 -/
theorem flux_identity (mu muN s2 s2N : ℝ) :
    (s2N + muN ^ 2) - mu ^ 2 - s2 - 2 * mu * (muN - mu)
      = (s2N - s2) + (muN - mu) ^ 2 := by
  ring

/-- 新增单元来自右侧截断正态时，条件矩前提（B 类外部工具）给 K = s^2*a*lambda。 -/
theorem trunc_flux (s a lam : ℝ) :
    (s ^ 2 * (1 + a * lam - lam ^ 2) - s ^ 2) + (s * lam) ^ 2
      = s ^ 2 * a * lam := by
  ring

/-! ### 三、自洽反馈：扩大速度不能当成外生读数 -/

/-- 反馈参数 eta = C*K/(2s)。 -/
noncomputable def eta (C K s : ℝ) : ℝ := C * K / (2 * s)

/-- 隐函数方程 g*(2s-CK)=C*A 的唯一解。 -/
theorem solve_self_consistent (A C K s g : ℝ) (hden : 2 * s - C * K ≠ 0)
    (h : g * (2 * s - C * K) = C * A) :
    g = C * A / (2 * s - C * K) := by
  exact (eq_div_iff hden).2 h

/-- 偏读解 g0=C*A/(2s) 与严格解的比值 = 1-eta。 -/
theorem amplification (A C K s : ℝ) (hs : s ≠ 0) (hA : A ≠ 0) (hC : C ≠ 0)
    (hden : 2 * s - C * K ≠ 0) :
    (C * A / (2 * s)) / (C * A / (2 * s - C * K)) = 1 - eta C K s := by
  unfold eta
  field_simp [hs, hA, hC, hden]

/-- eta>0 等价于 C*K>0（s>0）。 -/
theorem eta_pos_iff (C K s : ℝ) (hs : 0 < s) :
    0 < eta C K s ↔ 0 < C * K := by
  unfold eta
  have h2s : 0 < 2 * s := by positivity
  constructor
  · intro h
    rcases (div_pos_iff.mp h) with hpos | hneg
    · exact hpos.1
    · exfalso
      exact (not_lt_of_ge (le_of_lt h2s)) hneg.2
  · intro h
    exact div_pos h h2s

/-- eta<1 等价于 C*K<2s（s>0）。 -/
theorem eta_lt_one_iff (C K s : ℝ) (hs : 0 < s) :
    eta C K s < 1 ↔ C * K < 2 * s := by
  unfold eta
  have h2s : 0 < 2 * s := by positivity
  exact (div_lt_one h2s)

/-- 正反馈且未越界时，严格解严格大于偏读解（偏读低估扩大）。 -/
theorem strict_grows (A C K s : ℝ) (hA : 0 < A) (hC : 0 < C) (hs : 0 < s)
    (he0 : 0 < eta C K s) (he1 : eta C K s < 1) :
    C * A / (2 * s) < C * A / (2 * s - C * K) := by
  have h2s : 0 < 2 * s := by positivity
  have hCK : 0 < C * K := (eta_pos_iff C K s hs).1 he0
  have hCKlt : C * K < 2 * s := (eta_lt_one_iff C K s hs).1 he1
  have hden : 0 < 2 * s - C * K := by linarith
  have hnum : 0 < C * A := by positivity
  rw [div_lt_div_iff₀ h2s hden]
  nlinarith

/-- eta=1 是隐函数失效面：A≠0、C≠0 时方程无解。 -/
theorem critical_no_solution (A C K s : ℝ) (hcrit : C * K = 2 * s)
    (hA : A ≠ 0) (hC : C ≠ 0) :
    ¬ ∃ g : ℝ, g * (2 * s - C * K) = C * A := by
  rintro ⟨g, hg⟩
  have hz : (0 : ℝ) = C * A := by
    simpa [hcrit] using hg
  exact (mul_ne_zero hC hA) hz.symm

/-! ### 四、温度通道漏项（R141 与 R142 的接口） -/

/-- 同一 p 读数若同时依赖 s 与 T，偏读 dot p 缺 p_T*dot T。 -/
theorem pdot_missing_channel (pS pT sdot Tdot : ℝ) :
    pS * sdot = pS * sdot + pT * Tdot - pT * Tdot := by
  ring

/-- 把缺失通道补回后，dot M 的严格链式式（离散系数已取 N-1/2）。 -/
theorem mdot_full_chain (Neff pS pT sdot Tdot N : ℝ) :
    (N - 1 / 2) * Neff * (pS * sdot + pT * Tdot)
      = (N - 1 / 2) * Neff * (pS * sdot) + (N - 1 / 2) * Neff * (pT * Tdot) := by
  ring

end CQM.ExpansionFeedback
