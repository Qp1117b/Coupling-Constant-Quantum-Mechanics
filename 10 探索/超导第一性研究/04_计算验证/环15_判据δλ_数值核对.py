# -*- coding: utf-8 -*-
"""环 15（第 202 轮）数值核对：判据的 δ／λ 形式与 r 的双侧夹逼（G-188b-2g）。
只做外部约束/反馈：验证恒等式与符号一致性、定位近相切窗口；不反充第一性输入。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

def wGap(T):
    u = np.linspace(0.0, 1.0, 4001)
    return np.trapezoid(2 * u * np.tanh(u / (2 * T)), u)

def wDeriv(T):
    u = np.linspace(0.0, 1.0, 4001)
    return -np.trapezoid(u ** 2 * (1 / np.cosh(u / (2 * T)) ** 2), u) / T ** 2

def fields(T):
    h = np.tanh(1.0 / (2 * T))
    S = 1.0 / np.cosh(1.0 / (2 * T)) ** 2
    w = wGap(T)
    wp = wDeriv(T)
    Phi = w / h
    r = T ** 2 * abs(wp) / S
    S2 = (T ** 2 * abs(wp))  # = dis-scaled numerator
    delta = 1 - Phi
    lam = S / (2 * T * h)
    R = delta * (1 + delta) / (1 - delta)
    G = 2 * T * h * (1 - Phi) * (2 - Phi) - Phi * (1 - h ** 2)
    return dict(h=h, S=S, w=w, wp=wp, Phi=Phi, r=r, delta=delta, lam=lam, R=R, G=G,
                lam_alt=1.0 / (T * np.sinh(1.0 / T)), up=1.0 / (3 * S))

Ts = np.linspace(0.050, 1.199, 1150)
rec = {k: [] for k in ["r", "Phi", "lam", "lam_alt", "R", "G", "up", "delta"]}
for T in Ts:
    f = fields(T)
    for k in rec:
        rec[k].append(f[k])
for k in rec:
    rec[k] = np.array(rec[k])

print("=== 1. r 的双侧夹逼 ===")
print("  min r =", rec["r"].min(), " (>=1/3 违反点数 =", int((rec["r"] < 1/3).sum()), ")")
print("  max r =", rec["r"].max())
print("  r <= 1/(3S) 违反点数 =", int((rec["r"] > rec["up"] + 1e-12).sum()),
      " max(r-(1/(3S))) =", float((rec["r"] - rec["up"]).max()))
print("  1/(3S) 最小值 =", rec["up"].min(), " r 在 T_c 处 =", float(np.interp(0.3, Ts, rec["r"])))

print("=== 2. lambda 初等形式 ===")
rel = np.abs(rec["lam"] - rec["lam_alt"]) / np.abs(rec["lam_alt"])
print("  max rel err =", float(rel.max()))
print("  lambda(T=0.3435) =", float(np.interp(0.3435, Ts, rec["lam"])),
      " lambda(T=0.3) =", float(np.interp(0.3, Ts, rec["lam"])),
      " lambda(T=1.2) =", float(np.interp(1.2, Ts, rec["lam"])))

print("=== 3. 判据一致性：S'<0（用 G>0）vs lambda<R ===")
mismatch = int((np.sign(rec["G"]) != np.sign(rec["R"] - rec["lam"])).sum())
print("  sign(G>0) 与 (lambda<R) 不一致点数 =", mismatch)
idx = [i for i in range(len(Ts) - 1) if np.sign(rec["G"][i]) != np.sign(rec["G"][i + 1])]
print("  G 变号区间 =", [(float(Ts[i]), float(Ts[i+1])) for i in idx])
gap = rec["R"] - rec["lam"]
imin = int(np.argmin(gap))
print("  min(R-lambda) =", float(gap[imin]), " at T =", float(Ts[imin]))

print("=== 4. 近相切窗口（判据可定号的远区）===")
print("  gap(T=0.30) =", float(np.interp(0.30, Ts, gap)),
      " gap(T=0.3435) =", float(np.interp(0.3435, Ts, gap)),
      " gap(T=0.40) =", float(np.interp(0.40, Ts, gap)))
print("  T 使 0<gap<1e-3 的区间：",
      float(Ts[(gap > 0) & (gap < 1e-3)][0]),
      "~", float(Ts[(gap > 0) & (gap < 1e-3)][-1]))

print("=== 采样行 T：Phi / r / lambda / R / G / S ===")
for T in [0.15, 0.30, 0.3435, 0.40, 0.50, 0.70, 1.20]:
    f = fields(T)
    print(f"  {T:5.4f}: Phi={f['Phi']:.6f} r={f['r']:.6f} lam={f['lam']:.6f} "
          f"R={f['R']:.6f} G={f['G']:+.3e} S={f['S']:.6f}")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
ax[0].plot(Ts, rec["r"], label="r(T)")
ax[0].plot(Ts, rec["up"], "--", label="1/(3S)")
ax[0].axhline(1/3, linestyle=":", label="1/3")
ax[0].axhline(1.0, linestyle=":", color="gray", label="r=1")
ax[0].set_ylim(0.2, 4.5); ax[0].set_xlabel("T"); ax[0].set_ylabel("r"); ax[0].legend(); ax[0].set_title("(a) 判据比与夹逼")

ax[1].plot(Ts, rec["R"], label="R(delta)")
ax[1].plot(Ts, rec["lam"], label="lambda=1/(T sinh(1/T))")
ax[1].set_xlabel("T"); ax[1].legend(); ax[1].set_title("(b) 端点尺度与阈值")
zoom = (Ts > 0.32) & (Ts < 0.38)
ax2 = ax[1].inset_axes([0.45, 0.12, 0.5, 0.45])
ax2.plot(Ts[zoom], rec["R"][zoom], label="R")
ax2.plot(Ts[zoom], rec["lam"][zoom], label="lambda")
ax2.set_title("近相切", fontsize=9); ax2.tick_params(labelsize=7)

ax[2].plot(Ts, rec["G"], label="G")
ax[2].plot(Ts, rec["R"] - rec["lam"], "--", label="R-lambda")
ax[2].axhline(0, linestyle=":", color="gray")
ax[2].set_xlabel("T"); ax[2].legend(); ax[2].set_title("(c) 判据同号")
plt.tight_layout()
plt.savefig("环15_判据δλ形式_夹逼与近相切.png", dpi=150)
print("plot saved")
