"""
从226个材料反推δ_v，寻找与材料参数的经验关系

思路：
  Tc = θ_D / (2·arccoth(x)), x = 3β²Δδ₀²/(16(1-βδ_v)·GAP)
  反推: δ_v = (1 - 3β²Δδ₀²/(16·x·GAP)) / β, x = coth(θ_D/(2Tc))

  关键量: ε = λ + βδ_v - 1 (到临界点距离)
  Tc = θ_D / ln(2λ/ε)

  如果ε能从材料参数预测，就能前向预测Tc。

  探索ε与以下参数的关系:
    - Δδ₀ (晶格涨落)
    - θ_D (Debye温度)
    - M (原子质量)
    - L (晶格常数)
    - 结构类型
    - 类别
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

import csv
import re
import math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
GAP = 21.022040 - 14.134725
C2 = 2.0 / 3.0
DELTA_C = 1.0 / BETA

ATOM_DB['Hg'] = (200.59, 0, 1.51, 25)  # 修正Hg

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

def ddv_inter(M, L, tD, z, f=0.5):
    L_m = L * 1e-10; w = tD * KB / HBAR; s = z * 2.0 / (M * AMU)
    return math.sqrt(max((C2/L_m**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))

def ddv_intra(edges, l, tD, f=0.5):
    l_m = l * 1e-10; w = tD * KB / HBAR
    s = sum((1.0/(mi*AMU) + 1.0/(mj*AMU)) for mi, mj in edges)
    return math.sqrt(max((C2/l_m**2) * (3*HBAR/(4*w)) * (1-f) * s, 0))

def rev_delta(ddv0, tD, tc):
    if tc <= 0 or tD <= 0: return None
    arg = tD / (2*tc)
    if arg < 1: return None
    x = 1.0 / math.tanh(arg)
    om = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if om <= 0 or om > 1: return None
    return (1 - om) / BETA

def lambda_calc(ddv0):
    return 3 * BETA**2 * ddv0**2 / (16 * GAP)

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
        tD = ATOM_DB.get(list(comp.keys())[0], (0, 300, 1.5, 50))[1] or tD
        if tD < 50: tD = 300
        z = 12; f = 0.5
        if '高压' in cat:
            B = max(get_bulk(comp), 50) * 3; P = max(P, 100)
    elif 'A15' in cat: tD = max(tD, 400); z = 8; L = 2*r*0.9; f = 0.4
    elif '氢化物' in cat:
        tD = max(tD, 1500); B = max(B, 200); P = max(P, 150); z = 8; L = 2.0; l_intra = 1.7
        n_h = comp.get('H', 0); n_m = n_atoms - n_h
        if n_h > 0 and n_m > 0:
            m_m = (M - n_h*1.008)/n_m; edges = [(m_m, 1.008)] * int(min(n_h, 4))
        f = 0.5
    elif '铜氧' in cat:
        tD = max(tD, 400); z = 6; L = 3.8; l_intra = 1.9
        if 'Cu' in comp and 'O' in comp: edges = [(63.55, 16.0)] * 2
        f = 0.4
    elif '铁基' in cat:
        tD = max(tD, 350); z = 6; L = 3.5; l_intra = 2.0
        if 'Fe' in comp:
            if 'As' in comp: edges = [(55.85, 74.92)] * 2
            elif 'Se' in comp: edges = [(55.85, 78.97)] * 2
        f = 0.4
    elif '有机' in cat: tD = max(tD, 100); z = 4; L = 5.0; f = 0.5
    elif '富勒烯' in cat: tD = 100; z = 4; L = 10.0; M = 720; f = 0.5
    elif '石墨' in cat: tD = 200; z = 3; L = 3.35; f = 0.5
    elif '合金' in cat: tD = max(tD, 200); z = 12; f = 0.5
    else: tD = max(tD, 200); z = 8; f = 0.5
    return tD, M, L, z, edges, l_intra, B, P, f

# ============================================================
# 读取数据
# ============================================================
input_file = r"D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv"

with open(input_file, 'r', encoding='utf-8-sig') as fh:
    reader = csv.reader(fh)
    header = next(reader)
    rows = list(reader)

print(f"读取 {len(rows)} 条记录")

# ============================================================
# 计算每个材料的ε和λ
# ============================================================
data = []
for row in rows:
    cat = row[0]; formula = row[1]; tc_str = row[3]
    condition = row[7] if len(row) > 7 else ''
    tc_match = re.match(r'~?(\d+\.?\d*)', tc_str.strip())
    if not tc_match: continue
    tc = float(tc_match.group(1))
    params = estimate_params(formula, cat, condition)
    if not params: continue
    tD, M, L, z, edges, l_intra, B, P, f = params
    dp = P / (3*B) if B > 0 else 0
    di = ddv_inter(M, L, tD, z, f)
    dn = ddv_intra(edges, l_intra, tD, f) if edges else 0
    ddv0 = math.sqrt(di**2 + dn**2)
    dv = rev_delta(ddv0, tD, tc)
    if dv is None or dv <= 0: continue
    lam = lambda_calc(ddv0)
    eps = lam + BETA * dv - 1  # 到临界点距离
    if eps <= 0: continue
    # ln(2λ/ε) = θ_D/Tc
    y = tD / tc  # = ln(2λ/ε)
    data.append({
        'formula': formula, 'cat': cat, 'tc': tc, 'tD': tD,
        'M': M, 'L': L, 'z': z, 'ddv0': ddv0, 'lam': lam,
        'dv': dv, 'eps': eps, 'y': y, 'P': P, 'B': B,
        'n_atoms': sum(parse_formula(formula).values()),
    })

print(f"有效数据: {len(data)}个")

# ============================================================
# 分析1: y = θ_D/Tc 与材料参数的关系
# ============================================================
print("\n" + "=" * 90)
print("分析1: y = θ_D/Tc 与材料参数的关系")
print("  Tc = θ_D/y, 如果y能从材料参数预测，就能前向预测Tc")
print("=" * 90)

# y = ln(2λ/ε) = ln(2λ) - ln(ε)
# 如果 ε = α·g(材料), 则 y = ln(2λ) - ln(α) - ln(g)

# 先看y的分布
ys = [d['y'] for d in data]
print(f"\ny = θ_D/Tc 统计:")
print(f"  范围: {min(ys):.1f} - {max(ys):.1f}")
print(f"  中位数: {np.median(ys):.1f}")
print(f"  均值: {np.mean(ys):.1f}")

# 按类别看y
cat_ys = defaultdict(list)
for d in data:
    cat_ys[d['cat']].append(d['y'])

print(f"\n按类别:")
print(f"{'类别':<24} {'数量':>4} {'y中位':>7} {'y范围':>15}")
for cat in sorted(cat_ys.keys()):
    ys_c = cat_ys[cat]
    print(f"{cat:<24} {len(ys_c):>4} {np.median(ys_c):>7.1f} {min(ys_c):>7.1f}-{max(ys_c):.1f}")

# ============================================================
# 分析2: y与ln(λ)的关系
# ============================================================
print("\n" + "=" * 90)
print("分析2: y vs ln(λ)")
print("=" * 90)

# y = ln(2λ/ε) = ln(2) + ln(λ) - ln(ε)
# 如果ε = const, 则 y = ln(2) + ln(λ) - ln(const) = ln(λ) + const
# y与ln(λ)线性关系，斜率1

ln_lams = [np.log(d['lam']) for d in data]
print(f"\ny vs ln(λ) 相关性:")
corr = np.corrcoef(ys, ln_lams)[0, 1]
print(f"  相关系数: {corr:.4f}")

# 线性拟合 y = a·ln(λ) + b
A = np.vstack([ln_lams, np.ones(len(ln_lams))]).T
a, b = np.linalg.lstsq(A, ys, rcond=None)[0]
residuals = ys - (a * np.array(ln_lams) + b)
rmse = np.sqrt(np.mean(residuals**2))
print(f"  y = {a:.3f}·ln(λ) + {b:.3f}")
print(f"  RMSE = {rmse:.1f}")
print(f"  如果斜率≈1且RMSE小，则ε≈const")

# ============================================================
# 分析3: ε与材料参数的关系
# ============================================================
print("\n" + "=" * 90)
print("分析3: ε与材料参数的关系")
print("=" * 90)

eps_vals = [d['eps'] for d in data]
print(f"\nε统计:")
print(f"  范围: {min(eps_vals):.2e} - {max(eps_vals):.2e}")
print(f"  跨越: {max(eps_vals)/min(eps_vals):.0e}个数量级")

# ln(ε)与材料参数
ln_eps = [np.log(d['eps']) for d in data]
params_to_test = {
    'ln(Δδ₀)': [np.log(d['ddv0']) for d in data],
    'ln(λ)': ln_lams,
    'ln(θ_D)': [np.log(d['tD']) for d in data],
    'ln(M)': [np.log(d['M']) for d in data],
    'ln(L)': [np.log(d['L']) for d in data],
    'θ_D/Tc': ys,
    'ln(P+1)': [np.log(d['P']+1) for d in data],
}

print(f"\nln(ε)与各参数相关性:")
print(f"{'参数':<12} {'相关系数':>10}")
for name, vals in params_to_test.items():
    c = np.corrcoef(ln_eps, vals)[0, 1]
    print(f"{name:<12} {c:>10.4f}")

# ============================================================
# 分析4: 关键关系 y = θ_D/Tc 与 λ 和 类别
# ============================================================
print("\n" + "=" * 90)
print("分析4: y = θ_D/Tc 的预测模型")
print("=" * 90)

# y = ln(2λ/ε)
# 如果 ε = α_cat · λ^γ (按类别不同的α)
# 则 y = ln(2λ/(α_cat·λ^γ)) = ln(2/α_cat) + (1-γ)·ln(λ)

# 按类别拟合 y = a·ln(λ) + b
print(f"\n按类别拟合 y = a·ln(λ) + b:")
print(f"{'类别':<24} {'n':>4} {'a':>6} {'b':>8} {'RMSE':>7} {'Tc误差%':>8}")
print("-" * 65)

cat_models = {}
for cat in sorted(cat_ys.keys()):
    cat_data = [d for d in data if d['cat'] == cat]
    if len(cat_data) < 3: continue
    ys_c = [d['y'] for d in cat_data]
    lls_c = [np.log(d['lam']) for d in cat_data]
    A = np.vstack([lls_c, np.ones(len(lls_c))]).T
    result = np.linalg.lstsq(A, ys_c, rcond=None)
    a_c, b_c = result[0]
    res = np.array(ys_c) - (a_c * np.array(lls_c) + b_c)
    rmse_c = np.sqrt(np.mean(res**2))

    # 前向Tc误差
    tc_errors = []
    for d in cat_data:
        y_pred = a_c * np.log(d['lam']) + b_c
        tc_pred = d['tD'] / y_pred
        if d['tc'] > 0:
            tc_errors.append(abs(tc_pred - d['tc']) / d['tc'] * 100)

    med_err = np.median(tc_errors) if tc_errors else 0
    cat_models[cat] = (a_c, b_c)
    print(f"{cat:<24} {len(cat_data):>4} {a_c:>6.3f} {b_c:>8.3f} {rmse_c:>7.1f} {med_err:>8.1f}%")

# ============================================================
# 分析5: 全局模型 y = a·ln(λ) + b_cat（类别偏置）
# ============================================================
print("\n" + "=" * 90)
print("分析5: 全局模型 y = a·ln(λ) + b_cat")
print("=" * 90)

# 固定a=1（理论值），拟合每类别的b
print(f"\n固定a=1（理论y = ln(2λ/ε), ε=const/类）:")
print(f"{'类别':<24} {'n':>4} {'b':>8} {'ε=2e^(-b)':>10} {'Tc中位误差%':>12}")
print("-" * 65)

for cat in sorted(cat_ys.keys()):
    cat_data = [d for d in data if d['cat'] == cat]
    if len(cat_data) < 3: continue
    # y = ln(λ) + b → b = y - ln(λ) = ln(2/ε)
    bs = [d['y'] - np.log(d['lam']) for d in cat_data]
    b_med = np.median(bs)
    eps_cat = 2 * np.exp(-b_med)

    tc_errors = []
    for d in cat_data:
        y_pred = np.log(d['lam']) + b_med
        tc_pred = d['tD'] / y_pred
        if d['tc'] > 0:
            tc_errors.append(abs(tc_pred - d['tc']) / d['tc'] * 100)
    med_err = np.median(tc_errors) if tc_errors else 0
    print(f"{cat:<24} {len(cat_data):>4} {b_med:>8.3f} {eps_cat:>10.2e} {med_err:>12.1f}%")

# ============================================================
# 分析6: ε与Δδ₀的关系（关键！）
# ============================================================
print("\n" + "=" * 90)
print("分析6: ε与Δδ₀的关系")
print("=" * 90)

# ε = 2λ·exp(-θ_D/Tc)
# λ = 3β²Δδ₀²/(16·GAP) ∝ Δδ₀²
# ε = 2·(3β²/(16·GAP))·Δδ₀²·exp(-θ_D/Tc)

# 如果exp(-θ_D/Tc)与Δδ₀无关，则ε ∝ Δδ₀²
# 但exp(-θ_D/Tc)变化很大

# 看ε/λ = 2·exp(-θ_D/Tc)的分布
eps_over_lam = [d['eps']/d['lam'] for d in data]
print(f"\nε/λ = 2·exp(-θ_D/Tc) 统计:")
print(f"  范围: {min(eps_over_lam):.2e} - {max(eps_over_lam):.2e}")
print(f"  中位数: {np.median(eps_over_lam):.2e}")
print(f"  跨越: {max(eps_over_lam)/min(eps_over_lam):.0e}个数量级")

# ln(ε/λ) = ln(2) - θ_D/Tc
# 所以 θ_D/Tc = ln(2) - ln(ε/λ) = ln(2λ/ε) = y
# 这是恒等式

# 关键：θ_D/Tc能否从材料参数预测（不通过ε）？
# θ_D/Tc = y = ln(2λ/ε)
# 如果ε = f(材料)，则y = ln(2λ) - ln(f(材料))

# 尝试: ln(ε) = a·ln(Δδ₀) + b·ln(θ_D) + c
print(f"\n多元回归: ln(ε) = a·ln(Δδ₀) + b·ln(θ_D) + c")

X = np.array([[np.log(d['ddv0']), np.log(d['tD']), 1] for d in data])
y_vec = np.array(ln_eps)
result = np.linalg.lstsq(X, y_vec, rcond=None)
a, b, c = result[0]
res = y_vec - X @ result[0]
rmse = np.sqrt(np.mean(res**2))
print(f"  a = {a:.3f}, b = {b:.3f}, c = {c:.3f}")
print(f"  RMSE = {rmse:.2f}")

# 前向Tc
tc_errors = []
for d in data:
    ln_eps_pred = a * np.log(d['ddv0']) + b * np.log(d['tD']) + c
    eps_pred = np.exp(ln_eps_pred)
    y_pred = np.log(2 * d['lam'] / eps_pred)
    tc_pred = d['tD'] / y_pred
    if d['tc'] > 0 and tc_pred > 0:
        tc_errors.append(abs(tc_pred - d['tc']) / d['tc'] * 100)

print(f"  前向Tc中位误差: {np.median(tc_errors):.1f}%")
print(f"  前向Tc 90%误差: {np.percentile(tc_errors, 90):.1f}%")

# ============================================================
# 分析7: 最优模型搜索
# ============================================================
print("\n" + "=" * 90)
print("分析7: 最优模型搜索")
print("=" * 90)

# 尝试多种参数组合
param_combos = [
    ['ln(ddv0)', 'ln(tD)'],
    ['ln(ddv0)', 'ln(tD)', 'ln(M)'],
    ['ln(ddv0)', 'ln(tD)', 'ln(L)'],
    ['ln(ddv0)', 'ln(tD)', 'ln(P+1)'],
    ['ln(ddv0)', 'ln(tD)', 'ln(M)', 'ln(L)'],
    ['ln(lam)', 'ln(tD)'],
    ['ln(lam)', 'ln(tD)', 'ln(P+1)'],
]

def get_param(d, name):
    if name == 'ln(ddv0)': return np.log(d['ddv0'])
    if name == 'ln(tD)': return np.log(d['tD'])
    if name == 'ln(M)': return np.log(d['M'])
    if name == 'ln(L)': return np.log(d['L'])
    if name == 'ln(P+1)': return np.log(d['P']+1)
    if name == 'ln(lam)': return np.log(d['lam'])
    return 0

print(f"\n{'参数组合':<40} {'RMSE(ln ε)':>10} {'Tc中位误差%':>12} {'Tc 90%误差%':>12}")
print("-" * 80)

best_model = None
best_err = 1e10

for combo in param_combos:
    X = np.array([[get_param(d, p) for p in combo] + [1] for d in data])
    result = np.linalg.lstsq(X, y_vec, rcond=None)
    res = y_vec - X @ result[0]
    rmse = np.sqrt(np.mean(res**2))

    tc_errs = []
    for i, d in enumerate(data):
        ln_eps_pred = (X[i] @ result[0])
        eps_pred = np.exp(ln_eps_pred)
        y_pred = np.log(2 * d['lam'] / eps_pred)
        tc_pred = d['tD'] / y_pred
        if d['tc'] > 0 and tc_pred > 0:
            tc_errs.append(abs(tc_pred - d['tc']) / d['tc'] * 100)

    med = np.median(tc_errs)
    p90 = np.percentile(tc_errs, 90)
    combo_str = ", ".join(combo)
    print(f"{combo_str:<40} {rmse:>10.3f} {med:>12.1f} {p90:>12.1f}")

    if med < best_err:
        best_err = med
        best_model = (combo, result[0])

print(f"\n最佳模型: {', '.join(best_model[0])}")
print(f"  中位误差: {best_err:.1f}%")

# ============================================================
# 分析8: 按类别分别拟合
# ============================================================
print("\n" + "=" * 90)
print("分析8: 按类别分别拟合 ln(ε) = a·ln(Δδ₀) + b·ln(θ_D) + c")
print("=" * 90)

print(f"\n{'类别':<24} {'n':>4} {'a':>6} {'b':>6} {'c':>8} {'Tc中位误差%':>12}")
print("-" * 70)

all_preds = []
all_exps = []
for cat in sorted(cat_ys.keys()):
    cat_data = [d for d in data if d['cat'] == cat]
    if len(cat_data) < 5: continue
    X_c = np.array([[np.log(d['ddv0']), np.log(d['tD']), 1] for d in cat_data])
    y_c = np.array([np.log(d['eps']) for d in cat_data])
    result = np.linalg.lstsq(X_c, y_c, rcond=None)
    a_c, b_c, c_c = result[0]

    tc_errs = []
    for d in cat_data:
        ln_eps_pred = a_c * np.log(d['ddv0']) + b_c * np.log(d['tD']) + c_c
        eps_pred = np.exp(ln_eps_pred)
        y_pred = np.log(2 * d['lam'] / eps_pred)
        tc_pred = d['tD'] / y_pred
        if d['tc'] > 0 and tc_pred > 0:
            err = abs(tc_pred - d['tc']) / d['tc'] * 100
            tc_errs.append(err)
            all_preds.append(tc_pred)
            all_exps.append(d['tc'])

    med = np.median(tc_errs) if tc_errs else 0
    print(f"{cat:<24} {len(cat_data):>4} {a_c:>6.3f} {b_c:>6.3f} {c_c:>8.3f} {med:>12.1f}%")

if all_preds:
    all_errs = [abs(p-e)/e*100 for p, e in zip(all_preds, all_exps)]
    print(f"\n总体前向Tc预测:")
    print(f"  材料数: {len(all_preds)}")
    print(f"  中位误差: {np.median(all_errs):.1f}%")
    print(f"  平均误差: {np.mean(all_errs):.1f}%")
    print(f"  90%误差: {np.percentile(all_errs, 90):.1f}%")
    # 在2倍范围内的比例
    within_2x = sum(1 for p, e in zip(all_preds, all_exps) if 0.5 < p/e < 2) / len(all_preds)
    print(f"  在2倍范围内: {within_2x*100:.0f}%")