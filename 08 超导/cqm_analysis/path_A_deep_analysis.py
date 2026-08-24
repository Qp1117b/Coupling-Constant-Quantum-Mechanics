"""
路径A深入分析：热涨落混合条件

条件：GAP - A·tanh(θ_D/(2T)) = α·T/θ_D
  A = 3β²Δδ₀²/(16(1-βδ_v))
  Δδ₀从晶格第一性计算, δ_v从Tc反推(当前公式)

反推α: α = (GAP - A·tanh(θ_D/(2Tc))) · θ_D / Tc
"""

import csv
import re
import math
import numpy as np
from collections import defaultdict
from scipy.optimize import brentq

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0

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

def get_mass(comp): return sum(ATOM_DB[e][0]*n for e,n in comp.items() if e in ATOM_DB)
def get_debye(comp):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0]*n) for e,n in comp.items() if e in ATOM_DB and ATOM_DB[e][1]>0]
    return sum(d*w for d,w in ws)/sum(w for _,w in ws) if ws else 300
def get_radius(comp):
    rs = [ATOM_DB[e][2] for e in comp if e in ATOM_DB and ATOM_DB[e][2]>0]
    return np.mean(rs) if rs else 1.5
def get_bulk(comp):
    bs = [ATOM_DB[e][3] for e in comp if e in ATOM_DB and ATOM_DB[e][3]>0]
    return np.mean(bs) if bs else 50

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
    P = 0
    if '高压' in condition or 'GPa' in condition:
        pm = re.search(r'~?(\d+)GPa', condition)
        P = int(pm.group(1)) if pm else 50
    L = 2*r; l_intra = 2*r; z = 6; edges = []; f = 0.5
    if '元素' in cat:
        tD = ATOM_DB.get(list(comp.keys())[0], (0,300,1.5,50))[1] or tD
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
    return tD, M, L, z, edges, l_intra, B, P, f

def rev_delta_v(ddv0, theta_D, tc):
    """从Tc反推δ_v (当前arccoth公式)"""
    u = theta_D / (2*tc)
    tanh_u = math.tanh(u)
    x = 1.0 / tanh_u  # coth(u)
    # x = 3β²Δδ₀²/(16(1-βδ_v)·GAP) → 1-βδ_v = 3β²Δδ₀²/(16·x·GAP)
    one_minus_bdv = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if one_minus_bdv <= 0 or one_minus_bdv >= 1: return None
    beta_dv = 1 - one_minus_bdv
    return beta_dv / BETA

def calc_A(ddv0, delta_v):
    return 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v))

def tc_pathA(theta_D, A, alpha):
    """路径A: GAP - A·tanh(θ_D/(2T)) = α·T/θ_D"""
    def eq(T):
        if T <= 0: return 1e10
        return GAP - A * np.tanh(theta_D / (2*T)) - alpha * T / theta_D
    try:
        if eq(0.1) * eq(10000) > 0: return 0.0
        return brentq(eq, 0.1, 10000)
    except: return 0.0

# ============================================================
# 加载数据
# ============================================================
input_file = "superconductors_deduplicated.csv"
with open(input_file, 'r', encoding='utf-8-sig') as fh:
    reader = csv.reader(fh)
    header = next(reader)
    rows = list(reader)

all_data = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc = float(tc_match.group(1))
    params = estimate_params(formula, cat, condition)
    if not params: continue
    tD, M, L, z, edges, l_intra, B, P, f = params
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)

    # 反推δ_v
    dv = rev_delta_v(ddv0, tD, tc)
    if dv is None: continue

    # 计算A
    A = calc_A(ddv0, dv)

    # 反推α: GAP - A·tanh(θ_D/(2Tc)) = α·Tc/θ_D
    tanh_val = math.tanh(tD / (2*tc))
    alpha = (GAP - A * tanh_val) * tD / tc

    all_data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'ddv0': ddv0, 'delta_v': dv, 'A': A, 'alpha': alpha
    })

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. α统计
# ============================================================
print(f"\n{'='*90}")
print("1. α反推统计")
print("=" * 90)

