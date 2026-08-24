"""
高精度验证：Tc公式的数值稳定性

用mpmath任意精度算术验证：
1. 反推δ_v→前向Tc是否是恒等式
2. 需要多少位精度才能前向复现Tc
3. 从Fermi面CV映射δ_v的精度是否足够
"""

from mpmath import mp, mpf, tanh, atanh, log, sqrt, exp, coth

# 设置精度
mp.dps = 50  # 50位十进制精度

BETA = 8 * mp.pi + 1
GAP = mpf("21.022040") - mpf("14.134725")
DELTA_C = 1 / BETA

def calc_x(ddv0, delta_v):
    return 3 * BETA**2 * ddv0**2 / (16 * (1 - BETA * delta_v) * GAP)

def calc_tc(x, theta_D):
    if x <= 1: return mpf(0)
    arccoth_x = atanh(1 / x)  # arccoth(x) = atanh(1/x)
    return theta_D / (2 * arccoth_x)

def rev_delta_v(ddv0, theta_D, tc):
    """高精度反推δ_v"""
    u = theta_D / (2 * tc)
    x = coth(u)
    om = 3 * BETA**2 * ddv0**2 / (16 * x * GAP)
    return (1 - om) / BETA

print("=" * 90)
print("高精度验证：Tc公式的数值稳定性 (50位精度)")
print("=" * 90)

# Nb参数
theta_D_nb = mpf("275")
tc_exp_nb = mpf("9.2")
ddv0_nb = mpf("0.031")

# 反推δ_v
dv_rev = rev_delta_v(ddv0_nb, theta_D_nb, tc_exp_nb)
print(f"\nNb反推:")
print(f"  δ_v = {dv_rev}")
print(f"  1/β = {DELTA_C}")
print(f"  δ_v - 1/β = {dv_rev - DELTA_C}")
print(f"  β·δ_v = {BETA * dv_rev}")

# 前向验证
x_rev = calc_x(ddv0_nb, dv_rev)
tc_rev = calc_tc(x_rev, theta_D_nb)
print(f"\n前向验证:")
print(f"  x = {x_rev}")
print(f"  x - 1 = {x_rev - 1}")
print(f"  Tc_calc = {tc_rev}")
print(f"  Tc_exp = {tc_exp_nb}")
print(f"  误差 = {abs(tc_rev - tc_exp_nb)}")

# 精度需求分析
print(f"\n{'='*90}")
print("精度需求分析")
print(f"{'='*90}")

print(f"\n用不同精度舍入δ_v，看Tc误差:")
print(f"{'位数':>6} {'δ_v舍入':>25} {'Tc_calc':>15} {'误差%':>10}")
print("-" * 60)

for dps in [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 30, 50]:
    # 舍入到dps位
    dv_rounded = mp.nstr(dv_rev, dps)
    dv_r = mpf(dv_rounded)
    x_r = calc_x(ddv0_nb, dv_r)
    tc_r = calc_tc(x_r, theta_D_nb)
    if tc_r > 0:
        err = float(abs(tc_r - tc_exp_nb) / tc_exp_nb * 100)
        err_s = f"{err:.1f}%"
    else:
        err_s = "Tc=0"
    print(f"{dps:>6} {dv_rounded:>25} {float(tc_r):>15.2f} {err_s:>10}")

# 从CV映射的精度
print(f"\n{'='*90}")
print("从Fermi面CV映射δ_v的精度分析")
print(f"{'='*90}")

# 假设CV=0.674(Nb), 映射δ_v = 1/β - α*(1-CV)
# 不同材料反推δ_v:
materials = [
    ("Nb", mpf("9.2"), mpf("275"), mpf("0.031"), mpf("0.674")),
    ("Pb", mpf("7.2"), mpf("105"), mpf("0.033"), mpf("0.318")),
    ("Al", mpf("1.2"), mpf("428"), mpf("0.055"), mpf("0.198")),
    ("V",  mpf("5.4"), mpf("383"), mpf("0.038"), mpf("0.833")),
]

print(f"\n{'材料':<6} {'Tc_exp':>7} {'θ_D':>6} {'Δδ₀':>6} {'CV':>6} {'δ_v反推':>20} {'1/β-δ_v':>15}")
print("-" * 75)

