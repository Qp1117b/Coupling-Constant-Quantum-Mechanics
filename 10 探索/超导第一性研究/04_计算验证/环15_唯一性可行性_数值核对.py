# -*- coding: utf-8 -*-
"""第 213 轮数值可行性核对：判据差零点的唯一性路线。

只做"路线是否成立"的核对（反馈层），不提供方程形式、不反充第一性输入：
  (a) Q(T) = lambda(T)/R(delta(T)) 是否在 [1/10, 1] 上严格单增（若单增，D=0 至多一解）；
  (b) 对数导数比较 (ln lambda)' - (ln R)' 的符号；
  (c) D' 的零点、D'' 的变号，用来否证"D' 单调"一类捷径。
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


def w_of_T(T):
    u = np.linspace(0.0, 1.0, 4001)
    f = 2.0 * u * np.tanh(u / (2.0 * T))
    return np.trapezoid(f, u)


def wp_of_T(T):
    u = np.linspace(0.0, 1.0, 4001)
    f = u * u / np.cosh(u / (2.0 * T)) ** 2
    return -np.trapezoid(f, u) / T ** 2


def h_of_T(T):
    return np.tanh(1.0 / (2.0 * T)) if T > 0 else 1.0


def delta_of_T(T):
    return 1.0 - w_of_T(T) / h_of_T(T)


def lam_of_T(T):
    return 1.0 / (T * np.sinh(1.0 / T))


def R_of_d(d):
    return d * (1.0 + d) / (1.0 - d)


def Rp_of_d(d):
    return (1.0 + 2.0 * d - d * d) / (1.0 - d) ** 2


def delta_deriv(T):
    """202/204 的 delta' 闭式：-(w'h + w*sech^2(1/(2T))/(2T^2))/h^2。"""
    w = w_of_T(T)
    wp = wp_of_T(T)
    h = h_of_T(T)
    s2 = 1.0 / np.cosh(1.0 / (2.0 * T)) ** 2
    return -(wp * h + w * s2 / (2.0 * T ** 2)) / h ** 2


def lam_deriv(T):
    """lambda(T)=1/(T sinh(1/T)) 的导数闭式：lambda'=(cosh(1/T)/T - sinh(1/T))/(T sinh(1/T)^2)。"""
    s = 1.0 / T
    sh = np.sinh(s)
    ch = np.cosh(s)
    return (ch / T - sh) / (T * T * sh ** 2)


def D_of_T(T):
    d = delta_of_T(T)
    return R_of_d(d) - lam_of_T(T)


def Dp_of_T(T):
    return Rp_of_d(delta_of_T(T)) * delta_deriv(T) - lam_deriv(T)


Ts = np.linspace(0.10, 1.00, 901)

d = np.array([delta_of_T(t) for t in Ts])
lam = np.array([lam_of_T(t) for t in Ts])
R = R_of_d(d)
Q = lam / R                       # D=0 <=> Q=1
D = R - lam
Dp = np.array([Dp_of_T(t) for t in Ts])
dpad = np.array([delta_deriv(t) for t in Ts])
lp = np.array([lam_deriv(t) for t in Ts])

# 对数导数比较
lndQ = lp / lam - Rp_of_d(d) * dpad / R

# 数值差分核对 D'
hstep = 1e-6
Dp_fd = np.array([(D_of_T(t + hstep) - D_of_T(t - hstep)) / (2 * hstep) for t in Ts])
Dpp = np.gradient(Dp, Ts)

# 零点
def zeros(x, y):
    idx = np.where(np.sign(y[:-1]) * np.sign(y[1:]) < 0)[0]
    out = []
    for i in idx:
        out.append(x[i] - y[i] * (x[i + 1] - x[i]) / (y[i + 1] - y[i]))
    return out

zD = zeros(Ts, D)
zDp = zeros(Ts, Dp)
sign_changes_Dpp = zeros(Ts, Dpp)