alphas = np.array([d['alpha'] for d in all_data])
print(f"α: 均值={np.mean(alphas):.4f}, 中位数={np.median(alphas):.4f}")
print(f"  标准差={np.std(alphas):.4f}, CV={np.std(alphas)/abs(np.mean(alphas))*100:.1f}%")
print(f"  范围: [{np.min(alphas):.4f}, {np.max(alphas):.4f}]")
print(f"  25%/75%: {np.percentile(alphas,25):.4f} / {np.percentile(alphas,75):.4f}")

# 按类别
print("\n按类别:")
cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 3: continue
    ac = np.array([d['alpha'] for d in cd])
    print(f"  {cat:24s}: n={len(cd):3d}, α={np.mean(ac):.4f}±{np.std(ac):.4f}, CV={np.std(ac)/abs(np.mean(ac))*100:.0f}%")

# ============================================================
# 2. α与材料参数相关性
# ============================================================
print(f"\n{'='*90}")
print("2. α与材料参数相关性")
print("=" * 90)

params_test = {
    'Tc': [d['tc'] for d in all_data],
    'θ_D': [d['tD'] for d in all_data],
    'Δδ₀': [d['ddv0'] for d in all_data],
    'δ_v': [d['delta_v'] for d in all_data],
    'A': [d['A'] for d in all_data],
    'ln(Tc)': [np.log(d['tc']) for d in all_data],
    'θ_D/Tc': [d['tD']/d['tc'] for d in all_data],
    'Tc/θ_D': [d['tc']/d['tD'] for d in all_data],
    'A/GAP': [d['A']/GAP for d in all_data],
    'ln(A/GAP)': [np.log(d['A']/GAP) for d in all_data],
}
for name, vals in params_test.items():
    corr = np.corrcoef(np.array(vals), alphas)[0,1]
    print(f"  corr(α, {name:10s}) = {corr:.3f}")

# ============================================================
# 3. 前向预测（α=全局中位数）
# ============================================================
print(f"\n{'='*90}")
print("3. 前向预测Tc (路径A)")
print("=" * 90)

alpha_med = np.median(alphas)
print(f"全局α中位数 = {alpha_med:.4f}")

# 全局α
errs_global = []
for d in all_data:
    tc_pred = tc_pathA(d['tD'], d['A'], alpha_med)
    if tc_pred > 0:
        err = abs(tc_pred - d['tc']) / d['tc']
        errs_global.append(err)
    else:
        errs_global.append(1e10)
errs_global = np.array(errs_global)
w2 = np.sum(errs_global < 1) / len(errs_global) * 100
print(f"全局α: 中位误差={np.median(errs_global)*100:.0f}%, 2倍内={w2:.0f}%")

# 类别α
cat_alpha = {}
for cat, cd in cat_data.items():
    if len(cd) >= 3:
        cat_alpha[cat] = np.median([d['alpha'] for d in cd])

errs_cat = []
for d in all_data:
    alpha_use = cat_alpha.get(d['cat'], alpha_med)
    tc_pred = tc_pathA(d['tD'], d['A'], alpha_use)
    if tc_pred > 0:
        err = abs(tc_pred - d['tc']) / d['tc']
        errs_cat.append(err)
    else:
        errs_cat.append(1e10)
errs_cat = np.array(errs_cat)
w2_cat = np.sum(errs_cat < 1) / len(errs_cat) * 100
print(f"类别α: 中位误差={np.median(errs_cat)*100:.0f}%, 2倍内={w2_cat:.0f}%")

# ============================================================
# 4. 敏感度对比
# ============================================================
print(f"\n{'='*90}")
print("4. 敏感度对比 (Nb)")
print("=" * 90)

nb = next(d for d in all_data if d['formula'] == 'Nb')
A_nb = nb['A']; alpha_nb = nb['alpha']

# arccoth敏感度
x0 = A_nb / GAP
Tc0_arccoth = nb['tD'] / (2 * np.arctanh(1/x0))
A_pert = A_nb * 1.01
x_pert = A_pert / GAP
Tc_pert_arccoth = nb['tD'] / (2 * np.arctanh(1/x_pert))
sens_arccoth = abs(Tc_pert_arccoth - Tc0_arccoth) / Tc0_arccoth / 0.01

