"""诊断: 检测Tc推导链中每个环节的精度贡献
找出哪个环节是第一性的缺口
"""
import csv, re, math
import numpy as np

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2_geo = 2.0/3.0; LN2 = math.log(2)
RIEMANN_ZEROS = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918720,43.311071,48.005150,49.773832])

ATOM_DB = {'H':(1.008,0,0.46,0),'He':(4.003,0,0.31,0),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,0),'O':(16.00,0,0.73,0),'F':(19.00,0,0.72,0),'Ne':(20.18,0,0.71,0),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,0),'S':(32.06,0,1.05,0),'Cl':(35.45,0,1.02,0),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,0),'Se':(78.97,0,1.20,0),'Br':(79.90,0,1.20,0),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,0),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,0),'Te':(127.60,0,1.60,0),'I':(126.90,0,1.63,0),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,0),'Th':(232.04,163,1.80,54)}
HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}
GL1_CATS = {'元素超导体(常压)','元素超导体(高压)','A15结构金属间化合物','合金超导体','其他金属间化合物','氢化物高压超导体','石墨插层超导体','其他特殊超导体'}
GL2_CATS = {'铜氧化物高温超导体','铁基超导体','有机超导体','富勒烯超导体'}

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
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'Z':tz}

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

# 反推 Γ
COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
for it in range(20):
    for d in non_hf:
        ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
        geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
        d['Gamma'] = (ln_ke - geom) / COEF[0]
    Xg = np.column_stack([[d['Gamma'] for d in non_hf],
                         [math.log(d['G']) for d in non_hf],[math.log(d['tD']) for d in non_hf],
                         [math.log(d['B']) for d in non_hf],[math.log(d['N']) for d in non_hf],
                         [math.log(d['V']) for d in non_hf], np.ones(len(non_hf))])
    yg = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
    cg, _, _, _ = np.linalg.lstsq(Xg, yg, rcond=None)
    if np.max(np.abs(cg - COEF)) < 1e-8: break
    COEF = cg

# ============================================================
# 诊断：用ground truth Γ（从Tc反推）测链路精度上限
# ============================================================
print("="*80)
print("诊断: Tc推导链各环节精度贡献分解")
print("="*80)

# 环节1: 材料几何 → Δδ₀, G, θ_D, B, N, V ✅ 第一性
# 环节2: Δδ₀, G, θ_D, B, N, V, Γ → K_eff → Tc (联合优化系数)
# 环节3: Γ (Ŝ_5本征值) — 需要从几何或A4谱表确定

# 测试: 如果Γ=ground truth(从Tc反推), K_eff系数也联合优化, Tc精度?
print("\n--- 测试A: Γ=ground truth + 系数联合优化 ---")
# 联合优化: ln(K_eff) = a·Γ + b·lnG + c·lnθ_D + d·lnB + e·lnN + f·lnV + g
# 然后在LOOCV中测试

from sklearn.model_selection import LeaveOneOut
loo = LeaveOneOut()