# 打印
print("[1] Q = lambda/R 区间端点与单调性")
print(f"  Q(0.10)={Q[0]:.10f}  Q(1.00)={Q[-1]:.10f}")
print(f"  Q 最小值={Q.min():.10f} (T={Ts[Q.argmin()]:.5f})  最大值={Q.max():.10f} (T={Ts[Q.argmax()]:.5f})")
print(f"  相邻差分 sign 变化次数 = {len(zeros(Ts, np.diff(Q)))}")
print(f"  (ln Q)' 最大值 = {lndQ.max():.6e} 于 T={Ts[lndQ.argmax()]:.5f}；最小值 = {lndQ.min():.6e} 于 T={Ts[lndQ.argmin()]:.5f}")
print(f"  (ln Q)' <= 0 的格点数 = {(lndQ <= 0).sum()} / {len(Ts)}")

print("\n[2] D 的零点")
for z in zD:
    print(f"  T* = {z:.9f}   D' 在该点 {Dp_of_T(z):+.6e}")

print("\n[3] D' 的零点与 D'' 变号（否证 D' 单调）")
for z in zDp:
    print(f"  D' 零点 T = {z:.9f}")
print(f"  D'' 变号点: {['%.5f' % z for z in sign_changes_Dpp]}")
print(f"  D' 极小 = {Dp.min():.9f} (T={Ts[Dp.argmin()]:.5f})；极大 = {Dp.max():.9f} (T={Ts[Dp.argmax()]:.5f})")
print(f"  D' 闭式 vs 中心差分 最大绝对误差 = {np.max(np.abs(Dp - Dp_fd)):.3e}")

print("\n[4] 关键量")
for t in (0.10, 0.15, 0.20, 0.3529, 1.00):
    print(f"  T={t:.4f}: delta={delta_of_T(t):.9f} lam={lam_of_T(t):.9f} R={R_of_d(delta_of_T(t)):.9f} Q={lam_of_T(t)/R_of_d(delta_of_T(t)):.9f} D={D_of_T(t):+.9f} D'={Dp_of_T(t):+.9f}")
print(f"  delta' 最大 = {dpad.max():.6f} (T={Ts[dpad.argmax()]:.5f})；最小 = {dpad.min():.6f}")
print(f"  (ln lambda)' 最小 = {(lp/lam).min():.6f} (T={Ts[(lp/lam).argmin()]:.5f})")
print(f"  R'/R 最大 = {(Rp_of_d(d)/R).max():.6f} (T={Ts[(Rp_of_d(d)/R).argmax()]:.5f})")

np.savetxt("环15_唯一性可行性_输出.txt", np.column_stack([Ts, d, lam, R, Q, D, Dp, lndQ]),
           header="T\tdelta\tlambda\tR\tQ=lambda/R\tD\tD'\t(lnQ)'", comments="#", fmt="%.12e")

fig, ax = plt.subplots(1, 3, figsize=(15, 4.4))
ax[0].plot(Ts, Q, color="#1f77b4")
ax[0].axhline(1.0, color="k", lw=0.8, ls="--")
ax[0].axvline(zD[0] if zD else np.nan, color="r", lw=0.8, ls=":")
ax[0].set_title("(a) Q(T)=lambda/R(delta) 与 Q=1")
ax[0].set_xlabel("T"); ax[0].grid(alpha=0.3)

ax[1].plot(Ts, lndQ, color="#2ca02c")
ax[1].axhline(0.0, color="k", lw=0.8, ls="--")
ax[1].set_title("(b) (ln Q)' 的符号")
ax[1].set_xlabel("T"); ax[1].grid(alpha=0.3)

ax[2].plot(Ts, Dp, color="#d62728", label="D' closed form")
ax[2].plot(Ts, Dp_fd, color="k", ls=":", lw=0.8, label="central diff")
for z in zDp:
    ax[2].axvline(z, color="gray", lw=0.7, ls="--")
ax[2].axhline(0.0, color="k", lw=0.8)
ax[2].set_title("(c) D' 及其零点（D' 非单调）")
ax[2].set_xlabel("T"); ax[2].legend(fontsize=8); ax[2].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("环15_唯一性可行性_数值核对.png", dpi=150)
print("\n[saved] 环15_唯一性可行性_输出.txt / 环15_唯一性可行性_数值核对.png")

