-- Spec.lean（v26，第 199 轮 2026-11-26）：本环目标陈述（只 import 依赖基线，不 import 任何证明模块）
-- v26 变更（第 199 轮）：增 `wGapDeriv2Alt`（$w''=w'/T+\mathrm{sech}^2\frac1{2T}/T^3$ 端点闭式）与
--   `TargetPropWGapDeriv2Alt`（两式恒等）、`TargetPropWGapDeriv2Pos`（条件式正性）、`TargetPropShapeDerivSign`（$S'$ 符号判据）。
-- v25 变更（第 198 轮）：增 `wGapDeriv2`／`shapeDeriv` 与 `TargetPropWGapDeriv2`（$w$ 的二阶导数表示）、
--   `TargetPropShapeDeriv`（形状项 $w/|w'|$ 的导数闭式），把 G-188b 的第一步落进链内。
-- v24 变更（第 197 轮）：增 `TargetPropWGapIbp`（$w=\tanh\frac1{2T}+\frac T2w'$ 分部积分恒等式）、
--   `TargetPropShapeSplit`（形状项分解）、`TargetPropShapeEnd`（端点亏损恒等式）、`TargetPropShapeEndGt`（端点严格高于平均）。
-- v23 变更（第 196 轮）：增 `sechSq`／`wGapDeriv`（$w$ 的导数表示）与 `TargetPropWGapDeriv`（导数恒等式）、
--   `TargetPropWGapDerivNeg`（导数处处为负 ⇒ $|w'|=-w'$），把 G-190c 落进链内。
-- v22 变更（第 195 轮）：增 `TargetPropTChanDominate`（主导项闸，充分条件式）与 `TargetPropTChanCriterion`
--   （$\Delta t>0\iff$ 两通道之和 $>0$，充要判据），把 G-186c 写成可消费的条件式命题。
-- v21 变更（第 194 轮）：增 `TargetPropTEffMPMono`（t 对 p 严格增）与 `TargetPropTChanSplit`（y／p 两通道反号分解），
--   判 G-186p 的形态：p 通道压低 t、y 通道抬高 t，复合符号须主导项比较（G-186c）。
-- v20 变更（第 193 轮）：增 `yOfT`（y 律 K=Υ₀w(T)/T 的显式定义）与 `TargetPropKStrictAnti`／
--   `TargetPropYStrictMono`／`TargetPropTStrictMono`（w 严格减沿 T→K→y→t 链传出，G-186 通道严格化）。
-- v19 变更（第 192 轮）：增 `TargetPropWGapStrictAnti`（0<T₁<T₂ ⇒ w(T₂)<w(T₁)），即 190 的"不增"升级为"严格减"（G-190b 收口）。
-- v18 变更（第 191 轮）：增 `TargetPropSolSurj`／`TargetPropSolNeg`（$s$ 同名判否：可解性因子值域 (0,∞)、可负，不是半整数格点）。
-- v16 变更（第 189 轮）：增 `phiBkt`／`phiMin`／`TargetPropPhiMono`／`TargetPropPhiBktVal`／
--   `TargetPropPhiMinEq`／`TargetPropPhiConflict`（Φ 不进逸度的判据：Φ_BKT/Φ_min = 2β_KT/π = K_BKT）。
-- v17 变更（第 190 轮）：增 `wGap`（w(T)=2∫₀¹ u tanh(u/(2T)) du）与 `TargetPropWGapPos`／
--   `TargetPropWGapAnti`／`TargetPropWGapLeOne`；新增基线 import（IntervalIntegral.Basic、Complex.Trigonometric）。
--   读法注：`wGap 0 = 0`（Lean 总除法），链内 w(0)=1 只能作 T↓0 的极限（G-190a）。
-- v13 变更（第 186 轮）：增 `TargetPropTEffMMono`／`TargetPropTEffMGeOne`（t 的方向与下界）。
-- v14 变更（第 187 轮）：增 `pPairThr`／`TargetPropThrLog`／`TargetPropThrRpow`（t 到 x_* 的接口）。
-- v15 变更（第 188 轮）：增 `rOfW`（r=2α_V w/(3ε_ν|w'|)）、`sOfLock`（s=2/[C(aλ-r)]）
--   与 `TargetPropROfEps`（ε 通道反比）、`TargetPropSFail`（s>0 ⟺ r<aλ，只要求 C>0）。
--   前件必须带 0<w、w'≠0：R-155 的 2α_V/(3ε_ν|d ln w/dT|) 形与 R-157 的 2α_V w/(3ε_ν|w'|) 形
--   只在 w>0 时同值；缺它两式可差符号。|w'| 取绝对值，故 w' 的符号不进结论。
--   命名注：aλ 不能作标识符（λ 是 lambda 关键字），故用 aLam。
-- Spec.lean（v12，第 185 轮 2026-11-25）：本环目标陈述（只 import 依赖基线，不 import 任何证明模块）
-- v12 变更：v11 的 `epsVarFromTheta`／`TargetPropVarBridge` 整体撤销（旧版进 DISCARD 第 185 轮行）；
--   原由见卡 §十八：该桥把 σ_θ²=k_BT/Υ₀ 当独立来源，而 (161.4) 的第二等号前件 σ²(T)=σ₀²[1+2n_B]
--   对应的 (4.1) 第一项已被第 138 轮（R-147，m_eff=0 于 N_I）撤销，且把 E_c 的 Υ 冻成 Υ₀ 与 (15L.3) 冲突。
-- v12 新增：逸度作为刚度比 K=Υ/T 的函数，及其单调性／(15L.5) 界／Υ₀ 下界。
-- Spec.lean（v11，第 183 轮 2026-11-25）：本环目标陈述（只 import 依赖基线，不 import 任何证明模块）
-- 环 15 / 审-6：锁定重数 m_lock = 1 的定义授权
-- v1 缺陷（已登记 DISCARD.md 第 162 轮行）：lockMult 直接返回 0/1，TargetProp 沦为定义展开。
-- v2 修订：m_lock 改为"连接 a,b 的键的基数"，≤1 由键图编码（简单图 / SB.3）承担，
--          ≥1 由"存在键"假设承担；两半不再写进同一个 0/1 值函数。
import Mathlib.Data.Sym.Sym2
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.SpecialFunctions.Log.Deriv
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Analysis.Complex.Trigonometric

