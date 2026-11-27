# -*- coding: utf-8 -*-
"""环 15（第 203 轮）数值核对：判据两侧的单调性（G-188b-2h 前件）。
只做外部约束/反馈：验证单增/值域、定位交点与"两侧同增仍不足"的增速交叉；不反充第一性输入。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

def wGap(T):
    u = np.linspace(0.0, 1.0, 20001)
    return np.trapezoid(2 * u * np.tanh(u / (2 * T)), u)

def fields(T):
    h = np.tanh(1.0 / (2 * T))
    S = 1.0 / np.cosh(1.0 / (2 * T)) ** 2
    Phi = wGap(T) / h
    delta = 1 - Phi
    lam = S / (2 * T * h)
    lam_alt = 1.0 / (T * np.sinh(1.0 / T))
    R = delta * (1 + delta) / (1 - delta)
    return dict(h=h, S=S, Phi=Phi, delta=delta, lam=lam, lam_alt=lam_alt, R=R)

# ---------- 1. R(delta) 纯代数单增 ----------
print("=== 1. R(delta) 单增（纯代数）===")
a = np.linspace(0.001, 0.999, 2000)
R = a * (1 + a) / (1 - a)
print("  相邻差全 > 0 :", bool((np.diff(R) > 0).all()))
print("  R(0.1)=", float(np.interp(0.1, a, R)), " R(0.5)=", float(np.interp(0.5, a, R)),
      " R(0.9)=", float(np.interp(0.9, a, R)))
ra = 0.30; rb = 0.55
Ra = ra * (1 + ra) / (1 - ra); Rb = rb * (1 + rb) / (1 - rb)
diff_formula = (rb - ra) * (1 + ra + rb - ra * rb) / ((1 - ra) * (1 - rb))
print("  (a=0.30,b=0.55): R(b)-R(a)=", Rb - Ra, " 闭式差=", diff_formula,
      " 相对差=", abs((Rb - Ra) - diff_formula) / abs(diff_formula))

# ---------- 2. lambda 严格单增与值域 ----------
Ts = np.linspace(0.030, 1.500, 3001)
lam = np.array([fields(T)["lam"] for T in Ts])
R_T = np.array([fields(T)["R"] for T in Ts])
Phi = np.array([fields(T)["Phi"] for T in Ts])
delta = np.array([fields(T)["delta"] for T in Ts])
rel = np.abs([fields(T)["lam"] - fields(T)["lam_alt"] for T in Ts]) / np.abs(lam)

print("=== 2. lambda 严格单增 / 值域 ===")
print("  相邻差全 > 0 :", bool((np.diff(lam) > 0).all()),
      " 最小相邻差 =", float(np.diff(lam).min()))
print("  max lambda =", float(lam.max()), " min lambda =", float(lam.min()))
print("  0<lambda<1 违反点数 =", int(((lam <= 0) | (lam >= 1)).sum()))
print("  lambda 闭式 vs 窗口商 max rel err =", float(rel.max()))
print("  lambda(0.05)=", float(np.interp(0.05, Ts, lam)), " lambda(1.199)=", float(np.interp(1.199, Ts, lam)))

# ---------- 3. 解析导数：dlambda/dT > 0 ----------
def dlam(T):
    s = 1.0 / T
    return (np.sinh(s) - s * np.cos(s * 0 + 0) * np.cosh(s)) / (np.sinh(s) ** 2) * (-1.0 / T ** 2)

def dlam2(T):
    s = 1.0 / T
    return ((np.sinh(s) - s * np.cosh(s)) / np.sinh(s) ** 2) * (-1.0 / T ** 2)

d_lam = np.array([dlam2(T) for T in Ts])
print("=== 3. dlambda/dT（闭式 sin h s - s cosh s < 0 乘 ds/dT<0）===")
print("  min dlambda/dT =", float(d_lam.min()), " 全 > 0 :", bool((d_lam > 0).all()))

# ---------- 4. delta(T) 与 R( delta(T) ) 的单调性（复合侧）----------
dPhi = np.diff(Phi)
print("=== 4. delta(T) 单增（即 Phi 单减）与 R(delta(T)) ===")
print("  dPhi<0 的相邻对数 =", int((dPhi < 0).sum()), " / ", len(dPhi))
print("  R(delta(T)) 相邻差全 > 0 :", bool((np.diff(R_T) > 0).all()))

# ---------- 5. 增速比较：两侧同增仍不足的依据 ----------
dR = np.gradient(R_T, Ts)
rate = d_lam - dR
isign = np.where(np.sign(rate[:-1]) != np.sign(rate[1:]))[0]
print("=== 5. 增速比较 dlambda/dT - dR/dT ===")
print("  符号变化位置 T =", [float(Ts[i]) for i in isign][:6])
print("  在 T=0.15: dlam=", float(np.interp(0.15, Ts, d_lam)), " dR=", float(np.interp(0.15, Ts, dR)),
      " 差=", float(np.interp(0.15, Ts, rate)))
print("  在 T=0.3439: dlam=", float(np.interp(0.3439, Ts, d_lam)), " dR=", float(np.interp(0.3439, Ts, dR)),
      " 差=", float(np.interp(0.3439, Ts, rate)))
print("  在 T=0.70: dlam=", float(np.interp(0.70, Ts, d_lam)), " dR=", float(np.interp(0.70, Ts, dR)),
      " 差=", float(np.interp(0.70, Ts, rate)))

# ---------- 6. 交点（lambda = R）与 T_min ----------
gap = R_T - lam
ii = np.where(np.sign(gap[:-1]) != np.sign(gap[1:]))[0]
print("=== 6. lambda-R 变号 ===")
print("  变号区间 =", [(float(Ts[i]), float(Ts[i + 1])) for i in ii])

def gapfun(T):
    f = fields(T)
    return f["R"] - f["lam"]

lo, hi = 0.30, 0.40
if gapfun(lo) * gapfun(hi) < 0:
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if gapfun(lo) * gapfun(mid) <= 0:
            hi = mid
        else:
            lo = mid
    Tmin = 0.5 * (lo + hi)
    print("  T_min (lambda=R) =", Tmin, "  gap 端值 =", gapfun(lo), gapfun(hi))
    print("  delta(T_min) =", fields(Tmin)["delta"], " Phi(T_min) =", fields(Tmin)["Phi"])
else:
    Tmin = float("nan")
    print("  区间内无变号")

print("=== 采样行 T：Phi / delta / lambda / R / R-lambda / dlam / dR ===")
for T in [0.15, 0.30, 0.3439, 0.40, 0.70, 1.20]:
    f = fields(T)
    print(f"  {T:6.4f}: Phi={f['Phi']:.6f} delta={f['delta']:.6f} lam={f['lam']:.6f} "
          f"R={f['R']:.6f} R-lam={f['R']-f['lam']:+.4e} "
          f"dlam={np.interp(T, Ts, d_lam):.6f} dR={np.interp(T, Ts, dR):.6f}")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
ax[0].plot(Ts, lam, label="lambda(T)")
ax[0].plot(Ts, R_T, label="R(delta(T))")
if np.isfinite(Tmin):
    ax[0].axvline(Tmin, linestyle=":", color="k", label=f"T_min={Tmin:.6f}")
    ax[0].plot([Tmin], [fields(Tmin)["lam"]], "o", color="k", markersize=4)
ax[0].set_xlabel("T"); ax[0].set_ylabel("lambda, R"); ax[0].legend(); ax[0].set_title("(a) 两侧各自单增与唯一交点")

ax[1].plot(Ts, d_lam, label="dlambda/dT")
ax[1].plot(Ts, dR, label="dR/dT")
ax[1].axhline(0, linestyle=":", color="gray")
ax[1].set_xlabel("T"); ax[1].set_ylabel("导数"); ax[1].legend(); ax[1].set_title("(b) 增速比较：同增不等于定号")

ax[2].plot(Ts, lam, label="lambda")
ax[2].axhline(0, linestyle=":", color="gray")
ax[2].axhline(1, linestyle=":", color="gray")
ax[2].axhspan(0, 1, alpha=0.08)
ax[2].set_ylim(-0.05, 1.10); ax[2].set_xlabel("T"); ax[2].set_ylabel("lambda")
ax[2].legend(); ax[2].set_title("(c) 0<lambda<1：左端不可越 1，右端可")
plt.tight_layout()
plt.savefig("环15_判据两侧单调性_交点与增速.png", dpi=150)
print("plot saved")
