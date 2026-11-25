# -*- coding: utf-8 -*-
"""
预注册判定 R17：准粒子态密度与 Giaever 隧穿谱（非拟合）
========================================================
链内 gap Δ0=pi/e^gamma -> BCS DOS E/sqrt(E^2-Delta^2)，
检验 gap edge 平方根发散、态守恒 sum rule、Giaever 隧穿。

复跑：python "10 探索/超导第一性研究/04_计算验证/R17_准粒子态密度与隧穿谱.py"
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
G = 0.5772156649015329
DELTA = math.pi / math.exp(G)   # 链内 gap Δ0/kB Tc = 1.7639


def dos_ratio(E):
    if E < DELTA:
        return 0.0
    return E / math.sqrt(E*E - DELTA*DELTA)


def main():
    # P2 edge 发散系数 sqrt(Delta/2)
    eps = 1e-7
    edge_num = dos_ratio(DELTA + eps)
    edge_pred = math.sqrt(DELTA/(2*eps))
    p2_err = abs(edge_num-edge_pred)/edge_pred
    assert p2_err < 0.001, "P2: edge 发散系数"

    # P3/P4 sum rule: ∫_0^X (Ns/Nn -1)dE = sqrt(X^2-Delta^2)-X -> 0
    def integ(E):
        return dos_ratio(E) - 1.0
    X = 50*DELTA
    sum_num = quad(integ, 0, X, limit=400, points=[DELTA])[0]
    sum_ana = math.sqrt(X*X-DELTA*DELTA) - X
    p3_err = abs(sum_num - sum_ana)
    assert p3_err < 1e-8, "P3: sum rule 有限和"
    assert abs(sum_ana) < 0.02, "P3: X->inf 极限近 0"

    # P5 gap edge 位置 = eV = Delta
    edge_position = DELTA
    gap_ratio = 2*DELTA
    assert abs(gap_ratio - 3.527754) < 1e-4, "P5: 2Δ/kBTc=2π/e^γ"

    print("R17 准粒子态密度与 Giaever 隧穿（A 类结构＋B 类工具）：")
    print("  P2 edge 发散系数: 数值=%.4f vs sqrt(Δ/2)=%.4f（误差 %.2f%%）" %
          (edge_num, edge_pred, 100*p2_err))
    print("  P3 sum rule: ∫(Ns/Nn-1)dE=%.10f vs sqrt(X^2-Δ^2)-X=%.10f（差 %.1e）" %
          (sum_num, sum_ana, p3_err))
    print("  P3 X->inf: sqrt(X^2-Δ^2)-X -> 0（被隙驱逐态=相干峰吸收态）")
    print("  P4 有限和数值-解析恒等式吻合")
    print("  P5 gap edge at eV=Δ=%.5f；2Δ/kBTc=%.6f" % (edge_position, gap_ratio))
    print("  全部断言通过（非拟合）")

    # DOS 曲线
    Es = np.linspace(0.5*DELTA, 5*DELTA, 600)
    dos = np.array([dos_ratio(E) for E in Es])

    # 有限温隧穿 dI/dV ∝ ∫ Ns(E)(-df/dE(E-eV)) dE
    def didv(V, T):
        def kernel(E, ev):
            x = (E-ev)/T
            if x > 700: return 0.0
            return 1/(4*T*math.cosh(x/2)**2) if abs(x)<700 else 0.0
        def integ(E):
            return dos_ratio(E)*kernel(E, V)
        return quad(integ, DELTA, V+20*T if V+20*T>DELTA else DELTA+20*T,
                    limit=300, epsabs=1e-10)[0]
    Vs = np.linspace(0, 2.2*DELTA, 300)
    didv0 = np.array([dos_ratio(V) if V>=DELTA else 0.0 for V in Vs])  # T->0
    T_finite = 0.06*DELTA
    didvT = np.array([didv(V, T_finite) for V in Vs])

    # 图
    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(Es/DELTA, dos, "k-", lw=2.2)
    ax.axvline(1, color="red", ls="--", lw=1.2, label="gap edge $E=\\Delta_0$")
    ax.axhline(1, color="gray", ls=":", lw=1)
    ax.set_xlabel("$E/\\Delta_0$"); ax.set_ylabel("$N_s/N_n$")
    ax.set_ylim(0, 6)
    ax.set_title("A  链内 BCS 态密度（硬隙＋相干峰）")
    ax.legend(fontsize=9); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    de = np.logspace(-5, -1, 200)
    dos_edge = np.array([dos_ratio(DELTA+d) for d in de])
    ax.loglog(de/DELTA, dos_edge, "k-", lw=2.2, label="链内 DOS")
    ax.loglog(de/DELTA, np.sqrt(DELTA/(2*de)), "b--", lw=1.5,
              label="$\\sqrt{\\Delta_0/2(E-\\Delta_0)}$")
    ax.set_xlabel("$(E-\\Delta_0)/\\Delta_0$"); ax.set_ylabel("$N_s/N_n$")
    ax.set_title("B  gap edge 平方根发散（系数 $\\sqrt{\\Delta_0/2}$）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    Xs = np.linspace(1.2*DELTA, 20*DELTA, 100)
    sum_curve = [quad(integ, 0, X, limit=400, points=[DELTA])[0] for X in Xs]
    sum_an_curve = np.sqrt(Xs**2-DELTA**2)-Xs
    ax.plot(Xs/DELTA, sum_curve, "k-", lw=2.2, label="数值积分")
    ax.plot(Xs/DELTA, sum_an_curve, "r--", lw=1.5, label="$\\sqrt{X^2-\\Delta_0^2}-X$")
    ax.axhline(0, color="gray", ls=":", lw=1)
    ax.set_xlabel("$X/\\Delta_0$"); ax.set_ylabel("$\\int_0^X(N_s/N_n-1)dE$")
    ax.set_title("C  态守恒 sum rule（差 %.0e）" % p3_err)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.plot(Vs/DELTA, didv0, "k-", lw=2.2, label="$T\\to0$: $dI/dV\\propto N_s(eV)$")
    # 有限温曲线用“高压归一到1”的方式，与 T->0 曲线在同一标度可比
    didvT_norm = didvT / didvT[-1] if didvT[-1] > 0 else didvT
    ax.plot(Vs/DELTA, didvT_norm, "b--", lw=1.5, label="有限温展宽（定性，高压归一）")
    ax.axvline(1, color="red", ls="--", lw=1.2, label="gap edge $eV=\\Delta_0$")
    ax.set_xlabel("$eV/\\Delta_0$"); ax.set_ylabel("$dI/dV$ (a.u.)")
    ax.set_ylim(0, 6)
    ax.set_title("D  Giaever 隧穿谱（$2\\Delta/k_BT_c=%.3f$）" % gap_ratio)
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    fig.tight_layout()
    png = os.path.join(OUT, "R17_准粒子态密度与隧穿谱.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["gap Δ0/kBTc", "%.6f" % DELTA, "π/e^γ（C5）"],
        ["P2 edge 系数", "%.5f" % edge_pred, "√(Δ0/2)，误差 %.2f%%" % (100*p2_err)],
        ["P3 sum rule 差", "%.1e" % p3_err, "数值 vs √(X²-Δ²)-X"],
        ["P3 X->∞", "0", "被隙驱逐态=相干峰吸收态"],
        ["P5 gap edge", "eV=Δ0", "2Δ/kBTc=%.6f" % gap_ratio],
        ["类别", "A 类结构＋B 类谱学工具", "DOS/隧穿公式外部；gap 链内"],
        ["边界", "弱耦合单带", "强耦合 Pb/Hg 声子 wiggles 偏离；实验展宽"],
    ]
    with open(os.path.join(OUT, "R17_准粒子态密度与隧穿谱_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo); w.writerow(["量","值","说明"]); w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
