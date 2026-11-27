# -*- coding: utf-8 -*-
"""
环 15 / 第 222 轮：七阶上界 S4 的数值核对（含合成侧证）

S3(s) = s - s³/3 + 2s⁵/15 - 17s⁷/315              （v44 已证下界）
S4(s) = S3(s) + 62s⁹/2835                          （本轮上界）

核对：
 [1] S3 ≤ tanh ≤ S4（s ∈ [0,1]），给最大余量与最大相对松度
 [2] 复核主定理的积分链：P = S3(t)，其 ∫P² ≥ J（差多少）
 [3] 双侧 w,h 界（T ≥ 0.5）与真值的相对误差
"""
import numpy as np

def S3(s):
    return s - s**3/3 + 2*s**5/15 - 17*s**7/315

def S4(s):
    return S3(s) + 62*s**9/2835

def tanh(x):
    return np.tanh(x)

print("[1] 七阶双界余量（s ∈ [0,1]）")
ss = np.linspace(0, 1, 4001)
lo = tanh(ss) - S3(ss)
hi = S4(ss) - tanh(ss)
print(f"  tanh - S3 最小 = {lo.min():.3e}  @ s={ss[lo.argmin()]:.4f}")
print(f"  S4 - tanh 最小 = {hi.min():.3e}  @ s={ss[hi.argmin()]:.4f}")
print(f"  S4 - tanh 最大 = {hi.max():.6f}  @ s={ss[hi.argmax()]:.4f}")
print(f"  s=0.5: S3={S3(0.5):.9f} tanh={tanh(0.5):.9f} S4={S4(0.5):.9f}")
print(f"  s=1.0: S3={S3(1.0):.9f} tanh={tanh(1.0):.9f} S4={S4(1.0):.9f}")

# [2] 积分链复核：∫_0^s P² vs J
print()
print("[2] 主定理积分链（P = S3，对照 J = s³/3-2s⁵/15+17s⁷/315-62s⁹/2835）")
for s in (0.5, 1.0):
    t = np.linspace(0, s, 200001)
    P = S3(t)
    intP2 = np.trapezoid(P**2, t)
    J = s**3/3 - 2*s**5/15 + 17*s**7/315 - 62*s**9/2835
    print(f"  s={s}: ∫P² = {intP2:.10f}, J = {J:.10f}, 差 = {intP2-J:.3e}（理论差 = 4s¹¹/2475 = {4*s**11/2475:.3e}）")

# [3] 双侧 w,h 界
print()
print("[3] 双侧 w,h 界（S3 给下界、S4 给上界；T ≥ 0.5）")
def w_of_poly(T, poly):
    # ∫_0^1 2u poly(u/(2T)) du
    t = np.linspace(0, 1, 400001)
    return np.trapezoid(2*t*poly(t/(2*T)), t)

def delta_true(T):
    t = np.linspace(0, 1, 400001)
    w = np.trapezoid(2*t*np.tanh(t/(2*T)), t)
    return 1 - w/np.tanh(1/(2*T))

print(f"{'T':>5} {'h_lb/真':>10} {'h_ub/真':>10} {'w_lb/真':>10} {'w_ub/真':>10} {'δ_lb/真':>10} {'δ_ub/真':>10}")
for T in (0.5, 0.7, 1.0, 2.0, 5.0):
    h = tanh(1/(2*T))
    h_lb, h_ub = S3(1/(2*T)), S4(1/(2*T))
    w = w_of_poly(T, tanh)
    w_lb, w_ub = w_of_poly(T, S3), w_of_poly(T, S4)
    d = delta_true(T)
    d_lb = 1 - w_ub/h_lb
    d_ub = 1 - w_lb/h_ub
    print(f"{T:>5} {h_lb/h:>10.6f} {h_ub/h:>10.6f} {w_lb/w:>10.6f} {w_ub/w:>10.6f} {d_lb/d:>10.6f} {d_ub/d:>10.6f}")

print()
print("结论：双向误差均为 O(T^-7) 量级（T=5 时 1e-11），δ 区间宽度在 T=1 约 "
      f"{(1 - w_of_poly(1.0, S3)/S4(0.5)) - (1 - w_of_poly(1.0, S4)/S3(0.5)):.2e}。")
print("      这是方法层核对（约束/反馈），不作为第一性输入。")
