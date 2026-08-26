# -*- coding: utf-8 -*-
"""
CQM 超导理论核心计算模块

包含：
  - 物理常数（SI）
  - CQM 理论固定常数（A4谱间隙、谱量子常数C等）
  - 角亏 δ_v 估算（从晶格结构/层状参数）
  - 零温涨落 Δδ_0（中子缺陷模型）
  - 声子频率 Ω_0（从德拜温度）
  - BCS-CQM 修正 Tc 公式（跃迁耦级 2ln n 修正版）
  - McMillan / Allen-Dynes 强耦合 Tc
  - 自由能交叉 Tc = (E2-E1)/(S2-S1)
  - 跃迁耦级 n 判定（磁通量子/能隙比）
"""
import math
from dataclasses import dataclass
from typing import Optional
import os
import sys

_super_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _super_dir not in sys.path:
    sys.path.insert(0, _super_dir)

from cqm_framework.constants import (
    HBAR, KB, PI, GAMMA_EULER,
    A4_EIGENVALUES, SPECTRAL_GAP, SPECTRAL_QUANTUM_C,
    FIRST_COUPLING_E1, MATHIEU_CRITICAL, DYNKIN_INDEX,
    LN4, BETA_CQM, TRANSITION_N_VALUES,
    transition_coupling, spectral_constant,
)

BCS_PREFACTOR = 1.1339
UNIVERSAL_GAP_RATIO = 3.5278

DEFAULT_BETA = BETA_CQM
DEFAULT_DELTA_0 = None
DEFAULT_MU_STAR = 0.13


@dataclass
class CQMParameters:
    delta_v: float = 0.0
    delta_delta_0: float = 0.0
    omega_0: float = 0.0
    beta: float = DEFAULT_BETA
    n_transition: int = 2
    lambda_epc: float = 0.0
    mu_star: float = DEFAULT_MU_STAR
    theta_D: float = 0.0
    omega_log: float = 0.0
    omega_rms: float = 0.0


@dataclass
class SuperconductorRecord:
    formula: str
    tc_experimental: float
    pressure_gpa: float = 0.0
    family: str = ""
    year: int = 0
    theta_D: Optional[float] = None
    lambda_epc: Optional[float] = None
    mu_star: float = DEFAULT_MU_STAR
    source: str = ""
    is_ambient: bool = True
    gap_ratio: Optional[float] = None
    pairing_symmetry: str = ""
    is_multigap: bool = False
    flux_quantum_factor: int = 2



def debye_to_omega(theta_D: float) -> float:
    return KB * theta_D / HBAR


def debye_to_omega_log_K(theta_D: float) -> float:
    """德拜模型对数平均声子频率 ω_log (K单位，用于McMillan/Allen-Dynes)"""
    return 0.65 * theta_D


def debye_to_omega_rms_K(theta_D: float) -> float:
    """德拜模型均方根声子频率 √⟨ω²⟩ (K单位)"""
    return 0.77 * theta_D



def estimate_delta_v_layered(n_layers: int, mismatch: float = 0.05) -> float:
    return n_layers * mismatch * (PI / 3.0)


def estimate_delta_v_caged(n_hydrogen: int, compression: float = 0.1) -> float:
    return n_hydrogen * compression * SPECTRAL_GAP


def estimate_delta_v_a15() -> float:
    return 0.03


def estimate_delta_v_bcc() -> float:
    return 0.01


def estimate_delta_v_fcc() -> float:
    return 0.005


def estimate_delta_delta_0(delta_0: float, beta: float, n_total: int,
                            family: str = "", delta_v: float = 0.0) -> float:
    """
    零温涨落 Δδ_0 估算
    物理范围: ~0.05-0.30
    - 简单元素: 0.05-0.10
    - 层状结构: 0.10-0.20
    - 笼状结构: 0.15-0.30
    - 与角亏 δ_v 正相关
    """
    base = 0.05 + 0.5 * delta_v  # 基础值与角亏正相关
    # 家族修正
    if "铜氧化物" in family:
        base *= 2.5
    elif "铁基" in family:
        base *= 2.0
    elif "富氢化物" in family or "三元富氢化物" in family:
        base *= 3.0
    elif "A15" in family:
        base *= 1.5
    return min(max(base, 0.03), 0.50)


def bcs_cqm_tc(params: CQMParameters) -> float:
    C = spectral_constant()
    sqr = math.sqrt(max(1.0 - params.beta * params.delta_v, 1e-10))
    coupling_log = transition_coupling(params.n_transition)
    denominator = params.beta * coupling_log * params.delta_delta_0
    if denominator < 1e-15:
        return 0.0
    y = C * sqr / denominator
    if y >= 1.0:
        return 0.0
    return HBAR * params.omega_0 / (2.0 * KB * math.atanh(y * y))


def mcmillan_tc(omega_log_K: float, lambda_epc: float, mu_star: float) -> float:
    """
    McMillan 经典强耦合公式 (omega_log 用 K 单位)
    Tc = (ω_log/1.2) · exp[-1.04(1+λ)/(λ-μ*(1+0.62λ))]
    """
    denom = lambda_epc - mu_star * (1.0 + 0.62 * lambda_epc)
    if denom <= 0:
        return 0.0
    exponent = -1.04 * (1.0 + lambda_epc) / denom
    return (omega_log_K / 1.2) * math.exp(exponent)


