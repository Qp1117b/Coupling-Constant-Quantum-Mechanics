# -*- coding: utf-8 -*-
"""
纯CQM第一性推导链 v7: 中子缺陷δ(Z,N)为变量

核心改进 (用户洞察: 中子缺陷本身是变化的, 不是定值):

1. δ(Z,N) = δ_base·(1 + a·(N-Z)/A)
   - δ_base 是基础缺陷值 (从数据拟合, 不假设具体定值)
   - a 是核环境修正系数 (从数据拟合)
   - (N-Z)/A 是中子过剩比
   - 不同元素(Z)和同位素(N)的δ不同
   - δ(Z,N) 的完整函数形式与具体数值是未确认的开放问题

2. δ(Z,N)影响中子嘉当矩阵D(δ)的谱间隙:
   D(δ) = [[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-δ],[0,0,-δ,2]]
   λ_min(δ) = D(δ)的最小本征值
   δ=1时λ_min = (3-√5)/2 (纯A4谱间隙)
   δ≠1时λ_min偏移 → 影响角亏 → 影响Tc

3. 角亏δ_v受δ(Z,N)调制:
   δ_v = δ_v^Lindemann · (λ_min(δ)/λ_min(1))^p
   - δ=1时无修正 (零阶近似)
   - δ≠1时谱间隙变化调制角亏

4. Tc = E_s·(Δδ₀)²·du²/2·exp(-c/η_eff) (v6量子隧穿公式)

无BCS概念: 没有电声耦合λ, 没有McMillan, 没有BCS能隙方程
机制: CQM耦合常数跃迁 α→n²α, 由几何参数(含δ(Z,N))决定
"""
import sys, os, math, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from constants import (HBAR, KB, PI, GAMMA_EULER, PHI,
                        M_PROTON, M_NEUTRON, M_NUCLEON, DELTA_M_NP,
                        BETA_CQM)
from constants import spectral_constant

SPECTRAL_C = spectral_constant()
SPECTRAL_GAP_A4 = (3.0 - math.sqrt(5.0)) / 2.0


def neutron_defect_delta(Z, N, delta_base, a_nuc=0.0):
    """
    中子缺陷δ(Z,N) — 依赖元素和同位素的变量

    δ(Z,N) = δ_base·(1 + a·(N-Z)/A)

    - δ_base: 基础缺陷值 (从数据拟合, 不假设具体定值)
    - a: 核环境修正系数 (从数据拟合)
    - (N-Z)/A: 中子过剩比
    - a=0时退化为定值δ_base
    - δ(Z,N) 的完整函数形式与具体数值是未确认的开放问题
    """
    A = Z + N
    if A == 0:
        return delta_base
    return delta_base * (1.0 + a_nuc * (N - Z) / A)


def neutron_cartan_D(delta):
    """中子嘉当矩阵D(δ) (缺陷形变)"""
    return np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-delta],[0,0,-delta,2]],
                     dtype=float)


def spectral_gap_D(delta):
    """D(δ)的最小本征值 (谱间隙)"""
    D = neutron_cartan_D(delta)
    eigvals = np.linalg.eigvalsh(D)
    return float(eigvals[0])


def lindemann_delta_v(A_sub, E0, a, f_aniso=2.0):
    """Lindemann角亏: δ_v = (δ_rms/a)²·f"""
    M = A_sub * M_NUCLEON
    omega_0 = KB * E0 / HBAR
    delta_rms = math.sqrt(HBAR / (2.0 * M * omega_0))
    return (delta_rms / a)**2 * f_aniso


def delta_v_with_neutron_defect(dv_lind, delta_ZN, p_spec=1.0):
    """
    受中子缺陷调制的角亏:
    δ_v = δ_v^Lind · (λ_min(δ)/λ_min(1))^p

    - δ=1时λ_min(δ)/λ_min(1)=1, 无修正 (零阶近似)
    - δ≠1时谱间隙变化调制角亏
    - p_spec: 谱间隙调制幂次 (从数据拟合)
    """
    lam_min = spectral_gap_D(delta_ZN)
    ratio = lam_min / SPECTRAL_GAP_A4
    return dv_lind * ratio**p_spec


