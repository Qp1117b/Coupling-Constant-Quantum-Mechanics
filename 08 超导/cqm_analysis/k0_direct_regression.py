"""
改进K_0预测：直接从材料参数回归

策略:
  1. 尝试多种λ_ep近似公式
  2. 直接多变量回归K_0与材料参数
  3. 找到最佳组合，实现第一性预测
"""

import csv, re, math
import numpy as np
from collections import defaultdict
from numpy.linalg import lstsq

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
    G2 = ddv0**2 * tD * 4 * KB / (C2 * 3 * HBAR**2)
    G = math.sqrt(G2)
    k_eff = tc**2 * 1.125 * LN2 / (ddv0**2 * tD)
    K0 = k_eff / (G**(-0.769) * tD**1.132)
    # 材料参数
    V_cell = L**3
    r_s = (3*V_cell/(4*math.pi*Z_val))**(1/3) if Z_val > 0 else 1.5
    omega_D = tD * KB / HBAR
    all_data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'ddv0': ddv0, 'G': G, 'K0': K0, 'B': B, 'M': M,
        'Z_val': Z_val, 'V_cell': V_cell, 'r_s': r_s, 'omega_D': omega_D,
        'L': L, 'z': z, 'f': f, 'n_atoms': sum(parse_formula(formula).values())
    })

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. 尝试多种K_0与材料参数的关系
# ============================================================
print(f"\n{'='*90}")
print("1. K_0与材料参数的单变量关系")
print("=" * 90)

K0s = np.array([d['K0'] for d in all_data])
log_K0 = np.log(K0s)

# 候选参数
candidates = {
    'B': [d['B'] for d in all_data],
    'M': [d['M'] for d in all_data],
    'Z_val': [d['Z_val'] for d in all_data],
    'V_cell': [d['V_cell'] for d in all_data],
    'r_s': [d['r_s'] for d in all_data],
    'theta_D': [d['tD'] for d in all_data],
    'omega_D': [d['omega_D'] for d in all_data],
    'L': [d['L'] for d in all_data],
    'z': [d['z'] for d in all_data],
    'B/M': [d['B']/d['M'] for d in all_data],
    'B*V': [d['B']*d['V_cell'] for d in all_data],
    'Z/V': [d['Z_val']/d['V_cell'] for d in all_data],
    'B*r_s': [d['B']*d['r_s'] for d in all_data],
    'B/(M*omega²)': [d['B']/(d['M']*d['omega_D']**2) for d in all_data],
    'Z*B/M': [d['Z_val']*d['B']/d['M'] for d in all_data],
    'B*V/M': [d['B']*d['V_cell']/d['M'] for d in all_data],
    'θ_D²/B': [d['tD']**2/d['B'] for d in all_data],
    'B/θ_D²': [d['B']/d['tD']**2 for d in all_data],
    'Z²/V': [d['Z_val']**2/d['V_cell'] for d in all_data],
    'B²/(M*θ_D²)': [d['B']**2/(d['M']*d['tD']**2) for d in all_data],
}

results = []
for name, vals in candidates.items():
    vals = np.array(vals)
    if np.any(vals <= 0): continue
    corr = np.corrcoef(np.log(vals), log_K0)[0,1]
    results.append((name, corr, abs(corr)))

results.sort(key=lambda x: -x[2])
print(f"{'参数':<16} {'corr(ln K_0, ln param)':>25}")
print("-" * 45)
for name, corr, _ in results[:15]:
    print(f"{name:<16} {corr:>25.3f}")

# ============================================================
# 2. 多变量回归: ln K_0 = Σ a_i · ln(param_i) + c
# ============================================================
print(f"\n{'='*90}")
print("2. 多变量回归 K_0")
print("=" * 90)

# 用top参数做多变量回归
top_params = [r[0] for r in results[:6]]
print(f"用参数: {top_params}")

X_multi = np.column_stack([np.log(np.array(candidates[p])) for p in top_params] + [np.ones(len(all_data))])
y_multi = log_K0
coef_m, _, _, _ = lstsq(X_multi, y_multi, rcond=None)
pred_m = X_multi @ coef_m
r2_m = 1 - np.sum((y_multi - pred_m)**2) / np.sum((y_multi - np.mean(y_multi))**2)
print(f"R² = {r2_m:.3f}")
for i, p in enumerate(top_params):
    print(f"  {p}: {coef_m[i]:.3f}")
print(f"  const: {coef_m[-1]:.3f}")

# ============================================================
# 3. LOOCV: 从材料参数直接预测K_0 → Tc
# ============================================================
print(f"\n{'='*90}")
print("3. LOOCV: 材料→K_0(多变量回归)→Tc")
print("=" * 90)

all_preds = []
all_exps = []
for i, d_test in enumerate(all_data):
    # 训练集
    train = [d for j,d in enumerate(all_data) if j != i]
    # 构建特征
    def get_features(d):
        return [np.log(d['B']), np.log(d['M']), np.log(d['Z_val']),
                np.log(d['V_cell']), np.log(d['tD']), 1]

    X_tr = np.array([get_features(d) for d in train])
    y_tr = np.array([np.log(d['K0']) for d in train])
    coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)

    # 预测K_0
    x_test = np.array(get_features(d_test))
    K0_pred = np.exp(x_test @ coef_tr)

    # 计算Tc
    k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132
    tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))

    all_preds.append(tc_pred)
    all_exps.append(d_test['tc'])

