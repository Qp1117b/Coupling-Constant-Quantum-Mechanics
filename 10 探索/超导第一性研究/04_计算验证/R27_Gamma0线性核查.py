# -*- coding: utf-8 -*-
"""
R27：E2 的 Gamma_0 前提核查——"T^2 填平"误引，相位权重不能充当对寿命
=====================================================================
预注册 R27 的 P1–P5（跑数前写死）：
  P1 文献卡逐字引文含 "proportional to T-Tc" / "linearly" / Gamma0=8(T-Tc)/pi
  P2 Gamma0(Tc)=0 而 omega_D*(1-w(Tc))>0 ⇒ 常数重标度不可能
  P3 Delta_pg(0)/Gamma0(T*) ∈ [0.5,2]（两个 PRB 样品）
  P4 两分量谱归一 ∫A=1；Tc 附近尖锐、T* 填平
  P5 Lean Gamma0VsPhaseWeight

复跑：python "10 探索/超导第一性研究/04_计算验证/R27_Gamma0线性核查.py"
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
GAMMA = 0.5772156649015329


def w_full(x):
    """(10B.1) 全域 w(T)=2∫_0^1 y tanh(y/(2x)) dy，x=T/omega_D。"""
    if x <= 0:
        return 1.0
    return 2.0 * quad(lambda y: y * math.tanh(y / (2.0 * x)), 0.0, 1.0,
                      epsabs=1e-13, epsrel=1e-13)[0]


def main():
    # ---------- P1：原文逐字核查 ----------
    card = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "01_文献基线",
                             "文献卡_R27_Gamma0线性.md"), encoding="utf-8").read()
    for phrase in ["proportional to T-Tc", "linearly with T", "Gamma_0(T)=8(T-T_c)/pi",
                   "T* corresponds to where"]:
        assert phrase in card, "P1: 引文缺失 %s" % phrase
    assert "(T/T_c)^2" in card, "P1: 误引记录缺失"

    # ---------- P2：零点不相容 ----------
    Tc, wD = 83.0, 300.0                       # PRB 欠掺样品 + 典型 Debye 能标（仅为对照）
    xc = Tc / wD
    wc = w_full(xc)
    gap_c = wD * (1.0 - wc)                    # 链候选 Γ_chain = ω_D(1-w)
    gamma0_c = (8.0 / math.pi) * (Tc - Tc)     # = 0（严格）
    assert gamma0_c == 0.0, "P2: Γ0(Tc) 应为 0"
    assert gap_c > 0.0, "P2: 1-w(Tc) 应 >0"

    Ts = np.linspace(Tc + 1e-3, 210.0, 200)
    g0 = (8.0 / math.pi) * (Ts - Tc)
    gc = np.array([wD * (1.0 - w_full(t / wD)) for t in Ts])
    ratio = gc / g0
    print("R27 Gamma_0 前提核查（文献原文＋结构判定，无拟合）：")
    print("  P1 两篇原文均为 Γ0∝T−Tc（线性），项目笔记的 (T/Tc)^2 是误引")
    print("  P2 Γ0(Tc)=0；ω_D[1−w(Tc)]=%.3f k_B K >0 ⇒ 常数重标度不可行" % gap_c)
    print("     比值 Γ_chain/Γ0 在 [Tc+0.001,210] 上从 %.3g 变到 %.3g（跨 %.1f 个量级）"
          % (ratio[0], ratio[-1], math.log10(ratio[0] / ratio[-1])))

    # 低温展开有效域
    xs = np.logspace(-2, 0, 200)
    full = np.array([1.0 - w_full(v) for v in xs])
    lead = (math.pi ** 2 / 3.0) * xs ** 2
    dev = np.abs(lead - full) / full
    i_half = int(np.argmin(np.abs(xs - 0.5)))
    assert dev[i_half] > 0.3, "P2: x=0.5 处低温展开应显著失效"

    # ---------- P3：外部锚点量级 ----------
    samples = [(200.0, 83.0), (150.0, 67.0)]
    ratios = []
    for ts, tc in samples:
        delta = (math.pi / math.exp(GAMMA)) * ts          # Δ_pg(0)/k_B
        g0s = (8.0 / math.pi) * (ts - tc)                  # Γ0(T*)/k_B
        r = delta / g0s
        ratios.append(r)
        assert 0.5 <= r <= 2.0, "P3: 比值 %.3f 越界" % r
    print("  P3 Δ_pg(0)/Γ0(T*) = %.3f (200/83)、%.3f (150/67) ∈ [0.5,2]" % tuple(ratios))

    # ---------- P4：两分量谱（形状综合，B 类） ----------
    omega = np.linspace(-1.0, 1.0, 8001)   # 宽域保证截断误差 <1e-12；作图时再缩 x 限
    # 相干分量：两个窄峰 ±Δ；非相干分量：宽峰 Γ0（均为归一高斯，仅为形状示意）
    def gauss(center, width):
        g = np.exp(-0.5 * ((omega - center) / width) ** 2) / (width * math.sqrt(2 * math.pi))
        g += np.exp(-0.5 * ((omega + center) / width) ** 2) / (width * math.sqrt(2 * math.pi))
        return g / 2.0     # 双峰总权重 1

    delta_eV = 0.03
    a_coh = gauss(delta_eV, 0.004)
    a_incoh = gauss(0.0, 0.06)
    q_tc, q_star = 0.592746, 0.40     # 仅示意：q(Tc)=座渗流阈；q(T*)<p_c
    A_tc = q_tc * a_coh + (1 - q_tc) * a_incoh
    A_star = q_star * a_coh + (1 - q_star) * a_incoh
    for A in (A_tc, A_star):
        assert abs(float(np.trapezoid(A, omega)) - 1.0) < 1e-12, "P4: 谱未归一"

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(Ts, g0, "b-", lw=2.4, label="$\\Gamma_0(T)=8(T-T_c)/\\pi$（线性，$T_c$ 处为 0）")
    ax.plot(Ts, gc, "r--", lw=2.2, label="$\\omega_D[1-w(T)]$（$T_c$ 处为正）")
    ax.plot([Tc], [0], "o", ms=9, color="b")
    ax.plot([Tc], [gap_c], "s", ms=8, color="r")
    ax.annotate("零点位置不同", (Tc + 4, gap_c + 12), fontsize=9)
    ax.set_xlabel("$T$ (K)")
    ax.set_ylabel("能量（$k_B$ K）")
    ax.set_title("A  对寿命宽度 vs 相位权重：$T_c$ 处不相容")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.loglog(xs, full, "k-", lw=2.4, label="全域 $1-w$（(10B.1)）")
    ax.loglog(xs, lead, "r--", lw=2.2, label="低温展开 $\\pi^2T^2/(3\\omega_D^2)$")
    ax.plot([0.5], [1 - w_full(0.5)], "o", ms=8, color="k")
    ax.annotate("$T^*/\\omega_D\\approx0.5$ 处偏离 %.0f%%" % (100 * dev[i_half]),
                (0.12, 0.02), fontsize=9)
    ax.set_xlabel("$T/\\omega_D$")
    ax.set_ylabel("$1-w$")
    ax.set_title("B  低温 $T^2$ 展开在 $T^*$ 附近失效")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    labels = ["200/83 K", "150/67 K"]
    ax.bar(labels, ratios, color=["#1f77b4", "#d62728"], alpha=0.85)
    ax.axhline(1.0, color="gray", ls="--", lw=1.2)
    ax.set_ylabel("$\\Delta_{\\rm pg}(0)/\\Gamma_0(T^*)$")
    ax.set_ylim(0, 1.6)
    ax.set_title("C  外部量级自洽：$\\Delta_{\\rm pg}(0)\\approx\\Gamma_0(T^*)$（B 类）")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.plot(omega * 1e3, A_tc, "b-", lw=2.2, label="$T\\to T_c^+$（$\\Gamma_0\\to0$，尖锐）")
    ax.plot(omega * 1e3, A_star, "r--", lw=2.2, label="$T\\to T^*$（$\\Gamma_0\\approx\\Delta$，填平）")
    ax.set_xlabel("$\\omega$ (meV)")
    ax.set_ylabel("$A(\\omega)$（归一）")
    ax.set_xlim(-120, 120)
    ax.set_title("D  两分量谱形状（B 类示意，$q$ 与宽度外生）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.tight_layout()
    png = os.path.join(OUT, "R27_Gamma0线性核查.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "两篇原文 Γ0∝T−Tc（线性）", "误引确认"],
        ["P2", "Γ0(Tc)=0；ω_D[1−w(Tc)]=%.3f k_B K" % gap_c, "映射否决"],
        ["P3", "Δ/Γ0(T*)=%.3f, %.3f" % tuple(ratios), "量级自洽（B 类）"],
        ["P4", "两分量谱 ∫A=1", "形状可写（B 类）"],
        ["P5", "零点不相容（Lean）", "由 Lean 承载"],
        ["结论", "E2 与 G21 状态不动", "未闭合"],
    ]
    with open(os.path.join(OUT, "R27_Gamma0线性核查_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("  P4 两分量谱归一残差 <1e-12；Tc 尖锐、T* 填平")
    print("图:", png)


if __name__ == "__main__":
    main()
