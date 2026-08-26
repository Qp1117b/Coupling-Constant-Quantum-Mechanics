"""
K_eff最优幂律分解搜索

当前: K_eff = K_0^cat · G^(-0.77) · θ_D^1.13, K_0跨15个数量级
目标: 找到最优分解 K_eff = K_0' · x1^a1 · x2^a2 · ...
      使K_0'的变异(标准差/均值)最小

搜索空间:
  K_eff = K_0' · Δδ₀^a · G^b · θ_D^c · l^d · M^e · Z^f · V^g · n_atoms^h

对每个候选分解:
  1. 计算K_0' = K_eff / (x1^a1 · x2^a2 · ...)
  2. 计算K_0'的变异系数(CV = std/mean)
  3. 按类别计算K_0'的类别内CV和类别间CV
  4. LOOCV验证Tc预测精度
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db

import csv, re, math
import numpy as np
from collections import defaultdict
from itertools import combinations

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)


def parse_formula(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def calc_all_params(formula):
    atoms = parse_formula(formula)
    if not atoms:
        return None
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    total_z = sum(atoms[el] * ATOM_DB[el][3] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_m = total_m / n_atoms
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
    V_cell = l**3
    f_corr = 1.0 - 0.3 * (1.0 - 1.0/n_atoms)
    edge_sum = 0
    els = list(atoms.keys())
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU
            mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            edge_sum += (1.0/mi + 1.0/mj)
    if not edge_sum:
        mi = total_m * AMU / n_atoms
        edge_sum = (n_atoms * (n_atoms-1) / 2) * 2.0 / mi
    G = (1.0/l) * math.sqrt((1.0 - f_corr) * edge_sum)
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3*HBAR / (4*omega_d)) * (1 - f_corr) * edge_sum
    dd0 = math.sqrt(abs(dd0_sq))
    # 体模量估计 (从θ_D和M)
    B_est = total_m * theta_d**2 * KB / V_cell * 1e-3
    return {
        'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d,
        'M': total_m, 'Z': total_z, 'V': V_cell,
        'n_atoms': n_atoms, 'B': B_est, 'avg_m': avg_m,
    }

# 加载数据
data = []
with open("superconductors_deduplicated.csv", 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try:
            tc = float(row['临界温度 Tc (K)'])
        except:
            continue
        if tc <= 0:
            continue
        mp = calc_all_params(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0:
            continue
        cat = row['类别']
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, **mp})

print(f"加载 {len(data)} 个材料")

# ============================================================
# 1. 全局最优幂律分解 (对数空间线性回归)
# ============================================================

print("\n" + "="*80)
print("1. 全局最优幂律分解: ln(K_eff) = Σ a_i · ln(x_i) + ln(K_0')")
print("="*80)

# 候选变量
VARS = ['dd0', 'G', 'tD', 'l', 'M', 'Z', 'V', 'n_atoms', 'B']
var_labels = {
    'dd0': 'Δδ₀', 'G': 'G', 'tD': 'θ_D', 'l': 'l', 'M': 'M',
    'Z': 'Z', 'V': 'V_cell', 'n_atoms': 'N', 'B': 'B'
}

# 全变量回归
X_full = np.column_stack([np.log(np.array([d[v] for d in data])) for v in VARS] + [np.ones(len(data))])
y = np.log(np.array([d['k_eff'] for d in data]))
coef_full, _, _, _ = np.linalg.lstsq(X_full, y, rcond=None)
y_pred = X_full @ coef_full
r2_full = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
k0_prime = np.exp(y - y_pred)
print(f"\n全变量回归 (9变量): R² = {r2_full:.3f}")
print(f"  K_0'范围: [{np.min(k0_prime):.4f}, {np.max(k0_prime):.4f}]")
print(f"  K_0'中位: {np.median(k0_prime):.4f}, CV: {np.std(k0_prime)/np.mean(k0_prime)*100:.0f}%")
print(f"  ln(K_0')标准差: {np.std(np.log(k0_prime)):.3f}")
print(f"  幂指数:")
for i, v in enumerate(VARS):
    print(f"    {var_labels[v]:>8}: {coef_full[i]:.4f}")

# ============================================================
# 2. 逐步回归: 找到最小K_0'变异的变量子集
# ============================================================

print("\n" + "="*80)
print("2. 逐步回归: 寻找最优变量子集")
print("="*80)

results = []
for n_vars in range(1, len(VARS) + 1):
    for combo in combinations(range(len(VARS)), n_vars):
        vars_subset = [VARS[i] for i in combo]
        X = np.column_stack([np.log(np.array([d[v] for d in data])) for v in vars_subset] + [np.ones(len(data))])
        coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
        y_pred = X @ coef
        r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
        k0p = np.exp(y - y_pred)
        ln_k0p = np.log(k0p)
        cv = np.std(ln_k0p)  # ln空间标准差
        results.append({
            'vars': vars_subset, 'r2': r2, 'cv': cv,
            'coef': coef, 'k0p_median': np.median(k0p),
        })

# 按R²排序
results.sort(key=lambda x: x['r2'], reverse=True)

print(f"\nTop 10 分解 (按R²排序):")
print(f"{'变量':>40} {'R²':>6} {'σ(ln K_0\')':>10} {'K_0\'中位':>10}")
print("-"*70)
for r in results[:10]:
    vars_str = "·".join(var_labels[v] for v in r['vars'])
    print(f"{vars_str:>40} {r['r2']:>6.3f} {r['cv']:>10.3f} {r['k0p_median']:>10.4f}")

# ============================================================
# 3. 最优分解的详细分析
# ============================================================

best = results[0]
print(f"\n最优分解: K_eff = K_0' · " + " · ".join(f"{var_labels[v]}^({best['coef'][i]:.3f})" for i, v in enumerate(best['vars'])))
print(f"R² = {best['r2']:.3f}, σ(ln K_0') = {best['cv']:.3f}")

# 计算K_0'的类别分布
X_best = np.column_stack([np.log(np.array([d[v] for d in data])) for v in best['vars']] + [np.ones(len(data))])
y_pred_best = X_best @ best['coef']
k0p_best = np.exp(y - y_pred_best)

for d, k0p in zip(data, k0p_best):
    d['k0p'] = k0p

print(f"\nK_0'的类别分布:")
cat_data = defaultdict(list)
for d in data:
    cat_data[d['cat']].append(d['k0p'])

print(f"{'类别':<28} {'n':>4} {'K_0\'中位':>10} {'σ(ln K_0\')':>10} {'CV%':>6}")
print("-"*70)
for cat in sorted(cat_data.keys()):
    k0ps = np.array(cat_data[cat])
    ln_k0ps = np.log(k0ps)
    cv = np.std(ln_k0ps)
    print(f"{cat:<28} {len(k0ps):>4} {np.median(k0ps):>10.4f} {cv:>10.3f} {np.std(k0ps)/np.mean(k0ps)*100:>6.0f}%")

# ============================================================
# 4. LOOCV: 最优分解→Tc
# ============================================================

print("\n" + "="*80)
print("4. LOOCV: 最优分解→Tc")
print("="*80)

# 全局K_0'中位数
errors_global = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    X_tr = np.column_stack([np.log(np.array([d[v] for d in train])) for v in best['vars']] + [np.ones(len(train))])
    y_tr = np.log(np.array([d['k_eff'] for d in train]))
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    # K_0'从训练集中位
    y_pred_tr = X_tr @ coef
    k0p_train = np.exp(y_tr - y_pred_tr)
    k0p_med = np.median(k0p_train)
    # 预测
    x_test = np.array([np.log(test[v]) for v in best['vars']] + [1.0])
    k_eff_pred = k0p_med * np.exp(x_test @ coef)
    tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
    err = abs(tc_pred - test['tc']) / test['tc']
    errors_global.append(err)

errors_global = np.array(errors_global)
print(f"全局K_0'中位数: 中位{np.median(errors_global)*100:.0f}%, 2倍内{np.mean(errors_global <= 1.0)*100:.0f}%, 5倍内{np.mean(errors_global <= 4.0)*100:.0f}%")

# 类别K_0'中位数
errors_cat = []
for i in range(len(data)):
    train = [data[j] for j in range(len(data)) if j != i]
    test = data[i]
    X_tr = np.column_stack([np.log(np.array([d[v] for d in train])) for v in best['vars']] + [np.ones(len(train))])
    y_tr = np.log(np.array([d['k_eff'] for d in train]))
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)
    y_pred_tr = X_tr @ coef
    # 按类别
    train_with_k0p = list(zip(train, np.exp(y_tr - y_pred_tr)))
    cat_train = [k0p for d, k0p in train_with_k0p if d['cat'] == test['cat']]
    k0p_med = np.median(cat_train) if cat_train else np.median([k0p for _, k0p in train_with_k0p])
    x_test = np.array([np.log(test[v]) for v in best['vars']] + [1.0])
    k_eff_pred = k0p_med * np.exp(x_test @ coef)
    tc_pred = math.sqrt(8 * test['dd0']**2 * k_eff_pred * test['tD'] / (9 * LN2))
    err = abs(tc_pred - test['tc']) / test['tc']
    errors_cat.append(err)

errors_cat = np.array(errors_cat)
print(f"类别K_0'中位数: 中位{np.median(errors_cat)*100:.0f}%, 2倍内{np.mean(errors_cat <= 1.0)*100:.0f}%, 5倍内{np.mean(errors_cat <= 4.0)*100:.0f}%")

# ============================================================
# 5. 对比: 当前分解 vs 最优分解
# ============================================================

print("\n" + "="*80)
print("5. 当前分解 vs 最优分解")
print("="*80)

# 当前分解: K_eff = K_0 · G^(-0.77) · θ_D^1.13
k0_current = np.array([d['k_eff'] / (d['G']**(-0.769) * d['tD']**1.132) for d in data])
ln_k0_current = np.log(k0_current)

print(f"当前分解 (G, θ_D):")
print(f"  σ(ln K_0) = {np.std(ln_k0_current):.3f}")
print(f"  K_0范围: [{np.min(k0_current):.2e}, {np.max(k0_current):.2e}] ({np.log(np.max(k0_current))-np.log(np.min(k0_current)):.1f}个数量级)")

print(f"\n最优分解 ({', '.join(var_labels[v] for v in best['vars'])}):")
print(f"  σ(ln K_0') = {best['cv']:.3f}")
print(f"  K_0'范围: [{np.min(k0p_best):.4f}, {np.max(k0p_best):.4f}] ({np.log(np.max(k0p_best))-np.log(np.min(k0p_best)):.1f}个数量级)")
print(f"  R² = {best['r2']:.3f}")

print(f"\n变异压缩: σ从{np.std(ln_k0_current):.3f}→{best['cv']:.3f} (压缩{np.std(ln_k0_current)/best['cv']:.1f}倍)")

# ============================================================
# 6. 2变量和3变量最优分解的详细展示
# ============================================================

print("\n" + "="*80)
print("6. 各变量数的最优分解")
print("="*80)

for n_vars in [1, 2, 3, 4, 5]:
    best_n = max([r for r in results if len(r['vars']) == n_vars], key=lambda x: x['r2'])
    vars_str = " · ".join(f"{var_labels[v]}^({best_n['coef'][i]:.3f})" for i, v in enumerate(best_n['vars']))
    print(f"\n{n_vars}变量: R²={best_n['r2']:.3f}, σ(ln K_0')={best_n['cv']:.3f}")
    print(f"  K_eff = K_0' · {vars_str}")

# ============================================================
# 7. 关键问题: 最优分解后K_0'是否还依赖类别?
# ============================================================

print("\n" + "="*80)
print("7. 最优分解后K_0'的类别依赖性")
print("="*80)

# ANOVA: 类别间变异 vs 类别内变异
cat_means = {}
cat_stds = {}
for cat in sorted(cat_data.keys()):
    k0ps = np.array(cat_data[cat])
    cat_means[cat] = np.mean(np.log(k0ps))
    cat_stds[cat] = np.std(np.log(k0ps))

# 类别间变异
between_var = np.var(list(cat_means.values()))
# 类别内变异（加权平均）
within_var = np.mean([s**2 for s in cat_stds.values()])
# 总变异
total_var = np.var(np.log(k0p_best))

print(f"类别间变异: {between_var:.3f}")
print(f"类别内变异: {within_var:.3f}")
print(f"总变异: {total_var:.3f}")
print(f"类别解释的变异比: {between_var/total_var*100:.1f}%")
print(f"→ K_0'{'仍强依赖类别' if between_var/total_var > 0.3 else '已不依赖类别'}")

# ============================================================
# 8. 总结
# ============================================================

print("\n" + "="*80)
print("8. 总结")
print("="*80)
print(f"""
最优幂律分解:
  K_eff = K_0' · {' · '.join(f'{var_labels[v]}^({best['coef'][i]:.3f})' for i, v in enumerate(best['vars']))}
  R² = {best['r2']:.3f}
  σ(ln K_0') = {best['cv']:.3f} (当前σ = {np.std(ln_k0_current):.3f})

变异压缩: {np.std(ln_k0_current)/best['cv']:.1f}倍
数量级跨度: 从{np.log(np.max(k0_current))-np.log(np.min(k0_current)):.1f}→{np.log(np.max(k0p_best))-np.log(np.min(k0p_best)):.1f}

K_0'的类别依赖: 类别解释{between_var/total_var*100:.1f}%变异

LOOCV:
  全局K_0'中位数: 中位{np.median(errors_global)*100:.0f}%
  类别K_0'中位数: 中位{np.median(errors_cat)*100:.0f}%

结论:
  1. 最优分解将K_0'的变异从σ={np.std(ln_k0_current):.2f}压缩到σ={best['cv']:.2f}
  2. K_0'仍{('强依赖类别' if between_var/total_var > 0.3 else '弱依赖类别')}({between_var/total_var*100:.0f}%变异来自类别间)
  3. {'需要更多变量或非幂律关系' if best['cv'] > 1.0 else '幂律分解已接近最优'}
  4. 进一步改进需要非幂律关系或额外变量(如DFT量)
""")