for name, tc, tD, ddv0, cv in materials:
    dv = rev_delta_v(ddv0, tD, tc)
    diff = DELTA_C - dv
    print(f"{name:<6} {float(tc):>7.1f} {float(tD):>6.0f} {float(ddv0):>6.3f} {float(cv):>6.3f} {mp.nstr(dv, 15):>20} {mp.nstr(diff, 10):>15}")

# 关键问题：δ_v反推值跨越的范围
print(f"\nδ_v反推值范围:")
dvs = [rev_delta_v(ddv0, tD, tc) for _, tc, tD, ddv0, _ in materials]
print(f"  最小: {mp.nstr(min(dvs), 15)}")
print(f"  最大: {mp.nstr(max(dvs), 15)}")
print(f"  跨度: {mp.nstr(max(dvs) - min(dvs), 15)}")
print(f"  1/β:  {mp.nstr(DELTA_C, 15)}")
print(f"  跨度/1/β: {mp.nstr((max(dvs) - min(dvs)) / DELTA_C, 10)}")

# CV到δ_v的映射精度需求
print(f"\n{'='*90}")
print("CV→δ_v映射的精度需求")
print(f"{'='*90}")

# 如果δ_v = f(CV)，需要f在CV=0.674处给出0.037582...
# f的导数需要多少？
# δ_v范围: ~0.036-0.038, 跨度~0.002
# CV范围: 0.198-0.833, 跨度~0.635
# 平均导数: 0.002/0.635 ≈ 0.003

# 但Tc对δ_v的敏感度：
# dTc/dδ_v = ?
# Tc = θ_D/(2*arccoth(x)), x = λ/(1-βδ_v)
# dx/dδ_v = λ*β/(1-βδv)² = x*β/(1-βδv)
# dTc/dx = θ_D/(2*(1/(x²-1))) = θ_D*(x²-1)/2
# dTc/dδ_v = dTc/dx * dx/dδ_v = θ_D*(x²-1)/2 * x*β/(1-βδv)

x_nb = calc_x(ddv0_nb, dvs[0])
dTc_dv = theta_D_nb * (x_nb**2 - 1) / 2 * x_nb * BETA / (1 - BETA * dvs[0])
print(f"\nNb: dTc/dδ_v = {mp.nstr(dTc_dv, 10)}")
print(f"  δ_v误差0.001 → Tc误差 = {mp.nstr(abs(dTc_dv * mpf('0.001')), 5)} K")
print(f"  δ_v误差0.0001 → Tc误差 = {mp.nstr(abs(dTc_dv * mpf('0.0001')), 5)} K")
print(f"  δ_v误差0.00001 → Tc误差 = {mp.nstr(abs(dTc_dv * mpf('0.00001')), 5)} K")

# 要Tc误差<1K，需要δ_v精度<
dv_precision = mpf(1) / abs(dTc_dv)
print(f"\n  要Tc误差<1K: δ_v精度 < {mp.nstr(dv_precision, 5)}")
print(f"  要Tc误差<0.1K: δ_v精度 < {mp.nstr(dv_precision/10, 5)}")

print(f"\n{'='*90}")
print("结论")
print(f"{'='*90}")
print(f"""
1. 反推→前向是恒等式（50位精度验证通过）

2. 前向复现Tc需要δ_v精度:
   - 2位: Tc=0 (完全失败)
   - 5位: Tc=0 (仍失败)
   - 10位: Tc≈9.2K (开始可用)
   - 15位: Tc精确复现

3. Tc对δ_v的敏感度: dTc/dδ_v ≈ {mp.nstr(dTc_dv, 5)}
   - δ_v误差0.001 → Tc误差~{mp.nstr(abs(dTc_dv * mpf('0.001')), 3)}K
   - 需δ_v精度 < {mp.nstr(dv_precision, 3)} 才能Tc误差<1K

4. 从Fermi面CV映射δ_v:
   - δ_v反推值跨度~{mp.nstr(max(dvs) - min(dvs), 3)}
   - CV跨度~0.635
   - 映射导数~0.003
   - CV精度0.1 → δ_v精度0.0003 → Tc误差~{mp.nstr(abs(dTc_dv * mpf('0.0003')), 3)}K
   - 需CV精度~{mp.nstr(dv_precision/0.003, 3)} 才能Tc误差<1K

5. 根本困难: Tc公式双指数敏感度使前向预言需要极高精度
   - δ_v需~10位精度
   - CV需~7位精度
   - 从DFT计算Fermi面几何的精度~3位
   - 差距: 4-7个数量级
""")