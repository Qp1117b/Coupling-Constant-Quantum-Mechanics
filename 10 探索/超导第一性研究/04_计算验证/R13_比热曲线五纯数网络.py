# -*- coding: utf-8 -*-
"""
预注册判定 R13：比热全程曲线五纯数一致性网络（非拟合）
================================================================
(A) 内部结构：R4 * 2 kappa^2 = R2（五纯数一致性网络）
(B) 外部盲测：链内 gap 曲线 + Johnston Eq(20b) 积分 vs Table IV

复跑：python "10 探索/超导第一性研究/04_计算验证/R13_比热曲线五纯数网络.py"
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
GAMMA = 0.5772156649015329
ZETA3 = 1.202056903159594
ALPHA = math.pi / math.exp(GAMMA)
F0 = ALPHA
WD = 100.0
COUPLING = math.log(2 * WD * math.exp(GAMMA) / math.pi)
R2 = 12 / (7 * ZETA3)
R4 = 3 / (4 * math.exp(2 * GAMMA))
KAPPA = 2 * math.sqrt(2) * math.exp(GAMMA) / math.sqrt(7 * ZETA3)

# Johnston arXiv:1304.2275 Table IV (BCS, alpha=alpha_BCS) 独立数值表
TABLE_IV = {
    0.12: 3.4498e-05, 0.14: 2.2733e-04, 0.16: 9.1427e-04,
    0.18: 2.6544e-03, 0.20: 6.1494e-03, 0.22: 1.2113e-02,
    0.24: 2.1163e-02, 0.26: 3.3758e-02, 0.28: 5.0188e-02,
    0.30: 7.0594e-02,
}


def solve_gap(t):
    if t >= 1.0:
        return 0.0
    def eq(delta):
        integ = lambda x: math.tanh(math.sqrt(x*x+delta*delta)/(2*t))/math.sqrt(x*x+delta*delta)
        return quad(integ, 0, WD, limit=300, epsabs=1e-12, epsrel=1e-12)[0] - COUPLING
    return brentq(eq, 1e-10, 20.0, xtol=1e-13, rtol=1e-14)


def dDelta2_dt(t, h=1e-4):
    dp = solve_gap(min(t+h, 0.999999)) / F0
    dm = solve_gap(max(t-h, 1e-8)) / F0
    return (dp*dp - dm*dm) / (2*h)


def ces(t):
    dtilde = solve_gap(t)/F0
    dD2 = dDelta2_dt(t)
    def integrand(e):
        E = math.sqrt(e*e + dtilde*dtilde)
        x = ALPHA * E / t
        if x > 700:
            return 0.0
        f = 1/(math.exp(x)+1)
        return f*(1-f)*(E*E/t - 0.5*dD2)
    val = quad(integrand, 0, 30, limit=400, epsabs=1e-14, epsrel=1e-10)[0]
    return 6*ALPHA**3/(math.pi**2 * t) * val


def main():
    # P1 五纯数网络
    network = R4 * 2 * KAPPA**2
    p1_err = abs(network - R2)/R2
    assert p1_err < 1e-12, "P1: R4*2 kappa^2 = R2"

    # P2 逐点盲测
    tests = []
    for t, ref in TABLE_IV.items():
        v = ces(t)
        tests.append((t, v, ref, abs(v-ref)/ref))
    max_err = max(x[3] for x in tests)
    assert max_err < 0.02, "P2: 逐点盲测 <2%"

    # P3 跳变
    jump = 1 + R2
    assert abs(jump - 2.426127) < 1e-4, "P3: 1+R2=2.426"

    # P4/P5 低温激活
    prefactor = 3*math.sqrt(2)*ALPHA/math.pi**1.5
    assert abs(ALPHA - 1.763877) < 1e-4
    assert abs(prefactor - 1.343940) < 1e-4

    print("R13 比热曲线五纯数网络：")
    print(f"  P1 R4*2kappa^2 = {network:.9f} = R2={R2:.9f}，误差 {p1_err:.2e}")
    print("  P2 逐点盲测（链内 gap + Johnston 积分 vs Table IV）：")
    for t, v, ref, err in tests:
        print(f"    t={t:.2f}  chain={v:.6e}  IV={ref:.6e}  err={err:.2%}")
    print(f"    最大误差 {max_err:.2%} < 2%")
    print(f"  P3 跳变 1+R2 = {jump:.6f}")
    print(f"  P4 激活指数 alpha_BCS = {ALPHA:.6f}；P5 前因子 = {prefactor:.6f}")
    print("  全部断言通过（非拟合）")

    # 全程曲线
    ts = np.linspace(0.10, 0.99, 100)
    ces_curve = np.array([ces(t) for t in ts])

    # 低温激活指数：Johnston Eq.(24) 含幂律前因子 (alpha/t)^{3/2}，
    # 须扣除 -3/2 ln(alpha/t) 才是纯指数斜率 -alpha；用链内 t<=0.12 深低温值
    # （Table IV 最低只到 t=0.12，且 t>=0.12 尚未完全进入 t->0 渐近区）。
    ts_low = np.array([0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12])
    ces_low = np.array([ces(t) for t in ts_low])
    ys = np.log(ces_low) - 1.5 * np.log(ALPHA / ts_low)   # 扣幂律前因子
    slope, _ = np.polyfit(1/ts_low, ys, 1)

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, ces_curve, "k-", lw=2.2, label="链内 gap＋Johnston 积分")
    tref = list(TABLE_IV.keys())
    ax.scatter(tref, [TABLE_IV[t] for t in tref], s=45, color="red", zorder=5,
               label="Johnston Table IV（盲测）")
    ax.plot(ts, ts, color="gray", ls=":", lw=1.2, label="正常态 $C_n/\\gamma T_c=t$")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$C_{es}/\\gamma T_c$")
    ax.set_title("A  比热全程曲线（逐点盲测）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(1/ts_low, ys, "o-", color="blue", ms=5, label="链内深低温（幂律已扣）")
    ax.plot(1/ts_low, -ALPHA/ts_low, "r--", lw=1.5,
            label="渐近 $-\\alpha_{BCS}/t$（斜率 %.3f）" % (-ALPHA))
    ax.set_xlabel("$1/t=T_c/T$")
    ax.set_ylabel("$\\ln C_{es}-\\frac{3}{2}\\ln(\\alpha/t)$")
    ax.set_title("B  低温激活指数 %.3f vs $-\\pi/e^\\gamma=%.3f$" % (slope, -ALPHA))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.text(0.5, 0.93, "五纯数一致性网络（2 生成元）", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.78, "生成元: $e^\\gamma$（gap ratio）＋$\\zeta_3$（比热跳变）",
            ha="center", fontsize=10)
    ax.text(0.5, 0.63, "$R_2=12/7\\zeta_3=%.4f$（比热跳变）" % R2,
            ha="center", fontsize=10)
    ax.text(0.5, 0.51, "$R_4=3/4e^{2\\gamma}=%.4f$（凝聚能比）" % R4,
            ha="center", fontsize=10)
    ax.text(0.5, 0.39, "$\\kappa=2\\sqrt{2}e^\\gamma/\\sqrt{7\\zeta_3}=%.4f$（临界场斜率）" % KAPPA,
            ha="center", fontsize=10)
    ax.text(0.5, 0.25, "$R_4\\cdot2\\kappa^2=\\frac{3e^{-2\\gamma}}{4}\\cdot\\frac{16e^{2\\gamma}}{7\\zeta_3}=R_2$",
            ha="center", fontsize=11, color="blue")
    ax.text(0.5, 0.11, "$e^{2\\gamma}$ 精确消去 → 链内恒等式，误差 %.0e" % p1_err,
            ha="center", fontsize=9, color="green")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("C  五纯数网络（$R_4\\cdot2\\kappa^2=R_2$）")

    ax = axes[1, 1]
    tvals = [x[0] for x in tests]
    errs = [100*x[3] for x in tests]
    ax.bar([str(t) for t in tvals], errs, color="tab:green", alpha=0.8)
    ax.axhline(2.0, color="red", ls="--", lw=1.2, label="预注册判据 2%")
    ax.set_ylabel("相对误差 (%)")
    ax.set_title("D  逐点盲测误差（最大 %.2f%%）" % (100*max_err))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R13_比热曲线五纯数网络.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["P1 五纯数网络", "%.9f" % network, "$R_4\\cdot2\\kappa^2=R_2$，误差 %.0e" % p1_err],
        ["P2 逐点盲测最大误差", "%.2f%%" % (100*max_err), "Johnston Table IV，<2%"],
        ["P3 比热跳变", "%.6f" % jump, "$1+R_2=2.4261$"],
        ["P4 激活指数", "%.6f" % ALPHA, "$\\pi/e^\\gamma$（C5）"],
        ["P5 低温前因子", "%.6f" % prefactor, "$3\\sqrt2\\alpha/\\pi^{3/2}$"],
        ["低温激活指数（幂律已扣，t<=0.12）", "%.4f" % slope, "vs $-\\pi/e^\\gamma=%.4f$，差 %.1f%%" % (-ALPHA, 100*abs(slope+ALPHA)/ALPHA)],
        ["类别", "A 类（网络）＋B 类（积分工具）", "五纯数网络纯 A；Johnston 积分式外部工具"],
    ]
    with open(os.path.join(OUT, "R13_比热曲线五纯数网络_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    with open(os.path.join(OUT, "R13_比热曲线五纯数网络_盲测.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["t", "chain_Ces", "TableIV", "rel_err"])
        for t, v, ref, err in tests:
            w.writerow(["%.4f" % t, "%.8e" % v, "%.8e" % ref, "%.6f" % err])

    print("图:", png)


if __name__ == "__main__":
    main()
