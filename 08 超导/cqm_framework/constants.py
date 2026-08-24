# -*- coding: utf-8 -*-
"""
CQM 超导计算框架 - 物理常数与理论常数

纯CQM第一性: 无BCS概念 (无电声耦合λ, 无McMillan, 无μ*)
中子缺陷 δ(Z,N) 是变量 (依赖元素和同位素), 非定值
"""
import math

# === SI 物理常数 ===
HBAR = 1.054571817e-34      # J·s
KB = 1.380649e-23           # J/K
ME = 9.10938370e-31         # kg (电子质量)
E = 1.602176634e-19         # C (电子电荷)
PI = math.pi
GAMMA_EULER = 0.5772156649015329

# === 核子质量 (第一性起点) ===
M_PROTON = 1.6726219e-27    # kg
M_NEUTRON = 1.6749275e-27   # kg
M_NUCLEON = 1.6738e-27      # kg (平均核子质量)
DELTA_M_NP = M_NEUTRON - M_PROTON  # 中子-质子质量差

# === CQM 理论固定常数 ===
A4_MATRIX = [[2, -1, 0, 0], [-1, 2, -1, 0], [0, -1, 2, -1], [0, 0, -1, 2]]
A4_EIGENVALUES = [0.38196601125, 1.38196601125, 2.61803398875, 3.61803398875]
SPECTRAL_GAP = 0.38196601125          # (3-√5)/2 = 1/φ²
SPECTRAL_QUANTUM_C = 0.02309570897    # C = ξ'(1)/ξ(1)
FIRST_COUPLING_E1 = 200.04045483
MATHIEU_CRITICAL = 1.316022911
DYNKIN_INDEX = 5.0 / 3.0
LN4 = math.log(4.0)
PHI = (1.0 + math.sqrt(5.0)) / 2.0  # 黄金比例

# === CQM 几何常数 ===
BETA_CQM = 8.0 * PI + 1.0  # β = 8π+1 ≈ 26.1327 (Klein四元群)

# === 中子缺陷 δ(Z,N) ===
# δ(Z,N) 是依赖元素(Z)和同位素(N)的变量 — 非定值
# δ(Z,N) 的完整函数形式与具体数值是未确认的开放问题
# 不假设具体定值, 不采用质量反推

# === 跃迁耦级谱 ===
TRANSITION_N_VALUES = [2, 4, 6, 8, 10]

def transition_coupling(n: int) -> float:
    """跃迁耦级 2ln(n) (A4表示论 4⊗4=10_s⊕6_a)"""
    return 2.0 * math.log(n)

def spectral_constant() -> float:
    """C = ξ'(1)/ξ(1) = 1 + γ/2 - ln(2√π)"""
    return 1.0 + GAMMA_EULER / 2.0 - math.log(2.0 * math.sqrt(PI))
