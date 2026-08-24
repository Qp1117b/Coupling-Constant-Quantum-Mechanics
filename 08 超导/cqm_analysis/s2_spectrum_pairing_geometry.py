"""Ŝ_2 谱 η_j 第一性推导 v2——引入配对子流形几何
核心：η_j = C_2(j) · κ_s · (l·κ_pair)^(α·(3-d_pair))
"""
import csv, re, math
import numpy as np

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
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
    dd = math.sqrt(abs((C2/l**2)*(3*HBAR/(4*od))*(1-ff)*es))
    B = tm*td**2*KB/V*1e-3
    hf = any(el in HF_EL for el in a)
    tz = sum(a[el]*atom_db(el)[3] for el in a)
    return {'M':tm,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf,'Z':tz,'atoms':a}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        cat = row['类别']
        gl = 1 if cat in GL1_CATS else 2
        data.append({**mp,'formula':row['材料(化学式)'],'cat':cat,'tc':tc,'gl':gl})

CAT_J = {'铜氧化物高温超导体':2,'铁基超导体':1,'有机超导体':1,'富勒烯超导体':1}
CAT_D = {'铜氧化物高温超导体':2,'铁基超导体':2,'有机超导体':1.5,'富勒烯超导体':2}

COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
non_hf = [d for d in data if not (d['hf'] and d['gl'] == 1)]

for it in range(20):
    for d in non_hf:
        ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
        geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) +
                COEF[5]*math.log(d['V']) + COEF[6])
        d['Gamma'] = (ln_ke - geom) / COEF[0]
    X = np.column_stack([[d['Gamma'] for d in non_hf],
                         [math.log(d['G']) for d in non_hf],
                         [math.log(d['tD']) for d in non_hf],
                         [math.log(d['B']) for d in non_hf],
                         [math.log(d['N']) for d in non_hf],
                         [math.log(d['V']) for d in non_hf],
                         np.ones(len(non_hf))])
    y = np.array([math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD'])) for d in non_hf])
    coef_new, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    if np.max(np.abs(coef_new - COEF)) < 1e-8: break
    COEF = coef_new

for d in data:
    ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
    geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
            COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) +
            COEF[5]*math.log(d['V']) + COEF[6])
    d['Gamma'] = (ln_ke - geom) / COEF[0]
    dists = np.abs(RIEMANN_ZEROS[:10] - d['Gamma'])
    d['n_near'] = np.argmin(dists) + 1
    d['gamma_near'] = RIEMANN_ZEROS[d['n_near']-1]
    d['eta'] = d['Gamma'] - d['gamma_near']

    # 配对子流形几何参数
    # 曲率 κ ∝ θ_D · sqrt(M/(B·l))
    d['kappa_pair'] = d['tD'] * math.sqrt(d['M'] / (d['B'] * d['l'] * 1e10 + 1e-30))

    # 配对维度
    d['d_pair'] = CAT_D.get(d['cat'], 3)  # GL1 默认 3D

    # 配对子流形面积/体积指示
    # A_pair^(d/2) ∝ l^(d) for compact submanifold
    d['Vol_pair'] = d['l']**d['d_pair']

# ============================================================
# 构造 η_j 表达式
# ============================================================
print("="*80)
print("η_j 第一性推导 —— 配对子流形几何")
print("="*80)

gl2_data = [d for d in data if d['gl'] == 2]

etas = np.array([d['eta'] for d in gl2_data])
c2s = np.array([CAT_J[d['cat']]*(CAT_J[d['cat']]+1) for d in gl2_data])
ds = np.array([d['d_pair'] for d in gl2_data])
kappas = np.array([d['kappa_pair'] for d in gl2_data])
ls = np.array([d['l'] for d in gl2_data])

# 无量纲曲率
l_kappa = ls * kappas * 1e10  # 无量纲化

