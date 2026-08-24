"""
诚实的前向计算检验：CQM超导理论能否独立预言Tc？

核心问题：
  之前"100%成功率"用的是反推法：
    1. 从实验Tc反推δ_v = (1 - 3β²Δδ₀²/(16x·GAP))/β, x=coth(θ_D/(2Tc))
    2. 检查δ_v是否在"合理范围"(0.3-3.0倍1/β)
    3. tc_calc = tc_exp  ← 直接赋值！

  这是数学恒等式：给定任何Tc>0都能反推出δ_v。
  100%成功率来自反推公式的数学结构，不是物理预言。

前向计算应该是：
  1. 从材料结构独立计算Δδ₀（晶格常数、原子质量、Debye温度）
  2. 假设δ_intrinsic（无法独立计算，需DFT Berry曲率）
  3. 正向计算Tc = θ_D/(2·arccoth(x))
  4. 比较Tc_calc与Tc_exp

本脚本做诚实的前向计算，暴露真实差距。
"""

import csv
import re
import math
import numpy as np

HBAR = 1.0546e-34
KB = 1.381e-23
AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAMMA_1 = 14.134725
GAMMA_2 = 21.022040
GAP = GAMMA_2 - GAMMA_1
C2 = 2.0 / 3.0
DELTA_C = 1.0 / BETA

ATOM_DB = {
    'H': (1.008, 0, 0.46, 0), 'He': (4.003, 0, 0.31, 0),
    'Li': (6.94, 344, 1.52, 11), 'Be': (9.01, 1440, 1.12, 130),
    'B': (10.81, 1480, 0.87, 185), 'C': (12.01, 2230, 0.77, 338),
    'N': (14.01, 0, 0.75, 0), 'O': (16.00, 0, 0.73, 0),
    'F': (19.00, 0, 0.72, 0), 'Ne': (20.18, 0, 0.71, 0),
    'Na': (22.99, 158, 1.86, 7), 'Mg': (24.31, 400, 1.60, 35),
    'Al': (26.98, 428, 1.43, 76), 'Si': (28.09, 645, 1.18, 100),
    'P': (30.97, 0, 1.10, 0), 'S': (32.06, 0, 1.05, 0),
    'Cl': (35.45, 0, 1.02, 0), 'K': (39.10, 91, 2.27, 3),
    'Ca': (40.08, 230, 1.97, 15), 'Sc': (44.96, 360, 1.62, 44),
    'Ti': (47.87, 420, 1.47, 110), 'V': (50.94, 383, 1.34, 162),
    'Cr': (52.00, 435, 1.28, 160), 'Mn': (54.94, 410, 1.27, 120),
    'Fe': (55.85, 470, 1.26, 170), 'Co': (58.93, 445, 1.25, 180),
    'Ni': (58.69, 450, 1.24, 180), 'Cu': (63.55, 343, 1.28, 140),
    'Zn': (65.38, 327, 1.34, 70), 'Ga': (69.72, 240, 1.35, 40),
    'Ge': (72.63, 374, 1.22, 75), 'As': (74.92, 0, 1.21, 0),
    'Se': (78.97, 0, 1.20, 0), 'Br': (79.90, 0, 1.20, 0),
    'Rb': (85.47, 56, 2.48, 2), 'Sr': (87.62, 147, 2.15, 12),
    'Y': (88.91, 280, 1.80, 37), 'Zr': (91.22, 291, 1.60, 95),
    'Nb': (92.91, 275, 1.46, 170), 'Mo': (95.96, 425, 1.39, 230),
    'Tc': (98.00, 0, 1.36, 0), 'Ru': (101.07, 0, 1.34, 220),
    'Rh': (102.91, 0, 1.34, 150), 'Pd': (106.42, 274, 1.37, 180),
    'Ag': (107.87, 215, 1.44, 100), 'Cd': (112.41, 209, 1.49, 42),
    'In': (114.82, 108, 1.62, 11), 'Sn': (118.71, 200, 1.58, 50),
    'Sb': (121.76, 0, 1.61, 0), 'Te': (127.60, 0, 1.60, 0),
    'I': (126.90, 0, 1.63, 0), 'Cs': (132.91, 38, 2.65, 2),
    'Ba': (137.33, 110, 2.22, 9), 'La': (138.91, 142, 1.87, 24),
    'Ce': (140.12, 0, 1.82, 22), 'Pr': (140.91, 0, 1.82, 21),
    'Nd': (144.24, 0, 1.82, 20), 'Sm': (150.36, 0, 1.81, 18),
    'Eu': (151.96, 0, 1.81, 8), 'Gd': (157.25, 0, 1.80, 25),
    'Tb': (158.93, 0, 1.79, 25), 'Dy': (162.50, 0, 1.79, 25),
    'Ho': (164.93, 0, 1.78, 26), 'Er': (167.26, 0, 1.78, 26),
    'Tm': (168.93, 0, 1.77, 28), 'Yb': (173.05, 0, 1.77, 10),
    'Lu': (174.97, 0, 1.77, 30), 'Hf': (178.49, 252, 1.59, 110),
    'Ta': (180.95, 240, 1.46, 200), 'W': (183.84, 400, 1.39, 310),
    'Re': (186.21, 430, 1.37, 370), 'Os': (190.23, 500, 1.35, 400),
    'Ir': (192.22, 420, 1.36, 355), 'Pt': (195.08, 240, 1.39, 230),
    'Au': (196.97, 170, 1.44, 180), 'Hg': (200.59, 0, 1.51, 25),
    'Tl': (204.38, 78, 1.70, 8), 'Pb': (207.20, 105, 1.75, 23),
    'Bi': (208.98, 0, 1.70, 0), 'Th': (232.04, 163, 1.80, 54),
    'Pa': (231.04, 0, 1.80, 0), 'U': (238.03, 207, 1.75, 100),
    'Np': (237.05, 0, 1.75, 0), 'Pu': (244.06, 0, 1.75, 0),
    'Am': (243.06, 0, 1.75, 0), 'Cm': (247.07, 0, 1.75, 0),
}

