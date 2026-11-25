# -*- coding: utf-8 -*-
"""
预注册判定 R14：熵积分闭环（非拟合）
====================================
从链内 gap 曲线经熵积分闭合回 T=0 凝聚能纯数 R4=3/4e^{2gamma}。
Johnston Eq(20a) 熵 + Eq(31) 积分；Table III 全温区盲测。

复跑：python "10 探索/超导第一性研究/04_计算验证/R14_熵积分闭环.py"
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
ZETA3 = 1.202056903159594
A = math.pi / math.exp(G)
WD = 100.0
C = math.log(2 * WD * math.exp(G) / math.pi)
R4 = 3 / (4 * math.exp(2 * G))
HC0_NORM = math.sqrt(6 * math.pi) * math.exp(-G)

# Johnston Table III (BCS alpha=alpha_BCS) 独立数值表（webfetch 核对）
TABLE_III = {
    0.10: 1.3680e-07, 0.12: 2.4094e-06, 0.14: 1.8577e-05,
    0.16: 8.5599e-05, 0.18: 2.8013e-04, 0.20: 7.2207e-04,
    0.22: 1.5656e-03, 0.24: 2.9834e-03, 0.26: 5.1499e-03,
    0.28: 8.2286e-03, 0.30: 1.2364e-02, 0.32: 1.7678e-02,
    0.34: 2.4267e-02, 0.36: 3.2209e-02, 0.38: 4.1557e-02,
    0.40: 5.2352e-02, 0.50: 1.2852e-01, 0.60: 2.4099e-01,
    0.70: 3.8726e-01, 0.80: 5.6434e-01, 0.90: 7.6941e-01,
}


def gap(t):
    if t >= 1:
        return 0.0
    def eq(d):
        return quad(lambda x: math.tanh(math.sqrt(x*x+d*d)/(2*t))/math.sqrt(x*x+d*d),
                    0, WD, limit=300, epsabs=1e-12)[0] - C
    return brentq(eq, 1e-10, 20, xtol=1e-13)


def entropy(t):
    d = gap(t) / A
    def integ(e):
        E = math.sqrt(e*e + d*d)
        x = A * E / t
        if x > 700:
            return 0.0
        f = 1/(math.exp(x)+1)
        return f * (E + e*e/E)
    val = quad(integ, 0, 30, limit=400, epsabs=1e-13, epsrel=1e-10)[0]
    return 6*A*A/(math.pi**2*t) * val


def main():
    # P1 熵曲线盲测
    tests = []
    for t, ref in TABLE_III.items():
        s = entropy(t)
        tests.append((t, s, ref, abs(s-ref)/ref))
    max_err = max(x[3] for x in tests)
    assert max_err < 0.005, "P1: 熵曲线盲测 <0.5%"

    # P2 熵积分闭环
    integral = quad(lambda t: t - entropy(t), 1e-6, 1.0, limit=300, epsabs=1e-10)[0]
    closure_err = abs(integral - R4)/R4
    assert closure_err < 0.001, "P2: 熵积分闭合 <0.1%"

    # P3 Hc(0) 归一
    assert abs(HC0_NORM - 2.43764) < 1e-4, "P3: sqrt(6pi)e^-gamma=2.4376"

    # P4 ΔS(Tc)=0
    s_tc = entropy(0.999999)
    assert abs(s_tc - 1.0) < 1e-3, "P4: S_es(1)=1, Delta S(Tc)=0"

    # P5 低温指数趋零
    s_low = entropy(0.02)
    assert s_low < 1e-30, "P5: S_es(0.02)<1e-30"

    print("R14 熵积分闭环：")
    print("  P1 熵曲线 vs Johnston Table III 全温区盲测：")
    for t, s, ref, err in tests:
        print("    t=%.2f  chain=%.6e  III=%.6e  err=%.2f%%" % (t, s, ref, 100*err))
    print("    最大误差 %.2f%% < 0.5%%" % (100*max_err))
    print("  P2 entropy integral = %.9f vs R4 = %.9f, rel err = %.3f%%" % (integral, R4, 100*closure_err))
    print("  P3 Hc(0)/sqrt(gamma Tc^2) = %.5f" % HC0_NORM)
    print("  P4 S_es(1) = %.6f (Delta S(Tc)=0)" % s_tc)
    print("  P5 S_es(0.02) = %.3e (<1e-30)" % s_low)
    print("  全部断言通过（非拟合）")

    # 曲线
    ts = np.linspace(0.02, 0.99, 120)
    ent_curve = np.array([entropy(t) for t in ts])
    integrand = ts - ent_curve
    area = np.trapezoid(integrand, ts)

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, ent_curve, "k-", lw=2.2, label="链内 gap＋Eq.(20a)")
    ax.scatter(list(TABLE_III.keys()), list(TABLE_III.values()), s=40, color="red",
               zorder=5, label="Johnston Table III（盲测）")
    ax.plot(ts, ts, color="gray", ls=":", lw=1.2, label="正常态 $S_n/\\gamma T_c=t$")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$S_{es}/\\gamma T_c$")
    ax.set_title("A  电子熵曲线（全温区盲测）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.fill_between(ts, 0, integrand, color="tab:green", alpha=0.35)
    ax.plot(ts, integrand, "g-", lw=2.0, label="$t-S_{es}/\\gamma T_c$")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("熵差密度 $S_n-S_s$")
    ax.set_title("B  曲线下面积=凝聚能 $R_4=%.4f$（数值 %.4f）" % (R4, area))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    nodes = ["gap ratio\n$2\\pi/e^\\gamma$", "gap 曲线\n$\\tilde\\Delta(t)$",
             "比热/临界场\n$R_2,\\kappa$", "熵积分\nEq.(31)",
             "凝聚能\n$R_4=3/4e^{2\\gamma}$", "闭合\n回 $e^\\gamma$"]
    angles = np.linspace(0, 2*np.pi, len(nodes), endpoint=False)
    ax2 = fig.add_subplot(2, 2, 3, projection="polar")
    angles2 = np.linspace(0, 2*np.pi, len(nodes)+1, endpoint=False)
    ax2.plot(angles2, [1]*len(angles2), "k-", lw=1)
    for ang, nd in zip(angles, nodes):
        ax2.text(ang, 1.18, nd, ha="center", va="center", fontsize=8)
    ax2.set_ylim(0, 1.5); ax2.axis("off")
    ax2.set_title("C  热力学链闭环（T=0 出发回到 T=0）", pad=10)
    ax.axis("off")

    ax = axes[1, 1]
    tvals = [x[0] for x in tests]
    errs = [100*x[3] for x in tests]
    ax.bar([str(t) for t in tvals], errs, color="tab:blue", alpha=0.8)
    ax.axhline(0.5, color="red", ls="--", lw=1.2, label="判据 0.5%")
    ax.set_ylabel("相对误差 (%)")
    ax.set_title("D  熵盲测误差（最大 %.2f%%）＋闭合 %.3f%%" % (100*max_err, 100*closure_err))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")
    ax.tick_params(axis="x", rotation=90, labelsize=7)

    fig.tight_layout()
    png = os.path.join(OUT, "R14_熵积分闭环.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["P1 熵盲测最大误差", "%.2f%%" % (100*max_err), "Johnston Table III，21 点，<0.5%"],
        ["P2 熵积分闭合", "%.9f" % integral, "vs R4=%.9f，差 %.3f%%" % (R4, 100*closure_err)],
        ["P3 Hc(0) 归一", "%.5f" % HC0_NORM, "$\\sqrt{6\\pi}e^{-\\gamma}$"],
        ["P4 Delta S(Tc)", "%.6f" % (s_tc-1), "无潜热（二级相变）"],
        ["P5 S_es(0.02)", "%.3e" % s_low, "低温指数趋零"],
        ["类别", "A 类闭合＋B 类工具", "熵积分工具外部；gap/alpha/R4 链内"],
    ]
    with open(os.path.join(OUT, "R14_熵积分闭环_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    with open(os.path.join(OUT, "R14_熵积分闭环_盲测.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["t", "chain_S", "TableIII", "rel_err"])
        for t, s, ref, err in tests:
            w.writerow(["%.4f" % t, "%.8e" % s, "%.8e" % ref, "%.6f" % err])

    print("图:", png)


if __name__ == "__main__":
    main()
