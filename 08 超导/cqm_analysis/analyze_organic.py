"""分析有机超导体和石墨插层的误差模式"""

import sys, os, math, csv
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cqm_no_classification_framework import *

data_file = os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv')
data = []
with open(data_file, 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'formula': row['材料(化学式)'], 'cat': row['类别'], 'tc_exp': tc})

print("="*80)
print("有机超导体 + 石墨插层 详细分析")
print("="*80)

for target_cat in ['有机超导体', '石墨插层超导体']:
    print(f"\n--- {target_cat} ---")
    materials = [d for d in data if d['cat'] == target_cat]
    for d in sorted(materials, key=lambda x: x['tc_exp']):
        tc_pred, info = predict_tc_first_principles(d['formula'])
        if tc_pred <= 0:
            print(f"  {d['formula']:25s} exp={d['tc_exp']:8.2f}K pred=FAILED")
            continue
        ratio = tc_pred / d['tc_exp']
        err = max(ratio, 1.0/ratio) - 1.0
        gamma_n = info.get('gamma_n', 0)
        n_c = info.get('n_continuous', 0)
        sg = info.get('spectral_gap', 0)
        cond = info.get('cond_A', 0)

        atoms = parse_formula(d['formula'])
        atom_feat = compute_atom_features(atoms) if atoms else {}

        print(f"  {d['formula']:25s} exp={d['tc_exp']:8.2f}K pred={tc_pred:10.2f}K "
              f"ratio={ratio:8.2f} err={err*100:8.0f}% γ={gamma_n:.1f} n_c={n_c:.1f} "
              f"sg={sg:.3f} cond={cond:.1f} "
              f"o={atom_feat.get('o_fraction',0):.2f} "
              f"f={atom_feat.get('f_fraction',0):.3f} "
              f"dp={atom_feat.get('dp_hybrid',0):.2f} "
              f"d0={atom_feat.get('d0_fraction',0):.2f}")

# 分析所有类别的2x内材料
print("\n" + "="*80)
print("各类别2x内统计(对称误差)")
print("="*80)

cat_results = {}
for d in data:
    tc_pred, info = predict_tc_first_principles(d['formula'])
    if tc_pred <= 0: continue
    ratio = tc_pred / d['tc_exp']
    err = max(ratio, 1.0/ratio) - 1.0
    cat = d['cat']
    if cat not in cat_results: cat_results[cat] = []
    cat_results[cat].append((d['formula'], d['tc_exp'], tc_pred, ratio, err))

for cat in sorted(cat_results.keys()):
    r = cat_results[cat]
    w2 = sum(1 for x in r if x[4] < 1.0)
    over = sum(1 for x in r if x[3] > 2.0)  # 高估>2x
    under = sum(1 for x in r if x[3] < 0.5)  # 低估<0.5x
    good = sum(1 for x in r if 0.5 <= x[3] <= 2.0)
    print(f"  {cat:25s}: {len(r):3d}个 2x内={w2:3d}({w2/len(r)*100:4.0f}%) "
          f"高估={over:3d} 低估={under:3d} 正确={good:3d}")