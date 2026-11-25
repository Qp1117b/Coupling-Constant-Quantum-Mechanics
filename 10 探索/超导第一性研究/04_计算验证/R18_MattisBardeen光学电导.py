# -*- coding: utf-8 -*-
"""
预注册判定 R18：Mattis-Bardeen 光学电导与 FGT sum rule（非拟合）
==================================================================
链内 gap Δ0=pi/e^gamma -> MB 光学阈值 2Δ0、硬隙、FGT 谱重守恒。

复跑：python "10 探索/超导第一性研究/04_计算验证/R18_MattisBardeen光学电导.py"
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
from scipy.special import ellipk, ellipe
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
G = 0.5772156649015329
D = math.pi / math.exp(G)   # 链内 gap Δ0/kB Tc


def mb_sigma1(w):
    """MB Eq.61: sigma1s/sigma1n, w in kB Tc=1 units, gap=D."""
    if w <= 2 * D:
        return 0.0
    k = (w - 2 * D) / (w + 2 * D)
    m = k * k
    return (1 + 2 * D / w) * ellipe(m) - (4 * D / w) * ellipk(m)


def mb_sigma2(w):
    """MB Eq.63: sigma2s/sigma1n (T=0). k' = sqrt(1-k^2), k=(w-2D)/(w+2D)."""
    k = (w - 2 * D) / (w + 2 * D)
    kp2 = max(0.0, 1 - k * k)   # k'^2, in (0,1] for w>0
    return (D / w + 0.5) * ellipe(kp2) + (D / w - 0.5) * ellipk(kp2)