def parse_formula(formula):
    formula = formula.strip()
    formula = re.sub(r'[\(（].*?[\)）]', '', formula)
    tokens = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula)
    result = {}
    for elem, count in tokens:
        if elem in ATOM_DB:
            n = float(count) if count else 1.0
            result[elem] = result.get(elem, 0) + n
    return result

def get_mass(comp):
    return sum(ATOM_DB[e][0] * n for e, n in comp.items() if e in ATOM_DB)

def get_debye(comp):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0] * n) for e, n in comp.items() if e in ATOM_DB and ATOM_DB[e][1] > 0]
    if not ws: return 300
    return sum(d * w for d, w in ws) / sum(w for _, w in ws)

def get_radius(comp):
    rs = [ATOM_DB[e][2] for e in comp if e in ATOM_DB and ATOM_DB[e][2] > 0]
    return np.mean(rs) if rs else 1.5

def get_bulk(comp):
    bs = [ATOM_DB[e][3] for e in comp if e in ATOM_DB and ATOM_DB[e][3] > 0]
    return np.mean(bs) if bs else 50

def ddv_inter(M_amu, L_ang, theta_D, z, f=0.5):
    L = L_ang * 1e-10
    w = theta_D * KB / HBAR
    s = z * 2.0 / (M_amu * AMU)
    return math.sqrt(max((C2/L**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))

def ddv_intra(edges, l_ang, theta_D, f=0.5):
    l = l_ang * 1e-10
    w = theta_D * KB / HBAR
    s = sum((1.0/(mi*AMU) + 1.0/(mj*AMU)) for mi, mj in edges)
    return math.sqrt(max((C2/l**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))

def calc_Tc_forward(ddv0, delta_v, theta_D):
    """前向计算Tc：从Δδ₀和δ_v直接计算"""
    if BETA * delta_v >= 1:
        return 0, 0
    x = 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA*delta_v) * GAP)
    if x > 1:
        arccoth_x = 0.5 * math.log((x+1)/(x-1))
        return x, theta_D / (2 * arccoth_x)
    return x, 0

def rev_delta(ddv0, theta_D, tc, dp=0):
    """反推δ_v"""
    if tc <= 0 or theta_D <= 0: return None
    arg = theta_D / (2*tc)
    if arg < 1: return None
    x = 1.0 / math.tanh(arg)
    om = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if om <= 0 or om > 1: return None
    return (1 - om) / BETA - dp

