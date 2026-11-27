# -*- coding: utf-8 -*-
"""
环 15 / 第 219 轮：δ ≤ 1/3 − (9/500)/T²（T ≥ 1）的数值核对（反馈层，不反充第一性输入）

链内本环给出：w ≥ 1/(3T) − 1/(60T³)、h ≤ 1/(2T) − 1/(24T³) + 1/(240T⁵)（T ≥ 1），
交叉相乘后余量 1.52T⁴ − 1.46T² − 0.054（T=1 处 0.006）。
脚本核对三件事：[1] 界是否成立且贴住；[2] 余量单调性；[3] 与真 δ 的相对松紧。
"""
import numpy as np

def w_of_T(T, n=400001):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def delta_true(T):
    return 1.0 - w_of_T(T) / np.tanh(1.0 / (2.0 * T))

def delta_bound(T):
    return 1.0 / 3.0 - (9.0 / 500.0) / T ** 2

def margin_poly(T):
    return 1.52 * T ** 4 - 1.46 * T ** 2 - 0.054

print("[1] δ(T) 与 1/3 − (9/500)/T² 的比较（T ≥ 1）")
print(f"{'T':>8} {'δ_true':>14} {'δ_bound':>14} {'余量':>12} {'成立':>6}")
for T in (1.0, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0):
    d = delta_true(T)
    b = delta_bound(T)
    print(f"{T:>8} {d:>14.9f} {b:>14.9f} {b - d:>12.3e} {str(d <= b):>6}")

print()
print("[2] 交叉相乘后的余量多项式（T ≥ 1 应恒正）")
ts = np.linspace(1.0, 50.0, 5000)
ms = margin_poly(ts)
print(f"  最小余量 = {ms.min():.6f}（T = {ts[ms.argmin()]:.3f}）；T=1 处 {margin_poly(1.0):.6f}")
print(f"  导数在 T=1 处 = {6.08 - 2.92:.3f} > 0，故余量在 T ≥ 1 上单增")

print()
print("[3] 与真 δ 的差距（读数：界在 T=1 最紧，随 T 变松）")
for T in (1.0, 2.0, 5.0, 10.0, 50.0):
    d = delta_true(T)
    b = delta_bound(T)
    print(f"  T={T:>5}: 1/3-δ_true = {1/3-d:.3e}, 界的余量 = {b-d:.3e}, 比值 = {(b-d)/(1/3-d):.3f}")
print("  注：T→∞ 时真值 1/3−δ ~ 1/(45T²)=0.0222/T²，而界给 0.018/T² ⇒ 界始终有效、渐近松 19%。")
