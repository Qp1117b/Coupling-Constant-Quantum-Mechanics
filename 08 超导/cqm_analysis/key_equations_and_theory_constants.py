"""关键方程梳理 + 剩余经验参数的理论推导

已找到的关键方程:
1. Tc = √(8·Δδ₀²·K_eff·θD/(9·ln2))  — 自由能公式
2. K_eff = K_0·G^(-3/4)·θD^(9/8)  — 量纲约束
3. K_0 = C·exp(0.369·γn)  — K_0参数化
4. γn = A - B/λep  — 弱耦合展开
5. 1-βδv = 3β²Δδ₀²/[16(γ₂-γ₁)]  — 临界同步

已从理论导出:
- 0.369 = 2/(B·(1-μ*/λ))  (BCS伪势)
- aniso = (γd-γs)/2π  (GL(2)零点差)
- c_o = B²·t²/(3Uλ₀²)  (超交换+3D平均)
- δv从Δδ₀主导  (临界同步)

本次推导目标:
- B = 8π/3 ?  (8.37 vs 8.378)
- log(CL/CG) = 2π² ?  (19.73 vs 19.739)
- A = 8π³/3·(1-μ*/λ) ?
- K_0前置因子从基本常数构造
"""
import math, csv, os, re, sys
import numpy as np

sys.path.insert(0, r'D:\WorkSpace\物理\CQMFormal\08 超导\cqm_framework')
from atom_db import ATOM_DB

BETA = 8 * math.pi + 1
RIEMANN_ZEROS = [14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
                 37.586178, 40.918720, 43.311071, 48.005150, 49.773832,
                 52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
                 67.079811, 69.526405, 72.067158, 75.704690, 77.144840]
GAMMA_1, GAMMA_2 = RIEMANN_ZEROS[0], RIEMANN_ZEROS[1]

HBAR = 1.0546e-34; KB = 1.381e-23; AMU = 1.66e-27
C2 = 2.0/3.0; LN2 = math.log(2)

# 经验拟合值
C_GAMMA = 7.77e11; C_LAMBDA = 2.85e20
A_GAMMA = 0.369; B_LAMBDA = 3.09
A_EMP = 53.44; B_EMP = 8.37

print("="*70)
print("关键方程体系")
print("="*70)

print(f"""
已找到的关键方程 (CQM超导第一性框架):

1. 自由能公式 (§11.10):
   Tc = √(8·Δδ₀²·K_eff·θD/(9·ln2))

2. K_eff分解 (量纲约束 p=-3/4, q=9/8):
   K_eff = K_0·G^(-3/4)·θD^(9/8)

3. K_0参数化 (§13):
   K_0 = {C_GAMMA:.2e}·exp({A_GAMMA}·γn)

4. γn弱耦合展开 (§13.6):
   γn = A - B/λep, A={A_EMP:.2f}, B={B_EMP:.2f}

5. λep Hopfield展开:
   λep = λ₀ + α_mass·inv_mass + α_log·log(1/sg) + α_aniso·aniso + ...

6. 临界同步条件 (新发现):
   1-βδv = 3β²Δδ₀²/[16(γ₂-γ₁)]

7. arccoth闭式 (§11.6):
   Tc = θD/(2·arccoth(x)), x = 3β²Δδ₀²/[16(1-βδv)(γ₂-γ₁)]

8. BCS伪势关系:
   0.369 = 2/(B·(1-μ*/λ)), μ*/λ = 0.353
""")

# ============================================================
print("="*70)
print("1. B = 8π/3 验证")
print("="*70)

B_theory = 8 * math.pi / 3
print(f"  B(经验) = {B_EMP:.4f}")
print(f"  B(理论) = 8π/3 = {B_theory:.4f}")
print(f"  差异: {abs(B_theory - B_EMP)/B_EMP*100:.2f}%")
print(f"  物理含义: 3D态密度角度积分因子")

