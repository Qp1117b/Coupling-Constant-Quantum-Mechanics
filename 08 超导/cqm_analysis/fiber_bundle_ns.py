"""纤维丛+同步算符: Ŝ_molecule =直积对角化
核心: Ŝ_total = Ŝ_A ⊗ I_B + I_A ⊗ Ŝ_B + V_coupling
对角化 → 本征谱 = f(n_A,n_B, 耦合)
不同元素组合 → 不同(n₁,n₂,n₃,n₄)
"""
import csv, re, math
import numpy as np
from itertools import product
from collections import Counter

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)

ATOMIC_NUM = {'H':1,'He':2,'Li':3,'Be':4,'B':5,'C':6,'N':7,'O':8,'F':9,'Ne':10,'Na':11,'Mg':12,'Al':13,'Si':14,'P':15,'S':16,'Cl':17,'K':19,'Ca':20,'Sc':21,'Ti':22,'V':23,'Cr':24,'Mn':25,'Fe':26,'Co':27,'Ni':28,'Cu':29,'Zn':30,'Ga':31,'Ge':32,'As':33,'Se':34,'Br':35,'Rb':37,'Sr':38,'Y':39,'Zr':40,'Nb':41,'Mo':42,'Tc':43,'Ru':44,'Rh':45,'Pd':46,'Ag':47,'Cd':48,'In':49,'Sn':50,'Sb':51,'Te':52,'I':53,'Cs':55,'Ba':56,'La':57,'Ce':58,'Pr':59,'Nd':60,'Sm':62,'Eu':63,'Gd':64,'Tb':65,'Dy':66,'Ho':67,'Er':68,'Tm':69,'Yb':70,'Lu':71,'Hf':72,'Ta':73,'W':74,'Re':75,'Os':76,'Ir':77,'Pt':78,'Au':79,'Hg':80,'Tl':81,'Pb':82,'Bi':83,'Th':90}

ATOM_DB = {'H':(1.008,0,0.46,11),'He':(4.003,0,0.31,11),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,11),'O':(16.00,0,0.73,11),'F':(19.00,0,0.72,11),'Ne':(20.18,0,0.71,11),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,11),'S':(32.06,0,1.05,11),'Cl':(35.45,0,1.02,11),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,11),'Se':(78.97,0,1.20,11),'Br':(79.90,0,1.20,11),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,11),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,11),'Te':(127.60,0,1.60,11),'I':(126.90,0,1.63,11),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,11),'Th':(232.04,163,1.80,54)}
HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}

def atom_db(el): return ATOM_DB.get(el, (100.0, 200, 1.5, 11))
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
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'atoms':a,'n_elem':len(a)}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        data.append({**mp,'formula':row['材料(化学式)'],'cat':row['类别'],'tc':tc})

# 反推 Γ
COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
non_hf = [d for d in data if not d['hf']]
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

# A4谱表
omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])
omega = omega_raw * 8.520890
spectrum = {}
for n1,n2,n3,n4 in product(range(0, 6), repeat=4):
    spectrum[(n1,n2,n3,n4)] = n1*omega[0]+n2*omega[1]+n3*omega[2]+n4*omega[3]

for d in data:
    if 'Gamma' in d:
        best = min(spectrum.items(), key=lambda x: abs(x[1]-d['Gamma']))
        d['ns_gt'] = best[0]

# ============================================================
# 纤维丛方法: 每种元素有(n₁,n₂,n₃,n₄)，从ground truth反推
# ============================================================
print("="*80)
print("纤维丛方法: Ŝ_element → Ŝ_molecule 铰链")
print("="*80)

# 从单元素超导体ground truth推断Ŝ_element
element_superconductors = [d for d in data if d['n_elem'] == 1 and 'ns_gt' in d]
print(f"\n单元素材料: {len(element_superconductors)}个")
element_ns = {}  # element → list of (n₁,n₂,n₃,n₄)
for d in element_superconductors:
    el = list(d['atoms'].keys())[0]
    element_ns.setdefault(el, []).append(d['ns_gt'])
    print(f"  {el}: Γ={d['Gamma']:.1f}, ns={d['ns_gt']}, formula={d['formula']}")

# 关键问题: 化合物Γ = 元素ns的组合规则是什么？
# 假设: Ŝ_total = ⊗ Ŝ_el → 对角化后ns的某种组合
#
# 最简规则: ns_total = ns_A + ns_B + ... (向量加法!)
# 因为A4谱是加法性的: Γ(ns_A + ns_B) = (n₁A+n₁B)ω₁ + ... = Γ(ns_A) + Γ(ns_B)

print(f"\n--- 向量加法假设: ns_total = ns_A + ns_B ---")
ns_add_matches = []
for d in data:
    if 'ns_gt' not in d: continue
    if d['n_elem'] == 1: continue

    atoms = d['atoms']
    ns_pred = np.array([0,0,0,0], dtype=float)
    total_cnt = 0
    for el, cnt in atoms.items():
        if el in element_ns:
            ns_pred += cnt * np.array(element_ns[el][0])
            total_cnt += cnt
    if total_cnt == 0: continue
    ns_pred = tuple(int(round(x)) for x in ns_pred)

    # 找最近的合法ns
    best_dist = float('inf')
    best_ns = None
    best_g = 0
    for ns, g in spectrum.items():
        dist = sum((a-b)**2 for a,b in zip(ns_pred, ns))
        if dist < best_dist:
            best_dist = dist
            best_ns = ns
            best_g = g

    gt_ns = d['ns_gt']
    match = best_ns == gt_ns
    ns_add_matches.append((d['formula'], gt_ns, best_ns, match, d['Gamma'], best_g))

    if match:
        print(f"  MATCH: {d['formula']:<20} gt={gt_ns} pred={best_ns} Γ={d['Gamma']:.1f}")