def proper_time_velocity(beta, delta_v):
    return math.sqrt(max(1.0 - beta * delta_v, 1e-10))

def transition_coupling_level(n):
    return 2.0 * math.log(n)


def transition_sufficiency(n, beta, delta_v, dd0):
    """跃迁充盈度η (CQM§9.2资格条件)"""
    dtau = proper_time_velocity(beta, delta_v)
    du = transition_coupling_level(n)
    return beta * du * dd0 / (SPECTRAL_C * dtau)


def delta_dd0_cqm(delta_v, f_aniso, k_dd0):
    """Δδ₀ = k_dd0·√(δ_v/f) (Lindemann零点涨落)"""
    rms = math.sqrt(max(delta_v / max(f_aniso, 0.1), 1e-10))
    return k_dd0 * rms


def tc_quantum_tunneling(n, E_s, beta, delta_v, dd0, E0, c_tun,
                          E_ref, q_e0=1.0):
    """Tc = E_s·(Δδ₀)²·du²/2·exp(-c/η_eff) (量子隧穿)"""
    eta_raw = transition_sufficiency(n, beta, delta_v, dd0)
    eta_eff = eta_raw * (E_ref / max(E0, 1.0))**q_e0

    if eta_eff < 1.0:
        return 0.0, eta_raw, eta_eff

    du = transition_coupling_level(n)
    tunneling = math.exp(-c_tun / eta_eff)
    condensation = dd0**2 * du**2 / 2.0
    tc = E_s * condensation * tunneling
    return tc, eta_raw, eta_eff


def find_best_tc(E_s, beta, delta_v, dd0, E0, c_tun, E_ref, q_e0=1.0):
    if not isinstance(q_e0, (int, float)):
        q_e0 = 1.0
    best_tc = 0.0
    best_n = 0
    best_eta = 0.0
    for n in [2, 4, 6]:
        tc, eta_r, eta_e = tc_quantum_tunneling(
            n, E_s, beta, delta_v, dd0, E0, c_tun, E_ref, q_e0)
        if tc > best_tc:
            best_tc = tc
            best_n = n
            best_eta = eta_e
    return best_tc, best_n, best_eta


# ============================================================
# 材料数据 (含Z和N)
# ============================================================

STRUCTURE_MAP = {
    "Hg": (3.0, 3.0e-10, 202, 80), "Pb": (1.0, 3.5e-10, 208, 82),
    "Nb": (2.0, 3.3e-10, 93, 41), "Al": (1.0, 2.86e-10, 27, 13),
    "V":  (2.0, 3.0e-10, 51, 23), "Sn": (8.0, 2.8e-10, 120, 50),
    "In": (2.0, 3.25e-10, 115, 49), "La": (2.0, 3.7e-10, 139, 57),
    "Ta": (2.0, 3.3e-10, 181, 73), "Tc": (2.0, 2.74e-10, 99, 43),
    "Th": (1.0, 3.6e-10, 232, 90), "Be": (3.0, 2.2e-10, 9, 4),
    "Zn": (3.0, 2.66e-10, 66, 30), "Ga": (5.0, 2.8e-10, 71, 31),
    "Cd": (3.0, 2.98e-10, 114, 48), "Tl": (2.0, 3.4e-10, 205, 81),
    "Re": (2.0, 2.74e-10, 187, 75), "W":  (2.0, 3.16e-10, 184, 74),
    "Mo": (2.0, 3.15e-10, 96, 42), "Zr": (2.0, 3.2e-10, 92, 40),
    "Ru": (2.0, 2.7e-10, 102, 44), "Ti": (2.0, 2.9e-10, 48, 22),
    "Nb3Ge": (6.0, 3.5e-10, 93, 41), "MgB2": (5.0, 3.5e-10, 10, 5),
    "H3S": (10.0, 3.0e-10, 1, 1), "LaH10": (15.0, 3.5e-10, 1, 1),
    "CaH6": (12.0, 3.0e-10, 1, 1), "YH9": (14.0, 3.2e-10, 1, 1),
    "YH6": (12.0, 3.2e-10, 1, 1),
}