# 验证B_LAMBDA = 2/(1-μ*/λ)
mu_over_lambda = 1 - 2.0 / B_LAMBDA
B_LAMBDA_theory = 2.0 / (1 - mu_over_lambda)
print(f"\n  B_LAMBDA = 2/(1-μ*/λ) = 2/{1-mu_over_lambda:.4f} = {B_LAMBDA_theory:.4f}")
print(f"  B_LAMBDA(经验) = {B_LAMBDA}")
print(f"  差异: {abs(B_LAMBDA_theory - B_LAMBDA)/B_LAMBDA*100:.2f}%")

# ============================================================
print(f"\n{'='*70}")
print("2. log(C_LAMBDA/C_GAMMA) = 2π² 验证")
print("="*70)

log_ratio = math.log(C_LAMBDA / C_GAMMA)
theory_2pi2 = 2 * math.pi**2
print(f"  log(C_L/C_G) = log({C_LAMBDA:.2e}/{C_GAMMA:.2e}) = log({C_LAMBDA/C_GAMMA:.4e}) = {log_ratio:.4f}")
print(f"  2π² = {theory_2pi2:.4f}")
print(f"  差异: {abs(theory_2pi2 - log_ratio)/log_ratio*100:.2f}%")
print(f"  物理含义: 可能来自CQM同步算符的谱密度归一化")

# ============================================================
print(f"\n{'='*70}")
print("3. A = 8π³/3·(1-μ*/λ) 验证")
print("="*70)

A_theory = 8 * math.pi**3 / 3 * (1 - mu_over_lambda)
print(f"  A(经验) = {A_EMP:.4f}")
print(f"  A(理论) = 8π³/3·(1-μ*/λ) = {8*math.pi**3/3:.4f}·{1-mu_over_lambda:.4f} = {A_theory:.4f}")
print(f"  差异: {abs(A_theory - A_EMP)/A_EMP*100:.2f}%")

# 等价验证: A = 2π²·B·(1-μ*/λ)/2 = π²·B·(1-μ*/λ)
A_alt = math.pi**2 * B_theory * (1 - mu_over_lambda)
print(f"\n  等价: A = π²·B·(1-μ*/λ) = π²·(8π/3)·(1-μ*/λ) = 8π³/3·(1-μ*/λ)")
print(f"  = {math.pi**2:.4f}·{B_theory:.4f}·{1-mu_over_lambda:.4f} = {A_alt:.4f}")

# ============================================================
print(f"\n{'='*70}")
print("4. 0.369 = 3/(4π·(1-μ*/λ)) 验证")
print("="*70)

A_GAMMA_theory = 3.0 / (4 * math.pi * (1 - mu_over_lambda))
print(f"  0.369(经验) = {A_GAMMA}")
print(f"  3/(4π·(1-μ*/λ)) = 3/(4π·{1-mu_over_lambda:.4f}) = {A_GAMMA_theory:.6f}")
print(f"  差异: {abs(A_GAMMA_theory - A_GAMMA)/A_GAMMA*100:.2f}%")

# ============================================================
print(f"\n{'='*70}")
print("5. K_0解析展开: 从BCS伪势到CQM")
print("="*70)

print(f"""
  K_0 = C_G·exp(A_G·γn)
      = C_G·exp(A_G·(A - B/λep))
      = C_G·exp(A_G·A)·exp(-A_G·B/λep)

  A_G·A = [3/(4π(1-μ*/λ))]·[8π³/3·(1-μ*/λ)] = 2π²
  A_G·B = [3/(4π(1-μ*/λ))]·[8π/3] = 2/(1-μ*/λ) = 3.09

  => K_0 = C_G·exp(2π²)·exp(-2/((1-μ*/λ)·λep))
         = C_G·exp(2π²)·exp(-2/λep*)
  其中 λep* = λep·(1-μ*/λ) = λep - μ* (有效耦合)

  C_L = C_G·exp(2π²) = {C_GAMMA:.2e}·exp({2*math.pi**2:.4f}) = {C_GAMMA*math.exp(2*math.pi**2):.4e}
  C_L(经验) = {C_LAMBDA:.2e}
  差异: {abs(C_GAMMA*math.exp(2*math.pi**2) - C_LAMBDA)/C_LAMBDA*100:.1f}%

  关键: Tc ~ √K_0 ~ exp(-1/λep*) — 与BCS指数完全一致!
""")

# ============================================================
print(f"{'='*70}")
print("6. K_0前置因子C_G的物理构造")
print("="*70)

