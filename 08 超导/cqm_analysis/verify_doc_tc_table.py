"""
验证文档中Tc数值验证表的正确性

文档§11.10声称:
| Nb | 0.038 | 0.031 | 0.5 | 1.00 | 9.2 K | 9.2 K |
| Pb | 0.037 | 0.033 | 0.5 | 1.00 | 7.2 K | 7.2 K |
| Al | 0.036 | 0.055 | 0.5 | 1.00 | 1.2 K | 1.2 K |

文档§11.10(第1286行)又声称:
| Nb | 9.2 | 275 | 0.216 | 1.000 | 常压元素 |
| Pb | 7.2 | 105 | 0.223 | 1.000 | 常压元素 |

两套数据都声称x=1.00, Tc=实验值。验证是否正确。
"""

import numpy as np

BETA = 8 * np.pi + 1
GAP = 21.022040 - 14.134725

def calc_x(ddv0, delta_v):
    return 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA*delta_v) * GAP)

def calc_tc(x, theta_D):
    if x <= 1: return 0
    arccoth = 0.5 * np.log((x+1)/(x-1))
    return theta_D / (2 * arccoth)

def rev_delta_v(ddv0, theta_D, tc):
    """反推δ_v"""
    if tc <= 0: return None
    arg = theta_D / (2*tc)
    x = 1.0 / np.tanh(arg)
    om = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    if om > 1: return None
    return (1 - om) / BETA

print("=" * 90)
print("验证文档中Tc数值验证表")
print("=" * 90)

# 表1: §11.10 第1393行
print("\n表1: §11.10 第1393行 (δ_v≈1/β, Δδ₀从晶格)")
print(f"{'材料':<6} {'δ_v':>7} {'Δδ₀':>7} {'x':>10} {'Tc_calc':>10} {'Tc_exp':>7} {'正确?':>8}")
print("-" * 60)

table1 = [
    ("Nb", 0.038, 0.031, 275, 9.2),
    ("Pb", 0.037, 0.033, 105, 7.2),
    ("Al", 0.036, 0.055, 428, 1.2),
]

for name, dv, ddv0, tD, tc_exp in table1:
    x = calc_x(ddv0, dv)
    tc = calc_tc(x, tD)
    ok = "✓" if abs(tc - tc_exp)/tc_exp < 0.1 else "✗"
    print(f"{name:<6} {dv:>7.3f} {ddv0:>7.3f} {x:>10.4f} {tc:>10.1f} {tc_exp:>7.1f} {ok:>8}")

# 表2: §11.10 第1286行
print("\n表2: §11.10 第1286行 (δ_v=0.01, Δδ₀反推)")
print(f"{'材料':<6} {'δ_v':>7} {'Δδ₀':>7} {'x':>10} {'Tc_calc':>10} {'Tc_exp':>7} {'正确?':>8}")
print("-" * 60)

table2 = [
    ("Nb", 0.01, 0.216, 275, 9.2),
    ("Pb", 0.01, 0.223, 105, 7.2),
    ("Al", 0.01, 0.183, 428, 1.2),  # Al不在原表，用YBCO代替
]

for name, dv, ddv0, tD, tc_exp in table2:
    x = calc_x(ddv0, dv)
    tc = calc_tc(x, tD)
    ok = "✓" if abs(tc - tc_exp)/tc_exp < 0.1 else "✗"
    print(f"{name:<6} {dv:>7.3f} {ddv0:>7.3f} {x:>10.4f} {tc:>10.1f} {tc_exp:>7.1f} {ok:>8}")

# 反推验证
print("\n" + "=" * 90)
print("反推δ_v（从实验Tc和晶格Δδ₀）")
print("=" * 90)

print(f"\n{'材料':<6} {'Δδ₀':>7} {'θ_D':>6} {'Tc_exp':>7} {'δ_v反推':>10} {'x反推':>12} {'Tc验证':>10}")
print("-" * 65)

for name, dv_doc, ddv0, tD, tc_exp in table1:
    dv_rev = rev_delta_v(ddv0, tD, tc_exp)
    if dv_rev:
        x_rev = calc_x(ddv0, dv_rev)
        tc_rev = calc_tc(x_rev, tD)
        print(f"{name:<6} {ddv0:>7.3f} {tD:>6.0f} {tc_exp:>7.1f} {dv_rev:>10.6f} {x_rev:>12.8f} {tc_rev:>10.2f}")

# 敏感度分析
print("\n" + "=" * 90)
print("Tc对δ_v的敏感度分析")
print("=" * 90)

print(f"\nNb (Δδ₀=0.031, θ_D=275):")
ddv0_nb = 0.031
print(f"{'δ_v':>10} {'x':>10} {'Tc':>10} {'Tc/9.2':>10}")
for dv in [0.0370, 0.0375, 0.0376, 0.03759, 0.03758, 0.037587, 0.0380, 0.0383]:
    x = calc_x(ddv0_nb, dv)
    tc = calc_tc(x, 275)
    ratio = tc/9.2 if tc > 0 else 0
    print(f"{dv:>10.6f} {x:>10.4f} {tc:>10.1f} {ratio:>10.4f}")

print(f"\n关键发现:")
print(f"  δ_v=0.037587 → Tc=9.2K (反推值)")
print(f"  δ_v=0.038000 → Tc=333K (文档表1值)")
print(f"  δ�差0.000413 → Tc差36倍!")
print(f"  文档表1的δ_v=0.038给出Tc=333K，不是9.2K!")

# 精确反推
print("\n" + "=" * 90)
print("精确反推：δ_v需要多少位精度？")
print("=" * 90)

for name, dv_doc, ddv0, tD, tc_exp in table1:
    dv_rev = rev_delta_v(ddv0, tD, tc_exp)
    if dv_rev:
        # 测试不同精度
        print(f"\n{name} (Tc_exp={tc_exp}K, θ_D={tD}K, Δδ₀={ddv0}):")
        print(f"  精确δ_v = {dv_rev:.15f}")
        for digits in [2, 3, 4, 5, 6, 8, 10, 15]:
            dv_rounded = round(dv_rev, digits)
            x = calc_x(ddv0, dv_rounded)
            tc = calc_tc(x, tD)
            err = abs(tc - tc_exp)/tc_exp if tc > 0 else 1
            print(f"  {digits}位精度: δ_v={dv_rounded:.{digits}f} → Tc={tc:.1f}K (误差{err*100:.0f}%)")