# -*- coding: utf-8 -*-
"""第 206 轮第 0–1 步可行性评估：判据差 D 的二阶结构（D'' 符号、D' 零点唯一性、λ' 单峰）。

用途：检验 205 停点写下的意图命题"D' 在 (0,∞) 严格单减"是否成立——若不成立，
则 206 环的意图命题必须改写（改为"D' 零点唯一"），并把被否证的强命题记入 DISCARD。
只读既有 Spec v32 的闭式，作反馈层核对，不改方程、不调参。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

NQ = 4001


def _grid(T):
    u = np.linspace(0.0, 1.0, NQ * 4 + 1)
    h = 1.0 / (2.0 * T)
    return u, np.tanh(u * h), 1.0 / np.cosh(u * h) ** 2


def shape_h(T):
    return np.tanh(1.0 / (2.0 * T))


def w_gap(T):
    u, tanh, _ = _grid(T)
    return np.trapezoid(2.0 * u * tanh, u)


def abs_w_deriv(T):
    u, _, sech2 = _grid(T)
    return np.trapezoid(u ** 2 * sech2, u) / T ** 2


def deficit(T):
    return 1.0 - w_gap(T) / shape_h(T)


def deficit_deriv(T):
    h = shape_h(T)
    s = 1.0 / np.cosh(1.0 / (2.0 * T)) ** 2
    return -((-abs_w_deriv(T)) * h + w_gap(T) * s / (2.0 * T ** 2)) / h ** 2


def ratio(d):
    return d * (1.0 + d) / (1.0 - d)


def ratio_deriv(d):
    return (1.0 + 2.0 * d - d ** 2) / (1.0 - d) ** 2


def lam(T):
    return 1.0 / (T * np.sinh(1.0 / T))


def lam_deriv(T):
    return (np.cosh(1.0 / T) / T - np.sinh(1.0 / T)) / (T * np.sinh(1.0 / T)) ** 2


def gap(T):
    return ratio(deficit(T)) - lam(T)


def gap_deriv(T):
    return ratio_deriv(deficit(T)) * deficit_deriv(T) - lam_deriv(T)


def num_deriv(f, T, dT=1e-6):
    return (f(T + dT) - f(T - dT)) / (2.0 * dT)


print("=" * 74)
print("第 206 轮第 0–1 步：D 的二阶结构（检验 D' 单调性是否成立）")
print("=" * 74)

Ts = np.linspace(0.03, 1.50, 3001)
Dp = np.array([gap_deriv(T) for T in Ts])
Dpp = np.array([num_deriv(gap_deriv, T) for T in Ts])
L1 = np.array([lam_deriv(T) for T in Ts])
d1 = np.array([deficit_deriv(T) for T in Ts])

print("\n[1] D' 是否严格单减？相邻差 dD'/dT 的符号统计")
neg = int(np.sum(np.diff(Dp) < 0))
pos = int(np.sum(np.diff(Dp) > 0))
print(f"    dD' < 0 的区间段数 {neg}，dD' > 0 的区间段数 {pos}（共 {len(Dp)-1} 段）")
idx_min = int(np.argmin(Dp))
print(f"    D' 的最小值 {Dp[idx_min]: .6f} 于 T={Ts[idx_min]:.5f}")
print(f"    D'(0.10)={gap_deriv(0.10): .6f}  D'(0.20)={gap_deriv(0.20): .6f}  "
      f"D'(0.3439)={gap_deriv(0.3439): .6f}  D'(1.20)={gap_deriv(1.20): .6f}  "
      f"D'(1.50)={gap_deriv(1.50): .6f}")

print("\n[2] D'' 的符号变号点")
idx = np.where(np.sign(Dpp[:-1]) != np.sign(Dpp[1:]))[0]
print(f"    变号次数 = {len(idx)}")
for i in idx[:5]:
    print(f"      T ∈ ({Ts[i]:.5f}, {Ts[i+1]:.5f})  D'' 由 {Dpp[i]: .3e} 到 {Dpp[i+1]: .3e}")

print("\n[3] D' 的零点（决定 D 的单峰位置）")
z = np.where(np.sign(Dp[:-1]) != np.sign(Dp[1:]))[0]
print(f"    零点数 = {len(z)}")
for i in z:
    lo, hi = Ts[i], Ts[i + 1]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if gap_deriv(lo) * gap_deriv(mid) <= 0:
            hi = mid
        else:
            lo = mid
    print(f"    T* = {0.5*(lo+hi):.9f}   D' 两侧: {gap_deriv(Ts[i]): .3e} / {gap_deriv(Ts[i+1]): .3e}")

print("\n[4] λ'(T) 的形状：两端趋于 0 的钟形？")
idx_max = int(np.argmax(L1))
print(f"    λ' 最大 {L1[idx_max]: .6f} 于 T={Ts[idx_max]:.5f}")
for T in [0.05, 0.15, 0.3439, 0.60, 1.00, 1.50]:
    print(f"      T={T:6.4f}  λ'={lam_deriv(T): .6f}")

print("\n[5] δ'(T) 的单调性（δ'' 的符号）")
print(f"    相邻差为正的段数 {int(np.sum(np.diff(d1) > 0))}（应为 0）")
print(f"    δ'(0.15)={deficit_deriv(0.15): .6f}  δ'(1.20)={deficit_deriv(1.20): .6f}")

fig, ax = plt.subplots(1, 3, figsize=(16.5, 4.8))
ax[0].plot(Ts, L1, color="#1f4e79", lw=1.6)
ax[0].axvline(Ts[idx_max], color="#c00000", ls=":", lw=0.9,
              label=rf"$\lambda'$ 极大 $\approx{Ts[idx_max]:.3f}$")
ax[0].set_xlabel(r"$T$"); ax[0].set_ylabel(r"$\lambda'$")
ax[0].set_title(r"(a) $\lambda'$ 是钟形（两端趋于 0）")
ax[0].legend(fontsize=8)

ax[1].plot(Ts, Dp, color="#7030a0", lw=1.6, label=r"$D'(T)$")
ax[1].axhline(0.0, color="k", lw=0.8, ls="--")
ax[1].axvline(Ts[idx_min], color="#c00000", ls=":", lw=0.9,
              label=rf"$D'$ 极小 $\approx{Ts[idx_min]:.3f}$")
ax[1].set_xlabel(r"$T$"); ax[1].set_ylabel(r"$D'$")
ax[1].set_title(r"(b) $D'$ 不是单调：先降后升（U 形）")
ax[1].legend(fontsize=8)

ax[2].plot(Ts, np.sign(Dpp), color="#2e7d32", lw=1.4, label=r"$\mathrm{sign}\,D''$")
ax[2].set_xlabel(r"$T$"); ax[2].set_ylabel(r"sign")
ax[2].set_title(r"(c) $D''$ 变号一次（$D'$ 的拐点）")
ax[2].legend(fontsize=8)

fig.tight_layout()
fig.savefig("环15_判据差二阶_数值核对.png", dpi=140)
print("\n[6] 图已保存：环15_判据差二阶_数值核对.png")