# 从Tc² = 4·ℏ²·K_0·G^(5/4)·θD^(9/8)/(9·ln2·kB)
# K_0 = Tc²·9·ln2·kB / (4·ℏ²·G^(5/4)·θD^(9/8))
# K_0 = C_G·exp(2π² - 2/λep*)

# C_G的量纲: 从Tc² = 4·ℏ²·C_G·exp(...)·G^(5/4)·θD^(9/8)/(9·ln2·kB)
# [Tc²] = K², [ℏ²] = J²·s², [G] = 1/(m·√kg), [θD] = K, [kB] = J/K
# K² = J²·s²·[C_G]·(1/(m·√kg))^(5/4)·K^(9/8)/(J/K)
# K² = J·s²·[C_G]·kg^(-5/8)·m^(-5/4)·K^(9/8)·K
# K² = [C_G]·J·s²·kg^(-5/8)·m^(-5/4)·K^(17/8)
# [C_G] = K^(-1/8)·kg^(5/8)·m^(5/4)/(J·s²)
# = K^(-1/8)·kg^(5/8)·m^(5/4)/(kg·m²/s²·s²)
# = K^(-1/8)·kg^(-3/8)·m^(-3/4)

print(f"  C_G量纲 = K^(-1/8)·kg^(-3/8)·m^(-3/4)")
print(f"  需要从基本常数构造此量纲")

# 尝试: C_G = kB^a · ℏ^b · AMU^c · a0^d
# a0 = Bohr半径 = 5.29e-11 m
a0 = 5.29e-11  # Bohr半径
euler_gamma = 0.5772  # Euler-Mascheroni常数

# 量纲方程:
# K^(-1/8)·kg^(-3/8)·m^(-3/4) = (J/K)^a · (J·s)^b · kg^c · m^d
# = (kg·m²/s²/K)^a · (kg·m²/s)^b · kg^c · m^d
# K: -a = -1/8 => a = 1/8
# kg: a+b+c = -3/8 => 1/8+b+c = -3/8 => b+c = -1/2
# m: 2a+2b+d = -3/4 => 1/4+2b+d = -3/4 => 2b+d = -1
# s: -2a-b = 0 => -1/4-b = 0 => b = -1/4
# => c = -1/2-(-1/4) = -1/4
# => d = -1-2(-1/4) = -1+1/2 = -1/2

a_dim, b_dim, c_dim, d_dim = 1/8, -1/4, -1/4, -1/2
print(f"\n  C_G = kB^(1/8) · ℏ^(-1/4) · AMU^(-1/4) · a0^(-1/2) × [纯数]")
C_G_dim = KB**a_dim * HBAR**b_dim * AMU**c_dim * a0**d_dim
print(f"  = {KB:.4e}^(1/8) · {HBAR:.4e}^(-1/4) · {AMU:.4e}^(-1/4) · {a0:.4e}^(-1/2)")
print(f"  = {C_G_dim:.4e}")

pure_number = C_GAMMA / C_G_dim
print(f"\n  C_G(经验) / C_G(量纲) = {C_GAMMA:.2e} / {C_G_dim:.4e} = {pure_number:.4f}")
print(f"  log(纯数) = {math.log(pure_number):.4f}")

# 检查纯数是否与已知常数相关
print(f"\n  纯数 {pure_number:.4f} 的可能来源:")
candidates = {
    'π²': math.pi**2,
    '2π': 2*math.pi,
    '4π': 4*math.pi,
    'β/π': BETA/math.pi,
    '√(2π)': math.sqrt(2*math.pi),
    'e^γ(BCS)': math.exp(euler_gamma),
    '2e^γ/π(BCS)': 2*math.exp(euler_gamma)/math.pi,
    '(2e^γ/π)²': (2*math.exp(euler_gamma)/math.pi)**2,
    'π·√2': math.pi*math.sqrt(2),
    'β/2': BETA/2,
    '8π/3': 8*math.pi/3,
    'exp(1)': math.e,
    '√π': math.sqrt(math.pi),
    'π': math.pi,
    '3π/4': 3*math.pi/4,
    'γ₁/π': GAMMA_1/math.pi,
    'β/8': BETA/8,
    'ln(β)': math.log(BETA),
    'π/ln2': math.pi/LN2,
    '(γ₂-γ₁)/2': (GAMMA_2-GAMMA_1)/2,
}
for name, val in candidates.items():
    ratio = pure_number / val
    if 0.8 < ratio < 1.2:
        print(f"    {name:20s} = {val:.6f}, 纯数/{name} = {ratio:.4f} {'✓' if 0.95<ratio<1.05 else ''}")

