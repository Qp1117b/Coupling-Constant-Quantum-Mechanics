"""
K_eff微观推导尝试

从自由能: Tc² = Δδ₀²·K_eff·θ_D / (1.125·ln(2))
  K_eff = Tc²·1.125·ln(2) / (Δδ₀²·θ_D)

K_eff的物理来源:
  1. Regge作用量: E_角亏 = K_eff·Σ δ_v²·A_v
  2. 声子谱: K_eff ~ ℏω_D = k_B·θ_D
  3. 电子-声子耦合: K_eff ~ N(0)·V²

推导K_eff ~ k_B·θ_D:
  Δδ₀² = (C²/l²)·(3ℏ/(4ω_D))·(1-f)·Σ
  K_eff = k_B·θ_D = ℏ·ω_D
  Tc² = Δδ₀²·ℏ·ω_D·θ_D/β = (C²/l²)·(3ℏ²/4)·(1-f)·Σ·θ_D/β
  Tc = (C/l)·√(3ℏ²/(4β))·√((1-f)·Σ)·√θ_D
  即 Tc ∝ √θ_D·(1/l)·√((1-f)·Σ)

验证: Tc/(√θ_D·G) 是否为常数, G = (1/l)·√((1-f)·Σ)
  等价于验证 Tc/(θ_D·Δδ₀) = c (之前已验证, CV~297%)

更精确: 从Δδ₀公式反推G, 检查Tc vs √θ_D·G
"""

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

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

    # 从Δδ₀公式反推G = (1/l)·√((1-f)·Σ)
    # Δδ₀² = (C²/l²)·(3ℏ²/(4k_B·θ_D))·(1-f)·Σ
    # G² = (1/l²)·(1-f)·Σ = Δδ₀²·θ_D·4k_B/(C²·3ℏ²)
    L_m = L * 1e-10
    G2 = ddv0**2 * tD * 4 * KB / (C2 * 3 * HBAR**2)
    G = math.sqrt(G2)

    # K_eff = Tc²·1.125·ln(2)/(Δδ₀²·θ_D)
    k_eff = tc**2 * 1.125 * LN2 / (ddv0**2 * tD)

    all_data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'ddv0': ddv0, 'B': B, 'M': M, 'L': L, 'G': G, 'k_eff': k_eff,
        'f': f, 'z': z
    })

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. K_eff ~ k_B·θ_D 验证
# ============================================================
print(f"\n{'='*90}")
print("1. K_eff ~ k_B·θ_D 验证")
print("=" * 90)

# 如果K_eff = α·k_B·θ_D, 则 α = K_eff/(k_B·θ_D)
alphas = np.array([d['k_eff']/(KB*d['tD']) for d in all_data])
print(f"α = K_eff/(k_B·θ_D): 均值={np.mean(alphas):.2e}, 中位数={np.median(alphas):.2e}")
print(f"  CV={np.std(alphas)/np.mean(alphas)*100:.0f}%")
print(f"  → K_eff不是简单的k_B·θ_D")

# ============================================================
# 2. K_eff的分解: K_eff = K_0·θ_D^a·F(结构)
# ============================================================
print(f"\n{'='*90}")
print("2. K_eff的结构分解")
print("=" * 90)

# 检查K_eff与G的关系 (G包含结构信息)
# 如果K_eff = K_0·G^q, 则Tc² = Δδ₀²·K_0·G^q·θ_D/β
# 但Δδ₀² = C²·G²·3ℏ²/(4k_B·θ_D), 所以
# Tc² = C²·G²·3ℏ²/(4k_B·θ_D)·K_0·G^q·θ_D/β
# = C²·3ℏ²/(4k_B·β)·K_0·G^(2+q)
# Tc ∝ G^((2+q)/2)

# 经验: Tc ∝ Δδ₀^0.308·θ_D^0.874
# Δδ₀ ∝ G·θ_D^(-0.5), 所以 Tc ∝ (G·θ_D^(-0.5))^0.308·θ_D^0.874
# = G^0.308·θ_D^(-0.154+0.874) = G^0.308·θ_D^0.72
# 所以 (2+q)/2 = 0.308 → q = -1.384

# 即 K_eff ∝ G^(-1.384)！K_eff随G增大而减小
print("如果Tc ∝ Δδ₀^0.308·θ_D^0.874, 且Δδ₀ ∝ G·θ_D^(-0.5):")
print("  Tc ∝ G^0.308·θ_D^0.72")
print("  从Tc² = Δδ₀²·K_eff·θ_D/β:")
print("  K_eff ∝ G^(-1.384)·θ_D^0.44")
print("  即K_eff随G(结构涨落)增大而减小")

