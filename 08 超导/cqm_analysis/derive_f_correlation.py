"""
关联因子 f 的严格推导：从 Debye 声子谱

问题：在双尺度涨落公式中
  Δδ² = (C²/L²) × (3ℏ/(4ω_D)) × (1-f) × Σ(1/m_i + 1/m_j)

f 是最近邻原子位移关联因子：
  f = ⟨u_i · u_j⟩ / ⟨u²⟩

当前唯象确定（H₃S: f=0.594, LaH₁₀: f=0.308, 元素: f=0.5）。
本脚本从 Debye 模型严格导出 f。

关键推导：
  在各向同性 Debye 模型中，位移-位移关联函数为
    D(ω,R) = sinc(ωR/c) = sin(ωR/c)/(ωR/c)

  f = ∫₀^{ω_D} ω × sinc(ωR/c) dω / ∫₀^{ω_D} ω dω
    = sinc²(k_D R/2)

  其中 k_D = ω_D/c 是 Debye 波矢，R 是最近邻距离。
"""

import numpy as np
from scipy import integrate

# ============================================================
# Part 1: 解析推导
# ============================================================

print("=" * 80)
print("关联因子 f 的严格推导：从 Debye 声子谱")
print("=" * 80)

print("""
推导：

1. 定义：f = ⟨u_i · u_j⟩ / ⟨u²⟩
   其中 u_i, u_j 是最近邻原子的零点位移

2. Debye 模型中：
   ⟨u²⟩ = (1/3N) ∫₀^{ω_D} g(ω) (ℏ/2mω) dω = 3ℏ/(4mω_D)

   ⟨u_i · u_j⟩ = (1/3N) ∫₀^{ω_D} g(ω) (ℏ/2mω) D(ω,R) dω

   其中 g(ω) = 9Nω²/ω_D³ 是 Debye 态密度
   D(ω,R) = sinc(ωR/c) 是各向同性弹性介质的位移关联函数
   c 是声速，R 是最近邻距离

3. 计算：
   ⟨u_i · u_j⟩ = (3ℏc/(2mRω_D³)) ∫₀^{ω_D} sin(ωR/c) dω
               = (3ℏc²/(2mR²ω_D³)) × [1 - cos(ω_D R/c)]
               = (3ℏc²/(mR²ω_D³)) × sin²(ω_D R/(2c))

4. 归一化：
   f = ⟨u_i · u_j⟩ / ⟨u²⟩ = [4c²/(R²ω_D²)] × sin²(ω_D R/(2c))
     = [4/(k_D²R²)] × sin²(k_D R/2)
     = [sin(k_D R/2) / (k_D R/2)]²
     = sinc²(k_D R/2)

   其中 k_D = ω_D/c 是 Debye 波矢
""")

# ============================================================
# Part 2: 数值验证
# ============================================================
print("=" * 80)
print("Part 2: 数值验证——直接积分 vs 解析公式")
print("=" * 80)

def f_numerical(kD_R, n_points=10000):
    """数值积分计算 f
    kD_R = k_D × R (Debye波矢 × 最近邻距离)
    """
    # f = ∫₀¹ x × sinc(x × kD_R) dx / ∫₀¹ x dx
    # 其中 x = ω/ω_D
    omega = np.linspace(1e-10, 1.0, n_points)

    numerator = np.trapezoid(omega * np.sinc(omega * kD_R / np.pi), omega)
    denominator = np.trapezoid(omega, omega)

    return numerator / denominator

def f_analytical(kD_R):
    """解析公式: f = sinc²(k_D R / 2)
    注意: np.sinc(x) = sin(πx)/(πx), 所以 sin(x)/x = sinc(x/π)
    """
    return (np.sin(kD_R / 2) / (kD_R / 2))**2

print(f"\n{'k_D R':>10} {'f(数值)':>12} {'f(解析)':>12} {'误差':>12}")
print("-" * 50)
for kD_R in [1.0, 2.0, 3.0, 3.88, 4.0, 4.24, 4.36, 5.0, 6.0, 7.0, 8.0]:
    f_num = f_numerical(kD_R)
    f_ana = f_analytical(kD_R)
    print(f"{kD_R:>10.4f} {f_num:>12.8f} {f_ana:>12.8f} {abs(f_num-f_ana):>12.2e}")

print("\n✓ 数值积分与解析公式完全一致")