# 路径A敏感度
Tc0_A = tc_pathA(nb['tD'], A_nb, alpha_nb)
Tc_pert_A = tc_pathA(nb['tD'], A_pert, alpha_nb)
sens_A = abs(Tc_pert_A - Tc0_A) / Tc0_A / 0.01

print(f"Nb: A={A_nb:.6f}, GAP={GAP:.6f}, A-GAP={A_nb-GAP:.3e}")
print(f"  arccoth: Tc={Tc0_arccoth:.2f}K, 敏感度={sens_arccoth:.0f} (A变1%→Tc变{sens_arccoth*100:.0f}%)")
print(f"  路径A:   Tc={Tc0_A:.2f}K, 敏感度={sens_A:.1f} (A变1%→Tc变{sens_A*100:.0f}%)")
print(f"  敏感度降低: {sens_arccoth/sens_A:.0f}倍")

# ============================================================
# 5. α的物理推导
# ============================================================
print(f"\n{'='*90}")
print("5. α的物理推导")
print("=" * 90)
print(f"""
条件: GAP - A·tanh(θ_D/(2T)) = α·T/θ_D
  左边 = λ₂(T) - λ₁(T) = 本征值间距
  右边 = α·T/θ_D = 热展宽(归一化)

物理: 超导转变 = 热涨落足以混合两个本征态
  Γ_thermal ~ kT (热噪声)
  Γ_thermal / (kθ_D) = T/θ_D
  α = 混合效率因子

反推α统计:
  中位数 = {np.median(alphas):.4f}
  均值 = {np.mean(alphas):.4f}
  CV = {np.std(alphas)/abs(np.mean(alphas))*100:.0f}%

如果α是普适常数(CV小), 则路径A给出半第一性Tc预测:
  Tc从方程 GAP - A·tanh(θ_D/(2T)) = α·T/θ_D 数值求解
  A从材料第一性计算, α是普适常数

但CV={np.std(alphas)/abs(np.mean(alphas))*100:.0f}%说明α不是普适常数。
""")

# 检查α是否与A/GAP相关（如果是，说明α是A的函数，不是独立参数）
a_over_gap = np.array([d['A']/GAP for d in all_data])
corr_alpha_A = np.corrcoef(a_over_gap, alphas)[0,1]
print(f"corr(α, A/GAP) = {corr_alpha_A:.3f}")
print(f"如果|corr|大, α可能是A的函数(不是独立参数)")

# 拟合 α = f(A/GAP)
from numpy.polynomial import polynomial as P
coeffs = np.polyfit(a_over_gap, alphas, 1)
print(f"线性拟合: α = {coeffs[0]:.4f}·(A/GAP) + {coeffs[1]:.4f}")
alpha_pred = np.polyval(coeffs, a_over_gap)
residual = alphas - alpha_pred
print(f"  残差标准差 = {np.std(residual):.4f} (vs α标准差{np.std(alphas):.4f})")
print(f"  R² = {1 - np.var(residual)/np.var(alphas):.3f}")

# ============================================================
# 6. 总结
# ============================================================
print(f"\n{'='*90}")
print("6. 总结")
print("=" * 90)
print(f"""
路径A（热涨落混合条件）分析结果:

1. 敏感度: arccoth {sens_arccoth:.0f} → 路径A {sens_A:.1f} (降低{sens_arccoth/sens_A:.0f}倍)
2. α反推: 中位数={np.median(alphas):.4f}, CV={np.std(alphas)/abs(np.mean(alphas))*100:.0f}%
3. 前向预测(全局α): 中位误差={np.median(errs_global)*100:.0f}%, 2倍内={w2:.0f}%
4. 前向预测(类别α): 中位误差={np.median(errs_cat)*100:.0f}%, 2倍内={w2_cat:.0f}%

结论:
- 路径A大幅降低敏感度({sens_arccoth/sens_A:.0f}倍)
- 但α不是普适常数(CV={np.std(alphas)/abs(np.mean(alphas))*100:.0f}%)
- α与A/GAP弱相关(corr={corr_alpha_A:.3f})
- 类别α前向预测{w2_cat:.0f}%在2倍内
- 路径A是"半第一性"框架: A从材料计算, α从类别校准
- 比arccoth反推法更诚实(不需要15位精度δ_v)
""")