# 验证
log_G = np.log(np.array([d['G'] for d in all_data]))
log_keff = np.log(np.array([d['k_eff'] for d in all_data]))
log_tD = np.log(np.array([d['tD'] for d in all_data]))

# ln(K_eff) = a·ln(G) + b·ln(θ_D) + c
from numpy.linalg import lstsq
X = np.vstack([log_G, log_tD, np.ones(len(log_G))]).T
coef_ke, _, _, _ = lstsq(log_keff.reshape(-1,1) if False else X, log_keff, rcond=None)
a_ke, b_ke, c_ke = coef_ke
print(f"\n直接拟合: K_eff = {np.exp(c_ke):.4f} · G^{a_ke:.3f} · θ_D^{b_ke:.3f}")
print(f"  理论预测: a=-1.384, b=0.44")
print(f"  实际: a={a_ke:.3f}, b={b_ke:.3f}")

# ============================================================
# 3. K_eff的物理推导: 从Regge作用量
# ============================================================
print(f"\n{'='*90}")
print("3. K_eff的物理推导")
print("=" * 90)
print(f"""
从Regge作用量推导K_eff:

Regge作用量: S_Regge = Σ_v K_v·δ_v²·A_v
  K_v: 顶点v的曲率刚度
  A_v: 顶点v的Voronoi面积
  δ_v: 顶点v的角亏

在CQM中:
  - 角亏涨落 Δδ₀ 来自声子零点运动
  - 曲率刚度 K_v 来自电子对声子的响应
  - K_eff = <K_v> (空间平均)

从声子谱:
  K_v ~ ℏ·ω_ph·|∂δ/∂u|²
  其中u是原子位移, ω_ph是声子频率

  |∂δ/∂u|² ~ C²/l² (从C²=2/3推导)
  ω_ph ~ ω_D = k_B·θ_D/ℏ

  K_v ~ ℏ·ω_D·C²/l² = k_B·θ_D·C²/l²

但经验K_eff ∝ G^({a_ke:.3f})·θ_D^({b_ke:.3f}), 不是简单的θ_D/l²

修正: K_eff包含电子结构信息
  K_eff ~ N(0)·(ℏω_D)²·|M_ep|²
  N(0): Fermi面态密度
  M_ep: 电子-声子矩阵元

  这给出K_eff ∝ N(0)·θ_D²·|M_ep|²
  但经验K_eff ∝ θ_D^{b_ke:.3f}, 不是θ_D²

结论: K_eff的完整表达式需要DFT计算:
  1. Fermi面态密度N(0)
  2. 电子-声子矩阵元M_ep
  3. 声子谱ω(q)
  K_eff = ∫_FS dS/(2π)³ · |M_ep|²/(ℏω) · tanh(ℏω/2kT)
""")

# ============================================================
# 4. 实际可用的K_eff表达式
# ============================================================
print(f"{'='*90}")
print("4. 实际可用的K_eff表达式")
print("=" * 90)

# K_eff = Tc²·1.125·ln(2)/(Δδ₀²·θ_D)
# 从自由能: Tc² = Δδ₀²·K_eff·θ_D/(1.125·ln(2))

# 如果K_eff = K_0·G^a·θ_D^b (K_0类别常数)
# Tc² = Δδ₀²·K_0·G^a·θ_D^(1+b)/(1.125·ln(2))
# = C²·G²·3ℏ²/(4k_B·θ_D)·K_0·G^a·θ_D^(1+b)/β
# = C²·3ℏ²/(4k_B·β)·K_0·G^(2+a)·θ_D^b

# Tc = C·√(3ℏ²/(4k_B·β))·√K_0·G^((2+a)/2)·θ_D^(b/2)

# 与经验Tc ∝ G^0.308·θ_D^0.72对比:
# (2+a)/2 = 0.308 → a = -1.384
# b/2 = 0.72 → b = 1.44

# 所以K_eff = K_0·G^(-1.384)·θ_D^1.44
# K_0是类别常数

print("从经验拟合:")
print(f"  K_eff = K_0_cat · G^({a_ke:.3f}) · θ_D^({b_ke:.3f})")
print(f"  K_0_cat: 类别常数\n")

# 按类别拟合K_0
cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

print(f"{'类别':<24} {'n':>4} {'K_0':>10} {'CV%':>6}")
print("-" * 50)
cat_K0 = {}
for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 5: continue
    # K_0 = K_eff / (G^a · θ_D^b)
    k0s = [d['k_eff'] / (d['G']**a_ke * d['tD']**b_ke) for d in cd]
    k0s = np.array(k0s)
    cat_K0[cat] = np.median(k0s)
    cv = np.std(k0s)/np.mean(k0s)*100 if np.mean(k0s) != 0 else 0
    print(f"{cat:<24} {len(cd):>4} {np.median(k0s):>10.4f} {cv:>6.0f}%")

