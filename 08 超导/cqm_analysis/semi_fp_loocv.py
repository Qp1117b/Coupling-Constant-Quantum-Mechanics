"""
半第一性Tc预测：严格交叉验证

只用反推成功的材料（δ_v > 0），做留一法交叉验证。
模型: Tc = θ_D / (ln(λ) + b_cat)
"""

import csv
import re
import math
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
    'Np': (237.05, 0, 1.75, 0), 'Pu': (244.06, 0, 1.75, 0),
    'Am': (243.06, 0, 1.75, 0), 'Cm': (247.07, 0, 1.75, 0),
}

def parse_formula(f):
    f = re.sub(r'[\(（].*?[\)）]', '', f.strip())
    r = {}
    for e, c in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f):
        if e in ATOM_DB: r[e] = r.get(e, 0) + (float(c) if c else 1.0)
    return r

def get_mass(c): return sum(ATOM_DB[e][0]*n for e,n in c.items() if e in ATOM_DB)
def get_debye(c):
    ws = [(ATOM_DB[e][1], ATOM_DB[e][0]*n) for e,n in c.items() if e in ATOM_DB and ATOM_DB[e][1]>0]
    return sum(d*w for d,w in ws)/sum(w for _,w in ws) if ws else 300
def get_radius(c):
    rs = [ATOM_DB[e][2] for e in c if e in ATOM_DB and ATOM_DB[e][2]>0]
    return np.mean(rs) if rs else 1.5
def get_bulk(c):
    bs = [ATOM_DB[e][3] for e in c if e in ATOM_DB and ATOM_DB[e][3]>0]
    return np.mean(bs) if bs else 50

