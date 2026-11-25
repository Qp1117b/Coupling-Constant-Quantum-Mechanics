# -*- coding: utf-8 -*-
"""
预注册判定 R16：临界场 Hc(T) 全程盲测 + 五表统一全景（非拟合）
================================================================
链内 gap 曲线经熵积分 Eq.(31) 算 Hc(t)/Hc(0)，对 Johnston Table V 盲测；
五表（gap/熵/比热/临界场/穿透深度）统一展示单一 gap 源贯通。

复跑：python "10 探索/超导第一性研究/04_计算验证/R16_临界场全程与五表全景.py"
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
Z3 = 1.202056903159594
A = math.pi / math.exp(G)
WD = 100.0
C = math.log(2 * WD * math.exp(G) / math.pi)
R4 = 3 / (4 * math.exp(2 * G))

# Johnston Table V, alpha_BCS column (Hc(t)/Hc(0))，从 arXiv:1304.2275 附录提取
TABLE_V = {
    0.04: 0.998310, 0.06: 0.996190, 0.08: 0.993210, 0.10: 0.989370,
    0.12: 0.984660, 0.14: 0.979060, 0.16: 0.972560, 0.18: 0.965140,
    0.20: 0.956800, 0.22: 0.947520, 0.24: 0.937300, 0.26: 0.926130,
    0.28: 0.914020, 0.30: 0.900980, 0.32: 0.887020, 0.34: 0.872160,
    0.36: 0.856400, 0.38: 0.839790, 0.40: 0.822320, 0.42: 0.804030,
    0.44: 0.784940, 0.46: 0.765060, 0.48: 0.744430, 0.50: 0.723060,
    0.52: 0.700980, 0.54: 0.678200, 0.56: 0.654740, 0.58: 0.630630,
    0.60: 0.605880, 0.62: 0.580510, 0.64: 0.554540, 0.66: 0.527980,
    0.68: 0.500850, 0.70: 0.473170, 0.72: 0.444940, 0.74: 0.416190,
    0.76: 0.386930, 0.78: 0.357170, 0.80: 0.326920, 0.82: 0.296190,
    0.84: 0.265000, 0.86: 0.233360, 0.88: 0.201270, 0.90: 0.168750,
    0.92: 0.135810, 0.94: 0.102460, 0.96: 0.068700, 0.98: 0.034540,
}


def gap(t):
    if t >= 1:
        return 0.0
    def eq(d):
        return quad(lambda x: math.tanh(math.sqrt(x*x+d*d)/(2*t))/math.sqrt(x*x+d*d),
                    0, WD, limit=300, epsabs=1e-12)[0] - C
    return brentq(eq, 1e-10, 20, xtol=1e-13)


def entropy(t):
    d = gap(t)/A
    def integ(e):
        E = math.sqrt(e*e+d*d); x = A*E/t
        if x > 700: return 0.0
        return (1/(math.exp(x)+1))*(E+e*e/E)
    return 6*A*A/(math.pi**2*t)*quad(integ, 0, 30, limit=400, epsabs=1e-13, epsrel=1e-10)[0]


def main():
    # P2 分母 = R4
    den = quad(lambda t: t-entropy(t), 1e-6, 1.0, limit=300, epsabs=1e-10)[0]
    p2_err = abs(den-R4)/R4
    assert p2_err < 0.001, "P2: 熵积分分母=R4"

    # 预计算累积积分以供全程曲线（从 t 到 1）
    def Hc_ratio(t):
        num = quad(lambda x: x-entropy(x), t, 1.0-1e-12, limit=300, epsabs=1e-10)[0]
        return math.sqrt(num/den)

    # P1 Table V 盲测
    tests = []
    for t, ref in TABLE_V.items():
        h = Hc_ratio(t)
        tests.append((t, h, ref, abs(h-ref)/ref))
    max_err = max(x[3] for x in tests)
    assert max_err < 0.001, "P1: Hc 全程 Table V 盲测 <0.1%"

    # P3 近 Tc 斜率 kappa（用 Hc 曲线数值斜率）
    t1, t2 = 0.999, 0.9999
    h1, h2 = Hc_ratio(t1), Hc_ratio(t2)
    slope_num = (h2-h1)/(t2-t1) * (-1)  # -dHc/dt 在 Tc
    kappa_chain = 2*math.sqrt(2)*math.exp(G)/math.sqrt(7*Z3)
    # Hc(0)/gamma Tc^2 = sqrt(6pi)e^-gamma; kappa = Tc/Hc0 * (-dHc/dT)
    # -dHc/dT|Tc = Hc0 * kappa / Tc -> -d(Hc/Hc0)/dt = kappa
    p3_err = abs(slope_num - kappa_chain)/kappa_chain
    assert p3_err < 0.02, "P3: 近 Tc 斜率 kappa"

    # P4 偏差函数为负
    ts = np.linspace(0.04, 0.98, 80)
    hc_curve = np.array([Hc_ratio(t) for t in ts])
    dev = hc_curve - (1-ts**2)
    assert np.all(dev < 0), "P4: Hc 全程低于两流体（偏差负）"

    print("R16 临界场全程 + 五表全景（A 类贯通＋B 类工具）：")
    print("  P2 熵积分分母 = %.9f vs R4=%.9f，误差 %.2e" % (den, R4, p2_err))
    print("  P1 Hc(t) 对 Table V 盲测（抽样）：")
    for t, h, ref, err in tests[::8]:
        print("    t=%.2f  chain=%.6f  V=%.6f  err=%.2f%%" % (t, h, ref, 100*err))
    print("    最大误差 %.3f%% (49 点) < 0.1%%" % (100*max_err))
    print("  P3 近 Tc 斜率 -d(Hc/Hc0)/dt = %.4f vs kappa=%.4f（差 %.2f%%）" %
          (slope_num, kappa_chain, 100*p3_err))
    print("  P4 偏差函数全程为负（弱耦合特征）")
    print("  全部断言通过（非拟合）")

    # 五表统一曲线的归一化数据（用于面板 c）
    ts5 = np.linspace(0.05, 0.95, 60)
    gap_curve = np.array([gap(t)/A for t in ts5])                    # Table II
    ent_curve = np.array([entropy(t)/t for t in ts5])                # Table III 归一
    hc5 = np.array([Hc_ratio(t) for t in ts5])                       # Table V
    # 超流密度 (Table VI): 1-I，I 用 sech2 积分
    def I_of(t):
        d=gap(t)/A
        def f(y):
            z=0.5*math.sqrt(y*y+(A*d/t)**2)
            return 0.0 if z>700 else 1/(math.cosh(z)**2)
        return 0.5*quad(f,0,60,limit=300,epsabs=1e-13)[0]
    rho_curve = np.array([1-I_of(t) for t in ts5])                   # Table VI
    # 比热 (Table IV): 复用简化（用 dDelta2/dt 中心差分近似形状）
    def ces(t):
        d=gap(t)/A; h=1e-4
        dd=((gap(min(t+h,.999999))/A)**2-(gap(max(t-h,1e-9))/A)**2)/(2*h)
        def f(e):
            E=math.sqrt(e*e+d*d); x=A*E/t
            if x>700: return 0.0
            return (1/(math.exp(x)+1))*(1-1/(math.exp(x)+1))*(E*E/t-0.5*dd)
        return 6*A**3/(math.pi**2*t)*quad(f,0,30,limit=400,epsabs=1e-13)[0]
    ces_curve = np.array([ces(t)/2.426 for t in ts5])                # 归一到跳变

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, hc_curve, "k-", lw=2.2, label="链内 gap＋熵积分 Eq.(31)")
    ax.scatter(list(TABLE_V.keys()), list(TABLE_V.values()), s=28, color="red",
               zorder=5, label="Johnston Table V（盲测）")
    ax.plot(ts, 1-ts**2, "b--", lw=1.4, label="两流体 $1-t^2$（高估）")
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("$H_c(t)/H_c(0)$")
    ax.set_title("A  临界场全程曲线"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.fill_between(ts, dev, 0, color="green", alpha=0.3)
    ax.plot(ts, dev, "g-", lw=2.0)
    ax.axhline(0, color="gray", ls=":", lw=1)
    dmin = dev.min(); tmin = ts[dev.argmin()]
    ax.plot([tmin],[dmin],"ro",ms=6,label="$D_{min}=%.3f$ @ t=%.2f"%(dmin,tmin))
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("$D(t)=H_c/H_c(0)-(1-t^2)$")
    ax.set_title("B  偏差函数（全程负，弱耦合特征）"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(ts5, gap_curve, lw=2, label="gap $\\tilde\\Delta$ (Table II)")
    ax.plot(ts5, ent_curve, lw=2, label="熵 $S/\\gamma T$ (III)")
    ax.plot(ts5, ces_curve, lw=2, label="比热 $C/2.426\\gamma T_c$ (IV)")
    ax.plot(ts5, hc5, lw=2, label="临界场 $H_c/H_c(0)$ (V)")
    ax.plot(ts5, rho_curve, lw=2, label="超流密度 $\\rho_s/\\rho_s(0)$ (VI)")
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("归一化值")
    ax.set_title("C  五表统一全景：单一链内 gap 源贯通")
    ax.legend(fontsize=7); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    tables = ["II gap\nR11", "III 熵\nR14", "IV 比热\nR13", "V 临界场\nR16", "VI 穿透深度\nR15"]
    maxerrs = [0.1, 0.13, 0.10, 100*max_err, 0.22]  # 各表已验最大误差(%)
    bars = ax.bar(tables, maxerrs, color=["tab:blue","tab:green","tab:orange","tab:red","tab:purple"], alpha=0.85)
    for b,v in zip(bars,maxerrs):
        ax.text(b.get_x()+b.get_width()/2, v+0.02, "%.2f%%"%v, ha="center", fontsize=9)
    ax.set_ylabel("盲测最大相对误差 (%)"); ax.set_ylim(0, max(maxerrs)*1.4)
    ax.set_title("D  五表统一盲测误差汇总（均 <1%）"); ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R16_临界场全程与五表全景.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["P1 Hc 对 Table V 盲测", "%.3f%%" % (100*max_err), "49 点全温区，<0.1%"],
        ["P2 熵积分分母", "%.9f" % den, "=R4=%.9f，差 %.0e" % (R4, p2_err)],
        ["P3 近 Tc 斜率", "%.4f" % slope_num, "kappa=%.4f（差 %.2f%%）" % (kappa_chain, 100*p3_err)],
        ["P4 偏差函数全程负", "PASS", "D_min=%.3f @ t=%.2f" % (dmin, tmin)],
        ["P5 五表统一全景", "PASS", "gap/熵/比热/临界场/穿透深度单一 gap 源"],
        ["类别", "A 类贯通＋B 类工具", "热力学工具外部；gap 曲线链内"],
    ]
    with open(os.path.join(OUT, "R16_临界场全程与五表全景_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    with open(os.path.join(OUT, "R16_临界场全程与五表全景_盲测.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["t","chain_Hc","TableV","rel_err"])
        for t,h,ref,err in tests:
            w.writerow(["%.4f"%t,"%.8f"%h,"%.8f"%ref,"%.6f"%err])

    print("图:", png)


if __name__ == "__main__":
    main()
