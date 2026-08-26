"""
第一性预测链条补全：1-βδ_v与Δδ₀的标度关系

关键问题：从Tc反推的δ_v和第一性Δδ₀之间是否有标度关系？
  如果 1-βδ_v = K·Δδ₀^p，则可以从Δδ₀前向计算δ_v

从Tc公式: 1-βδ_v = 3β²Δδ₀²/(16·coth(θ_D/(2Tc))·GAP)
  当Tc << θ_D: coth ≈ 1, 1-βδ_v ≈ 3β²Δδ₀²/(16·GAP) ∝ Δδ₀² (p=2)
  但此时Tc = θ_D/(2·arccoth(x)), x = 常数, Tc ∝ θ_D (不依赖Δδ₀)
  与经验Tc ∝ θ_D·Δδ₀^0.7矛盾

需要数值验证实际标度关系
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0


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

def rev_delta_v(ddv0, theta_D, tc):
    u = theta_D / (2*tc)
    tanh_u = math.tanh(u)
    x = 1.0 / tanh_u
    one_minus_bdv = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if one_minus_bdv <= 0 or one_minus_bdv >= 1: return None
    return (1 - one_minus_bdv) / BETA

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
    dv = rev_delta_v(ddv0, tD, tc)
    if dv is None: continue
    one_minus_bdv = 1 - BETA * dv
    all_data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'ddv0': ddv0, 'delta_v': dv, 'one_minus_bdv': one_minus_bdv
    })

print(f"加载 {len(all_data)} 个材料")

# ============================================================
# 1. 标度关系 1-βδ_v vs Δδ₀
# ============================================================
print(f"\n{'='*90}")
print("1. 标度关系 1-βδ_v vs Δδ₀")
print("=" * 90)

ddv0s = np.array([d['ddv0'] for d in all_data])
ombdvs = np.array([d['one_minus_bdv'] for d in all_data])

# ln(1-βδ_v) = p·ln(Δδ₀) + ln(K)
log_ddv0 = np.log(ddv0s)
log_ombdv = np.log(ombdvs)

# 线性回归
A = np.vstack([log_ddv0, np.ones(len(log_ddv0))]).T
p_fit, logK_fit = np.linalg.lstsq(A, log_ombdv, rcond=None)[0]
K_fit = np.exp(logK_fit)

print(f"全局拟合: 1-βδ_v = {K_fit:.4f} · Δδ₀^{p_fit:.3f}")
print(f"  即 p = {p_fit:.3f}")

# R²
pred = p_fit * log_ddv0 + logK_fit
ss_res = np.sum((log_ombdv - pred)**2)
ss_tot = np.sum((log_ombdv - np.mean(log_ombdv))**2)
r2 = 1 - ss_res/ss_tot
print(f"  R² = {r2:.3f}")

# 残差
residuals = log_ombdv - pred
print(f"  残差标准差 = {np.std(residuals):.3f} (对数空间)")
print(f"  即 K的变异范围: ×{np.exp(np.std(residuals)):.2f}")

# ============================================================
# 2. 按类别拟合
# ============================================================
print(f"\n{'='*90}")
print("2. 按类别拟合 1-βδ_v = K_cat · Δδ₀^p_cat")
print("=" * 90)

cat_data = defaultdict(list)
for d in all_data: cat_data[d['cat']].append(d)

print(f"{'类别':<24} {'n':>4} {'p':>6} {'K':>8} {'R²':>6} {'残差σ':>6}")
print("-" * 60)

cat_params = {}
for cat in sorted(cat_data.keys(), key=lambda c: -len(cat_data[c])):
    cd = cat_data[cat]
    if len(cd) < 5: continue
    x = np.log(np.array([d['ddv0'] for d in cd]))
    y = np.log(np.array([d['one_minus_bdv'] for d in cd]))
    A_cat = np.vstack([x, np.ones(len(x))]).T
    try:
        p_c, logK_c = np.linalg.lstsq(A_cat, y, rcond=None)[0]
        pred_c = p_c * x + logK_c
        ss_r = np.sum((y - pred_c)**2)
        ss_t = np.sum((y - np.mean(y))**2)
        r2_c = 1 - ss_r/ss_t if ss_t > 0 else 0
        sig = np.std(y - pred_c)
        print(f"{cat:<24} {len(cd):>4} {p_c:>6.3f} {np.exp(logK_c):>8.4f} {r2_c:>6.3f} {sig:>6.3f}")
        cat_params[cat] = (p_c, np.exp(logK_c))
    except:
        pass

# ============================================================
# 3. 从标度关系前向计算Tc
# ============================================================
print(f"\n{'='*90}")
print("3. 从标度关系前向计算Tc")
print("=" * 90)
print("""
如果 1-βδ_v = K·Δδ₀^p, 则:
  x = 3β²Δδ₀²/(16·K·Δδ₀^p·GAP) = 3β²/(16·K·GAP) · Δδ₀^(2-p)
  Tc = θ_D/(2·arccoth(x))

  当x >> 1: Tc ≈ θ_D/x ∝ θ_D·Δδ₀^(p-2)
  当x ≈ 1: Tc ≈ θ_D/ln(2/(x-1)) (对数发散)
