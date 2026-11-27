# -*- coding: utf-8 -*-
"""环 15（第 204 轮）数值核对：δ 的导数闭式、严格单增与右端 R(δ(T)) 的单增（G-188b-2i 前件）。
只作外部约束/反馈：验证闭式与差分一致、符号全正、关键核不等式与点位不等式成立；
不反充第一性输入、不调参。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

U = np.linspace(0.0, 1.0, 20001)

def wGap(T):
    return np.trapezoid(2 * U * np.tanh(U / (2 * T)), U)

def wDeriv(T):
    """w'(T) = -(1/T^2) * ∫ u^2 sech^2(u/(2T)) du"""
    return -(1.0 / T ** 2) * np.trapezoid(U ** 2 / np.cosh(U / (2 * T)) ** 2, U)

def fields(T):
    h = np.tanh(1.0 / (2 * T))
    S = 1.0 / np.cosh(1.0 / (2 * T)) ** 2
    w = wGap(T)
    Phi = w / h
    delta = 1 - Phi
    lam = S / (2 * T * h)
    R = delta * (1 + delta) / (1 - delta)
    return dict(h=h, S=S, w=w, Phi=Phi, delta=delta, lam=lam, R=R)

def deficitDeriv(T):
    f = fields(T)
    wp = wDeriv(T)
    return -(wp * f["h"] + f["w"] * f["S"] / (2 * T ** 2)) / f["h"] ** 2

# ---------- 1. δ' 闭式 vs 差分 ----------
print("=== 1. δ' 闭式 vs 中心差分 ===")
for T in [0.15, 0.30, 0.3439, 0.50, 0.70, 1.20]:
    dT = 1e-6
    dnum = (fields(T + dT)["delta"] - fields(T - dT)["delta"]) / (2 * dT)
    dan = deficitDeriv(T)
    print(f"  T={T:6.4f}: 闭式={dan:+.8f} 差分={dnum:+.8f} rel={abs(dan - dnum) / abs(dnum):.3e}")

# ---------- 2. δ' 全正（301 点，含两端与相切区） ----------
Ts = np.linspace(0.030, 1.500, 301)
d_delta = np.array([deficitDeriv(T) for T in Ts])
print("=== 2. δ'(T) > 0 全检 ===")
print("  点数 =", len(Ts), " 最小 δ' =", float(d_delta.min()), " 负值点数 =", int((d_delta <= 0).sum()))
print("  0<δ<1 违反点数 =", int(sum(1 for T in Ts if not (0 < fields(T)["delta"] < 1))))

# ---------- 3. 关键核不等式 S*w < 2 T^2 h |w'| ----------
print("=== 3. 核不等式 sech^2(1/2T)*w < 2T^2 tanh(1/2T)*|w'| ===")
viol = 0; worst = 1e9
for T in Ts:
    f = fields(T)
    lhs = f["S"] * f["w"]
    rhs = 2 * T ** 2 * f["h"] * abs(wDeriv(T))
    ratio = lhs / rhs
    worst = min(worst, 1 - ratio)
    if ratio >= 1:
        viol += 1
print("  违反点数 =", viol, " 最小相对余量 (1-比值) =", float(worst))

# ---------- 4. 点位不等式 sinh(2us) <= u sinh(2s)（u∈[0,1]） ----------
print("=== 4. 点位不等式 sinh(2us) ≤ u sinh(2s) ===")
bad = 0; maxdiff = -1e9
for s in [0.5, 1.0, 2.0, 3.3333, 10.0]:
    for u in np.linspace(1e-6, 1.0, 2001):
        d = np.sinh(2 * u * s) - u * np.sinh(2 * s)
        maxdiff = max(maxdiff, d)
        if d > 1e-12 * max(1.0, abs(u * np.sinh(2 * s))):
            bad += 1
print("  违反点数 =", bad, " 最大超出 =", float(maxdiff))

# ---------- 5. δ 严格单增 与 R(δ(T)) 单增 ----------
delta = np.array([fields(T)["delta"] for T in Ts])
R_T = np.array([fields(T)["R"] for T in Ts])
print("=== 5. δ 与 R(δ(T)) 的相邻差 ===")
print("  δ 相邻差全 > 0 :", bool((np.diff(delta) > 0).all()), " 最小相邻差 =", float(np.diff(delta).min()))
print("  R 相邻差全 > 0 :", bool((np.diff(R_T) > 0).all()), " 最小相邻差 =", float(np.diff(R_T).min()))

# ---------- 6. 交点 T_min（沿用 203 的二分） ----------
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
else:
    Tmin = float("nan")
print("=== 6. 交点 ===")
print("  T_min =", Tmin, " δ(T_min) =", fields(Tmin)["delta"], " Φ(T_min) =", fields(Tmin)["Phi"])
print("  δ'(T_min) =", deficitDeriv(Tmin))

print("=== 采样行 T：δ / δ' / R / R' 与核不等式比值 ===")
fR = np.array([fields(T)["R"] for T in Ts])
dR = np.gradient(fR, Ts)
for T in [0.15, 0.30, 0.3439, 0.40, 0.70, 1.20]:
    f = fields(T)
    ratio = f["S"] * f["w"] / (2 * T ** 2 * f["h"] * abs(wDeriv(T)))
    print(f"  {T:6.4f}: δ={f['delta']:.6f} δ'={deficitDeriv(T):.6f} "
          f"R={f['R']:.6f} dR/dT={np.interp(T, Ts, dR):.6f} 核比={ratio:.6f}")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
ax[0].plot(Ts, delta, color="C0", label="δ(T)=1-Φ(T)")
ax[0].plot(Ts, d_delta, color="C1", label="δ'(T)（闭式）")
ax[0].axhline(0, linestyle=":", color="gray")
ax[0].axvline(Tmin, linestyle=":", color="k", label=f"T_min={Tmin:.6f}")
ax[0].set_xlabel("T"); ax[0].set_ylabel("δ, δ'"); ax[0].legend(); ax[0].set_title("(a) δ 严格单增且 δ'>0 处处成立")

ratio = np.array([fields(T)["S"] * fields(T)["w"] /
                  (2 * T ** 2 * fields(T)["h"] * abs(wDeriv(T))) for T in Ts])
ax[1].plot(Ts, ratio, color="C2", label="S·w /(2T²h|w'|)")
ax[1].axhline(1, linestyle=":", color="r", label="临界 1")
ax[1].set_xlabel("T"); ax[1].set_ylabel("核不等式比值"); ax[1].legend()
ax[1].set_title("(b) 核不等式严格成立：比值 < 1")

ax[2].plot(Ts, R_T, color="C3", label="R(δ(T))")
ax[2].axvline(Tmin, linestyle=":", color="k")
ax[2].plot([Tmin], [fields(Tmin)["lam"]], "o", color="k", markersize=4, label="交点 λ=R")
ax[2].set_xlabel("T"); ax[2].set_ylabel("R"); ax[2].legend()
ax[2].set_title("(c) 右端 R(δ(T)) 随 T 严格单增")
plt.tight_layout()
plt.savefig("环15_δ导数与核不等式_数值核对.png", dpi=150)
print("plot saved")