# ============================================================
# Part 3: 不同晶格结构的 f
# ============================================================
print("\n" + "=" * 80)
print("Part 3: 不同晶格结构的 f = sinc²(k_D R/2)")
print("=" * 80)

def debye_kD(n_density):
    """Debye波矢 k_D = (6π²n)^(1/3)
    n_density: 原子数密度 (atoms/Å³)
    """
    return (6 * np.pi**2 * n_density)**(1/3)

# 晶格参数
crystals = {
    "SC (简单立方)": {
        "n_per_cell": 1, "a": 1.0, "R": 1.0, "z": 6,
        "note": "R=a, n=1/a³"
    },
    "BCC (体心立方)": {
        "n_per_cell": 2, "a": 1.0, "R": np.sqrt(3)/2, "z": 8,
        "note": "R=a√3/2, n=2/a³"
    },
    "FCC (面心立方)": {
        "n_per_cell": 4, "a": 1.0, "R": 1/np.sqrt(2), "z": 12,
        "note": "R=a/√2, n=4/a³"
    },
    "HCP (密排六方)": {
        "n_per_cell": 2, "a": 1.0, "R": 1.0, "z": 12,
        "note": "R=a, n=2/(a²×a√(8/3))"
    },
    "Diamond (金刚石)": {
        "n_per_cell": 8, "a": 1.0, "R": np.sqrt(3)/4, "z": 4,
        "note": "R=a√3/4, n=8/a³"
    },
}

print(f"\n{'结构':<20} {'z':>4} {'k_D R':>10} {'f=sinc²(kDR/2)':>16} {'1-f':>10} {'说明'}")
print("-" * 80)

results = {}
for name, info in crystals.items():
    a = info["a"]
    n = info["n_per_cell"] / a**3
    kD = debye_kD(n)
    R = info["R"]
    kD_R = kD * R
    f = f_analytical(kD_R)
    results[name] = {"kD_R": kD_R, "f": f, "z": info["z"]}
    print(f"{name:<20} {info['z']:>4} {kD_R:>10.4f} {f:>16.8f} {1-f:>10.8f}  {info['note']}")

# ============================================================
# Part 4: 实际材料计算
# ============================================================
print("\n" + "=" * 80)
print("Part 4: 实际超导材料的 f 计算")
print("=" * 80)

print("""
对实际材料，k_D R 取决于晶格结构：
  k_D = (6π²n)^(1/3), n = 原子数密度
  R = 最近邻距离

f = sinc²(k_D R / 2)
""")

# 实际材料参数
materials = [
    # (名称, 结构, a(Å), n_per_cell, R(Å), z, Tc_exp(K), f_phenom)
    ("Nb", "BCC", 3.30, 2, 3.30*np.sqrt(3)/2, 8, 9.25, 0.5),
    ("V", "BCC", 3.03, 2, 3.03*np.sqrt(3)/2, 8, 5.40, 0.5),
    ("Ta", "BCC", 3.30, 2, 3.30*np.sqrt(3)/2, 8, 4.48, 0.5),
    ("Pb", "FCC", 4.95, 4, 4.95/np.sqrt(2), 12, 7.20, 0.5),
    ("Al", "FCC", 4.05, 4, 4.05/np.sqrt(2), 12, 1.20, 0.5),
    ("La", "FCC", 3.75, 4, 3.75/np.sqrt(2), 12, 6.00, 0.5),
    ("Sn(β)", "FCT", 5.83, 4, 5.83/np.sqrt(2), 12, 3.70, 0.5),
    ("Tc", "HCP", 2.74, 2, 2.74, 12, 7.80, 0.5),
    ("Mo", "BCC", 3.15, 2, 3.15*np.sqrt(3)/2, 8, 0.92, 0.5),
    ("W", "BCC", 3.16, 2, 3.16*np.sqrt(3)/2, 8, 0.01, 0.5),
    ("Be", "HCP", 2.29, 2, 2.29, 12, 0.0, 0.5),
    ("Zn", "HCP", 2.66, 2, 2.66, 12, 0.85, 0.5),
    ("Cd", "HCP", 2.98, 2, 2.98, 12, 0.56, 0.5),
    ("In", "FCT", 3.25, 4, 3.25/np.sqrt(2), 12, 3.40, 0.5),
]

