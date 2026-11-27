# -*- coding: utf-8 -*-
"""第 205 轮数值核对：判据差 D(T)=R(δ(T))-λ(T) 的导数结构（G-188b-2j 前件）。

只作约束／反馈层旁证：不反充第一性输入、不据数值调参。
闭式全部取自 Spec v32：deficitDeriv / ratioFunDeriv / lambdaDeriv / criterionGapDeriv。
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
    tanh = np.tanh(u * h)
    sech2 = 1.0 / np.cosh(u * h) ** 2
    return u, tanh, sech2


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
    wd = -abs_w_deriv(T)                      # w 单调减
    return -((wd * h + w_gap(T) * s / (2.0 * T ** 2)) / h ** 2)


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


def fd_gap_deriv(T, dT=1e-6):
    return (gap(T + dT) - gap(T - dT)) / (2.0 * dT)


print("=" * 72)
print("第 205 轮：判据差导数结构与交点定位的数值核对")
print("=" * 72)

# ---- 1. D' 闭式 vs 中心差分 ----
print("\n[1] D'(T) 闭式 vs 中心差分（dT=1e-6）")
for T in [0.10, 0.15, 0.20, 0.30, 0.3439, 0.45, 0.70, 1.00, 1.20]:
    a = gap_deriv(T)
    b = fd_gap_deriv(T)
    rel = abs(a - b) / max(abs(b), 1e-30)
    print(f"  T={T:7.4f}  D'={a: .6e}  FD={b: .6e}  rel={rel:.2e}")

# ---- 2. D 的值与零点 ----
print("\n[2] D 与 D' 的采样（T：δ／R／λ／D／D'）")
for T in [0.15, 0.1941, 0.30, 0.3439, 0.40, 0.70, 1.20]:
    d = deficit(T)
    print(f"  T={T:7.4f}  δ={d:.6f}  R={ratio(d):.6f}  λ={lam(T):.6f}  "
          f"D={gap(T): .6e}  D'={gap_deriv(T): .6e}")

Ts = np.linspace(0.03, 1.5, 3001)
D = np.array([gap(T) for T in Ts])
Dp = np.array([gap_deriv(T) for T in Ts])
sign_change = np.where(np.sign(Dp[:-1]) != np.sign(Dp[1:]))[0]
print("\n[3] D' 在 (0.03,1.5) 的变号点数 =", len(sign_change))
for i in sign_change:
    print(f"    变号于 T ∈ ({Ts[i]:.5f}, {Ts[i+1]:.5f})")

idx_max = int(np.argmax(D))
print(f"[4] D 的极大值 D={D[idx_max]:.6e} 于 T={Ts[idx_max]:.5f}（D'={(Dp[idx_max]): .3e}）")

zero = np.where(np.sign(D[:-1]) != np.sign(D[1:]))[0]
print("[5] D 的零点数 =", len(zero))
for i in zero:
    lo, hi = Ts[i], Ts[i + 1]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if gap(lo) * gap(mid) <= 0:
            hi = mid
        else:
            lo = mid
    print(f"    T_min = {0.5*(lo+hi):.9f}   两端 D: {gap(Ts[i]): .3e} / {gap(Ts[i+1]): .3e}")

print(f"\n[6] 边界行为：T=0.03 -> D={gap(0.03): .3e}, T=1.50 -> D={gap(1.50): .3e}")
print("[7] δ' 全检：min =", min(deficit_deriv(T) for T in Ts), " 负值点 =",
      sum(1 for T in Ts if deficit_deriv(T) < 0))
print("[8] λ' 全检：min =", min(lam_deriv(T) for T in Ts), " 负值点 =",
      sum(1 for T in Ts if lam_deriv(T) < 0))

# ---- 图：三面板 ----
fig, ax = plt.subplots(1, 3, figsize=(16.5, 4.8))

ax[0].plot(Ts, D, color="#1f4e79", lw=1.8, label=r"$D(T)=R(\delta(T))-\lambda(T)$")
ax[0].axhline(0.0, color="k", lw=0.8, ls="--")
ax[0].axvline(0.343857873, color="#c00000", lw=0.9, ls=":",
              label=r"$T_{\min}=0.343857873$")
ax[0].set_xlabel(r"$T$")
ax[0].set_ylabel(r"$D$")
ax[0].set_title(r"(a) 判据差 $D$ 与唯一零点")
ax[0].legend(fontsize=8)

ax[1].plot(Ts, Dp, color="#7030a0", lw=1.6, label=r"$D'(T)$")
ax[1].axhline(0.0, color="k", lw=0.8, ls="--")
ax[1].axvline(0.1941, color="#c00000", lw=0.9, ls=":",
              label=r"$D'$ 变号 $\approx0.1941$")
ax[1].set_xlabel(r"$T$")
ax[1].set_ylabel(r"$D'$")
ax[1].set_title(r"(b) $D'$ 只变号一次（单峰）")
ax[1].legend(fontsize=8)

Ts2 = np.linspace(0.10, 1.20, 60)
rel = [abs(gap_deriv(T) - fd_gap_deriv(T)) / max(abs(fd_gap_deriv(T)), 1e-30) for T in Ts2]
ax[2].semilogy(Ts2, rel, "o-", ms=3.2, color="#2e7d32")
ax[2].set_xlabel(r"$T$")
ax[2].set_ylabel("相对误差")
ax[2].set_title(r"(c) $D'$ 闭式 vs 中心差分")
ax[2].grid(alpha=0.3)

fig.tight_layout()
fig.savefig("环15_判据差导数_数值核对.png", dpi=140)
print("\n[9] 图已保存：环15_判据差导数_数值核对.png")