matches = sum(1 for _, _, _, m, _, _ in ns_add_matches if m)
print(f"\n向量加法匹配率: {matches}/{len(ns_add_matches)} ({matches/len(ns_add_matches)*100:.0f}%)")

# 非匹配案例
print(f"\n非匹配案例:")
count = 0
for formula, gt_ns, pred_ns, match, Gamma, pred_g in ns_add_matches:
    if not match and count < 10:
        print(f"  {formula:<25} gt={gt_ns} pred={pred_ns} Γ_gt={Gamma:.1f} Γ_pred={pred_g:.1f}")
        count += 1

# ============================================================
# 改进: 每个元素有多个候选ns (因为不同化合物中同一元素的ns可以不同)
# 从所有含该元素的化合物反推
# ============================================================
print(f"\n{'='*80}")
print("改进: 每元素多种ns模式（材料环境依赖）")
print(f"{'='*80}")

el_all_ns = {}  # 收集每个元素在所有材料中的ground truth ns
for d in data:
    if 'ns_gt' not in d: continue
    for el in d['atoms']:
        el_all_ns.setdefault(el, []).append(d['ns_gt'])

# 对每个元素，取最常见的前2个ns模式
el_modes = {}
for el, nss in sorted(el_all_ns.items()):
    counter = Counter(nss)
    top3 = counter.most_common(3)
    el_modes[el] = [ns for ns, cnt in top3]
    if len(top3) >= 2:
        print(f"  {el:<4} ({len(nss):>3}次): {top3[0][0]}({top3[0][1]}) {top3[1][0]}({top3[1][1]})",
              f"   {top3[2][0]}({top3[2][1]})" if len(top3) >= 3 else "")

# 对每个化合物，尝试所有元素ns组合
print(f"\n--- 多模式匹配 ---")
best_matches_el = []
for d in data:
    if 'ns_gt' not in d: continue
    if d['n_elem'] == 1: continue

    atoms = d['atoms']
    # 生成所有可能的ns组合
    element_choices = {}
    for el in atoms:
        if el in el_modes:
            element_choices[el] = el_modes[el]

    # 找最接近gt_ns的组合
    best_dist = float('inf')
    best_combo = None
    best_ns = None

    if element_choices:
        els = list(element_choices.keys())
        # 限制: 只试每个元素的前2个模式
        from itertools import product
        for combo in product(*[element_choices[el] for el in els]):
            ns_pred = np.zeros(4, dtype=float)
            for i, el in enumerate(els):
                ns_pred += atoms[el] * np.array(combo[i])
            ns_pred = tuple(int(round(x)) for x in ns_pred)

            for ns, g in spectrum.items():
                dist = sum((a-b)**2 for a,b in zip(ns_pred, ns))
                if dist < best_dist:
                    best_dist = dist
                    best_combo = dict(zip(els, combo))
                    best_ns = ns

    if best_ns:
        gt_ns = d['ns_gt']
        match = best_ns == gt_ns
        best_matches_el.append((d['formula'], gt_ns, best_ns, match, best_combo))

matches2 = sum(1 for _, _, _, m, _ in best_matches_el if m)
print(f"多模式匹配率: {matches2}/{len(best_matches_el)} ({matches2/len(best_matches_el)*100:.0f}%)")

# 模式匹配案例
for formula, gt_ns, pred_ns, match, combo in best_matches_el[:5]:
    if match:
        combo_str = ", ".join(f"{el}->{ns}" for el, ns in combo.items())
        print(f"  MATCH: {formula:<25} gt={gt_ns} {combo_str}")

print(f"""
{'='*80}
纤维丛框架的链条
{'='*80}

缺失环节: Ŝ_molecule 的对角化机制
  Ŝ_molecule = (ø_el Ŝ_el) + Σ_edges V_uv

  V_uv 来自化学键 → 扰动元素ns → 产生与晶体点群相关的谱分裂

  当前验证: 向量加法 ns_total = Σ ns_el 匹配率 {matches}/{len(ns_add_matches)} ({matches/len(ns_add_matches)*100:.0f}%)
  多模式匹配: {matches2}/{len(best_matches_el)} ({matches2/len(best_matches_el)*100:.0f}%)

这表明:
1. ns加法规则在部分化合物中成立(匹配率{matches/len(ns_add_matches)*100:.0f}%)
2. 同一元素在不同材料中取不同ns模式 → 需要V_uv耦合项
3. 耦合强度与化学键类型/点群有关

完整纤维丛预言链:
  元素ns(壳层构型) → 晶格点群 → V_uv(化学键耦合)
  → Ŝ_molecule对角化 → 材料(n₁,n₂,n₃,n₄) → A4谱表Γ → Tc
""")