namespace CQM.Ring15.Spec

noncomputable section

open MeasureTheory
open scoped Interval

/-- 键的载体：无序对 `Sym2 ℕ`。 -/
abbrev Edge := Sym2 ℕ

/-- 键图：`Finset` 去重，编码层即"简单图"。
对应 SB.3：每对相邻且两端均占据的节点之间只加一条诱导键。 -/
abbrev BondGraph := Finset Edge

/-- 邻接：`a,b` 在 `edges` 中有键。 -/
def Adj (edges : BondGraph) (a b : ℕ) : Prop := Sym2.mk a b ∈ edges

/-- 诱导键 $B_{ij}=s_is_j$：相邻且两端均占据。 -/
def InducedBond (s : ℕ → Bool) (edges : BondGraph) (a b : ℕ) : Prop :=
  Adj edges a b ∧ s a = true ∧ s b = true

/-- 锁定重数 $m_{\rm lock}$：连接 `a,b` 的键的条数（键级计数，不是节点星级计数）。
`a = b` 不承载键，记 0。 -/
def lockMult (edges : BondGraph) (a b : ℕ) : ℕ :=
  if a = b then 0 else (edges.filter (fun e => e = Sym2.mk a b)).card

/-- 本环意图命题（写死的目标陈述）：
`a ≠ b` 时，锁定重数恰为 1 当且仅当该对之间存在键；且恒有 $m_{\rm lock}\le 1$。
即：`m_lock` 是键的存在性指标，既不是节点度数，也不是涡旋绕数量子数。 -/
def TargetProp : Prop :=
  ∀ (edges : BondGraph) (a b : ℕ), a ≠ b →
    (lockMult edges a b = 1 ↔ Adj edges a b) ∧ lockMult edges a b ≤ 1

/-- 锁定概率的键级复合：$m$ 条键**同时**无涡旋的概率。
键间独立取 SB.3 的独立键系综（与 $p_{\rm pair}$ 同一层），不另立新假设。 -/
def pLock (y : ℝ) (m : ℕ) : ℝ := (1 - y) ^ m

/-- 由 $p^{t}=p_{\rm pair}\,p_{\rm lock}$ 反解出的粗粒化指数；$m$ 即锁定重数 $m_{\rm lock}$。 -/
def tEffM (p y : ℝ) (m : ℕ) : ℝ := 1 + (m : ℝ) * Real.log (1 - y) / Real.log p

/-- 本环第二段意图命题：`m_lock=1` ⇒ 锁定概率 $1-y$；
`m=2`（星级读法）⇒ $(1-y)^2$ 严格更小、且 $t$ 严格更大。 -/
def TargetPropLock : Prop :=
  ∀ (p y : ℝ), 0 < p → p < 1 → 0 < y → y < 1 →
    p ^ tEffM p y 1 = p * (1 - y) ∧
    p ^ tEffM p y 2 = p * (1 - y) ^ 2 ∧
    p * (1 - y) ^ 2 ≤ p * (1 - y) ∧
    tEffM p y 1 ≤ tEffM p y 2

/- ===== v3（第 170／173 轮）：独立键前提的授权层显式化 ===== -/

/-- 条件层：**给定 `m` 条键均已存在**，各条失锁彼此独立 ⇒ `(1-y)^m`。
第 170 轮判定：`pLock` 的乘积形式只能授权在这一层；无条件层（乘存在概率）
与登记值 `p_sync(T_c)=0.8754138` 不相容，故不采用。 -/
def pLockCond (y : ℝ) (m : ℕ) : ℝ := (1 - y) ^ m

/-- 无条件层：再乘"`m` 条键全部存在"的概率 `q^m`。
链内 `q = p_pair^2`（SB.3 座占据独立），见第 156／170 轮。 -/
def pLockUncond (q y : ℝ) (m : ℕ) : ℝ := q ^ m * (1 - y) ^ m

/-- 本环第三段意图命题（授权层的形式侧）：
在 `0 ≤ q ≤ 1`、`0 ≤ y ≤ 1` 下，无条件层**不超过**条件层；且 `q = 1` 时两者相等。
即：把"键独立"从座级外推到键级只会压低锁定概率，不会抬高——
这是第 170 轮"无条件层与登记值冲突"的形式对应物。 -/
def TargetPropLayer : Prop :=
  ∀ (q y : ℝ) (m : ℕ), 0 ≤ q → q ≤ 1 → 0 ≤ y → y ≤ 1 →
    pLockUncond q y m ≤ pLockCond y m ∧ (q = 1 → pLockUncond q y m = pLockCond y m)

/- ===== v4（第 175 轮）：锁定概率对刚度／逸度的单调方向 ===== -/

/-- 同步概率（键级）：$p_{\rm sync}=p_{\rm pair}(1-y)^{m}$。 -/
def pSync (ppair y : ℝ) (m : ℕ) : ℝ := ppair * (1 - y) ^ m

/-- 逸度 $y=2\pi e^{-E_c/T}$（前因子 $2\pi$ 为外部边界，见 DISCARD 第 161 轮）。 -/
def yFug (Ec T : ℝ) : ℝ := 2 * Real.pi * Real.exp (-Ec / T)

/-- 方向性命题（一）：刚度升高 ⇒ 核心能升高 ⇒ 逸度**下降**。 -/
def TargetPropFugMono : Prop :=
  ∀ (Ec1 Ec2 T : ℝ), 0 < T → Ec1 ≤ Ec2 → yFug Ec2 T ≤ yFug Ec1 T

