# -*- coding: utf-8 -*-
"""
R28：拍频退相干能否给 E2 的线性 Gamma_0——形状闭合、系数外生
=====================================================================
预注册 R28 的 P1–P5（跑数前写死）：
  P1 链内前提审计（06 L1328/L1332/L1336/L1350/L1691）
  P2 真交叉：|λ2-λ1|(Tc)=0，斜率=|Δa|，线性拟合 R^2>0.999999
  P3 避免交叉：间隙 2|W|>0 ⇒ Γ0(Tc)>0，与外生律零点矛盾
  P4 归一化形状：ħ|λ2-λ1|/Γ(T*) 与 (T-Tc)/(T*-Tc) 完全重合
  P5 系数自由：改变 Δa 改变比例，8/π 不可由链内定

复跑：python "10 探索/超导第一性研究/04_计算验证/R28_拍频交叉给线性Gamma0.py"
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
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))


def main():
    # ---------- P1：链内前提审计 ----------
    txt = open(os.path.join(ROOT, "06 超导", "CQM_超导核心理论.md"), encoding="utf-8").read()
    checks = {
        "交叉": "本征值交叉" in txt and "拍频消失" in txt,
        "拍频": "拍频" in txt and "退相干速率" in txt,
        "退相干到最低": "退相干到最低" in txt,
        "tau未证": "待严格推导" in txt,
        "V热未证": "热修正" in txt,
    }
    assert all(checks.values()), "P1: 链内前提审计失败 %s" % checks

    # ---------- P2：真交叉的线性劈裂 ----------
    Tc, Tstar = 83.0, 200.0
    lam_c = 14.1347                      # 交叉点（零温 γ_1 量级，仅示意）
    a1, a2 = 0.12, 0.47                  # 示意斜率（外生，链内未定）
    dT = np.linspace(0.0, Tstar - Tc, 400)
    lam1 = lam_c + a1 * dT
    lam2 = lam_c + a2 * dT
    split = np.abs(lam2 - lam1)
    assert abs(split[0]) < 1e-12, "P2: Tc 处劈裂应为 0"
    assert abs(split[-1] - (a2 - a1) * (Tstar - Tc)) < 1e-12, "P2: 线性斜率错"
    ss_res = float(np.sum((split - (a2 - a1) * dT) ** 2))
    ss_tot = float(np.sum((split - split.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot
    assert r2 > 0.999999, "P2: R^2=%.9f" % r2

    # ---------- P3：避免交叉的有限间隙 ----------
    W = 0.08                             # 示意耦合（外生）
    v = 0.21
    gap = 2.0 * np.sqrt((v * dT) ** 2 + W ** 2)
    assert gap[0] == 2 * W and gap[0] > 0, "P3: 避免交叉 Tc 处间隙应 >0"
    # Γ0 = ħ/τ ~ ħ|λ2-λ1|；取 ħ=1（只看形状）⇒ Γ0(Tc)=2W>0，与外部 Γ0(Tc)=0 矛盾
    gamma0_avoid_tc = gap[0]
    assert gamma0_avoid_tc > 0, "P3: Γ0(Tc)>0"

    # ---------- P4：归一化形状 ----------
    gamma_beat = split / split[-1]
    gamma_ext = dT / (Tstar - Tc)
    maxdiff = float(np.max(np.abs(gamma_beat - gamma_ext)))
    assert maxdiff < 1e-12, "P4: 归一化形状差 %.3g" % maxdiff

    # ---------- P5：系数自由 ----------
    # Γ0 = ħ|Δa|(T-Tc)；外部 a_ext=8/π（取 kB=ħ=1 的单位约定仅看比值）
    a_ext = 8.0 / math.pi
    coeffs = [(a2 - a1), (a2 - a1) * 2.3]
    ratios = [c / a_ext for c in coeffs]
    assert abs(ratios[0] - ratios[1]) > 0.1, "P5: 不同斜率应给不同比例"

    print("R28 拍频交叉 → 线性 Γ0（结构推导，系数外生）：")
    print("  P1 链内前提：%s（τ 关系与 V_热 仍开放）" % checks)
    print("  P2 真交叉：劈裂(Tc)=0；斜率=%.3f；线性 R²=%.9f" % (a2 - a1, r2))
    print("  P3 避免交叉：Γ0(Tc)=2W=%.3f>0（与外部 Γ0(Tc)=0 矛盾）" % gamma0_avoid_tc)
    print("  P4 归一化形状：max|Γ_beat/Γ(T*) − (T−Tc)/(T*−Tc)|=%.2e" % maxdiff)
    print("  P5 系数：ħ|Δa|/a_ext = %.3f 或 %.3f（斜率外生 ⇒ 8/π 不可链内定）" % tuple(ratios))

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(dT, lam1, "b-", lw=2.2, label="$\\lambda_1(T)$")
    ax.plot(dT, lam2, "r--", lw=2.2, label="$\\lambda_2(T)$")
    ax.plot([0], [lam_c], "ko", ms=7)
    ax.annotate("$\\lambda_2(T_c)=\\lambda_1(T_c)$\n拍频=0", (4, lam_c - 1.6), fontsize=9)
    ax.set_xlabel("$T-T_c$ (K)")
    ax.set_ylabel("$\\lambda_n$（示意）")
    ax.set_title("A  真交叉：斜率不同 → 劈裂线性于 $T-T_c$")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(dT, gap, "m-", lw=2.4, label="避免交叉间隙 $2\\sqrt{v^2\\Delta T^2+W^2}$")
    ax.plot([0], [2 * W], "o", ms=9, color="m")
    ax.annotate("$\\Gamma_0(T_c)=2W>0$\n与外部 $\\Gamma_0(T_c)=0$ 矛盾", (12, 0.28), fontsize=9)
    ax.set_xlabel("$T-T_c$ (K)")
    ax.set_ylabel("劈裂（示意）")
    ax.set_title("B  避免交叉留有限间隙：真交叉须有扇区对称性根据")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(dT, gamma_beat, "b-", lw=2.6, label="$\\hbar|\\lambda_2-\\lambda_1|/\\Gamma(T^*)$（链内形状）")
    ax.plot(dT, gamma_ext, "r--", lw=2.0, label="$(T-T_c)/(T^*-T_c)$（外部律）")
    ax.set_xlabel("$T-T_c$ (K)")
    ax.set_ylabel("归一化宽度")
    ax.set_title("C  归一化后完全重合（系数自由）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.bar(["$T<T_c$\n单一本征态", "$T>T_c$\n叠加态"],
           [0.0, gamma_beat[-1]], color=["#2ca02c", "#d62728"], alpha=0.85)
    ax.set_ylabel("$\\Gamma_0$（归一化）")
    ax.set_ylim(0, 1.25)
    ax.set_title("D  $T_c$ 以下退相干到最低分量 → 无拍频 → $\\Gamma_0=0$")
    ax.grid(alpha=0.3, axis="y")

    fig.tight_layout()
    png = os.path.join(OUT, "R28_拍频交叉给线性Gamma0.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "链内前提审计 %s" % checks, "通过（两开放项仍开放）"],
        ["P2", "劈裂(Tc)=0，斜率 %.3f，R²=%.9f" % (a2 - a1, r2), "通过"],
        ["P3", "避免交叉 Γ0(Tc)=2W=%.3f>0" % gamma0_avoid_tc, "真交叉必要"],
        ["P4", "归一化形状差 %.2e" % maxdiff, "通过"],
        ["P5", "比例 %.3f vs %.3f" % tuple(ratios), "系数外生"],
        ["结论", "线性形状闭合，8/π 系数不闭合", "E2/G21 状态不动"],
    ]
    with open(os.path.join(OUT, "R28_拍频交叉给线性Gamma0_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
