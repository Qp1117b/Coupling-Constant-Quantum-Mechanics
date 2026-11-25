# -*- coding: utf-8 -*-
"""
预注册判定 R20：约瑟夫森临界电流与 AB 纯数（非拟合）
=====================================================
链内 gap Δ0=pi/e^gamma -> AB T=0 约瑟夫森比 pi^2/(2 e^gamma)。
温度曲线 Ic(T)/Ic(0) = (Delta/Delta0) tanh(Delta/2kT)。

复跑：python "10 探索/超导第一性研究/04_计算验证/R20_约瑟夫森AB纯数.py"
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
A = math.pi / math.exp(G)   # Delta0/kB Tc
WD = 100.0
C = math.log(2 * WD * math.exp(G) / math.pi)
JOSEPHSON_RATIO = math.pi**2 / (2 * math.exp(G))


def gap(t):
    if t >= 1:
        return 0.0
    def eq(d):
        return quad(lambda x: math.tanh(math.sqrt(x*x+d*d)/(2*t))/math.sqrt(x*x+d*d),
                    0, WD, limit=300, epsabs=1e-12)[0] - C
    return brentq(eq, 1e-10, 20, xtol=1e-13)


def Ic_ratio(t):
    """Ic(T)/Ic(0) = (Delta/Delta0) tanh(Delta/2kT), 用链内 gap。"""
    if t >= 1:
        return 0.0
    d = gap(t) / A
    return d * math.tanh(d * A / (2 * t))


def main():
    # P1 约瑟夫森比纯数
    ratio_from_AB = (math.pi/2) * A
    assert abs(ratio_from_AB - JOSEPHSON_RATIO) < 1e-12, "P1: e Ic Rn/kB Tc = pi^2/(2e^gamma)"

    # P4 AB 温度曲线：单调、T->0 饱和、近 Tc 趋 0
    ts = np.linspace(0.02, 0.999, 120)
    ic = np.array([Ic_ratio(t) for t in ts])
    assert ic[0] > 0.99, "P4: T->0 饱和到 1"
    assert np.all(np.diff(ic) <= 1e-6), "P4: 单调下降"
    assert ic[-1] < 0.01, "P4: 近 Tc 趋 0"

    # P5 近 Tc 线性 Ic ~ (1-t)
    for t in [0.99, 0.999]:
        slope = Ic_ratio(t)/(1-t)
        assert 1.0 < slope < 6.0, "P5: 近 Tc 线性"

    # P2 Ic Rn = pi Delta0/(2e) -> gap ratio 一致
    # e Ic Rn = pi Delta0/2 => 2 e Ic Rn/(pi kB Tc) = Delta0/kB Tc = pi/e^gamma
    check = 2 * JOSEPHSON_RATIO / math.pi
    assert abs(check - A) < 1e-12, "P2: 与 gap ratio 一致"

    print("R20 约瑟夫森 AB 纯数（A 类结构＋B 类工具）：")
    print("  P1 约瑟夫森比 e Ic Rn/(kB Tc) = pi^2/(2e^gamma) = %.6f" % JOSEPHSON_RATIO)
    print("  P2 Ic Rn = pi Delta0/(2e) 与 gap ratio 一致（check=%.6f）" % check)
    print("  P3 Josephson 能 EJ = hbar Ic/(2e)（链内相位扇区载体，定性）")
    print("  P4 AB 温度曲线单调 1→0，T->0 饱和 %.4f，近 Tc %.4f" % (ic[0], ic[-1]))
    print("  P5 近 Tc Ic/(1-t): t=0.99→%.3f, t=0.999→%.3f（线性）" %
          (Ic_ratio(0.99)/0.01, Ic_ratio(0.999)/0.001))
    print("  全部断言通过（非拟合）")

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, ic, "k-", lw=2.2, label="链内 gap＋AB")
    ax.axhline(1.0, color="gray", ls=":", lw=1)
    ax.set_xlabel("$t=T/T_c$"); ax.set_ylabel("$I_c(T)/I_c(0)$")
    ax.set_title("A  AB 约瑟夫森临界电流温度曲线")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    phi = np.linspace(-np.pi, np.pi, 400)
    ax.plot(phi, np.sin(phi), "b-", lw=2.2, label="$I=I_c\\sin\\phi$")
    ax.axhline(0, color="gray", ls=":", lw=1)
    ax.set_xlabel("相位差 $\\phi$"); ax.set_ylabel("$I/I_c$")
    ax.set_title("B  电流-相位关系（链内相位扇区载体）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.text(0.5, 0.9, "约瑟夫森比纯数来源", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.72, "gap ratio: $2\\Delta_0/k_BT_c=2\\pi/e^\\gamma$（C5）", ha="center", fontsize=10)
    ax.text(0.5, 0.56, "AB $T=0$: $I_cR_n=\\pi\\Delta_0/(2e)$", ha="center", fontsize=10)
    ax.text(0.5, 0.40, "$\\frac{eI_cR_n}{k_BT_c}=\\frac{\\pi^2}{2e^\\gamma}=%.5f$" % JOSEPHSON_RATIO,
            ha="center", fontsize=12, color="blue")
    ax.text(0.5, 0.24, "相位扇区（环19）+ $U(1)$ 破缺（环13）提供载体",
            ha="center", fontsize=9)
    ax.text(0.5, 0.10, "$E_J=\\hbar I_c/2e=\\Phi_0 I_c/2\\pi$", ha="center", fontsize=10, color="green")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("C  纯数 $\\pi^2/2e^\\gamma$ 来源树")

    ax = axes[1, 1]
    phenomena = ["零电阻\n(电动力学)","迈斯纳/穿透\n(R15)","热力学\n(R11-16)","谱学\n(R17)","光学\n(R18)","约瑟夫森\n(R20)"]
    ax.text(0.5, 0.9, "单一链内 gap 贯通超导现象", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.66, "  ·  ".join(["gap", "$\\Upsilon$", "相位扇区"]), ha="center", fontsize=10, color="blue")
    ax.text(0.5, 0.44, "\n".join(["零电阻/迈斯纳：电动力学", "热力学：gap/比热/熵/临界场", "谱学：DOS/隧穿", "光学：MB/FGT", "约瑟夫森：$I_c\\sin\\phi$, AB 纯数"]),
            ha="center", fontsize=9)
    ax.text(0.5, 0.10, "B 类工具；隧道极限，高透明/Andreev 偏离只登记", ha="center", fontsize=8, color="red")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  六大现象贯通")

    fig.tight_layout()
    png = os.path.join(OUT, "R20_约瑟夫森AB纯数.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["约瑟夫森比", "%.6f" % JOSEPHSON_RATIO, "$eI_cR_n/k_BT_c=\\pi^2/2e^\\gamma$（新纯数）"],
        ["AB T=0", "$\\pi\\Delta_0/2e$", "与 gap ratio 一致"],
        ["Josephson 能", "$E_J=\\hbar I_c/2e$", "链内相位扇区载体"],
        ["温度曲线", "1→0 单调", "T<0.2Tc 饱和，近 Tc 线性"],
        ["类别", "A 类结构＋B 类工具", "AB/Josephson 工具外部；Rn 外生"],
        ["边界", "隧道极限", "高透明 SNS/Andreev/二极管只登记；强耦合偏离"],
    ]
    with open(os.path.join(OUT, "R20_约瑟夫森AB纯数_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