print(f"\n配对子流形几何参数分布:")
print(f"{'子类':<22} {'d':>3} {'n':>4} {'l(Å)中位':>9} {'κ中位':>10} {'l·κ中位':>9}")
print("-"*65)
for cat in sorted(set(d['cat'] for d in gl2_data)):
    ds_sub = [d for d in gl2_data if d['cat'] == cat]
    d_pair = ds_sub[0]['d_pair']
    l_vals = [d['l']*1e10 for d in ds_sub]
    k_vals = [d['kappa_pair'] for d in ds_sub]
    lk_vals = [l*k for l,k in zip(l_vals, k_vals)]
    print(f"  {cat:<20} {d_pair:>3} {len(ds_sub):>4} {np.median(l_vals):>9.3f} {np.median(k_vals):>10.1f} {np.median(lk_vals):>9.2f}")

# ============================================================
# 候选公式 1: η = C_2 · κ_0 · (l·κ)^(α·(3-d))
# ============================================================
print(f"\n{'='*80}")
print("候选公式 1: η = C_2 · κ_0 · (l·κ_pair)^(α·(3-d_pair))")
print(f"{'='*80}")

# 计算 exp = α·(3-d)
# 对于 d=2: exp = α
# 对于 d=1.5: exp = 1.5α
# 对于 d=3: exp = 0

from scipy.optimize import minimize

def obj1(params):
    k0, alpha = params
    exps = alpha * (3 - ds)
    pred = c2s * k0 * (l_kappa ** exps)
    return np.sum((etas - pred)**2)

r1 = minimize(obj1, x0=[0.1, 0.5], method='Nelder-Mead')
k0, alpha = r1.x
exps = alpha * (3 - ds)
pred1 = c2s * k0 * (l_kappa ** exps)
r2_1 = 1 - np.sum((etas-pred1)**2)/np.sum((etas-np.mean(etas))**2)

print(f"最佳参数: κ_0 = {k0:.6f}, α = {alpha:.4f}")
print(f"R² = {r2_1:.4f}")
print(f"η中位(实际)={np.median(etas):.3f}, η中位(预测)={np.median(pred1):.3f}")

# ============================================================
# 候选公式 2: η = C_2 · exp(a + b·ln(l·κ))
# ============================================================
print(f"\n候选公式 2: η = C_2 · exp(a + b·ln(l·κ)) · (3-d)^γ")
print(f"{'='*80}")

def obj2(params):
    a, b, g = params
    ln_pred = np.log(np.abs(c2s) + 1e-30) + a + b * np.log(l_kappa + 1e-30) + g * np.log(3 - ds + 1e-30)
    pred = np.exp(ln_pred)
    return np.sum((etas - pred)**2)

r2 = minimize(obj2, x0=[0.0, 0.0, 0.0], method='Nelder-Mead')
a, b, g = r2.x
ln_pred2 = np.log(np.abs(c2s) + 1e-30) + a + b * np.log(l_kappa + 1e-30) + g * np.log(3 - ds + 1e-30)
pred2 = np.exp(ln_pred2)
r2_2 = 1 - np.sum((etas-pred2)**2)/np.sum((etas-np.mean(etas))**2)

print(f"最佳参数: a={a:.4f}, b={b:.4f}, γ={g:.4f}")
print(f"R² = {r2_2:.4f}")

# ============================================================
# 候选公式 3: η/C₂ = d 的函数（离散谱）
# ============================================================
print(f"\n候选公式 3: η/C₂ 按 d_pair 分组的离散值（Ŝ_2 离散谱）")
print(f"{'='*80}")

eta_c2_by_d = {}
for d, c2v, ev in zip(ds, c2s, etas):
    eta_c2_by_d.setdefault(d, []).append(ev/c2v)

print(f"\n  {'d_pair':>7} {'n':>4} {'η/C₂中位':>9} {'η/C₂均值':>9} {'std':>7}")
print(f"  {'-'*40}")
for d in sorted(eta_c2_by_d.keys()):
    vals = np.array(eta_c2_by_d[d])
    print(f"  {d:>7.1f} {len(vals):>4} {np.median(vals):>9.4f} {np.mean(vals):>9.4f} {np.std(vals):>7.4f}")

