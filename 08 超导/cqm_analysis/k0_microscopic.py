"""
K_0^cat的微观推导：从BCS类比建立K_0^cat与λ_ep的关系

思路:
  CQM: Tc² = Δδ₀²·K_eff·θ_D/(9ln2/8)
  BCS: Tc = 1.14·θ_D·exp(-1.04(1+λ)/(λ-μ*(1+0.62λ)))

  如果两者等价，K_0^cat类比BCS的λ_ep-μ*

步骤:
  1. 从BCS公式反推λ_ep（μ*=0.1）
  2. 计算K_0^cat（去除G和θ_D依赖）
  3. 检查K_0^cat与λ_ep的关系
"""

import csv, re, math
import numpy as np
from collections import defaultdict
from scipy.optimize import brentq

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

ATOM_DB = {
    'H': (1.008, 0, 0.46, 0, 1), 'He': (4.003, 0, 0.31, 0, 2),
    'Li': (6.94, 344, 1.52, 11, 1), 'Be': (9.01, 1440, 1.12, 130, 2),
    'B': (10.81, 1480, 0.87, 185, 3), 'C': (12.01, 2230, 0.77, 338, 4),
    'N': (14.01, 0, 0.75, 0, 5), 'O': (16.00, 0, 0.73, 0, 6),
    'F': (19.00, 0, 0.72, 0, 7), 'Ne': (20.18, 0, 0.71, 0, 8),
    'Na': (22.99, 158, 1.86, 7, 1), 'Mg': (24.31, 400, 1.60, 35, 2),
    'Al': (26.98, 428, 1.43, 76, 3), 'Si': (28.09, 645, 1.18, 100, 4),
    'P': (30.97, 0, 1.10, 0, 5), 'S': (32.06, 0, 1.05, 0, 6),
    'Cl': (35.45, 0, 1.02, 0, 7), 'K': (39.10, 91, 2.27, 3, 1),
    'Ca': (40.08, 230, 1.97, 15, 2), 'Sc': (44.96, 360, 1.62, 44, 3),
    'Ti': (47.87, 420, 1.47, 110, 4), 'V': (50.94, 383, 1.34, 162, 5),
    'Cr': (52.00, 435, 1.28, 160, 6), 'Mn': (54.94, 410, 1.27, 120, 7),
    'Fe': (55.85, 470, 1.26, 170, 8), 'Co': (58.93, 445, 1.25, 180, 9),
    'Ni': (58.69, 450, 1.24, 180, 10), 'Cu': (63.55, 343, 1.28, 140, 11),
    'Zn': (65.38, 327, 1.34, 70, 12), 'Ga': (69.72, 240, 1.35, 40, 3),
    'Ge': (72.63, 374, 1.22, 75, 4), 'As': (74.92, 0, 1.21, 0, 5),
    'Se': (78.97, 0, 1.20, 0, 6), 'Br': (79.90, 0, 1.20, 0, 7),
    'Rb': (85.47, 56, 2.48, 2, 1), 'Sr': (87.62, 147, 2.15, 12, 2),
    'Y': (88.91, 280, 1.80, 37, 3), 'Zr': (91.22, 291, 1.60, 95, 4),
    'Nb': (92.91, 275, 1.46, 170, 5), 'Mo': (95.96, 425, 1.39, 230, 6),
    'Tc': (98.00, 0, 1.36, 0, 7), 'Ru': (101.07, 0, 1.34, 220, 8),
    'Rh': (102.91, 0, 1.34, 150, 9), 'Pd': (106.42, 274, 1.37, 180, 10),
    'Ag': (107.87, 215, 1.44, 100, 11), 'Cd': (112.41, 209, 1.49, 42, 12),
    'In': (114.82, 108, 1.62, 11, 3), 'Sn': (118.71, 200, 1.58, 50, 4),
    'Sb': (121.76, 0, 1.61, 0, 5), 'Te': (127.60, 0, 1.60, 0, 6),
    'I': (126.90, 0, 1.63, 0, 7), 'Cs': (132.91, 38, 2.65, 2, 1),
    'Ba': (137.33, 110, 2.22, 9, 2), 'La': (138.91, 142, 1.87, 24, 3),
    'Ce': (140.12, 0, 1.82, 22, 4), 'Pr': (140.91, 0, 1.82, 21, 3),
    'Nd': (144.24, 0, 1.82, 20, 4), 'Sm': (150.36, 0, 1.81, 18, 6),
    'Eu': (151.96, 0, 1.81, 8, 7), 'Gd': (157.25, 0, 1.80, 25, 8),
    'Tb': (158.93, 0, 1.79, 25, 9), 'Dy': (162.50, 0, 1.79, 25, 10),
    'Ho': (164.93, 0, 1.78, 26, 11), 'Er': (167.26, 0, 1.78, 26, 12),
    'Tm': (168.93, 0, 1.77, 28, 13), 'Yb': (173.05, 0, 1.77, 10, 14),
    'Lu': (174.97, 0, 1.77, 30, 15), 'Hf': (178.49, 252, 1.59, 110, 4),
    'Ta': (180.95, 240, 1.46, 200, 5), 'W': (183.84, 400, 1.39, 310, 6),
    'Re': (186.21, 430, 1.37, 370, 7), 'Os': (190.23, 500, 1.35, 400, 8),
    'Ir': (192.22, 420, 1.36, 355, 9), 'Pt': (195.08, 240, 1.39, 230, 10),
    'Au': (196.97, 170, 1.44, 180, 11), 'Hg': (200.59, 0, 1.51, 25, 12),
    'Tl': (204.38, 78, 1.70, 8, 3), 'Pb': (207.20, 105, 1.75, 23, 4),
    'Bi': (208.98, 0, 1.70, 0, 5), 'Th': (232.04, 163, 1.80, 54, 4),
    'Pa': (231.04, 0, 1.80, 0, 5), 'U': (238.03, 207, 1.75, 100, 6),
}

