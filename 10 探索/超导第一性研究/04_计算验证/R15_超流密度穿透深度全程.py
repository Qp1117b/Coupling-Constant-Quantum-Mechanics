# -*- coding: utf-8 -*-
"""
预注册判定 R15：超流密度与 London 穿透深度全程曲线（非拟合）
============================================================
链内 gap 曲线经 Johnston Eq.(42a)/(40) 唯一决定 rho_s(t), lambda(t)。
两路径一致性闭环 + 近 Tc 斜率纯数 -2 + 低温激活。

复跑：python "10 探索/超导第一性研究/04_计算验证/R15_超流密度穿透深度全程.py"
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
G = 0.5772156649015329
A = math.pi / math.exp(G)
WD = 100.0
C = math.log(2 * WD * math.exp(G) / math.pi)

# Johnston Table VI (BCS alpha=alpha_BCS): t -> I(t), Delta lambda/lambda(0)
# 从 arXiv:1304.2275 附录 Table VI 双列提取（已核对对齐）
TABLE_VI = {
    0.06: (2.3513e-12, 1.1757e-12), 0.07: (1.4543e-10, 7.2714e-11),
    0.08: (3.1803e-09, 1.5902e-09), 0.10: (2.3490e-07, 1.1745e-07),
    0.12: (4.0716e-06, 2.0358e-06), 0.16: (1.4018e-04, 7.0099e-05),
    0.20: (1.1467e-03, 5.7386e-04), 0.25: (6.0616e-03, 3.0447e-03),
    0.30: (1.8240e-02, 9.2465e-03), 0.35: (3.9972e-02, 2.0606e-02),
    0.40: (7.2078e-02, 3.8112e-02), 0.45: (1.1433e-01, 6.2587e-02),
    0.50: (1.6596e-01, 9.4982e-02), 0.54: (2.1335e-01, 1.2748e-01),
    0.60: (2.9333e-01, 1.8957e-01), 0.65: (3.6706e-01, 2.5695e-01),
    0.70: (4.4629e-01, 3.4387e-01), 0.75: (5.3023e-01, 4.5901e-01),
    0.80: (6.1822e-01, 6.1843e-01), 0.85: (7.0966e-01, 8.5587e-01),
    0.90: (8.0405e-01, 1.2591e+00), 0.95: (9.0096e-01, 2.1775e+00),
    0.99: (9.8004e-01, 6.0775e+00),
}


def gap(t):
    if t >= 1:
        return 0.0
    def eq(d):
        return quad(lambda x: math.tanh(math.sqrt(x*x+d*d)/(2*t))/math.sqrt(x*x+d*d),
                    0, WD, limit=300, epsabs=1e-12)[0] - C
    return brentq(eq, 1e-10, 20, xtol=1e-13)


def I_from_gap(t):
    """Eq.(40): I = 1/2 ∫ sech^2(z) dy"""
    d = gap(t) / A
    def integ(y):
        z = 0.5 * math.sqrt(y*y + (A*d/t)**2)
        if z > 700:
            return 0.0
        return 1.0/(math.cosh(z)**2)
    return 0.5 * quad(integ, 0, 60, limit=300, epsabs=1e-13, epsrel=1e-11)[0]


def dDelta2_dt(t, h=1e-4):
    dp = gap(min(t+h, 0.999999))/A
    dm = gap(max(t-h, 1e-9))/A
    return (dp*dp - dm*dm)/(2*h)


def Lambda_ratio(t):
    """Eq.(42a): Lambda/Lambda0 = 1 - t/(2 Delta^2) dDelta2/dt"""
    d = gap(t)/A
    return 1 - t/(2*d*d)*dDelta2_dt(t)


def main():
    # P1 I(t) 盲测
    tests = []
    for t, (Iref, dLref) in TABLE_VI.items():
        Ic = I_from_gap(t)
        err = abs(Ic-Iref)/Iref
        tests.append((t, Ic, Iref, err, dLref))
    mid = [x for x in tests if 0.2 <= x[0] <= 0.9]
    low = [x for x in tests if x[0] < 0.2]
    max_mid = max(x[3] for x in mid)
    max_low = max(x[3] for x in low)
    assert max_mid < 0.005 and max_low < 0.02, "P1: I(t) 盲测"

    # P2 两路径一致性
    path_tests = []
    for t in [0.3, 0.5, 0.7, 0.9]:
        Ic = I_from_gap(t)
        inv = 1/(1-Ic)
        Lam = Lambda_ratio(t)
        path_tests.append((t, inv, Lam, abs(inv-Lam)/inv))
    max_path = max(x[3] for x in path_tests)
    assert max_path < 0.001, "P2: 两路径一致性"

    # P3 近 Tc 斜率 rho_s/(1-t) -> 2
    slopes = []
    for t in [0.99, 0.999, 0.9999]:
        rho = 1 - I_from_gap(t)
        slopes.append((t, rho/(1-t)))
    slope_tc = slopes[-1][1]
    assert abs(slope_tc - 2.0)/2.0 < 0.01, "P3: rho_s'(1)=-2"

    # P4 低温激活指数 (扣 t^-1/2)
    ts_low = np.array([0.10, 0.12, 0.14, 0.16, 0.18, 0.20])
    dL = np.array([1/math.sqrt(1-I_from_gap(t))-1 for t in ts_low])
    ys = np.log(dL) + 0.5*np.log(ts_low)   # 扣 t^-1/2
    slope_low, _ = np.polyfit(1/ts_low, ys, 1)
    assert abs(slope_low + A)/A < 0.05, "P4: 低温激活指数 -pi/e^gamma"

    # P5 λ 盲测
    dL_tests = []
    for t, Ic, Iref, err, dLref in tests:
        if dLref and dLref < 3:
            dLc = 1/math.sqrt(1-Ic)-1
            dL_tests.append((t, dLc, dLref, abs(dLc-dLref)/dLref))
    max_dL = max(x[3] for x in dL_tests)
    assert max_dL < 0.005, "P5: lambda 盲测"

    print("R15 超流密度/穿透深度全程（A 类结构＋B 类工具）：")
    print("  P1 I(t) 盲测: 中温最大 %.2f%%, 低温最大 %.2f%%" % (100*max_mid, 100*max_low))
    print("  P2 两路径一致性最大误差 %.3f%%" % (100*max_path))
    print("  P3 rho_s/(1-t) @t=0.9999 = %.5f (目标 2)" % slope_tc)
    print("  P4 低温激活指数 %.4f (目标 -pi/e^gamma=%.4f)" % (slope_low, -A))
    print("  P5 lambda 盲测最大误差 %.2f%%" % (100*max_dL))
    print("  全部断言通过（非拟合）")

    # 曲线
    ts = np.linspace(0.06, 0.999, 120)
    Ic_curve = np.array([I_from_gap(t) for t in ts])
    rho_curve = 1 - Ic_curve
    dL_curve = 1/np.sqrt(1-Ic_curve) - 1

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, rho_curve, "k-", lw=2.2, label="链内 gap→Eq.(42a)")
    ax.scatter([x[0] for x in tests], [1-x[2] for x in tests], s=35, color="red",
               zorder=5, label="Johnston Table VI（盲测）")
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("$\\rho_s(t)/\\rho_s(0)$")
    ax.set_title("A  超流密度全程曲线"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(ts, dL_curve, "k-", lw=2.2, label="链内")
    ax.scatter([x[0] for x in dL_tests], [x[2] for x in dL_tests], s=35,
               color="red", zorder=5, label="Table VI Δλ（盲测）")
    ax.plot(ts, [math.sqrt(math.pi*A/(2*t))*math.exp(-A/t) for t in ts],
            "b:", lw=1.4, label="低温渐近 Eq.(45b)")
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("$\\Delta\\lambda/\\lambda(0)$")
    ax.set_ylim(0, 7)
    ax.set_title("B  穿透深度变化量（近 $T_c$ 发散）"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    for t, inv, Lam, e in path_tests:
        ax.plot(t, inv, "bo", ms=7)
        ax.plot(t, Lam, "rx", ms=7)
    ax.set_xlabel("$t$"); ax.set_ylabel("$\\Lambda/\\Lambda_0$")
    ax.set_title("C  两路径一致（蓝=积分，红=gap导数；差<%.2f%%）" % (100*max_path))
    ax.grid(alpha=0.3)
    ax.text(0.31, 4.7, "近 $T_c$: $\\rho_s\\to2(1-t)$，斜率 $-2$（新纯数，与 $\\kappa$ 同源）",
            fontsize=9, va="top")

    ax = axes[1, 1]
    ax.text(0.5, 0.92, "超流密度形状：链内 gap 唯一决定", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.76, "$\\tilde\\Delta(t)$（R11 C5 隙方程）", ha="center", fontsize=10)
    ax.text(0.5, 0.62, "→ $d\\tilde\\Delta^2/dt$ → $\\Lambda/\\Lambda_0$（Eq.42a）",
            ha="center", fontsize=10)
    ax.text(0.5, 0.48, "→ $\\rho_s/\\rho_s(0)=1-I$，$\\lambda/\\lambda(0)=1/\\sqrt{1-I}$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.34, "近 $T_c$ 斜率 $-2$ ∝ $d\\tilde\\Delta^2/dt|_1$\n与 $\\kappa$ 同出 $8e^{2\\gamma}/7\\zeta_3$",
            ha="center", fontsize=10, color="blue")
    ax.text(0.5, 0.16, "接 Uemura（R98）T=0 刚度 → 全程形状", ha="center", fontsize=9)
    ax.text(0.5, 0.06, "B 类工具（BCS 电动力学）；强耦合/Pippard(Al) 偏离", ha="center", fontsize=8, color="red")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  纯数来源树")

    fig.tight_layout()
    png = os.path.join(OUT, "R15_超流密度穿透深度全程.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["P1 I(t) 中温盲测", "%.2f%%" % (100*max_mid), "Table VI，<0.5%"],
        ["P1 I(t) 低温盲测", "%.2f%%" % (100*max_low), "Table VI，<2%"],
        ["P2 两路径一致性", "%.3f%%" % (100*max_path), "gap导数 vs sech²积分"],
        ["P3 近 Tc rho_s 斜率", "%.4f" % slope_tc, "目标 -2（rho_s/(1-t)→2）"],
        ["P4 低温激活指数", "%.4f" % slope_low, "目标 -pi/e^gamma=%.4f" % (-A)],
        ["P5 lambda 盲测", "%.2f%%" % (100*max_dL), "Table VI Δλ"],
        ["类别", "A 类结构＋B 类工具", "超流密度形状链内决定；电动力学工具外部"],
    ]
    with open(os.path.join(OUT, "R15_超流密度穿透深度全程_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量", "值", "说明"]); w.writerows(summary)

    with open(os.path.join(OUT, "R15_超流密度穿透深度全程_盲测.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["t", "I_chain", "I_TableVI", "rel_err", "dL_TableVI"])
        for t, Ic, Iref, err, dLref in tests:
            w.writerow(["%.4f" % t, "%.8e" % Ic, "%.8e" % Iref, "%.6f" % err,
                        ("%.6e" % dLref) if dLref else ""])

    print("图:", png)


if __name__ == "__main__":
    main()
