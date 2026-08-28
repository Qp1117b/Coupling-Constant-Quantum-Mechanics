"""用理论C_GAMMA = e^(1/beta) * alpha_fs^3 * dim_factor 替换经验值
验证完整框架精度

物理推导:
  C_GAMMA = e^(1/beta) * alpha_fs^3 * hbar^(-1/4) * k_B^(1/8) * m_e^(-1/4) * a0^(-1/2)

  e^(1/beta): 路径积分量子修正, beta=8*pi+1 (主丛曲率参数, Klein四元群和乐)
  alpha_fs^3: 运动三重分化 (惯性×能动张量×作用量), 每分支贡献一个alpha_fs
  维度因子: 自然单位制转换 (Hartree原子单位 → SI)
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB
import csv, re, math, numpy as np

# 精确物理常数
HBAR = 1.054571817e-34; KB = 1.380649e-23; AMU = 1.66e-27
ME = 9.10938370e-31; E_CHARGE = 1.602176634e-19
EPS0 = 8.854187817e-12; C_LIGHT = 2.99792458e8
A0 = 5.291772109e-11

ALPHA_FS = E_CHARGE**2 / (4 * math.pi * EPS0 * HBAR * C_LIGHT)
BETA = 8 * math.pi + 1

# 理论C_GAMMA
C_GAMMA_THEORY = math.exp(1/BETA) * ALPHA_FS**3 * HBAR**(-0.25) * KB**(0.125) * ME**(-0.25) * A0**(-0.5)
C_GAMMA_FIT = 7.77e11

print(f"理论C_GAMMA = e^(1/beta) * alpha_fs^3 * dim = {C_GAMMA_THEORY:.6e}")
print(f"拟合C_GAMMA = {C_GAMMA_FIT:.6e}")
print(f"偏差 = {abs(C_GAMMA_THEORY/C_GAMMA_FIT-1)*100:.3f}%")
print()

# 读取框架代码
with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\cqm_no_classification_framework.py', 'r', encoding='utf-8') as f:
    original_code = f.read()
verify_start = original_code.find('data = []')
func_code = original_code[:verify_start]

def run_framework(c_gamma, label):
    modified_code = func_code.replace('C_GAMMA = 7.77e11', f'C_GAMMA = {c_gamma}')
    g = {
        'ATOM_DB': ATOM_DB, 'math': math, 'np': np, 'csv': csv, 're': re,
        'HBAR': HBAR, 'KB': KB, 'AMU': AMU,
        'defaultdict': __import__('collections').defaultdict,
    }
    exec(modified_code, g)
    predict = g['predict_tc_first_principles']

    data = []
    with open(r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_analysis\superconductors_deduplicated.csv', 'r', encoding='utf-8-sig') as fh:
        for row in csv.DictReader(fh):
            try: tc = float(row['临界温度 Tc (K)'])
            except: continue
            if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

    results = []
    for d in data:
        tc_pred, info = predict(d['formula'])
        if tc_pred > 0:
            ratio = tc_pred / d['tc_exp']
            err = max(ratio, 1.0/ratio) - 1.0
            results.append({**d, 'tc_pred': tc_pred, 'error': err, 'ratio': ratio})

    errs = np.array([r['error'] for r in results])
    print(f"{label}:")
    print(f"  中位{np.median(errs)*100:.1f}%  2倍内{np.sum(errs<1)*100/len(errs):.1f}%  5倍内{np.sum(errs<4)*100/len(errs):.1f}%")
    return results

# 运行对比
print("="*60)
results_theory = run_framework(C_GAMMA_THEORY, "理论C_GAMMA (e^(1/beta)*alpha_fs^3*dim)")
results_fit = run_framework(C_GAMMA_FIT, "拟合C_GAMMA (7.77e11)")
print("="*60)

# 按类别分析
print("\n按类别精度对比:")
cats = sorted(set(r['cat'] for r in results_theory))
print(f"{'类别':<20} {'理论2倍内':>10} {'拟合2倍内':>10} {'理论中位':>10} {'拟合中位':>10} {'数量':>6}")
for cat in cats:
    rt = [r for r in results_theory if r['cat'] == cat]
    rf = [r for r in results_fit if r['cat'] == cat]
    if rt and rf:
        et = np.array([r['error'] for r in rt])
        ef = np.array([r['error'] for r in rf])
        print(f"{cat:<20} {np.sum(et<1)*100/len(et):>9.1f}% {np.sum(ef<1)*100/len(ef):>9.1f}% {np.median(et)*100:>9.1f}% {np.median(ef)*100:>9.1f}% {len(rt):>6}")

# 逐材料差异
print(f"\n差异最大的材料 (理论 vs 拟合):")
diffs = []
for rt, rf in zip(results_theory, results_fit):
    if rt['formula'] == rf['formula']:
        diffs.append({
            'formula': rt['formula'],
            'tc_exp': rt['tc_exp'],
            'tc_theory': rt['tc_pred'],
            'tc_fit': rf['tc_pred'],
            'diff': abs(rt['tc_pred'] - rf['tc_pred']) / rt['tc_exp'],
        })
diffs.sort(key=lambda x: x['diff'], reverse=True)
print(f"{'材料':<20} {'Tc_exp':>8} {'Tc_理论':>10} {'Tc_拟合':>10} {'相对差':>8}")
for d in diffs[:10]:
    print(f"{d['formula']:<20} {d['tc_exp']:>8.2f} {d['tc_theory']:>10.2f} {d['tc_fit']:>10.2f} {d['diff']*100:>7.2f}%")

print(f"\n最大相对差 = {diffs[0]['diff']*100:.3f}%")
print(f"平均相对差 = {np.mean([d['diff'] for d in diffs])*100:.3f}%")