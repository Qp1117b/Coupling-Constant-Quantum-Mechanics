"""中子缺陷映射的深层结构分析

发现:
  1. 根向量归一化 cosh(0.5·ln(mi/mj)) = (mi+mj)/(2√mi·mj) → 48.7%
  2. 中子缺陷修正 exp(-κ·d/A) 在单一同位素数据上无效

深层物理:
  中子缺陷 d=N-Z 是连续参数(同位素变化)
  S(d) 应是参数化变换族, 满足:
    a. d=0 (N=Z, 轻元素): S=I (无修正)
    b. d>0 (N>Z, 重元素): S=f(d) (非平凡)
    c. 稳定线 d~0.4A^(2/3): S=f(Z) (隐含Z依赖)

  从核物理(SEMF): E_sym = a_a·d²/A (对称能)
  → g(d) 可能是 d²/A 依赖, 不是 d/A

  从CQM: "特殊变化"可能是
    a. 模形式 (Riemann零点关联)
    b. 自守表示 (嘉当矩阵改变表示)
    c. L-函数零点

本脚本: 分析核信息结构, 探索d²/A和其他特殊映射
"""
import math, csv, os, re, sys
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

BETA = 8 * math.pi + 1
C2 = 2.0 / 3.0
B_THEORY = 8 * math.pi / 3
MU_THEORY = 1.0 / (2 * math.sqrt(2))
LAM0_THEORY = 1.0 / math.e
AG_THEORY = 3.0 / (4 * math.pi * (1 - MU_THEORY))
GAMMA_D_GL2 = 2.196681962

RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
LN2 = math.log(2)
C_GAMMA = 7.77e11
COEF_EQUATION8 = 3 * BETA**2 / 16
M_PROTON = 1.007276; M_NEUTRON = 1.008665

ATOMIC_NUMBERS = {}
for _el, _z in [('H',1),('He',2),('Li',3),('Be',4),('B',5),('C',6),('N',7),('O',8),('F',9),('Ne',10),
    ('Na',11),('Mg',12),('Al',13),('Si',14),('P',15),('S',16),('Cl',17),('Ar',18),('K',19),('Ca',20),
    ('Sc',21),('Ti',22),('V',23),('Cr',24),('Mn',25),('Fe',26),('Co',27),('Ni',28),('Cu',29),('Zn',30),
    ('Ga',31),('Ge',32),('As',33),('Se',34),('Br',35),('Kr',36),('Rb',37),('Sr',38),('Y',39),('Zr',40),
    ('Nb',41),('Mo',42),('Tc',43),('Ru',44),('Rh',45),('Pd',46),('Ag',47),('Cd',48),('In',49),('Sn',50),
    ('Sb',51),('Te',52),('I',53),('Xe',54),('Cs',55),('Ba',56),('La',57),('Ce',58),('Pr',59),('Nd',60),
    ('Gd',64),('Tb',65),('Dy',66),('Ho',67),('Er',68),('Tm',69),('Yb',70),('Lu',71),('Hf',72),('Ta',73),
    ('W',74),('Re',75),('Os',76),('Ir',77),('Pt',78),('Au',79),('Hg',80),('Tl',81),('Pb',82),('Bi',83),
    ('Th',90),('Pa',91),('U',92),('Np',93),('Pu',94),('Am',95),('Cm',96)]:
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

def get_nuclear_info(el):
    Z = ATOMIC_NUMBERS.get(el, 50)
    mass_amu = ATOM_DB[el][0]
    N = round((mass_amu - Z * M_PROTON) / M_NEUTRON)
    A = Z + N; d = N - Z
    return Z, N, A, d