KNOWN_SC = [
    ("Hg",80,122,4.15,"元素",275.0), ("Pb",82,126,7.19,"元素",105.0),
    ("Nb",41,52,9.25,"元素",275.0), ("Al",13,14,1.18,"元素",428.0),
    ("V",23,28,5.38,"元素",383.0), ("Sn",50,70,3.72,"元素",200.0),
    ("In",49,66,3.41,"元素",108.0), ("La",57,82,4.90,"元素",142.0),
    ("Ta",73,108,4.48,"元素",240.0), ("Tc",43,56,7.80,"元素",315.0),
    ("Th",90,142,1.37,"元素",163.0), ("Be",4,5,0.026,"元素",1460.0),
    ("Zn",30,36,0.85,"元素",327.0), ("Ga",31,40,1.09,"元素",320.0),
    ("Cd",48,66,0.56,"元素",209.0), ("Tl",81,124,2.39,"元素",78.0),
    ("Re",75,112,1.70,"元素",430.0), ("W",74,110,0.012,"元素",400.0),
    ("Mo",42,54,0.92,"元素",460.0), ("Zr",40,52,0.55,"元素",310.0),
    ("Ru",44,58,0.49,"元素",600.0), ("Ti",22,26,0.39,"元素",420.0),
    ("Nb3Ge",41*3+32,52*3+40,23.2,"A15",302.0),
    ("MgB2",12+2*5,12+2*6,39.0,"MgB2",900.0),
    ("H3S",1*3+16,0*3+32,203.0,"hydride",1500.0),
    ("LaH10",57+10,82,250.0,"hydride",2000.0),
    ("CaH6",20+6,20,215.0,"hydride",1600.0),
    ("YH9",39+9,50,244.0,"hydride",1800.0),
    ("YH6",39+6,50,224.0,"hydride",1700.0),
]


def full_chain(name, E0, E_s, c_tun, k_dd0, E_ref, q_e0,
                delta_base, a_nuc, p_spec, Z, N,
                sn_f=8.0, struct_enh=1.9):
    f_aniso, a, A_sub, Z_struct = STRUCTURE_MAP.get(name, (2.0, 3.3e-10, 100, 50))
    if name == "Sn":
        f_aniso = sn_f

    # 中子缺陷δ(Z,N) — 变量!
    delta_ZN = neutron_defect_delta(Z, N, delta_base, a_nuc)
    lam_min = spectral_gap_D(delta_ZN)

    # Lindemann角亏
    dv_lind = lindemann_delta_v(A_sub, E0, a, f_aniso)

    # 受中子缺陷调制的角亏
    dv = delta_v_with_neutron_defect(dv_lind, delta_ZN, p_spec)

    beta = BETA_CQM
    g = beta * dv
    dtau = proper_time_velocity(beta, dv)
    dd0 = delta_dd0_cqm(dv, f_aniso, k_dd0)

    tc_model, best_n, eta_eff = find_best_tc(
        E_s, beta, dv, dd0, E0, c_tun, E_ref, q_e0)

    struct_f = struct_enh if name in ("Nb3Ge", "MgB2") else 1.0
    tc_pred = tc_model * struct_f

    return {
        'name': name, 'E0': E0, 'delta_v': dv, 'g': g,
        'dtau_dt': dtau, 'dd0': dd0, 'tc_model': tc_model,
        'tc_pred': tc_pred, 'n_best': best_n, 'eta_eff': eta_eff,
        'delta_ZN': delta_ZN, 'lam_min': lam_min,
    }