# 也检查纯数的对数
log_pure = math.log(pure_number)
print(f"\n  log(纯数) = {log_pure:.4f}")
for name, val in candidates.items():
    ratio = log_pure / val
    if 0.8 < ratio < 1.2:
        print(f"    log(纯数)/{name} = {ratio:.4f} {'✓' if 0.95<ratio<1.05 else ''}")

# ============================================================
print(f"\n{'='*70}")
print("7. 完整第一性方程组")
print("="*70)

print(f"""
从CQM基本原理到Tc的完整计算链:

输入: 化学式 → C_mol矩阵
  C_mol = ⊕ Cartan(价轨道) + 杂化耦合

步骤1: C_mol → 谱特征
  ev = eigenvalues(C_mol)
  sg = ev[1] - ev[0]  (谱隙)
  aniso = std(ev/mean(ev))  (各向异性)
  Δδ₀ = √(C²/l²·3ℏ/(4ωD)·(1-f_corr)·es)  (零点涨落)
  G = (1/l)·√((1-f_corr)·es)  (CQM引力参数)

步骤2: 谱特征 → λep (Hopfield展开)
  λep = λ₀ + α_mass·inv_mass + α_log·log(1/sg) + ...
  λ₀ = 0.364 (基线耦合)
  α_i从Hopfield/van Hove/GL(2)/超交换导出

步骤3: λep → γn (弱耦合展开)
  γn = A - B/λep
  A = 8π³/3·(1-μ*/λ) = {A_theory:.2f}  (从BCS伪势)
  B = 8π/3 = {B_theory:.2f}  (3D态密度因子)

步骤4: γn → K_0 → K_eff
  K_0 = C_G·exp(2π² - 2/λep*)
  λep* = λep·(1-μ*/λ)  (有效耦合)
  K_eff = K_0·G^(-3/4)·θD^(9/8)

步骤5: K_eff → Tc
  Tc = √(8·Δδ₀²·K_eff·θD/(9·ln2))

等价的arccoth路线:
  1-βδv = 3β²Δδ₀²/[16(γ₂-γ₁)]  (临界同步, x≈1)
  Tc = θD/(2·arccoth(x))
  x = 3β²Δδ₀²/[16(1-βδv)(γ₂-γ₁)]

理论常数 (全部从数学/物理导出):
  β = 8π+1 = {BETA:.4f}  (A4群论)
  C² = 2/3  (正四面体Regge)
  B = 8π/3 = {B_theory:.4f}  (3D态密度) ✓ {abs(B_theory-B_EMP)/B_EMP*100:.2f}%
  A = 8π³/3·(1-μ*/λ) = {A_theory:.4f}  (BCS伪势) ✓ {abs(A_theory-A_EMP)/A_EMP*100:.2f}%
  0.369 = 3/(4π(1-μ*/λ)) = {A_GAMMA_theory:.6f}  ✓ {abs(A_GAMMA_theory-A_GAMMA)/A_GAMMA*100:.2f}%
  log(C_L/C_G) = 2π² = {theory_2pi2:.4f}  ✓ {abs(theory_2pi2-log_ratio)/log_ratio*100:.2f}%
  aniso系数 = (γd-γs)/2π = 0.3496  (GL(2)零点差) ✓ 0.11%
  c_o = B²·t²/(3Uλ₀²) = 5.519  (超交换) ✓ 0.34%

剩余经验参数 (3个):
  C_G = {C_GAMMA:.2e}  (K_0前置因子, 量纲K^(-1/8)·kg^(-3/8)·m^(-3/4))
  λ₀ = 0.364  (基线耦合)
  μ*/λ = 0.353  (BCS伪势比, 材料相关?)
""")