def main():
    # P1 光学阈值
    gap_ratio = 2 * D
    assert abs(gap_ratio - 3.527754) < 1e-4, "P1: 2Δ/kBTc=2π/e^γ"

    # P3 硬隙
    assert mb_sigma1(0.5 * D) == 0.0 and mb_sigma1(1.99 * D) == 0.0, "P3: 硬隙 σ1=0"
    assert mb_sigma1(2.0 * D) == 0.0, "P3: 阈值处为 0"

    # P2 曲线：单调上升 + 高ω趋1
    ws = np.linspace(1.5*D, 20*D, 400)
    s1 = np.array([mb_sigma1(w) for w in ws])
    hi = ws >= 2*D
    assert np.all(np.diff(s1[hi]) >= -1e-6), "P2: 单调上升"
    assert abs(mb_sigma1(200*D) - 1.0) < 0.02, "P2: 高ω趋1"

    # P4 FGT sum rule：累积谱重（缺失面积）趋平台
    def missing(Omega):
        return quad(lambda w: 1.0 - mb_sigma1(w), 0, Omega,
                    limit=500, points=[2*D] if Omega > 2*D else None)[0]
    Omega_scan = np.linspace(D, 100*D, 80)
    cum = np.array([missing(O) for O in Omega_scan])
    # 平台值：Omega=100D 时；谱重缺失应有限（硬隙驱逐）
    plateau = cum[-1]
    assert plateau > 0 and np.isfinite(plateau), "P4: FGT 谱重缺失有限"

    # P5 omega*sigma2 -> pi*Delta (Tinkham dirty-limit 标准结果)
    # 修正记录：初版误把 k' 写为 1（当 w<2Δ），得假象 e^γ；按 Eq.63 k'=sqrt(1-k^2) 修正后为 π。
    wsmall = 1e-4 * D
    w_sig2 = wsmall * mb_sigma2(wsmall) / D
    target = math.pi
    p5_err = abs(w_sig2 - target)/target
    assert p5_err < 0.001, "P5: ωσ2→πΔ"

    print("R18 Mattis-Bardeen 光学电导（A 类结构＋B 类工具）：")
    print("  P1 光学阈值 2Δ0/kBTc = %.6f（eV=Δ0=%.5f）" % (gap_ratio, D))
    print("  P2 曲线单调上升、高ω趋1（σ1(200Δ)=%.5f）" % mb_sigma1(200*D))
    print("  P3 硬隙 ω<2Δ0: σ1=0 严格成立")
    print("  P4 FGT 缺失谱重 ∫(σ1n-σ1s)dω → 平台 %.5f (×σ1n·kBTc)" % plateau)
    print("  P5 ωσ2/σ1n → π·Δ: 数值 %.6f vs π=%.6f（差 %.3f%%）" % (w_sig2, target, 100*p5_err))
    print("  全部断言通过（非拟合）")

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    wn = ws / (2*D)   # 归一到光学阈值
    ax.plot(wn, s1, "k-", lw=2.2)
    wn2 = np.linspace(0, 2.0, 100)
    ax.plot(wn2, np.zeros_like(wn2), "k-", lw=2.2)
    ax.axvline(1, color="red", ls="--", lw=1.2, label="光学阈值 $\\hbar\\omega_g=2\\Delta_0$")
    ax.set_xlabel("$\\hbar\\omega/2\\Delta_0$"); ax.set_ylabel("$\\sigma_{1s}/\\sigma_{1n}$")
    ax.set_ylim(0, 1.1)
    ax.set_title("A  Mattis-Bardeen $\\sigma_1$（硬隙＋阈值）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ws2 = np.linspace(0.05*D, 10*D, 300)
    s2 = np.array([mb_sigma2(w) for w in ws2])
    ax.plot(ws2/D, ws2*s2/D, "k-", lw=2.2, label="$\\omega\\sigma_{2s}/\\sigma_{1n}\\Delta$")
    ax.axhline(math.pi, color="blue", ls="--", lw=1.4, label="$\\pi$（Tinkham 标准）")
    ax.set_xlabel("$\\omega/\\Delta_0$"); ax.set_ylabel("$\\omega\\sigma_2/\\sigma_{1n}\\Delta_0$")
    ax.set_ylim(0, 3.6)
    ax.set_title("B  $\\sigma_2$ 低频极限 $\\to\\pi\\Delta$")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(Omega_scan/(2*D), cum, "g-", lw=2.2, label="累积缺失谱重")
    ax.axhline(plateau, color="red", ls="--", lw=1.2, label="平台=%.4f" % plateau)
    ax.set_xlabel("$\\Omega/2\\Delta_0$"); ax.set_ylabel("$\\int_0^\\Omega(\\sigma_{1n}-\\sigma_{1s})d\\omega$")
    ax.set_title("C  FGT sum rule：谱重缺失趋平台（=超流密度）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    dims = ["热力学\nR11-R16", "电动力学\nR15", "隧穿谱\nR17", "光学谱\nR18"]
    ax.text(0.5, 0.88, "四个维度：单一链内 gap 贯通", ha="center", fontsize=11, weight="bold")
    ax.text(0.5, 0.68, "$\\Delta_0=\\pi e^{-\\gamma}k_BT_c$（C5）", ha="center", fontsize=11, color="blue")
    ax.text(0.5, 0.50, "热力学: gap/比热/熵/临界场/凝聚能\n电动力学: ρ_s/λ\n隧穿: DOS 边/sum rule\n光学: 阈值 2Δ_0/FGT",
            ha="center", fontsize=9)
    ax.text(0.5, 0.22, "$2\\Delta_0/k_BT_c=3.5278$ 贯穿四维度", ha="center", fontsize=10, color="green")
    ax.text(0.5, 0.08, "B 类电动力学工具；强耦合/无序 sub-gap 偏离", ha="center", fontsize=8, color="red")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  四维度统一")

    fig.tight_layout()
    png = os.path.join(OUT, "R18_MattisBardeen光学电导.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["光学阈值", "2Δ0=%.5f" % gap_ratio, "$2\\Delta_0/k_BT_c=2\\pi/e^\\gamma$"],
        ["硬隙", "PASS", "ω<2Δ0: σ1s=0"],
        ["曲线单调趋1", "PASS", "σ1(200Δ)=%.4f" % mb_sigma1(200*D)],
        ["FGT 平台", "%.5f" % plateau, "谱重缺失→超流密度"],
        ["ωσ2 极限", "%.5f" % w_sig2, "$\\pi\\Delta_0$（Tinkham 标准）"],
        ["类别", "A 类结构＋B 类电动力学工具", "gap 链内；MB/FGT 工具外部"],
        ["边界", "弱耦合干净极限", "强耦合/无序 sub-gap 偏离；绝对 Tc 外生"],
    ]
    with open(os.path.join(OUT, "R18_MattisBardeen光学电导_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
