"""
修正版：晶胞作为Regge剖分顶点
================================

概念修正:
  Regge剖分顶点 = 晶胞（原子/分子/复合物），不是单个原子

  对元素超导体: 晶胞=原子, 顶点=原子
  对化合物: 顶点=晶胞(复合物), 不是组成原子

晶胞不是刚体——晶胞内原子相对运动贡献角亏涨落:

  Δδ₀² = Δδ_inter² + Δδ_intra²

  Δδ_inter: 晶胞间涨落(声学模)
    - 质量 = 晶胞总质量 M_cell
    - 距离 = 晶胞间距离 L ~ a
    - 频率 = 声学模频率 ω_ac

  Δδ_intra: 晶胞内涨落(光学模)
    - 质量 = 约化质量 μ (H轻→μ≈m_H)
    - 距离 = 晶胞内原子间距 l
    - 频率 = 光学模频率 ω_op

  对元素超导体: 晶胞=原子, 无晶胞内结构, Δδ_intra=0
  对氢化物: 晶胞内H相对重原子运动, Δδ_intra主导
"""

import numpy as np
import math

HBAR = 1.0546e-34
KB = 1.381e-23
NA = 6.022e23
AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAMMA_1 = 14.134725
GAMMA_2 = 21.022040
GAP = GAMMA_2 - GAMMA_1
C2_REGGE = 2.0 / 3.0
DELTA_C = 1.0 / BETA

def calc_ddv0_inter(M_cell_amu, L_ang, theta_D, z, f=0.5):
    """晶胞间涨落(声学模)
    M_cell: 晶胞质量(amu)
    L: 晶胞间距离(Å)
    """
    L = L_ang * 1e-10
    omega = theta_D * KB / HBAR
    M = M_cell_amu * AMU
    sum_inv_m = z * 2.0 / M  # z条边, 每条2/M
    ddv0_sq = (C2_REGGE / L**2) * (3*HBAR/(4*omega)) * (1-f) * sum_inv_m
    return math.sqrt(max(ddv0_sq, 0))

def calc_ddv0_intra(edges_intra, l_ang, theta_D, f=0.5):
    """晶胞内涨落(光学模)
    edges_intra: [(m_i_amu, m_j_amu), ...] 晶胞内原子对
    l: 晶胞内原子间距(Å)
    """
    l = l_ang * 1e-10
    omega = theta_D * KB / HBAR
    sum_inv_m = sum((1.0/(mi*AMU) + 1.0/(mj*AMU)) for mi, mj in edges_intra)
    ddv0_sq = (C2_REGGE / l**2) * (3*HBAR/(4*omega)) * (1-f) * sum_inv_m
    return math.sqrt(max(ddv0_sq, 0))

def calc_Tc(ddv0, delta_v, theta_D):
    if BETA * delta_v >= 1:
        return 0, 0
    x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v) * GAP)
    if x > 1:
        arccoth_x = 0.5 * math.log((x + 1) / (x - 1))
        return x, theta_D / (2 * arccoth_x)
    return x, 0

def reverse_delta(ddv0, theta_D, tc_exp, delta_p=0):
    if tc_exp <= 0 or theta_D <= 0:
        return None
    arg = theta_D / (2 * tc_exp)
    if arg < 1.0:
        return None
    x = 1.0 / math.tanh(arg)
    one_minus = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if one_minus <= 0 or one_minus > 1:
        return None
    return (1 - one_minus) / BETA - delta_p

print("=" * 85)
print("修正版: 晶胞作为Regge剖分顶点")
print("=" * 85)

# ============================================================
# A. 元素超导体: 晶胞=原子, 只有Δδ_inter
# ============================================================
print(f"\n{'='*85}")
print("A. 元素超导体: 晶胞=原子, Δδ=Δδ_inter(声学模)")
print(f"{'='*85}")
print(f"{'材料':<6} {'结构':<5} {'M_cell':>7} {'L(Å)':>6} {'z':>4} {'θ_D':>6} {'Tc_exp':>7} {'Δδ₀':>8} {'δ_intr':>10} {'βδ':>8} {'判定':>4}")
print(f"{'-'*80}")

