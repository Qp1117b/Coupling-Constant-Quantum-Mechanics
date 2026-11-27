import Mathlib.Data.Real.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Tactic.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-!
# CQM 超导发生学：基础索引与状态

本目录只承载《CQM_探索_推导链》的 27 环发生学。原则：

- 能定义的只定义，能证的只证代数/定义层命题；
- 物理同一、数值、表示论与热力学身份不证，登记为缺口；
- 不使用 `axiom`、`sorry`、`admit`、`native_decide`、`unsafe`；
- 每个 `def`/`theorem` 的 docstring 标明所属环与缺口。
-/

namespace CQM.SuperconductivityChain

/-- 27 环发生学索引；`r1`–`r27` 与推导链环号一一对应。 -/
inductive RingIndex
  | r1 | r2 | r3 | r4 | r5 | r6 | r7 | r8 | r9
  | r10 | r11 | r12 | r13 | r14 | r15 | r16 | r17 | r18
  | r19 | r20 | r21 | r22 | r23 | r24 | r25 | r26 | r27
  deriving DecidableEq, Repr

namespace RingIndex

/-- 环号（自然数 1–27）。 -/
def toNat : RingIndex → Nat
  | r1 => 1 | r2 => 2 | r3 => 3 | r4 => 4 | r5 => 5 | r6 => 6 | r7 => 7
  | r8 => 8 | r9 => 9 | r10 => 10 | r11 => 11 | r12 => 12 | r13 => 13
  | r14 => 14 | r15 => 15 | r16 => 16 | r17 => 17 | r18 => 18 | r19 => 19
  | r20 => 20 | r21 => 21 | r22 => 22 | r23 => 23 | r24 => 24 | r25 => 25
  | r26 => 26 | r27 => 27

/-- 阶段号（1–9）；阶段是章，环是步，不另立并列轴。 -/
def stage : RingIndex → Nat
  | r1 => 1
  | r2 => 1
  | r3 => 1
  | r4 => 1
  | r5 => 2
  | r6 => 2
  | r7 => 2
  | r8 => 3
  | r9 => 3
  | r10 => 3
  | r11 => 4
  | r12 => 4
  | r13 => 5
  | r14 => 6
  | r15 => 7
  | r16 => 7
  | r17 => 7
  | r18 => 7
  | r19 => 8
  | r20 => 8
  | r21 => 8
  | r22 => 8
  | r23 => 8
  | r24 => 8
  | r25 => 9
  | r26 => 9
  | r27 => 9

/-- 环名（代码内短名；中文名称见目录 `README.md`）。 -/
def name : RingIndex → String
  | r1 => "reproduction_commutator"
  | r2 => "phonon_field"
  | r3 => "deficit_angle"
  | r4 => "deficit_fluctuation"
  | r5 => "proper_time_speed"
  | r6 => "history_pair"
  | r7 => "difference_rate"
  | r8 => "distributed_noncommutativity"
  | r9 => "variance"
  | r10 => "pair_strength"
  | r11 => "pair_charge"
  | r12 => "allowed_channel"
  | r13 => "pair_domain"
  | r14 => "memory_kernel_start"
  | r15 => "percolation"
  | r16 => "resource_allocation"
  | r17 => "expansion"
  | r18 => "termination"
  | r19 => "crisis"
  | r20 => "anchor_isomorphism"
  | r21 => "anchor_switch"
  | r22 => "anchor_kernel"
  | r23 => "order_group"
  | r24 => "kernel_spatial"
  | r25 => "kernel_integral"
  | r26 => "prime_oscillation"
  | r27 => "riemann_encoding"

end RingIndex

open RingIndex

/-- 全部环的显式清单；用 `allRings_length` 校验没有漏环。 -/
def allRings : List RingIndex :=
  [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14,
   r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27]

theorem allRings_length : allRings.length = 27 := by
  decide

/-- 环状态；对应推导链 §15 的状态栏，不把构造升格为已证。 -/
inductive RingStatus
  | interpretation
  | strict
  | geometricStrict
  | conditionalStrict
  | constructed
  | assumption
  | unproved
  | standardMath
  | target
  deriving DecidableEq, Repr

/-- 27 环状态登记。该表只抄录推导链 §15 的状态，不重新判定。 -/
def ringStatus : RingIndex → RingStatus
  | r1 => .interpretation
  | r2 => .geometricStrict
  | r3 => .geometricStrict
  | r4 => .conditionalStrict
  | r5 => .assumption
  | r6 => .strict
  | r7 => .strict
  | r8 => .constructed
  | r9 => .conditionalStrict
  | r10 => .conditionalStrict
  | r11 => .strict
  | r12 => .standardMath
  | r13 => .constructed
  | r14 => .constructed
  | r15 => .constructed
  | r16 => .constructed
  | r17 => .constructed
  | r18 => .strict
  | r19 => .unproved
  | r20 => .strict
  | r21 => .conditionalStrict
  | r22 => .constructed
  | r23 => .constructed
  | r24 => .strict
  | r25 => .constructed
  | r26 => .constructed
  | r27 => .constructed

/-- 缺口性质；只描述缺口类型，不表示“可忽略”。 -/
inductive GapStatus
  | structural
  | missingDefinition
  | missingDynamics
  | external
  | conjecture
  | unproved
  deriving DecidableEq, Repr

end CQM.SuperconductivityChain
