"""
探索替代Tc推导路径

当前问题：
  Tc = θ_D / (2·arccoth(x)), x = A/GAP, A = 3β²Δδ₀²/(16(1-βδ_v))
  当x→1⁺时arccoth发散，Tc对参数双指数敏感

根源：tanh(θ_D/(2T))在T<<θ_D时≈1-2exp(-θ_D/T)，Tc由指数尾部决定

替代路径探索：
  A. 热涨落混合条件（不要求精确交叉）
  B. 线性温度近似
  C. 平方根参数化
  D. 自由能直接计算
  E. 同步相干阈值
"""

import numpy as np
from scipy.optimize import brentq

BETA = 8 * np.pi + 1
GAP = 21.022040 - 14.134725
C = np.sqrt(2/3)

print("=" * 90)
print("替代Tc推导路径探索")
print("=" * 90)

# Nb参数
theta_D = 275.0
Tc_exp = 9.2
# 反推参数
x_rev = 1.0 / np.tanh(theta_D / (2 * Tc_exp))
A_rev = x_rev * GAP
# 取 λ = 0.018, 1-βδ_v = λ/x
lam = 0.018
one_minus_bdv = lam / x_rev
delta_v = (1 - one_minus_bdv) / BETA
dd0 = 0.031  # Nb的Δδ₀

print(f"\nNb参数: θ_D={theta_D}K, Tc_exp={Tc_exp}K")
print(f"  反推: x={x_rev:.10f}, A={A_rev:.6f}, δ_v={delta_v:.8f}")
print(f"  GAP={GAP:.6f}, A-GAP={A_rev-GAP:.3e}")

# ============================================================
# 路径A：热涨落混合条件
# ============================================================
print(f"\n{'='*90}")
print("路径A：热涨落混合条件")
print(f"{'='*90}")
print("""
物理思想：本征值不是无穷尖锐的，有热展宽Γ~kT。
超导转变不要求精确交叉λ₁=λ₂，而是热涨落足以混合两个本征态：
  |λ₂(T) - λ₁(T)| = Γ(T)

条件：GAP - A·tanh(θ_D/(2T)) = α·kT/ℏΩ₀
简化：GAP - A·tanh(θ_D/(2T)) = α·T/θ_D

当GAP≈A时，左边≈A·2exp(-θ_D/T)很小，右边=α·T/θ_D也不为零，
Tc不会发散！
""")

# 数值求解：GAP - A·tanh(θ_D/(2T)) = α·T/θ_D
for alpha in [0.01, 0.1, 1.0, 10.0]:
    def eq_A(T):
        if T <= 0:
            return 1e10
        return GAP - A_rev * np.tanh(theta_D / (2*T)) - alpha * T / theta_D

    # 找根
    try:
        Tc_A = brentq(eq_A, 0.1, 1000)
        # 检查敏感度：A变化1%时Tc变化多少
        A_pert = A_rev * 1.01
        def eq_A_pert(T):
            return GAP - A_pert * np.tanh(theta_D / (2*T)) - alpha * T / theta_D
        Tc_A_pert = brentq(eq_A_pert, 0.1, 1000)
        sens = abs(Tc_A_pert - Tc_A) / Tc_A / 0.01
        print(f"  α={alpha:5.2f}: Tc={Tc_A:.2f}K, A变化1%→Tc变化{sens*100:.1f}% (敏感度{sens:.1f})")
    except:
        print(f"  α={alpha:5.2f}: 无解")

# ============================================================
# 路径B：线性温度近似
# ============================================================
print(f"\n{'='*90}")
print("路径B：线性温度近似")
print(f"{'='*90}")
print("""
如果Δδ_v(T) = Δδ₀·(1 - T/θ_D) [线性近似，非tanh]
则 Δδ_v² = Δδ₀²·(1-T/θ_D)²

本征值交叉：GAP = A·(1-Tc/θ_D)²
Tc = θ_D·(1 - √(GAP/A))

当A≈GAP时：Tc ≈ θ_D·(A-GAP)/(2A) — 线性依赖，不发散！
""")

Tc_B = theta_D * (1 - np.sqrt(GAP / A_rev))
sens_B = 0.5 * np.sqrt(GAP / A_rev) / (1 - np.sqrt(GAP / A_rev))
print(f"  Tc = {Tc_B:.2f}K (实验{Tc_exp}K)")
print(f"  理论敏感度: A变化1%→Tc变化{sens_B*100:.1f}%")
print(f"  对比arccoth: A变化1%→Tc变化~10000%")

