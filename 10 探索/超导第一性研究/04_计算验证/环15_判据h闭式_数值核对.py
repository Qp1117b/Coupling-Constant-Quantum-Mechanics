# -*- coding: utf-8 -*-
"""
环 15 / 第 220 轮（纸面环）：判据的 h-闭式与 δ′ 要求的定量化

导出并核对：
  (1) λ = (1−h²)/(2Th)，h = tanh(1/2T)  ⇒  λ′ = (1−h²)(1+h²−2Th)/(4T³h²)
  (2) (ln λ)′ = (1+h²−2Th)/(2T²h)      （λ 的 h-闭式对数导数）
  (3) (ln Q)′ = (1+h²−2Th)/(2T²h) − δ′·(1/δ + 1/(1+δ) + 1/(1−δ))
  (4) 判号要求 δ′ ≤ (1+h²−2Th)/(2T²h·W)，W := 1/δ+1/(1+δ)+1/(1−δ)
      并与真 δ′ 比较，给出余量（这决定 221 需要多精的 δ′ 界）。
"""
import numpy as np

def h_of(T):
    return np.tanh(1.0 / (2.0 * T))

def w_of(T, n=400001):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def delta_of(T):
    return 1.0 - w_of(T) / h_of(T)

def delta_prime(T, eps=1e-5):
    return (delta_of(T + eps) - delta_of(T - eps)) / (2 * eps)

def lam_of(T):
    h = h_of(T)
    return (1.0 - h * h) / (2.0 * T * h)

def lam_prime_formula(T):
    h = h_of(T)
    return (1.0 - h * h) * (1.0 + h * h - 2.0 * T * h) / (4.0 * T ** 3 * h * h)

def lnlam_formula(T):
    h = h_of(T)
    return (1.0 + h * h - 2.0 * T * h) / (2.0 * T ** 2 * h)

def lnq_formula(T):
    d = delta_of(T)
    W = 1.0 / d + 1.0 / (1.0 + d) + 1.0 / (1.0 - d)
    return lnlam_formula(T) - delta_prime(T) * W

print("[1] λ 的 h-闭式：与差分导数比较（相对误差）")
for T in (0.1, 0.2, 0.3439, 0.5, 1.0, 2.0, 5.0):
    lp = (lam_of(T + 1e-6) - lam_of(T - 1e-6)) / 2e-6
    f = lam_prime_formula(T)
    print(f"  T={T:>7}: λ′_差分={lp:>12.6f}, 闭式={f:>12.6f}, 相对差={abs(f-lp)/abs(lp):.2e}")

print()
print("[2] (ln Q)′ 的 h-闭式：与 λ/R 的数值对数导数比较")
for T in (0.1, 0.2, 0.3439, 0.5, 1.0, 1.5, 2.0, 5.0):
    def lnQ(T):
        d = delta_of(T)
        return np.log(lam_of(T)) - np.log(d * (1 + d) / (1 - d))
    num = (lnQ(T + 1e-6) - lnQ(T - 1e-6)) / 2e-6
    f = lnq_formula(T)
    print(f"  T={T:>7}: 数值={num:>10.6f}, 闭式={f:>10.6f}, 绝对差={abs(f-num):.2e}")

print()
print("[3] 判号所需的 δ′ 上界与真 δ′（T ≥ 0.1）")
print(f"{'T':>8} {'δ′真':>12} {'δ′要求':>12} {'余量比':>10} {'1+h²−2Th':>12}")
for T in (0.10, 0.15, 0.20, 0.30, 0.3439, 0.5, 0.75, 1.0, 1.5, 2.0, 5.0):
    d = delta_of(T)
    h = h_of(T)
    W = 1.0 / d + 1.0 / (1.0 + d) + 1.0 / (1.0 - d)
    need = (1.0 + h * h - 2.0 * T * h) / (2.0 * T ** 2 * h * W)
    dp = delta_prime(T)
    print(f"{T:>8} {dp:>12.6f} {need:>12.6f} {need/dp:>10.3f} {1+h*h-2*T*h:>12.6f}")

print()
print("[4] 若把 1+h²−2Th 换成粗下界 h²（由 2Th≤1），要求会变成多少？")
print(f"{'T':>8} {'δ′要求(粗)':>14} {'真 δ′':>12} {'是否可行':>10}")
for T in (0.10, 0.3439, 1.0, 2.0, 5.0):
    d = delta_of(T); h = h_of(T)
    W = 1.0/d + 1.0/(1+d) + 1.0/(1-d)
    need_coarse = (h * h) / (2.0 * T ** 2 * h * W)
    dp = delta_prime(T)
    print(f"{T:>8} {need_coarse:>14.6f} {dp:>12.6f} {str(need_coarse > dp):>10}")
print("  注：粗界在 T≥1 处仍高于真 δ′ 十余倍，说明必须用 1+h²−2Th 的 T⁻² 精度，不能用 h²。")
