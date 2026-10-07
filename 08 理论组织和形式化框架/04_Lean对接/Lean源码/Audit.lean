import CouplingSpace
import Superconductivity

-- 诚实审计：验证“已证明”定理不偷偷依赖 physical_hypothesis 公理
-- 若某定理的 axiom 列表中含 physical_hypothesis，则它其实依赖未证物理假设。

#print axioms CouplingSpace.robertson_ccr_inequality
#print axioms Superconductivity.Reduction.criticalTemperature_pos
#print axioms Superconductivity.Reduction.bcs_universal_gap_ratio