elem_data = [
    ("Nb", "BCC", 92.9, 3.30, 8, 275, 9.25),
    ("V",  "BCC", 50.9, 3.03, 8, 383, 5.40),
    ("Ta", "BCC", 180.9, 3.30, 8, 240, 4.48),
    ("Pb", "FCC", 207.2, 4.95, 12, 105, 7.20),
    ("Al", "FCC", 27.0, 4.05, 12, 428, 1.20),
    ("Hg", "RHL", 200.6, 3.01, 6, 72, 4.15),
    ("Tc", "HCP", 98.9, 2.74, 12, 511, 7.80),
    ("La", "FCC", 138.9, 3.75, 12, 142, 6.00),
    ("Sn", "FCT", 118.7, 5.83, 12, 200, 3.70),
    ("In", "FCT", 114.8, 3.25, 12, 108, 3.40),
]

elem_results = []
for name, struct, M, a, z, theta_D, tc_exp in elem_data:
    if struct == "BCC":
        L = a * math.sqrt(3) / 2
    elif struct == "FCC":
        L = a / math.sqrt(2)
    else:
        L = a

    # 元素: 晶胞=原子, 只有晶胞间涨落
    ddv0 = calc_ddv0_inter(M, L, theta_D, z, f=0.5)
    delta_intr = reverse_delta(ddv0, theta_D, tc_exp)

    if delta_intr is not None:
        beta_d = BETA * delta_intr
        ok = "✓" if 0.8 < delta_intr/DELTA_C < 1.2 else "?"
        elem_results.append((name, ddv0, delta_intr, ok))
        print(f"{name:<6} {struct:<5} {M:>7.1f} {L:>6.3f} {z:>4} {theta_D:>6} {tc_exp:>7.2f} {ddv0:>8.5f} {delta_intr:>10.6f} {beta_d:>8.4f} {ok:>4}")
    else:
        print(f"{name:<6} {struct:<5} {M:>7.1f} {L:>6.3f} {z:>4} {theta_D:>6} {tc_exp:>7.2f} {ddv0:>8.5f} {'N/A':>10} {'N/A':>8} {'??':>4}")

# ============================================================
# B. 氢化物: 晶胞=复合物, Δδ=Δδ_inter+Δδ_intra
# ============================================================
print(f"\n{'='*85}")
print("B. 氢化物: 晶胞=复合物, Δδ=Δδ_inter(声学)+Δδ_intra(光学)")
print(f"{'='*85}")

hydride_data = [
    # name, a, B(GPa), P(GPa), θ_D, Tc_exp
    # 晶胞内: H相对重原子运动
    ("H3S", 3.08, 350, 155, 300, 203,
     35.0,        # M_cell = 32+3 = 35 amu (化学式单元)
     3.08,        # L = a (晶胞间)
     6,           # z_inter (cubic)
     [(32.1, 1.0)]*6,  # 晶胞内S-H边
     3.08/math.sqrt(2)),  # l_intra = S-H距离
    ("LaH10", 5.10, 280, 170, 350, 250,
     148.9,       # M_cell = 139+10 = 149
     5.10,
     12,
     [(138.9, 1.0)]*12,  # La-H边
     5.10/math.sqrt(2)),
    ("YH6", 3.10, 220, 166, 280, 224,
     94.9,        # 89+6 = 95
     3.10, 8,
     [(88.9, 1.0)]*8, 3.10/math.sqrt(2)),
    ("CaH6", 3.30, 220, 150, 300, 235,
     46.1,        # 40+6
     3.30, 8,
     [(40.1, 1.0)]*8, 3.30/math.sqrt(2)),
    ("ScH6", 3.13, 200, 130, 280, 287,
     51.0,        # 45+6
     3.13, 8,
     [(45.0, 1.0)]*8, 3.13/math.sqrt(2)),
]