""")

# 用全局p, K前向计算
print(f"全局 p={p_fit:.3f}, K={K_fit:.4f}")
errs_global = []
for d in all_data:
    ombdv_pred = K_fit * d['ddv0']**p_fit
    x_pred = 3 * BETA**2 * d['ddv0']**2 / (16 * ombdv_pred * GAP)
    if x_pred > 1:
        tc_pred = d['tD'] / (2 * np.arctanh(1/x_pred))
    else:
        tc_pred = 0
    if tc_pred > 0:
        err = abs(tc_pred - d['tc']) / d['tc']
        errs_global.append(err)
    else:
        errs_global.append(1e10)

errs_global = np.array(errs_global)
print(f"  中位误差: {np.median(errs_global)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_global<1)/len(errs_global)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_global<4)/len(errs_global)*100:.0f}%")

# 用类别p, K前向计算
print(f"\n类别 p_cat, K_cat:")
errs_cat = []
for d in all_data:
    if d['cat'] in cat_params:
        p_c, K_c = cat_params[d['cat']]
    else:
        p_c, K_c = p_fit, K_fit
    ombdv_pred = K_c * d['ddv0']**p_c
    x_pred = 3 * BETA**2 * d['ddv0']**2 / (16 * ombdv_pred * GAP)
    if x_pred > 1:
        tc_pred = d['tD'] / (2 * np.arctanh(1/x_pred))
    else:
        tc_pred = 0
    if tc_pred > 0:
        err = abs(tc_pred - d['tc']) / d['tc']
        errs_cat.append(err)
    else:
        errs_cat.append(1e10)

errs_cat = np.array(errs_cat)
print(f"  中位误差: {np.median(errs_cat)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_cat<1)/len(errs_cat)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_cat<4)/len(errs_cat)*100:.0f}%")

# ============================================================
# 4. LOOCV
# ============================================================
print(f"\n{'='*90}")
print("4. LOOCV: 从标度关系前向预测Tc")
print("=" * 90)

all_preds_loo = []
all_exps_loo = []
for i, d_test in enumerate(all_data):
    cat = d_test['cat']
    train = [d for j,d in enumerate(all_data) if j != i and d['cat'] == cat]
    if len(train) < 5:
        train = [d for j,d in enumerate(all_data) if j != i]
    x_tr = np.log(np.array([d['ddv0'] for d in train]))
    y_tr = np.log(np.array([d['one_minus_bdv'] for d in train]))
    A_tr = np.vstack([x_tr, np.ones(len(x_tr))]).T
    try:
        p_tr, logK_tr = np.linalg.lstsq(A_tr, y_tr, rcond=None)[0]
        K_tr = np.exp(logK_tr)
        ombdv_pred = K_tr * d_test['ddv0']**p_tr
        x_pred = 3 * BETA**2 * d_test['ddv0']**2 / (16 * ombdv_pred * GAP)
        if x_pred > 1:
            tc_pred = d_test['tD'] / (2 * np.arctanh(1/x_pred))
        else:
            tc_pred = 0
        if tc_pred > 0:
            all_preds_loo.append(tc_pred)
            all_exps_loo.append(d_test['tc'])
    except:
        pass

errs_loo = np.abs(np.array(all_preds_loo) - np.array(all_exps_loo)) / np.array(all_exps_loo)
print(f"LOOCV: {len(errs_loo)}个材料")
print(f"  中位误差: {np.median(errs_loo)*100:.0f}%")
print(f"  2倍内: {np.sum(errs_loo<1)/len(errs_loo)*100:.0f}%")
print(f"  5倍内: {np.sum(errs_loo<4)/len(errs_loo)*100:.0f}%")

# ============================================================
# 5. 分析p的物理含义
# ============================================================
print(f"\n{'='*90}")
print("5. 标度关系分析")
print("=" * 90)
print(f"""
全局标度关系: 1-βδ_v = {K_fit:.4f} · Δδ₀^{p_fit:.3f}  (R²={r2:.3f})

