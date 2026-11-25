# -*- coding: utf-8 -*-
"""
第89轮补（成果登记 R-98）：审-11——自由能三扇区与比热跳变（非拟合）
====================================================================
检验：
  A 曲率热自由能 F=EZ-A*T^4 单减、光滑（锚的非解析性不来自热占据）；
  B Debye 热容 C∝T^3（低温）→ 3nkB（高温 Dulong-Petit）；
  C 凝聚能：T=0 为 -½N(0)Δ0²；近 T* 为二次律 ∝-(1-T/T*)²，
    与"错误线性律 -½N(0)Δ²(T)"对照（本轮关键订正）；
  D 比热跳变 ΔC/γT* = 12/(7ζ(3)) ≈ 1.43。

图像用于检验极限/单调性/幂次/符号，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环19_审11_自由能三扇区与比热跳变.py"
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


def debye_C(x):
    """归一化 Debye 热容 C/(3NkB)=3/x³ ∫₀ˣ t⁴eᵗ/(eᵗ-1)² dt。
    用 e^{-t} 形式避免大 x 时 e^t 溢出：t⁴e^{-t}/(1-e^{-t})²。"""
    if x < 1e-8:
        return 1.0  # 高温极限（x→0）Dulong–Petit

    def integrand(t):
        if t < 1e-8:
            return t * t            # t→0 极限 t⁴e^{-t}/(1-e^{-t})² → t²
        em = np.exp(-t)
        return t**4 * em / (1.0 - em)**2

    val, _ = quad(integrand, 0, x, limit=200)
    return 3.0 / x**3 * val


def main():
    # ---------- 参数（示意，非拟合） ----------
    thetaD = 300.0        # Debye 温度 (K)
    Tstar = 10.0          # 配对温度 (K)
    zeta3 = 1.202056903159594
    jump_ratio = 12.0 / (7.0 * zeta3)
    gamma_over_3NkB = 1.0  # 仅作归一化示意

    # ---------- A: 曲率热自由能 ----------
    T_f = np.linspace(1e-3, thetaD, 600)
    A_coef = 1.0
    EZ = 100.0
    F = EZ - A_coef * (T_f / thetaD)**4      # 归一化
    assert np.all(np.diff(F) <= 0), "F_curv 非单减"

    # ---------- B: Debye 热容 ----------
    T_c = thetaD * np.logspace(-2, 1.5, 60)           # 0.01θD ~ 31θD，覆盖两极限
    xs = thetaD / T_c
    C_ratio = np.array([debye_C(x) for x in xs])       # C/(3NkB)
    # 低温端 C ∝ T³：log-log 斜率应为 3
    low = T_c < 0.05 * thetaD
    slope = np.polyfit(np.log(T_c[low]), np.log(C_ratio[low]), 1)[0]
    assert abs(slope - 3.0) < 0.05, f"低温热容幂次应为 3，实得 {slope}"
    # 高温端 → 1（Dulong-Petit）
    assert abs(C_ratio[-1] - 1.0) < 0.02, "高温未趋 Dulong-Petit"

    # ---------- C: 凝聚能 ----------
    t = np.linspace(0, 1.2, 600)            # T/T*
    # GL-BCS 插值（标准插值，非链内第一性）
    fcond_interp = -(1.0 - t**2)**2          # 归一到 T=0 值 -1
    # 近 T* 二次渐近：4(1-t)²（插值展开）
    quad_asym = -4.0 * (1.0 - t)**2
    # 错误线性律：-½N(0)Δ²(T) 若误用于近 T* 会给 ∝-(1-t)
    wrong_linear = -(1.0 - t)
    near = (t > 0.9) & (t < 1.0)
    # 二次渐近在近区应远好于线性
    err_quad = np.mean(np.abs(fcond_interp[near] - quad_asym[near]))
    err_lin = np.mean(np.abs(fcond_interp[near] - wrong_linear[near]))
    assert err_quad < err_lin * 0.2, "近 T* 应为二次律而非线性律"
    # 指数核对：log|F| vs log(1-t) 斜率 ≈ 2（渐近只在近区有效，不用于低温）
    tt = np.linspace(0.999, 0.99999, 50)
    sl = np.polyfit(np.log(1 - tt), np.log(np.abs(-(1 - tt**2)**2)), 1)[0]
    assert abs(sl - 2.0) < 1e-3, f"近 T* 凝聚能幂次应为 2，实得 {sl}"
    # 解析局部指数：dln|F|/dln(1-t) = 4t/(1+t) → 2（t→1）
    tloc = 0.9999
    assert abs(4.0 * tloc / (1.0 + tloc) - 2.0) < 1e-3
    assert abs(jump_ratio - 1.426126) < 1e-5

    # ---------- 四面板图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A
    ax = axes[0, 0]
    ax.plot(T_f / thetaD, F, lw=2.0, color="#1f77b4")
    ax.set_xlabel("$T/\\Theta_D$")
    ax.set_ylabel("$F_{\\rm curv}$（归一）")
    ax.set_title("A  曲率热自由能：光滑 $T^4$，锚的非解析性不来自热占据")
    ax.legend(["$F=E_Z-AT^4$"], fontsize=9)

    # B
    ax = axes[0, 1]
    ax.plot(T_c / thetaD, C_ratio, lw=2.0, color="#1f77b4",
            label="Debye $C_V/(3Nk_B)$")
    ax.plot(T_c / thetaD, (T_c / thetaD)**3 / (T_c / thetaD)**3,
            ls=":", lw=0.8, color="gray")
    ax.set_xscale("log")
    ax.set_xlabel("$T/\\Theta_D$")
    ax.set_ylabel("$C_V/(3Nk_B)$")
    ax.set_ylim(0, 1.1)
    ax.set_title("B  Debye 热容：$T^3$ → Dulong–Petit（第88轮截断封顶）")
    ax.axhline(1.0, color="r", ls="--", lw=1.0, label="3Nk_B")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    ax.plot(t, fcond_interp, lw=2.2, color="#1f77b4",
            label="凝聚能（GL-BCS 插值）")
    ax.plot(t, quad_asym, "--", lw=1.6, color="g",
            label="近 $T^*$ 二次渐近 $-4(1-t)^2$")
    ax.plot(t, wrong_linear, ":", lw=1.5, color="r",
            label="错误线性律 $-½N(0)\\Delta^2(T)$")
    ax.axvline(1.0, color="k", ls="--", lw=0.8)
    ax.set_xlabel("$T/T^*$")
    ax.set_ylabel("$F_S-F_N$（归一）")
    ax.set_title("C  关键订正：近 $T^*$ 是二次律，不是 $T=0$ 的线性律")
    ax.legend(fontsize=8)

    # D
    ax = axes[1, 1]
    tD = np.linspace(0.8, 1.2, 300)
    # 示意：正常态 C_N=γT，超导态在 T* 处比热跳变 ΔC=1.43γT*
    CN = tD
    CS = np.where(tD < 1.0, CN + jump_ratio, CN)
    ax.plot(tD, CN, "--", lw=1.4, color="gray", label="正常态 $C_N=\\gamma T$")
    ax.plot(tD, CS, lw=2.2, color="#1f77b4", label="超导态 $C_S$")
    ax.axvline(1.0, color="r", ls="--", lw=1.0, label="$T^*$")
    ax.set_xlabel("$T/T^*$")
    ax.set_ylabel("$C/(\\gamma T^*)$（示意）")
    ax.set_title(f"D  比热跳变 $\\Delta C/\\gamma T^*=12/(7\\zeta_3)={jump_ratio:.3f}$")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "环19_审11_自由能三扇区与比热跳变.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["F_curv 单减", "PASS", "600 点，$F=E_Z-AT^4$"],
        ["低温热容幂次", f"{slope:.6f}", "应为 3（3D Debye）"],
        ["高温 Debye 归一", f"{C_ratio[-1]:.6f}", "→1（Dulong–Petit）"],
        ["近 T* 凝聚能幂次", f"{sl:.6f}", "应为 2（订正线性律之误）"],
        ["近区二次 vs 线性误差比", f"{err_quad/err_lin:.4f}", "<0.2，二次律胜出"],
        ["ΔC/γT*", f"{jump_ratio:.6f}", "12/(7ζ(3))≈1.43"],
        ["三扇区非解析性", "曲率光滑/相位锚/振幅跳变", "锚只给相位扇区、是 Tc 上界"],
    ]
    with open(os.path.join(OUT, "环19_审11_自由能三扇区与比热跳变_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(OUT, "环19_审11_自由能三扇区与比热跳变.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["T_over_Tstar", "F_cond_interp", "quad_asym", "wrong_linear"])
        for i in range(len(t)):
            w.writerow([f"{t[i]:.6g}", f"{fcond_interp[i]:.6g}",
                        f"{quad_asym[i]:.6g}", f"{wrong_linear[i]:.6g}"])

    print("第89轮补 审-11 自由能三扇区与比热跳变：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
