# -*- coding: utf-8 -*-
"""
G19 容差标定的数值核对（环 6）。

1. theta_lin: 精确 theta = 2*pi*s*(1-exp(2*lam)) 与线性 -4*pi*s*lam 的偏差；
2. fidelity: cos(s*N*eps) 的周期与死区；
3. w(tau): Debye 谱精确积分（Z 与 V_coh 之比，不是拟合）；
4. onset: 解 w(tau)*cos(Theta) = g*tau 得 tau_*(eps)。

只用 numpy + matplotlib；不引入 scipy。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环06_G19容差.png")
OUT_CSV = os.path.join(HERE, "环06_G19容差.csv")

TWO_PI = 2.0 * np.pi


# ---------------------------------------------------------------- Debye 权重
def nB(y):
    """Bose 占据，带溢出保护。"""
    y = np.asarray(y, dtype=float)
    out = np.empty_like(y)
    small = y < 1e-8
    out[small] = 1.0 / np.maximum(y[small], 1e-300)
    big = ~small
    with np.errstate(over="ignore"):
        out[big] = 1.0 / np.expm1(y[big])
    return out


def w_debye(tau, xgrid=None):
    """w(tau) = 2 * int_0^1 x / (1 + 2 n_B(x/tau)) dx。tau = T/omega_D。"""
    if xgrid is None:
        xgrid = np.linspace(0.0, 1.0, 4001)
    if tau <= 0:
        return 1.0
    occ = 1.0 + 2.0 * nB(xgrid / tau)
    f = xgrid / occ
    return float(2.0 * np.trapezoid(f, xgrid))


# ---------------------------------------------------------------- theta 与线性
def theta_exact(lam, s=1.0):
    return TWO_PI * s * (1.0 - np.exp(2.0 * lam))


def theta_linear(lam, s=1.0):
    return -4.0 * np.pi * s * lam


# ---------------------------------------------------------------- onset
def tau_onset(Theta, g, wtab_tau, wtab_val, amp=1.0):
    """解 A*amp * w(tau)*cos(Theta) = g*tau。无解返回 nan。"""
    c = np.cos(Theta)
    if c <= 0.0:
        return np.nan
    c = c * amp
    F = wtab_val * c - g * wtab_tau
    idx = np.where(F <= 0.0)[0]
    if idx.size == 0:
        return np.nan
    i = idx[0]
    if i == 0:
        return float(wtab_tau[0])
    lo, hi = wtab_tau[i - 1], wtab_tau[i]
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        Fm = w_debye(mid) * c - g * mid
        if Fm > 0:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def main():
    rows = []

    # ---- 1. 线性化偏差
    lams = np.array([-0.001, -0.003, -0.01, -0.03, -0.1, -0.2])
    rel = []
    for lam in lams:
        te = theta_exact(lam)
        tl = theta_linear(lam)
        rel.append(abs(te - tl) / abs(te))
        rows.append(("lin_rel_error", lam, te, tl, rel[-1]))
    for lam, r in zip(lams, rel):
        print(f"lam={lam:+.3f}  rel_err={r*100:.4f}%")

    # ---- 2. 死区（s=1, N=1）
    dead = []
    for k in range(0, 2):
        dead.append((np.pi / 2 + TWO_PI * k, 3 * np.pi / 2 + TWO_PI * k))
    print("dead zones (eps, s=N=1):", [(round(a, 6), round(b, 6)) for a, b in dead])
    rows.append(("dead_zone", dead[0][0], dead[0][1], np.nan, np.nan))
    # ---- 3. w(tau)
    taus = np.logspace(-2, 1.2, 60)
    ws = np.array([w_debye(t) for t in taus])
    for t in [0.1, 0.5, 1.0, 3.0, 10.0]:
        wv = w_debye(t)
        rows.append(("w_debye", t, wv, 1.0 / (3.0 * t), np.nan))
    print(f"w(0.1)={w_debye(0.1):.6f}  w(1)={w_debye(1.0):.6f}  w(10)={w_debye(10.0):.6f}")
    print(f"high-T check: 1/(3*tau) at tau=10 -> {1/30:.6f}")

    # ---- 4. onset tau_*(eps)
    tau_tab = np.linspace(1e-3, 12.0, 4001)
    w_tab = np.array([w_debye(t) for t in tau_tab])
    eps = np.linspace(0.0, 2.0 * TWO_PI, 801)
    specs = [
        ("A=1, g=0.02", 0.02, lambda e: 1.0, "tab:blue"),
        ("A=1, g=0.05", 0.05, lambda e: 1.0, "tab:orange"),
        (r"A=$\varepsilon/(\pi/2)$, g=0.05", 0.05,
         lambda e: min(e / (np.pi / 2.0), 1.0), "tab:green"),
    ]
    curves = {}
    for label, g, afun, col in specs:
        tstar = np.array([tau_onset(e, g, tau_tab, w_tab, amp=afun(e)) for e in eps])
        curves[label] = (tstar, col)
        rows.append(("onset", g, np.nan, np.nan, float(np.nanmax(tstar))))
        peaks = []
        seg = []
        for e, t in zip(eps, tstar):
            if np.isfinite(t):
                seg.append((e, t))
            elif seg:
                peaks.append(max(seg, key=lambda p: p[1]))
                seg = []
        if seg:
            peaks.append(max(seg, key=lambda p: p[1]))
        print(f"{label}: finite frac={np.isfinite(tstar).mean():.3f}; peaks=" +
              ", ".join(f"(eps={p[0]:.3f},tau*={p[1]:.4f})" for p in peaks[:4]))

    # ---- 写 CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.0, 9.2))

    # A: 精确 vs 线性
    lam = np.linspace(-0.25, 0.0, 500)
    ax[0, 0].plot(lam, theta_exact(lam), lw=2.2, color="tab:blue",
                  label=r"精确 $\theta=2\pi s(1-e^{2\lambda})$")
    ax[0, 0].plot(lam, theta_linear(lam), lw=1.6, ls="--", color="tab:red",
                  label=r"线性 $-4\pi s\lambda$")
    for lm in (-0.01, -0.1):
        ax[0, 0].axvline(lm, color="0.6", lw=0.8, ls=":")
        ax[0, 0].annotate(f"{abs(theta_exact(lm)-theta_linear(lm))/abs(theta_exact(lm))*100:.2f}%",
                          xy=(lm, theta_exact(lm)), xytext=(lm + 0.008, theta_exact(lm) * 0.55),
                          fontsize=8, color="0.3")
    ax[0, 0].set_xlabel(r"$\lambda=\ln r$")
    ax[0, 0].set_ylabel(r"$\theta$")
    ax[0, 0].set_title("A  相位：精确式与线性式（s=1）")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B: 保真度与死区
    ee = np.linspace(0.0, 2.0 * TWO_PI, 1200)
    for N, col in [(1, "tab:blue"), (2, "tab:orange"), (5, "tab:green")]:
        ax[0, 1].plot(ee, np.cos(N * ee), lw=1.7, color=col, label=f"N={N}")
    ax[0, 1].axhspan(-1.05, 0.0, color="tab:red", alpha=0.08)
    ax[0, 1].axvspan(np.pi / 2, 3 * np.pi / 2, color="tab:red", alpha=0.10)
    ax[0, 1].axvline(np.pi / 2, color="tab:red", lw=0.9, ls="--")
    ax[0, 1].axvline(3 * np.pi / 2, color="tab:red", lw=0.9, ls="--")
    ax[0, 1].text(np.pi, 0.62, "死区\n(N=1)", ha="center", fontsize=8, color="tab:red")
    ax[0, 1].set_xlabel(r"$\varepsilon$（每边亏角）")
    ax[0, 1].set_ylabel(r"$\cos(sN\varepsilon)$")
    ax[0, 1].set_title("B  保真度：周期 $2\\pi/(sN)$，红色为死区")
    ax[0, 1].legend(fontsize=8, loc="lower right")
    ax[0, 1].grid(alpha=0.3)

    # C: w(tau)
    ax[1, 0].loglog(taus, ws, lw=2.2, color="tab:purple", label=r"$w(\tau)$ Debye 精确")
    hi = taus >= 2.0
    ax[1, 0].loglog(taus[hi], 1.0 / (3.0 * taus[hi]), lw=1.4, ls="--", color="0.35",
                    label=r"高温渐近 $\omega_D/(3T)=1/(3\tau)$")
    lo = taus <= 0.35
    ax[1, 0].loglog(taus[lo], 1.0 - (np.pi ** 2 / 3.0) * taus[lo] ** 2,
                    lw=1.4, ls=":", color="tab:red",
                    label=r"低温渐近 $1-\frac{\pi^2}{3}\tau^2$")
    ax[1, 0].set_xlabel(r"$\tau=T/\omega_D$")
    ax[1, 0].set_ylabel(r"$w(\tau)$")
    ax[1, 0].set_title("C  相干权重：随温度单调减（双对数）")
    ax[1, 0].legend(fontsize=7)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: tau_*(eps)
    for label, (t, col) in curves.items():
        ax[1, 1].plot(eps, t, lw=1.9, color=col, label=label)
    for a, b in dead:
        if a < eps[-1]:
            ax[1, 1].axvspan(a, min(b, eps[-1]), color="tab:red", alpha=0.10)
    ax[1, 1].set_xlabel(r"$\varepsilon$")
    ax[1, 1].set_ylabel(r"$\tau_*=T_*/\omega_D$")
    ax[1, 1].set_title("D  局域闭合温度：叶心在 $\\varepsilon\\equiv0\\ (2\\pi)$")
    ax[1, 1].legend(fontsize=7)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("saved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
