"""分化树深度验证：当前框架的GL(1)/GL(2)统一结构

发现: GL(1)/GL(2)通道分离反而更差(48.7% vs 50.3%)
原因: 偏度/峰度是嘉当矩阵谱性质, 同时影响两个GL层

分化树确认:
  嘉当矩阵 = 能动张量 = 哈密顿量(统一体)
  → 所有谱矩从同一嘉当矩阵导出, 不应人为分离
  → GL(2)零点差GAMMA_D_GL2已通过C_ANISO=GAMMA_D_GL2/(2π)进入

新方向: SU(5)破缺分支规则 → o_fraction/dp_hybrid系数
  SU(5) → U(1)×SU(2)×SU(3)
  U(1) → GL(1) → 电磁配对 → o_fraction (系数C_O=5.40)
  SU(2) → GL(2) → 自旋配对 → dp_hybrid (系数0.05)
  分支规则应给出这两个系数的关系

新方向: 质数自组织 → 跃迁耦级Δu_n=2ln(n)
  质数在超导中的直接作用
"""
import sys, os, csv, re, math
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)
BETA = 8 * math.pi + 1
AG_THEORY = 3.0 / (4 * math.pi * (1 - 1.0/(2*math.sqrt(2))))
C_GAMMA = 7.77e11
COEF_EQUATION8 = 3 * BETA**2 / 16
GAMMA_D_GL2 = 2.196681962
C_ANISO = GAMMA_D_GL2 / (2 * math.pi)
B_THEORY = 8 * math.pi / 3
LAM0_THEORY = 1.0 / math.e
C_O = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
C_F_SUPP = BETA / math.sqrt(3)
T0_BASE = 0.1
C_DP = 0.05  # dp_hybrid系数

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

ATOMIC_NUMBERS = {}
for i, el in enumerate(['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar',
             'K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr',
             'Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe',
             'Cs','Ba','La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu',
             'Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi'], 1):
    ATOMIC_NUMBERS[el] = i
for _el, _z in [('Th',90),('Pa',91),('U',92),('Np',93),('Pu',94),('Am',95),('Cm',96)]:
    ATOMIC_NUMBERS[_el] = _z

A1 = np.array([[2.0]])
A3 = np.array([[2,-1,0],[-1,2,-1],[0,-1,2]])
A4 = np.array([[2,-1,0,0],[-1,2,-1,0],[0,-1,2,-1],[0,0,-1,2]])

def madelung_config(z):
    order = []
    for n in range(1, 8):
        for l in range(n): order.append((n+l, n, l))
    order.sort(key=lambda x: (x[0], x[1]))
    config = {}; remaining = z
    for _, n, l in order:
        cap = 2*(2*l+1); fill = min(remaining, cap)
        if fill > 0: config[(n, l)] = fill; remaining -= fill
        if remaining == 0: break
    exceptions = {57: {(4,3): 0, (5,2): 1}, 58: {(4,3): 1, (5,2): 1}, 64: {(4,3): 7, (5,2): 1},
                  89: {(5,3): 0, (6,2): 1}, 90: {(5,3): 0, (6,2): 2}, 96: {(5,3): 7, (6,2): 1},
                  24: {(3,2): 5, (4,0): 1}, 29: {(3,2): 10, (4,0): 1},
                  41: {(4,2): 4, (5,0): 1}, 42: {(4,2): 5, (5,0): 1},
                  44: {(4,2): 7, (5,0): 1}, 45: {(4,2): 9, (5,0): 1},
                  46: {(4,2): 10, (5,0): 0}, 47: {(4,2): 10, (5,0): 1}}
    if z in exceptions:
        for (n, l), occ in exceptions[z].items():
            if occ == 0: config.pop((n, l), None)
            else: config[(n, l)] = occ
    return config

def valence_orbitals(z):
    config = madelung_config(z)
    if not config: return []
    max_n = max(n for n, l in config)
    return [(l, occ, 2*(2*l+1)) for (n, l), occ in sorted(config.items(), reverse=True) if n >= max_n - 1]

def build_Cmol(atoms, s_root=0.5):
    els = list(atoms.keys()); blocks = []; bi = []
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50)
        for l, occ, cap in valence_orbitals(z):
            if l == 0: blocks.append(A1.copy()); bi.append((el, 's', 1))
            elif l == 1: blocks.append(A3.copy()); bi.append((el, 'p', 3))
            elif l == 2: blocks.append(A4.copy()); bi.append((el, 'd', 4))
    if not blocks: return np.array([[2.0]]), bi
    size = sum(b.shape[0] for b in blocks); C = np.zeros((size, size)); idx = 0
    for b in blocks:
        s_sz = b.shape[0]; C[idx:idx+s_sz, idx:idx+s_sz] = b; idx += s_sz
    idx_i = 0
    for i, binfo in enumerate(bi):
        si = binfo[2]; idx_j = idx_i + si
        mi = ATOM_DB[binfo[0]][0]
        for j, bjinfo in enumerate(bi[i+1:], start=i+1):
            sj = bjinfo[2]; ri = ATOM_DB[binfo[0]][2]; rj = ATOM_DB[bjinfo[0]][2]
            mj = ATOM_DB[bjinfo[0]][0]
            t0 = T0_BASE * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5
            if s_root != 0 and mi != mj:
                t0 *= math.cosh(s_root * math.log(mi / mj))
            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            idx_j += sj
        idx_i += si
    return C, bi

