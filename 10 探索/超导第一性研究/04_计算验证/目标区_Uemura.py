# -*- coding: utf-8 -*-
"""
目标区：从 BKT 普适跳变 + 渗流刚度推导 Uemura 标度，并核对失效条件。

归一化：k_B = 1, hbar = 1, omega_D = 1, Z = 1, Upsilon_bond = U0 (扫描).
只做解析形状、不等式与交点核对；不拟合任何实验数据。

外部输入（只作对照，不写成 CQM 已证）：
  Uemura et al., PRL 62, 2317 (1989); arXiv:cond-mat/0212643
  Homes et al., Nature 430, 539 (2004), DOI 10.1038/nature02673
  Imry, Strongin & Homes, PRL 109, 067003 (2012)
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "目标区_Uemura.png")
OUT_CSV = os.path.join(HERE, "目标区_Uemura.csv")
OUT_SUM = os.path.join(HERE, "目标区_Uemura_摘要.csv")

# 复用环 19 的 Debye 权重与渗流读出，保证口径一致
import importlib.util
SPEC = importlib.util.spec_from_file_location("ring19", os.path.join(HERE, "环19_相位刚度.py"))
R19 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(R19)

w_debye = R19.w_debye
phi = R19.Phi_power
PC = R19.PC_SITE

N_CELL = 4          # chi-square 自由度（偶数，取精确有限和）
SIGMA_C2 = 0.20     # sigma_c^2 / Z
C_CORE = 2.0        # 涡旋核心能形状参数 y0 = exp(-c K0)


# ---------------------------------------------------------------- p_pair (环 15)


def p_pair(T):
    """环 15 的条件 chi-square 尾，n_cell = 4: e^{-x/2}(1 + x/2)."""
    if T <= 0.0:
        x = N_CELL * SIGMA_C2 / 1.0   # w(0) = 1
    else:
        x = N_CELL * SIGMA_C2 / w_debye(T)
    if x > 700.0:
        return 0.0
    return math.exp(-x / 2.0) * (1.0 + x / 2.0)


def u_bare(T, U0):
    """环 19 (19P.20) 的裸刚度读出。"""
    return U0 * w_debye(T) * phi(p_pair(T))


# ---------------------------------------------------------------- Kosterlitz RG


def rg_light(K0, c=C_CORE, n=4000, lmax=10.0):
    """轻量 RK4：返回 (超流?, K_R/K0)。
    系数 4 pi^2 取 Nelson 约定；只依赖不动点 2/pi 与流向。"""
    if K0 <= 0.0:
        return False, 0.0
    y0 = math.exp(-c * K0)
    if y0 <= 1e-300:
        return True, 1.0
    u = 1.0 / K0
    y = y0
    dl = lmax / n
    for _ in range(n):
        def deriv(uu, yy):
            return 4.0 * math.pi ** 2 * yy * yy, (2.0 - math.pi / uu) * yy
        k1 = deriv(u, y)
        k2 = deriv(u + 0.5 * dl * k1[0], y + 0.5 * dl * k1[1])
        k3 = deriv(u + 0.5 * dl * k2[0], y + 0.5 * dl * k2[1])
        k4 = deriv(u + dl * k3[0], y + dl * k3[1])
        u += dl * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6.0
        y += dl * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6.0
        if y > 10.0:
            return False, 0.0
    KR = 1.0 / u
    return y < y0, min(1.0, KR / K0)


def superfluid(K0):
    return rg_light(K0)[0]


def renorm_factor(K0):
    return rg_light(K0)[1]


def Tc_of_U0(U0):
    """自洽解 K_R(T_c) = 2/pi，其中 K0(T) = U_bare(T)/T."""
    lo, hi = 1e-6, 50.0
    for _ in range(36):
        T = 0.5 * (lo + hi)
        K0 = u_bare(T, U0) / T
        if superfluid(K0):
            lo = T
        else:
            hi = T
    return 0.5 * (lo + hi)


# ---------------------------------------------------------------- main


def main():
    rows = []
    U0_list = np.concatenate([
        np.linspace(0.05, 1.0, 16),
        np.linspace(1.1, 4.0, 10),
    ])

    results = []
    for U0 in U0_list:
        Tc = Tc_of_U0(float(U0))
        Uzero = u_bare(0.0, float(U0))
        K0 = u_bare(Tc, float(U0)) / Tc
        # 在自洽 Tc 上，普适跳变给 K_R(Tc)=2/pi；故 g = K_R/K0 = (2/pi)/K0，
        # 这是恒等式，不需要从 RG 流的有限尺度终值抽取（后者在分离点附近收敛很慢）。
        g = min(1.0, (2.0 / math.pi) / K0)
        r = w_debye(Tc) * phi(p_pair(Tc)) / phi(p_pair(0.0))
        Q = r * g
        Tlin = math.pi * Uzero / 2.0
        results.append((U0, Uzero, Tc, Tlin, r, g, Q))
        rows.append(("scan", U0, Uzero, Tc, Tlin, r, g, Q))

    # 数值核对：线性段斜率、Q 的上界、单调性
    small = [x for x in results if x[0] <= 0.4]
    slopes = [x[2] / x[1] for x in small]
    dTc = [results[i + 1][2] - results[i][2] for i in range(len(results) - 1)]
    dU = [results[i + 1][1] - results[i][1] for i in range(len(results) - 1)]
    secant = [a / b for a, b in zip(dTc, dU)]

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "U0", "U_bare0", "Tc", "T_linear", "r", "g_ren", "Q"])
        wr.writerows(rows)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["quantity", "value", "note"])
        wr.writerow(["p_pair(0)", p_pair(0.0), "chi-square n=4, sigma_c2=0.2"])
        wr.writerow(["Phi(p_pair(0))", phi(p_pair(0.0)), "pc=site 0.592746, t_U=1.3"])
        wr.writerow(["slope_small_min", min(slopes), "min Tc/U_bare(0) for U0<=0.4"])
        wr.writerow(["slope_small_max", max(slopes), "max Tc/U_bare(0) for U0<=0.4"])
        wr.writerow(["pi_over_2", math.pi / 2.0, "ideal Uemura slope (kB=1)"])
        wr.writerow(["Q_max", max(x[6] for x in results), "must be <= 1"])
        wr.writerow(["Q_min", min(x[6] for x in results), "must be > 0"])
        wr.writerow(["monotone_Tc", all(a > 0 for a in dTc), "all dTc > 0"])
        wr.writerow(["concave_after_linear", all(secant[i + 1] < secant[i] for i in range(len(secant) - 1)),
                     "secant slope decreasing"])
        wr.writerow(["Tc_le_linear", all(x[2] <= x[3] + 1e-9 for x in results), "(U.3) check"])

    # ---------------------------------------------------------------- figure
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))
    Uzero = np.array([x[1] for x in results])
    Tc = np.array([x[2] for x in results])
    Q = np.array([x[6] for x in results])
    rr = np.array([x[4] for x in results])
    gg = np.array([x[5] for x in results])
    ws = np.array([w_debye(x[2]) for x in results])
    phir = np.array([phi(p_pair(x[2])) / phi(p_pair(0.0)) for x in results])

    ax[0, 0].plot(Uzero, Tc, "o-", lw=1.8, ms=4, label=r"CQM  $T_c$")
    ax[0, 0].plot(Uzero, np.pi * Uzero / 2.0, "--", lw=1.6,
                  label=r"Uemura 线 $\pi\Upsilon_{\rm bare}(0)/2$")
    ax[0, 0].set_xlabel(r"$\Upsilon_{\rm bare}(0)$")
    ax[0, 0].set_ylabel(r"$T_c$")
    ax[0, 0].set_title("A  Uemura 线性段与大 $\\Upsilon_0$ 向下偏离")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(Uzero, Q, "o-", lw=1.8, ms=4, color="tab:red")
    ax[0, 1].axhline(1.0, color="k", ls=":", lw=1.0)
    ax[0, 1].set_xlabel(r"$\Upsilon_{\rm bare}(0)$")
    ax[0, 1].set_ylabel(r"$Q=r\,g_{\rm ren}$")
    ax[0, 1].set_title("B  损耗因子 $Q\\leq1$；$Q\\to1$ 给 Uemura 线")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(Uzero, ws, lw=1.6, label=r"$w(T_c)$")
    ax[1, 0].plot(Uzero, phir, lw=1.6, label=r"$\Phi(p_{\rm pair}(T_c))/\Phi(p_{\rm pair}(0))$")
    ax[1, 0].plot(Uzero, gg, lw=1.6, label=r"$g_{\rm ren}(T_c)$")
    ax[1, 0].plot(Uzero, Q, lw=2.0, ls="--", label=r"$Q$")
    ax[1, 0].set_xlabel(r"$\Upsilon_{\rm bare}(0)$")
    ax[1, 0].set_ylabel("因子")
    ax[1, 0].set_ylim(0.0, 1.05)
    ax[1, 0].set_title("C  三个损耗通道：$w$、$\\Phi$ 比、$g_{\\rm ren}$")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(Uzero[1:], secant, "s-", lw=1.8, ms=4)
    ax[1, 1].axhline(math.pi / 2.0, color="k", ls="--", lw=1.0,
                     label=r"$\pi/2$")
    ax[1, 1].set_xlabel(r"$\Upsilon_{\rm bare}(0)$")
    ax[1, 1].set_ylabel(r"$dT_c/d\Upsilon_{\rm bare}(0)$")
    ax[1, 1].set_title("D  斜率下降 $\\Rightarrow$ Uemura 只在小 $\\Upsilon_0$ 成立")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    # ---------------------------------------------------------------- printed checks
    print(f"p_pair(0) = {p_pair(0.0):.6f}, Phi(p_pair(0)) = {phi(p_pair(0.0)):.6f}")
    print(f"ideal slope pi/2 = {math.pi/2:.6f}")
    print("small-U0 slopes Tc/U_bare(0): " +
          ", ".join(f"{s:.6f}" for s in slopes[:8]))
    print(f"Q range: [{min(x[6] for x in results):.6f}, {max(x[6] for x in results):.6f}]")
    print("sample (U0, U_bare0, Tc, T_linear, r, g, Q):")
    for idx in [0, 5, 10, 15, 20, 25]:
        if idx < len(results):
            x = results[idx]
            print("  " + ", ".join(f"{v:.6f}" for v in x))
    print(f"all dTc > 0: {all(a > 0 for a in dTc)}")
    print(f"all Tc <= pi*U_bare(0)/2: {all(x[2] <= x[3] + 1e-9 for x in results)}")
    print(f"secant slopes decreasing: {all(secant[i+1] < secant[i] for i in range(len(secant)-1))}")


if __name__ == "__main__":
    main()