def estimate_params(formula, category, tc_exp, condition):
    comp = parse_formula(formula)
    n_atoms = sum(comp.values())
    M_cell = get_mass(comp)
    r_avg = get_radius(comp)
    theta_D = get_debye(comp)
    B = get_bulk(comp)
    P_GPa = 0
    if '高压' in condition or 'GPa' in condition:
        pm = re.search(r'~?(\d+)GPa', condition)
        P_GPa = int(pm.group(1)) if pm else 50
    L = 2 * r_avg
    l_intra = 2 * r_avg
    z_inter = 6
    edges_intra = []
    f = 0.5
    cat = category
    if '元素' in cat:
        theta_D = ATOM_DB.get(list(comp.keys())[0], (0, 300, 1.5, 50))[1] or theta_D
        if theta_D < 50: theta_D = 300
        z_inter = 12
        L = 2 * r_avg
        if '高压' in cat:
            elem = list(comp.keys())[0]
            atom_data = ATOM_DB.get(elem, (0, 300, 1.5, 50))
            B = max(atom_data[3], 50) * 3
            P_GPa = 100
        f = 0.5
    elif 'A15' in cat:
        theta_D = max(theta_D, 400); z_inter = 8; L = 2 * r_avg * 0.9; f = 0.4
    elif '氢化物' in cat:
        theta_D = max(theta_D, 1500); B = max(B, 200); P_GPa = max(P_GPa, 150)
        z_inter = 8; L = 2.0; l_intra = 1.7
        n_h = comp.get('H', 0); n_metal = n_atoms - n_h
        if n_h > 0 and n_metal > 0:
            m_metal = (M_cell - n_h * 1.008) / n_metal
            edges_intra = [(m_metal, 1.008)] * int(min(n_h, 4))
        f = 0.5
    elif '铜氧' in cat:
        theta_D = max(theta_D, 400); z_inter = 6; L = 3.8; l_intra = 1.9
        if 'Cu' in comp and 'O' in comp: edges_intra = [(63.55, 16.0)] * 2
        f = 0.4
    elif '铁基' in cat:
        theta_D = max(theta_D, 350); z_inter = 6; L = 3.5; l_intra = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges_intra = [(55.85, 74.92)] * 2
            elif 'Se' in comp: edges_intra = [(55.85, 78.97)] * 2
            elif 'Te' in comp: edges_intra = [(55.85, 127.60)] * 2
        f = 0.4
    elif '有机' in cat:
        theta_D = max(theta_D, 100); z_inter = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat:
        theta_D = 100; z_inter = 4; L = 10.0; M_cell = 720; f = 0.5
    elif '石墨' in cat:
        theta_D = 200; z_inter = 3; L = 3.35; f = 0.5
    elif '合金' in cat:
        theta_D = max(theta_D, 200); z_inter = 12; f = 0.5
    else:
        theta_D = max(theta_D, 200); z_inter = 8; f = 0.5
    return theta_D, M_cell, L, z_inter, edges_intra, l_intra, B, P_GPa, f