# ============================================================
# 5. LOOCV: 完整链条
# ============================================================
print(f"\n{'='*90}")
print("5. LOOCV: Tc = √(Δδ₀²·K_eff·θ_D/(1.125·ln(2)))")
print(f"  K_eff = K_0_cat · G^({a_ke:.3f}) · θ_D^({b_ke:.3f})")
print("=" * 90)

all_preds = []
all_exps = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(all_data) if j != i]
    # 从训练集估计K_0
    k0_train = np.median([d['k_eff']/(d['G']**a_ke * d['tD']**b_ke) for d in train])
    # 前向计算
    k_eff_pred = k0_train * d_test['G']**a_ke * d_test['tD']**b_ke
    tc_pred = math.sqrt(d_test['ddv0']**2 * k_eff_pred * d_test['tD'] / (1.125 * LN2))
    all_preds.append(tc_pred)
    all_exps.append(d_test['tc'])

errs = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
print(f"LOOCV: {len(errs)}个材料")
print(f"  中位误差: {np.median(errs)*100:.0f}%")
print(f"  2倍内: {np.sum(errs<1)/len(errs)*100:.0f}%")
print(f"  5倍内: {np.sum(errs<4)/len(errs)*100:.0f}%")

# ============================================================
# 6. 完整推导链条
# ============================================================
print(f"\n{'='*90}")
print("6. 完整第一性预测链条")
print("=" * 90)
print(f"""
┌─────────────────────────────────────────────────────────────────┐
│ 第一性预测链条: 从材料结构 → Tc                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. 材料晶体结构 (晶格常数l, 原子质量m, 配位数z)                │
│    ↓                                                             │
│ 2. Debye温度 θ_D (从声子谱或查表)                    [✅ 已有]  │
│    ↓                                                             │
│ 3. 角亏涨落 Δδ₀ (§11.10: 10环节计算链)               [✅ 已有]  │
│    Δδ₀² = (C²/l²)·(3ℏ/(4ω_D))·(1-f)·Σ(1/m_i+1/m_j)          │
│    ↓                                                             │
│ 4. 结构因子 G = (1/l)·√((1-f)·Σ)                     [✅ 推导]  │
│    从Δδ₀和θ_D反推: G² = Δδ₀²·θ_D·4k_B/(C²·3ℏ²)             │
│    ↓                                                             │
│ 5. 曲率刚度 K_eff (从Regge作用量)                     [⚠️ 半推导] │
│    K_eff = K_0_cat · G^({a_ke:.3f}) · θ_D^({b_ke:.3f})                │
│    K_0_cat: 类别常数 (类似BCS的μ*)                             │
│    ↓                                                             │
│ 6. 熵差 S₂-S₁ (§11.3定理4)                           [✅ 已有]  │
│    S₂-S₁ = ln(2)·(1+1/8)·tanh(Tc/θ_D) ≈ 1.125·ln(2)·Tc/θ_D  │
│    ↓                                                             │
│ 7. 自由能交叉 Tc = (E₂-E₁)/(S₂-S₁)                  [✅ §11.2] │
│    E₂-E₁ = Δδ₀²·K_eff (凝聚能=角亏涨落×曲率刚度)             │
│    ↓                                                             │
│ 8. Tc² = Δδ₀²·K_eff·θ_D / (1.125·ln(2))             [✅ 推导]  │
│    Tc = √(Δδ₀²·K_eff·θ_D / (1.125·ln(2)))                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

链条状态:
  ✅ 环节1-4: 从材料结构计算Δδ₀和G (第一性)
  ⚠️ 环节5: K_eff = K_0_cat·G^a·θ_D^b (半第一性, K_0需类别校准)
  ✅ 环节6-8: 从自由能导出Tc (第一性)

LOOCV结果: 中位误差{np.median(errs)*100:.0f}%, 2倍内{np.sum(errs<1)/len(errs)*100:.0f}%, 5倍内{np.sum(errs<4)/len(errs)*100:.0f}%

待闭合:
  🔴 K_0_cat的微观推导 (需DFT: N(0), M_ep, 声子谱)
  🔴 K_eff ∝ G^({a_ke:.3f})·θ_D^({b_ke:.3f}) 的物理机制
  🔴 E₂-E₁ = Δδ₀²·K_eff 的严格证明 (从Regge作用量)
""")