print(f"{'材料':<8} {'M_cell':>7} {'δ_P':>7} {'Δδ_inter':>9} {'Δδ_intra':>9} {'Δδ_total':>9} {'x':>7} {'Tc_calc':>8} {'Tc_exp':>8} {'比值':>7}")
print(f"{'-'*80}")

hyd_results = []
for name, a, B, P, theta_D, tc_exp, M_cell, L, z_inter, edges_intra, l_intra in hydride_data:
    delta_P = P / (3 * B) if B > 0 else 0
    delta_v = min(delta_P, 1.0 / (2 * BETA))

    # 晶胞间涨落(声学模)
    ddv_inter = calc_ddv0_inter(M_cell, L, theta_D, z_inter, f=0.5)

    # 晶胞内涨落(光学模)
    ddv_intra = calc_ddv0_intra(edges_intra, l_intra, theta_D, f=0.5)

    # 总涨落
    ddv0 = math.sqrt(ddv_inter**2 + ddv_intra**2)

    x, tc_calc = calc_Tc(ddv0, delta_v, theta_D)

    ratio = tc_calc/tc_exp if tc_calc > 0 and tc_exp > 0 else 0
    ok = "✓" if 0.5 < ratio < 2.0 else "?"
    hyd_results.append((name, ddv_inter, ddv_intra, ddv0, tc_calc, tc_exp, ratio, ok))

    r_str = f"{ratio:.2f}" if ratio > 0 else "—"
    tc_str = f"{tc_calc:.1f}" if tc_calc > 0 else "0"
    print(f"{name:<8} {M_cell:>7.1f} {delta_v:>7.4f} {ddv_inter:>9.5f} {ddv_intra:>9.5f} {ddv0:>9.5f} {x:>7.3f} {tc_str:>8} {tc_exp:>8.0f} {r_str:>7} {ok}")

# ============================================================
# C. 化合物: 晶胞=复合物
# ============================================================
print(f"\n{'='*85}")
print("C. 二元化合物: 晶胞=复合物, Δδ=Δδ_inter+Δδ_intra")
print(f"{'='*85}")

comp_data = [
    # A15: Nb3Sn, 晶胞含8原子(4Nb3Sn), 化学式单元Nb3Sn
    ("Nb3Sn", 5.29, 228, 18.5,
     397.4,       # M_cell = 3×92.9+118.7 = 397.4
     5.29,        # L (晶胞间)
     6,           # z_inter
     [(92.9, 118.7)]*6,  # Nb-Sn边
     5.29/2),     # l_intra
    ("Nb3Ge", 5.14, 230, 23.2,
     351.3, 5.14, 6,
     [(92.9, 72.6)]*6, 5.14/2),
    ("V3Si", 4.72, 330, 17.1,
     180.8, 4.72, 6,
     [(50.9, 28.1)]*6, 4.72/2),
    ("MgB2", 3.52, 900, 39.0,
     45.9,        # 24.3+2×10.8 = 45.9
     3.52, 6,
     [(24.3, 10.8)]*6, 3.52/2),
    ("NbTi", 3.27, 250, 9.5,
     140.8,       # 92.9+47.9
     3.27*math.sqrt(3)/2, 8,
     [(92.9, 47.9)]*8, 3.27*math.sqrt(3)/2),
]

print(f"{'材料':<8} {'M_cell':>7} {'Δδ_inter':>9} {'Δδ_intra':>9} {'Δδ_total':>9} {'Tc_exp':>7} {'δ_intr':>10} {'βδ':>8} {'判定':>4}")
print(f"{'-'*70}")

