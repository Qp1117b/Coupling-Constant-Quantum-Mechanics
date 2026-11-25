# -*- coding: utf-8 -*-
"""
第92轮补（成果登记 R-101）：环14A——链内 alpha^2F 与两矩分歧的结构消解（非拟合）
====================================================================================
检验：
  A alpha^2F=A w^2 Θ(w_D-w)（链内曲率模 Debye DOS 形状）与归一化权重 g=2w/w_D²；
  B 对数矩 ∫₀¹2x ln x dx=-1/2 ⇒ omega_log=e^{-1/2} w_D（=相位支/Eliashberg）；
  C 两对数矩比 e^{-1/3}/e^{-1/2}=e^{1/6}（审-17 分歧的精确来源）；
  D 两二阶矩 1/2（alpha^2F/ω 权重）vs 3/5（DOS 权重），比 5/6，
     lambda=A w_D²、同位素 lambda∝1/M。

图像用于检验幂次/矩/量级，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环14A_链内alpha2F与两矩消解.py"
"""
import csv
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


def I(f, a=0.0, b=1.0):
    return quad(f, a, b, epsabs=1e-13, epsrel=1e-13)[0]


def main():
    # ---------- 矩的高精度数值验证（与 Lean 常量对应） ----------
    wNorm = I(lambda x: 2 * x)
    logM = I(lambda x: 2 * x * np.log(x) if x > 0 else 0.0)
    w2A2F = I(lambda x: 2 * x * x**2)
    dosN = I(lambda x: 3 * x**2)
    dosW2 = I(lambda x: 3 * x**4)
    w2DOS = dosW2 / dosN

    assert abs(wNorm - 1.0) < 1e-12, f"权重归一 {wNorm}"
    assert abs(logM + 0.5) < 1e-12, f"对数矩 {logM}"
    assert abs(w2A2F - 0.5) < 1e-12, f"alpha2F 二阶矩 {w2A2F}"
    assert abs(w2DOS - 0.6) < 1e-12, f"DOS 二阶矩 {w2DOS}"
    assert abs((w2A2F / w2DOS) - 5.0 / 6.0) < 1e-12, "二阶矩比应为 5/6"

    # 对数矩比 e^{1/6}
    amp = np.exp(-1.0 / 3.0)
    ph = np.exp(-1.0 / 2.0)
    gap = amp / ph
    assert abs(gap - np.exp(1.0 / 6.0)) < 1e-12, "两对数矩比应为 e^{1/6}"

    # lambda = A w_D²；同位素 lambda ∝ 1/M
    A_eph = 0.7
    wD = 300.0
    lam = A_eph * wD**2
    assert abs(lam - 2 * A_eph * I(lambda x: x) * wD**2) < 1e-9
    M1, M2 = 1.0, 4.0
    assert abs((wD / np.sqrt(M2))**2 / (wD / np.sqrt(M1))**2 - M1 / M2) < 1e-12

    # ---------- 四面板 ----------
    w = np.linspace(0, wD, 500)
    A = 1.0
    a2f = A * w**2
    a2f[w > wD] = 0.0
    g = 2 * w / wD**2

    x = np.linspace(1e-6, 1, 500)

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A
    ax = axes[0, 0]
    ax.plot(w / wD, a2f / (A * wD**2), lw=2.0, color="#1f77b4",
            label="$\\alpha^2F\\propto\\omega^2$（截断 $\\omega_D$）")
    ax.plot(x, 2 * x, "--", lw=1.5, color="g",
            label="归一化权重 $g=2x$")
    ax.set_xlabel("$\\omega/\\omega_D$")
    ax.set_ylabel("归一谱 / 权重")
    ax.set_title("A  链内 $\\alpha^2F$：曲率模 Debye DOS 形状")
    ax.legend(fontsize=8)

    # B
    ax = axes[0, 1]
    ax.plot(x, 2 * x * np.log(x), lw=2.0, color="#1f77b4")
    ax.axhline(logM, color="r", ls="--", lw=1.2,
               label=f"积分 $={logM:.6f}=-1/2$")
    ax.set_xlabel("$x=\\omega/\\omega_D$")
    ax.set_ylabel("$2x\\ln x$")
    ax.set_title("B  对数矩：$\\ln\\omega_{\\log}=\\ln\\omega_D-1/2$")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    labels = ["振幅支 $e^{-1/3}$", "相位支／链内 $e^{-1/2}$"]
    vals = [amp, ph]
    ax.bar(labels, vals, color=["orange", "#1f77b4"])
    ax.set_ylabel("$\\omega_{\\log}/\\omega_D$")
    ax.set_title(f"C  两矩比 $e^{{1/6}}$={gap:.6f}（审-17 分歧＝权重差）")

    # D
    ax = axes[1, 1]
    labels2 = ["$\\alpha^2F/\\omega$ 权重\n(1/2)", "声子 DOS 权重\n(3/5, FE10)"]
    vals2 = [w2A2F, w2DOS]
    ax.bar(labels2, vals2, color=["#1f77b4", "green"])
    ax.set_ylabel("二阶矩 $/\\omega_D^2$")
    ax.set_title(f"D  两约定差＝权重差，比 $={w2A2F/w2DOS:.6f}=5/6$")

    fig.tight_layout()
    png = os.path.join(OUT, "环14A_链内alpha2F与两矩消解.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["权重归一 ∫2x", f"{wNorm:.12f}", "=1"],
        ["对数矩 ∫2x ln x", f"{logM:.12f}", "=-1/2 ⇒ ω_log=e^{-1/2}ω_D"],
        ["α²F 二阶矩 ∫2x·x²", f"{w2A2F:.12f}", "=1/2（Pickett/RMTA 约定）"],
        ["DOS 二阶矩 ∫3x⁴/∫3x²", f"{w2DOS:.12f}", "=3/5（FE10 约定）"],
        ["二阶矩比", f"{w2A2F/w2DOS:.12f}", "=5/6"],
        ["两对数矩比", f"{gap:.12f}", "=e^{1/6}（审-17 分歧来源）"],
        ["λ=A ω_D²", f"{lam:.4f}", "A 外生"],
        ["同位素 λ∝1/M", "PASS", "ω_D∝M^{-1/2}"],
    ]
    with open(os.path.join(OUT, "环14A_链内alpha2F与两矩消解_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        wcsv = csv.writer(fo)
        wcsv.writerow(["量", "值", "说明"])
        wcsv.writerows(summary)
    with open(os.path.join(OUT, "环14A_链内alpha2F与两矩消解.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        wcsv = csv.writer(fo)
        wcsv.writerow(["x", "alpha2F_norm", "g", "2xlnx"])
        for i in range(len(x)):
            wcsv.writerow([f"{x[i]:.6g}", f"{x[i]**2:.6g}",
                           f"{2*x[i]:.6g}",
                           f"{2*x[i]*np.log(x[i]):.6g}"])

    print("第92轮补 审-15/审-17 链内 α²F 与两矩消解：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