def parse_formula(f):
    f = re.sub(r'[\(（].*?[\)）]', '', f.strip())
    return {e: (float(c) if c else 1.0) for e,c in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f) if e in ATOM_DB}

def get_mass(c): return sum(ATOM_DB[e][0]*n for e,n in c.items())
def get_debye(c):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0]*n) for e,n in c.items() if ATOM_DB[e][1]>0]
    return sum(d*w for d,w in ws)/sum(w for _,w in ws) if ws else 300
def get_radius(c):
    rs = [ATOM_DB[e][2] for e in c if ATOM_DB[e][2]>0]
    return np.mean(rs) if rs else 1.5
def get_bulk(c):
    bs = [ATOM_DB[e][3] for e in c if ATOM_DB[e][3]>0]
    return np.mean(bs) if bs else 50
def get_valence(c):
    vs = [ATOM_DB[e][4] for e in c if ATOM_DB[e][4]>0]
    return np.mean(vs) if vs else 4

def ddv_inter(M, L, tD, z, f=0.5):
    L_m = L*1e-10; w = tD*KB/HBAR; s = z*2.0/(M*AMU)
    return math.sqrt(max((C2/L_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def ddv_intra(edges, l, tD, f=0.5):
    l_m = l*1e-10; w = tD*KB/HBAR
    s = sum((1.0/(mi*AMU)+1.0/(mj*AMU)) for mi,mj in edges)
    return math.sqrt(max((C2/l_m**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def estimate_params(formula, cat, condition):
    comp = parse_formula(formula)
    if not comp: return None
    n_atoms = sum(comp.values())
    M = get_mass(comp); r = get_radius(comp); tD = get_debye(comp); B = get_bulk(comp)
    Z_val = get_valence(comp)
    P = 0
    if '高压' in condition or 'GPa' in condition:
        pm = re.search(r'~?(\d+)GPa', condition)
        P = int(pm.group(1)) if pm else 50
    L = 2*r; l_intra = 2*r; z = 6; edges = []; f = 0.5
    if '元素' in cat:
        tD = ATOM_DB.get(list(comp.keys())[0], (0,300,1.5,50,4))[1] or tD
        if tD < 50: tD = 300
        z = 12; f = 0.5
        if '高压' in cat: B = max(get_bulk(comp),50)*3; P = max(P,100)
    elif 'A15' in cat: tD = max(tD,400); z = 8; L = 2*r*0.9; f = 0.4
    elif '氢化物' in cat:
        tD = max(tD,1500); B = max(B,200); P = max(P,150); z = 8; L = 2.0; l_intra = 1.7
        n_h = comp.get('H',0); n_m = n_atoms - n_h
        if n_h > 0 and n_m > 0:
            m_m = (M - n_h*1.008)/n_m; edges = [(m_m,1.008)]*int(min(n_h,4))
        f = 0.5
    elif '铜氧' in cat:
        tD = max(tD,400); z = 6; L = 3.8; l_intra = 1.9
        if 'Cu' in comp and 'O' in comp: edges = [(63.55,16.0)]*2
        f = 0.4
    elif '铁基' in cat:
        tD = max(tD,350); z = 6; L = 3.5; l_intra = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges = [(55.85,74.92)]*2
            elif 'Se' in comp: edges = [(55.85,78.97)]*2
        f = 0.4
    elif '有机' in cat: tD = max(tD,100); z = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
    elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
    elif '合金' in cat: tD = max(tD,200); z = 12; f = 0.5
    else: tD = max(tD,200); z = 8; f = 0.5
    return tD, M, L, z, edges, l_intra, B, P, f, Z_val

def rev_lambda_ep(tc, theta_D, mu_star=0.1):
    """从BCS反推λ_ep: Tc = θ_D/1.2·exp(-1.04(1+λ)/(λ-μ*(1+0.62λ)))"""
    if tc <= 0 or theta_D <= 0: return None
    ratio = 1.2 * tc / theta_D
    if ratio >= 1: return None
    exponent = -math.log(ratio)  # 1.04(1+λ)/(λ-μ*(1+0.62λ))
    # 1.04(1+λ) = exponent·(λ - μ*(1+0.62λ))
    # 1.04 + 1.04λ = exponent·λ - exponent·μ* - exponent·μ*·0.62·λ
    # 1.04 + exponent·μ* = λ·(exponent - 1.04 + exponent·μ*·0.62)
    denom = exponent - 1.04 + exponent * mu_star * 0.62
    if abs(denom) < 1e-10: return None
    lam = (1.04 + exponent * mu_star) / denom
    return lam if lam > 0 else None

def calc_N0_free_electron(Z_val, V_cell_ang3):
    """自由电子模型计算N(0) (states/eV/cell)"""
    # n = Z/V (电子密度, /Å³)
    n = Z_val / V_cell_ang3  # /Å³
    n_m3 = n * 1e30  # /m³
    # k_F = (3π²n)^(1/3)
    kF = (3 * math.pi**2 * n_m3)**(1/3)
    # E_F = ℏ²k_F²/(2m_e) in eV
    m_e = 9.109e-31
    EF_J = HBAR**2 * kF**2 / (2 * m_e)
    EF_eV = EF_J / 1.602e-19
    # N(0) = 3n/(2EF) in states/J/m³ → states/eV/cell
    N0_per_J_m3 = 3 * n_m3 / (2 * EF_J)
    N0_per_eV_m3 = N0_per_J_m3 * 1.602e-19
    V_cell_m3 = V_cell_ang3 * 1e-30
    N0_per_eV_cell = N0_per_eV_m3 * V_cell_m3
    return N0_per_eV_cell, EF_eV

# 加载
with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
    reader = csv.reader(fh); header = next(reader); rows = list(reader)

all_data = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc = float(tc_match.group(1))
    params = estimate_params(formula, cat, condition)
    if not params: continue
    tD, M, L, z, edges, l_intra, B, P, f, Z_val = params
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)

    # G和K_eff
    G2 = ddv0**2 * tD * 4 * KB / (C2 * 3 * HBAR**2)
    G = math.sqrt(G2)
    k_eff = tc**2 * 1.125 * LN2 / (ddv0**2 * tD)

    # K_0 (去除G^a·θ_D^b依赖, a=-0.77, b=1.13)
    a_ke, b_ke = -0.769, 1.132
    K0 = k_eff / (G**a_ke * tD**b_ke)

    # BCS反推λ_ep
    lam_ep = rev_lambda_ep(tc, tD, mu_star=0.1)

    # 自由电子N(0)
    V_cell = L**3  # 简化: 立方晶胞
    N0, EF = calc_N0_free_electron(Z_val, V_cell)

    # 近似λ_ep从材料参数: λ ~ N(0)·B/(M·ω_D²)
    omega_D = tD * KB / HBAR
    # λ_ep_approx ~ N(0)·<I²>/(M·ω²), <I²>~B·V/某个常数
    # 简化: λ_ep_approx = N0 * B / (M * omega_D²) * scale
    # 量纲不对，用无量纲化
    lam_approx = N0 * B / (M * omega_D**2) * 1e40  # 经验缩放

    all_data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'ddv0': ddv0, 'G': G, 'k_eff': k_eff, 'K0': K0,
        'lam_ep': lam_ep, 'N0': N0, 'EF': EF, 'B': B, 'M': M,
        'Z_val': Z_val, 'V_cell': V_cell, 'lam_approx': lam_approx
    })

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. BCS反推λ_ep统计
# ============================================================
print(f"\n{'='*90}")
print("1. BCS反推λ_ep (μ*=0.1)")
print("=" * 90)

valid = [d for d in all_data if d['lam_ep'] is not None and d['lam_ep'] > 0]
lams = np.array([d['lam_ep'] for d in valid])
print(f"有效材料: {len(valid)}/{len(all_data)}")
print(f"λ_ep: 均值={np.mean(lams):.3f}, 中位数={np.median(lams):.3f}")
print(f"  范围: [{np.min(lams):.3f}, {np.max(lams):.3f}]")

# 按类别
print("\n按类别:")
cat_data = defaultdict(list)
for d in valid: cat_data[d['cat']].append(d)

for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 3: continue
    ls = np.array([d['lam_ep'] for d in cd])
    print(f"  {cat:24s}: n={len(cd):3d}, λ={np.mean(ls):.3f}±{np.std(ls):.3f}")

# ============================================================
# 2. K_0与λ_ep的关系
# ============================================================
print(f"\n{'='*90}")
print("2. K_0与λ_ep的关系")
print("=" * 90)

K0s = np.array([d['K0'] for d in valid])
lams = np.array([d['lam_ep'] for d in valid])

# 相关性
corr = np.corrcoef(np.log(K0s), np.log(lams))[0,1]
print(f"corr(ln K_0, ln λ_ep) = {corr:.3f}")

# 拟合 K_0 = c · λ_ep^a
X = np.vstack([np.log(lams), np.ones(len(lams))]).T
y = np.log(K0s)
from numpy.linalg import lstsq
a_fit, c_fit = lstsq(X, y, rcond=None)[0]
print(f"K_0 = {np.exp(c_fit):.4e} · λ_ep^{a_fit:.3f}")

# R²
pred = a_fit * np.log(lams) + c_fit
r2 = 1 - np.sum((y - pred)**2) / np.sum((y - np.mean(y))**2)
print(f"R² = {r2:.3f}")

# ============================================================
# 3. K_0与其他BCS参数的关系
# ============================================================
print(f"\n{'='*90}")
print("3. K_0与BCS参数关系")
print("=" * 90)

# λ_ep - μ*
lam_minus_mu = lams - 0.1
corr2 = np.corrcoef(np.log(K0s), np.log(lam_minus_mu))[0,1]
print(f"corr(ln K_0, ln(λ_ep - μ*)) = {corr2:.3f}")

# N(0)
N0s = np.array([d['N0'] for d in valid])
corr_N0 = np.corrcoef(np.log(K0s), np.log(N0s))[0,1]
print(f"corr(ln K_0, ln N(0)) = {corr_N0:.3f}")

# E_F
EFs = np.array([d['EF'] for d in valid])
corr_EF = np.corrcoef(np.log(K0s), np.log(EFs))[0,1]
print(f"corr(ln K_0, ln E_F) = {corr_EF:.3f}")

# B (体模量)
Bs = np.array([d['B'] for d in valid])
corr_B = np.corrcoef(np.log(K0s), np.log(Bs))[0,1]
print(f"corr(ln K_0, ln B) = {corr_B:.3f}")

# 多变量回归: ln K_0 = a·ln(λ_ep) + b·ln(N0) + c·ln(B) + d
print("\n多变量回归:")
X_multi = np.array([[np.log(d['lam_ep']), np.log(d['N0']), np.log(d['B']), 1] for d in valid])
y_multi = np.array([np.log(d['K0']) for d in valid])
coef_multi, _, _, _ = lstsq(X_multi, y_multi, rcond=None)
pred_multi = X_multi @ coef_multi
r2_multi = 1 - np.sum((y_multi - pred_multi)**2) / np.sum((y_multi - np.mean(y_multi))**2)
print(f"  ln K_0 = {coef_multi[0]:.3f}·ln(λ) + {coef_multi[1]:.3f}·ln(N0) + {coef_multi[2]:.3f}·ln(B) + {coef_multi[3]:.3f}")
print(f"  R² = {r2_multi:.3f}")

# ============================================================
# 4. 从材料参数近似计算λ_ep
# ============================================================
print(f"\n{'='*90}")
print("4. 从材料参数近似计算λ_ep")
print("=" * 90)
print("""
BCS: λ_ep = N(0)·<I²>/(M·ω²)
  N(0): Fermi面态密度 (自由电子近似)
  <I²>: 电子-声子矩阵元平方 (Hopfield参数)
  M: 原子质量
  ω: 声子频率

Hopfield近似: <I²> ~ 2·B·r_s/3
  B: 体模量
  r_s: Wigner-Seitz半径
""")

# 计算近似λ_ep
for d in valid:
    # Wigner-Seitz半径
    r_s_ang = (3 * d['V_cell'] / (4 * math.pi * d['Z_val']))**(1/3)
    # <I²> ~ B·r_s (量纲近似)
    I2 = d['B'] * r_s_ang  # GPa·Å
    # ω_D
    omega_D = d['tD'] * KB / HBAR
    # λ_ep近似 (需要量纲匹配，用经验缩放)
    d['lam_approx2'] = d['N0'] * I2 / (d['M'] * omega_D**2) * 1e35

lam_approx2 = np.array([d['lam_approx2'] for d in valid])
corr_approx = np.corrcoef(np.log(lam_approx2), np.log(lams))[0,1]
print(f"corr(ln λ_approx, ln λ_ep(BCS反推)) = {corr_approx:.3f}")

# 拟合 λ_ep = c · λ_approx^a
X_la = np.vstack([np.log(lam_approx2), np.ones(len(lam_approx2))]).T
y_la = np.log(lams)
a_la, c_la = lstsq(X_la, y_la, rcond=None)[0]
print(f"λ_ep(反推) = {np.exp(c_la):.4e} · λ_approx^{a_la:.3f}")
pred_la = a_la * np.log(lam_approx2) + c_la
r2_la = 1 - np.sum((y_la - pred_la)**2) / np.sum((y_la - np.mean(y_la))**2)
print(f"R² = {r2_la:.3f}")

# ============================================================
# 5. 完整第一性预测: 材料参数 → λ_ep → K_0 → Tc
# ============================================================
print(f"\n{'='*90}")
print("5. 完整第一性预测链条验证")
print("=" * 90)

# LOOCV: 从材料参数预测λ_ep → K_0 → Tc
all_preds = []
all_exps = []
for i, d_test in enumerate(valid):
    cat = d_test['cat']
    train = [d for j,d in enumerate(valid) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(valid) if j != i]

    # Step 1: 从训练集学习 λ_ep vs λ_approx 关系
    x_tr = np.log(np.array([d['lam_approx2'] for d in train]))
    y_tr = np.log(np.array([d['lam_ep'] for d in train]))
    A_tr = np.vstack([x_tr, np.ones(len(x_tr))]).T
    a_tr, c_tr = lstsq(A_tr, y_tr, rcond=None)[0]

    # Step 2: 预测λ_ep
    lam_pred = np.exp(c_tr) * d_test['lam_approx2']**a_tr

    # Step 3: 从训练集学习 K_0 vs λ_ep 关系
    x_k = np.log(np.array([d['lam_ep'] for d in train]))
    y_k = np.log(np.array([d['K0'] for d in train]))
    A_k = np.vstack([x_k, np.ones(len(x_k))]).T
    a_k, c_k = lstsq(A_k, y_k, rcond=None)[0]

    # Step 4: 预测K_0
    K0_pred = np.exp(c_k) * lam_pred**a_k

    # Step 5: 计算K_eff
    k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132

    # Step 6: 计算Tc
    tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))

    all_preds.append(tc_pred)
    all_exps.append(d_test['tc'])

errs = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
print(f"完整链条LOOCV: {len(errs)}个材料")
print(f"  中位误差: {np.median(errs)*100:.0f}%")
print(f"  2倍内: {np.sum(errs<1)/len(errs)*100:.0f}%")
print(f"  5倍内: {np.sum(errs<4)/len(errs)*100:.0f}%")

# 对比: 直接用类别K_0
print(f"\n对比: 直接用类别K_0校准:")
all_preds2 = []
all_exps2 = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(all_data) if j != i]
    k0_train = np.median([d['K0'] for d in train])
    k_eff_pred = k0_train * d_test['G']**(-0.769) * d_test['tD']**1.132
    tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))
    all_preds2.append(tc_pred)
    all_exps2.append(d_test['tc'])