从Tc公式精确推导:
  1-βδ_v = 3β²Δδ₀²/(16·coth(θ_D/(2Tc))·GAP)
  当Tc << θ_D: coth ≈ 1 + 2exp(-θ_D/Tc)
  1-βδ_v ≈ 3β²Δδ₀²/(16·GAP) · (1 - 2exp(-θ_D/Tc))
         ≈ {3*BETA**2/(16*GAP):.4f} · Δδ₀² · (1 - 2exp(-θ_D/Tc))

  理论p = 2, K = {3*BETA**2/(16*GAP):.4f}
  实际p = {p_fit:.3f}, K = {K_fit:.4f}

差异分析:
  理论p=2来自coth≈1近似(Tc<<θ_D)
  实际p={p_fit:.3f}偏离2，因为:
    1. coth≠1的修正: coth = 1 + 2exp(-θ_D/Tc)
    2. Tc本身依赖Δδ₀(自洽问题)
    3. 不同材料θ_D/Tc不同

  如果Tc ∝ θ_D·Δδ₀^a, 则 θ_D/Tc ∝ Δδ₀^(-a)
  exp(-θ_D/Tc) ∝ exp(-c/Δδ₀^a)
  1-βδ_v ∝ Δδ₀²·(1 - exp(-c/Δδ₀^a))
    当Δδ₀大: ≈ Δδ₀² (p→2)
    当Δδ₀小: ≈ Δδ₀²·exp(-c/Δδ₀^a) (p→2+某修正)

  实际p={p_fit:.3f} < 2，说明exp修正使p减小
""")

# 检查：不同Tc/θ_D范围的p
print("按Tc/θ_D分组检查p:")
for lo, hi in [(0, 0.02), (0.02, 0.05), (0.05, 0.1), (0.1, 0.3), (0.3, 1.0)]:
    subset = [d for d in all_data if lo <= d['tc']/d['tD'] < hi]
    if len(subset) < 5: continue
    x = np.log(np.array([d['ddv0'] for d in subset]))
    y = np.log(np.array([d['one_minus_bdv'] for d in subset]))
    A_s = np.vstack([x, np.ones(len(x))]).T
    try:
        p_s, _ = np.linalg.lstsq(A_s, y, rcond=None)[0]
        print(f"  Tc/θ_D ∈ [{lo:.2f},{hi:.2f}): n={len(subset)}, p={p_s:.3f}")
    except:
        pass

# ============================================================
# 6. 关键问题：标度关系是数学恒等式还是物理关系？
# ============================================================
print(f"\n{'='*90}")
print("6. 标度关系是数学恒等式还是物理关系？")
print("=" * 90)
print(f"""
从Tc公式: 1-βδ_v = 3β²Δδ₀²/(16·coth(θ_D/(2Tc))·GAP)

如果Tc从实验知道(反推)，则1-βδ_v完全由Δδ₀和θ_D/Tc决定。
标度关系1-βδ_v ∝ Δδ₀^p来自coth(θ_D/(2Tc))的变化。

关键检验：如果标度关系是纯数学的(从Tc公式+实验Tc导出)，
则用标度关系前向计算Tc应该给出0%误差(恒等式)。

实际LOOCV误差={np.median(errs_loo)*100:.0f}%，说明:
  - 标度关系不是纯恒等式(有{np.median(errs_loo)*100:.0f}%误差)
  - 但也不是纯物理关系(因为δ_v从Tc反推)
  - 它是"半经验"关系：从训练集学习K,p，应用到测试集

要变成纯第一性，需要:
  从物理推导1-βδ_v = K·Δδ₀^p，不通过Tc反推
  即从Fermi面几何独立计算δ_v，验证1-βδ_v ∝ Δδ₀^p
""")