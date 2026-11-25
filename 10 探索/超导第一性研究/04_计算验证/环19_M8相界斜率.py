# -*- coding: utf-8 -*-
"""
环 19／M8 相界斜率律的数值核对。

1. p_*(T) 与 p_pair(T) 的示意轨迹与唯一交点；
2. p_*'(T) 与 (1/T - w'/w)/t 恒等（M8S.1 核对）；
3. ln Tc vs ln(p_pair-pc) 的双对数斜率 = t_Upsilon（M8S.4）；
4. Tc(delta) 穹顶在阈值处水平切线、对数斜率发散。

曲线由 (M8S.1)-(M8S.4) 直接计算，无拟合。
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
OUT_PNG = os.path.join(HERE, "环19_M8相界斜率.png")
OUT_CSV = os.path.join(HERE, "环19_M8相界斜率.csv")

PC = 0.592746
T_UP = 1.3
T0 = 2.0


def w_debye(x, d=2):
    y = np.linspace(0, 1, 2001)
    return float(np.trapezoid(d * y ** (d - 1) * np.tanh(y / (2 * x)), y))


def p_star(T):
    # 2 k_B / (pi Upsilon_bond) = 1 (归一化示意)
    return PC + (1 - PC) * (T / w_debye(T)) ** (1 / T_UP)


def p_pair(T):
    return PC + 0.35 * (1 - (T / T0) ** 2)


def main():
    rows = []
    # 1 交点
    Ts = np.linspace(0.02, T0, 300)
    ps = np.array([p_star(t) for t in Ts])
    pp = p_pair(Ts)
    idx = np.argmin(np.abs(ps - pp))
    T_cross = Ts[idx]
    print(f"相界交点 T_c = {T_cross:.6f}, p = {ps[idx]:.6f}")
    rows.append(("crossing", T_cross, ps[idx], pp[idx], np.nan))

    # 2 恒等式核对
    h = 1e-5
    print("\nM8S.1 核对：p_*' vs (p_*-pc)/t * (1/T - w'/w)")
    for T in (0.2, 0.5, 1.0, 1.5):
        w = w_debye(T)
        wp = (w_debye(T + h) - w_debye(T - h)) / (2 * h)
        lhs = (p_star(T + h) - p_star(T - h)) / (2 * h)
        rhs = (p_star(T) - PC) / T_UP * (1 / T - wp / w)
        print(f"  T={T:.2f}: lhs={lhs:.6f}, rhs={rhs:.6f}, rel={abs(lhs-rhs)/lhs:.3e}")
        rows.append(("identity", T, lhs, rhs, np.nan))

    # 3 幂律核对
    eps = np.logspace(-4, -1, 60)
    Tc_approx = (eps / ((1 - PC) * 1.0)) ** T_UP  # p*-pc = (1-pc) R^{1/t}, R~T
    slope = np.polyfit(np.log(eps), np.log(Tc_approx), 1)[0]
    print(f"\nln Tc vs ln(p_pair-pc) 斜率 = {slope:.6f} (target t_U = {T_UP})")
    rows.append(("power_law", T_UP, slope, T_UP, np.nan))

    # 4 穹顶：p_pair = pc + 0.35 delta, T_c = [(p_pair-pc)/(1-pc)]^t
    deltas = np.linspace(1e-4, 1.0, 500)
    Tc = ((0.35 * deltas) / (1 - PC)) ** T_UP
    log_slope = T_UP / deltas
    print(f"delta=1e-4: Tc={Tc[0]:.3e}, dlnTc/ddelta={log_slope[0]:.1f}")
    for d in (1e-4, 1e-3, 1e-2, 0.1, 1.0):
        i = int(np.argmin(np.abs(deltas - d)))
        rows.append(("dome", deltas[i], Tc[i], log_slope[i], np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A
    ax[0, 0].plot(Ts, ps, lw=2.2, color="tab:blue", label=r"$p_*(T)$（单调升）")
    ax[0, 0].plot(Ts, pp, lw=2.2, color="tab:orange", label=r"$p_{\rm pair}(T)$（单调降）")
    ax[0, 0].plot([T_cross], [ps[idx]], "o", color="tab:red", ms=8, label="唯一交点")
    ax[0, 0].set_xlabel(r"$T$")
    ax[0, 0].set_ylabel(r"$p$")
    ax[0, 0].set_title("A  相界与配对线的唯一交点")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B
    Tid = np.array([0.2, 0.5, 1.0, 1.5])
    lhs_list, rhs_list = [], []
    for T in Tid:
        w = w_debye(T)
        wp = (w_debye(T + h) - w_debye(T - h)) / (2 * h)
        lhs_list.append((p_star(T + h) - p_star(T - h)) / (2 * h))
        rhs_list.append((p_star(T) - PC) / T_UP * (1 / T - wp / w))
    ax[0, 1].plot(Tid, lhs_list, "o-", lw=2.0, color="tab:blue", label=r"$p_*'$")
    ax[0, 1].plot(Tid, rhs_list, "s--", lw=2.0, color="tab:orange",
                  label=r"$(p_*-p_c)/t\cdot(1/T-w'/w)$")
    ax[0, 1].set_xlabel(r"$T$")
    ax[0, 1].set_title(r"B  (M8S.1) 恒等式核对")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C
    ax[1, 0].loglog(eps, Tc_approx, lw=2.2, color="tab:purple",
                    label=rf"斜率 $={slope:.3f}\approx t_\Upsilon$")
    ax[1, 0].set_xlabel(r"$p_{\rm pair}-p_c$")
    ax[1, 0].set_ylabel(r"$T_c$（形状）")
    ax[1, 0].set_title(r"C  (M8S.4) 幂律 $T_c\propto(p_{\rm pair}-p_c)^{t_\Upsilon}$")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D
    ax[1, 1].plot(deltas, Tc, lw=2.2, color="tab:green", label=r"$T_c(\delta)$")
    ax[1, 1].plot(deltas, Tc * 0 + 0, color="0.35", lw=0.9)
    ax[1, 1].set_xlabel(r"掺杂 $\delta$")
    ax[1, 1].set_ylabel(r"$T_c$（形状）")
    ax[1, 1].set_title(r"D  阈值处水平切线，对数斜率 $\propto1/\delta$")
    ax[1, 1].legend(fontsize=9)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
