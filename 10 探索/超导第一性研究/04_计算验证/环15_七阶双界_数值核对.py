# -*- coding: utf-8 -*-
"""
环 15 / 第 221 轮（纸面环）：七阶 tanh 双界的可行域核对

七阶（交错级数两项截断，仅在 0 ≤ s ≤ 1 成立）：
  L(s) = s - s³/3 + 2s⁵/15 - 17s⁷/315
  U(s) = L(s) + 62s⁹/2835
数值核对：
 [1] L ≤ tanh ≤ U（s ∈ [0,1]）
 [2] 由 L、U 压出的 w_lb、w_ub、h_lb、h_ub（T ≥ 0.5）
 [3] δ′ 上界 δ′ ≤ 2δ_ub/T − K_lb 与 220 的允许域（1.43 倍）之比
 [4] T < 0.5 时 s = 1/(2T) > 1：双界失效 —— 量化低端另需的命题
"""
import numpy as np

def L(s):
    return s - s**3/3 + 2*s**5/15 - 17*s**7/315

def U(s):
    return L(s) + 62*s**9/2835

def tanh(x):
    return np.tanh(x)

print("[1] 七阶双界在 s ∈ [0,1] 上的余量")
ss = np.linspace(0, 1, 2001)
lo = tanh(ss) - L(ss)
hi = U(ss) - tanh(ss)
print(f"  tanh - L 最小 = {lo.min():.3e}（s={ss[lo.argmin()]:.3f}）")
print(f"  U - tanh 最小 = {hi.min():.3e}（s={ss[hi.argmin()]:.3f}）")
print(f"  s=0.5: L={L(0.5):.9f}, tanh={tanh(0.5):.9f}, U={U(0.5):.9f}")

# 由七阶界积分出的 w,h 界（T>=0.5）
def w_lb(T):
    # ∫2u L(u/2T) du, 0..1
    s = 1/(2*T)
    return 1/(3*T) - 1/(60*T**3) + 1/(840*T**5) - 17/(181440*T**7)

def w_ub(T):
    s = 1/(2*T)
    return w_lb(T) + 62/(7983360*T**9)

def h_lb(T):
    return L(1/(2*T))

def h_ub(T):
    return U(1/(2*T))

def delta_true(T, n=400001):
    u = np.linspace(0, 1, n)
    w = np.trapezoid(2*u*np.tanh(u/(2*T)), u)
    return 1 - w/np.tanh(1/(2*T))

def delta_prime(T, eps=1e-5):
    return (delta_true(T+eps) - delta_true(T-eps))/(2*eps)

def delta_ub(T):
    return 1 - w_lb(T)/h_ub(T)

def K_lb(T):
    hb = h_ub(T)
    return w_lb(T)*(1-hb**2)/(2*T**2*hb**2)

def need(T):
    """220 的允许域：(1+h²−2Th)/(2T²h W)，用精确 h."""
    h = h_ub(T); d = delta_true(T)
    W = 1/d + 1/(1+d) + 1/(1-d)
    return (1+h*h-2*T*h)/(2*T*T*h*W)

print()
print("[2][3] T ∈ [0.5,1]：δ′ 上界 vs 允许域")
print(f"{'T':>6} {'δ′真':>11} {'δ′上界':>11} {'允许域':>10} {'上界/允许':>10} {'h_lb−真':>10} {'h_ub−真':>10}")
for T in (0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 5.0):
    dp = delta_prime(T)
    dub = 2*delta_ub(T)/T - K_lb(T)
    nd = need(T)
    print(f"{T:>6} {dp:>11.6f} {dub:>11.6f} {nd:>10.6f} {dub/nd:>10.3f} {h_lb(T)-tanh(1/(2*T)):>10.2e} {h_ub(T)-tanh(1/(2*T)):>10.2e}")

print()
print("[4] T < 0.5：s = 1/(2T) > 1，七阶界不成立（tanh 级数在 s=π/2 外发散）")
for T in (0.10, 0.20, 0.30, 0.40, 0.45):
    s = 1/(2*T)
    h = np.tanh(s)
    d = delta_true(T)
    W = 1/d + 1/(1+d) + 1/(1-d)
    nd = (1+h*h-2*T*h)/(2*T*T*h*W)
    dp = delta_prime(T)
    print(f"  T={T:>5}: s={s:>6.2f}, δ={d:>7.4f}, 2δ/T={2*d/T:>7.4f}, δ′真={dp:>7.4f}, 允许域={nd:>7.4f}, 2δ/T 是否已超={2*d/T>nd}")
print("  结论：低端 T<0.5 不能用 tanh 多项式界（s>1）；需要另一条只依赖「h≈1、w 接近 1」的估计。")
print(f"  参考：T=0.1 时 δ={delta_true(0.1):.4f}，若只能证 δ≤1/3 则 2δ/T=6.67 ≫ 允许域 2.77。")
