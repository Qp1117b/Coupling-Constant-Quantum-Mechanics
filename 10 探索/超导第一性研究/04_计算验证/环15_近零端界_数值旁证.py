# -*- coding: utf-8 -*-
"""第 211 轮：近零端 D>0 的数值旁证（T<=1/10 的三条界与余量）。

只验证纸面三条不等式在数值上成立并给余量：
  A. delta(T) >= (8/15)T^2      （T<=1/10）
  B. lambda(T) <= T^2/3         （T<=1/10）
  C. D(T) = R(delta) - lambda > 0（T<=1/10，实际极小值处 D 下界 T^2/5 = 0.2T^2）
不提供方程形式、不调参，只作约束/反馈层。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


def w_of(T, N=1_000_001):
    u = np.linspace(0.0, 1.0, N)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)


def quantities(T):
    h = np.tanh(1.0 / (2.0 * T))
    w = np.array([w_of(t) for t in np.atleast_1d(T)])
    delta = 1.0 - w / np.tanh(1.0 / (2.0 * np.atleast_1d(T)))
    lam = 1.0 / (np.atleast_1d(T) * np.sinh(1.0 / np.atleast_1d(T)))
    R = delta * (1.0 + delta) / (1.0 - delta)
    D = R - lam
    return delta, lam, D


T = np.array([0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.10])
delta, lam, D = quantities(T)

print("T, delta/T^2, 8/15, lambda/T^2, 1/3, D, T^2/5")
for t, d, l, dd in zip(T, delta, lam, D):
    print(f"{t:.4f}  {d/t**2:.6f}  {8/15:.6f}  {l/t**2:.6f}  {1/3:.6f}  {dd:.6e}  {t**2/5:.3e}")

print("min margin A:", np.min(delta / T**2 - 8 / 15))
print("min margin B:", np.min(1 / 3 - lam / T**2))
print("min D on grid:", np.min(D), "at T=", T[np.argmin(D)])

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ax.plot(T, delta / T**2, "o-", label="δ(T)/T²")
ax.axhline(8 / 15, color="r", ls="--", label="8/15")
ax.set_title("(a) δ ≥ (8/15)T²（近零端）")
ax.set_xlabel("T")
ax.legend()
ax.grid(alpha=0.3)

ax = axes[1]
ax.plot(T, lam / T**2, "o-", label="λ(T)/T²")
ax.axhline(1 / 3, color="r", ls="--", label="1/3")
ax.set_title("(b) λ ≤ T^2/3（近零端）")
ax.set_xlabel("T")
ax.legend()
ax.grid(alpha=0.3)

ax = axes[2]
ax.plot(T, D, "o-", label="D(T)=R(δ)−λ")
ax.plot(T, T**2 / 5, "r--", label="T²/5（下界）")
ax.axhline(0, color="k", lw=0.8)
ax.set_title("(c) 近零端 D>0")
ax.set_xlabel("T")
ax.legend()
ax.grid(alpha=0.3)

fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.12, wspace=0.25)
fig.savefig("环15_近零端界_数值旁证.png", dpi=200)
print("saved 环15_近零端界_数值旁证.png")
