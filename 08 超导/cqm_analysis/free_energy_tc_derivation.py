"""
从自由能推导Tc：Tc = (E2-E1)/(S2-S1)

推导链:
  1. 凝聚能 E2-E1 ~ Δδ₀²·K_eff (角亏涨落×曲率刚度)
  2. 熵差 S2-S1 ~ ln(2)·tanh(Tc/θ_D) (§11.3定理4)
  3. 低温近似 tanh(Tc/θ_D) ≈ Tc/θ_D
  4. Tc = Δδ₀²·K_eff / (ln(2)·Tc/θ_D)
  5. Tc² = Δδ₀²·K_eff·θ_D / ln(2)
  6. 如果 K_eff ∝ θ_D: Tc ∝ θ_D·Δδ₀

验证: Tc²/(Δδ₀²·θ_D) = K_eff/ln(2) 是否为类别常数
"""

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
LN2 = math.log(2)

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
    tD, M, L, z, edges, l_intra, B, P, f = params
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)
    all_data.append({'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
                     'ddv0': ddv0, 'B': B, 'M': M})

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. 验证 Tc² ∝ Δδ₀²·θ_D (即 K_eff = const)
# ============================================================
print(f"\n{'='*90}")
print("1. 验证 Tc² ∝ Δδ₀²·θ_D (K_eff=常数)")
print("=" * 90)

# K_eff/ln(2) = Tc²/(Δδ₀²·θ_D)
k_effs = np.array([d['tc']**2 / (d['ddv0']**2 * d['tD']) for d in all_data])
print(f"K_eff/ln(2) = Tc²/(Δδ₀²·θ_D):")
print(f"  均值={np.mean(k_effs):.3f}, 中位数={np.median(k_effs):.3f}")
print(f"  CV={np.std(k_effs)/np.mean(k_effs)*100:.0f}%")
print(f"  范围: [{np.min(k_effs):.3f}, {np.max(k_effs):.3f}]")

# 按类别
print("\n按类别:")
cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 3: continue
    ks = np.array([d['tc']**2/(d['ddv0']**2*d['tD']) for d in cd])
    print(f"  {cat:24s}: n={len(cd):3d}, K/ln2={np.median(ks):.3f}±{np.std(ks):.3f}, CV={np.std(ks)/np.mean(ks)*100:.0f}%")

# ============================================================
# 2. 更一般: Tc² = C · Δδ₀^a · θ_D^b
# ============================================================
print(f"\n{'='*90}")
print("2. 一般形式: ln(Tc²) = a·ln(Δδ₀) + b·ln(θ_D) + c")
print("=" * 90)

from numpy.linalg import lstsq
X = np.array([[2*np.log(d['ddv0']), np.log(d['tD']), 1] for d in all_data])
y = np.array([2*np.log(d['tc']) for d in all_data])
coef, _, _, _ = lstsq(X, y, rcond=None)
a2, b2, c2_val = coef
print(f"  a={a2:.3f} (Δδ₀指数), b={b2:.3f} (θ_D指数), c={c2_val:.3f}")
print(f"  即 Tc² = {np.exp(c2_val):.3f} · Δδ₀^{a2:.3f} · θ_D^{b2:.3f}")
print(f"  即 Tc = {np.exp(c2_val/2):.3f} · Δδ₀^{a2/2:.3f} · θ_D^{b2/2:.3f}")

tc_pred = np.exp(X @ coef)
errs = np.abs(np.exp(y) - tc_pred) / np.exp(y) * 100  # Tc²的误差
errs_tc = np.abs(np.sqrt(np.exp(y)) - np.sqrt(tc_pred)) / np.sqrt(np.exp(y)) * 100
print(f"  Tc中位误差: {np.median(errs_tc):.0f}%, 2倍内: {np.sum(errs_tc<100)/len(errs_tc)*100:.0f}%")

# 理论对比
print(f"\n  理论(自由能): a=2, b=1 (Tc²∝Δδ₀²·θ_D)")
print(f"  经验: a={a2:.3f}, b={b2:.3f}")
print(f"  差异: Δa={a2-2:.3f}, Δb={b2-1:.3f}")

# ============================================================
# 3. K_eff的物理来源探索
# ============================================================
print(f"\n{'='*90}")
print("3. K_eff的物理来源探索")
print("=" * 90)
print("""
从自由能推导:
  Tc² = Δδ₀²·K_eff·θ_D / ln(2)
  K_eff = Tc²·ln(2) / (Δδ₀²·θ_D)

如果 K_eff ∝ θ_D^b_eff:
  Tc² ∝ Δδ₀²·θ_D^(1+b_eff)
  即 b = 1 + b_eff
""")

# 检查 K_eff 与 θ_D 的关系
k_eff_vals = np.array([d['tc']**2 * LN2 / (d['ddv0']**2 * d['tD']) for d in all_data])
theta_Ds = np.array([d['tD'] for d in all_data])

# ln(K_eff) = b_eff·ln(θ_D) + const
X_ke = np.vstack([np.log(theta_Ds), np.ones(len(theta_Ds))]).T
y_ke = np.log(k_eff_vals)
b_eff, c_eff = lstsq(X_ke, y_ke, rcond=None)[0]
print(f"K_eff ∝ θ_D^{b_eff:.3f}")
print(f"  理论b = 1 + b_eff = {1+b_eff:.3f} (vs 经验b={b2:.3f})")