/-- 方向性命题（二）：逸度**越低**，同步概率**越高**（$m$ 条键同时锁定；
`pSync = p_pair (1-y)^m` 关于 $y$ 单调不增）。
即"刚度越大 ⇒ 逸度越小 ⇒ 越易同步"——这是 $\Upsilon\to T_{\rm sync}$ 单调性的概率层。 -/
def TargetPropSyncMono : Prop :=
  ∀ (ppair y1 y2 : ℝ) (m : ℕ), 0 ≤ ppair → 0 ≤ y1 → y1 ≤ y2 → y2 ≤ 1 →
    pSync ppair y2 m ≤ pSync ppair y1 m

/- ===== v5（第 176 轮）：共点两键的相位差相关系数 ===== -/

/-- 共点两键相位差的相关系数（顶点相位独立、等方差 $v$）：
$\mathrm{Cov}(\theta_i-\theta_j,\theta_j-\theta_k)=-v$、各自方差 $2v$，故 $\rho=-v/\sqrt{2v\cdot 2v}=-1/2$。
本命题只写算术核（概率语义在卡内），不冒充统计定理。 -/
def TargetPropAdjCorr : Prop :=
  ∀ (v : ℝ), 0 < v → (-v) / Real.sqrt (2 * v * (2 * v)) = -(1 / 2 : ℝ)

/- ===== v6（第 177 轮）：带顶点相关 ρ_v 的一般式（v5 为其 ρ_v=0 特例） ===== -/

/-- 共点相位差相关系数的一般式。顶点相位方差 $v$、共点相关 $\rho_v<1$ 时
$X=\theta_i-\theta_j$、$Y=\theta_j-\theta_k$ 有 $\mathrm{Cov}(X,Y)=v(2\rho_v-1)$、
$\mathrm{Var}X=\mathrm{Var}Y=2v(1-\rho_v)$，故 $\rho_{XY}=(2\rho_v-1)/[2(1-\rho_v)]$。
仍是算术核：$\rho_v$ 的链内取值（第 84 轮 Bessel 核）不写进陈述。 -/
def adjCorrGen (rv v : ℝ) : ℝ :=
  (v * (2 * rv - 1)) / Real.sqrt ((2 * v * (1 - rv)) * (2 * v * (1 - rv)))

def TargetPropAdjCorrGen : Prop :=
  ∀ (rv v : ℝ), 0 < v → rv < 1 → adjCorrGen rv v = (2 * rv - 1) / (2 * (1 - rv))

/- ===== v7（第 177 轮）：补入距离 2 相关 ρ₂（v6 隐含 ρ₂=0，被 B 闸抓到） ===== -/

/-- 共点相位差相关的**完整**算术核：$\rho_1$ 为相邻（距离 1）顶点相关、$\rho_2$ 为
距离 2 顶点相关（$\theta_i$ 与 $\theta_k$），则
$\mathrm{Cov}(X,Y)=v(2\rho_1-1-\rho_2)$、$\mathrm{Var}X=2v(1-\rho_1)$，故
$\rho_{XY}=(2\rho_1-1-\rho_2)/[2(1-\rho_1)]$。$\rho_1=\rho_2=0$ 退化为 $-1/2$（v5），
$\rho_2=0$ 退化为 v6。 -/
def adjCorrNear (r1 r2 v : ℝ) : ℝ :=
  (v * (2 * r1 - 1 - r2)) / Real.sqrt ((2 * v * (1 - r1)) * (2 * v * (1 - r1)))

def TargetPropAdjCorrNear : Prop :=
  ∀ (r1 r2 v : ℝ), 0 < v → r1 < 1 →
    adjCorrNear r1 r2 v = (2 * r1 - 1 - r2) / (2 * (1 - r1))

/- ===== v8（第 178 轮）：ρ_XY 与共同相位振幅无关（尺度不变） ===== -/

/-- 尺度不变：$\rho_{XY}$ 不依赖共同振幅 $v$。含义是——$\varepsilon$ 层与 $\lambda$ 层
若只差一个公共线性因子 $\kappa_f$（第 139 轮 $\delta\lambda=\kappa_f\delta\varepsilon$
在 $\sigma\to0$ 的一阶），则两层给出**同一个** $\rho_{XY}$，无需另立参数。 -/
def TargetPropAdjCorrScale : Prop :=
  ∀ (r1 r2 v : ℝ), 0 < v → r1 < 1 → adjCorrNear r1 r2 v = adjCorrNear r1 r2 1


/- ===== v9（第 181 轮）：锁条件的非线性映射 $r=\sqrt{1-\varepsilon/2\pi}$、$\lambda=\ln r$ ===== -/

/-- $\lambda(e)=\tfrac12\ln(1-e/2\pi)$：即 $\lambda=\ln\sqrt{1-\varepsilon/2\pi}$。含义是——
链路 (9.x) 的 $r=\sqrt{1-\varepsilon/2\pi}$ 是**有界**函数（$\varepsilon\to2\pi$ 处奇点），
所以"锁 ⇔ $|\theta|>\pi$"不是 $\varepsilon$ 的线性事件；一阶系数须由导数给出，
二阶修正须由凹凸性给出。 -/
noncomputable def lockLam (e : ℝ) : ℝ := (1 / 2) * Real.log (1 - e / (2 * Real.pi))

/-- 一阶系数：$\lambda'(e)=-\dfrac{1}{2(2\pi-e)}$。$e\to0$ 时 $=-1/(4\pi)$，
与 `审-2` 的 $\kappa_f=-\partial_\varepsilon\ln v_\tau=1/(4\pi)$ 同值——这是链内两个
独立来源（(9.x) 的 $r$ 形式 与 `审-2` 的 $v_\tau$ 形式）在 $\varepsilon\to0$ 处相合的**断言**。 -/
def TargetPropLockLamDeriv : Prop :=
  ∀ e : ℝ, e < 2 * Real.pi → HasDerivAt lockLam (-(1 / (2 * (2 * Real.pi - e)))) e

/-- $\lambda$ 在 $e<2\pi$ 上**严格单调减**：亏角越大，周长比越小、固有时率越低。
单调性是"锁事件可换到 $\varepsilon$ 空间说"的授权（否则 $\theta$ 的越界条件无对应）。 -/
def TargetPropLockLamAnti : Prop :=
  StrictAntiOn lockLam (Set.Iio (2 * Real.pi))