comp_results = []
for name, a, theta_D, tc_exp, M_cell, L, z_inter, edges_intra, l_intra in comp_data:
    ddv_inter = calc_ddv0_inter(M_cell, L, theta_D, z_inter, f=0.5)
    ddv_intra = calc_ddv0_intra(edges_intra, l_intra, theta_D, f=0.5)
    ddv0 = math.sqrt(ddv_inter**2 + ddv_intra**2)

    delta_intr = reverse_delta(ddv0, theta_D, tc_exp)

    if delta_intr is not None:
        beta_d = BETA * delta_intr
        ok = "✓" if 0.5 < delta_intr/DELTA_C < 2.0 else "?"
        comp_results.append((name, ddv0, delta_intr, ok))
        print(f"{name:<8} {M_cell:>7.1f} {ddv_inter:>9.5f} {ddv_intra:>9.5f} {ddv0:>9.5f} {tc_exp:>7.1f} {delta_intr:>10.6f} {beta_d:>8.4f} {ok:>4}")
    else:
        print(f"{name:<8} {M_cell:>7.1f} {ddv_inter:>9.5f} {ddv_intra:>9.5f} {ddv0:>9.5f} {tc_exp:>7.1f} {'N/A':>10} {'N/A':>8} {'??':>4}")

# ============================================================
# D. 铜氧化物: 晶胞=复合物
# ============================================================
print(f"\n{'='*85}")
print("D. 铜氧化物: 晶胞=CuO2复合物")
print(f"{'='*85}")

cup_data = [
    ("La2CuO4", 3.79, 400, 14.0),
    ("YBCO7", 3.85, 400, 92.0),
    ("Bi2212", 3.83, 350, 85.0),
    ("Bi2223", 3.85, 350, 110.0),
    ("Hg1223", 3.86, 350, 134.0),
]

print(f"{'材料':<12} {'M_cell':>7} {'Δδ_inter':>9} {'Δδ_intra':>9} {'Δδ_total':>9} {'Tc_exp':>7} {'δ_intr':>10} {'βδ':>8} {'判定':>4}")
print(f"{'-'*75}")

cup_results = []
for name, a, theta_D, tc_exp in cup_data:
    # CuO2单元: M = 63.5 + 2×16 = 95.5
    M_cell = 95.5
    L = a
    z_inter = 4  # 平面内
    # 晶胞内: Cu-O边
    edges_intra = [(63.5, 16.0)] * 4
    l_intra = a / 2

    ddv_inter = calc_ddv0_inter(M_cell, L, theta_D, z_inter, f=0.5)
    ddv_intra = calc_ddv0_intra(edges_intra, l_intra, theta_D, f=0.5)
    ddv0 = math.sqrt(ddv_inter**2 + ddv_intra**2)

    delta_intr = reverse_delta(ddv0, theta_D, tc_exp)

    if delta_intr is not None:
        beta_d = BETA * delta_intr
        ok = "✓" if 0.3 < delta_intr/DELTA_C < 3.0 else "?"
        cup_results.append((name, ddv0, delta_intr, ok))
        print(f"{name:<12} {M_cell:>7.1f} {ddv_inter:>9.5f} {ddv_intra:>9.5f} {ddv0:>9.5f} {tc_exp:>7.1f} {delta_intr:>10.6f} {beta_d:>8.4f} {ok:>4}")

# ============================================================
# E. 铁基: 晶胞=FeAs复合物
# ============================================================
print(f"\n{'='*85}")
print("E. 铁基: 晶胞=FeAs复合物")
print(f"{'='*85}")

iron_data = [
    ("LaFeAsO", 4.03, 360, 26.0),
    ("SmFeAsO", 3.94, 360, 55.0),
    ("FeSe", 3.77, 280, 8.0),
    ("BaFe2As2", 3.96, 300, 38.0),
    ("LiFeAs", 3.77, 300, 18.0),
]

