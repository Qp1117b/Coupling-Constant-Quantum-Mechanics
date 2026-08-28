"""深入探索嘉当矩阵=能动张量=哈密顿量的物理含义

如果嘉当矩阵同时是能动张量和哈密顿量, 那么质量进入方式应满足:
1. 能动张量: T_00 = ρc² (质量密度), T_ij = pδ_ij + ρv_iv_j (动量流)
2. 哈密顿量: H|ψ> = E|ψ>, E = mc² + ℏω(n+1/2)
3. 希格斯: m = y·v/√2, 质量来自Yukawa耦合×VEV

探索方向:
A. 能动张量分量分解: 嘉当矩阵分解为"质量密度"部分+"动能"部分+"势能"部分
B. 哈密顿量本征值修正: 本征值直接含mc²项
C. 希格斯场形变展开: C(v) = C_0 + v·δC + v²·δC²
D. 规范群破缺: G→H, 嘉当矩阵简化, 破缺方向获得质量
E. 相对论修正: 检查重费米子系统是否s→1
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
                  89: {(5,3): 0, (6,2): 1}, 90: {(5,3): 0, (6,2): 2}, 96: {(5,3): 7, (6,2): 1}}
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

def build_Cmol(atoms, s=0.5, mode='cosh'):
    """不同质量修正模式的嘉当矩阵"""
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
            t0 = 0.1 * math.exp(-(ri + rj) / 3.0)
            if (binfo[1] == 'd' and bjinfo[1] == 'p') or (binfo[1] == 'p' and bjinfo[1] == 'd'): t0 *= 1.5

            if mi != mj:
                ratio = mi / mj
                log_r = math.log(ratio)

                if mode == 'cosh':
                    t0 *= math.cosh(s * log_r)
                elif mode == 'power':
                    # 幂律修正: (mi*mj)^s / (mi^s * mj^s) = 1 (平凡)
                    # 改用: ((mi+mj)/2)^s / (mi*mj)^(s/2)
                    t0 *= ((mi + mj) / 2)**s / (mi * mj)**(s/2)
                elif mode == 'sqrt_ratio':
                    # √(mi/mj) + √(mj/mi) / 2 = cosh(0.5*ln(mi/mj))
                    # 但用不同方式: (√mi + √mj)² / (2*√(mi*mj))
                    t0 *= (math.sqrt(mi) + math.sqrt(mj))**2 / (2 * mi * mj)
                elif mode == 'higgs_exp':
                    # 希格斯指数展开: 1 + s²·(ln(mi/mj))²/2 + ...
                    # 取前两项: 1 + (s·ln(mi/mj))²/2
                    t0 *= (1 + (s * log_r)**2 / 2)
                elif mode == 'am_gm':
                    # 算术平均/几何平均 (s=0.5的精确形式)
                    t0 *= (mi + mj) / (2 * math.sqrt(mi * mj))
                elif mode == 'rms_gm':
                    # 均方根/几何平均 (s=1的精确形式)
                    t0 *= math.sqrt((mi**2 + mj**2) / 2) / math.sqrt(mi * mj)
                elif mode == 'harmonic':
                    # 调和平均/几何平均
                    t0 *= 2 * mi * mj / ((mi + mj) * math.sqrt(mi * mj))
                elif mode == 'energy_tensor':
                    # 能动张量分解: T_ij = T_mass + T_kinetic + T_potential
                    # T_mass ~ (mi + mj)/2 (质量密度)
                    # T_kinetic ~ √(mi*mj) (动能, 几何平均)
                    # T_potential ~ 1/(1/mi + 1/mj) (势能, 调和平均)
                    # 比例: T_mass / T_kinetic = (mi+mj)/(2√(mi*mj)) = cosh(0.5*ln)
                    t0 *= (mi + mj) / (2 * math.sqrt(mi * mj))
                elif mode == 'weyl_norm':
                    # Weyl群归一化: 根向量长度归一化
                    # |α_i'| = |α_i| * √mi, 归一化后 cosh(0.5*ln(mi/mj))
                    t0 *= math.cosh(0.5 * log_r)

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

def solve_tc(formula, s=0.5, mode='cosh', eq8_coef=1.5):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None
    C, bi = build_Cmol(atoms, s=s, mode=mode)
    els = list(atoms.keys()); n_atoms = sum(atoms.values())
    ev = np.sort(np.linalg.eigvalsh(C))
    if len(ev) < 2: return None
    sg = max(ev[1] - ev[0], 0.05)
    m_ev = np.mean(ev); aniso = np.std(ev / m_ev if m_ev > 0 else ev)
    avg_r = sum(atoms[el] * ATOM_DB[el][2] for el in els) / n_atoms
    l = max(2 * avg_r * 1e-10, 1e-20)
    theta_d = sum(atoms[el] * ATOM_DB[el][1] for el in els) / n_atoms
    if theta_d <= 0: return None
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
    eq8_term = eq8_coef * COEF_EQUATION8 * dd0_sq
    dp = 0; d0 = 0; f_count = 0
    for el in els:
        z = ATOMIC_NUMBERS.get(el, 50); vo = valence_orbitals(z)
        hd = hp = False
        for l_qn, occ, cap in vo:
            if l_qn == 2: hd = True
            if l_qn == 1: hp = True
            if l_qn == 2 and occ == 0: d0 += atoms[el]
        if hd and hp: dp += atoms[el]
        config = madelung_config(z)
        for (n_qn, l_qn), occ in config.items():
            if l_qn == 3 and 0 < occ < 14: f_count += atoms[el]; break
    dp /= n_atoms; d0 /= n_atoms; f_frac = f_count / n_atoms
    o_frac = atoms.get('O', 0) / n_atoms
    nc = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
          + eq8_term + 0.05 * dp + C_O * o_frac)
    gn = interpolate_gamma_n(nc)
    K0 = C_GAMMA * math.exp(AG_THEORY * gn)
    K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    suppress = math.exp(-C_F_SUPP * f_frac) * math.exp(-3.0 * d0)
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress
    return Tc

data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

def eval_mode(mode, s=0.5, label=""):
    errs = []; cat_errs = {}
    for d in data:
        tc_pred = solve_tc(d['f'], s=s, mode=mode)
        if tc_pred is None or tc_pred <= 0: continue
        e = sym_err(tc_pred, d['tc'])
        errs.append(e)
        if d['cat'] not in cat_errs: cat_errs[d['cat']] = []
        cat_errs[d['cat']].append(e)
    if not errs: return 0
    errs.sort()
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    print(f"{label:55s}: n={len(errs):3d}, 2倍内{w2:.1f}%, 中位{errs[len(errs)//2]*100:.1f}%")
    return w2

print("="*70)
print("嘉当矩阵=能动张量=哈密顿量: 不同质量修正模式")
print("="*70)

modes = [
    ('cosh', 0.0, "无修正 (s=0)"),
    ('cosh', 0.5, "cosh(0.5·ln) [标准]"),
    ('cosh', 1.0, "cosh(ln) [纯希格斯s=1]"),
    ('am_gm', 0, "算术平均/几何平均 [s=0.5精确]"),
    ('rms_gm', 0, "均方根/几何平均 [s=1精确]"),
    ('harmonic', 0, "调和平均/几何平均"),
    ('energy_tensor', 0, "能动张量分解: T_mass/T_kinetic"),
    ('weyl_norm', 0, "Weyl群根向量归一化"),
    ('sqrt_ratio', 0, "(√mi+√mj)²/(2·mi·mj)"),
    ('higgs_exp', 0.5, "希格斯指数展开: 1+(s·ln)²/2"),
    ('higgs_exp', 1.0, "希格斯指数展开: 1+(ln)²/2"),
]

print("\n--- 不同质量修正模式 ---")
best_w2 = 0; best_label = ""
for mode, s, label in modes:
    w2 = eval_mode(mode, s=s, label=label)
    if w2 > best_w2:
        best_w2 = w2; best_label = label

print(f"\n最佳: {best_label} ({best_w2:.1f}%)")

# 分析: 不同平均的物理含义
print(f"\n{'='*70}")
print("不同平均的物理含义与希格斯机制关系")
print("="*70)

pairs = [('H','La'), ('H','S'), ('C','O'), ('Nb','Sn'), ('Fe','Se'), ('Pb','C')]
print(f"\n{'原子对':10s} {'m_i/m_j':>8s} {'AM/GM':>8s} {'RMS/GM':>8s} {'HM/GM':>8s} {'cosh(0.5ln)':>12s} {'cosh(ln)':>10s}")
for el1, el2 in pairs:
    m1 = ATOM_DB[el1][0]; m2 = ATOM_DB[el2][0]
    ratio = m1 / m2
    am_gm = (m1 + m2) / (2 * math.sqrt(m1 * m2))
    rms_gm = math.sqrt((m1**2 + m2**2) / 2) / math.sqrt(m1 * m2)
    hm_gm = 2 * m1 * m2 / ((m1 + m2) * math.sqrt(m1 * m2))
    cosh_half = math.cosh(0.5 * math.log(ratio))
    cosh_full = math.cosh(math.log(ratio))
    print(f"{el1+'-'+el2:10s} {ratio:8.3f} {am_gm:8.3f} {rms_gm:8.3f} {hm_gm:8.3f} {cosh_half:12.3f} {cosh_full:10.3f}")

print(f"""
物理对应:
  算术平均/几何平均 (AM/GM) = cosh(0.5·ln(m_i/m_j))  ← s=0.5, 非相对论极限
  均方根/几何平均 (RMS/GM) = cosh(ln(m_i/m_j))      ← s=1, 纯希格斯
  调和平均/几何平均 (HM/GM) = 1/cosh(0.5·ln(m_i/m_j)) ← s=-0.5, 逆修正

  AM/GM ≥ 1 (量子-经典偏离因子, 永远增强耦合)
  RMS/GM ≥ AM/GM (更强增强, 纯希格斯过强)
  HM/GM ≤ 1 (减弱耦合, 物理不合理)

  能动张量分解:
    T_mass = (m_i + m_j)/2  (质量密度, 算术平均)
    T_kinetic = √(m_i·m_j)  (动能, 几何平均)
    T_mass / T_kinetic = AM/GM = cosh(0.5·ln)  ← 自然导出s=0.5!

  希格斯机制:
    纯Yukawa → RMS/GM = cosh(ln) → s=1 (过强)
    非相对论 → AM/GM = cosh(0.5·ln) → s=0.5 (最佳)
    物理来源: T_mass/T_kinetic, 质量密度与动能的比值
""")