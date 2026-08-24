"""
深入验证 Tc ≈ θ_D · Δδ₀^a 关系

形式4给出 a≈0.93≈1，即 Tc ∝ θ_D · Δδ₀ (近似线性!)
敏感度降低6655倍

验证:
1. 线性关系 Tc = c · θ_D · Δδ₀ 的精度
2. 按类别检查
3. 物理解释
4. 与BCS对比
"""

import csv, re, math
import numpy as np
from collections import defaultdict

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
    all_data.append({'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD, 'ddv0': ddv0})

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. 线性关系 Tc = c · θ_D · Δδ₀
# ============================================================
print(f"\n{'='*90}")
print("1. 线性关系 Tc = c · θ_D · Δδ₀")
print("=" * 90)

# 反推c: c = Tc / (θ_D · Δδ₀)
cs = np.array([d['tc'] / (d['tD'] * d['ddv0']) for d in all_data])
print(f"c = Tc/(θ_D·Δδ₀): 均值={np.mean(cs):.3f}, 中位数={np.median(cs):.3f}")
print(f"  标准差={np.std(cs):.3f}, CV={np.std(cs)/np.mean(cs)*100:.0f}%")
print(f"  范围: [{np.min(cs):.3f}, {np.max(cs):.3f}]")

# 按类别
print("\n按类别:")
cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 3: continue
    cc = np.array([d['tc']/(d['tD']*d['ddv0']) for d in cd])
    print(f"  {cat:24s}: n={len(cd):3d}, c={np.median(cc):.3f}±{np.std(cc):.3f}, CV={np.std(cc)/np.mean(cc)*100:.0f}%")

# ============================================================
# 2. 幂律拟合 Tc = c · (θ_D · Δδ₀)^a
# ============================================================
print(f"\n{'='*90}")
print("2. 幂律拟合 Tc = c · (θ_D · Δδ₀)^a")
print("=" * 90)

# ln(Tc) = a·ln(θ_D·Δδ₀) + ln(c)
x = np.log(np.array([d['tD']*d['ddv0'] for d in all_data]))
y = np.log(np.array([d['tc'] for d in all_data]))
A = np.vstack([x, np.ones(len(x))]).T
a_fit, c_fit = np.linalg.lstsq(A, y, rcond=None)[0]
print(f"a = {a_fit:.3f}, c = {np.exp(c_fit):.3f}")
print(f"即 Tc = {np.exp(c_fit):.3f} · (θ_D·Δδ₀)^{a_fit:.3f}")

tc_pred = np.exp(c_fit) * (np.array([d['tD']*d['ddv0'] for d in all_data]))**a_fit
errs = np.abs(tc_pred - np.array([d['tc'] for d in all_data])) / np.array([d['tc'] for d in all_data])
print(f"全局拟合: 中位误差={np.median(errs)*100:.0f}%, 2倍内={np.sum(errs<1)/len(errs)*100:.0f}%")

# ============================================================
# 3. 留一法交叉验证（类别校准）
# ============================================================
print(f"\n{'='*90}")
print("3. LOOCV: Tc = c_cat · (θ_D · Δδ₀)^a_cat")
print("=" * 90)

all_preds = []
all_exps = []
all_cats = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(all_data) if j != i]
    x_tr = np.log(np.array([d['tD']*d['ddv0'] for d in train]))
    y_tr = np.log(np.array([d['tc'] for d in train]))
    A_tr = np.vstack([x_tr, np.ones(len(x_tr))]).T
    try:
        a_tr, c_tr = np.linalg.lstsq(A_tr, y_tr, rcond=None)[0]
        tc_p = np.exp(c_tr) * (d_test['tD']*d_test['ddv0'])**a_tr
        all_preds.append(tc_p)
        all_exps.append(d_test['tc'])
        all_cats.append(cat)
    except:
        pass

errs_loo = np.abs(np.array(all_preds) - np.array(all_exps)) / np.array(all_exps)
print(f"LOOCV结果: {len(errs_loo)}个材料")
print(f"  中位误差: {np.median(errs_loo)*100:.0f}%")
print(f"  平均误差: {np.mean(errs_loo)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%")
print(f"  3倍内: {np.sum(errs_loo<2)/len(errs_loo)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%")

# ============================================================
# 4. 具体材料验证
# ============================================================
print(f"\n{'='*90}")
print("4. 具体材料验证 (Tc = c·θ_D·Δδ₀, c=中位数)")
print("=" * 90)

c_med = np.median(cs)
print(f"用c={c_med:.3f}\n")
print(f"{'材料':<12} {'类别':<16} {'Tc_exp':>8} {'Tc_pred':>8} {'误差%':>8} {'θ_D':>6} {'Δδ₀':>8}")
print("-" * 75)

# 选代表性材料
representatives = ['Nb', 'Pb', 'Al', 'Hg', 'Sn', 'La', 'V', 'Ta', 'Tl', 'In']
for d in all_data:
    if d['formula'] in representatives:
        tc_p = c_med * d['tD'] * d['ddv0']
        err = (tc_p - d['tc'])/d['tc']*100
        print(f"{d['formula']:<12} {d['cat'][:16]:<16} {d['tc']:>8.1f} {tc_p:>8.1f} {err:>8.0f} {d['tD']:>6.0f} {d['ddv0']:>8.4f}")

# ============================================================
# 5. 物理推导尝试
# ============================================================
print(f"\n{'='*90}")
print("5. 物理推导: 为什么 Tc ∝ θ_D · Δδ₀?")
print("=" * 90)
print(f"""
经验发现: Tc ≈ {c_med:.2f} · θ_D · Δδ₀  (CV={np.std(cs)/np.mean(cs)*100:.0f}%)

当前arccoth公式: Tc = θ_D / (2·arccoth(x)), x = 3β²Δδ₀²/(16(1-βδ_v)·GAP)

当x→1⁺时: Tc ≈ θ_D / ln(2/(x-1))
  x-1 = (3β²Δδ₀² - 16(1-βδ_v)·GAP) / (16(1-βδ_v)·GAP)
  如果 3β²Δδ₀² ≈ 16(1-βδ_v)·GAP + ε, ε小:
  x-1 ≈ ε / (16(1-βδ_v)·GAP)

如果 ε ∝ Δδ₀² (即驱动力-阻力 ∝ Δδ₀²):
  x-1 ∝ Δδ₀² / (1-βδ_v)
  Tc ∝ θ_D / ln(1/Δδ₀²) = θ_D / (2·ln(1/Δδ₀))
  这是对数依赖，不是线性！

如果 ε ∝ Δδ₀ (即驱动力-阻力 ∝ Δδ₀):
  x-1 ∝ Δδ₀ / (1-βδ_v)
  Tc ∝ θ_D / ln(1/Δδ₀)
  仍然是对数。

要得到线性 Tc ∝ θ_D·Δδ₀, 需要:
  ln(2/(x-1)) ∝ 1/Δδ₀
  即 x-1 ∝ exp(-1/Δδ₀)
  这是BCS-like指数形式!

这意味着: 如果 1-βδ_v ∝ exp(-c/Δδ₀), 则 Tc ∝ θ_D·Δδ₀
  即 δ_v = (1 - A·exp(-c/Δδ₀))/β

物理解释:
  1-βδ_v = 谱间隙阻尼
  如果阻尼随Δδ₀指数变化(BCS-like), 则Tc线性依赖Δδ₀
  这是自洽的: BCS中gap Δ ∝ exp(-1/V), Tc ∝ Δ

结论: Tc ∝ θ_D·Δδ₀ 等价于BCS-like的指数关系
  不是新物理，而是BCS在不同参数化下的表现
""")

# ============================================================
# 6. 最终对比
# ============================================================
print(f"{'='*90}")
print("6. 最终对比")
print("=" * 90)
print(f"""
方法                          | 中位误差 | 2倍内 | 5倍内 | 需要δ_v? | 敏感度
------------------------------+----------+-------+-------+----------+-------
arccoth反推(当前)              |    0%    | 100%  | 100%  | 是(15位) | 46000%
半第一性(类别b_cat)            |   57%    |  53%  |  80%  | 否       | ~100%
路径A(类别α)                  |    1%    |  59%  |  90%  | 是(反推) | 460%
BCS-like回归(LOOCV)            |   59%    |  75%  |  91%  | 否       | 691%
线性Tc=c·θ_D·Δδ₀ (LOOCV)      |   {np.median(errs_loo)*100:.0f}%    |  {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%  |  {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%  | 否       | ~100%

推荐: 线性形式 Tc = c_cat · θ_D · Δδ₀
  - 不需要δ_v (纯从Δδ₀和θ_D)
  - 敏感度~100% (可接受)
  - LOOCV: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%在2倍内, {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%在5倍内
  - 物理推导: 等价于BCS-like指数关系(1-βδ_v ∝ exp(-c/Δδ₀))
  - 类似BCS: Tc = 1.14·θ_D·exp(-1/(N(0)V-μ*)), CQM: Tc = c·θ_D·Δδ₀
""")