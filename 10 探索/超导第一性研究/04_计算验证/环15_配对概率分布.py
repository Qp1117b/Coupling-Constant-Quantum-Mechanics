"""
环 15：配对概率的 chi-square 分布（条件推导，不是数据拟合）

假设（工作假设，明确标注）：
  delta C_ij 是零均值高斯随机场，局域格胞含 n_cell 个独立模。
  则 n_cell * V_hat / V_coh ~ chi^2_{n_cell}。
  p_pair(T) = Pr[V_hat > sigma_c^2]
            = 1 - F_chi2(n_cell, n_cell * sigma_c^2 / V_coh(T))
            = chi2_sf(n_cell, x),  x = n_cell * sigma_c^2 / (Z w(T)).

  注：n_cell 是 chi-square 统计自由度，不是 06／主链的容量 n_eff；
      两者是否同一对象未证。

输出：
  环15_配对概率分布.csv
  环15_配对概率分布_交点.csv
  环15_配对概率分布.png
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_CSV = os.path.join(HERE, "环15_配对概率分布.csv")
OUT_CROSS = os.path.join(HERE, "环15_配对概率分布_交点.csv")
OUT_PNG = os.path.join(HERE, "环15_配对概率分布.png")

Z = 1.0
OMEGA_D = 1.0
SIGMA_C2 = 0.20          # sigma_c^2 / Z
P_C = 0.592746           # 2D site percolation threshold
N_LIST = [4, 16, 64]
T_GRID = np.logspace(-2, 1, 500)


def w_debye(T):
    """Debye 多模相干权重 w(T)=2∫_0^1 x tanh(x/(2T)) dx."""
    xg = np.linspace(0.0, 1.0, 4000)
    return 2.0 * np.trapezoid(xg * np.tanh(xg / (2.0 * T)), xg)


def chi2_sf_even(n, x):
    """Survival function of chi-square with even n at x.

    For n=2m: sf = exp(-x/2) * sum_{k=0}^{m-1} (x/2)^k / k!.
    """
    if x <= 0.0:
        return 1.0
    if x > 1000.0:
        return 0.0
    m = n // 2
    half = 0.5 * x
    s = 0.0
    term = 1.0
    for k in range(m):
        s += term
        term *= half / (k + 1)
    return math.exp(-half) * s


def p_pair(T, n, sigma_c2=SIGMA_C2):
    w = w_debye(T)
    x = n * sigma_c2 / (Z * w)
    return chi2_sf_even(n, x)


def crossing_T(n, target=P_C, sigma_c2=SIGMA_C2):
    """First T where p_pair(T) <= target; linear interpolation in T."""
    ps = np.array([p_pair(t, n, sigma_c2) for t in T_GRID])
    idx = np.where(ps <= target)[0]
    if len(idx) == 0:
        return float("nan")
    i = idx[0]
    if i == 0:
        return float(T_GRID[0])
    t0, t1 = T_GRID[i - 1], T_GRID[i]
    p0, p1 = ps[i - 1], ps[i]
    return float(t0 + (target - p0) * (t1 - t0) / (p1 - p0))


def low_T_slope(n, sigma_c2, t0=0.005, t1=0.05):
    """Numerical exponent of 1-p_pair ~ T^p at low T."""
    ts = np.logspace(np.log10(t0), np.log10(t1), 24)
    ys = np.array([max(1.0 - p_pair(t, n, sigma_c2), 1e-300) for t in ts])
    return float(np.polyfit(np.log(ts), np.log(ys), 1)[0])


def low_T_excess_slope(n, sigma_c2, t0=0.005, t1=0.05):
    """Numerical exponent of p_pair(0)-p_pair(T) at low T."""
    p0 = chi2_sf_even(n, n * sigma_c2 / Z)
    ts = np.logspace(np.log10(t0), np.log10(t1), 24)
    ys = np.array([max(p0 - p_pair(t, n, sigma_c2), 1e-300) for t in ts])
    return float(np.polyfit(np.log(ts), np.log(ys), 1)[0])


def chi2_sf_asymp(n, x):
    """Leading large-x tail of chi-square with n dof."""
    return (x ** (n / 2 - 1) * math.exp(-x / 2)
            / (2 ** (n / 2 - 1) * math.gamma(n / 2)))


def main():
    w = np.array([w_debye(t) for t in T_GRID])
    p = {n: np.array([chi2_sf_even(n, n * SIGMA_C2 / (Z * wi)) for wi in w])
         for n in N_LIST}
    psync2 = {n: p[n] ** 2 for n in N_LIST}
    psync3 = {n: p[n] ** 3 for n in N_LIST}

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["T_over_omegaD", "w_debye"] +
                    [f"p_pair_n{n}" for n in N_LIST] +
                    ["p_sync_t2_n16", "p_sync_t3_n16"])
        for i, t in enumerate(T_GRID):
            wr.writerow([f"{t:.10g}", f"{w[i]:.12g}"] +
                        [f"{p[n][i]:.12g}" for n in N_LIST] +
                        [f"{psync2[16][i]:.12g}", f"{psync3[16][i]:.12g}"])

    cross_rows = []
    for n in N_LIST:
        cross_rows.append((n, p[n][0], crossing_T(n)))
    for n in [4, 16, 64]:
        for s2 in [0.10, 0.20, 0.30]:
            cross_rows.append((n, s2, crossing_T(n, sigma_c2=s2)))

    with open(OUT_CROSS, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["n_cell", "sigma_c2_over_Z", "T_star_over_omegaD"])
        for n, s2, tstar in cross_rows:
            wr.writerow([n, f"{s2:.6g}", f"{tstar:.12g}"])

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.0))
    ax = axes[0, 0]
    for n in N_LIST:
        ax.plot(T_GRID, p[n], lw=2.0, label=f"n_cell={n}")
    ax.axhline(P_C, color="k", ls="--", lw=1.2, label=f"p_c={P_C:.4f}")
    ax.set_xscale("log")
    ax.set_xlabel(r"$T/\omega_D$")
    ax.set_ylabel(r"$p_{\rm pair}(T)$")
    ax.set_title("(a) chi-square pair occupancy")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    xg = np.logspace(-2, 3, 400)
    for n in N_LIST:
        ax.plot(xg, [chi2_sf_even(n, x) for x in xg], lw=2.0,
                label=f"n_cell={n}")
    ax.set_xscale("log")
    ax.set_xlabel(r"$x=n_{\rm cell}\sigma_c^2/V_{\rm coh}$")
    ax.set_ylabel("survival function")
    ax.set_title(r"(b) universal tails $1-F_{\chi^2_n}(x)$")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ns = np.array([4, 8, 16, 24, 36, 48, 64])
    for s2, marker in [(0.10, "o"), (0.20, "s"), (0.30, "^")]:
        ts = [crossing_T(int(n), sigma_c2=s2) for n in ns]
        ax.plot(ns, ts, marker=marker, lw=1.8,
                label=fr"$\sigma_c^2/Z={s2}$")
    ax.set_xlabel(r"$n_{\rm cell}$")
    ax.set_ylabel(r"$T_*/\omega_D$ at $p_{\rm pair}=p_c$")
    ax.set_title(r"(c) crossing vs $n_{\rm cell}$ and $\sigma_c^2$")
    ax.legend()
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.plot(T_GRID, p[16], lw=2.2, label=r"$p_{\rm pair}$, n=16")
    ax.plot(T_GRID, psync2[16], lw=1.8, label=r"$p_{\rm pair}^2$")
    ax.plot(T_GRID, psync3[16], lw=1.8, label=r"$p_{\rm pair}^3$")
    ax.axhline(P_C, color="k", ls="--", lw=1.2, label=r"$p_c$")
    ax.set_xscale("log")
    ax.set_xlabel(r"$T/\omega_D$")
    ax.set_ylabel("occupancy / sync fraction")
    ax.set_title(r"(d) $p_{\rm sync}=p_{\rm pair}^{\,t}$, n=16")
    ax.set_ylim(0, 1.05)
    ax.legend()
    ax.grid(alpha=0.3)

    fig.suptitle("Ring 15: conditional chi-square pair occupancy "
                 "(Gaussian cell-variance working assumption; not a data fit)")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(OUT_PNG, dpi=160)

    print(f"Z={Z}, omega_D={OMEGA_D}, sigma_c^2/Z={SIGMA_C2}, p_c={P_C}")
    for n in N_LIST:
        print(f"n={n:3d}  p_pair(Tmin)={p[n][0]:.12g}  "
              f"p_pair(Tmax)={p[n][-1]:.12g}  Tstar={crossing_T(n):.12g}")
    print(f"w(Tmin)={w[0]:.12g}  w(Tmax)={w[-1]:.12g}")
    for n in [4, 8, 16]:
        print(f"low-T excess slope for n={n:2d}, sigma_c2/Z=0.2: "
              f"{low_T_excess_slope(n, 0.2):.6f} (expect 2)")
    for n in [4, 16]:
        t_hi = 10.0
        x = n * SIGMA_C2 / (Z * w_debye(t_hi))
        ratio = p_pair(t_hi, n) / chi2_sf_asymp(n, x)
        print(f"high-T asymptotic ratio n={n:2d}, T=10: {ratio:.6f} (expect 1)")
    for s2 in [0.10, 0.20, 0.30]:
        print(f"sigma_c2/Z={s2:.2f}  Tstar(n=16)={crossing_T(16, sigma_c2=s2):.12g}")
    print(f"files: {OUT_CSV}, {OUT_CROSS}, {OUT_PNG}")


if __name__ == "__main__":
    main()
