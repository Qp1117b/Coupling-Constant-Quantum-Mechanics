"""输出所有材料的Tc预测表"""
import csv, re, math
import numpy as np
from scipy.optimize import minimize

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
BETA = 8 * math.pi + 1; C2 = 2.0/3.0; LN2 = math.log(2); C_GEO = math.sqrt(C2)
RIEMANN_ZEROS = [14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918720,43.311071,48.005150,49.773832]

ATOM_DB = {'H':(1.008,0,0.46,0),'He':(4.003,0,0.31,0),'Li':(6.94,344,1.52,11),'Be':(9.01,1440,1.12,130),'B':(10.81,1480,0.87,185),'C':(12.01,2230,0.77,338),'N':(14.01,0,0.75,0),'O':(16.00,0,0.73,0),'F':(19.00,0,0.72,0),'Ne':(20.18,0,0.71,0),'Na':(22.99,158,1.86,7),'Mg':(24.31,400,1.60,35),'Al':(26.98,428,1.43,76),'Si':(28.09,645,1.18,100),'P':(30.97,0,1.10,0),'S':(32.06,0,1.05,0),'Cl':(35.45,0,1.02,0),'K':(39.10,91,2.27,3),'Ca':(40.08,230,1.97,15),'Sc':(44.96,360,1.62,44),'Ti':(47.87,420,1.47,110),'V':(50.94,383,1.34,162),'Cr':(52.00,435,1.28,160),'Mn':(54.94,410,1.27,120),'Fe':(55.85,470,1.26,170),'Co':(58.93,445,1.25,180),'Ni':(58.69,450,1.24,180),'Cu':(63.55,343,1.28,140),'Zn':(65.38,327,1.34,70),'Ga':(69.72,240,1.35,40),'Ge':(72.63,374,1.22,75),'As':(74.92,0,1.21,0),'Se':(78.97,0,1.20,0),'Br':(79.90,0,1.20,0),'Rb':(85.47,56,2.48,2),'Sr':(87.62,147,2.15,12),'Y':(88.91,280,1.80,37),'Zr':(91.22,291,1.60,95),'Nb':(92.91,275,1.46,170),'Mo':(95.96,425,1.39,230),'Tc':(98.00,0,1.36,0),'Ru':(101.07,0,1.34,220),'Rh':(102.91,0,1.34,150),'Pd':(106.42,274,1.37,180),'Ag':(107.87,215,1.44,100),'Cd':(112.41,209,1.49,42),'In':(114.82,108,1.62,11),'Sn':(118.71,200,1.58,50),'Sb':(121.76,0,1.61,0),'Te':(127.60,0,1.60,0),'I':(126.90,0,1.63,0),'Cs':(132.91,38,2.65,2),'Ba':(137.33,110,2.22,9),'La':(138.91,142,1.87,24),'Ce':(140.12,0,1.82,22),'Pr':(140.91,0,1.82,21),'Nd':(144.24,0,1.82,20),'Sm':(150.36,0,1.81,18),'Eu':(151.96,0,1.81,8),'Gd':(157.25,0,1.80,25),'Tb':(158.93,0,1.79,25),'Dy':(162.50,0,1.79,25),'Ho':(164.93,0,1.78,26),'Er':(167.26,0,1.78,26),'Tm':(168.93,0,1.77,28),'Yb':(173.05,0,1.77,10),'Lu':(174.97,0,1.77,30),'Hf':(178.49,252,1.59,110),'Ta':(180.95,240,1.46,200),'W':(183.84,400,1.39,310),'Re':(186.21,430,1.37,370),'Os':(190.23,500,1.35,400),'Ir':(192.22,420,1.36,355),'Pt':(195.08,240,1.39,230),'Au':(196.97,170,1.44,180),'Hg':(200.59,0,1.51,25),'Tl':(204.38,78,1.70,8),'Pb':(207.20,105,1.75,23),'Bi':(208.98,0,1.70,0),'Th':(232.04,163,1.80,54),'Pa':(231.04,0,1.80,0),'U':(238.03,207,1.75,100)}

HF_EL = {'Ce','Yb','U','Pr','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Lu','Nd','Np','Pu'}
GL1_CATS = {'元素超导体(常压)','元素超导体(高压)','A15结构金属间化合物','合金超导体','其他金属间化合物','氢化物高压超导体','石墨插层超导体','其他特殊超导体'}
GL2_CATS = {'铜氧化物高温超导体','铁基超导体','有机超导体','富勒烯超导体'}
CAT_N = {'石墨插层超导体':1,'有机超导体':3,'A15结构金属间化合物':7,'铁基超导体':8,'铜氧化物高温超导体':9,'氢化物高压超导体':10,'元素超导体(常压)':5,'元素超导体(高压)':6,'其他金属间化合物':4,'其他特殊超导体':5,'合金超导体':4,'富勒烯超导体':3}
CAT_J = {'铜氧化物高温超导体':2,'铁基超导体':1,'有机超导体':1,'富勒烯超导体':1}

def pf(f):
    pairs = re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f)
    a = {}
    for el, cnt in pairs:
        if el in ATOM_DB: a[el] = a.get(el,0)+(float(cnt) if cnt else 1.0)
    return a

