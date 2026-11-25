# -*- coding: utf-8 -*-
"""
预注册判定 R11：从链内 C5 隙方程推完整普适 gap 曲线（非拟合）
==================================================================
核心：近-Tc 斜率 sqrt(f1) = pi*sqrt(8/(7 zeta3)) = pi*sqrt((2/3)*DeltaC/gamma Tc)
      ——完全由链内 gap ratio (e^gamma) + 比热跳变 (12/7 zeta3) 导出。
数值：稳定分解解 C5 隙方程，omega_D/Tc=100，k_B Tc=1。

复跑：python "10 探索/超导第一性研究/04_计算验证/R11_普适gap温度曲线.py"
"""
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
GAMMA_E = 0.5772156649015329
ZETA3 = 1.202056903159594
F0 = math.pi / math.exp(GAMMA_E)                  # 1.7639 = pi/e^gamma
SQRT_F1 = math.pi * math.sqrt(8 / (7 * ZETA3))   # 3.06326 链内纯数
DELTA_C = 12 / (7 * ZETA3)                        # 1.42613 比热跳变
WD = 100.0                                        # omega_D / k_B T_c
COUPLING = math.log(2 * WD * math.exp(GAMMA_E) / math.pi)


def solve_gap(t):
    """稳定分解解 C5 隙方程；返回 Delta/k_B T_c。"""
    if t >= 1.0:
        return 0.0

    def eq(delta):
        def integrand(x):
            E = math.sqrt(x * x + delta * delta)
            return math.tanh(E / (2 * t)) / E
        val = quad(integrand, 0, WD, limit=300, epsabs=1e-12, epsrel=1e-12)[0]
        return val - COUPLING

    return brentq(eq, 1e-10, 20.0, xtol=1e-13, rtol=1e-14)


