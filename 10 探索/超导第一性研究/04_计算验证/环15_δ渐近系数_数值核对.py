"""
环 15 / 第 216 轮：delta 的 T→∞ 渐近系数核对（反馈层，不反充第一性输入）

delta(T) = 1 - Phi(T),  Phi = w/h,  h = tanh(1/(2T)),  w = ∫_0^1 2u tanh(u/(2T)) du
解析展开（本环纸面推导，见主卡 §四十九）：
    delta = 1/3 - 1/(45 T^2) + O(T^-4),      delta' ~ 2/(45 T^3)
本脚本只核对系数 1/45 与 T^2 * delta' 的量级，不生成任何方程形式。
"""
import numpy as np

def w_of_T(T, n=200001):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def h_of_T(T):
    return np.tanh(1.0 / (2.0 * T))

def delta(T):
    return 1.0 - w_of_T(T) / h_of_T(T)

def dprime(T, rel=1e-4):
    dT = rel * T
    return (delta(T + dT) - delta(T - dT)) / (2.0 * dT)

print("[1] 渐近系数 1/45 的核对")
print(f"{'T':>6} {'delta(T)':>16} {'1/3-delta':>12} {'1/(45T^2)':>12} {'比值':>10}")
for T in (5, 10, 20, 50, 100, 200):
    d = delta(T)
    gap = 1.0 / 3.0 - d
    main = 1.0 / (45.0 * T * T)
    print(f"{T:>6} {d:>16.10f} {gap:>12.4e} {main:>12.4e} {gap/main:>10.4f}")

print()
print("[2]  delta' 与 2/(45T^3)、T^2 delta' 的量级")
print(f"{'T':>6} {'delta_center':>14} {'2/(45T^3)':>12} {'比值':>8} {'T^2*delta':>11}")
for T in (1, 2, 5, 10, 50):
    dp = dprime(T)
    main = 2.0 / (45.0 * T ** 3)
    print(f"{T:>6} {dp:>14.8e} {main:>12.4e} {dp/main:>8.3f} {T*T*dp:>11.4e}")

print()
print("[3]  T^2 delta' 在全域的最大值（决定 C 的下界需求）")
Ts = [0.05 + 0.005 * i for i in range(int((10.0 - 0.05) / 0.005) + 1)]
vals = [(T, T * T * dprime(T)) for T in Ts if T > 0.05]
Tmax, vmax = max(vals, key=lambda p: p[1])
print(f"  argmax T = {Tmax:.4f},  T^2 delta' = {vmax:.6f}")
print(f"  参考：若要用 delta' <= C/T^2，则 C 至少需 {vmax:.6f}；链内 T=1 处 delta'(1) = {dprime(1.0):.6f}")
