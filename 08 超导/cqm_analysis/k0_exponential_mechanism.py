"""
K_0与CQM指数机制的关系

幂律分解失败(R²=0.226)说明K_0不是材料参数的幂律函数。
K_0的15个数量级跨度可能来自指数机制:
1. 黎曼零点: K_0 ~ exp(a·γ_n)
2. Regge路径积分: K_0 ~ exp(-S_Regge/ℏ)
3. 丛和乐: K_0 ~ exp(i∮A)
4. BCS-like指数: K_0 ~ θ_D·exp(-1/λ)

检查K_0^cat是否能对应黎曼零点的指数。
"""

import csv, re, math
import numpy as np
from collections import defaultdict

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
LN2 = math.log(2)
C = math.sqrt(C2)

# 黎曼零点
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

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
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    atoms = {}
    for el, cnt in pairs:
        if el in ATOM_DB:
            atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def calc_params(formula):
    atoms = parse_formula(formula)
    if not atoms:
        return None
    total_m = sum(atoms[el] * ATOM_DB[el][0] for el in atoms)
    n_atoms = sum(atoms.values())
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in atoms) / n_atoms
    l = 2 * avg_r * 1e-10
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in atoms) / n_atoms
    if theta_d == 0:
        return None
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
    return {'l': l, 'G': G, 'dd0': dd0, 'tD': theta_d}

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
        mp = calc_params(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0:
            continue
        cat = row['类别']
        k_eff = tc**2 * 9 * LN2 / (8 * mp['dd0']**2 * mp['tD'])
        a_ke, b_ke = -0.769, 1.132
        k0 = k_eff / (mp['G']**a_ke * mp['tD']**b_ke)
        data.append({'cat': cat, 'tc': tc, 'k_eff': k_eff, 'k0': k0, **mp})

print(f"加载 {len(data)} 个材料")

# ============================================================
# 1. K_0^cat的值 vs 黎曼零点
# ============================================================

print("\n" + "="*80)
print("1. K_0^cat vs 黎曼零点")
print("="*80)

cat_data = defaultdict(list)
for d in data:
    cat_data[d['cat']].append(d['k0'])

cat_k0 = {}
for cat in cat_data:
    cat_k0[cat] = np.median(cat_data[cat])

print(f"{'类别':<28} {'ln K_0':>8} {'最近γ_n':>8} {'n':>3} {'ln K_0 / γ_n':>12} {'ln K_0 - γ_n':>12}")
print("-"*80)
cat_gamma_map = {}
for cat in sorted(cat_k0.keys()):
    ln_k0 = np.log(cat_k0[cat])
    # 找最近的黎曼零点
    diffs = [abs(ln_k0 - g) for g in RIEMANN_ZEROS]
    n_closest = np.argmin(diffs)
    gamma_closest = RIEMANN_ZEROS[n_closest]
    ratio = ln_k0 / gamma_closest
    diff = ln_k0 - gamma_closest
    cat_gamma_map[cat] = n_closest + 1
    print(f"{cat:<28} {ln_k0:>8.3f} {gamma_closest:>8.3f} {n_closest+1:>3} {ratio:>12.4f} {diff:>12.3f}")

# ============================================================
# 2. ln(K_0) = a·γ_n + b 的拟合
# ============================================================

print("\n" + "="*80)
print("2. ln(K_0) = a·γ_n + b 拟合")
print("="*80)

# 为每个类别分配一个γ_n
# 尝试: 按K_0排序，分配γ_1, γ_2, ...
sorted_cats = sorted(cat_k0.keys(), key=lambda c: np.log(cat_k0[c]))
n_cats = len(sorted_cats)

# 方案A: 按顺序分配γ_1到γ_n
print("\n方案A: 按K_0排序分配γ_1到γ_n")
gammas_A = RIEMANN_ZEROS[:n_cats]
ln_k0s = [np.log(cat_k0[cat]) for cat in sorted_cats]

X_A = np.column_stack([gammas_A, np.ones(n_cats)])
y = np.array(ln_k0s)
coef_A, _, _, _ = np.linalg.lstsq(X_A, y, rcond=None)
y_pred = X_A @ coef_A
r2_A = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
print(f"  a = {coef_A[0]:.4f}, b = {coef_A[1]:.4f}, R² = {r2_A:.3f}")

for i, cat in enumerate(sorted_cats):
    print(f"    {cat:<28} → γ_{i+1}={gammas_A[i]:.3f}, ln K_0={ln_k0s[i]:.3f}, pred={y_pred[i]:.3f}")

# 方案B: 用γ_n的间距
print("\n方案B: 用γ_n的间距(γ_{n+1}-γ_n)")
gamma_gaps = [RIEMANN_ZEROS[i+1] - RIEMANN_ZEROS[i] for i in range(n_cats-1)]
gamma_gaps_full = gamma_gaps + [gamma_gaps[-1]]  # 补齐

X_B = np.column_stack([gamma_gaps_full, np.ones(n_cats)])
coef_B, _, _, _ = np.linalg.lstsq(X_B, y, rcond=None)
y_pred_B = X_B @ coef_B
r2_B = 1 - np.sum((y - y_pred_B)**2) / np.sum((y - np.mean(y))**2)
print(f"  a = {coef_B[0]:.4f}, b = {coef_B[1]:.4f}, R² = {r2_B:.3f}")

# 方案C: 用γ_n²
print("\n方案C: ln(K_0) = a·γ_n² + b")
gammas_sq = [g**2 for g in gammas_A]
X_C = np.column_stack([gammas_sq, np.ones(n_cats)])
coef_C, _, _, _ = np.linalg.lstsq(X_C, y, rcond=None)
y_pred_C = X_C @ coef_C
r2_C = 1 - np.sum((y - y_pred_C)**2) / np.sum((y - np.mean(y))**2)
print(f"  a = {coef_C[0]:.6f}, b = {coef_C[1]:.4f}, R² = {r2_C:.3f}")

# ============================================================
# 3. K_0 ~ exp(a·γ_n)的直接验证
# ============================================================

print("\n" + "="*80)
print("3. K_0 ~ exp(a·γ_n)的直接验证")
print("="*80)

# 如果K_0 = C·exp(a·γ_n), 则ln(K_0) = ln(C) + a·γ_n
# 用方案A的拟合
a_fit = coef_A[0]
b_fit = coef_A[1]
print(f"拟合: ln(K_0) = {a_fit:.4f}·γ_n + {b_fit:.4f}")
print(f"即: K_0 = exp({b_fit:.4f})·exp({a_fit:.4f}·γ_n) = {math.exp(b_fit):.2e}·exp({a_fit:.4f}·γ_n)")
print(f"R² = {r2_A:.3f}")

# 验证: 用拟合参数预测K_0
print(f"\n验证:")
print(f"{'类别':<28} {'K_0实际':>12} {'K_0预测':>12} {'误差':>8}")
print("-"*65)
for i, cat in enumerate(sorted_cats):
    k0_actual = cat_k0[cat]
    k0_pred = math.exp(b_fit + a_fit * gammas_A[i])
    err = abs(k0_pred - k0_actual) / k0_actual
    print(f"{cat:<28} {k0_actual:>12.2e} {k0_pred:>12.2e} {err*100:>7.1f}%")

# ============================================================
# 4. BCS-like指数关系: K_0 ~ exp(-c/λ_eff)
# ============================================================

print("\n" + "="*80)
print("4. BCS-like指数: K_0 ~ θ_D·exp(-c/λ_eff)")
print("="*80)

# 从BCS公式反推λ_ep
# Tc = θ_D·exp(-1.04(1+λ)/(λ-μ*(1+0.62λ)))
# 简化: Tc ≈ θ_D·exp(-1/(λ-μ*)), μ*=0.1
MU_STAR = 0.1

for d in data:
    tc = d['tc']
    td = d['tD']
    if tc >= td:
        d['lambda_ep'] = None
        continue
    ratio = tc / td
    if ratio <= 0 or ratio >= 1:
        d['lambda_ep'] = None
        continue
    # -1/(λ-μ*) = ln(ratio) → λ = μ* - 1/ln(ratio)
    lam = MU_STAR - 1.0 / math.log(ratio)
    d['lambda_ep'] = lam if lam > 0 else None

valid = [d for d in data if d['lambda_ep'] is not None and d['lambda_ep'] > 0.01]
print(f"有效材料: {len(valid)}")

# 按类别计算λ_ep中位数
cat_lambda = defaultdict(list)
for d in valid:
    cat_lambda[d['cat']].append(d['lambda_ep'])

print(f"\n{'类别':<28} {'λ_ep中位':>8} {'ln K_0':>8} {'-1/λ_ep':>8} {'ln(K_0/θ_D)':>10}")
print("-"*70)
for cat in sorted(cat_k0.keys()):
    if cat in cat_lambda:
        lam_med = np.median(cat_lambda[cat])
        ln_k0 = np.log(cat_k0[cat])
        inv_lam = -1.0 / lam_med
        # ln(K_0/θ_D) 用类别中位θ_D
        tds = [d['tD'] for d in data if d['cat'] == cat]
        ln_k0_over_td = ln_k0 - np.log(np.median(tds))
        print(f"{cat:<28} {lam_med:>8.3f} {ln_k0:>8.3f} {inv_lam:>8.3f} {ln_k0_over_td:>10.3f}")

# ============================================================
# 5. K_0与1/λ_ep的指数关系
# ============================================================

print("\n" + "="*80)
print("5. ln(K_0) vs 1/λ_ep 回归")
print("="*80)

ln_k0_vals = []
inv_lam_vals = []
for d in valid:
    ln_k0_vals.append(np.log(d['k0']))
    inv_lam_vals.append(1.0 / d['lambda_ep'])

ln_k0_vals = np.array(ln_k0_vals)
inv_lam_vals = np.array(inv_lam_vals)

corr = np.corrcoef(inv_lam_vals, ln_k0_vals)[0, 1]
print(f"corr(ln K_0, 1/λ_ep) = {corr:.3f}")

# 回归: ln(K_0) = a/λ_ep + b
X = np.column_stack([inv_lam_vals, np.ones(len(inv_lam_vals))])
y = ln_k0_vals
coef, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
y_pred = X @ coef
r2 = 1 - np.sum((y - y_pred)**2) / np.sum((y - np.mean(y))**2)
print(f"ln(K_0) = {coef[0]:.3f}/λ_ep + {coef[1]:.3f}, R² = {r2:.3f}")
print(f"即: K_0 = exp({coef[1]:.3f})·exp({coef[0]:.3f}/λ_ep)")
print(f"    K_0 = {math.exp(coef[1]):.2e}·exp({coef[0]:.3f}/λ_ep)")

# ============================================================
# 6. 综合: K_0的CQM指数公式
# ============================================================

print("\n" + "="*80)
print("6. K_0的CQM指数公式候选")
print("="*80)

print(f"""
候选公式:
  A) K_0 = C·exp(a·γ_n)
     R² = {r2_A:.3f} (γ_n按类别排序分配)
     → {'有效' if r2_A > 0.7 else '无效'}

  B) K_0 = C·exp(a/λ_ep + b)
     R² = {r2:.3f}, corr = {corr:.3f}
     → {'有效' if r2 > 0.7 else '中等' if r2 > 0.3 else '无效'}

  C) K_0 = C·exp(a·γ_n² + b)
     R² = {r2_C:.3f}
     → {'有效' if r2_C > 0.7 else '无效'}

关键观察:
  - 黎曼零点指数(R²={r2_A:.3f}): {'可以' if r2_A > 0.5 else '不能'}解释K_0^cat变异
  - BCS-like指数(R²={r2:.3f}): {'可以' if r2 > 0.5 else '不能'}解释K_0^cat变异
  - 但1/λ_ep本身需要DFT计算...
""")

# ============================================================
# 7. 从CQM角度: 破缺能标的指数机制
# ============================================================

print("="*80)
print("7. 破缺能标的CQM指数机制")
print("="*80)

print("""
幂律分解失败(R²=0.226)证明K_0不是材料参数的幂律函数。
K_0的15个数量级跨度来自指数机制。

CQM中的指数机制:
  1. Regge路径积分: exp(-S_Regge/ℏ)
     S_Regge = Σ_h δ_h²/A_h (角亏作用量)
     → K_0 ~ exp(-c·Σ δ_h²/A_h)

  2. 丛和乐: exp(i∮A) → |hol| = exp(-∮Im(A))
     → K_0 ~ exp(-c·|F_A|·L²) (曲率×面积)

  3. 黎曼零点渐近: γ_n ~ 2πn/ln(n/2π)
     → K_0 ~ exp(a·γ_n) (零点指数)

  4. 破缺能标: Λ_break ~ exp(-c/g²) (非微扰)
     → K_0 ~ exp(-c/g²_CQM)

BCS-like指数(R²=""" + f"{r2:.3f}" + """)是最强的经验关系,
但1/λ_ep需要DFT计算。

CQM替代方案: 从Regge作用量直接计算指数
  S_Regge = Σ_h δ_h²/A_h
  K_0 ~ exp(-c·S_Regge)

  这需要具体的Regge剖分参数(δ_h, A_h),
  不需要DFT但需要晶格几何细节。
""")

# ============================================================
# 8. 尝试: K_0 ~ exp(-c·S_Regge) 从已有几何量估计
# ============================================================

print("="*80)
print("8. K_0 ~ exp(-c·S_Regge) 检验")
print("="*80)

# S_Regge ~ Σ δ_h²/A_h ~ Δδ₀²/l² (角亏涨落/面积)
# 但Δδ₀已经在K_eff公式中用了...
# 尝试: S_Regge ~ 1/(Δδ₀²·l²) 或 S_Regge ~ G²/Δδ₀²

# 检查 ln(K_0) vs 各种几何量的指数
geo_vars = {
    '1/Δδ₀²': np.array([1.0/d['dd0']**2 for d in data]),
    '1/(Δδ₀²·l²)': np.array([1.0/(d['dd0']**2 * d['l']**2) for d in data]),
    'G²/Δδ₀²': np.array([d['G']**2/d['dd0']**2 for d in data]),
    '1/G²': np.array([1.0/d['G']**2 for d in data]),
    'l/Δδ₀': np.array([d['l']/d['dd0'] for d in data]),
    'θ_D/Δδ₀²': np.array([d['tD']/d['dd0']**2 for d in data]),
}

ln_k0_all = np.array([np.log(d['k0']) for d in data])

print(f"{'几何量':>14} {'corr(ln K_0, ln量)':>18} {'corr(ln K_0, 量)':>18}")
print("-"*55)
for name, vals in geo_vars.items():
    corr_log = np.corrcoef(np.log(vals), ln_k0_all)[0, 1]
    corr_lin = np.corrcoef(vals, ln_k0_all)[0, 1]
    print(f"{name:>14} {corr_log:>18.3f} {corr_lin:>18.3f}")

# 最强的关系
print(f"\n最强幂律关系: ", end="")
best_corr = 0
best_name = ""
for name, vals in geo_vars.items():
    corr = abs(np.corrcoef(np.log(vals), ln_k0_all)[0, 1])
    if corr > best_corr:
        best_corr = corr
        best_name = name
print(f"{best_name}, |corr| = {best_corr:.3f}")

print(f"\n最强线性(指数)关系: ", end="")
best_corr = 0
best_name = ""
for name, vals in geo_vars.items():
    corr = abs(np.corrcoef(vals, ln_k0_all)[0, 1])
    if corr > best_corr:
        best_corr = corr
        best_name = name
print(f"{best_name}, |corr| = {best_corr:.3f}")