def main():
    # ---------- P1 零温截距 ----------
    f0_num = solve_gap(0.01)
    p1_err = abs(f0_num - F0) / F0
    assert p1_err < 0.001, "P1: f(0)=pi/e^gamma"

    # ---------- P2 近-Tc 斜率 ----------
    t_slope = 0.9999
    slope_num = solve_gap(t_slope) / math.sqrt(1 - t_slope)
    p2_err = abs(slope_num - SQRT_F1) / SQRT_F1
    assert p2_err < 0.001, "P2: 近-Tc 斜率=pi sqrt(8/(7 zeta3))"

    # ---------- P3 Gross 系数 a=2/3 ----------
    lhs = 8 / (7 * ZETA3)
    rhs = (2 / 3) * DELTA_C
    assert abs(lhs - rhs) < 1e-12, "P3: a=2/3 代数恒等式"

    # ---------- P4 全程单调 ----------
    ts = np.linspace(0.02, 0.999, 120)
    fs = np.array([solve_gap(t) for t in ts])
    mono = bool(np.all(np.diff(fs) <= 1e-9))
    assert mono and fs[-1] < 0.15, "P4: 单调递减且趋于 0"

    # ---------- P5 Al 实验 ----------
    al_exp, al_err = 3.53, 0.02
    p5_ok = (al_exp - al_err) <= 2 * F0 <= (al_exp + al_err)
    assert p5_ok, "P5: 2f(0)=3.528 落入 Al 3.53+/-0.02"

    # ---------- 曲线与渐近线 ----------
    ratios = fs / f0_num
    # 渐近线只在各自有效区间画（避免无效区间的误导外推）
    asym_low = np.array([1 - math.sqrt(2 * math.pi * t / F0) * math.exp(-F0 / t)
                         if t <= 0.3 else np.nan for t in ts])
    asym_high = np.array([SQRT_F1 / F0 * math.sqrt(1 - t)
                          if t >= 0.7 else np.nan for t in ts])
    interp_tanh = np.array([math.tanh(1.74 * math.sqrt(1 / t - 1)) for t in ts])

    # 斜率收敛序列（P2 面板）
    ts_conv = np.linspace(0.9, 0.9999, 60)
    slopes = np.array([solve_gap(t) / math.sqrt(1 - t) for t in ts_conv])

    print("R11 普适 gap 温度曲线（A 类，链内 C5 隙方程）：")
    print(f"  F0 = pi/e^gamma = {F0:.6f}；数值 f(0) = {f0_num:.6f}，误差 {p1_err:.3%}")
    print(f"  sqrt(f1) = pi sqrt(8/(7 zeta3)) = {SQRT_F1:.6f}；数值斜率(t={t_slope}) = {slope_num:.6f}，误差 {p2_err:.3%}")
    print(f"  Gross a=2/3: 8/(7 zeta3)={lhs:.9f} = (2/3)*DeltaC={rhs:.9f}")
    print(f"  单调={mono}, f(t=0.999)={solve_gap(0.999):.5f}；2f(0)={2*F0:.4f} 落入 Al [{al_exp-al_err},{al_exp+al_err}]")
    print("  全部断言通过（非拟合）")

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, ratios, "k-", lw=2.2, label="C5 隙方程数值解（链内）")
    ax.plot(ts, asym_low, "b:", lw=1.4, label="低温激活渐近 $t\\lesssim0.3$")
    ax.plot(ts, asym_high, "r--", lw=1.4, label="近 $T_c$ 渐近 $\\sqrt{f_1}\\sqrt{1-t}$")
    ax.plot(ts, interp_tanh, color="gray", ls="-.", lw=1.2, label="$\\tanh(1.74\\sqrt{1/t-1})$ 插值")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$\\Delta(T)/\\Delta_0$")
    ax.set_title("A  链内 C5 普适 gap 曲线（无参数）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(ts_conv, slopes, "k-", lw=2.0, label="数值斜率 $f/\\sqrt{1-t}$")
    ax.axhline(SQRT_F1, color="red", ls="--", lw=1.5,
               label="链内纯数 $\\pi\\sqrt{8/7\\zeta_3}=%.4f$" % SQRT_F1)
    ax.set_xlabel("$t$")
    ax.set_ylabel("$f(t)/\\sqrt{1-t}$")
    ax.set_title("B  近 $T_c$ 斜率收敛（误差 %.3f%%）" % (100 * p2_err))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.text(0.5, 0.93, "链内两个纯数 → 普适曲线斜率", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.74, "gap ratio: $2\\Delta_0/k_BT_c=2\\pi/e^\\gamma$  $\\Rightarrow$  $e^\\gamma$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.58, "比热跳变: $\\Delta C/\\gamma T_c=12/7\\zeta_3$  $\\Rightarrow$  $\\zeta_3$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.42, "$\\sqrt{f_1}=\\pi\\sqrt{8/7\\zeta_3}=\\pi\\sqrt{\\frac{2}{3}\\frac{\\Delta C}{\\gamma T_c}}$",
            ha="center", fontsize=11, color="blue")
    ax.text(0.5, 0.24, "Gross(1980) $a=2/3$ 由链内纯数推出，非拟合参数",
            ha="center", fontsize=9)
    ax.text(0.5, 0.09, "数值验证: %.5f vs %.5f (差 %.3f%%)" % (slope_num, SQRT_F1, 100 * p2_err),
            ha="center", fontsize=9, color="green")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("C  纯数关系树（$a=2/3$ 的来源）")

    ax = axes[1, 1]
    els = ["Al (Blackford-March 1968)"]
    chain_val = 2 * F0
    ax.errorbar([0], [al_exp], yerr=[al_err], fmt="o", color="tab:orange", ms=9,
                capsize=6, label="Al 实验 $3.53\\pm0.02$（21 结）")
    ax.plot([-0.3, 0.3], [chain_val, chain_val], "b--", lw=1.6,
            label="链内 $2f(0)=2\\pi/e^\\gamma=%.4f$" % chain_val)
    ax.text(0.12, 3.50, "Townsend–Sutton(1962)\nSn/Ta/Nb 曲线略高于\nBCS（图数据，不伪造点）",
            fontsize=8, va="center")
    ax.set_xlim(-0.35, 0.55)
    ax.set_ylim(3.4, 3.68)
    ax.set_ylabel("$2\\Delta_0/k_BT_c$")
    ax.set_title("D  零温截距 vs 精密隧穿实验")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R11_普适gap温度曲线.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["F0=pi/e^gamma", "%.6f" % F0, "C5 gap ratio 一半"],
        ["数值 f(0)", "%.6f" % f0_num, "P1 误差 %.3f%%" % (100 * p1_err)],
        ["sqrt(f1) 链内纯数", "%.6f" % SQRT_F1, "$\\pi\\sqrt{8/7\\zeta_3}$（gap ratio＋比热跳变）"],
        ["数值近-Tc 斜率", "%.6f" % slope_num, "P2 误差 %.3f%%" % (100 * p2_err)],
        ["Gross a", "2/3", "$8/(7\\zeta_3)=(2/3)\\cdot12/(7\\zeta_3)$ 精确"],
        ["Langmann-Triola 2023", "~3.0633", "独立精确 BCS 普适函数对照"],
        ["单调 f(1)=0", "PASS", "P4"],
        ["Al 实验覆盖", "PASS", "$2f(0)=%.4f\\in[3.51,3.55]$" % chain_val],
        ["类别", "A 类（条件具备）", "C5 隙方程；弱耦合 s 波单带；绝对 Tc 外生"],
    ]
    with open(os.path.join(OUT, "R11_普适gap温度曲线_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    # 曲线数据 CSV
    with open(os.path.join(OUT, "R11_普适gap温度曲线_数据.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["t", "Delta/Delta0", "asym_low", "asym_high", "tanh_interp"])
        for row in zip(ts, ratios, asym_low, asym_high, interp_tanh):
            w.writerow(["%.6f" % v for v in row])

    print("图:", png)


if __name__ == "__main__":
    main()