def allen_dynes_tc(omega_log_K: float, omega_rms_K: float,
                   lambda_epc: float, mu_star: float) -> float:
    """
    Allen-Dynes 1975 强耦合公式 (omega 用 K 单位)
    """
    denom = lambda_epc - mu_star * (1.0 + 0.62 * lambda_epc)
    if denom <= 0:
        return 0.0
    exponent = -1.04 * (1.0 + lambda_epc) / denom
    tc_base = (omega_log_K / 1.2) * math.exp(exponent)
    lambda1 = 2.46 * (1.0 + 3.8 * mu_star)
    f1 = (1.0 + (lambda_epc / lambda1) ** 1.5) ** (1.0 / 3.0)
    if omega_log_K > 0 and omega_rms_K > 0:
        ratio = omega_rms_K / omega_log_K
        lambda2 = 1.82 * (1.0 + 6.3 * mu_star) * omega_rms_K
        f2 = 1.0 + ((ratio - 1.0) * lambda_epc ** 2) / (lambda_epc ** 2 + lambda2 ** 2)
    else:
        f2 = 1.0
    return tc_base * f1 * f2


def free_energy_crossing_tc(E1: float, E2: float, S1: float, S2: float) -> float:
    ds = S2 - S1
    if abs(ds) < 1e-15:
        return float('inf')
    return (E2 - E1) / ds


def estimate_macroscopic_energy(n: int, theta_D: float, lambda_epc: float,
                                 delta_v: float, beta: float) -> float:
    """
    结构群 U(1)/Z_n 的宏观能量 E_n (单位: K, 即 E/kB)
    E_n/kB ≈ θ_D · λ · (1 - βδ_v) · ln(n) / (2π)
    n=1: 基态（无凝聚），E_1/kB ≈ θ_D·λ·(1-βδ_v)/(2π)·ln(1) = 0
    """
    return theta_D * lambda_epc * (1.0 - beta * delta_v) * math.log(n) / (2.0 * PI)


def estimate_entropy(n: int, theta_D: float, lambda_epc: float,
                     delta_v: float, beta: float) -> float:
    """
    结构群 U(1)/Z_n 的熵 S_n (单位: kB)
    S_n/kB ≈ λ · ln(n) · (1 + 1/(2n²)) · (1 + βδ_v)
    n=1: S_1 = 0（无简并）
    """
    return lambda_epc * math.log(n) * (1.0 + 1.0 / (2.0 * n * n)) * (1.0 + beta * delta_v)


def eligibility_margin(delta_delta_0: float, delta_v: float, beta: float,
                        n: int, C: Optional[float] = None) -> float:
    if C is None:
        C = spectral_constant()
    sqr = math.sqrt(max(1.0 - beta * delta_v, 1e-10))
    threshold = C * sqr / (2.0 * beta * math.log(n))
    return delta_delta_0 - threshold


def infer_n_from_gap_ratio(gap_ratio: float) -> int:
    if abs(gap_ratio - 3.53) < 0.3:
        return 2
    elif 4.0 < gap_ratio < 5.0:
        return 4
    elif gap_ratio >= 5.0:
        return 6
    return 2


def infer_n_from_pairing(symmetry: str) -> int:
    s = symmetry.lower()
    if 'd' in s:
        return 4
    if 'p' in s:
        return 6
    return 2


