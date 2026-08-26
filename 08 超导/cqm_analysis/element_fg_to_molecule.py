"""元素FG → 分子FG: 从元素壳层构型确定材料在A4谱表上的位置
核心假设: 每种元素的(n₁,n₂,n₃,n₄)由其壳层构型(价电子轨道类型)决定
材料Γ = Σ_el w_el · Γ_el
"""
import sys; sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework'); from atom_db import ATOM_DB, atom_db
import csv, re, math
import numpy as np
from itertools import product

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)
RIEMANN_ZEROS = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918720,43.311071,48.005150,49.773832])

HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}
GL1_CATS = {'元素超导体(常压)','元素超导体(高压)','A15结构金属间化合物','合金超导体','其他金属间化合物','氢化物高压超导体','石墨插层超导体','其他特殊超导体'}
GL2_CATS = {'铜氧化物高温超导体','铁基超导体','有机超导体','富勒烯超导体'}

# 价电子构型判断
def valence_orbital_type(el, Z):
    """判断元素的主导价轨道类型 s/p/d/f"""
    electrons = int(Z)
    configs = [(1,'s',2),(2,'s',2),(2,'p',6),(3,'s',2),(3,'p',6),(4,'s',2),(3,'d',10),
               (4,'p',6),(5,'s',2),(4,'d',10),(5,'p',6),(6,'s',2),(4,'f',14),
               (5,'d',10),(6,'p',6),(7,'s',2),(5,'f',14),(6,'d',10)]

    remaining = electrons
    last_orbital = 's'
    for n, orb, cap in configs:
        filled = min(remaining, cap)
        if filled > 0:
            last_orbital = orb
        remaining -= filled
        if remaining <= 0:
            break
    return last_orbital

def atom_db(el): return ATOM_DB.get(el, (100.0, 200, 1.5, 0))
def pf(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    a = {}
    for el, cnt in pairs:
        if el in ATOM_DB: a[el] = a.get(el,0)+(float(cnt) if cnt else 1.0)
    return a

def cp(formula):
    a = pf(formula)
    if not a: return None
    tm = sum(a[el]*atom_db(el)[0] for el in a)
    na = sum(a.values())
    ar = sum(a[el]*atom_db(el)[2] for el in a)/na
    l = 2*ar*1e-10
    td = sum(a[el]*atom_db(el)[1] for el in a)/na
    if td == 0: return None
    V = l**3
    ff = 1.0-0.3*(1.0-1.0/na)
    es = 0
    els = list(a.keys())
    for i in range(len(els)):
        for j in range(i+1,len(els)):
            es += 1.0/(a[els[i]]*atom_db(els[i])[0]*AMU) + 1.0/(a[els[j]]*atom_db(els[j])[0]*AMU)
    if not es:
        mi = tm*AMU/na
        es = (na*(na-1)/2)*2.0/mi
    G = (1.0/l)*math.sqrt((1.0-ff)*es)
    od = td*KB/HBAR
    dd = math.sqrt(abs((C2_geo/l**2)*(3*HBAR/(4*od))*(1-ff)*es))
    B = tm*td**2*KB/V*1e-3
    hf = any(el in HF_EL for el in a)
    tz = sum(a[el]*atom_db(el)[3] for el in a)
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'Z':tz,'atoms':a,'n_elem':len(a)}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        data.append({**mp,'formula':row['材料(化学式)'],'cat':row['类别'],'tc':tc})

non_hf = [d for d in data if not (d['hf'])]

# 反推 Γ 和 (n₁,n₂,n₃,n₄)
COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
for it in range(20):
    for d in non_hf:
        ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
        geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
        d['Gamma'] = (ln_ke - geom) / COEF[0]
    X = np.column_stack([[d['Gamma'] for d in non_hf],
                         [math.log(d['G']) for d in non_hf],[math.log(d['tD']) for d in non_hf],
                         [math.log(d['B']) for d in non_hf],[math.log(d['N']) for d in non_hf],
                         [math.log(d['V']) for d in non_hf], np.ones(len(non_hf))])
    y = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
    cnew, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    if np.max(np.abs(cnew - COEF)) < 1e-8: break
    COEF = cnew

# 扩展到所有数据 (包括HF)
for d in data:
    if 'Gamma' not in d:
        d['Gamma'] = 30.0  # fallback，不对HF做精确计算

# A4 谱表
omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])
omega = omega_raw * 8.520890
spectrum = {}
for n1,n2,n3,n4 in product(range(0,6), repeat=4):
    spectrum[(n1,n2,n3,n4)] = n1*omega[0]+n2*omega[1]+n3*omega[2]+n4*omega[3]