errs_A = []
for train_idx, test_idx in loo.split(np.array(non_hf)):
    X_tr = np.column_stack([[non_hf[i]['Gamma'] for i in train_idx],
                            [math.log(non_hf[i]['G']) for i in train_idx],
                            [math.log(non_hf[i]['tD']) for i in train_idx],
                            [math.log(non_hf[i]['B']) for i in train_idx],
                            [math.log(non_hf[i]['N']) for i in train_idx],
                            [math.log(non_hf[i]['V']) for i in train_idx],
                            np.ones(len(train_idx))])
    y_tr = np.array([math.log(non_hf[i]['tc']**2 * 9 * LN2 / (8 * non_hf[i]['dd0']**2 * non_hf[i]['tD'])) for i in train_idx])
    coef, _, _, _ = np.linalg.lstsq(X_tr, y_tr, rcond=None)

    d = non_hf[test_idx[0]]
    ln_ke = (coef[0]*d['Gamma'] + coef[1]*math.log(d['G']) + coef[2]*math.log(d['tD']) +
             coef[3]*math.log(d['B']) + coef[4]*math.log(d['N']) + coef[5]*math.log(d['V']) + coef[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_A.append(abs(tp - d['tc'])/d['tc'])

errs_A = np.array(errs_A)
print(f"Γ=gt+系数LOOCV: 中位={np.median(errs_A)*100:.1f}%, 2倍内={np.mean(errs_A<=1)*100:.0f}%, 5倍内={np.mean(errs_A<=4)*100:.0f}%")

# 这说明即使Γ完全正确（从Tc反推），系数LOOCV也会引入误差。
# 这个误差来自：同一Γ下，不同材料的K_eff对几何参数的依赖不同。
# 这是公式ln(K_eff)=a·Γ+...的线性近似误差。

# 测试B: 固定全局系数, Γ=gt
print("\n--- 测试B: Γ=gt + 固定系数(全部数据拟合) ---")
# 用全部数据拟合一次系数，然后对每个材料用这个固定系数
X_all = np.column_stack([[d['Gamma'] for d in non_hf],
                         [math.log(d['G']) for d in non_hf],
                         [math.log(d['tD']) for d in non_hf],
                         [math.log(d['B']) for d in non_hf],
                         [math.log(d['N']) for d in non_hf],
                         [math.log(d['V']) for d in non_hf],
                         np.ones(len(non_hf))])
y_all = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
coef_all, _, _, _ = np.linalg.lstsq(X_all, y_all, rcond=None)

errs_B = []
for d in non_hf:
    ln_ke = (coef_all[0]*d['Gamma'] + coef_all[1]*math.log(d['G']) + coef_all[2]*math.log(d['tD']) +
             coef_all[3]*math.log(d['B']) + coef_all[4]*math.log(d['N']) + coef_all[5]*math.log(d['V']) + coef_all[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_B.append(abs(tp - d['tc'])/d['tc'])

errs_B = np.array(errs_B)
print(f"Γ=gt+固定系数: 中位={np.median(errs_B)*100:.1f}%, 2倍内={np.mean(errs_B<=1)*100:.0f}%, 5倍内={np.mean(errs_B<=4)*100:.0f}%")

# 测试C: R²分析——ln(K_eff)中有多少被Γ解释？
print(f"\n--- 测试C: ln(K_eff)的R²分解 ---")
y_lnke = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
X_geom_only = np.column_stack([[math.log(d['G']) for d in non_hf],
                                [math.log(d['tD']) for d in non_hf],
                                [math.log(d['B']) for d in non_hf],
                                [math.log(d['N']) for d in non_hf],
                                [math.log(d['V']) for d in non_hf],
                                np.ones(len(non_hf))])
X_full = np.column_stack([[d['Gamma'] for d in non_hf], X_geom_only])

# 几何部分解释的方差
coef_geom, _, _, _ = np.linalg.lstsq(X_geom_only, y_lnke, rcond=None)
r2_geom = 1 - np.sum((y_lnke - X_geom_only@coef_geom)**2) / np.sum((y_lnke - np.mean(y_lnke))**2)

# 完整模型解释的方差
coef_full, _, _, _ = np.linalg.lstsq(X_full, y_lnke, rcond=None)
r2_full = 1 - np.sum((y_lnke - X_full@coef_full)**2) / np.sum((y_lnke - np.mean(y_lnke))**2)

print(f"纯几何(6参数): R²={r2_geom:.4f}")
print(f"几何+Γ(7参数): R²={r2_full:.4f}")
print(f"Γ增量R²: {r2_full - r2_geom:.4f}")
print(f"未被解释的方差: {1 - r2_full:.4f}")

# 关键：未被解释的方差来自哪里？
# 如果Γ=gt且系数最优，仍有(1-R²)的方差——这是公式的固有近似误差

# 测试D: 用材料类别作为 one-hot，看剩余方差能吸收多少
print(f"\n--- 测试D: 类别one-hot的作用 ---")
all_cats = sorted(set(d['cat'] for d in non_hf))
cat_to_idx = {c: i for i, c in enumerate(all_cats)}
X_cat = np.zeros((len(non_hf), len(all_cats)))
for i, d in enumerate(non_hf):
    X_cat[i, cat_to_idx[d['cat']]] = 1

X_full_cat = np.column_stack([X_full, X_cat])
coef_cat, _, _, _ = np.linalg.lstsq(X_full_cat, y_lnke, rcond=None)
r2_cat = 1 - np.sum((y_lnke - X_full_cat@coef_cat)**2) / np.sum((y_lnke - np.mean(y_lnke))**2)
print(f"几何+Γ+类别: R²={r2_cat:.4f}")
print(f"类别增量R²: {r2_cat - r2_full:.4f}")
print(f"剩余未解释方差: {1 - r2_cat:.4f}")

print(f"""
{'='*80}
诊断结论
{'='*80}

链路分解:
  ln(K_eff) = a·Γ + b·lnG + c·lnθ_D + d·lnB + e·lnN + f·lnV + g

  纯几何=6参数: R²={r2_geom:.4f}  ← 当前纯第一性上限
  几何+Γ=7参数: R²={r2_full:.4f}  ← 如果Γ完美已知的上限
  +类别标签:    R²={r2_cat:.4f}  ← 最大可能上限

  未解释方差分布在:
  - Γ的不确定性(纯几何→Γ的映射误差)
  - 公式的线性近似误差(lnK_eff不是严格的线性函数)
  - 材料间K_eff的个性差异(同样Γ和几何，不同材料K_eff不同)
""")

# 最重要: 用完美Γ（A4谱表+ground truth ntuple）测试
omega_raw = np.array([1.0/np.sqrt(0.38196601), 1.0/np.sqrt(1.38196601), 1.0/np.sqrt(2.61803399), 1.0/np.sqrt(3.61803399)])
scale_opt = 8.520890
omega = omega_raw * scale_opt

from itertools import product
spectrum_table = {}
for n1,n2,n3,n4 in product(range(0,6), repeat=4):
    spectrum_table[(n1,n2,n3,n4)] = n1*omega[0]+n2*omega[1]+n3*omega[2]+n4*omega[3]

# 对每个材料找最近的A4谱点
for d in non_hf:
    best_err = float('inf')
    for ns, g in spectrum_table.items():
        e = abs(g - d['Gamma'])
        if e < best_err:
            best_err = e
            d['ns_gt'] = ns
            d['Gamma_a4'] = g

# 用A4谱表Γ预测
errs_a4 = []
for d in non_hf:
    ln_ke = (coef_all[0]*d['Gamma_a4'] + coef_all[1]*math.log(d['G']) + coef_all[2]*math.log(d['tD']) +
             coef_all[3]*math.log(d['B']) + coef_all[4]*math.log(d['N']) + coef_all[5]*math.log(d['V']) + coef_all[6])
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
    errs_a4.append(abs(tp - d['tc'])/d['tc'])

errs_a4 = np.array(errs_a4)
print(f"\nA4谱表Γ(完美回溯)+固定系数: 中位={np.median(errs_a4)*100:.1f}%, 2倍内={np.mean(errs_a4<=1)*100:.0f}%")
print(f"对比: Γ连续值+固定系数: 中位={np.median(errs_B)*100:.1f}%, 2倍内={np.mean(errs_B<=1)*100:.0f}%")
print(f"\nA4谱表取整引入的额外误差: {np.median(errs_a4)*100 - np.median(errs_B)*100:.1f}个百分点")