FAMILY_PARAMS = {
    "元素超导体": {"delta_v_func": lambda: estimate_delta_v_bcc(), "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
    "A15": {"delta_v_func": estimate_delta_v_a15, "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
    "铜氧化物": {"delta_v_func": lambda: estimate_delta_v_layered(3, 0.08), "n_layers": 3, "is_layered": True, "typical_n": 4, "pairing": "d"},
    "铁基": {"delta_v_func": lambda: estimate_delta_v_layered(2, 0.05), "n_layers": 2, "is_layered": True, "typical_n": 4, "pairing": "s±"},
    "富氢化物": {"delta_v_func": lambda: estimate_delta_v_caged(10, 0.15), "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
    "二硼化镁": {"delta_v_func": lambda: estimate_delta_v_layered(1, 0.06), "n_layers": 1, "is_layered": True, "typical_n": 2, "pairing": "s"},
    "重费米子": {"delta_v_func": lambda: 0.02, "n_layers": 0, "is_layered": False, "typical_n": 6, "pairing": "p"},
    "钌酸盐": {"delta_v_func": lambda: 0.015, "n_layers": 2, "is_layered": True, "typical_n": 6, "pairing": "p"},
    "无限层镍酸盐": {"delta_v_func": lambda: estimate_delta_v_layered(1, 0.07), "n_layers": 1, "is_layered": True, "typical_n": 4, "pairing": "d"},
    "石墨插层": {"delta_v_func": lambda: estimate_delta_v_layered(1, 0.03), "n_layers": 1, "is_layered": True, "typical_n": 2, "pairing": "s"},
    "富勒烯": {"delta_v_func": lambda: 0.04, "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
    "有机超导体": {"delta_v_func": lambda: 0.025, "n_layers": 2, "is_layered": True, "typical_n": 4, "pairing": "d"},
    "高压元素超导体": {"delta_v_func": lambda: 0.02, "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
    "三元富氢化物": {"delta_v_func": lambda: estimate_delta_v_caged(12, 0.18), "n_layers": 0, "is_layered": False, "typical_n": 2, "pairing": "s"},
}


def get_family_params(family: str) -> dict:
    for key, params in FAMILY_PARAMS.items():
        if key in family or family in key:
            return params
    return FAMILY_PARAMS["元素超导体"]


def estimate_cqm_params(record: SuperconductorRecord,
                        beta: float = DEFAULT_BETA,
                        delta_0: float = DEFAULT_DELTA_0) -> CQMParameters:
    family_params = get_family_params(record.family)
    delta_v = family_params["delta_v_func"]()
    theta_D = record.theta_D or 300.0
    omega_0 = debye_to_omega(theta_D)
    omega_log = debye_to_omega_log_K(theta_D)
    omega_rms = debye_to_omega_rms_K(theta_D)
    n_atoms = sum(1 for c in record.formula if c.isupper())
    n_total = max(n_atoms * 10, 20)
    delta_delta_0 = estimate_delta_delta_0(delta_0, beta, n_total, record.family, delta_v)
    n_transition = family_params["typical_n"]
    if record.gap_ratio:
        n_transition = infer_n_from_gap_ratio(record.gap_ratio)
    elif record.pairing_symmetry:
        n_transition = infer_n_from_pairing(record.pairing_symmetry)
    lambda_epc = record.lambda_epc or 0.5
    return CQMParameters(
        delta_v=delta_v, delta_delta_0=delta_delta_0,
        omega_0=omega_0, beta=beta, n_transition=n_transition,
        lambda_epc=lambda_epc, mu_star=record.mu_star,
        theta_D=theta_D, omega_log=omega_log, omega_rms=omega_rms,
    )


def compute_all_tc_estimates(record: SuperconductorRecord,
                             params: CQMParameters) -> dict:
    results = {}
    results["bcs_cqm"] = bcs_cqm_tc(params)
    if params.lambda_epc > 0 and params.omega_log > 0:
        results["mcmillan"] = mcmillan_tc(params.omega_log, params.lambda_epc, params.mu_star)
        results["allen_dynes"] = allen_dynes_tc(params.omega_log, params.omega_rms, params.lambda_epc, params.mu_star)
    else:
        results["mcmillan"] = 0.0
        results["allen_dynes"] = 0.0
    E1 = estimate_macroscopic_energy(1, params.theta_D, params.lambda_epc, params.delta_v, params.beta)
    E2 = estimate_macroscopic_energy(params.n_transition, params.theta_D, params.lambda_epc, params.delta_v, params.beta)
    S1 = estimate_entropy(1, params.theta_D, params.lambda_epc, params.delta_v, params.beta)
    S2 = estimate_entropy(params.n_transition, params.theta_D, params.lambda_epc, params.delta_v, params.beta)
    results["free_energy_cross"] = free_energy_crossing_tc(E1, E2, S1, S2)
    results["experimental"] = record.tc_experimental
    return results


def eligibility_check(params: CQMParameters) -> dict:
    results = {}
    for n in TRANSITION_N_VALUES:
        margin = eligibility_margin(params.delta_delta_0, params.delta_v, params.beta, n)
        results[n] = {"eligible": margin >= 0, "margin": margin, "coupling_log": transition_coupling_log(n)}
    return results


if __name__ == "__main__":
    print("=" * 70)
    print("CQM 核心模块自检")
    print("=" * 70)
    C = spectral_constant()
    print(f"谱常数 C = {C:.7f}")
    print(f"A4 谱间隙 = {SPECTRAL_GAP:.10f}")
    print(f"ln4 = {LN4:.6f}")
    print()
    print("跃迁耦级谱 2ln(n):")
    for n in TRANSITION_N_VALUES:
        print(f"  n={n}: 2ln({n}) = {transition_coupling_log(n):.4f}")
    print()
    print("--- 测试: Nb ---")
    nb = SuperconductorRecord(formula="Nb", tc_experimental=9.25, family="元素超导体", theta_D=275.0, lambda_epc=0.98, year=1930)
    params = estimate_cqm_params(nb)
    print(f"  delta_v={params.delta_v:.4f}  delta_delta_0={params.delta_delta_0:.4f}")
    print(f"  omega_0={params.omega_0:.3e}  theta_D={params.theta_D:.1f}  lambda={params.lambda_epc:.2f}  n={params.n_transition}")
    tcs = compute_all_tc_estimates(nb, params)
    print(f"  Tc(exp)={tcs['experimental']:.2f}  Tc(McMillan)={tcs['mcmillan']:.2f}  Tc(AD)={tcs['allen_dynes']:.2f}")
    print(f"  Tc(BCS-CQM)={tcs['bcs_cqm']:.2f}  Tc(F-cross)={tcs['free_energy_cross']:.2f}")