/-- 反解：$\exp(2\lambda)=1-\varepsilon/2\pi$，即 $\varepsilon=2\pi(1-e^{2\lambda})$。
给出 $r$ 与 $\lambda$ 的**双射**，从而非线性不是"近似"，而是可逆的确定映射。 -/
def TargetPropLockLamExp : Prop :=
  ∀ e : ℝ, e < 2 * Real.pi → Real.exp (2 * lockLam e) = 1 - e / (2 * Real.pi)


/- ===== v10（第 182 轮）：锁条件的 ε 空间判据（由 v9 的单调性 + v9 的映射闭式） ===== -/

/-- 锁定判据换到 $\varepsilon$ 空间：$|\Delta\lambda|>1/(4|s|)$ 等价于两顶点"周长比"之比
超过 $e^{1/(2|s|)}$。它不是线性阈值，而是**比值判据**——因为 $\lambda=\ln r$ 把差变成商。
含义：$|s|=1/2$ 时门槛为 $e\approx2.718$，只有一端逼近奇点 $\varepsilon\to2\pi$（$r\to0$）才够。 -/
def TargetPropLockRatio : Prop :=
  ∀ (s e1 e2 : ℝ), s ≠ 0 → e1 < 2 * Real.pi → e2 < 2 * Real.pi → e1 < e2 →
    ((lockLam e1 - lockLam e2 > 1 / (4 * |s|)) ↔
      ((1 - e1 / (2 * Real.pi)) / (1 - e2 / (2 * Real.pi)) > Real.exp (1 / (2 * |s|))))


/- ===== v12（第 185 轮）：逸度归刚度——(15L.3) 的 Υ 是有效刚度，不是 Υ₀ ===== -/

/-- 逸度作为刚度比 $K=\Upsilon/(k_BT)$ 的函数：$y=2\pi e^{-\pi^2K/2}$。
(15L.3) 的原文即 $E_c=\tfrac{\pi^2}{2}\Upsilon$，故 $y$ 只依赖 $K$；$T$ 的依赖**全部**
经由 $\Upsilon(T)$（环 19 (19W.3)：$\Upsilon_{\rm bare}=\Upsilon_0w(T)$）。
$2\pi$ 前因子是外部边界，不在本环推导内。 -/
noncomputable def fugOfK (K : ℝ) : ℝ := 2 * Real.pi * Real.exp (-(Real.pi ^ 2 * K / 2))

/-- 意图命题（一）：$K$ 严格增大 ⇒ $y$ 严格减小；
等价说法：$\Upsilon/T$ 严格减 $\iff$ $y$ 严格增。$w$ 的形状（$w'<0$）在此不进陈述，
只进前提 $K_1<K_2$——形状留给数值层，陈述只承担"$y$ 是 $K$ 的严格减函数"。
这是把 $T$ 依赖从 $\sigma_\theta$ 归还刚度的形式侧。 -/
def TargetPropFugStiff : Prop :=
  ∀ (ups ups' T T' : ℝ), 0 < ups → 0 < T → 0 < ups' → 0 < T' →
    ups / T < ups' / T' → fugOfK (ups' / T') < fugOfK (ups / T)

/-- 意图命题（二）：(15L.5) 的界是**充要**的——$y(K)\le y(1/\beta)$ $\iff$ $K\ge1/\beta$。
界值 $y(1/\beta)=2\pi e^{-\pi^2/(2\beta)}$ 与 $\Upsilon$ 无关，故这是普适数，
不是某材料的估计。 -/
def TargetPropFugBound : Prop :=
  ∀ (beta K : ℝ), 0 < beta → 0 < K → (fugOfK K ≤ fugOfK (1 / beta) ↔ 1 / beta ≤ K)

/-- 意图命题（三）：把 (15L.5) 反解到 $\Upsilon_0$——$1/\beta\le \Upsilon_0 w/T$ ⇒
$\Upsilon_0\ge T/(\beta w)$。含义：普适界给出 $\Upsilon_0$ 的**下界**；
$w$ 与 $T_c$ 是登记值，故这是链内可判的不等式，不是新参数。 -/
def TargetPropUpsLower : Prop :=
  ∀ (ups w T beta : ℝ), 0 < ups → 0 < w → 0 < T → 0 < beta →
    1 / beta ≤ ups * w / T → T / (beta * w) ≤ ups

/- ===== v13（第 186 轮）：粗粒化指数 $t$ 对逸度的单调与下界（下游 $\epsilon_\nu$ 的口径链首环） ===== -/

/-- $y$ 增大 ⇒ $t$ 增大（锁损失越多，配对阈值越要抬高才到 $p_c$）。
这是 R-158 ④ 定义式的方向侧，接 R-157 的 $y\to t\to x_\ast\to\epsilon_\nu\to r$ 口径链。 -/
def TargetPropTEffMMono : Prop :=
  ∀ (p y1 y2 : ℝ) (m : ℕ), 0 < p → p < 1 → 0 ≤ y1 → y1 < y2 → y2 < 1 → 1 ≤ m →
    tEffM p y1 m < tEffM p y2 m

/-- $t\ge1$：$y\in[0,1)$ 时 $1-y\le1$ ⇒ $\ln(1-y)\le0$，与 $\ln p<0$ 相除为正，
故 $t=1+m\cdot(\cdot)\ge1$；等号只在 $y=0$（零温全锁）取到。 -/
def TargetPropTEffMGeOne : Prop :=
  ∀ (p y : ℝ) (m : ℕ), 0 < p → p < 1 → 0 ≤ y → y < 1 → 1 ≤ m →
    1 ≤ tEffM p y m

/- ===== v14（第 187 轮）：配对阈值与粗粒化指数的两条写法等价（$t\to x_\ast$ 的接口） ===== -/

/-- 配对阈值的定义（(15L.7)）：$p_{\rm pair}^{\rm thr}=p_c/(1-y)^m$。 -/
def pPairThr (p y : ℝ) (m : ℕ) : ℝ := p / (1 - y) ^ m