# 但线性近似在T<<θ_D时不正确
print(f"\n  ⚠️ 问题：线性近似在T<<θ_D时不正确")
print(f"  tanh(θ_D/(2T)) = 1-2exp(-θ_D/T) ≈ 1-10⁻¹³ (指数趋近)")
print(f"  1-T/θ_D = 1-9.2/275 = 0.967 (线性趋近)")
print(f"  两者行为完全不同，线性近似不物理")

# ============================================================
# 路径C：平方根参数化
# ============================================================
print(f"\n{'='*90}")
print("路径C：平方根参数化")
print(f"{'='*90}")
print("""
如果定义 η = x - 1 = A/GAP - 1 = (A-GAP)/GAP
则 arccoth(1+η) ≈ √(1/(2η)) for small η
Tc ≈ θ_D·√(η/2) = θ_D·√((A-GAP)/(2·GAP))

这是平方根依赖！η变化1%→Tc变化0.5%
但η仍然需要高精度计算（η~10⁻¹⁵）
""")

eta = (A_rev - GAP) / GAP
Tc_C = theta_D * np.sqrt(eta / 2)
print(f"  η = {eta:.3e}")
print(f"  Tc ≈ θ_D·√(η/2) = {Tc_C:.2f}K (实验{Tc_exp}K)")
print(f"  精确Tc = {Tc_exp}K, 近似误差 = {abs(Tc_C-Tc_exp)/Tc_exp*100:.1f}%")

# 关键问题：η能否从材料直接计算？
print(f"\n  关键问题：η = (A-GAP)/GAP 能否从材料直接计算？")
print(f"  A = 3β²Δδ₀²/(16(1-βδ_v)) [需要Δδ₀和δ_v]")
print(f"  A-GAP = 驱动力 - 阻力 [两个~O(0.1)量的差~10⁻¹⁵]")
print(f"  仍需高精度！平方根只缓解了Tc对η的敏感度，")
print(f"  但η本身仍需高精度计算。")

# ============================================================
# 路径D：自由能直接计算
# ============================================================
print(f"\n{'='*90}")
print("路径D：自由能直接计算 Tc = (E2-E1)/(S2-S1)")
print(f"{'='*90}")
print("""
§11.2给出 Tc = (E2-E1)/(S2-S1)

如果能从材料直接计算E_n和S_n：
  E_n = 结构群U(1)/Z_n的宏观能量
  S_n = 熵 = ln(n)·(1+1/(2n²))·tanh(T/θ_D) [§11.3定理4]

问题：E_n的计算需要超导态的具体结构（凝聚能等）
      这又回到需要知道超导gap的问题

在BCS中：E2-E1 ~ N(0)Δ²/2, S2-S1 ~ N(0)Δ²/Tc
→ Tc = (E2-E1)/(S2-S1) = Tc （恒等式，不给出新信息）

CQM中可能也是恒等式。
""")

# 用§11.3的熵公式
def S_n(n, T, theta_D):
    return np.log(n) * (1 + 1/(2*n**2)) * np.tanh(T / theta_D)

# Tc = (E2-E1)/(S2-S1)，如果E2-E1从反推知道
S2 = S_n(2, Tc_exp, theta_D)
S1 = S_n(1, Tc_exp, theta_D)
E_diff = Tc_exp * (S2 - S1)
print(f"  反推：S₂-S₁ = {S2-S1:.6f}")
print(f"  E₂-E₁ = Tc·(S₂-S₁) = {E_diff:.6f}")
print(f"  这是恒等式：知道Tc→算出E_diff→代回得到Tc")

# ============================================================
# 路径E：同步相干阈值（Kuramoto型）
# ============================================================
print(f"\n{'='*90}")
print("路径E：同步相干阈值（Kuramoto型）")
print(f"{'='*90}")
print("""
Kuramoto模型：同步临界耦合 K_c = 2/(π·g(0))
其中g(ω)是本征频率分布。

CQM类比：
  耦合强度 K ~ β·Δδ_v(T)² [角亏涨落耦合]
  频率分布 g(0) ~ 1/GAP [本征值间距的倒数]
  同步条件：K > K_c = 2·GAP/π

  β·Δδ_v(Tc)² = 2·GAP/π
  Δδ₀²·tanh(θ_D/(2Tc)) = 2·GAP/(π·β)
  tanh(θ_D/(2Tc)) = 2·GAP/(π·β·Δδ₀²)

  如果右边不接近1，Tc对参数不敏感！
""")

