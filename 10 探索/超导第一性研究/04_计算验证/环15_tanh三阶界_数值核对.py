"""
环 15 / 第 217 轮：三阶 tanh 界的数值旁证（反馈层，不反充第一性输入）

本环链内已证：tanh x >= x - x^3/3 (x >= 0)。
脚本只核对两件事：
  [1] 三阶界在 [0, 3] 上成立且余量非负（tanh 每点不低于下界）；
  [2] 把三阶界逐点代入 w，得到的 delta 上界是 1/3 + 1/(30T^2)（方向错），
      与真 delta 对比，说明 218 必须补 h 的五阶上界。
"""
import numpy as np

def w_of_T(T, n=400001):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def w_lower(T):
    # ∫_0^1 2u (u/2T - u^3/24T^3) du = 1/(3T) - 1/(60T^3)
    return 1.0 / (3.0 * T) - 1.0 / (60.0 * T ** 3)

print("[1] 三阶界 tanh x >= x - x^3/3 的余量（x >= 0）")
xs = np.linspace(0.0, 3.0, 3001)
res = np.tanh(xs) - (xs - xs ** 3 / 3.0)
print(f"  最小余量 = {res.min():.3e}（在 x = {xs[res.argmin()]:.3f}）；最大余量 = {res.max():.3e}（x = {xs[res.argmax()]:.3f}）")
print(f"  x=0.5 处：tanh={np.tanh(0.5):.6f}, 下界={0.5 - 0.125/3:.6f}, 余量={res[np.argmin(abs(xs-0.5))]:.3e}")

print()
print("[2] 三阶代入给出的 delta 上界 vs 真 delta")
print(f"{'T':>5} {'delta_true':>12} {'1/3+1/(30T^2)':>16} {'上界-真值':>12} {'w 下界用得上?':>14}")
for T in (0.5, 1.0, 2.0, 5.0, 10.0):
    d = 1.0 - w_of_T(T) / np.tanh(1.0 / (2.0 * T))
    ub = 1.0 / 3.0 + 1.0 / (30.0 * T ** 2)
    ok = w_lower(T) <= w_of_T(T)
    print(f"{T:>5} {d:>12.8f} {ub:>16.8f} {ub - d:>12.8f} {str(ok):>14}")
print("  注：上界 → 1/3（T→∞），比 1/3 更松；要得到 1/3 - c/T^2 必须补 h 的五阶上界。")
