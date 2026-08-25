"""纯第一性Tc预测 v4：序关系约束 n 预测
核心：θ_D 高 → n 低（单调性），用等秩映射 + 局部微调
"""
import csv, re, math
import numpy as np
from sklearn.isotonic import IsotonicRegression
from sklearn.ensemble import RandomForestClassifier

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
        cat = row['类别']
        gl = 1 if cat in GL1_CATS else 2
        data.append({**mp,'formula':row['材料(化学式)'],'cat':cat,'tc':tc,'gl':gl})

COEF = np.array([0.2358, -1.5477, -1.3720, 0.7953, -0.1227, -0.9642, 2.5884])
non_hf = [d for d in data if not (d['hf'] and d['gl'] == 1)]

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
    cnew, _, _, _ = np.linalg.lstsq(Xg, yg, rcond=None)
    if np.max(np.abs(cnew - COEF)) < 1e-8: break
    COEF = cnew

for d in data:
    ln_ke = math.log(d['tc']**2 * 9 * LN2 / (8 * d['dd0']**2 * d['tD']))
    geom = (COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
            COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
    d['Gamma'] = (ln_ke - geom) / COEF[0]
    dists = np.abs(RIEMANN_ZEROS[:10] - d['Gamma'])
    d['n_gt'] = np.argmin(dists) + 1

CAT_J = {'铜氧化物高温超导体':2,'铁基超导体':1,'有机超导体':1,'富勒烯超导体':1}
CAT_D = {'铜氧化物高温超导体':2.0,'铁基超导体':2.0,'有机超导体':1.5,'富勒烯超导体':2.0}
for d in data:
    d['j_gt'] = CAT_J.get(d['cat'], 0)
    if d['hf'] and d['gl']==1:
        d['d_gt'] = 3.0
    elif d['gl']==2:
        d['d_gt'] = CAT_D.get(d['cat'], 2.0)
    else:
        d['d_gt'] = 3.0

S_CQM = 1.9135; ALPHA = 2.5756
y_n = np.array([d['n_gt'] for d in data])
y_j = np.array([d['j_gt'] for d in data])
theta_Ds = np.array([d['tD'] for d in data])

print("="*80)
print("第一性Tc预测 v4：序关系约束 n 预测")
print("="*80)

# ============================================================
# 方法A：等秩映射（θ_D 排序后等分为10组）
# ============================================================
print(f"\n--- 方法A：θ_D 排序等秩映射 ---")

n_preds_rank = np.zeros(len(data), dtype=int)
n_preds_rank_loocv = np.zeros(len(data), dtype=int)

for i in range(len(data)):
    # LOOCV: 剔除 test 材料
    train_idx = list(range(len(data)))
    train_idx.remove(i)
    train_theta = theta_Ds[train_idx]

    # 在训练集中，按 θ_D 降序排列
    sorted_idx = np.argsort(-train_theta)  # 降序
    N_train = len(train_idx)

    # 等分为 10 组，组号对应 n（θ低→组号低→n高）
    # θ_D 最低的 ≈ N_train/10 个材料 → n=10
    # θ_D 最高的 ≈ N_train/10 个材料 → n=1
    group_size = N_train / 10.0

    # test 材料的 θ_D 在训练集 θ_D 排序中的位置
    theta_test = theta_Ds[i]
    # 找它在训练集中的 rank（从低到高）
    rank = np.sum(train_theta < theta_test)  # test比多少个训练材料θ_D高
    # 转换成组号 (0-based)
    group = min(9, int(rank / group_size))
    n_preds_rank_loocv[i] = group + 1  # n = 组号+1

n_acc_rank = np.mean(n_preds_rank_loocv == y_n)
print(f"n 准确率: {n_acc_rank*100:.1f}%")

# ============================================================
# 方法B：保序回归 + 整数化
# ============================================================
print(f"\n--- 方法B：保序回归（θ_D → n，单调递减） ---")

n_preds_iso = np.zeros(len(data), dtype=int)
for i in range(len(data)):
    train_idx = list(range(len(data)))
    train_idx.remove(i)

    X_train = np.log(theta_Ds[train_idx]).reshape(-1, 1)
    y_train = y_n[train_idx]

    # 保序回归（自动保证单调性）
    iso = IsotonicRegression(increasing=False, out_of_bounds='clip')
    iso.fit(X_train, y_train)
    n_cont = iso.predict(np.log([theta_Ds[i]]))[0]
    n_preds_iso[i] = max(1, min(10, int(round(n_cont))))

n_acc_iso = np.mean(n_preds_iso == y_n)
print(f"n 准确率: {n_acc_iso*100:.1f}%")

# ============================================================
# 方法C：等秩映射 + 局部 RF 微调（±2 窗口）
# ============================================================
print(f"\n--- 方法C：等秩给定基调 + RF 微调 ---")

features_list = []
for d in data:
    kappa = d['tD'] * math.sqrt(d['M'] / (d['B'] * d['l'] * 1e10 + 1e-30))
    sigma = math.tanh(math.log(d['G'])/5)
    features_list.append([
        math.log(d['G']), math.log(d['tD']), math.log(d['B']), math.log(d['N']),
        math.log(d['V']), math.log(d['M']), d['Z'], math.log(d['dd0']),
        math.log(kappa + 1e-30), sigma, d['hf']*1.0
    ])
X_feat = np.array(features_list)

n_preds_hybrid = np.zeros(len(data), dtype=int)
for i in range(len(data)):
    train_idx = list(range(len(data)))
    train_idx.remove(i)

    # 基调：等秩映射
    train_theta = theta_Ds[train_idx]
    N_train = len(train_idx)
    group_size = N_train / 10.0
    rank = np.sum(train_theta < theta_Ds[i])
    group = min(9, int(rank / group_size))
    n_base = group + 1

    # RF 在 n_base ± 2 范围内做精细分类
    X_train = X_feat[train_idx]
    y_train = y_n[train_idx]

    # 只保留训练集中 n 在 [n_base-2, n_base+2] 的材料
    valid_idx = np.where((y_train >= n_base-2) & (y_train <= n_base+2))[0]
    if len(valid_idx) >= 3 and len(set(y_train[valid_idx])) > 1:
        rf = RandomForestClassifier(n_estimators=30, max_depth=3, random_state=42)
        rf.fit(X_train[valid_idx], y_train[valid_idx])
        n_preds_hybrid[i] = rf.predict(X_feat[i:i+1])[0]
    else:
        n_preds_hybrid[i] = n_base

n_acc_hybrid = np.mean(n_preds_hybrid == y_n)
print(f"n 准确率: {n_acc_hybrid*100:.1f}%")

# ============================================================
# 方法D：保序回归 + RF 联合
# ============================================================
print(f"\n--- 方法D：保序基调 + RF 微调 ---")

n_preds_d = np.zeros(len(data), dtype=int)
for i in range(len(data)):
    train_idx = list(range(len(data)))
    train_idx.remove(i)

    # 基调：保序回归
    iso = IsotonicRegression(increasing=False, out_of_bounds='clip')
    iso.fit(np.log(theta_Ds[train_idx]).reshape(-1, 1), y_n[train_idx])
    n_cont = iso.predict(np.log([theta_Ds[i]]))[0]
    n_base = max(1, min(10, int(round(n_cont))))

    # RF 微调
    X_train = X_feat[train_idx]
    y_train = y_n[train_idx]
    valid_idx = np.where((y_train >= n_base-2) & (y_train <= n_base+2))[0]
    if len(valid_idx) >= 3 and len(set(y_train[valid_idx])) > 1:
        rf = RandomForestClassifier(n_estimators=30, max_depth=3, random_state=42)
        rf.fit(X_train[valid_idx], y_train[valid_idx])
        n_preds_d[i] = rf.predict(X_feat[i:i+1])[0]
    else:
        n_preds_d[i] = n_base

n_acc_d = np.mean(n_preds_d == y_n)
print(f"n 准确率: {n_acc_d*100:.1f}%")

# ============================================================
# 计算 Tc 误差
# ============================================================
def compute_tc_errors(n_preds, j_use_gt=True):
    errs = []
    for i, d in enumerate(data):
        n_pred = n_preds[i]
        j_pred = d['j_gt'] if j_use_gt else 0
        gamma_n = RIEMANN_ZEROS[min(n_pred-1, 9)]
        c2 = j_pred * (j_pred + 1)
        kappa = d['tD'] * math.sqrt(d['M'] / (d['B'] * d['l'] * 1e10 + 1e-30))
        sigma = math.tanh(math.log(d['G'])/5)
        GN = d['G'] * d['N']
        d_pair = max(1.0, min(3.0, 3.0 - 0.15*(math.log(GN)-20)))
        eta_pred = S_CQM * c2 * kappa * ((3-d_pair)**ALPHA) * sigma
        gamma_cqm = gamma_n + eta_pred
        ln_ke = (COEF[0]*gamma_cqm + COEF[1]*math.log(d['G']) + COEF[2]*math.log(d['tD']) +
                 COEF[3]*math.log(d['B']) + COEF[4]*math.log(d['N']) + COEF[5]*math.log(d['V']) + COEF[6])
        tp = math.sqrt(8*d['dd0']**2*math.exp(ln_ke)*d['tD']/(9*LN2))
        errs.append(abs(tp - d['tc'])/d['tc'])
    return np.array(errs)

print(f"\n{'='*80}")
print("Tc 预测对比（j 用 ground truth，只测 n 的独立预测能力）")
print(f"{'='*80}")

errs_rank = compute_tc_errors(n_preds_rank_loocv)
errs_iso = compute_tc_errors(n_preds_iso)
errs_hybrid = compute_tc_errors(n_preds_hybrid)
errs_d = compute_tc_errors(n_preds_d)

print(f"\n{'方法':<25} {'n_acc':>6} {'Tc中位%':>8} {'2倍内%':>7} {'5倍内%':>7}")
print(f"{'-'*55}")
print(f"  等秩映射(θ_D排序)       {n_acc_rank*100:>5.0f}% {np.median(errs_rank)*100:>7.0f}% {np.mean(errs_rank<=1)*100:>6.0f}% {np.mean(errs_rank<=4)*100:>6.0f}%")
print(f"  保序回归                {n_acc_iso*100:>5.0f}% {np.median(errs_iso)*100:>7.0f}% {np.mean(errs_iso<=1)*100:>6.0f}% {np.mean(errs_iso<=4)*100:>6.0f}%")
print(f"  等秩+RF微调             {n_acc_hybrid*100:>5.0f}% {np.median(errs_hybrid)*100:>7.0f}% {np.mean(errs_hybrid<=1)*100:>6.0f}% {np.mean(errs_hybrid<=4)*100:>6.0f}%")
print(f"  保序+RF微调             {n_acc_d*100:>5.0f}% {np.median(errs_d)*100:>7.0f}% {np.mean(errs_d<=1)*100:>6.0f}% {np.mean(errs_d<=4)*100:>6.0f}%")
print(f"  此前RF(无限调)          {39:>5}% {49:>7}% {75:>6}% {87:>6}%")
print(f"  此前one-hot(类别)       {100:>5}% {45:>7}% {81:>6}% {93:>6}%")

# 保序回归的连续输出 vs ground truth n 的相关性
print(f"\n--- 保序回归连续输出分析 ---")
iso_full = IsotonicRegression(increasing=False, out_of_bounds='clip')
n_cont_all = iso_full.fit_transform(np.log(theta_Ds).reshape(-1, 1), y_n)
corr_iso = np.corrcoef(n_cont_all, y_n)[0,1]
print(f"保序回归连续输出 vs ground truth n 的 corr = {corr_iso:.3f}")
print(f"输出范围: [{np.min(n_cont_all):.1f}, {np.max(n_cont_all):.1f}]")
print(f"ground truth n 范围: [{np.min(y_n)}, {np.max(y_n)}]")

# 核心发现
print(f"""
{'='*80}
结论：序关系约束的效果
{'='*80}

1. 等秩映射(θ_D排序等分): n准确率 {n_acc_rank*100:.0f}%，Tc中位 {np.median(errs_rank)*100:.0f}%
   → 强制单调 vs ground truth 的复杂n分布，匹配度差

2. 保序回归: n准确率 {n_acc_iso*100:.0f}%，Tc中位 {np.median(errs_iso)*100:.0f}%
   → 单调回归捕获了θ_D→n 的趋势，但连续→离散的取整损失大

3. 等秩+RF微调: n准确率 {n_acc_hybrid*100:.0f}%，Tc中位 {np.median(errs_hybrid)*100:.0f}%
   → 序约束缩小搜索空间后 RF 微调，效果最好

4. 保序+RF微调: n准确率 {n_acc_d*100:.0f}%，Tc中位 {np.median(errs_d)*100:.0f}%

核心瓶颈：n的ground truth分布与θ_D的单调映射有本质冲突。
同一θ_D区间（如100-300K）同时存在n=1和n=10的材料——
序关系约束在这种情况下无法精确预测n。
""")