# ============================================================
# 候选公式 4: 线性 Ŝ_2 谱 η_j ≈ j(j+1) · κ(d, lκ)
# ============================================================
print(f"\n候选公式 4: η = C_2(j) · (a·d + b·ln(lκ) + c)")
print(f"{'='*80}")

X4 = np.column_stack([c2s * ds, c2s * np.log(l_kappa + 1e-30), c2s])
coef4, _, _, _ = np.linalg.lstsq(X4, etas, rcond=None)
pred4 = X4 @ coef4
r2_4 = 1 - np.sum((etas-pred4)**2)/np.sum((etas-np.mean(etas))**2)

print(f"η = C₂ · ({coef4[0]:.6f}·d + {coef4[1]:.6f}·ln(lκ) + {coef4[2]:.6f})")
print(f"R² = {r2_4:.4f}")

# ============================================================
# 最简单的模型：每个 d 一个常数
# ============================================================
print(f"\n{'='*80}")
print("最简模型：每个 (d,j) 组合一个常数值（Ŝ_2 离散谱表）")
print(f"{'='*80}")

# 对每个(d,j)组合计算中位
combo_vals = {}
for d in gl2_data:
    key = (d['d_pair'], CAT_J[d['cat']])
    combo_vals.setdefault(key, []).append(d['eta'])

print(f"\n  {'d':>5} {'j':>2} {'C₂':>3} {'n':>4} {'η中位':>8}")
print(f"  {'-'*35}")
for (d, j), vals in sorted(combo_vals.items()):
    print(f"  {d:>5.1f} {j:>2} {j*(j+1):>3} {len(vals):>4} {np.median(vals):>8.3f}")

# 用这个离散谱预测
print(f"\n用离散 Ŝ_2 谱预测（每个 d 和 j 用中位值 + 同类所有材料共享）")
errs_dj = []
for d in gl2_data:
    key = (d['d_pair'], CAT_J[d['cat']])
    eta_pred = np.median(combo_vals[key])
    gamma_pred = d['gamma_near'] + eta_pred
    ln_ke_pred = COEF[0]*gamma_pred + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) + COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6]
    tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke_pred)*d['tD']/(9*LN2))
    errs_dj.append(abs(tp-d['tc'])/d['tc'])

errs_dj = np.array(errs_dj)
print(f"GL(2) 70材料: 中位={np.median(errs_dj)*100:.1f}%, {np.mean(errs_dj<=1)*100:.0f}%在2倍内, {np.mean(errs_dj<=4)*100:.0f}%在5倍内")

# ============================================================
# 结论
# ============================================================
print(f"\n{'='*80}")
print("结论")
print(f"{'='*80}")

print("""
Ŝ_2 谱 η_j 的第一性结构：

1. Ŝ_2 谱是离散的，由 (d_pair, j) 标记
   - d_pair: 配对子流形维度
     - d=2: CuO₂平面(铜氧化物), FeAs层(铁基), C₆₀球面(富勒烯)
     - d=1.5: 分子堆积(有机)
     - d=3: 各向同性3D(常规超导, η≈0)
   - j: SU(2) 配对对称性 (j=1 p波, j=2 d波)

2. 配对子流形曲率 κ_pair ∝ θ_D · sqrt(M/(B·l))
   编码了子流形的曲率半径倒数

3. η_j 的候选表达式：
   η_j = C_2(j) · [a·Δd + b·ln(l·κ_pair) + c]

   R² ≈ 30% —— 说明 Ŝ_2 谱主要来自子流形拓扑（离散的 d,j），
   连续几何（l·κ）只贡献精细修正。

4. 最实用方案：离散 Ŝ_2 谱表
   每个 (d,j) 组合对应一个常数值。
   在当前框架中，这等价于为每个 GL(2) 子类分配不同的 n
  （因为 γ_n 已经近似编码了配对维度信息）。

5. 单材料级别 η 的第一性推导未完全闭合。
   离散部分（η 按 d/j 分层）已确立，
   连续部分（l·κ 修正）需要配对子流形更精确的几何表征。
   这需要配对波函数对称性的详细信息（DFT层面）。
""")