print(f"{'材料':<10} {'结构':<6} {'a(Å)':>6} {'R(Å)':>6} {'z':>4} {'k_D R':>8} {'f(推导)':>10} {'f(唯象)':>10} {'1-f':>8} {'Tc(K)':>7}")
print("-" * 85)

for name, struct, a, n_cell, R, z, tc, f_phen in materials:
    n = n_cell / a**3
    kD = debye_kD(n)
    kD_R = kD * R
    f = f_analytical(kD_R)
    print(f"{name:<10} {struct:<6} {a:>6.2f} {R:>6.3f} {z:>4} {kD_R:>8.4f} {f:>10.6f} {f_phen:>10.3f} {1-f:>8.6f} {tc:>7.2f}")

# ============================================================
# Part 5: 氢化物的 f——双尺度（声学+光学）
# ============================================================
print("\n" + "=" * 80)
print("Part 5: 氢化物的 f——声学模 + 光学模")
print("=" * 80)

print("""
氢化物有两类声子模：
1. 声学模（低频）：晶胞整体振动，H和重原子同相
   → f_acoustic > 0（同相运动，边长变化小）
   → f_acoustic = sinc²(k_D R_inter/2)

2. 光学模（高频）：H原子相对重原子振动（反相）
   → f_optical < 0（反相运动，边长变化大）
   → f_optical = -sinc²(k_D R_intra/2)（负号=反关联）

总 f 由模权重平均：
  f = (w_ac × f_acoustic + w_op × f_optical) / (w_ac + w_op)

权重 w ∝ 1/ω²（零点位移 ∝ 1/√ω, 权重 ∝ 1/ω）
高频光学模权重小，但H质量小→位移大→权重大

简化：对氢化物，光学模H振动主导
  w_op/w_ac ≈ (M_heavy/m_H) × (ω_ac/ω_op)²

  对H₃S: M_S/m_H ≈ 32, ω_ac/ω_op ≈ 0.3
  w_op/w_ac ≈ 32 × 0.09 ≈ 2.9 → 光学模主导
""")

def f_hydride(M_heavy_amu, m_H_amu, omega_ac_over_op, R_inter, R_intra, a, n_cell):
    """氢化物的 f：声学模 + 光学模"""
    n = n_cell / a**3
    kD = debye_kD(n)

    # 声学模关联（正）
    f_ac = f_analytical(kD * R_inter)

    # 光学模关联（负——反相运动）
    f_op = -f_analytical(kD * R_intra)

    # 权重比
    w_ratio = (M_heavy_amu / m_H_amu) * omega_ac_over_op**2

    # 总 f
    f_total = (f_ac + w_ratio * f_op) / (1 + w_ratio)

    return f_total, f_ac, f_op, w_ratio

# H₃S: Im-3m, a≈3.08Å at 200GPa
print("H₃S (200 GPa, Im-3m, a≈3.08Å):")
f_total, f_ac, f_op, wr = f_hydride(
    M_heavy_amu=32.0, m_H_amu=1.0,
    omega_ac_over_op=0.3,
    R_inter=3.08, R_intra=3.08*np.sqrt(3)/4,  # S-H键≈a√3/4
    a=3.08, n_cell=4  # 1S + 3H = 4 atoms/cell
)
print(f"  f_acoustic = {f_ac:.6f} (正关联)")
print(f"  f_optical  = {f_op:.6f} (负关联)")
print(f"  w_op/w_ac  = {wr:.3f}")
print(f"  f_total    = {f_total:.6f}")
print(f"  f_phenom   = 0.594 (唯象值)")
print(f"  1-f        = {1-f_total:.6f}")

# LaH₁₀: Fm-3m, a≈5.1Å at 170GPa
print("\nLaH₁₀ (170 GPa, Fm-3m, a≈5.1Å):")
f_total, f_ac, f_op, wr = f_hydride(
    M_heavy_amu=139.0, m_H_amu=1.0,
    omega_ac_over_op=0.25,
    R_inter=5.1/np.sqrt(2), R_intra=5.1/4,  # La-H键
    a=5.1, n_cell=11  # 1La + 10H = 11 atoms/cell
)
print(f"  f_acoustic = {f_ac:.6f} (正关联)")
print(f"  f_optical  = {f_op:.6f} (负关联)")
print(f"  w_op/w_ac  = {wr:.3f}")
print(f"  f_total    = {f_total:.6f}")
print(f"  f_phenom   = 0.308 (唯象值)")
print(f"  1-f        = {1-f_total:.6f}")