def evaluate(E_s, c_tun, k_dd0, E_ref, q_e0, delta_base, a_nuc, p_spec,
              sn_f=8.0, struct_enh=1.9, verbose=False):
    results = []
    for name, Z, N, tc_exp, fam, E0 in KNOWN_SC:
        r = full_chain(name, E0, E_s, c_tun, k_dd0, E_ref, q_e0,
                        delta_base, a_nuc, p_spec, Z, N, sn_f, struct_enh)
        results.append({
            'name': name, 'tc_exp': tc_exp, 'tc_pred': r['tc_pred'],
            'family': fam, 'E0': E0, 'delta_v': r['delta_v'],
            'dd0': r['dd0'], 'tc_model': r['tc_model'],
            'n_best': r['n_best'], 'eta_eff': r['eta_eff'],
            'delta_ZN': r['delta_ZN'], 'lam_min': r['lam_min'],
        })

    valid = [r for r in results if r['tc_pred'] > 0 and r['tc_exp'] > 0]
    if not valid:
        return float('inf'), 0, 0, 0, results

    log_errs = [abs(math.log(r['tc_pred'] / r['tc_exp'])) for r in valid]
    exps = [r['tc_exp'] for r in valid]
    preds = [r['tc_pred'] for r in valid]
    r_corr = np.corrcoef(np.log(exps), np.log(preds))[0, 1]
    mean_err = np.mean(log_errs)
    within2 = sum(1 for e in log_errs if e < math.log(2))

    if verbose:
        print_results(results, mean_err, r_corr, within2, len(valid))

    return mean_err, r_corr, within2, len(valid), results


def print_results(results, mean_err, r_corr, w2, nv):
    print(f"\n{'='*125}")
    print("纯CQM v7 (中子缺陷δ(Z,N)为变量 + 量子隧穿exp(-c/η), 无BCS概念)")
    print(f"{'='*125}")
    print(f"\n  {'材料':<8}{'Tc_exp':>7} {'Tc_pred':>7} "
          f"{'E₀':>5} {'δ(Z,N)':>7} {'λ_min':>6} {'δ_v':>8} {'η_eff':>6} {'err':>8}")
    print(f"  {'-'*90}")
    for r in results:
        if r['tc_pred'] > 0 and r['tc_exp'] > 0:
            err = (r['tc_pred'] - r['tc_exp']) / r['tc_exp'] * 100
            marker = " ✓" if abs(math.log(r['tc_pred']/r['tc_exp'])) < math.log(2) else " ✗"
            print(f"  {r['name']:<8}{r['tc_exp']:>7.2f} {r['tc_pred']:>7.2f} "
                  f"{r['E0']:>5.0f} {r['delta_ZN']:>7.4f} {r['lam_min']:>6.4f} "
                  f"{r['delta_v']:>8.5f} {r['eta_eff']:>6.1f} {err:>+7.0f}%{marker}")
        else:
            print(f"  {r['name']:<8}{r['tc_exp']:>7.2f} {'无':>7} "
                  f"{r['E0']:>5.0f} {r['delta_ZN']:>7.4f} {r['lam_min']:>6.4f} "
                  f"{r['delta_v']:>8.5f}")
    if nv > 0:
        print(f"\n  r = {r_corr:+.4f}  误差 = {mean_err:.4f}  2倍内 = {w2}/{nv} ({w2/nv*100:.0f}%)")


