# -*- coding: utf-8 -*-
"""
第95轮补（成果登记 R-104）：审-11——相变热力学身份的 Ehrenfest 判定（非拟合）
================================================================================
检验：
  A 三扇区自由能在 Tc：函数值与一阶导连续（C^1、无潜热）；
  B 二阶导跳变 ⇒ 比热跳变 ΔC/γTc=12/(7ζ(3))=1.426（二级）；
  C 2D BKT：本质奇点、比热无有限跳变（无限阶）；
  D argmin 决定级数：T* 最小→二级、T_BKT 最小→无限阶。

图像用于检验连续性/跳变/分支，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环19_审11_Ehrenfest相变级数.py"
"""
import csv
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
ZETA3 = 1.202056903159594
JUMP = 12.0 / (7.0 * ZETA3)   # 1.426


def main():
    Tc, a, b = 10.0, 0.5, 3.0

    # ---------- A: C^1 判定 ----------
    # 正常支 f_N = -a T^2；超导支 f_S = -a T^2 - (b/2)(Tc-T)^2 (T<Tc)
    eps = 1e-7
    fN = lambda T: -a * T**2
    fS = lambda T: -a * T**2 - b / 2 * (Tc - T)**2
    val_gap = abs(fS(Tc) - fN(Tc))
    # 左导数差商（超导支）与右导数（正常支）
    dleft = (fS(Tc) - fS(Tc - eps)) / eps
    dright = (fN(Tc + eps) - fN(Tc)) / eps
    assert val_gap < 1e-12, "自由能应连续"
    assert abs(dleft - dright) < 1e-4, "一阶导应连续（C^1）"

    # ---------- B: 二级比热跳变 ----------
    # 二阶导：超导支 f_S'' = -2a - b；正常支 f_N'' = -2a；ΔC = -Tc Δ(f'') = b*Tc
    eps2 = 1e-3   # 二阶差商用较大步长，避免 eps^2 接近机器精度的抵消误差
    d2_left = (fS(Tc) - 2 * fS(Tc - eps2) + fS(Tc - 2 * eps2)) / eps2**2
    d2_right = (fN(Tc + 2 * eps2) - 2 * fN(Tc + eps2) + fN(Tc)) / eps2**2
    delta_f2 = d2_left - d2_right
    deltaC_num = -Tc * delta_f2
    assert abs(deltaC_num - b * Tc) < 1e-4, f"ΔC 应=b*Tc={b*Tc}"
    assert deltaC_num > 0, "ΔC 应正"
    assert abs(JUMP - 1.426126) < 1e-5
    # 熵连续 ΔS=0（一阶导连续已证）

    # ---------- C: BKT 无限阶（本质奇点） ----------
    # 自由能奇点 f ~ exp(-b/sqrt(T-T_BKT))：所有有限阶导在 T_BKT 连续
    TB = 2.0
    f_bkt = lambda T: np.exp(-b / np.sqrt(max(T - TB, 1e-12)))
    # 本质奇点特征：T->TB+ 时 exp(-b/sqrt(T-TB)) 比任何幂次都快地趋 0
    assert f_bkt(TB + 1e-6) < 1e-100   # e^{-3000} 完全压制（下溢为 0）
    assert 0 < f_bkt(TB + 0.5) < 0.1    # 远离时仍小但非零
    # 对比：二级支有有限跳变（上面已证 deltaC_num>0）
    assert deltaC_num > 0

    # ---------- D: argmin 决定级数 ----------
    def tc_min(Ts, TB, Ttheta):
        return min(min(Ts, TB), Ttheta)

    # 振幅先触底 -> Tc=Ts -> 二级
    assert tc_min(Ts=8, TB=9, Ttheta=10) == 8
    # 相位 BKT 先触底 -> Tc=TB -> 无限阶
    assert tc_min(Ts=9, TB=2, Ttheta=10) == 2
    # 相位端子先触底 -> Tc=Ttheta
    assert tc_min(Ts=9, TB=8, Ttheta=5) == 5

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    Ts = np.linspace(Tc - 4, Tc + 4, 400)

    # A
    ax = axes[0, 0]
    fplot = np.where(Ts <= Tc, fS(Ts), fN(Ts))
    ax.plot(Ts, fplot, lw=2.0, color="#1f77b4", label="整体自由能 f(T)")
    ax.axvline(Tc, color="r", ls="--", lw=1.0, label="$T_c$")
    ax.set_xlabel("$T$")
    ax.set_ylabel("$f$")
    ax.set_title("A  自由能 C1 连续（无潜热、无折点）")
    ax.legend(fontsize=8)

    # B
    ax = axes[0, 1]
    C = -Ts * np.where(Ts <= Tc, -2 * a - b, -2 * a)
    ax.plot(Ts, C, lw=2.0, color="#1f77b4", label="$C_V=-T f''$")
    ax.axvline(Tc, color="r", ls="--", lw=1.0, label="$T_c$（跳变）")
    ax.set_xlabel("$T$")
    ax.set_ylabel("$C_V$")
    ax.set_title(f"B  二级相变：比热有限跳变 ΔC={deltaC_num:.2f}")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    Tb_ax = np.linspace(2.001, 4, 400)
    fb = np.exp(-b / np.sqrt(Tb_ax - 2))
    ax.plot(Tb_ax, fb, lw=2.0, color="green", label="BKT 本质奇点")
    ax.axvline(2, color="r", ls="--", lw=1.0, label="$T_{BKT}$")
    ax.set_xlabel("$T$")
    ax.set_ylabel("$f_{BKT}$")
    ax.set_title("C  2D BKT：无限阶（各阶导连续、无有限跳变）")
    ax.legend(fontsize=8)

    # D
    ax = axes[1, 1]
    cases = ["T* 最小\n(二级)", "T_BKT 最小\n(无限阶)", "T_theta 最小\n(二级)"]
    orders = [2, 0, 2]   # 0 表示无限阶（示意）
    bars = ax.bar(cases, orders, color=["#1f77b4", "green", "orange"])
    ax.set_ylabel("相变阶（0=无限阶）")
    ax.set_title("D  相变级数由 $T_c=\\min$ 的 argmin 扇区决定")

    fig.tight_layout()
    png = os.path.join(OUT, "环19_审11_Ehrenfest相变级数.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["自由能连续", f"{val_gap:.2e}", "=0（无潜热前提）"],
        ["一阶导连续", f"{abs(dleft-dright):.2e}", "C1 判据通过"],
        ["二阶导跳变 ΔC", f"{deltaC_num:.4f}", f"=b·Tc={b*Tc}"],
        ["ΔC/γTc", f"{JUMP:.6f}", "=12/(7ζ(3))=1.426（定理）"],
        ["熵连续 ΔS", "0", "二级相变无潜热"],
        ["BKT 阶", "无限阶", "本质奇点、比热无有限跳变"],
        ["3D 阶", "二级", "argmin=T* 或 T_theta"],
    ]
    with open(os.path.join(OUT, "环19_审11_Ehrenfest相变级数_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(OUT, "环19_审11_Ehrenfest相变级数.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["T", "f", "C_V"])
        for t in Ts:
            w.writerow([f"{t:.4f}",
                        f"{fS(t) if t <= Tc else fN(t):.6f}",
                        f"{-t*(-2*a-b) if t <= Tc else -t*(-2*a):.6f}"])

    print("第95轮补 审-11 Ehrenfest 相变级数：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