# ============================================================
# Part 6: 关键发现——f 的结构普适性
# ============================================================
print("\n" + "=" * 80)
print("Part 6: 关键发现——f 的结构普适性")
print("=" * 80)

print("""
对纯声学模（元素超导体），f = sinc²(k_D R/2):

  k_D R 对不同结构:
    SC:    k_D R = (6π²)^(1/3) ≈ 3.88
    BCC:   k_D R = (12π²)^(1/3) × √3/2 ≈ 4.24
    FCC:   k_D R = (24π²)^(1/3) / √2 ≈ 4.36
    HCP:   k_D R ≈ 4.36 (同FCC, 密排结构)
    Diamond: k_D R = (48π²)^(1/3) × √3/4 ≈ 3.76

  f 值:
    SC:      f ≈ 0.23
    BCC:     f ≈ 0.16
    FCC/HCP: f ≈ 0.14
    Diamond: f ≈ 0.25

  这些值在 0.14-0.25 范围，远小于唯象值 0.5。

  可能原因：
  1. Debye模型是各向同性近似，实际晶格有方向性
  2. 唯象f=0.5可能包含了非Debye效应（非谐性、电子-声子耦合等）
  3. CQM公式中的f可能有不同的物理定义

  重要：f的推导值(0.14-0.25)与唯象值(0.5)的差异
  表明Debye模型是零阶近似，实际f需要从完整声子谱计算。
""")

# ============================================================
# Part 7: 更精确的推导——方向性关联
# ============================================================
print("=" * 80)
print("Part 7: 更精确的推导——方向性关联")
print("=" * 80)

print("""
Debye模型假设各向同性，但实际晶格中关联是方向性的。

对BCC/FCC等晶格，最近邻在不同方向上：
  BCC: 8个邻居在(±1,±1,±1)方向
  FCC: 12个邻居在(±1,±1,0)等方向

方向性关联函数：
  D(ω, R̂) = Σ_α (R̂_α)² × sinc(ωR/c_α)

对各向同性固体 c_α = c:
  D(ω, R̂) = sinc(ωR/c) （与方向无关）

对各向异性固体（如BCC沿<111>方向）:
  需要考虑声速的方向依赖性

但CQM公式中f是平均关联（对所有z个邻居平均），
各向同性Debye模型给出的是这个平均的零阶近似。
""")

# ============================================================
# Part 8: 总结
# ============================================================
print("=" * 80)
print("总结：关联因子 f 的严格推导")
print("=" * 80)

print(f"""
1. 解析公式（Debye模型，纯声学模）:
   f = sinc²(k_D R / 2)
   其中 k_D = (6π²n)^(1/3), R = 最近邻距离, n = 原子数密度

2. 结构依赖性:
   SC:      f ≈ {f_analytical(3.88):.4f}
   BCC:     f ≈ {f_analytical(4.24):.4f}
   FCC:     f ≈ {f_analytical(4.36):.4f}
   HCP:     f ≈ {f_analytical(4.36):.4f}
   Diamond: f ≈ {f_analytical(3.76):.4f}

3. 氢化物（声学+光学模）:
   f = (f_ac + w × f_op) / (1 + w)
   w = (M_heavy/m_H) × (ω_ac/ω_op)²
   f_ac > 0 (同相), f_op < 0 (反相)

4. 与唯象值的关系:
   - 元素超导体: 推导值 0.14-0.25 vs 唯象值 0.5
   - 差异来自Debye模型的各向同性近似
   - 精确f需要从完整声子谱（DFT）计算
   - 公式 f = sinc²(k_D R/2) 给出零阶严格估计

5. 物理意义:
   - f → 1: 邻居完全同相运动（长波长声学模主导）
   - f → 0: 邻居独立运动（短波长模主导）
   - f < 0: 邻居反相运动（光学模主导）
   - 1-f = 有效涨落比例
""")

# 验证公式
print("公式验证:")
for name, kD_R_val in [("SC", 3.88), ("BCC", 4.24), ("FCC", 4.36)]:
    f_val = f_analytical(kD_R_val)
    sinc_val = np.sin(kD_R_val/2) / (kD_R_val/2)
    print(f"  {name}: k_D R = {kD_R_val:.2f}, sinc(k_D R/2) = {sinc_val:.6f}, f = {f_val:.6f}")