def interpolate_gamma_n(n):
    n_int = int(n); frac = n - n_int
    if n_int < 1: return RIEMANN_ZEROS[0]
    if n_int >= len(RIEMANN_ZEROS):
        return 2 * math.pi * n / math.log(n / (2 * math.pi)) if n > 6 else RIEMANN_ZEROS[-1]
    g_low = RIEMANN_ZEROS[n_int - 1]
    g_high = RIEMANN_ZEROS[n_int] if n_int < len(RIEMANN_ZEROS) else RIEMANN_ZEROS[-1]
    return g_low + frac * (g_high - g_low)

def sym_err(p, e):
    if p <= 0 or e <= 0: return float('inf')
    return max(p/e, e/p) - 1

def parse_formula(f):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', f):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    return atoms

def compute_features(atoms):
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    dp = 0; d0 = 0; f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
        hd = hp = False
        for l, occ, cap in vo:
            if l == 2: hd = True
            if l == 1: hp = True
            if l == 2 and occ == 0: d0 += atoms[el]
        if hd and hp: dp += atoms[el]
        config = madelung_config(z)
        for (n, l), occ in config.items():
            if l == 3 and 0 < occ < 14: f_count += atoms[el]; break
    return dp/n_atoms, d0/n_atoms, f_count/n_atoms, atoms.get('O',0)/n_atoms

def solve_tc(formula, c_o=None, c_dp=None):
    atoms = parse_formula(formula)
    if not atoms: return None, {}
    C, bi = build_Cmol(atoms)
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None, {}
    sg = max(ev[1] - ev[0], 0.05)
    m_ev = np.mean(ev); ev_std = np.std(ev)
    aniso = np.std(ev / m_ev if m_ev > 0 else ev)
    skew = np.mean(((ev - m_ev) / ev_std) ** 3) if ev_std > 0 else 0
    kurt = np.mean(((ev - m_ev) / ev_std) ** 4) - 3 if ev_std > 0 else 0

    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return None, {}
    n_eff = max(2, n_atoms); f_corr = 1.0 - 0.3 * (1.0 - 1.0 / n_eff)
    es = 0
    for i in range(len(els)):
        for j in range(i+1, len(els)):
            mi = atoms[els[i]] * ATOM_DB[els[i]][0] * AMU; mj = atoms[els[j]] * ATOM_DB[els[j]][0] * AMU
            es += (1/mi + 1/mj)
    if not es:
        mi = sum(atoms[el] * ATOM_DB[el][0] for el in els) * AMU / n_atoms
        es = max(1, n_eff * (n_eff-1) / 2) * 2.0 / mi
    omega_d = theta_d * KB / HBAR
    dd0_sq = (C2 / l**2) * (3 * HBAR / (4 * omega_d)) * (1 - f_corr) * es
    dd0 = math.sqrt(abs(dd0_sq))
    G = (1 / l) * math.sqrt((1 - f_corr) * es)
    eq8_term = 1.5 * COEF_EQUATION8 * dd0_sq
    dp, d0, f_frac, o_frac = compute_features(atoms)

    co = C_O if c_o is None else c_o
    cd = C_DP if c_dp is None else c_dp
    nc = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
          + T0_BASE * skew + T0_BASE * kurt
          + eq8_term + cd * dp + co * o_frac)
    gn = interpolate_gamma_n(nc)
    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    suppress = math.exp(-C_F_SUPP * f_frac) * math.exp(-3.0 * d0)
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress
    return Tc, {}

data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def evaluate(c_o=None, c_dp=None, label=""):
    errs = []; cat_errs = {}
    for d in data:
        tc_pred, _ = solve_tc(d['f'], c_o=c_o, c_dp=c_dp)
        if tc_pred and tc_pred > 0:
            e = sym_err(tc_pred, d['tc'])
            errs.append(e)
            cat_errs.setdefault(d['cat'], []).append(e)
    if not errs: return 0
    errs.sort()
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    print(f"{label:55s}: n={len(errs):3d}, 2倍内{w2:.1f}%, 中位{errs[len(errs)//2]*100:.1f}%")
    return w2

print("="*80)
print("A. SU(5)破缺分支规则: o_fraction/dp_hybrid系数关系")
print("="*80)

print(f"\n当前系数: C_O={C_O:.4f}(GL(1)电磁配对), C_DP={C_DP:.4f}(GL(2)自旋配对)")
print(f"比值 C_O/C_DP = {C_O/C_DP:.1f}")