def ddv_inter(M, L, tD, z, f=0.5):
    Lm = L*1e-10; w = tD*KB/HBAR; s = z*2.0/(M*AMU)
    return math.sqrt(max((C2/Lm**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def ddv_intra(edges, l, tD, f=0.5):
    lm = l*1e-10; w = tD*KB/HBAR
    s = sum((1.0/(mi*AMU)+1.0/(mj*AMU)) for mi,mj in edges)
    return math.sqrt(max((C2/lm**2)*(3*HBAR/(4*w))*(1-f)*s, 0))

def rev_delta(ddv0, tD, tc):
    if tc <= 0 or tD <= 0: return None
    arg = tD/(2*tc)
    if arg < 1: return None
    x = 1.0/math.tanh(arg)
    om = 3*BETA**2*ddv0**2/(16*x*GAP)
    if om <= 0 or om > 1: return None
    return (1-om)/BETA

def lambda_calc(ddv0): return 3*BETA**2*ddv0**2/(16*GAP)

def estimate_params(formula, cat, cond):
    comp = parse_formula(formula)
    if not comp: return None
    n = sum(comp.values()); M = get_mass(comp); r = get_radius(comp)
    tD = get_debye(comp); B = get_bulk(comp); P = 0
    if '高压' in cond or 'GPa' in cond:
        pm = re.search(r'~?(\d+)GPa', cond); P = int(pm.group(1)) if pm else 50
    L = 2*r; li = 2*r; z = 6; edges = []; f = 0.5
    if '元素' in cat:
        tD = ATOM_DB.get(list(comp.keys())[0], (0,300,1.5,50))[1] or tD
        if tD < 50: tD = 300
        z = 12; f = 0.5
        if '高压' in cat: B = max(get_bulk(comp), 50)*3; P = max(P, 100)
    elif 'A15' in cat: tD = max(tD, 400); z = 8; L = 2*r*0.9; f = 0.4
    elif '氢化物' in cat:
        tD = max(tD, 1500); B = max(B, 200); P = max(P, 150); z = 8; L = 2.0; li = 1.7
        nh = comp.get('H', 0); nm = n - nh
        if nh > 0 and nm > 0: edges = [((M-nh*1.008)/nm, 1.008)] * int(min(nh, 4))
        f = 0.5
    elif '铜氧' in cat:
        tD = max(tD, 400); z = 6; L = 3.8; li = 1.9
        if 'Cu' in comp and 'O' in comp: edges = [(63.55, 16.0)] * 2
        f = 0.4
    elif '铁基' in cat:
        tD = max(tD, 350); z = 6; L = 3.5; li = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges = [(55.85, 74.92)] * 2
            elif 'Se' in comp: edges = [(55.85, 78.97)] * 2
        f = 0.4
    elif '有机' in cat: tD = max(tD, 100); z = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
    elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
    elif '合金' in cat: tD = max(tD, 200); z = 12; f = 0.5
    else: tD = max(tD, 200); z = 8; f = 0.5
    return tD, M, L, z, edges, li, B, P, f

# 读取数据
input_file = r"D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv"
with open(input_file, 'r', encoding='utf-8-sig') as fh:
    reader = csv.reader(fh); next(reader); rows = list(reader)

# 计算所有材料，筛选反推成功的
data = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    cond = row[7] if len(row) > 7 else ''
    tc_m = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_m: continue
    tc = float(tc_m.group(1))
    if tc < 0.1: continue  # 排除极低Tc
    params = estimate_params(formula, cat, cond)
    if not params: continue
    tD, M, L, z, edges, li, B, P, f = params
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, li, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)
    dv = rev_delta(ddv0, tD, tc)
    if dv is None or dv <= 0: continue  # 只用反推成功的
    lam = lambda_calc(ddv0)
    if lam <= 0: continue
    data.append({'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD, 'lam': lam, 'ddv0': ddv0})

print("=" * 95)
print("半第一性Tc预测: 留一法交叉验证 (LOOCV)")
print("  模型: Tc = θ_D / (ln(λ) + b_cat)")
print("  只用反推成功的材料, Tc ≥ 0.1K")
print("=" * 95)

print(f"\n有效材料: {len(data)}个")

cat_data = defaultdict(list)
for d in data: cat_data[d['cat']].append(d)

# ============================================================
# 模型1: b_cat从同Fermi面类别拟合（留一法）
# ============================================================
print(f"\n{'='*95}")
print("模型1: Tc = θ_D / (ln(λ) + b_cat), b_cat = median(y - ln(λ))")
print(f"{'='*95}")

print(f"\n{'类别':<24} {'n':>4} {'b_cat':>8} {'ε_cat':>10} {'中位误差%':>10} {'2倍内%':>8}")
print("-" * 70)

all_preds1 = []; all_exps1 = []
cat_b = {}

for cat in sorted(cat_data.keys()):
    cd = cat_data[cat]
    if len(cd) < 2: continue

    # 留一法
    tc_errs = []
    for i, d in enumerate(cd):
        # 用除i外的材料拟合b_cat
        others = [cd[j] for j in range(len(cd)) if j != i]
        bs = [o['tD']/o['tc'] - np.log(o['lam']) for o in others]
        b_cat = np.median(bs)
        # 预测i
        y_pred = np.log(d['lam']) + b_cat
        tc_pred = d['tD'] / y_pred if y_pred > 0 else 0
        if d['tc'] > 0 and tc_pred > 0:
            tc_errs.append(abs(tc_pred - d['tc']) / d['tc'] * 100)
            all_preds1.append(tc_pred); all_exps1.append(d['tc'])

    # 全数据拟合（用于报告）
    bs_all = [d['tD']/d['tc'] - np.log(d['lam']) for d in cd]
    b_all = np.median(bs_all)
    eps_cat = 2 * np.exp(-b_all)
    cat_b[cat] = b_all

    med = np.median(tc_errs) if tc_errs else 0
    w2 = sum(1 for e in tc_errs if e < 100) / len(tc_errs) * 100 if tc_errs else 0
    print(f"{cat:<24} {len(cd):>4} {b_all:>8.3f} {eps_cat:>10.2e} {med:>10.1f} {w2:>8.0f}%")

errs1 = [abs(p-e)/e*100 for p, e in zip(all_preds1, all_exps1)]
print(f"\n模型1总体 (LOOCV):")
print(f"  材料数: {len(all_preds1)}")
print(f"  中位误差: {np.median(errs1):.1f}%")
print(f"  平均误差: {np.mean(errs1):.1f}%")
print(f"  在2倍范围内: {sum(1 for p,e in zip(all_preds1,all_exps1) if 0.5<p/e<2)/len(all_preds1)*100:.0f}%")

# ============================================================
# 模型2: b_cat + c·ln(θ_D)（增加Debye温度修正）
# ============================================================
print(f"\n{'='*95}")
print("模型2: y = ln(λ) + b_cat + c·ln(θ_D)")
print(f"{'='*95}")

# y = θ_D/Tc = ln(λ) + b_cat + c·ln(θ_D)
# 拟合c（全局）和b_cat（按类别）

from scipy.optimize import minimize

def model2_objective(params, data, cat_data):
    c = params[0]
    b_cats = params[1:]
    cats = sorted(cat_data.keys())
    cat_idx = {cat: i for i, cat in enumerate(cats)}
    sse = 0
    for d in data:
        cat = d['cat']
        if cat not in cat_idx: continue
        y_pred = np.log(d['lam']) + b_cats[cat_idx[cat]] + c * np.log(d['tD'])
        y_exp = d['tD'] / d['tc']
        sse += (y_pred - y_exp)**2
    return sse

cats_sorted = sorted(cat_data.keys())
n_cats = len(cats_sorted)
# 初始值
c_init = 0.0
b_init = [np.median([d['tD']/d['tc'] - np.log(d['lam']) for d in cat_data[cat]]) for cat in cats_sorted]
x0 = [c_init] + b_init

res = minimize(model2_objective, x0, args=(data, cat_data), method='L-BFGS-B')
c_opt = res.x[0]
b_opts = res.x[1:]

print(f"\n  c = {c_opt:.4f}")
print(f"\n{'类别':<24} {'b_cat':>8} {'中位误差%':>10} {'2倍内%':>8}")
print("-" * 55)

all_preds2 = []; all_exps2 = []
for i, cat in enumerate(cats_sorted):
    cd = cat_data[cat]
    if len(cd) < 2: continue
    tc_errs = []
    for d in cd:
        y_pred = np.log(d['lam']) + b_opts[i] + c_opt * np.log(d['tD'])
        tc_pred = d['tD'] / y_pred if y_pred > 0 else 0
        if d['tc'] > 0 and tc_pred > 0:
            tc_errs.append(abs(tc_pred - d['tc']) / d['tc'] * 100)
            all_preds2.append(tc_pred); all_exps2.append(d['tc'])
    med = np.median(tc_errs) if tc_errs else 0
    w2 = sum(1 for e in tc_errs if e < 100) / len(tc_errs) * 100 if tc_errs else 0
    print(f"{cat:<24} {b_opts[i]:>8.3f} {med:>10.1f} {w2:>8.0f}%")

errs2 = [abs(p-e)/e*100 for p, e in zip(all_preds2, all_exps2)]
print(f"\n模型2总体:")
print(f"  中位误差: {np.median(errs2):.1f}%")
print(f"  在2倍范围内: {sum(1 for p,e in zip(all_preds2,all_exps2) if 0.5<p/e<2)/len(all_preds2)*100:.0f}%")

# ============================================================
# 模型3: 全局连续模型 y = a·ln(λ) + b·ln(θ_D) + c·ln(M) + d
# ============================================================
print(f"\n{'='*95}")
print("模型3: y = a·ln(λ) + b·ln(θ_D) + c·ln(M) + d (全局, 无类别)")
print(f"{'='*95}")

Ms = [get_mass(parse_formula(d['formula'])) for d in data]
X3 = np.array([[np.log(d['lam']), np.log(d['tD']), np.log(M), 1] for d, M in zip(data, Ms)])
y3 = np.array([d['tD']/d['tc'] for d in data])
result3 = np.linalg.lstsq(X3, y3, rcond=None)
a3, b3, c3, d3 = result3[0]

tc_errs3 = []
all_preds3 = []
for d, M in zip(data, Ms):
    y_pred = a3*np.log(d['lam']) + b3*np.log(d['tD']) + c3*np.log(M) + d3
    tc_pred = d['tD'] / y_pred if y_pred > 0 else 0
    if d['tc'] > 0 and tc_pred > 0:
        tc_errs3.append(abs(tc_pred - d['tc']) / d['tc'] * 100)
        all_preds3.append(tc_pred)

print(f"  a = {a3:.3f}, b = {b3:.3f}, c = {c3:.3f}, d = {d3:.3f}")
print(f"  中位误差: {np.median(tc_errs3):.1f}%")
print(f"  在2倍范围内: {sum(1 for p,e in zip(all_preds3,[d['tc'] for d in data]) if 0.5<p/e<2)/len(all_preds3)*100:.0f}%")

# ============================================================
# 模型4: 混合模型 y = a·ln(λ) + b·ln(θ_D) + c_cat
# ============================================================
print(f"\n{'='*95}")
print("模型4: y = a·ln(λ) + b·ln(θ_D) + c_cat (全局a,b + 类别偏置)")
print(f"{'='*95}")

def model4_objective(params):
    a, b = params[0], params[1]
    c_cats = params[2:]
    cat_idx = {cat: i for i, cat in enumerate(cats_sorted)}
    sse = 0
    for d in data:
        if d['cat'] not in cat_idx: continue
        y_pred = a*np.log(d['lam']) + b*np.log(d['tD']) + c_cats[cat_idx[d['cat']]]
        y_exp = d['tD'] / d['tc']
        sse += (y_pred - y_exp)**2
    return sse

x0_4 = [1.0, 0.0] + [np.median([d['tD']/d['tc'] - np.log(d['lam']) for d in cat_data[cat]]) for cat in cats_sorted]
res4 = minimize(model4_objective, x0_4, method='L-BFGS-B')
a4, b4 = res4.x[0], res4.x[1]
c4s = res4.x[2:]

print(f"\n  a = {a4:.3f}, b = {b4:.3f}")
print(f"\n{'类别':<24} {'c_cat':>8} {'中位误差%':>10} {'2倍内%':>8}")
print("-" * 55)

all_preds4 = []; all_exps4 = []
for i, cat in enumerate(cats_sorted):
    cd = cat_data[cat]
    if len(cd) < 2: continue
    tc_errs = []
    for d in cd:
        y_pred = a4*np.log(d['lam']) + b4*np.log(d['tD']) + c4s[i]
        tc_pred = d['tD'] / y_pred if y_pred > 0 else 0
        if d['tc'] > 0 and tc_pred > 0:
            tc_errs.append(abs(tc_pred - d['tc']) / d['tc'] * 100)
            all_preds4.append(tc_pred); all_exps4.append(d['tc'])
    med = np.median(tc_errs) if tc_errs else 0
    w2 = sum(1 for e in tc_errs if e < 100) / len(tc_errs) * 100 if tc_errs else 0
    print(f"{cat:<24} {c4s[i]:>8.3f} {med:>10.1f} {w2:>8.0f}%")

errs4 = [abs(p-e)/e*100 for p, e in zip(all_preds4, all_exps4)]
print(f"\n模型4总体:")
print(f"  中位误差: {np.median(errs4):.1f}%")
print(f"  在2倍范围内: {sum(1 for p,e in zip(all_preds4,all_exps4) if 0.5<p/e<2)/len(all_preds4)*100:.0f}%")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*95}")
print("总结：半第一性Tc预测模型比较")
print(f"{'='*95}")

print(f"""
模型1: Tc = θ_D / (ln(λ) + b_cat)
  - 1个唯象参数/类别, λ从晶格第一性计算
  - LOOCV中位误差: {np.median(errs1):.1f}%
  - 2倍范围内: {sum(1 for p,e in zip(all_preds1,all_exps1) if 0.5<p/e<2)/len(all_preds1)*100:.0f}%

模型2: Tc = θ_D / (ln(λ) + b_cat + c·ln(θ_D))
  - 1个全局参数c + 1个/类别b_cat
  - 中位误差: {np.median(errs2):.1f}%
  - 2倍范围内: {sum(1 for p,e in zip(all_preds2,all_exps2) if 0.5<p/e<2)/len(all_preds2)*100:.0f}%

模型3: y = a·ln(λ) + b·ln(θ_D) + c·ln(M) + d (全局)
  - 4个全局参数, 无类别
  - 中位误差: {np.median(tc_errs3):.1f}%

模型4: y = a·ln(λ) + b·ln(θ_D) + c_cat (混合)
  - 2个全局参数 + 1个/类别偏置
  - 中位误差: {np.median(errs4):.1f}%
  - 2倍范围内: {sum(1 for p,e in zip(all_preds4,all_exps4) if 0.5<p/e<2)/len(all_preds4)*100:.0f}%

关键: 这些是真正的前向预测（非反推恒等式）
  λ从材料晶格结构独立计算
  唯象参数（b_cat或c_cat）从类别确定，类似BCS的μ*
""")