# ============================================================
# Part 1: 核信息结构分析
# ============================================================
print("="*70)
print("核信息结构: 质子Z vs 中子缺陷d vs 质量A")
print("="*70)
print(f"{'元素':5s} {'Z':>3s} {'N':>4s} {'A':>4s} {'d':>4s} {'d/A':>6s} {'d²/A':>7s} {'d/Z':>6s} {'Z/A':>6s}")
elements_all = ['H','Li','Be','B','C','N','O','F','Na','Mg','Al','Si','P','S','K','Ca','Ti','V','Cr','Fe','Co','Ni','Cu','Zn','As','Se','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Sn','Sb','Te','Cs','Ba','La','Ce','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Th']
for el in elements_all:
    Z, N, A, d = get_nuclear_info(el)
    print(f"{el:5s} {Z:3d} {N:4d} {A:4d} {d:4d} {d/A:6.3f} {d**2/A:7.2f} {d/Z:6.3f} {Z/A:6.3f}")

# ============================================================
# Part 2: 质量分解 Z vs d 的物理含义
# ============================================================
print(f"\n{'='*70}")
print("质量分解: M ≈ 2Z·m_n + d·m_n")
print("  质子分量(化学): 2Z·m_n → 嘉当矩阵C_mol(Z)")
print("  中子缺陷分量(振动): d·m_n → 转换矩阵S(d)")
print("="*70)

# 关键比值: 质子分量/总质量 vs 中子缺陷分量/总质量
print(f"\n{'元素':5s} {'M':>7s} {'2Z·mn':>7s} {'d·mn':>7s} {'质子%':>7s} {'中子缺陷%':>9s}")
for el in ['H','C','O','S','Ca','Fe','Cu','Nb','Sn','La','Pb','Th','U']:
    Z, N, A, d = get_nuclear_info(el)
    M = ATOM_DB[el][0]
    proton_part = 2 * Z * M_NEUTRON
    defect_part = d * M_NEUTRON
    print(f"{el:5s} {M:7.2f} {proton_part:7.2f} {defect_part:7.2f} {proton_part/M*100:6.1f}% {defect_part/M*100:8.1f}%")

# ============================================================
# Part 3: 算术/几何平均的物理含义
# ============================================================
print(f"\n{'='*70}")
print("根向量归一化: cosh(0.5·ln(mi/mj)) = (mi+mj)/(2√(mi·mj))")
print("  = 算术平均/几何平均 = 量子-经典偏离因子")
print("="*70)

pairs = [('H','La'),('H','S'),('H','C'),('H','Pb'),('C','O'),('C','S'),
         ('Nb','Sn'),('Fe','Se'),('O','Cu'),('Cu','O'),('Pb','Bi'),('La','H')]
print(f"\n{'原子对':8s} {'mi':>5s} {'mj':>5s} {'算术':>7s} {'几何':>7s} {'比值':>7s} {'ln(mi/mj)':>10s}")
for el1, el2 in pairs:
    m1 = ATOM_DB[el1][0]; m2 = ATOM_DB[el2][0]
    arith = (m1+m2)/2; geom = math.sqrt(m1*m2)
    ratio = arith/geom
    print(f"{el1+'-'+el2:8s} {m1:5.1f} {m2:5.1f} {arith:7.2f} {geom:7.2f} {ratio:7.3f} {math.log(m1/m2):10.3f}")

# ============================================================
# Part 4: 中子缺陷的特殊变化映射
# ============================================================
print(f"\n{'='*70}")
print("中子缺陷映射 S(d): 可能的特殊函数")
print("="*70)

# 对比不同映射形式
print(f"\n{'元素':5s} {'d':>4s} {'A':>4s} {'d/A':>6s} {'d²/A':>7s} {'d/Z²':>7s} {'√d/A':>7s} {'d/A^(2/3)':>10s}")
for el in ['H','Li','B','C','O','S','Ca','Fe','Cu','Nb','Sn','La','Pb','Th','U']:
    Z, N, A, d = get_nuclear_info(el)
    print(f"{el:5s} {d:4d} {A:4d} {d/A:6.3f} {d**2/A:7.2f} {d/Z**2:7.4f} {math.sqrt(abs(d))/A:7.4f} {d/A**(2/3):10.4f}")

# ============================================================
# Part 5: 同位素效应预测
# ============================================================
print(f"\n{'='*70}")
print("同位素效应: S(d)对不同同位素的预测")
print("="*70)