# SU(5) → U(1)×SU(2)×SU(3) 分支规则
# 基本表示 5 → (1,1,1) + (0,2,3)
# U(1)权重: 1, SU(2)维度: 2
# 比值 = U(1)权重²/SU(2)Casimir = 1²/(2·1·(2+1)) = 1/6?
# 或比值 = U(1)权重/SU(2)维度 = 1/2?
# 或从B_THEORY和GAMMA_D_GL2导出

print(f"\n理论比值:")
print(f"  U(1)权重²/SU(2)Casimir = 1/(j(j+1)) = 1/2 = {1/2:.1f}")
print(f"  C_ANISO²/t0 = {C_ANISO**2/T0_BASE:.1f}")
print(f"  B_THEORY/GAMMA_D_GL2 = {B_THEORY/GAMMA_D_GL2:.1f}")
print(f"  (2π)²/GAMMA_D_GL2 = {(2*math.pi)**2/GAMMA_D_GL2:.1f}")

print(f"\n--- C_O/C_DP扫描(固定C_DP=0.05) ---")
for ratio in [50, 100, 108, 120, 150]:
    evaluate(c_o=ratio*C_DP, c_dp=C_DP, label=f"C_O/C_DP={ratio:.0f} (C_O={ratio*C_DP:.2f})")

print(f"\n--- C_O/C_DP扫描(固定C_O=5.40) ---")
for ratio in [50, 100, 108, 120, 150]:
    evaluate(c_o=C_O, c_dp=C_O/ratio, label=f"C_O/C_DP={ratio:.0f} (C_DP={C_O/ratio:.4f})")

print(f"\n{'='*80}")
print("B. 质数自组织: 跃迁耦级Δu_n=2ln(n)与超导")
print("="*80)

# 跃迁耦级: Δu_n = 2ln(n), n=2,4,6,...
# 资格条件: Δu_n ≥ 某阈值
# 质数n给出特殊性质

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
even_n = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

print(f"\n跃迁耦级 Δu_n = 2ln(n):")
print(f"{'n':>4s} {'Δu_n':>8s} {'质数?':>6s}")
for n in sorted(set(primes + even_n)):
    du = 2 * math.log(n)
    is_prime = "是" if n in primes else ""
    print(f"{n:4d} {du:8.4f} {is_prime:>6s}")

print(f"\n质数n的Δu_n vs 合数n的Δu_n:")
prime_dus = [2*math.log(p) for p in primes if p <= 50]
composite_dus = [2*math.log(n) for n in even_n if n not in primes]
print(f"  质数: 均值={np.mean(prime_dus):.4f}, std={np.std(prime_dus):.4f}")
print(f"  合数: 均值={np.mean(composite_dus):.4f}, std={np.std(composite_dus):.4f}")

print(f"\n{'='*80}")
print("C. 朗兰兹对应: L函数统一")
print("="*80)

print(f"\nGL(1) L函数 = ζ(s), 零点 = 黎曼零点γ_n")
print(f"  γ_1 = {RIEMANN_ZEROS[0]:.6f}")
print(f"  γ_2 = {RIEMANN_ZEROS[1]:.6f}")
print(f"  零点差 γ_2-γ_1 = {RIEMANN_ZEROS[1]-RIEMANN_ZEROS[0]:.6f}")

print(f"\nGL(2) L函数 = 椭圆曲线L(E,s)")
print(f"  d波(E: y²=x³-x, N=32): 零点差 = {GAMMA_D_GL2:.6f}")
print(f"  p波(E: y²=x³-1, N=27): 零点差 = {2.128515269:.6f}")

print(f"\n统一: C_ANISO = GAMMA_D_GL2/(2π) = {C_ANISO:.6f}")
print(f"  → GL(2)零点差通过各向异性系数进入n_c")
print(f"  → GL(1)零点通过γ_n进入K_0")
print(f"  → 两个L函数通过嘉当矩阵谱统一")

print(f"\n{'='*80}")
print("D. 当前框架的分化树完整对应")
print("="*80)

print(f"""
分化树 → Tc公式对应:
┌─ 惯性(希格斯→质量) → Δδ₀²~Σ(1/m) ──────────── 共同
├─ 几何(Regge→θ_D) → θ_D^(9/8) ──────────────── 共同
├─ 能动张量(嘉当谱投影):
│  ├─ GL(1): 谱间隙→log(1/sg), 各向异性→C_ANISO·aniso
│  ├─ GL(2): 零点差→C_ANISO=GAMMA_D_GL2/(2π)
│  └─ 高阶矩: 偏度→t0·skew, 峰度→t0·kurt
├─ 作用量(二阶层动力学):
│  ├─ GL(1): K_0=C·exp(AG·γ_n), γ_n=黎曼零点
│  └─ GL(2): 通过C_ANISO间接进入
├─ 配对机制(SU(5)破缺):
│  ├─ U(1)→GL(1): o_fraction·C_O (电磁配对s波)
│  └─ SU(2)→GL(2): dp_hybrid·C_DP (自旋配对d/p波)
└─ 方程8(同步条件): eq8_term=1.5·(3β²Δδ₀²/16)

当前精度: 50.3% (193材料2倍内, 中位99.7%)
""")