rhs = 2 * GAP / (np.pi * BETA * dd0**2)
print(f"  右边 = 2·GAP/(π·β·Δδ₀²) = {rhs:.4f}")
if rhs < 1:
    Tc_E = theta_D / (2 * np.arctanh(rhs))
    print(f"  Tc = θ_D/(2·arctanh(右边)) = {Tc_E:.2f}K")
else:
    print(f"  右边 > 1，无超导（阈值未达到）")
    # 用反推的Δδ₀
    dd0_rev = np.sqrt(2 * GAP / (np.pi * BETA * np.tanh(theta_D / (2 * Tc_exp))))
    print(f"  反推Δδ₀ = {dd0_rev:.4f} (实际{dd0})")
    rhs_rev = 2 * GAP / (np.pi * BETA * dd0_rev**2)
    Tc_E_rev = theta_D / (2 * np.arctanh(rhs_rev))
    print(f"  反推Tc = {Tc_E_rev:.2f}K")

    # 敏感度
    dd0_pert = dd0_rev * 1.01
    rhs_pert = 2 * GAP / (np.pi * BETA * dd0_pert**2)
    if rhs_pert < 1:
        Tc_pert = theta_D / (2 * np.arctanh(rhs_pert))
        sens_E = abs(Tc_pert - Tc_E_rev) / Tc_E_rev / 0.01
        print(f"  敏感度：Δδ₀变化1%→Tc变化{sens_E*100:.1f}%")
    print(f"\n  Kuramoto阈值条件: β·Δδ_v² = 2·GAP/π")
    print(f"  vs 本征值交叉: β²·Δδ_v²·3/(16(1-βδ_v)) = GAP")
    print(f"  Kuramoto: 耦合~β·Δδ_v² (无1/(1-βδ_v)因子)")
    print(f"  本征值交叉: 耦合~β²·Δδ_v²/(1-βδ_v) (有1/(1-βδ_v)发散)")

# ============================================================
# 路径F：不通过tanh，用多项式温度依赖
# ============================================================
print(f"\n{'='*90}")
print("路径F：多项式温度依赖（唯象）")
print(f"{'='*90}")
print("""
假设 Δδ_v(T) = Δδ₀·(1 - (T/θ_D)^p) [多项式]
则 Δδ_v² = Δδ₀²·(1 - (T/θ_D)^p)²

本征值交叉：GAP = A·(1 - (Tc/θ_D)^p)²
Tc = θ_D·(1 - (GAP/A)^(1/2))^(1/p)

当A≈GAP时：Tc ≈ θ_D·((A-GAP)/(2A))^(1/p) — p次根依赖
  p=1: 线性（不发散）
  p=2: 平方根（不发散）
  p→∞: 指数（发散，回到tanh）

多项式依赖不发散！但需要物理推导为什么是多项式。
""")

for p in [1, 2, 3, 4]:
    Tc_F = theta_D * (1 - (GAP / A_rev)**0.5)**(1/p)
    # 敏感度
    A_pert = A_rev * 1.01
    Tc_F_pert = theta_D * (1 - (GAP / A_pert)**0.5)**(1/p)
    sens_F = abs(Tc_F_pert - Tc_F) / Tc_F / 0.01
    print(f"  p={p}: Tc={Tc_F:.2f}K, 敏感度={sens_F:.2f} (A变化1%→Tc变化{sens_F*100:.0f}%)")

# ============================================================
# 总结
# ============================================================
print(f"\n{'='*90}")
print("总结：替代路径评估")
print(f"{'='*90}")
print("""
路径A（热涨落混合）: Tc不发散，但α未知，需新物理
路径B（线性近似）:   Tc不发散，但T<<θ_D时不物理
路径C（平方根参数化）: Tc对η敏感度降低，但η仍需高精度
路径D（自由能直接）:   恒等式，不给出新信息
路径E（Kuramoto阈值）: 无1/(1-βδ_v)发散因子，值得深入
路径F（多项式依赖）:   不发散，但需物理推导

最有希望：路径E（Kuramoto型同步阈值）
  - 物理基础：Kuramoto同步理论
  - 无1/(1-βδ_v)发散因子
  - 阈值条件K > K_c = 2/(π·g(0))是标准结果
  - 需要推导：CQM中K和g(0)的具体形式
""")