# -*- coding: utf-8 -*-
"""第 207 轮：尾段排除的数值旁证（$T\\ge1$ 时 $D<0$ 的界与 $\delta<1/3$ 的余量）。

只验证纸面判据里的三条不等式在数值上成立、并给出余量：
  A. tanh(u a) >= u tanh(a)  (a>0, u in [0,1])   -> w >= (2/3)h -> delta <= 1/3
  C. R(delta) <= R(1/3) = 2/3
  D. lambda(T) >= lambda(1) = 1/sinh(1) = 0.850918... > 2/3 (T >= 1)
不提供方程形式、不调参，只作约束/反馈层。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False


def w_h(T, N=400001):
    u = np.linspace(0.0, 1.0, N)
    a = 1.0 / (2.0 * T)
    return np.trapezoid(2.0 * u * np.tanh(u * a), u), np.tanh(a)


def delta(T, N=400001):
    w, h = w_h(T, N)
    return 1.0 - w / h


def R(d):
    return d * (1.0 + d) / (1.0 - d)


def lam(T):
    return 1.0 / (T * np.sinh(1.0 / T))


print("=" * 78)
print("第 207 轮：尾段不等式组的数值旁证")
print("=" * 78)
print(f"lambda(1) = 1/sinh(1) = {1.0/np.sinh(1.0):.9f}   2/3 = {2.0/3.0:.9f}")
print(f"R(1/3) = {(1/3)*(4/3)/(2/3):.9f}")
print()

print("A 项：w >= (2/3)h 的余量（w/((2/3)h) - 1）")
for T in [0.05, 0.1, 0.3, 0.5, 1.0, 3.0, 10.0, 100.0]:
    w, h = w_h(T)
    ratio = w / ((2.0 / 3.0) * h)
    print(f"  T={T:7.2f}  w={w:.9f}  (2/3)h={(2.0/3.0)*h:.9f}  余量 {ratio-1:+.3e}  delta={1-w/h:.9f}")

print()
print("C/D 项：T>=1 时 D = R(delta) - lambda 的值与上界")
print(f"  {'T':>8} {'delta':>12} {'R(delta)':>12} {'lambda':>12} {'D':>14} {'R-2/3':>12} {'lambda-2/3':>12}")
for T in [1.0, 1.5, 2.0, 3.0, 10.0, 30.0, 100.0]:
    d = delta(T)
    print(f"  {T:8.2f} {d:12.9f} {R(d):12.9f} {lam(T):12.9f} {R(d)-lam(T):14.9f} "
          f"{R(d)-2.0/3.0:12.3e} {lam(T)-2.0/3.0:12.3e}")

Ts = np.linspace(0.03, 1.50, 2001)
Dv = np.array([R(delta(T, 20001)) - lam(T) for T in Ts])
fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.4))
ax[0].plot(Ts, Dv, color="#1f4e79", lw=1.6, label=r"$D(T)=R(\delta)-\lambda$")
ax[0].axhline(0.0, color="k", lw=0.8, ls="--")
ax[0].axvline(1.0, color="#c00000", ls=":", lw=0.9, label=r"$T=1$（尾段界起点）")
ax[0].axvline(0.3439, color="#2e7d32", ls=":", lw=0.9, label=r"$T_{\min}\approx0.344$")
ax[0].set_xlabel(r"$T$"); ax[0].set_ylabel(r"$D$")
ax[0].set_title(r"(a) 尾段：$T\geq 1$ 时 $D<0$ 的数值显影")
ax[0].legend(fontsize=8)

ax[1].plot(Ts, [delta(T, 20001) for T in Ts], color="#7030a0", lw=1.6, label=r"$\delta(T)$")
ax[1].axhline(1.0 / 3.0, color="#c00000", lw=0.9, ls="--", label=r"$\delta=1/3$（上界）")
ax[1].set_xlabel(r"$T$"); ax[1].set_ylabel(r"$\delta$")
ax[1].set_title(r"(b) $\delta$ 严格低于 $1/3$，向 $1/3$ 单调逼近")
ax[1].legend(fontsize=8)
fig.tight_layout()
fig.savefig("环15_尾段界_数值旁证.png", dpi=140)
print("\n图已保存：环15_尾段界_数值旁证.png")