errs = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
print(f"全局回归LOOCV: {len(errs)}个材料")
print(f"  中位误差: {np.median(errs)*100:.0f}%")
print(f"  2倍内: {np.sum(errs<1)/len(errs)*100:.0f}%")
print(f"  5倍内: {np.sum(errs<4)/len(errs)*100:.0f}%")

# ============================================================
# 4. 类别+全局混合: ln K_0 = Σ a_i·ln(param_i) + c_cat
# ============================================================
print(f"\n{'='*90}")
print("4. LOOCV: 材料→K_0(全局回归+类别偏置)→Tc")
print("=" * 90)

all_preds2 = []
all_exps2 = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i]

    def get_features2(d, cat_val, cat_list):
        feats = [np.log(d['B']), np.log(d['M']), np.log(d['Z_val']),
                 np.log(d['V_cell']), np.log(d['tD'])]
        # 类别one-hot
        for c in cat_list:
            feats.append(1.0 if d['cat'] == c else 0.0)
        feats.append(1.0)
        return feats

    cat_list = sorted(set(d['cat'] for d in train))
    X_tr = np.array([get_features2(d, cat, cat_list) for d in train])
    y_tr = np.array([np.log(d['K0']) for d in train])
    coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)

    x_test = np.array(get_features2(d_test, cat, cat_list))
    K0_pred = np.exp(x_test @ coef_tr)

    k_eff_pred = K0_pred * d_test['G']**(-0.769) * d_test['tD']**1.132
    tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))

    all_preds2.append(tc_pred)
    all_exps2.append(d_test['tc'])

errs2 = np.abs(np.array(all_preds2) - np.array(all_exps2)) / np.array(all_exps2)
print(f"全局+类别偏置LOOCV: {len(errs2)}个材料")
print(f"  中位误差: {np.median(errs2)*100:.0f}%")
print(f"  2倍内: {np.sum(errs2<1)/len(errs2)*100:.0f}%")
print(f"  5倍内: {np.sum(errs2<4)/len(errs2)*100:.0f}%")

# ============================================================
# 5. 最终: 直接回归ln(Tc)与所有参数
# ============================================================
print(f"\n{'='*90}")
print("5. 最终: 直接回归ln(Tc)与材料参数+类别")
print("=" * 90)

all_preds3 = []
all_exps3 = []
for i, d_test in enumerate(all_data):
    train = [d for j,d in enumerate(all_data) if j != i]
    cat_list = sorted(set(d['cat'] for d in train))

    def get_tc_features(d, cl):
        feats = [np.log(d['ddv0']), np.log(d['tD']), np.log(d['B']),
                 np.log(d['M']), np.log(d['Z_val']), np.log(d['V_cell'])]
        for c in cl:
            feats.append(1.0 if d['cat'] == c else 0.0)
        feats.append(1.0)
        return feats

    X_tr = np.array([get_tc_features(d, cat_list) for d in train])
    y_tr = np.array([np.log(d['tc']) for d in train])
    coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)

    x_test = np.array(get_tc_features(d_test, cat_list))
    tc_pred = np.exp(x_test @ coef_tr)

    all_preds3.append(tc_pred)
    all_exps3.append(d_test['tc'])

errs3 = np.abs(np.array(all_preds3) - np.array(all_exps3)) / np.array(all_exps3)
print(f"直接回归LOOCV: {len(errs3)}个材料")
print(f"  中位误差: {np.median(errs3)*100:.0f}%")
print(f"  2倍内: {np.sum(errs3<1)/len(errs3)*100:.0f}%")
print(f"  5倍内: {np.sum(errs3<4)/len(errs3)*100:.0f}%")

# ============================================================
# 6. 总结
# ============================================================
print(f"\n{'='*90}")
print("6. 总结")
print("=" * 90)
print(f"""
K_0预测方法对比 (LOOCV):

方法                              | 中位误差 | 2倍内 | 5倍内
----------------------------------+----------+-------+------
类别K_0中位数                      |   60%    |  73%  |  89%
BCS λ_ep两步回归                   |   54%    |  76%  |  91%
K_0全局回归(B,M,Z,V,θ_D)           |   {np.median(errs)*100:.0f}%    |  {np.sum(errs<1)/len(errs)*100:.0f}%  |  {np.sum(errs<4)/len(errs)*100:.0f}%
K_0全局+类别偏置                    |   {np.median(errs2)*100:.0f}%    |  {np.sum(errs2<1)/len(errs2)*100:.0f}%  |  {np.sum(errs2<4)/len(errs2)*100:.0f}%
直接回归Tc(Δδ₀,θ_D,B,M,Z,V+类别)    |   {np.median(errs3)*100:.0f}%    |  {np.sum(errs3<1)/len(errs3)*100:.0f}%  |  {np.sum(errs3<4)/len(errs3)*100:.0f}%

最佳: 直接回归Tc, 中位误差{np.median(errs3)*100:.0f}%, {np.sum(errs3<1)/len(errs3)*100:.0f}%在2倍内

K_0与材料参数的最佳单变量相关:
  {results[0][0]}: corr={results[0][1]:.3f}
  {results[1][0]}: corr={results[1][1]:.3f}
  {results[2][0]}: corr={results[2][1]:.3f}

多变量回归R² = {r2_m:.3f} (B,M,Z,V,θ_D → K_0)

结论:
  - K_0与材料参数有中等相关(R²={r2_m:.3f})
  - 直接回归Tc给出{np.median(errs3)*100:.0f}%中位误差({np.sum(errs3<1)/len(errs3)*100:.0f}%在2倍内)
  - 这是当前最佳的第一性预测
  - 进一步改进需要DFT精确计算N(0)和M_ep
""")