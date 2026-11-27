# -*- coding: utf-8 -*-
"""第 223 轮：w 的七阶双侧界数值核对 + 判号可行域复核
（构造后验数字校验，待独立复现）

复合上界公式（与 Spec `deficitDerivAlt` 同形）：
  2(h-w)/(T h)          -> 上界 2(h_ub - w_lb)/(T h_lb)
  w sech^2/(2T^2 h^2)   -> 下界 w_lb (1 - h_ub^2)/(2T^2 h_ub^2)
"""
import numpy as np

NQ = 4000


def w_gap(T, n=NQ):
    u = np.linspace(0, 1, n)
    return np.trapezoid(2 * u * np.tanh(u / (2 * T)), u)


def h_(T):
    return np.tanh(1 / (2 * T))


def S3(x):
    return x - x ** 3 / 3 + 2 * x ** 5 / 15 - 17 * x ** 7 / 315


def S4(x):
    return S3(x) + 62 * x ** 9 / 2835


def w_lb(T):
    return 1 / (3 * T) - 1 / (60 * T ** 3) + 1 / (840 * T ** 5) - 17 / (181440 * T ** 7)


def w_ub(T):
    return w_lb(T) + 31 / (3991680 * T ** 9)


def deficit(T):
    return 1 - w_gap(T) / h_(T)


def deficit_d(T, eps=1e-6):
    return (deficit(T + eps) - deficit(T - eps)) / (2 * eps)


def delta_ub(T):
    return 1 - w_lb(T) / S4(1 / (2 * T))


def delta_d_ub(T):
    hl = S3(1 / (2 * T))
    hu = S4(1 / (2 * T))
    first = 2 * (hu - w_lb(T)) / (T * hl)
    Klow = w_lb(T) * (1 - hu ** 2) / (2 * T ** 2 * hu ** 2)
    return first - Klow


def W(d):
    return 1 / d + 1 / (1 + d) + 1 / (1 - d)


def A_lb(T):
    hu = S4(1 / (2 * T))
    num = 1 + hu ** 2 - 2 * T * hu
    return num / (2 * T ** 2 * hu)


print("=" * 78)
print("表 1  w 双侧界精度 (lb<=w<=ub)")
print(f"{'T':>6} {'w_num':>14} {'w_lb':>14} {'w_ub':>14} {'lb%':>9} {'ub%':>9}")
for T in [0.50, 0.55, 0.60, 0.70, 0.80, 1.0, 2.0, 5.0]:
    wv, a, b = w_gap(T), w_lb(T), w_ub(T)
    print(f"{T:6.2f} {wv:14.9f} {a:14.9f} {b:14.9f} "
          f"{100*(a-wv)/wv:9.4f} {100*(b-wv)/wv:9.4f}")

print("=" * 78)
print("表 2  delta_ub 与 delta'_ub(正确复合式) 及与真值之比")
print(f"{'T':>6} {'delta':>10} {'delta_ub':>10} {'dd':>10} {'dd_ub':>10} {'ratio':>9}")
for T in [0.50, 0.60, 0.70, 0.80, 0.90, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0]:
    dt, du = deficit(T), delta_ub(T)
    q, qu = deficit_d(T), delta_d_ub(T)
    print(f"{T:6.2f} {dt:10.6f} {du:10.6f} {q:10.6f} {qu:10.6f} {qu/q:9.5f}")

print("=" * 78)
print("表 3  sup(dd_ub/dd) 与 sup(delta_ub/delta) 细网格")
for lo, hi in [(0.5, 1.0), (1.0, 5.0)]:
    Ts = np.linspace(lo, hi, 451)
    r = np.array([delta_d_ub(T) / deficit_d(T) for T in Ts])
    rd = np.array([delta_ub(T) / max(deficit(T), 1e-12) for T in Ts])
    print(f"T in [{lo},{hi}]:  sup dd_ub/dd = {r.max():.5f} @ {Ts[int(np.argmax(r))]:.4f}"
          f"   sup delta_ub/delta = {rd.max():.5f}")
print(f"T=0.5 边界: dd={deficit_d(0.5):.6f} dd_ub={delta_d_ub(0.5):.6f} ratio={delta_d_ub(0.5)/deficit_d(0.5):.5f}")

print("=" * 78)
print("表 4 判号 (lnQ)'>0 的充分条件：A_lb >= dd_ub * W(delta_ub)")
print(f"{'T':>6} {'A_lb':>11} {'ddW_true':>11} {'ddubWub':>11} {'surplus':>10} {'verdict':>7}")
ok_all = True
for T in [0.50, 0.60, 0.70, 0.80, 0.90, 1.0, 1.2, 1.5, 2.0, 3.0, 5.0]:
    al = A_lb(T)
    prod_b = delta_d_ub(T) * W(delta_ub(T))
    ok = al >= prod_b
    ok_all &= ok
    print(f"{T:6.2f} {al:11.7f} {delta_d_ub(T)*W(deficit(T)):11.7f} {prod_b:11.7f} "
          f"{al/prod_b:10.4f} {'PASS' if ok else 'FAIL':>7}")

print("=" * 78)
Ts = np.linspace(0.5, 5.0, 451)
marg = np.array([A_lb(T) - delta_d_ub(T) * W(delta_ub(T)) for T in Ts])
print(f"T in [0.5,5]:  min surplus = {marg.min():.6f} @ T = {Ts[int(np.argmin(marg))]:.4f}")
print(f"  (surplus>0 处即 (lnQ)'>0 得证；surplus<0 处不足)")
print(f"umin surplus 区间例: T = 0.5..{Ts[np.argmax(marg < 0)]:.3f} 内仍有负值")
print(f"S4(1)-tanh(1) = {S4(1.0)-np.tanh(1.0):.3e}")
print(f"w_ub(0.5) 相对误差 = {100*(w_ub(0.5)-w_gap(0.5))/w_gap(0.5):.4f}%")