print(f"{'材料':<12} {'M_cell':>7} {'Δδ_inter':>9} {'Δδ_intra':>9} {'Δδ_total':>9} {'Tc_exp':>7} {'δ_intr':>10} {'βδ':>8} {'判定':>4}")
print(f"{'-'*75}")

iron_results = []
for name, a, theta_D, tc_exp in iron_data:
    # FeAs单元: M = 55.8 + 74.9 = 130.7
    M_cell = 130.7
    L = a
    z_inter = 4
    edges_intra = [(55.8, 74.9)] * 4
    l_intra = a / 2

    ddv_inter = calc_ddv0_inter(M_cell, L, theta_D, z_inter, f=0.5)
    ddv_intra = calc_ddv0_intra(edges_intra, l_intra, theta_D, f=0.5)
    ddv0 = math.sqrt(ddv_inter**2 + ddv_intra**2)

    delta_intr = reverse_delta(ddv0, theta_D, tc_exp)

    if delta_intr is not None:
        beta_d = BETA * delta_intr
        ok = "✓" if 0.3 < delta_intr/DELTA_C < 3.0 else "?"
        iron_results.append((name, ddv0, delta_intr, ok))
        print(f"{name:<12} {M_cell:>7.1f} {ddv_inter:>9.5f} {ddv_intra:>9.5f} {ddv0:>9.5f} {tc_exp:>7.1f} {delta_intr:>10.6f} {beta_d:>8.4f} {ok:>4}")

# ============================================================
# 汇总
# ============================================================
print(f"\n{'='*85}")
print("汇总")
print(f"{'='*85}")

cats = [
    ("A. 元素", elem_results),
    ("C. 化合物", comp_results),
    ("D. 铜氧化物", cup_results),
    ("E. 铁基", iron_results),
]

print(f"\n{'类别':<15} {'总数':>5} {'成功':>5} {'成功率':>7}")
print(f"{'-'*35}")
total = 0; success = 0
for cat, res in cats:
    t = len(res); s = sum(1 for r in res if r[-1] == "✓")
    print(f"{cat:<15} {t:>5} {s:>5} {s/t*100:>6.0f}%")
    total += t; success += s

# 氢化物单独
t_h = len(hyd_results); s_h = sum(1 for r in hyd_results if r[-1] == "✓")
print(f"{'B. 氢化物':<15} {t_h:>5} {s_h:>5} {s_h/t_h*100:>6.0f}%")
total += t_h; success += s_h

print(f"{'-'*35}")
print(f"{'总计':<15} {total:>5} {success:>5} {success/total*100:>6.0f}%")

# 涨落贡献分析
print(f"\n涨落贡献分析 (Δδ_inter vs Δδ_intra):")
print(f"{'材料':<8} {'Δδ_inter':>10} {'Δδ_intra':>10} {'intra/inter':>12} {'主导':>8}")
print(f"{'-'*50}")
for name, ddv_i, ddv_n, ddv0, tc_c, tc_e, r, ok in hyd_results:
    ratio = ddv_n / ddv_i if ddv_i > 0 else 999
    dom = "intra" if ddv_n > ddv_i else "inter"
    print(f"{name:<8} {ddv_i:>10.5f} {ddv_n:>10.5f} {ratio:>12.2f} {dom:>8}")

print(f"""
  物理图像:
    1. Regge剖分顶点 = 晶胞(原子/分子/复合物), 不是单个原子
    2. 晶胞不是刚体: 晶胞内原子相对运动贡献角亏涨落
    3. 双尺度涨落:
       - Δδ_inter: 晶胞间(声学模), 用晶胞质量M_cell
       - Δδ_intra: 晶胞内(光学模), 用约化质量μ
    4. 元素超导体: 晶胞=原子, 只有Δδ_inter
    5. 氢化物: Δδ_intra主导(H轻→约化质量小→涨落大)
    6. 铜氧化物: CuO2晶胞, Δδ_intra来自Cu-O相对运动
""")