# 检查 K_eff 与其他参数的关系
print("\nK_eff与材料参数相关性:")
params_test = {
    'θ_D': theta_Ds,
    'M': [d['M'] for d in all_data],
    'B(体模量)': [d['B'] for d in all_data],
    'Δδ₀': [d['ddv0'] for d in all_data],
    'ln(θ_D)': np.log(theta_Ds),
    'ln(M)': np.log([d['M'] for d in all_data]),
    'ln(B)': np.log([max(d['B'],1) for d in all_data]),
}
for name, vals in params_test.items():
    corr = np.corrcoef(np.array(vals), k_eff_vals)[0,1]
    print(f"  corr(K_eff, {name:10s}) = {corr:.3f}")

# ============================================================
# 4. 用自由能公式前向预测Tc (LOOCV)
# ============================================================
print(f"\n{'='*90}")
print("4. LOOCV: Tc = √(K_eff_cat·Δδ₀²·θ_D/ln(2))")
print("=" * 90)

# K_eff_cat从训练集估计
all_preds = []
all_exps = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(all_data) if j != i]
    # K_eff = median(Tc²·ln(2)/(Δδ₀²·θ_D))
    k_train = np.median([d['tc']**2 * LN2 / (d['ddv0']**2 * d['tD']) for d in train])
    tc_pred = math.sqrt(k_train * d_test['ddv0']**2 * d_test['tD'] / LN2)
    all_preds.append(tc_pred)
    all_exps.append(d_test['tc'])

errs_loo = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
print(f"LOOCV: {len(errs_loo)}个材料")
print(f"  中位误差: {np.median(errs_loo)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%")

# ============================================================
# 5. 更一般形式 LOOCV: Tc = c_cat · Δδ₀^a_cat · θ_D^b_cat
# ============================================================
print(f"\n{'='*90}")
print("5. LOOCV: Tc = c_cat · Δδ₀^a · θ_D^b (3参数类别校准)")
print("=" * 90)

all_preds3 = []
all_exps3 = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 8:
        train = [d for j,d in enumerate(all_data) if j != i]
    X_tr = np.array([[np.log(d['ddv0']), np.log(d['tD']), 1] for d in train])
    y_tr = np.array([np.log(d['tc']) for d in train])
    try:
        coef_tr, _, _, _ = lstsq(X_tr, y_tr, rcond=None)
        x_test = np.array([np.log(d_test['ddv0']), np.log(d_test['tD']), 1])
        tc_pred = np.exp(x_test @ coef_tr)
        all_preds3.append(tc_pred)
        all_exps3.append(d_test['tc'])
    except:
        pass

errs_loo3 = np.abs(np.array(all_preds3) - np.array(all_exps3)) / np.array(all_exps3)
print(f"LOOCV: {len(errs_loo3)}个材料")
print(f"  中位误差: {np.median(errs_loo3)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_loo3<1)/len(errs_loo3)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_loo3<4)/len(errs_loo3)*100:.0f}%")

# ============================================================
# 6. 总结
# ============================================================
print(f"\n{'='*90}")
print("6. 总结：自由能推导链条")
print("=" * 90)
print(f"""
推导链:
  1. 丛作用量交叉: Tc = (E2-E1)/(S2-S1)  [§11.2]
  2. 凝聚能: E2-E1 ~ Δδ₀²·K_eff  [角亏涨落×曲率刚度]
  3. 熵差: S2-S1 = ln(2)·(1+1/8)·tanh(Tc/θ_D)  [§11.3定理4]
  4. 低温近似: tanh(Tc/θ_D) ≈ Tc/θ_D
  5. 自洽方程: Tc = Δδ₀²·K_eff / (1.125·ln(2)·Tc/θ_D)
  6. 解出: Tc² = Δδ₀²·K_eff·θ_D / (1.125·ln(2))
  7. 如果 K_eff ∝ θ_D: Tc ∝ θ_D·Δδ₀

数值验证:
  - 全局拟合: Tc = {np.exp(c2_val/2):.3f} · Δδ₀^{a2/2:.3f} · θ_D^{b2/2:.3f}
  - 理论: Tc ∝ Δδ₀¹·θ_D¹ (a=2, b=1)
  - 经验: Tc ∝ Δδ₀^{a2/2:.3f}·θ_D^{b2/2:.3f} (a={a2:.3f}, b={b2:.3f})
  - K_eff ∝ θ_D^{b_eff:.3f}

LOOCV结果:
  - 自由能形式(K_eff=类别常数): 中位误差{np.median(errs_loo)*100:.0f}%, 2倍内{np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%
  - 3参数形式(a,b,c类别校准): 中位误差{np.median(errs_loo3)*100:.0f}%, 2倍内{np.sum(errs_loo3<1)/len(errs_loo3)*100:.0f}%

链条完整性:
  ✅ Tc = (E2-E1)/(S2-S1) [§11.2已推导]
  ✅ S2-S1 = ln(2)·(1+1/8)·tanh(Tc/θ_D) [§11.3已推导]
  ✅ 低温近似 tanh(x)≈x [数学]
  ⚠️ E2-E1 ~ Δδ₀²·K_eff [假设,需推导K_eff]
  ⚠️ K_eff ∝ θ_D^{b_eff:.3f} [经验,需物理推导]
  🔴 K_eff的微观表达式 [未推导]

待完成:
  1. K_eff的微观推导 (从Regge几何/声子谱)
  2. K_eff ∝ θ_D^b_eff 的物理机制
  3. E2-E1 ~ Δδ₀²·K_eff 的严格证明
""")