# Pb同位素
print("\nPb同位素 (Z=82):")
print(f"  {'同位素':8s} {'A':>4s} {'d':>4s} {'M(amu)':>7s} {'√(Z/A)':>7s} {'cosh(0.5·ln(M/207))':>20s}")
for A_iso in [204, 206, 207, 208]:
    d_iso = A_iso - 2*82
    M_iso = A_iso * 1.0  # 近似
    s_val = math.sqrt(82/A_iso)
    cosh_val = math.cosh(0.5 * math.log(M_iso/207.2))
    print(f"  Pb-{A_iso:<4d} {A_iso:4d} {d_iso:4d} {M_iso:7.1f} {s_val:7.4f} {cosh_val:20.6f}")

# H同位素
print("\nH同位素 (Z=1):")
print(f"  {'同位素':8s} {'A':>4s} {'d':>4s} {'M(amu)':>7s} {'√(Z/A)':>7s} {'备注':>10s}")
for name, A_iso, M_iso in [('H-1',1,1.008),('D-2',2,2.014),('T-3',3,3.016)]:
    d_iso = A_iso - 2*1
    s_val = math.sqrt(1/A_iso)
    note = 'd=0' if d_iso == 0 else f'd={d_iso}'
    print(f"  {name:8s} {A_iso:4d} {d_iso:4d} {M_iso:7.3f} {s_val:7.4f} {note:>10s}")

# Mg同位素 (超导MgB2的同位素效应)
print("\nMg同位素 (MgB2, Z=12):")
for A_iso in [24, 25, 26]:
    d_iso = A_iso - 2*12
    M_iso = A_iso * 1.0
    s_val = math.sqrt(12/A_iso)
    print(f"  Mg-{A_iso}: d={d_iso}, √(Z/A)={s_val:.4f}")

# ============================================================
# Part 6: 转换矩阵S的约束系统
# ============================================================
print(f"\n{'='*70}")
print("转换矩阵S的约束系统")
print("="*70)
print("""
S = S(Z, d) 满足:

1. Weyl群对称性: S保持嘉当矩阵块结构
   S = diag(s₁·I₁, s₂·I₃, s₃·I₄, ...)

2. Hermitian性: H = S†·C·S 对称
   → cosh(s·ln(mi/mj)) 形式

3. 量纲约束: [H] = 能量
   S ~ ℏ/(√m·l) → H = ℏ²/(m·l²)·C

4. 同位素约束: Z不变, d变化时
   δS/S = -α·δM/M = -α·m_n·δd/(2Z·m_n+d·m_n)
   BCS: α=0.5, CQM: α从Riemann零点导出

5. 轻元素约束: d=0 (N=Z)时
   S = √(Z/A) = √(Z/(2Z)) = 1/√2 (常数)
   → 所有轻元素(N=Z)有相同标度

6. 重元素约束: d>>Z时
   S ~ √(Z/d) → 0 (重元素耦合减弱)
   → Tc降低(与实验一致: 重元素Tc低)

7. 稳定线约束: d ~ 0.4·A^(2/3)
   S(stable) = √(Z/(Z + 0.4·A^(2/3)))
   → 隐含Z依赖(通过A~2Z)
""")

# 验证约束5: 轻元素d=0时S=1/√2
print("约束5验证 (d=0元素):")
for el in ['He','C','N','O','S','Ca','Mg','Ar']:
    Z, N, A, d = get_nuclear_info(el)
    if d == 0 or abs(d) <= 1:
        s_val = math.sqrt(Z/A) if A > 0 else 0
        print(f"  {el}: Z={Z}, A={A}, d={d}, √(Z/A)={s_val:.4f} (1/√2={1/math.sqrt(2):.4f})")

# 验证约束6: 重元素S→小
print("\n约束6验证 (重元素d大):")
for el in ['Pb','Bi','Th','U']:
    Z, N, A, d = get_nuclear_info(el)
    s_val = math.sqrt(Z/A) if A > 0 else 0
    print(f"  {el}: Z={Z}, A={A}, d={d}, √(Z/A)={s_val:.4f}")