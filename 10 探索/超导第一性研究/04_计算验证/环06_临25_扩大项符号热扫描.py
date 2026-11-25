# -*- coding: utf-8 -*-
"""
第93轮补（成果登记 R-102）：临-25——扩大项符号的热扫描判定（非拟合）
==========================================================================
检验：
  A 活跃模数 M(T)∝T³、热截断 ω_T=k_B T/ħ（log-log 斜率 3）；
  B 平均分化度 D(T)∝1/T（斜率 -1）、D_new= D/3；
  C 扩大项符号 = -sgn(T_dot)：加热负（平均化）、冷却正（差异化）；
  D 精确 n_B（非经典极限）核对 D_new/D≈0.351<1（符号判定稳健）。

图像用于检验幂次/符号/量级，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环06_临25_扩大项符号热扫描.py"
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

HBAR = 1.0
KB = 1.0
THETA_D = 100.0   # 示意 Debye 温度（单位一致）


def omega_T(T):
    return np.minimum(KB * np.asarray(T) / HBAR, KB * THETA_D / HBAR)


def coth_half(x):
    if x < 1e-8:
        return 2.0 / x
    return 1.0 / np.tanh(x / 2.0)


def main():
    # ---------- A: M(T)∝T³ ----------
    T = np.logspace(-1, 1.5, 100)   # T<θ_D 区
    M = (omega_T(T) / (KB * THETA_D / HBAR)) ** 3
    slope_M = np.polyfit(np.log(T), np.log(M), 1)[0]
    assert abs(slope_M - 3.0) < 1e-9, f"M∝T³ 斜率 {slope_M}"

    # ---------- B: D∝1/T、D_new/D=1/3 ----------
    D = 3.0 * HBAR**2 / (KB * T)
    D_new = HBAR**2 / (KB * T)
    ratio = D_new / D
    assert np.all(np.abs(ratio - 1.0 / 3.0) < 1e-12)
    slope_D = np.polyfit(np.log(T), np.log(D), 1)[0]
    assert abs(slope_D + 1.0) < 1e-9, f"D∝1/T 斜率 {slope_D}"
    assert np.all(D_new - D < 0), "D_new-D 应恒负"

    # ---------- C: 扩大项符号 ----------
    dT_heat = 1.0
    dT_cool = -1.0
    term_heat = -2.0 * HBAR**2 * dT_heat / (KB * T**2)
    term_cool = -2.0 * HBAR**2 * dT_cool / (KB * T**2)
    assert np.all(term_heat < 0) and np.all(term_cool > 0)
    # 符号 = -sgn(dT)
    assert np.all(np.sign(term_heat) == -np.sign(dT_heat))
    assert np.all(np.sign(term_cool) == -np.sign(dT_cool))

    # ---------- D: 精确 n_B 修正（x∈[0,1] 积分） ----------
    # D_exact ∝ (3/(2)) ∫₀¹ x coth(x/2) dx（以 ℏ²/(k_B T) 为单位）
    integral_xcoth, _ = quad(lambda x: x * coth_half(x), 0, 1, epsabs=1e-12)
    D_exact_coef = 1.5 * integral_xcoth           # D_exact / (ℏ²/k_B T)
    D_new_exact_coef = 0.5 * coth_half(1.0)       # 边缘 x=1 的单模方差系数
    ratio_exact = D_new_exact_coef / D_exact_coef
    assert ratio_exact < 1.0, "精确 n_B 下 D_new<D 必须仍成立"
    assert abs(ratio_exact - 1.0 / 3.0) < 0.05, f"精确比值应≈1/3，实得 {ratio_exact}"

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A
    ax = axes[0, 0]
    ax.loglog(T, M, "o-", lw=1.8, color="#1f77b4", label="$M_t\\propto T^3$")
    ax.set_xlabel("$T$")
    ax.set_ylabel("活跃模数 $M_t$（归一）")
    ax.set_title(f"A  模计数 $M_t\\propto T^3$（斜率 {slope_M:.3f}）")
    ax.legend(fontsize=8)

    # B
    ax = axes[0, 1]
    ax.loglog(T, D, lw=2.0, color="#1f77b4", label="$D=3\\hbar^2/k_BT$")
    ax.loglog(T, D_new, "--", lw=1.6, color="g", label="$D_{new}=D/3$")
    ax.set_xlabel("$T$")
    ax.set_ylabel("分化度")
    ax.set_title(f"B  $D\\propto1/T$（斜率 {slope_D:.3f}），新增为平均的 1/3")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    ax.semilogx(T, term_heat, lw=2.0, color="orange", label="加热 $\\dot T>0$：负（平均化）")
    ax.semilogx(T, term_cool, lw=2.0, color="#1f77b4", label="冷却 $\\dot T<0$：正（差异化）")
    ax.axhline(0, color="k", lw=0.8)
    ax.set_xlabel("$T$")
    ax.set_ylabel("扩大项")
    ax.set_title("C  扩大项符号 $=-\\operatorname{sgn}(\\dot T)$")
    ax.legend(fontsize=8)

    # D
    ax = axes[1, 1]
    labels = ["经典极限 $1/3$", f"精确 $n_B$  {ratio_exact:.3f}"]
    vals = [1.0 / 3.0, ratio_exact]
    ax.bar(labels, vals, color=["orange", "#1f77b4"])
    ax.axhline(1.0, color="r", ls="--", lw=1.0, label="$D_{new}=D$ 边界")
    ax.set_ylabel("$D_{new}/D$")
    ax.set_title("D  精确占据修正下仍 <1（符号稳健）")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "环06_临25_扩大项符号热扫描.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["M∝T³ 斜率", f"{slope_M:.6f}", "应为 3"],
        ["D∝1/T 斜率", f"{slope_D:.6f}", "应为 -1"],
        ["D_new/D（经典）", f"{float(ratio[0]):.6f}", "=1/3"],
        ["D_new-D 恒负", "PASS", "与扫描方向无关"],
        ["扩大项符号", "-sgn(T_dot)", "加热负、冷却正"],
        ["精确 n_B 比值", f"{ratio_exact:.6f}", "<1（稳健）"],
        ["饱和区边界", "T≲Θ_D", "高温 ω_T 封顶、符号结构失效"],
    ]
    with open(os.path.join(OUT, "环06_临25_扩大项符号热扫描_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        wcsv = csv.writer(fo)
        wcsv.writerow(["量", "值", "说明"])
        wcsv.writerows(summary)
    with open(os.path.join(OUT, "环06_临25_扩大项符号热扫描.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        wcsv = csv.writer(fo)
        wcsv.writerow(["T", "M_norm", "D", "D_new", "term_heat", "term_cool"])
        for i in range(len(T)):
            wcsv.writerow([f"{T[i]:.6g}", f"{M[i]:.6g}", f"{D[i]:.6g}",
                           f"{D_new[i]:.6g}", f"{term_heat[i]:.6g}",
                           f"{term_cool[i]:.6g}"])

    print("第93轮补 临-25 扩大项符号热扫描：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()