for d in data:
    best_err = float('inf')
    for ns, g in spectrum.items():
        e = abs(g - d['Gamma'])
        if e < best_err:
            best_err = e
            d['ns'] = ns
    d['nl_elem'] = {el: atomic_num for el, atomic_num in [(el, atom_db(el)[3]) for el in d['atoms']]}

# ============================================================
# 从元素超导体反推每种元素的FG→(n₁,n₂,n₃,n₄)映射
# ============================================================
print("="*80)
print("元素FG → 分子FG: 从元素壳层构型确定A4谱表位置")
print("="*80)

# 单元素超导体（不用高压的，因为高压改变了FG）
element_superconductors = [d for d in data if d['cat'] == '元素超导体(常压)' and d['n_elem'] == 1]
print(f"总单元素常压超导体: {len(element_superconductors)}")
if len(element_superconductors) == 0:
    # 放宽条件
    all_cats = set(d['cat'] for d in data)
    print(f"数据库中的类别: {all_cats}")
    eles = [d for d in data if d['n_elem'] == 1]
    print(f"单元素材料: {len(eles)}, 类别: {set(d['cat'] for d in eles)}")
    element_superconductors = eles

el_fg = {}
for d in element_superconductors:
    el = list(d['atoms'].keys())[0]
    el_fg.setdefault(el, []).append(d['ns'])

n_el_fg = len(el_fg)
print(f"\n从{n_el_fg}种常压元素超导体反推元素FG:")

# 对每个元素取平均数
el_ns = {}
for el, nss in el_fg.items():
    if len(nss) == 0: continue
    avg_ns = tuple(int(round(np.mean([n[j] for n in nss]))) for j in range(4))
    orbital = valence_orbital_type(el, atom_db(el)[3])
    print(f"  {el:<4} Z={atom_db(el)[3]:>3} 轨道={orbital}  n_mat={len(nss)}  ns={avg_ns}  (raw: {nss[:3]}...)")
    el_ns[el] = avg_ns

# ============================================================
# 测试: 分子FG = 元素FG的张量积在A4谱表上的投影
# 策略: 配对主导元素的FG权重最大
# ============================================================

# 对每个化合物，配对元素由"配对子流形"决定
# 简化: 取所有元素FG的平均（按原子数加权）
def predict_ns_from_elements(atoms, el_ns):
    """从元素FG推测材料的(n₁,n₂,n₃,n₄)"""
    ns_sum = np.zeros(4, dtype=float)
    total = 0
    for el, cnt in atoms.items():
        if el in el_ns:
            ns_sum += cnt * np.array(el_ns[el])
            total += cnt
    if total == 0:
        return None
    return tuple(int(round(x)) for x in ns_sum / total)

print(f"\n--- 测试: 元素FG加权 → 分子(n₁,n₂,n₃,n₄) ---")
matched = 0
total_compounds = 0
ns_pred_list = []

for d in non_hf:
    if d['n_elem'] == 1: continue  # 跳过单元素
    if d['hf']: continue
    pred_ns = predict_ns_from_elements(d['atoms'], el_ns)
    if pred_ns is None: continue
    total_compounds += 1

    # 在谱表中找最接近pred_ns的合法ns
    best_dist = float('inf')
    best_ns = None
    for ns in spectrum:
        dist = sum((a-b)**2 for a,b in zip(pred_ns, ns))
        if dist < best_dist:
            best_dist = dist
            best_ns = ns

    ns_pred_list.append((d['formula'], d['ns'], best_ns, best_ns == d['ns']))
    if best_ns == d['ns']:
        matched += 1

print(f"化合物总数: {total_compounds}")
print(f"完全匹配: {matched} ({matched/total_compounds*100:.1f}%)")

# 非匹配案例分析
print(f"\n非匹配案例(前10):")
print(f"{'材料':<25} {'gt_ns':<18} {'pred_ns':<18} {'Γ_gt':>8} {'Γ_pred':>8}")
mismatched = [x for x in ns_pred_list if not x[3]]
for formula, gt_ns, pred_ns, _ in mismatched[:10]:
    gt_g = spectrum.get(gt_ns, 0)
    pred_g = spectrum.get(pred_ns, 0)
    print(f"  {formula:<25} {str(gt_ns):<18} {str(pred_ns):<18} {gt_g:>8.2f} {pred_g:>8.2f}")

# ============================================================
# 改进: 配对元素不是所有元素——由类别决定配对轨道类型
# ============================================================
print(f"\n{'='*80}")
print("改进: 配对轨道类型筛选（s/p/d/f → 不同FG权重）")
print(f"{'='*80}")

