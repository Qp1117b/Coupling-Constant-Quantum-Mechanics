# -*- coding: utf-8 -*-
"""
预注册判定 R12：热力学临界场斜率纯数 kappa=2sqrt2 e^gamma/sqrt(7 zeta3)
========================================================================
链内 gap ratio + 比热跳变 + 严格热力学 Rutgers 公式 => kappa。
对照两流体抛物线(kappa=2)与 Al 精密临界场实验(Phys Rev 138 A1428)。

复跑：python "10 探索/超导第一性研究/04_计算验证/R12_临界场斜率纯数.py"
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
GAMMA = 0.5772156649015329
ZETA3 = 1.202056903159594

KAPPA_CHAIN = 2 * math.sqrt(2) * math.exp(GAMMA) / math.sqrt(7 * ZETA3)
KAPPA_TWOFLUID = 2.0
LOW_T_COEFF = math.exp(2 * GAMMA) / 3                 # 1.0574
HC0_OVER_SQRT = math.sqrt(6 * math.pi) * math.exp(-GAMMA)  # 2.438

# Al 实验：Phys. Rev. 138, A1428 (1965)
AL_TC, AL_DHDT, AL_DHDT_ERR, AL_H0, AL_H0_ERR = 1.175, 158.0, 4.0, 104.8, 0.6
KAPPA_AL = AL_TC * AL_DHDT / AL_H0
KAPPA_AL_ERR = KAPPA_AL * math.sqrt((AL_DHDT_ERR / AL_DHDT) ** 2 + (AL_H0_ERR / AL_H0) ** 2)

BETA_CHAIN = (4 - KAPPA_CHAIN) / 2
BETA_TWOFLUID = 1.0


def main():
    # ---------- 断言 ----------
    # P1 恒等式：kappa^2 = 8 e^{2gamma}/(7 zeta3)
    lhs = KAPPA_CHAIN ** 2
    rhs = 8 * math.exp(2 * GAMMA) / (7 * ZETA3)
    assert abs(lhs - rhs) < 1e-12, "P1: kappa^2=8 e^{2gamma}/(7 zeta3)"

    # P2 两流体高估
    over = (KAPPA_TWOFLUID - KAPPA_CHAIN) / KAPPA_TWOFLUID
    assert over > 0.10, "P2: 两流体高估 >10%"

    # P3 Al 实验更靠近链内
    d_chain = abs(KAPPA_AL - KAPPA_CHAIN)
    d_twofluid = abs(KAPPA_AL - KAPPA_TWOFLUID)
    assert d_chain < d_twofluid, "P3: Al 实验更靠近链内纯数"
    assert d_chain <= KAPPA_AL_ERR * 1.5, "P3: 链内落入 Al 实验 ~1sigma 附近"

    # P4/P5 纯数
    assert abs(LOW_T_COEFF - 1.0574) < 1e-3, "P4: e^{2gamma}/3=1.0574"
    assert abs(HC0_OVER_SQRT - 2.438) < 1e-3, "P5: sqrt(6pi)e^{-gamma}=2.438"

    print("R12 临界场斜率纯数（A 类，严格热力学）：")
    print(f"  kappa_chain = 2 sqrt2 e^g/sqrt(7 zeta3) = {KAPPA_CHAIN:.6f}")
    print(f"  kappa_twofluid = 2.0（高估 {over:.1%}）")
    print(f"  kappa_Al = {KAPPA_AL:.4f} +/- {KAPPA_AL_ERR:.4f} (Phys Rev 138 A1428)")
    print(f"  距链内 {d_chain:.4f}（{d_chain/KAPPA_CHAIN:.1%}），距两流体 {d_twofluid:.4f}（{d_twofluid/KAPPA_TWOFLUID:.1%}）")
    print(f"  beta_chain = {BETA_CHAIN:.5f} (>1, 两流体 beta=1)")
    print(f"  e^{{2g}}/3 = {LOW_T_COEFF:.5f}; sqrt(6pi)e^-g = {HC0_OVER_SQRT:.5f}")
    print("  全部断言通过（非拟合）")

    # ---------- 曲线 ----------
    ts = np.linspace(0, 1, 300)
    h_chain = 1 - BETA_CHAIN * ts ** 2 - (1 - BETA_CHAIN) * ts ** 4
    h_twofluid = 1 - ts ** 2
    d_chain_curve = h_chain - (1 - ts ** 2)     # = (1-beta)(t^4-t^2)
    d_min_idx = int(np.argmin(d_chain_curve))
    d_min = d_chain_curve[d_min_idx]

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(ts, h_chain, "k-", lw=2.2, label="链内 Taylor $\\beta=%.4f$" % BETA_CHAIN)
    ax.plot(ts, h_twofluid, "r--", lw=1.6, label="两流体 $\\beta=1$（抛物线）")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$H_c(t)/H_c(0)$")
    ax.set_title("A  归一化临界场：链内 vs 两流体")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(ts, d_chain_curve, "b-", lw=2.0, label="链内偏差函数 $D(t)$")
    ax.axhline(0, color="gray", ls=":", lw=1.0)
    ax.plot([ts[d_min_idx]], [d_min], "ro", ms=7,
            label="最小 $D_{min}=%.4f$ @ $t=%.2f$" % (d_min, ts[d_min_idx]))
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$D(t)=H_c/H_c(0)-(1-t^2)$")
    ax.set_title("B  偏差函数（弱耦合负偏差）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    labels = ["链内纯数\n$2\\sqrt{2} e^\\gamma/\\sqrt{7\\zeta_3}$",
              "Al 实验\nPhys Rev 138 A1428",
              "两流体近似\n$1-t^2$"]
    vals = [KAPPA_CHAIN, KAPPA_AL, KAPPA_TWOFLUID]
    cols = ["tab:blue", "tab:orange", "tab:red"]
    bars = ax.bar(labels, vals, color=cols, alpha=0.85)
    ax.errorbar([1], [KAPPA_AL], yerr=[KAPPA_AL_ERR], fmt="none",
                ecolor="black", capsize=6, ms=8)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.03, "%.3f" % v,
                ha="center", fontsize=10)
    ax.set_ylabel("$\\kappa=(T_c/H_c(0))|dH_c/dT|_{T_c}$")
    ax.set_ylim(1.5, 2.15)
    ax.set_title("C  $\\kappa$ 对照：链内最接近 Al 实验")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.text(0.5, 0.93, "链内两纯数 → 临界场斜率", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.76, "gap ratio: $2\\pi/e^\\gamma$  $\\Rightarrow$  $e^\\gamma$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.62, "比热跳变: $\\Delta C/\\gamma T_c=12/7\\zeta_3$  $\\Rightarrow$  $\\zeta_3$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.46, "Rutgers: $\\Delta C=\\frac{T_c}{4\\pi}(dH_c/dT)^2_{T_c}$",
            ha="center", fontsize=10)
    ax.text(0.5, 0.32, "$\\kappa=\\frac{2\\sqrt{2} e^\\gamma}{\\sqrt{7\\zeta_3}}=%.4f$" % KAPPA_CHAIN,
            ha="center", fontsize=12, color="blue")
    ax.text(0.5, 0.17, "两流体给 $\\kappa=2$（高估 %.1f%%）" % (100 * over),
            ha="center", fontsize=10, color="red")
    ax.text(0.5, 0.06, "Al 实验 %.3f±%.3f：链内差 %.1f%%" % (KAPPA_AL, KAPPA_AL_ERR, 100 * d_chain / KAPPA_CHAIN),
            ha="center", fontsize=9, color="green")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  纯数来源树")

    fig.tight_layout()
    png = os.path.join(OUT, "R12_临界场斜率纯数.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["kappa 链内", "%.6f" % KAPPA_CHAIN, "$2\\sqrt{2} e^\\gamma/\\sqrt{7\\zeta_3}$"],
        ["kappa 两流体", "2.000000", "抛物线 $1-t^2$，高估 %.1f%%" % (100 * over)],
        ["kappa Al 实验", "%.4f±%.4f" % (KAPPA_AL, KAPPA_AL_ERR), "Phys Rev 138 A1428 (1965)"],
        ["距链内", "%.1f%%" % (100 * d_chain / KAPPA_CHAIN), "落入 ~1sigma"],
        ["距两流体", "%.1f%%" % (100 * d_twofluid / KAPPA_TWOFLUID), "链内胜"],
        ["beta 链内", "%.5f" % BETA_CHAIN, "$H_c=H_{c0}[1-\\beta t^2-(1-\\beta)t^4]$"],
        ["D_min", "%.4f @ t=%.2f" % (d_min, ts[d_min_idx]), "文献 BCS 精确约 -0.037 @ t~0.5"],
        ["低温系数", "%.5f" % LOW_T_COEFF, "$e^{2\\gamma}/3$（Molinari）"],
        ["Hc0/sqrt(gamma Tc^2)", "%.5f" % HC0_OVER_SQRT, "$\\sqrt{6\\pi}e^{-\\gamma}$（Johnston Eq.30）"],
        ["类别", "A 类条件具备", "弱耦合单带；强耦合 Pb/Hg 偏离预注册允许"],
    ]
    with open(os.path.join(OUT, "R12_临界场斜率纯数_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