/-- 两条写法等价（一）：(15L.4) 的 $t=1+m\ln(1-y)/\ln p_{\rm pair}^{\rm thr}$ 恰等于 (15L.7) 的
$\ln p_c/\ln p_{\rm pair}^{\rm thr}$。退化点 $p_{\rm pair}^{\rm thr}=1$（即 $p_c=(1-y)^m$）须排除，
该处 $t=\infty$，见 `pPairThr` 值域注记。 -/
def TargetPropThrLog : Prop :=
  ∀ (p y : ℝ) (m : ℕ), 0 < p → p < 1 → 0 ≤ y → y < 1 → 1 ≤ m → p < (1 - y) ^ m →
    tEffM (pPairThr p y m) y m = Real.log p / Real.log (pPairThr p y m)

/-- 两条写法等价（二）：$p_c^{1/t}=p_{\rm pair}^{\rm thr}$，故 $x_\ast=\bar F^{-1}(p_c^{1/t})$
与 $\bar F^{-1}(p_{\rm pair}^{\rm thr})$ 是同一个数（下游 $x_\ast$ 不会两值）。 -/
def TargetPropThrRpow : Prop :=
  ∀ (p y : ℝ) (m : ℕ), 0 < p → p < 1 → 0 ≤ y → y < 1 → 1 ≤ m → p < (1 - y) ^ m →
    p ^ (1 / tEffM (pPairThr p y m) y m) = pPairThr p y m

/- ===== v15（第 188 轮）：$\epsilon_\nu\to r$ 的反比结构与失效面判据（口径链第三环） ===== -/