def cp(formula):
    a = pf(formula)
    if not a: return None
    tm = sum(a[el]*ATOM_DB[el][0] for el in a)
    tz = sum(a[el]*ATOM_DB[el][3] for el in a)
    na = sum(a.values())
    ar = sum(a[el]*ATOM_DB[el][2] for el in a)/na
    l = 2*ar*1e-10
    td = sum(a[el]*ATOM_DB[el][1] for el in a)/na
    if td == 0: return None
    V = l**3
    f = 1.0-0.3*(1.0-1.0/na)
    es = 0
    els = list(a.keys())
    for i in range(len(els)):
        for j in range(i+1,len(els)):
            es += 1.0/(a[els[i]]*ATOM_DB[els[i]][0]*AMU) + 1.0/(a[els[j]]*ATOM_DB[els[j]][0]*AMU)
    if not es:
        mi = tm*AMU/na
        es = (na*(na-1)/2)*2.0/mi
    G = (1.0/l)*math.sqrt((1.0-f)*es)
    od = td*KB/HBAR
    dd = math.sqrt(abs((C2/l**2)*(3*HBAR/(4*od))*(1-f)*es))
    B = tm*td**2*KB/V*1e-3
    hf = any(el in HF_EL for el in a)
    return {'M':tm,'Z':tz,'N':na,'l':l,'tD':td,'V':V,'G':G,'dd0':dd,'B':B,'hf':hf}

data = []
with open("superconductors_deduplicated.csv",'r',encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc <= 0: continue
        mp = cp(row['材料(化学式)'])
        if mp is None or mp['dd0'] == 0: continue
        cat = row['类别']
        gl = 1 if cat in GL1_CATS else (2 if cat in GL2_CATS else 1)
        j = CAT_J.get(cat,0)
        if mp['hf'] and gl == 1: n = 1; j = 0
        else: n = CAT_N.get(cat,5)
        gn = RIEMANN_ZEROS[n-1]
        cas = j*(j+1)
        ke = tc**2*9*LN2/(8*mp['dd0']**2*mp['tD'])
        formula = row['材料(化学式)']
        data.append({**mp,'formula':formula,'cat':cat,'tc':tc,'ke':ke,'gl':gl,'j':j,'cas':cas,'gn':gn,'n':n})

nd = len(data)
y = np.array([math.log(d['ke']) for d in data])

def bX(lam):
    X = np.zeros((nd,7))
    for i,d in enumerate(data):
        ge = d['gn']+lam*d['cas']
        X[i,0]=ge; X[i,1]=math.log(d['G']); X[i,2]=math.log(d['tD']); X[i,3]=math.log(d['B']); X[i,4]=math.log(d['N']); X[i,5]=math.log(d['V']); X[i,6]=1.0
    return X

def ob(lam):
    X = bX(lam[0]); c,_,_,_ = np.linalg.lstsq(X,y,rcond=None); return np.sum((y-X@c)**2)

r = minimize(ob, x0=[0.39], method='Nelder-Mead', options={'maxiter':10000})
LAM = r.x[0]
Xf = bX(LAM)
COEF,_,_,_ = np.linalg.lstsq(Xf,y,rcond=None)
A,P,Q,R,S,T,Bc = COEF

# LOOCV
preds = []
for i in range(nd):
    Xtr = np.delete(Xf,i,axis=0); ytr = np.delete(y,i)
    c,_,_,_ = np.linalg.lstsq(Xtr,ytr,rcond=None)
    d = data[i]
    ge = d['gn']+LAM*d['cas']
    lk = c[0]*ge+c[1]*math.log(d['G'])+c[2]*math.log(d['tD'])+c[3]*math.log(d['B'])+c[4]*math.log(d['N'])+c[5]*math.log(d['V'])+c[6]
    tp = math.sqrt(8*d['dd0']**2*math.exp(lk)*d['tD']/(9*LN2))
    er = abs(tp-d['tc'])/d['tc']
    preds.append((d['formula'],d['cat'],d['gl'],d['j'],d['n'],ge,d['G'],d['tD'],d['dd0'],d['B'],d['N'],d['V'],math.exp(lk),tp,d['tc'],er,d['hf']))

preds.sort(key=lambda x: x[15])

# 输出所有材料
print(f"所有{nd}个材料的Tc预测 (按误差排序)")
print(f"{'='*120}")
print(f"{'#':>3} {'材料':<25} {'类别':<20} {'GL':>2} {'j':>1} {'n':>2} {'γ_eff':>7} {'Tc_exp':>8} {'Tc_pred':>8} {'误差%':>8} {'比值':>6}")
print(f"{'-'*120}")
for i,p in enumerate(preds):
    ratio = p[13]/p[14] if p[14] > 0 else 0
    hf_mark = " [HF]" if p[16] else ""
    print(f"{i+1:>3} {p[0]:<25} {p[1]:<20} GL{p[2]} {p[3]} {p[4]:>2} {p[5]:>7.2f} {p[14]:>8.2f} {p[13]:>8.2f} {p[15]*100:>8.1f}% {ratio:>6.2f}{hf_mark}")

# 统计
errs = np.array([p[15] for p in preds])
print(f"\n{'='*80}")
print(f"统计 (LOOCV, {nd}个材料)")
print(f"{'='*80}")
print(f"中位误差: {np.median(errs)*100:.1f}%")
print(f"均值误差: {np.mean(errs)*100:.1f}%")
print(f"2倍内: {np.mean(errs<=1)*100:.1f}% ({sum(errs<=1)}/{nd})")
print(f"5倍内: {np.mean(errs<=4)*100:.1f}% ({sum(errs<=4)}/{nd})")
print(f"10倍内: {np.mean(errs<=9)*100:.1f}% ({sum(errs<=9)}/{nd})")
print(f"最佳: {min(errs)*100:.2f}% ({preds[0][0]})")
print(f"最差: {max(errs)*100:.0f}% ({preds[-1][0]})")