# -*- coding: utf-8 -*-
"""
环 10 温度桥：Debye 多模相干权重 vs 单模 tanh 代理。

归一化单位：omega_D = 1, k_B = 1, hbar = 1.
本脚本只核对解析恒等式、渐近标度与交点，不做数据拟合。
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

omega_D = 1.0
omega = np.linspace(0.0, omega_D, 40001)


def w_debye(T):
    """V_coh/Z = (2/omega_D^2) * ∫_0^omega_D omega tanh(omega/2T) domega."""
    if T <= 0:
        return 1.0
    integrand = omega * np.tanh(omega / (2.0 * T))
    return 2.0 * np.trapezoid(integrand, omega) / omega_D**2


def w_single(T):
    """06 §0.5 的单模代理 tanh(omega_D/2T)."""
    if T <= 0:
        return 1.0
    return np.tanh(omega_D / (2.0 * T))


def bisect_root(f, lo, hi, tol=1e-12, n=200):
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        raise ValueError(f"root not bracketed: f({lo})={flo}, f({hi})={fhi}")
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if abs(fm) < tol or 0.5 * (hi - lo) < tol:
            return mid
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return 0.5 * (lo + hi)


# 温度网格：低 T 用对数，高 T 用线性，合并去重
T_lo = np.logspace(-3, 0, 240)
T_hi = np.linspace(0.0, 10.0, 260)
T = np.unique(np.concatenate([T_lo, T_hi]))

wD = np.array([w_debye(t) for t in T])
wS = np.array([w_single(t) for t in T])
x = T / omega_D
w_high = 1.0 / (3.0 * np.maximum(x, 1e-12))
w_low = 1.0 - (np.pi**2 / 3.0) * x**2
sigma_norm = np.sqrt(np.maximum(wD, 0.0))

# BKT 交点：Upsilon0=1, w(T)=2T/pi
x_BKT_D = bisect_root(lambda t: w_debye(t) - 2.0 * t / np.pi, 1e-3, 2.0)
x_BKT_S = bisect_root(lambda t: w_single(t) - 2.0 * t / np.pi, 1e-3, 2.0)

# sigma_l = sqrt(V_coh) 的阈值交点：sigma_c=0.95 => w=0.9025
sigma_c = 0.95
x_pair = bisect_root(lambda t: w_debye(t) - sigma_c**2, 1e-3, 2.0)

# 关键数值
w_low_x = 0.01
w_high_x = 10.0
vals = {
    "w_debye(Tmin)": w_debye(1e-3),
    "w_debye(Tmax)": w_debye(10.0),
    "w_single(Tmin)": w_single(1e-3),
    "w_single(Tmax)": w_single(10.0),
    "x_BKT_debye": x_BKT_D,
    "x_BKT_single": x_BKT_S,
    "x_pair_sigma0.95": x_pair,
    "w_debye(x=0.01)": w_debye(w_low_x),
    "1-w_debye(x=0.01)": 1.0 - w_debye(w_low_x),
    "(pi^2/3)x^2(x=0.01)": (np.pi**2 / 3.0) * w_low_x**2,
    "ratio_low_asym": (1.0 - w_debye(w_low_x)) / ((np.pi**2 / 3.0) * w_low_x**2),
    "w_debye(x=10)": w_debye(w_high_x),
    "x*w_debye(x=10)": w_high_x * w_debye(w_high_x),
    "x*w_single(x=10)": w_high_x * w_single(w_high_x),
}

print("== 环 10 温度桥关键数值 ==")
for k, v in vals.items():
    print(f"{k:>24s} = {v:.12g}")

print("\n== 渐近残差 ==")
print(f"max |w_debye - (1-(pi^2/3)x^2)|, x<=0.02 = "
      f"{np.max(np.abs(wD[x <= 0.02] - w_low[x <= 0.02])):.6e}")
print(f"low-T coefficient (pi^2/3) = {np.pi**2/3.0:.12g}")
print(f"max |x*w_debye - 1/3|, x>=5 = "
      f"{np.max(np.abs(x[x >= 5] * wD[x >= 5] - 1.0/3.0)):.6e}")
print(f"max |x*w_single - 1/2|, x>=5 = "
      f"{np.max(np.abs(x[x >= 5] * wS[x >= 5] - 0.5)):.6e}")

# CSV
out_dir = Path(__file__).resolve().parent
csv_path = out_dir / "环10_温度桥.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow([
        "T_over_omegaD", "w_debye", "w_single", "w_high_asym",
        "w_low_asym", "sigma_norm", "upsilon_norm", "bkt_line", "ratio_debye_single"
    ])
    for i in range(len(T)):
        writer.writerow([
            f"{x[i]:.10g}", f"{wD[i]:.10g}", f"{wS[i]:.10g}",
            f"{w_high[i]:.10g}", f"{w_low[i]:.10g}",
            f"{sigma_norm[i]:.10g}", f"{wD[i]:.10g}",
            f"{2.0*x[i]/np.pi:.10g}",
            f"{(wD[i]/wS[i] if wS[i] > 0 else float('nan')):.10g}"
        ])

# 图像
fig, axes = plt.subplots(2, 2, figsize=(12, 8.5))

ax = axes[0, 0]
ax.plot(x, wD, label="Debye 多模 $V_{coh}/Z$", lw=2.2, color="#1f77b4")
ax.plot(x, wS, label="单模代理 $\\tanh(\\omega_D/2T)$", lw=1.6, ls="--", color="#d62728")
ax.plot(x, w_high, label="高温渐近 $1/(3x)$", lw=1.0, ls=":", color="#2ca02c")
ax.set_xlim(0, 5)
ax.set_ylim(0, 1.05)
ax.set_xlabel("$T/\\omega_D$")
ax.set_ylabel("$w(T)$")
ax.set_title("(a) 相干权重：多模与单模")
ax.legend(fontsize=8)
ax.grid(alpha=0.25)

ax = axes[0, 1]
mask = (x > 0) & (x <= 0.2)
ax.loglog(x[mask], 1.0 - wD[mask], lw=2.0, label="Debye $1-w$", color="#1f77b4")
ax.loglog(x[mask], (np.pi**2 / 3.0) * x[mask]**2, ls="--", lw=1.4,
          label="$\\frac{\\pi^2}{3}(T/\\omega_D)^2$", color="#2ca02c")
ax.loglog(x[mask], 2.0 * np.exp(-1.0 / (2.0 * x[mask])), ls=":", lw=1.4, label="单模 $2e^{-\\omega_D/2T}$", color="#d62728")
ax.set_xlabel("$T/\\omega_D$")
ax.set_ylabel("$1-w$")
ax.set_ylim(1e-7, 2e-2)
ax.set_title("(b) 低温：Debye 是 $T^2$，不是指数")
ax.legend(fontsize=8)
ax.grid(alpha=0.25, which="both")

ax = axes[1, 0]
mask = (x >= 1.0) & (x <= 10.0)
ax.plot(x[mask], x[mask] * wD[mask], lw=2.0, label="Debye $xw$", color="#1f77b4")
ax.plot(x[mask], x[mask] * wS[mask], lw=1.6, ls="--", label="单模 $xw$", color="#d62728")
ax.axhline(1.0/3.0, ls=":", lw=1.2, color="#2ca02c", label="Debye 高温极限 $1/3$")
ax.axhline(1.0/2.0, ls=":", lw=1.2, color="#ff7f0e", label="单模高温极限 $1/2$")
ax.set_xlim(1, 10)
ax.set_ylim(0.25, 0.55)
ax.set_xlabel("$T/\\omega_D$")
ax.set_ylabel("$T w(T)/\\omega_D$")
ax.set_title("(c) 高温系数：多模是 1/3，单模是 1/2")
ax.legend(fontsize=8)
ax.grid(alpha=0.25)

ax = axes[1, 1]
ax.plot(x, wD, lw=2.0, label="$\\Upsilon(T)/\\Upsilon_0=w(T)$", color="#1f77b4")
ax.plot(x, 2.0 * x / np.pi, lw=1.5, ls="--", label="BKT 线 $2T/(\\pi\\Upsilon_0)$", color="#d62728")
ax.axvline(x_BKT_D, ls=":", lw=1.2, color="#2ca02c", label=f"Debye $T_{{BKT}}={x_BKT_D:.3f}$")
ax.axvline(x_BKT_S, ls=":", lw=1.2, color="#ff7f0e", label=f"单模 $T_{{BKT}}={x_BKT_S:.3f}$")
ax.plot(x_pair, sigma_c**2, "o", ms=5, color="#9467bd", label=f"$\\sigma_c=0.95$ 交点 $T={x_pair:.3f}$")
ax.set_xlim(0, 2.0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("$T/\\omega_D$")
ax.set_ylabel("归一化刚度 / 阈值")
ax.set_title("(d) BKT 交点与配对阈值交点")
ax.legend(fontsize=8)
ax.grid(alpha=0.25)

fig.suptitle("环 10 温度桥：Debye 相干权重、刚度与交点（归一化单位；非数据拟合）", fontsize=11)
fig.tight_layout(rect=[0, 0, 1, 0.96])
png_path = out_dir / "环10_温度桥.png"
fig.savefig(png_path, dpi=180)
print(f"\nSaved: {csv_path.name}, {png_path.name}")