/-- 环 17 登记的 $r$（扩大动力学的失效面半径）：$r=\dfrac{2\alpha_Vw}{3\epsilon_\nu|w'|}$。 -/
def rOfW (alphaV w w' eps : ℝ) : ℝ := 2 * alphaV * w / (3 * eps * |w'|)

/-- 环 17 登记的 $s$：$s=\dfrac{2}{C(a\lambda-r)}$（$C$ 为已登记的正常数）。 -/
def sOfLock (C1 aLam r : ℝ) : ℝ := 2 / (C1 * (aLam - r))

/-- $\epsilon_\nu$ 越小 ⇒ $r$ 越大（同一组 $(\alpha_V,w,|w'|)$）：分子固定、分母反比。
这是"$\epsilon_\nu$ 的 T 移动如何搬到失效面"的纯结构侧。 -/
def TargetPropROfEps : Prop :=
  ∀ (aV w w' e1 e2 : ℝ), 0 < aV → 0 < w → w' ≠ 0 → 0 < e1 → e1 < e2 →
    rOfW aV w w' e2 < rOfW aV w w' e1

/-- 失效面判据：$s>0\iff a\lambda>r$（$C>0$ 固定符号即可，不钉数值）。 -/
def TargetPropSFail : Prop :=
  ∀ (C1 aLam r : ℝ), 0 < C1 → (0 < sOfLock C1 aLam r ↔ r < aLam)

/- ===== v16（第 189 轮）：$\Phi$ 是否进入 (15L.3) 的授权域 ===== -/

/-- BKT 钉住的渗流因子（(154.2)/(19P.24)：$\Phi_c=\kappa=2T_c/(\pi\Upsilon_0w_c)$）。 -/
def phiBkt (T U0 w : ℝ) : ℝ := 2 * T / (Real.pi * U0 * w)

/-- 由 (15L.5) 反解出的 $\Phi$ 下界：$\Phi\ge\phiMin$ 才使 $y\le y_{\rm crit}$。 -/
def phiMin (T U0 w yc : ℝ) : ℝ := (2 * T / (Real.pi ^ 2 * U0 * w)) * Real.log (2 * Real.pi / yc)

/-- $\Phi$ 只能抬高逸度：$0<\Phi_1\le\Phi_2$ $\Rightarrow$ $y(k\Phi_2)\le y(k\Phi_1)$。 -/
def TargetPropPhiMono : Prop :=
  ∀ (k Φ1 Φ2 : ℝ), 0 < k → 0 < Φ1 → Φ1 ≤ Φ2 → fugOfK (k * Φ2) ≤ fugOfK (k * Φ1)

/-- (15L.3) 在 BKT 钉住处取到普适临界值 $y=2\pi e^{-\pi}$（与 $T,\Upsilon_0,w$ 全无关）。 -/
def TargetPropPhiBktVal : Prop :=
  ∀ (T U0 w : ℝ), 0 < T → 0 < U0 → 0 < w →
    fugOfK (U0 * w * phiBkt T U0 w / T) = 2 * Real.pi * Real.exp (-Real.pi)

/-- $\Phi=\phiMin$ 恰好顶到 $y=y_{\rm crit}$（闭式代入，不是数值反解）。 -/
def TargetPropPhiMinEq : Prop :=
  ∀ (T U0 w yc : ℝ), 0 < T → 0 < U0 → 0 < w → 0 < yc → yc ≤ 2 * Real.pi →
    fugOfK (U0 * w * phiMin T U0 w yc / T) = yc

/-- 普适 no-go：$\beta_{\rm KT}<\pi/2$ $\Rightarrow$ $y(1/\beta)<y(2/\pi)$，即 (15L.5) 的上界恒**严于** BKT 值。 -/
def TargetPropPhiConflict : Prop :=
  ∀ (b : ℝ), 0 < b → b < Real.pi / 2 → fugOfK (1 / b) < fugOfK (2 / Real.pi)

/- ===== v17（第 190 轮）：$w(T)$ 的积分定义授权、正性、单调与上界 ===== -/

/-- 环 19 的归一化权重：$w(T)=2\int_0^1 u\tanh\frac{u}{2T}\,du$。
温度只经 $\tanh$ 的辐角 $u/(2T)$ 进入（occupation 差的 Fermi 窗平均），不进任何可调前因子。 -/
noncomputable def wGap (T : ℝ) : ℝ := ∫ u in (0 : ℝ)..1, 2 * u * Real.tanh (u / (2 * T))

/-- $T>0$ 时 $w>0$（integrand 在 $(0,1]$ 上逐点为正）。 -/
def TargetPropWGapPos : Prop := ∀ (T : ℝ), 0 < T → 0 < wGap T

/-- $w$ 随 $T$ 单调不增：$0<T_1\le T_2$ $\Rightarrow$ $w(T_2)\le w(T_1)$（逐点 $\tanh$ 单调＋积分保序）。 -/
def TargetPropWGapAnti : Prop := ∀ (T1 T2 : ℝ), 0 < T1 → T1 ≤ T2 → wGap T2 ≤ wGap T1

/-- $w\le 1$（$\tanh<1$ 与 $u\le 1$ 一起给；$T\to0$ 的归一值 $1$ 是上确界）。 -/
def TargetPropWGapLeOne : Prop := ∀ (T : ℝ), 0 < T → wGap T ≤ 1

/- ===== v18（第 191 轮）：$s$ 的同名判否——可解性因子 $s_{\rm sol}$ 不是半整数格点 ===== -/

/-- 可解性因子 $s_{\rm sol}=2/[C(a\lambda-r)]$（R155.1）正向**取遍** $(0,\infty)$：无格点结构。
代入 $C=1,r=0,a\lambda=2/y$ 即得任给的 $y>0$。 -/
def TargetPropSolSurj : Prop :=
  ∀ (y : ℝ), 0 < y → ∃ C1 aLam r : ℝ,
    0 < C1 ∧ 0 < aLam ∧ r < aLam ∧ sOfLock C1 aLam r = y

/-- 同一因子在 $a\lambda<r$ 分支上取负值，故它是**实值响应量**，与 $\frac12\mathbb Z$ 的表示权不是同一对象。 -/
def TargetPropSolNeg : Prop :=
  ∃ C1 aLam r : ℝ, 0 < C1 ∧ aLam < r ∧ sOfLock C1 aLam r < 0

/- ===== v19（第 192 轮）：$w$ 的严格单调（不增升级为严格减） ===== -/

/-- $0<T_1<T_2$ $\Rightarrow$ $w(T_2)<w(T_1)$：辐角严格变小、$\tanh$ 严格增，差值在 $u=1$ 处为正。 -/
def TargetPropWGapStrictAnti : Prop := ∀ (T1 T2 : ℝ), 0 < T1 → T1 < T2 → wGap T2 < wGap T1

/- ===== v20（第 193 轮）：$w$ 的严格减沿 $T\to K\to y\to t$ 链传下去（G-186 的通道严格化） ===== -/

/-- $y$ 作为 $T$ 的函数：$K=\Upsilon_0w(T)/T$、(15L.3) 的 $y=2\pi e^{-\pi^2K/2}$。
这是 185 轮改口径后的 $y$ 律的显式定义（此前只在文字里）。 -/
noncomputable def yOfT (ups0 T : ℝ) : ℝ := fugOfK (ups0 * wGap T / T)

/-- 链的第一环：$w$ 严格减 $\Rightarrow$ $K=\Upsilon_0w/T$ 严格减（分子变小、分母变大，两头同向）。
侧条件 $0<w(T_1)$ 显式写出：它是 $w$ 的正性（v17 已证），不在此重复证明。 -/
def TargetPropKStrictAnti : Prop :=
  ∀ (ups0 T1 T2 : ℝ), 0 < ups0 → 0 < T1 → T1 < T2 → 0 < wGap T1 →
    ups0 * wGap T2 / T2 < ups0 * wGap T1 / T1

/-- 链的第二环：$y$ 作为 $T$ 的函数严格**增**（$K$ 严格减、$e^{-\pi^2K/2}$ 严格增）。
方向上与"$w$ 随 $T$ 减"不冲突：$y$ 随 $T$ 升是 $K$ 掉得比分母涨得快。 -/
def TargetPropYStrictMono : Prop :=
  ∀ (ups0 T1 T2 : ℝ), 0 < ups0 → 0 < T1 → T1 < T2 → 0 < wGap T1 → 0 < wGap T2 →
    yOfT ups0 T1 < yOfT ups0 T2

/-- 链的第三环（复合）：$p$ 固定时 $t$ 在 $T$ 上严格增。
侧条件 $y<1$ 显式：$t$ 的定义域 $1-y>0$；$\Upsilon_0$、$p$ 的数值不入本陈述。 -/
def TargetPropTStrictMono : Prop :=
  ∀ (ups0 T1 T2 p : ℝ) (m : ℕ), 0 < ups0 → 0 < T1 → T1 < T2 → 0 < wGap T1 → 0 < wGap T2 →
    0 < p → p < 1 → 1 ≤ m → yOfT ups0 T1 < 1 → yOfT ups0 T2 < 1 →
    tEffM p (yOfT ups0 T1) m < tEffM p (yOfT ups0 T2) m

/- ===== v21（第 194 轮）：$t$ 的两条通道方向相反（G-186p 的形态判定） ===== -/

/-- $t$ 对 $p_{\rm pair}$ **严格增**：$0<p_2<p_1<1$、$y\in(0,1)$ ⇒ $t(p_2,y,m)<t(p_1,y,m)$。
故 $p_{\rm pair}$ 随 $T$ 减的那一支是**压低** $t$ 的，与 $y$ 通道（抬高 $t$）反号。 -/
def TargetPropTEffMPMono : Prop :=
  ∀ (p1 p2 y : ℝ) (m : ℕ), 0 < p2 → p2 < p1 → p1 < 1 → 0 < y → y < 1 → 1 ≤ m →
    tEffM p2 y m < tEffM p1 y m

/-- 两通道的**反号分解**：$y_1<y_2$（$y$ 通道）、$p_2<p_1$（$p$ 通道）时

$t(p_2,y_2)-t(p_1,y_1)=\dfrac{m\left[\,(\ln(1-y_2)-\ln(1-y_1))\ln p_1+\ln(1-y_1)(\ln p_1-\ln p_2)\,\right]}{\ln p_1\ln p_2}$，

且第一项 $>0$（$y$ 通道抬高 $t$）、第二项 $<0$（$p$ 通道压低 $t$）。故复合后的符号不由任一通道单独决定。 -/
def TargetPropTChanSplit : Prop :=
  ∀ (p1 p2 y1 y2 : ℝ) (m : ℕ), 0 < p2 → p2 < p1 → p1 < 1 → 0 < y1 → y1 < y2 → y2 < 1 → 1 ≤ m →
    tEffM p2 y2 m - tEffM p1 y1 m
        = (m : ℝ) * ((Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
            + Real.log (1 - y1) * (Real.log p1 - Real.log p2)) / (Real.log p1 * Real.log p2)
      ∧ 0 < (Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
      ∧ Real.log (1 - y1) * (Real.log p1 - Real.log p2) < 0

/- ===== v22（第 195 轮）：G-186c 的条件式主导项闸与充要判据 ===== -/

/-- **主导项闸（充分）**：$y_1<y_2$（$y$ 通道）、$p_2<p_1$（$p$ 通道）且
$(\ln(1-y_2)-\ln(1-y_1))\ln p_1+\ln(1-y_1)(\ln p_1-\ln p_2)>0$（$y$ 项压过 $p$ 项）⇒ $t(p_1,y_1,m)<t(p_2,y_2,m)$。
侧条件**显式**给出，不是藏起来的假设：下游 186 消费"$t$ 随 $T$ 严格增"时须逐点核这条不等式。 -/
def TargetPropTChanDominate : Prop :=
  ∀ (p1 p2 y1 y2 : ℝ) (m : ℕ), 0 < p2 → p2 < p1 → p1 < 1 → 0 < y1 → y1 < y2 → y2 < 1 → 1 ≤ m →
    0 < (Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
        + Real.log (1 - y1) * (Real.log p1 - Real.log p2) →
    tEffM p1 y1 m < tEffM p2 y2 m

/-- **充要判据**：$\Delta t>0$ $\iff$ 两通道之和 $>0$。
故复合的符号既不由 $y$ 通道单独决定、也不由 $p$ 通道单独决定，只由这一条标量不等式决定——
这是 G-186c 在链内的可判形态。 -/
def TargetPropTChanCriterion : Prop :=
  ∀ (p1 p2 y1 y2 : ℝ) (m : ℕ), 0 < p2 → p2 < p1 → p1 < 1 → 0 < y1 → y1 < y2 → y2 < 1 → 1 ≤ m →
    (tEffM p1 y1 m < tEffM p2 y2 m ↔
      0 < (Real.log (1 - y2) - Real.log (1 - y1)) * Real.log p1
          + Real.log (1 - y1) * (Real.log p1 - Real.log p2))

/- ===== v23（第 196 轮）：$w$ 的导数表示（G-190c） ===== -/

/-- $\mathrm{sech}^2 x:=1/\cosh^2 x$（与 $\tanh$ 的导数值同形）。 -/
noncomputable def sechSq (x : ℝ) : ℝ := 1 / Real.cosh x ^ 2

/-- $w'(T)=-\dfrac{1}{T^2}\displaystyle\int_0^1u^2\,\mathrm{sech}^2\dfrac{u}{2T}\,du$：
温度只经辐角进入，导数不带任何可调前因子。188 的形状项 $w/|w'|$ 需要这条表示。 -/
noncomputable def wGapDeriv (T : ℝ) : ℝ :=
  -(1 / T ^ 2) * ∫ u in (0 : ℝ)..1, u ^ 2 * sechSq (u / (2 * T))

/-- 导数恒等式（G-190c）：$w$ 在 $T>0$ 处可微，且导数就是 `wGapDeriv`。 -/
def TargetPropWGapDeriv : Prop := ∀ (T : ℝ), 0 < T → HasDerivAt wGap (wGapDeriv T) T

/-- 导数处处为负（被积函数 $u^2\mathrm{sech}^2>0$）⇒ $|w'|=-w'$ 可直接取用。 -/
def TargetPropWGapDerivNeg : Prop := ∀ (T : ℝ), 0 < T → wGapDeriv T < 0

/- ===== v24（第 197 轮）：$w$ 的分部积分恒等式与形状项分解（G-188a） ===== -/

/-- 分部积分恒等式：$w(T)=\tanh\dfrac{1}{2T}+\dfrac{T}{2}w'(T)$
——窗口平均＝端点上界＋半温差商，右侧两项均由链内量给出。 -/
def TargetPropWGapIbp : Prop :=
  ∀ (T : ℝ), 0 < T → wGap T = Real.tanh (1 / (2 * T)) + (T / 2) * wGapDeriv T

/-- 形状项分解：$\dfrac{w}{|w'|}=\dfrac{\tanh\frac{1}{2T}}{|w'|}-\dfrac{T}{2}$
——形状项不是独立对象，而是端点核值与导数模的商再减一个纯温度的 $\frac T2$。 -/
def TargetPropShapeSplit : Prop :=
  ∀ (T : ℝ), 0 < T →
    wGap T / |wGapDeriv T| = Real.tanh (1 / (2 * T)) / |wGapDeriv T| - T / 2

/-- 端点亏损恒等式：$\dfrac{T}{2}\,|w'|=\tanh\dfrac{1}{2T}-w$
——导数模恰是"端点上界减去窗口平均"的亏损，正比于半温。 -/
def TargetPropShapeEnd : Prop :=
  ∀ (T : ℝ), 0 < T → (T / 2) * |wGapDeriv T| = Real.tanh (1 / (2 * T)) - wGap T

/-- 端点严格高于窗口平均（$\tanh\dfrac{1}{2T}>w(T)$）：亏损为正，$|w'|>0$ 的直接推论。 -/
def TargetPropShapeEndGt : Prop :=
  ∀ (T : ℝ), 0 < T → wGap T < Real.tanh (1 / (2 * T))

/- ===== v25（第 198 轮）：$w$ 的二阶导数与形状项导数（G-188b 第一步） ===== -/

/-- $w''(T)=-\dfrac{2}{T}w'(T)-\dfrac{1}{T^4}\displaystyle\int_0^1u^3\,\mathrm{sech}^2\dfrac{u}{2T}\tanh\dfrac{u}{2T}\,du$
——$w'=-T^{-2}B$、$B=\int u^2\mathrm{sech}^2$、$B'=T^{-2}\int u^3\mathrm{sech}^2\tanh$，商法则合并。 -/
noncomputable def wGapDeriv2 (T : ℝ) : ℝ :=
  -(2 / T) * wGapDeriv T
    - (1 / T ^ 4) * ∫ u in (0 : ℝ)..1,
        u ^ 3 * sechSq (u / (2 * T)) * Real.tanh (u / (2 * T))

/-- 形状项导数 $S'(T)=\dfrac{w\,w''-(w')^2}{(w')^2}$，$S:=w/|w'|$（$w'<0$ 时 $|w'|=-w'$）。 -/
noncomputable def shapeDeriv (T : ℝ) : ℝ :=
  (wGap T * wGapDeriv2 T - wGapDeriv T ^ 2) / wGapDeriv T ^ 2

/-- 二阶导数表示（G-188b-1）：`wGapDeriv` 在 $T>0$ 处可微，导数即 `wGapDeriv2`。 -/
def TargetPropWGapDeriv2 : Prop := ∀ (T : ℝ), 0 < T → HasDerivAt wGapDeriv (wGapDeriv2 T) T

/-- 形状项导数（G-188b-2）：$S=w/|w'|$ 在 $T>0$ 处可微，导数即 `shapeDeriv`；
其符号将只由 $w\,w''-(w')^2$ 决定（下一步判据的落点）。 -/
def TargetPropShapeDeriv : Prop :=
  ∀ (T : ℝ), 0 < T → HasDerivAt (fun T => wGap T / |wGapDeriv T|) (shapeDeriv T) T

/- ===== v26（第 199 轮）：$w''$ 的端点闭式、条件式正性与形状项符号判据（G-188b-2） ===== -/

/-- $w''$ 的端点闭式：$w''(T)=\dfrac{w'(T)}{T}+\dfrac{1}{T^3}\mathrm{sech}^2\dfrac{1}{2T}$
——由 v24 恒等式 $w=\tanh\frac{1}{2T}+\frac T2w'$ 逐项对 $T$ 求导得到，故与 `wGapDeriv2` 同值。 -/
noncomputable def wGapDeriv2Alt (T : ℝ) : ℝ :=
  wGapDeriv T / T + sechSq (1 / (2 * T)) / T ^ 3

/-- 二阶导两式恒等（G-188b-2a）：`wGapDeriv2 T = wGapDeriv2Alt T`（$T>0$）。 -/
def TargetPropWGapDeriv2Alt : Prop :=
  ∀ (T : ℝ), 0 < T → wGapDeriv2 T = wGapDeriv2Alt T

/-- 条件式正性（G-188b-2b）：$T^2\,|w'(T)|<\mathrm{sech}^2\dfrac{1}{2T}$ ⇒ $w''(T)>0$。 -/
def TargetPropWGapDeriv2Pos : Prop :=
  ∀ (T : ℝ), 0 < T → T ^ 2 * |wGapDeriv T| < sechSq (1 / (2 * T)) → 0 < wGapDeriv2 T

/-- 形状项导数的符号判据（G-188b-2c）：$S'(T)<0\iff w(T)\,w''(T)<(w'(T))^2$（$T>0$）。 -/
def TargetPropShapeDerivSign : Prop :=
  ∀ (T : ℝ), 0 < T → (shapeDeriv T < 0 ↔ wGap T * wGapDeriv2 T < wGapDeriv T ^ 2)

/- ===== v27（第 200 轮）：形状比与判据比——$S'$ 符号的比值判据（G-188b-2 第二步） ===== -/

/-- 形状比 $\Phi(T):=\dfrac{w(T)}{\tanh\frac{1}{2T}}$：窗口平均相对端点上界的比例
（$T>0$ 时 $\Phi\in(0,1)$，由 v24 的端点亏损恒等式）。 -/
noncomputable def shapePhi (T : ℝ) : ℝ :=
  wGap T / Real.tanh (1 / (2 * T))

/-- 判据比 $r(T):=\dfrac{T^2\,|w'(T)|}{\mathrm{sech}^2\frac{1}{2T}}$：
亏损 $\tanh\frac{1}{2T}-w=\frac T2|w'|$ 折算成"半温差"的分数；$r<1$ 即 $w''>0$ 的判据（v26）。 -/
noncomputable def ratioR (T : ℝ) : ℝ :=
  T ^ 2 * |wGapDeriv T| / sechSq (1 / (2 * T))

/-- **比值判据（G-188b-2d）**：$S'(T)<0\iff\Phi(T)\,(1+r(T))<2\,r(T)$（$T>0$）。
把"$w\,w''$ 与 $(w')^2$ 相乘再比较"化成"两个无量纲比值的比较"：两条边都由链内恒等式读，
且 $w\,w''-(w')^2=\tanh\frac{1}{2T}\cdot\mathrm{sech}^2\frac{1}{2T}\cdot\bigl(\Phi(1+r)-2r\bigr)/T^3$。 -/
def TargetPropShapeSignRatio : Prop :=
  ∀ (T : ℝ), 0 < T →
    (shapeDeriv T < 0 ↔ shapePhi T * (1 + ratioR T) < 2 * ratioR T)

/-- **$r\ge1$ 段的符号定理（G-188b-2e）**：$1\le r(T)$ ⇒ $S'(T)<0$。
$1\le r$ 恰是 $w''\le0$（判据 $r<1$ 的反面），故"$w''\le0$ 段形状项必降"是无条件命题；
$r<1$ 段（$w''>0$）的符号仍须更锐的界，留下一步。 -/
def TargetPropShapeNegOfRatioGeOne : Prop :=
  ∀ (T : ℝ), 0 < T → 1 ≤ ratioR T → shapeDeriv T < 0

end

end CQM.Ring15.Spec