# ============================================================
# 读取数据
# ============================================================
input_file = r"D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv"
with open(input_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

# ============================================================
# Part 1: 暴露反推法的数学结构
# ============================================================
print("=" * 100)
print("Part 1: 反推法的数学结构——为什么'100%成功率'是假象")
print("=" * 100)

print("""
反推法:
  x = coth(θ_D/(2Tc_exp))           ← 从实验Tc得到x
  δ_v = (1 - 3β²Δδ₀²/(16x·GAP))/β  ← 从x和Δδ₀反推δ_v
  判定: 0.3 < δ_v/(1/β) < 3.0      ← 3倍范围都算"成功"

这是数学恒等式：给定任何Tc>0, 都能反推δ_v。
"成功"只要求δ_v落在(0.011, 0.115)——这是极宽的范围。
""")

# 验证：对任意Tc，反推都能给出δ_v
print("验证——对任意Tc反推δ_v:")
print(f"  {'Tc(K)':>10} {'θ_D(K)':>8} {'x':>10} {'δ_v(反推)':>12} {'δ_v/(1/β)':>10}")
for tc in [0.01, 0.1, 1, 10, 100, 200, 500]:
    td = 300
    x = 1.0/math.tanh(td/(2*tc))
    # 假设Δδ₀=0.05
    ddv0 = 0.05
    om = 3*BETA**2*ddv0**2/(16*x*GAP)
    dv = (1-om)/BETA if om < 1 else 0
    print(f"  {tc:>10.2f} {td:>8.0f} {x:>10.4f} {dv:>12.6f} {dv/DELTA_C:>10.4f}")

print("\n→ 任何Tc都能反推出δ_v≈1/β。这不是预言，是定义。")

# ============================================================
# Part 2: 前向计算——假设δ_intrinsic=0
# ============================================================
print("\n" + "=" * 100)
print("Part 2: 前向计算（δ_intrinsic=0, 只有压力δ_pressure）")
print("=" * 100)

print("""
前向计算:
  Δδ₀ = 从材料结构独立计算（晶格常数、原子质量、Debye温度）
  δ_v = δ_pressure = P/(3B)（压力诱导，常压=0）
  Tc_calc = θ_D/(2·arccoth(x)), x = 3β²Δδ₀²/(16(1-βδ_v)GAP)

问题: 常压材料δ_pressure=0, δ_intrinsic无法独立计算
      → 只能假设δ_intrinsic=0, 看前向Tc与实验差多少
""")

print(f"{'材料':<18} {'类别':<10} {'Tc_exp':>7} {'θ_D':>6} {'Δδ₀':>8} {'δ_press':>8} {'x':>8} {'Tc_calc':>9} {'比值':>7}")
print("-" * 90)

fwd_results = []
for row in rows[:60]:  # 前60个材料
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc_exp = float(tc_match.group(1))
    comp = parse_formula(formula)
    if not comp: continue

    theta_D, M_cell, L, z_inter, edges_intra, l_intra, B, P_GPa, f = \
        estimate_params(formula, cat, tc_exp, condition)

    dp = P_GPa / (3 * B) if B > 0 else 0
    dv_pressure = min(dp, 0.9 / BETA)

    di = ddv_inter(M_cell, L, theta_D, z_inter, f)
    dn = ddv_intra(edges_intra, l_intra, theta_D, f) if edges_intra else 0
    ddv0 = math.sqrt(di**2 + dn**2)

    # 前向计算: δ_v = δ_pressure only (δ_intrinsic=0)
    x, tc_calc = calc_Tc_forward(ddv0, dv_pressure, theta_D)
    ratio = tc_calc / tc_exp if tc_calc > 0 and tc_exp > 0 else 0

    fwd_results.append((formula, cat, tc_exp, theta_D, ddv0, dv_pressure, x, tc_calc, ratio))

    short = formula[:16]
    cs = cat[:8]
    tc_str2 = f"{tc_calc:.1f}" if tc_calc > 0 else "0"
    r_str = f"{ratio:.3f}" if ratio > 0 else "—"
    print(f"{short:<18} {cs:<10} {tc_exp:>7.1f} {theta_D:>6.0f} {ddv0:>8.4f} {dv_pressure:>8.5f} {x:>8.3f} {tc_str2:>9} {r_str:>7}")

# 统计
valid = [r for r in fwd_results if r[7] > 0]
print(f"\n前向计算统计 (δ_intrinsic=0):")
print(f"  有非零Tc的材料: {len(valid)}/{len(fwd_results)}")
if valid:
    ratios = [r[8] for r in valid]
    print(f"  Tc_calc/Tc_exp比值范围: {min(ratios):.4f} - {max(ratios):.4f}")
    print(f"  中位数比值: {np.median(ratios):.4f}")
    within_2x = sum(1 for r in ratios if 0.5 < r < 2.0)
    print(f"  在2倍范围内: {within_2x}/{len(valid)} = {within_2x/len(valid)*100:.1f}%")

# ============================================================
# Part 3: 前向计算——假设δ_intrinsic=1/β
# ============================================================
print("\n" + "=" * 100)
print("Part 3: 前向计算（假设δ_intrinsic=1/β, 即Fermi面临界）")
print("=" * 100)

print("""
如果假设所有超导体的δ_intrinsic=1/β（Fermi面拓扑临界）:
  δ_v = 1/β + δ_pressure
  但 βδ_v > 1 → Tc=0 (公式发散)!

这不对。需要δ_intrinsic略小于1/β。
试试δ_intrinsic = 0.95/β:
""")

for delta_intr_frac in [0.90, 0.95, 0.98, 0.99]:
    delta_intr = delta_intr_frac * DELTA_C
    print(f"\n  δ_intrinsic = {delta_intr_frac}×(1/β) = {delta_intr:.6f}:")
    print(f"  {'材料':<18} {'Tc_exp':>7} {'Δδ₀':>8} {'δ_v':>8} {'x':>8} {'Tc_calc':>9} {'比值':>7}")
    print("  " + "-" * 70)

    count_ok = 0; count_total = 0
    for row in rows[:30]:
        cat = row[0]; formula = row[1]; tc_str = row[3]
        condition = row[7] if len(row) > 7 else ''
        tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
        if not tc_match: continue
        tc_exp = float(tc_match.group(1))
        comp = parse_formula(formula)
        if not comp: continue

        theta_D, M_cell, L, z_inter, edges_intra, l_intra, B, P_GPa, f = \
            estimate_params(formula, cat, tc_exp, condition)
        dp = P_GPa / (3 * B) if B > 0 else 0
        dv_pressure = min(dp, 0.9 / BETA)
        di = ddv_inter(M_cell, L, theta_D, z_inter, f)
        dn = ddv_intra(edges_intra, l_intra, theta_D, f) if edges_intra else 0
        ddv0 = math.sqrt(di**2 + dn**2)

        dv = delta_intr + dv_pressure
        x, tc_calc = calc_Tc_forward(ddv0, dv, theta_D)
        ratio = tc_calc / tc_exp if tc_calc > 0 and tc_exp > 0 else 0
        count_total += 1
        if 0.5 < ratio < 2.0:
            count_ok += 1

        if count_total <= 15:
            short = formula[:16]
            tc_s = f"{tc_calc:.1f}" if tc_calc > 0 else "0"
            r_s = f"{ratio:.3f}" if ratio > 0 else "—"
            print(f"  {short:<18} {tc_exp:>7.1f} {ddv0:>8.4f} {dv:>8.5f} {x:>8.3f} {tc_s:>9} {r_s:>7}")

    print(f"\n  2倍范围内: {count_ok}/{count_total} = {count_ok/count_total*100:.1f}%")

# ============================================================
# Part 4: 反推δ_v的分布——检验"普适性"是否真实
# ============================================================
print("\n" + "=" * 100)
print("Part 4: 反推δ_v的分布——'普适性'检验")
print("=" * 100)

print("""
如果δ_v真的普适(≈1/β)，反推值应该集中在窄范围。
如果反推值分散，说明"普适性"是统计假象。
""")

rev_deltas = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc_exp = float(tc_match.group(1))
    comp = parse_formula(formula)
    if not comp: continue

    theta_D, M_cell, L, z_inter, edges_intra, l_intra, B, P_GPa, f = \
        estimate_params(formula, cat, tc_exp, condition)
    dp = P_GPa / (3 * B) if B > 0 else 0
    di = ddv_inter(M_cell, L, theta_D, z_inter, f)
    dn = ddv_intra(edges_intra, l_intra, theta_D, f) if edges_intra else 0
    ddv0 = math.sqrt(di**2 + dn**2)

    dv = rev_delta(ddv0, theta_D, tc_exp, dp)
    if dv is not None and dv > 0:
        rev_deltas.append((formula, cat, tc_exp, ddv0, dv, dv/DELTA_C))

print(f"反推δ_v统计 ({len(rev_deltas)}个材料):")
dvs = [r[4] for r in rev_deltas]
ratios = [r[5] for r in rev_deltas]
print(f"  均值: {np.mean(dvs):.6f} (1/β={DELTA_C:.6f})")
print(f"  标准差: {np.std(dvs):.6f}")
print(f"  最小值: {np.min(dvs):.6f} (比值{np.min(ratios):.4f})")
print(f"  最大值: {np.max(dvs):.6f} (比值{np.max(ratios):.4f})")
print(f"  中位数: {np.median(dvs):.6f}")
print(f"  变异系数(CV): {np.std(dvs)/np.mean(dvs)*100:.1f}%")

# 按Tc范围分组
print(f"\n按Tc范围分组:")
for tc_lo, tc_hi in [(0, 1), (1, 10), (10, 50), (50, 200), (200, 500)]:
    subset = [r for r in rev_deltas if tc_lo <= r[2] < tc_hi]
    if subset:
        sub_dvs = [r[4] for r in subset]
        sub_ratios = [r[5] for r in subset]
        print(f"  Tc={tc_lo:3d}-{tc_hi:3d}K: n={len(subset):3d}, δ_v均值={np.mean(sub_dvs):.5f}, "
              f"比值={np.mean(sub_ratios):.3f}±{np.std(sub_ratios):.3f}")

# ============================================================
# Part 5: 关键检验——Δδ₀能否独立区分超导/非超导?
# ============================================================
print("\n" + "=" * 100)
print("Part 5: Δδ₀能否独立区分超导/非超导?")
print("=" * 100)

print("""
如果Δδ₀是物理预言(不是反推), 它应该能区分超导和非超导。
检查: 超导体的Δδ₀是否系统性地大于非超导体?
""")

# 非超导体
non_sc = [
    ("Cu", "元素", 0, "FCC"), ("Ag", "元素", 0, "FCC"), ("Au", "元素", 0, "FCC"),
    ("Si", "元素", 0, "DIA"), ("Ge", "元素", 0, "DIA"),
    ("Na", "元素", 0, "BCC"), ("K", "元素", 0, "BCC"),
    ("Fe", "元素", 0, "BCC"), ("Co", "元素", 0, "HCP"), ("Ni", "元素", 0, "FCC"),
]

print(f"{'材料':<12} {'超导?':>5} {'Tc':>7} {'θ_D':>6} {'Δδ₀':>10} {'x(δv=0)':>10} {'Tc_calc':>9}")
print("-" * 65)

for name, cat, tc_exp, struct in non_sc:
    comp = parse_formula(name)
    theta_D = get_debye(comp)
    M = get_mass(comp)
    r = get_radius(comp)
    L = 2 * r
    z = 12 if struct in ["FCC", "HCP"] else 8
    f = 0.5
    ddv0 = ddv_inter(M, L, theta_D, z, f)
    x, tc_c = calc_Tc_forward(ddv0, 0, theta_D)
    tc_s = f"{tc_c:.2f}" if tc_c > 0 else "0"
    print(f"{name:<12} {'否':>5} {tc_exp:>7.1f} {theta_D:>6.0f} {ddv0:>10.6f} {x:>10.4f} {tc_s:>9}")

print()
# 超导体(前10个)
count = 0
for row in rows:
    if count >= 10: break
    cat = row[0]; formula = row[1]; tc_str = row[3]
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc_exp = float(tc_match.group(1))
    comp = parse_formula(formula)
    if not comp: continue
    theta_D, M_cell, L, z_inter, edges_intra, l_intra, B, P_GPa, f = \
        estimate_params(formula, cat, tc_exp, row[7] if len(row)>7 else '')
    di = ddv_inter(M_cell, L, theta_D, z_inter, f)
    dn = ddv_intra(edges_intra, l_intra, theta_D, f) if edges_intra else 0
    ddv0 = math.sqrt(di**2 + dn**2)
    x, tc_c = calc_Tc_forward(ddv0, 0, theta_D)
    tc_s = f"{tc_c:.2f}" if tc_c > 0 else "0"
    print(f"{formula[:12]:<12} {'是':>5} {tc_exp:>7.1f} {theta_D:>6.0f} {ddv0:>10.6f} {x:>10.4f} {tc_s:>9}")
    count += 1

# ============================================================
# Part 6: 诚实总结
# ============================================================
print("\n" + "=" * 100)
print("Part 6: 诚实总结")
print("=" * 100)

print(f"""
问题诊断:

1. "100%成功率"是数学假象:
   - 反推法: 从实验Tc反推δ_v, 再检查δ_v范围
   - 给定任何Tc>0, 都能反推δ_v≈1/β
   - 判定范围(0.3-3.0倍1/β)极宽, 几乎所有材料都"通过"
   - tc_calc=tc_exp: 计算Tc直接赋值为实验Tc

2. 前向计算无法复现实验Tc:
   - δ_intrinsic无法独立计算(需DFT Berry曲率)
   - 假设δ_intrinsic=0: 大部分材料Tc_calc=0
   - 假设δ_intrinsic=0.95/β: Tc对δ_intrinsic极度敏感
     (δ_intrinsic差1% → Tc差数倍)

3. 两套Δδ₀数据:
   - 代码中Δδ₀从材料参数计算(晶格常数、原子质量等)
   - 文档中Δδ₀是直接给出的数值
   - 两者可能不一致(需逐材料核对)

4. δ_v"普适性"的变异系数:
   - CV = {np.std(dvs)/np.mean(dvs)*100:.1f}%
   - 不是窄分布, 有相当分散
   - 不同Tc范围的δ_v比值有系统偏差

核心问题:
  CQM超导理论目前是**拟合框架**, 不是**预言框架**。
  - 已知: Δδ₀从材料结构计算(这是独立的)
  - 未知: δ_intrinsic从Fermi面计算(这是缺失的环节)
  - 反推δ_v = 把未知量当调节参数, 拟合实验Tc

  要成为预言框架, 必须:
  1. 从DFT计算Berry曲率 → δ_intrinsic
  2. 从DFT声子谱 → f (替代Debye近似)
  3. 正向计算Tc, 与实验比较
  4. 不用任何反推或拟合参数
""")