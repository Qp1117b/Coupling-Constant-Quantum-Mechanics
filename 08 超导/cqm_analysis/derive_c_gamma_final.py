"""检查1.037修正因子的理论来源

C_nat(拟合) / alpha_fs^3 = 1.037186
假设: 1.037 ≈ e^(1/beta), beta = 8*pi+1
"""
import math

ALPHA_FS = 1/137.036
BETA = 8 * math.pi + 1
AG = 3.0 / (4 * math.pi * (1 - 1.0/(2*math.sqrt(2))))
MU = 1.0 / (2 * math.sqrt(2))

ratio = 1.037186

print(f"目标比值 = {ratio:.6f}")
print(f"beta = 8*pi+1 = {BETA:.6f}")
print(f"AG = {AG:.6f}")
print()

# 尝试各种CQM常数组合
candidates = {
    'e^(1/beta)': math.exp(1/BETA),
    'e^(1/(8*pi))': math.exp(1/(8*math.pi)),
    '1+1/beta': 1 + 1/BETA,
    '1+1/(8*pi)': 1 + 1/(8*math.pi),
    'e^(AG/beta^2)': math.exp(AG/BETA**2),
    'e^(1/beta^2)': math.exp(1/BETA**2),
    'e^(mu/beta)': math.exp(MU/BETA),
    'e^(1/(beta*sqrt(2)))': math.exp(1/(BETA*math.sqrt(2))),
    'beta/(beta-1)': BETA/(BETA-1),
    '(beta+1)/beta': (BETA+1)/BETA,
    'e^(2/beta^2)': math.exp(2/BETA**2),
    'e^(pi/beta^2)': math.exp(math.pi/BETA**2),
    'e^(1/(8*pi+1))': math.exp(1/(8*math.pi+1)),
    '1+1/27': 1+1/27,
    'e^(1/27)': math.exp(1/27),
    '28/27': 28/27,
    'e^(AG^2/beta)': math.exp(AG**2/BETA),
    'e^(1/(beta*(1-mu)))': math.exp(1/(BETA*(1-MU))),
    'e^(mu/(beta*(1-mu)))': math.exp(MU/(BETA*(1-MU))),
}

print(f"{'表达式':<30} {'值':>12} {'比值/目标':>12} {'偏差%':>10}")
print("-"*70)
for label, val in sorted(candidates.items(), key=lambda x: abs(x[1] - ratio)):
    print(f"{label:<30} {val:>12.6f} {val/ratio:>12.6f} {(val/ratio-1)*100:>9.4f}%")

# 最佳候选
best = min(candidates.items(), key=lambda x: abs(x[1] - ratio))
print(f"\n最佳: {best[0]} = {best[1]:.6f}, 偏差 = {(best[1]/ratio-1)*100:.4f}%")

# 验证: e^(1/beta) * alpha_fs^3 * dim_factor
HBAR = 1.054571817e-34; KB = 1.380649e-23; ME = 9.10938370e-31; A0 = 5.291772109e-11
dim_factor = HBAR**(-0.25) * KB**(0.125) * ME**(-0.25) * A0**(-0.5)

C_theory = math.exp(1/BETA) * ALPHA_FS**3 * dim_factor
C_fit = 7.77e11
print(f"\n理论C_GAMMA = e^(1/beta) * alpha_fs^3 * dim = {C_theory:.4e}")
print(f"拟合C_GAMMA = {C_fit:.4e}")
print(f"比值 = {C_fit/C_theory:.6f} (偏差{(C_fit/C_theory-1)*100:.3f}%)")

# 更精确: 用精确alpha_fs
E_CHARGE = 1.602176634e-19; EPS0 = 8.854187817e-12; C_LIGHT = 2.99792458e8
ALPHA_FS_PRECISE = E_CHARGE**2 / (4 * math.pi * EPS0 * HBAR * C_LIGHT)
C_theory_precise = math.exp(1/BETA) * ALPHA_FS_PRECISE**3 * dim_factor
print(f"\n精确理论C_GAMMA = {C_theory_precise:.6e}")
print(f"精确比值 = {C_fit/C_theory_precise:.8f} (偏差{(C_fit/C_theory_precise-1)*100:.4f}%)")

# 物理含义
print(f"\n{'='*60}")
print(f"理论推导总结")
print(f"{'='*60}")
print(f"C_GAMMA = e^(1/beta) * alpha_fs^3 * hbar^(-1/4) * k_B^(1/8) * m_e^(-1/4) * a0^(-1/2)")
print(f"")
print(f"其中:")
print(f"  beta = 8*pi+1 = {BETA:.4f}  (CQM主丛曲率参数, Klein四元群和乐)")
print(f"  e^(1/beta) = {math.exp(1/BETA):.6f}  (1/beta量子修正)")
print(f"  alpha_fs = {ALPHA_FS_PRECISE:.6f} = 1/{1/ALPHA_FS_PRECISE:.3f}  (精细结构常数)")
print(f"  alpha_fs^3 = {ALPHA_FS_PRECISE**3:.6e}  (运动三重分化: 惯性×能动张量×作用量)")
print(f"  hbar^(-1/4)*k_B^(1/8)*m_e^(-1/4)*a0^(-1/2) = {dim_factor:.4e}  (维度转换)")
print(f"")
print(f"  => C_GAMMA = {C_theory_precise:.4e} (理论)")
print(f"  vs C_GAMMA = {C_fit:.4e} (拟合)")
print(f"  偏差 = {abs(C_theory_precise/C_fit-1)*100:.3f}%")