# 类别 → 配对轨道类型
PAIR_ORBITAL = {
    '铜氧化物高温超导体': {'Cu': 'd', 'O': 'p'},
    '铁基超导体': {'Fe': 'd', 'As': 'p', 'Se': 'p'},
    '氢化物高压超导体': {'H': 's'},
    'A15结构金属间化合物': {'Nb': 'd', 'V': 'd', 'Mo': 'd'},
    '有机超导体': {'C': 'p', 'S': 'p', 'N': 'p'},
    '富勒烯超导体': {'C': 'p'},
    '其他金属间化合物': {},
    '其他特殊超导体': {},
    '合金超导体': {},
}

def get_pairing_elements(atoms, cat):
    """找出配对主导元素"""
    if cat in PAIR_ORBITAL:
        orbit_targets = PAIR_ORBITAL[cat]
        if orbit_targets:
            return {el: cnt for el, cnt in atoms.items()
                    if valence_orbital_type(el, atom_db(el)[3]) in orbit_targets.values()
                    or el in orbit_targets}
    return atoms  # fallback: 所有元素

matched2 = 0
total2 = 0

for d in non_hf:
    if d['n_elem'] == 1: continue
    if d['hf']: continue

    pair_el = get_pairing_elements(d['atoms'], d['cat'])
    if not pair_el:
        pair_el = d['atoms']

    pred_ns = predict_ns_from_elements(pair_el, el_ns)
    if pred_ns is None: continue
    total2 += 1

    best_dist = float('inf')
    best_ns = None
    for ns in spectrum:
        dist = sum((a-b)**2 for a,b in zip(pred_ns, ns))
        if dist < best_dist:
            best_dist = dist
            best_ns = ns

    if best_ns == d['ns']:
        matched2 += 1

print(f"只用配对元素(按类别): 匹配 {matched2}/{total2} ({matched2/total2*100:.1f}%)")
print(f"用全部元素:         匹配 {matched}/{total_compounds} ({matched/total_compounds*100:.1f}%)")

# ============================================================
# 核心: 从元素FG直接计算材料Γ (不经过ns分类)
# ============================================================
print(f"\n{'='*80}")
print("直接计算: Γ_material = Σ_el w_el · Γ_el (不取整)")
print(f"{'='*80}")

# 为每种元素计算 Γ_el (从单元素超导体反推)
el_gamma = {}
for el, nss in el_fg.items():
    gammas = [spectrum[ns] for ns in nss]
    el_gamma[el] = np.median(gammas)

print(f"\n已知元素Γ (从常压元素超导体反推):")
for el, g in sorted(el_gamma.items(), key=lambda x: x[1]):
    orbital = valence_orbital_type(el, atom_db(el)[3])
    print(f"  {el:<4} Z={atom_db(el)[3]:>3} Γ={g:.2f} 轨道={orbital}")

# 对所有非HF材料预测Γ
errs_el = []
for d in non_hf:
    if d['hf']: continue
    g_pred = 0
    total_w = 0
    for el, cnt in d['atoms'].items():
        if el in el_gamma:
            # 权重: 原子数 × 1/mass (轻原子主导)
            w = cnt / atom_db(el)[0]
            g_pred += w * el_gamma[el]
            total_w += w

    if total_w == 0:
        # 对没有已知Γ的元素，用θ_D代理
        g_pred = 30 + 10 * math.log(d['tD']/300)
    else:
        g_pred /= total_w

    ln_ke = (COEF[0]*g_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
             COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_el.append(abs(tp - d['tc'])/d['tc'])

errs_el = np.array(errs_el)
print(f"\n元素FG→Γ→Tc: 中位={np.median(errs_el)*100:.1f}%, {np.mean(errs_el<=1)*100:.0f}%在2倍内, {np.mean(errs_el<=4)*100:.0f}%在5倍内")
print(f"(对比 此前GBR: 中位 47%, 79%在2倍内, 89%在5倍内)")

print(f"""
{'='*80}
发现
{'='*80}

1. 元素FG → 分子(n₁,n₂,n₃,n₄)匹配率: {matched}/{total_compounds} ({matched/total_compounds*100:.0f}%)
   只用配对元素: {matched2}/{total2} ({matched2/total2*100:.0f}%) — 改进有限

2. 元素Γ直接加权(不取整) → Tc: 中位 {np.median(errs_el)*100:.0f}%
   这个精度取决于有多少元素的Γ已知

3. 问题: 只有{n_el_fg}种元素有Γ数据(来自常压元素超导体)
   要覆盖所有化合物, 需要为所有元素确定Γ_el

4. Γ_el可以从元素的壳层构型第一性推导吗?
   — 答案在元素周期表推导(§11.7): 每个壳层有对应的γ_n
   — 元素的Γ_el由其价电子的壳层γ_n组合决定
""")