errs2 = np.abs(np.array(all_preds2) - np.array(all_exps2)) / np.array(all_exps2)
print(f"  中位误差: {np.median(errs2)*100:.0f}%, 2倍内: {np.sum(errs2<1)/len(errs2)*100:.0f}%, 5倍内: {np.sum(errs2<4)/len(errs2)*100:.0f}%")

# ============================================================
# 6. 总结
# ============================================================
print(f"\n{'='*90}")
print("6. 总结")
print("=" * 90)
print(f"""
K_0^cat的微观推导:

1. BCS反推λ_ep: {len(valid)}个材料, λ_ep范围[{np.min(lams):.2f}, {np.max(lams):.2f}]
2. K_0 vs λ_ep: corr(ln K_0, ln λ) = {corr:.3f}, R² = {r2:.3f}
   K_0 = {np.exp(c_fit):.4e} · λ_ep^{a_fit:.3f}
3. λ_ep近似: corr(λ_approx, λ_ep) = {corr_approx:.3f}, R² = {r2_la:.3f}
4. 完整链条LOOCV: 中位误差{np.median(errs)*100:.0f}%, 2倍内{np.sum(errs<1)/len(errs)*100:.0f}%
5. 对比(类别K_0): 中位误差{np.median(errs2)*100:.0f}%, 2倍内{np.sum(errs2<1)/len(errs2)*100:.0f}%

结论:
  - K_0与λ_ep弱相关(R²={r2:.3f}), 不是简单的BCS类比
  - λ_ep近似与反推弱相关(R²={r2_la:.3f}), 自由电子+Hopfield近似不够
  - 完整链条({np.median(errs)*100:.0f}%误差)与类别校准({np.median(errs2)*100:.0f}%误差)接近
  - K_0的微观推导需要更精确的DFT计算

链条状态:
  ✅ 材料→Δδ₀→G (第一性)
  ⚠️ G,θ_D→K_eff (K_0需校准)
  ⚠️ 材料→λ_ep近似 (自由电子+Hopfield, R²={r2_la:.3f})
  ⚠️ λ_ep→K_0 (R²={r2:.3f})
  ✅ K_eff→Tc (第一性)

要实现完全第一性, 需要:
  1. DFT精确计算N(0) (非自由电子近似)
  2. DFT精确计算<M_ep²> (非Hopfield近似)
  3. 建立K_0 = f(N(0), M_ep, ω(q))的严格关系
""")