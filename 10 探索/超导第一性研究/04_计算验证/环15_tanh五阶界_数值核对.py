"""
环 15 / 第 218 轮：五阶上界的数值旁证 + 由它合成的 delta 上界（反馈层，不反充第一性输入）

链内本环已证：tanh s <= s - s^3/3 + 2s^5/15 (0 <= s <= 1)。
脚本核对：
  [1] 五阶界余量非负；
  [2] 把它与 217 的三阶下界合用，得到 delta <= 1 - w_lb/h_ub，
      并读出 c(T) = T^2*(1/3 - delta_ub) 的取值（决定 219 能否写 delta <= 1/3 - c/T^2）。
"""
import numpy as np

def w_of_T(T, n=400001):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def w_lb(T):   # 1/(3T) - 1/(60 T^3)
    return 1.0 / (3.0 * T) - 1.0 / (60.0 * T ** 3)

def h_ub(T):   # s - s^3/3 + 2 s^5/15, s = 1/(2T)
    s = 1.0 / (2.0 * T)
    return s - s ** 3 / 3.0 + 2.0 * s ** 5 / 15.0

print("[1] 五阶界 tanh s <= s - s^3/3 + 2s^5/15 的余量（0 <= s <= 1）")
ss = np.linspace(0.0, 1.0, 2001)
res = (ss - ss ** 3 / 3.0 + 2.0 * ss ** 5 / 15.0) - np.tanh(ss)
print(f"  最小余量 = {res.min():.3e}（s = {ss[res.argmin()]:.3f}）；s=0.5 处余量 = {res[np.argmin(abs(ss-0.5))]:.4e}")
print(f"  s=1 处：上界={1 - 1/3 + 2/15:.6f}, tanh 1={np.tanh(1.0):.6f}")

print()
print("[2] 合成：delta <= 1 - w_lb/h_ub，读 c(T) = T^2*(1/3 - delta_ub)（T >= 1）")
print(f"{'T':>6} {'delta_true':>12} {'delta_ub':>12} {'1/3-delta_ub':>14} {'c(T)':>10} {'界成立?':>8}")
for T in (1.0, 1.5, 2.0, 3.0, 5.0, 10.0, 50.0):
    d = 1.0 - w_of_T(T) / np.tanh(1.0 / (2.0 * T))
    dub = 1.0 - w_lb(T) / h_ub(T)
    c = T * T * (1.0 / 3.0 - dub)
    print(f"{T:>6} {d:>12.8f} {dub:>12.8f} {1/3 - dub:>14.8e} {c:>10.6f} {str(d <= dub):>8}")
print("  注：c(T) 在 T>=1 上由约 0.0180 升到 0.0222（T→∞ 极限为 1/45=0.022222），故 219 的候选常数为 0.018。")
