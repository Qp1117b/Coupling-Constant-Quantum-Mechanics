"""从希格斯机制推导嘉当矩阵质量修正

物理推导链:
1. 希格斯VEV: <phi> = v*n_hat, 费米子质量 m_i = y_i * v / sqrt(2)
2. 根向量含Yukawa耦合: alpha_i -> alpha_i * y_i
3. 嘉当矩阵变形: H_ij = C_ij * cosh(ln(y_i/y_j)) = C_ij * (y_i^2+y_j^2)/(2*y_i*y_j)
4. 由于 m_i = y_i * v / sqrt(2), y_i = m_i * sqrt(2) / v
   -> H_ij = C_ij * cosh(ln(m_i/m_j))  (s=1, 纯希格斯)
5. 非相对论修正: y_eff = sqrt(m*E) * sqrt(2) / v
   -> H_ij = C_ij * cosh(0.5 * ln(m_i/m_j))  (s=0.5)

嘉当矩阵 = 能动张量 = 哈密顿量:
- 能动张量: T_00 = rho*c^2 = Sigma m_i*n_i*c^2/V (质量密度, 来自希格斯)
- 哈密顿量: H|psi> = E|psi>, E_n = hbar*omega*(n+1/2) + m*c^2 (质量通过mc^2进入)
- 嘉当矩阵统一两者: C_ij编码T_mu_nu的离散版本, 本征值=能量本征值
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

def build_Cmol_higgs(atoms, s=0.5, higgs_mode='standard'):
    """从希格斯机制推导的嘉当矩阵质量修正

    higgs_mode:
    - 'standard': cosh(s*ln(mi/mj)) -- 标准根向量归一化
    - 'yukawa': (y_i^2+y_j^2)/(2*y_i*y_j) -- 纯Yukawa, s=1
    - 'nr': cosh(0.5*ln(mi/mj)) -- 非相对论修正, s=0.5
    - 'full': cosh(s*ln(mi/mj)) + gauge_correction -- 含规范玻色子质量修正
    - 'trace': 对角元也修正(能动张量迹修正)
    """
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

    # 希格斯VEV方向: 用最重原子的方向作为破缺方向
    masses = [ATOM_DB[el][0] for el in els if el in ATOM_DB]
    v_higgs = max(masses) if masses else 100.0  # 希格斯VEV尺度

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
                if higgs_mode == 'yukawa':
                    # 纯Yukawa: (y_i^2+y_j^2)/(2*y_i*y_j) = cosh(ln(mi/mj))
                    y_i = mi * math.sqrt(2) / v_higgs
                    y_j = mj * math.sqrt(2) / v_higgs
                    t0 *= (y_i**2 + y_j**2) / (2 * y_i * y_j)
                elif higgs_mode == 'nr':
                    # 非相对论: y_eff = sqrt(m*E)*sqrt(2)/v -> cosh(0.5*ln(mi/mj))
                    t0 *= math.cosh(0.5 * math.log(mi / mj))
                elif higgs_mode == 'full':
                    # 含规范玻色子质量修正: 基本cosh + 秩1修正
                    base = math.cosh(s * math.log(mi / mj))
                    # 规范玻色子质量 m_W^2 = g^2*v^2/4, 秩1修正 ~ (mi*mj)/(v^2)
                    gauge_corr = (mi * mj) / (v_higgs**2) * 0.01
                    t0 *= (base + gauge_corr)
                elif higgs_mode == 'trace':
                    # 能动张量迹修正: 质量密度进入对角
                    t0 *= math.cosh(s * math.log(mi / mj))
                else:
                    t0 *= math.cosh(s * math.log(mi / mj))

            for a in range(si):
                for b in range(sj): C[idx_i+a, idx_j+b] = t0; C[idx_j+b, idx_i+a] = t0
            idx_j += sj

        # 能动张量迹修正: 对角元含质量密度
        if higgs_mode == 'trace':
            mass_density = mi / v_higgs
            for a in range(si):
                C[idx_i+a, idx_i+a] += 0.01 * mass_density

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

def solve_tc(formula, s=0.5, higgs_mode='standard', eq8_coef=1.5):
    atoms = {}
    for el, cnt in re.findall(r'([A-Z][a-z]?)(\d*\.?\d*)', formula):
        if el in ATOM_DB: atoms[el] = atoms.get(el, 0) + (float(cnt) if cnt else 1.0)
    if not atoms: return None
    C, bi = build_Cmol_higgs(atoms, s=s, higgs_mode=higgs_mode)
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

def eval_mode(s, higgs_mode, eq8_coef=1.5, label=""):
    errs = []; cat_errs = {}
    for d in data:
        tc_pred = solve_tc(d['f'], s=s, higgs_mode=higgs_mode, eq8_coef=eq8_coef)
        if tc_pred is None or tc_pred <= 0: continue
        e = sym_err(tc_pred, d['tc'])
        errs.append(e)
        if d['cat'] not in cat_errs: cat_errs[d['cat']] = []
        cat_errs[d['cat']].append(e)
    if not errs: return 0
    errs.sort()
    w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
    print(f"{label:50s}: n={len(errs):3d}, 2倍内{w2:.1f}%, 中位{errs[len(errs)//2]*100:.1f}%")
    for cat in ['氢化物高压超导体', '铜氧化物高温超导体', 'A15结构金属间化合物', '铁基超导体']:
        if cat in cat_errs and len(cat_errs[cat]) >= 3:
            ce = sorted(cat_errs[cat])
            cw2 = sum(1 for e in ce if e <= 1.0) / len(ce) * 100
            print(f"  {cat:20s}: 2倍内{cw2:.0f}% 中位{ce[len(ce)//2]*100:.0f}%")
    return w2

print("="*70)
print("从希格斯机制推导嘉当矩阵质量修正")
print("希格斯VEV → Yukawa耦合 → 根向量变形 → 嘉当矩阵修正")
print("="*70)

print("\n--- 希格斯机制不同模式 ---")
modes = [
    (0.0, 'standard', "无质量修正 (s=0)"),
    (0.5, 'standard', "标准根向量归一化 (s=0.5)"),
    (1.0, 'standard', "纯希格斯 s=1 (cosh(ln(mi/mj)))"),
    (0.5, 'nr', "非相对论修正 s=0.5 (cosh(0.5*ln))"),
    (1.0, 'yukawa', "纯Yukawa ((y_i²+y_j²)/(2y_iy_j))"),
    (0.5, 'full', "含规范玻色子修正 (cosh+gauge)"),
    (0.5, 'trace', "能动张量迹修正 (对角+非对角)"),
]

best_w2 = 0; best_label = ""
for s, mode, label in modes:
    w2 = eval_mode(s, mode, label=label)
    if w2 > best_w2:
        best_w2 = w2; best_label = label

print(f"\n最佳: {best_label} ({best_w2:.1f}%)")

# s精细扫描
print(f"\n--- s精细扫描 (standard模式) ---")
for s in [0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]:
    errs = []
    for d in data:
        tc_pred = solve_tc(d['f'], s=s, higgs_mode='standard')
        if tc_pred is None or tc_pred <= 0: continue
        errs.append(sym_err(tc_pred, d['tc']))
    if errs:
        errs.sort()
        w2 = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
        print(f"  s={s:.2f}: n={len(errs):3d}, 2倍内{w2:.1f}%, 中位{errs[len(errs)//2]*100:.1f}%")

# 物理分析
print(f"\n{'='*70}")
print("物理分析: 希格斯机制 vs 根向量归一化")
print("="*70)
print(f"""
推导链:
  希格斯VEV v → 费米子质量 m_i = y_i * v / √2
  Yukawa耦合进入根向量: α_i → α_i * y_i
  嘉当矩阵: C'_ij = C_ij * (y_i/y_j)  [非对称]
  Hermitian对称化: H_ij = C_ij * cosh(ln(y_i/y_j))
  = C_ij * (y_i² + y_j²) / (2*y_i*y_j)
  = C_ij * (m_i² + m_j²) / (2*m_i*m_j)  [因为 m ∝ y]
  = C_ij * cosh(ln(m_i/m_j))  [s=1, 纯希格斯]

非相对论修正:
  有效Yukawa: y_eff = √(m*E) * √2 / v  (E是典型能标)
  → cosh(ln(y_eff_i/y_eff_j)) = cosh(0.5*ln(m_i/m_j) + 0.5*ln(E_i/E_j))
  若 E_i ≈ E_j (同能级):
  → cosh(0.5*ln(m_i/m_j))  [s=0.5, 非相对论极限]

s=0.5的物理来源:
  非相对论极限下, Dirac方程的自旋-轨道耦合 ∝ 1/(mc²)
  有效质量 m_eff = √(m*E), Yukawa耦合含质量的平方根
  → 嘉当矩阵修正的指数 s = 1/2

嘉当矩阵 = 能动张量 = 哈密顿量:
  能动张量: T_00 = ρc² = Σm_i·n_i·c²/V (质量密度, 来自希格斯)
  哈密顿量: H|ψ⟩ = E|ψ⟩, E = ℏω(n+1/2) + mc² (质量通过mc²进入)
  嘉当矩阵统一: C_ij编码T_μν离散版本, 本征值=能量本征值
  希格斯机制: 质量同时进入T_00(质量密度)和H(本征值), 嘉当矩阵自然统一
""")