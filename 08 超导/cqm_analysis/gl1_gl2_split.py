"""完整分化树整合：GL(1)/GL(2)通道分离验证

分化树 → Tc公式对应:
  运动 → 惯性(希格斯) + 能动张量(嘉当投影) + 作用量(二阶层动力学)
  超导 = GL(1)+GL(2)自守形式选择
    常规s波: GL(1)非平凡 + GL(2)平凡
    非常规d/p波: GL(1)非平凡 + GL(2)非平凡

当前问题: 所有谱特征(各向异性+偏度+峰度)都进入同一个n_c→γ_n(GL(1)谱)
  但偏度/峰度是高阶矩, 属于GL(2)侧(非常规超导)

新结构:
  GL(1)通道(常规): 谱间隙 + 各向异性(2阶矩) + eq8 + o_frac → γ_n → K_GL1
  GL(2)通道(非常规): 偏度(3阶矩) + 峰度(4阶矩) + dp_hybrid → η_m → K_GL2
  K_eff = K_GL1 · K_GL2 · G^(-3/4) · θ_D^(9/8)

已有研究:
  GL(2)零点差: d波=2.196681962(GAMMA_D_GL2), p波=2.128515269
  GL(2)贡献约为GL(1)的31-32%
  Ŝ_2谱: η_j = s·C_2(j)·κ_pair·(3-d_pair)^α·σ_eff
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
GAMMA_D_GL2 = 2.196681962  # d波零点差(GL(2))
GAMMA_P_GL2 = 2.128515269  # p波零点差(GL(2))
C_ANISO = GAMMA_D_GL2 / (2 * math.pi)
B_THEORY = 8 * math.pi / 3
LAM0_THEORY = 1.0 / math.e
C_O = B_THEORY**2 * 0.25 / (3 * 8 * LAM0_THEORY**2)
C_F_SUPP = BETA / math.sqrt(3)
T0_BASE = 0.1

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

def solve_tc(formula, mode="current"):
    """多种GL(1)/GL(2)分离模式

    mode:
      "current": 当前框架(所有项进入同一个n_c)
      "split": GL(1)/GL(2)通道分离
      "split_exp": 分离+GL(2)指数贡献
      "split_linear": 分离+GL(2)线性贡献
    """
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

    if mode == "current":
        # 当前框架: 所有项进入同一个n_c
        nc = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
              + T0_BASE * skew + T0_BASE * kurt
              + eq8_term + 0.05 * dp + C_O * o_frac)
        gn = interpolate_gamma_n(nc)
        K0 = C_GAMMA * math.exp(AG_THEORY * gn)
        K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    elif mode == "split":
        # GL(1)/GL(2)通道分离
        # GL(1): 谱间隙 + 各向异性(2阶矩) + eq8 + o_frac(氧介导s波)
        n_gl1 = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
                 + eq8_term + C_O * o_frac)
        # GL(2): 偏度(3阶矩) + 峰度(4阶矩) + dp_hybrid(d-p杂化d波)
        n_gl2 = T0_BASE * skew + T0_BASE * kurt + 0.05 * dp

        gn = interpolate_gamma_n(n_gl1)
        K_gl1 = C_GAMMA * math.exp(AG_THEORY * gn)

        # GL(2)贡献: 通过零点差GAMMA_D_GL2标度
        eta_m = n_gl2 * GAMMA_D_GL2
        K_gl2 = math.exp(AG_THEORY * eta_m) if eta_m > 0 else 1.0

        K_eff = K_gl1 * K_gl2 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    elif mode == "split_exp":
        # 分离 + GL(2)指数贡献(负η_m抑制, 正η_m增强)
        n_gl1 = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
                 + eq8_term + C_O * o_frac)
        n_gl2 = T0_BASE * skew + T0_BASE * kurt + 0.05 * dp

        gn = interpolate_gamma_n(n_gl1)
        K_gl1 = C_GAMMA * math.exp(AG_THEORY * gn)

        # GL(2): η_m用GAMMA_D_GL2标度, 指数贡献
        eta_m = n_gl2 * GAMMA_D_GL2
        K_gl2 = math.exp(AG_THEORY * abs(eta_m))

        K_eff = K_gl1 * K_gl2 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    elif mode == "split_linear":
        # 分离 + GL(2)线性贡献
        n_gl1 = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
                 + eq8_term + C_O * o_frac)
        n_gl2 = T0_BASE * skew + T0_BASE * kurt + 0.05 * dp

        gn = interpolate_gamma_n(n_gl1)
        K_gl1 = C_GAMMA * math.exp(AG_THEORY * gn)

        # GL(2): 线性修正 1 + α·n_gl2
        K_gl2 = 1.0 + AG_THEORY * GAMMA_D_GL2 * n_gl2

        K_eff = K_gl1 * K_gl2 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)
    elif mode == "split_additive":
        # 分离 + GL(2)加性贡献到γ_n
        n_gl1 = (4.00 + 0.50 * math.log(1/sg) + C_ANISO * aniso
                 + eq8_term + C_O * o_frac)
        n_gl2 = T0_BASE * skew + T0_BASE * kurt + 0.05 * dp

        gn_gl1 = interpolate_gamma_n(n_gl1)
        # GL(2)谱: 用GAMMA_D_GL2作为零点差, n_gl2作为"序号"
        gn_gl2 = n_gl2 * GAMMA_D_GL2  # GL(2)谱贡献

        # 总γ = GL(1)γ + GL(2)γ
        gn_total = gn_gl1 + gn_gl2
        K0 = C_GAMMA * math.exp(AG_THEORY * gn_total)
        K_eff = K0 * max(G, 1e-6)**(-0.75) * theta_d**(1.125)

    suppress = math.exp(-C_F_SUPP * f_frac) * math.exp(-3.0 * d0)
    Tc = math.sqrt(8 * dd0**2 * K_eff * theta_d / (9 * LN2)) * suppress
    return Tc, {'n_gl1': n_gl1 if mode != "current" else nc,
                'n_gl2': n_gl2 if mode != "current" else 0,
                'gn': gn if mode in ("current", "split", "split_exp", "split_linear") else gn_total}

data = []
with open(os.path.join(os.path.dirname(__file__), 'superconductors_deduplicated.csv'), 'r', encoding='utf-8-sig') as fh:
    for row in csv.DictReader(fh):
        try: tc = float(row['临界温度 Tc (K)'])
        except: continue
        if tc > 0: data.append({'f': row['材料(化学式)'], 'cat': row['类别'], 'tc': tc})

print("="*80)
print("GL(1)/GL(2)通道分离验证")
print("分化树: 偏度/峰度→GL(2)侧, 各向异性→GL(1)侧")
print("="*80)

modes = ["current", "split", "split_exp", "split_linear", "split_additive"]
labels = {
    "current": "当前框架(混合)",
    "split": "GL(1)/GL(2)分离(乘性)",
    "split_exp": "GL(1)/GL(2)分离(指数)",
    "split_linear": "GL(1)/GL(2)分离(线性)",
    "split_additive": "GL(1)/GL(2)分离(加性γ)",
}

for mode in modes:
    print(f"\n--- {labels[mode]} ---")
    all_errs = []; cat_errs = {}
    for d in data:
        tc_pred, info = solve_tc(d['f'], mode=mode)
        if tc_pred and tc_pred > 0:
            e = sym_err(tc_pred, d['tc'])
            all_errs.append(e)
            cat_errs.setdefault(d['cat'], []).append(e)
    if all_errs:
        all_errs.sort()
        w2 = sum(1 for e in all_errs if e <= 1.0) / len(all_errs) * 100
        w5 = sum(1 for e in all_errs if e <= 4.0) / len(all_errs) * 100
        print(f"  总体: n={len(all_errs)}, 2倍内{w2:.1f}%, 5倍内{w5:.1f}%, 中位{all_errs[len(all_errs)//2]*100:.1f}%")
        for cat in sorted(cat_errs.keys()):
            errs = sorted(cat_errs[cat])
            w2c = sum(1 for e in errs if e <= 1.0) / len(errs) * 100
            tag = ""
            if cat in ['铜氧化物高温超导体', '铁基超导体', '有机超导体']:
                tag = " ←GL(2)非平凡"
            elif cat in ['A15结构金属间化合物', '元素超导体(常压)']:
                tag = " ←GL(2)平凡"
            print(f"  {cat:25s}: 2倍内{w2c:5.0f}%, 中位{errs[len(errs)//2]*100:7.0f}%{tag} ({len(errs)}个)")

print(f"\n{'='*80}")
print("GL(2)非平凡 vs 平凡: 偏度/峰度分布")
print("="*80)

gl2_cats = ['铜氧化物高温超导体', '铁基超导体', '有机超导体']
gl1_cats = ['A15结构金属间化合物', '元素超导体(常压)', '合金超导体']

for group, cats in [("GL(2)非平凡(非常规)", gl2_cats), ("GL(2)平凡(常规)", gl1_cats)]:
    print(f"\n--- {group} ---")
    for cat in cats:
        items = [d for d in data if d['cat'] == cat]
        skews = []; kurts = []; n_gl2s = []
        for d in items:
            atoms = parse_formula(d['f'])
            if not atoms: continue
            C, bi = build_Cmol(atoms)
            ev = np.sort(np.linalg.eigvalsh(C))
            if len(ev) < 2: continue
            m_ev = np.mean(ev); ev_std = np.std(ev)
            if ev_std <= 0: continue
            sk = np.mean(((ev - m_ev) / ev_std) ** 3)
            ku = np.mean(((ev - m_ev) / ev_std) ** 4) - 3
            skews.append(sk); kurts.append(ku)
            dp, _, _, _ = compute_features(atoms)
            n_gl2s.append(T0_BASE * sk + T0_BASE * ku + 0.05 * dp)
        if skews:
            print(f"  {cat:25s}: 偏度均值={np.mean(skews):.3f}, 峰度均值={np.mean(kurts):.3f}, n_GL2均值={np.mean(n_gl2s):.4f}")