def main():
    print("=" * 125)
    print("纯CQM v7: 中子缺陷δ(Z,N)为变量")
    print("δ(Z,N) = δ_base·(1 + a·(N-Z)/A)  (δ_base从数据拟合, a=核环境修正)")
    print("δ_v = δ_v^Lind·(λ_min(δ)/λ_min(1))^p  (谱间隙调制)")
    print("Tc = E_s·(Δδ₀)²·du²/2·exp(-c/η_eff)  (量子隧穿)")
    print("=" * 125)

    print(f"\n【Phase 0】m_p={M_PROTON:.6e}kg, β={BETA_CQM:.4f}, C={SPECTRAL_C:.10f}")
    print(f"  λ_min(A4)={SPECTRAL_GAP_A4:.6f}")
    print(f"  δ_base: 从数据拟合 (不假设具体定值, 未确认的开放问题)")

    # δ(Z,N)变化展示
    print(f"\n【δ(Z,N)变化展示】δ_base=0.99, a_nuc=0.01:")
    for name, Z, N, tc_exp, fam, E0 in [("Nb",41,52,9.25,"元素",275),
                                          ("Pb",82,126,7.19,"元素",105),
                                          ("Al",13,14,1.18,"元素",428),
                                          ("W",74,110,0.012,"元素",400),
                                          ("H3S",1*3+16,0*3+32,203,"hydride",1500)]:
        d = neutron_defect_delta(Z, N, 0.99, 0.01)
        lam = spectral_gap_D(d)
        print(f"  {name}: Z={Z}, N={N}, δ={d:.6f}, λ_min={lam:.6f}, "
              f"δ偏离={d-0.99:+.6f}")

    # 参数扫描
    print(f"\n{'='*125}")
    print("【参数扫描】E_s, c_tun, k_dd0, E_ref, q_e0, delta_base, a_nuc, p_spec")
    print(f"{'='*125}")

    best = (float('inf'), 0, 0, 0, {})
    for E_s in [200, 500, 1000, 2000, 5000]:
        for c_tun in [20, 50, 100, 150]:
            for k_dd0 in [5, 10, 15, 20]:
                for q_e0 in [1.0, 2.0, 3.0]:
                    for delta_base in [0.95, 0.97, 0.99, 0.995, 0.999, 1.0]:
                        for a_nuc in [0.0, 0.005, 0.01, 0.02, 0.05, 0.1, -0.01, -0.02]:
                            for p_spec in [0.0, 0.5, 1.0, 2.0]:
                                me, r, w2, nv, _ = evaluate(
                                    E_s, c_tun, k_dd0, 300.0, q_e0,
                                    delta_base, a_nuc, p_spec)
                                if me < best[0] and nv >= 20:
                                    best = (me, r, w2, nv, {
                                        'E_s': E_s, 'c_tun': c_tun, 'k_dd0': k_dd0,
                                        'E_ref': 300.0, 'q_e0': q_e0,
                                        'delta_base': delta_base,
                                        'a_nuc': a_nuc, 'p_spec': p_spec,
                                    })

    print(f"\n  最优: {best[4]}")
    print(f"  r = {best[1]:+.4f}, 误差 = {best[0]:.4f}, 2倍内 = {best[2]}/{best[3]}")

    p = best[4]
    me, r, w2, nv, results = evaluate(
        p['E_s'], p['c_tun'], p['k_dd0'], p['E_ref'],
        p['q_e0'], p['delta_base'], p['a_nuc'], p['p_spec'], verbose=True)

    output = {
        'model': 'pure_cqm_v7',
        'description': '纯CQM v7: δ(Z,N)变量+量子隧穿, 无BCS概念',
        'params': best[4],
        'statistics': {'r': float(r), 'mean_log_err': float(me),
                        'within_2x': w2, 'total': nv},
        'predictions': [{'name': r['name'], 'tc_exp': r['tc_exp'],
                         'tc_pred': r['tc_pred'], 'family': r['family'],
                         'delta_ZN': r['delta_ZN']}
                        for r in results],
    }
    with open("pure_cqm_v7_best.json", "w", encoding="utf-8") as fp:
        json.dump(output, fp, indent=2, ensure_ascii=False)
    print(f"\n  结果已保存到 pure_cqm_v7_best.json")


if __name__ == "__main__":
    main()