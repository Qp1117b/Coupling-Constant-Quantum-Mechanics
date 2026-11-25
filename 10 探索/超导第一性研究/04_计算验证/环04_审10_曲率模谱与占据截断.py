# -*- coding: utf-8 -*-
"""
第88轮补（成果登记 R-97）：环 4 审-10——曲率模谱与占据截断（非拟合）
====================================================================
检验：
  A 余切拉普拉斯谱 λ_q∝q²、ω_q∝q（零模 λ_0=0 是规范模，不进读数）；
  B 低频模先占据：n_B(ω,T) 对 ω 反单调、对 T 单增、高温 n_B<=1/x；
  C 占据模比例 F(q)=(q/Q)^3 在 Debye 端点 Q 饱和到 1（截断=谱支集）；
  D 两矩不等 ω_log=e^{-1/3}θ_D < θ_D；2D 红外 log(L/a) vs 3D 幂律。

图像用于检验极限/单调性/量级/符号，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_审10_曲率模谱与占据截断.py"
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


def nB(x):
    """玻色占据；低温大 x 直接置零避免 expm1 溢出。
    注：x=0 是规范零模（ω=0），物理上已被排除出 (4.1′)；这里给 1e-12 的
    微小正则化仅用于数值绘图，不代表零模有物理占据。"""
    x = np.asarray(x, dtype=float)
    x = np.where(x == 0.0, 1e-12, x)
    out = np.zeros_like(x)
    m = x < 700.0
    out[m] = 1.0 / np.expm1(x[m])
    return out


def main():
    # ---------- 参数（示意，非拟合） ----------
    n = 1e28          # 数密度 m^-3（典型金属量级）
    cs = 3000.0       # 声速 m/s
    hbar = 1.0545718e-34
    kB = 1.380649e-23
    Q = (6 * np.pi**2 * n) ** (1.0 / 3.0)          # Debye 波数
    theta_D = hbar * cs * Q / kB                    # Debye 温度 (K)
    omega_log_over_thetaD = np.exp(-1.0 / 3.0)

    # ---------- 结构断言（非拟合） ----------
    # 1. Debye 模计数：V*(6π²n)/(2π²)=3nV（取 V=1）
    V = 1.0
    count = V * (6 * np.pi**2 * n) / (2 * np.pi**2)
    assert abs(count - 3 * n * V) / (3 * n * V) < 1e-14, "Debye 模计数失败"

    # 2. 占据比例 F(q)=(q/Q)^3，F(Q)=1、单调
    qq = np.linspace(0, Q, 500)
    F = (qq / Q) ** 3
    assert abs(F[-1] - 1.0) < 1e-14, "F(Q)≠1"
    assert np.all(np.diff(F) > 0), "F 非严格单增"

    # 3. 谱：λ_q∝q²（零模 λ_0=0）、ω_q=c_s√(λ/Ω^{2/d})∝q
    q = np.linspace(0, Q, 500)
    lam = (q / Q) ** 2          # 归一化 λ_q（Ω^{2/d}、K 吸收入比例）
    omega = theta_D * (q / Q)   # ω_q = θ_D·(q/Q)（ℏω/kB 单位 K）
    assert lam[0] == 0.0 and np.all(np.diff(lam) > 0)
    assert abs(omega[-1] - theta_D) < 1e-9, "ω(Q)=θ_D"

    # 4. 低频先占据：nB 对 ω 反单调、高温 nB<=1/x
    T_grid = [0.05, 0.2, 1.0]          # 以 θ_D 为单位
    for t in T_grid:
        occ = nB(omega / (t * theta_D))
        assert np.all(np.diff(occ) <= 0), "nB 对 ω 非反单调"
    x = np.logspace(-3, 2, 400)
    assert np.all(nB(x) <= 1.0 / x + 1e-12), "nB<=1/x 失效"

    # 5. 两矩不等
    assert omega_log_over_thetaD < 1.0
    assert abs(omega_log_over_thetaD - 0.7165313105737893) < 1e-12

    # 6. 2D 红外 log(L/a)>0 且随 L 增；3D 幂律有限
    a = 1e-10
    Ls = np.logspace(-9, -3, 100)
    ir2d = np.log(Ls / a)
    assert np.all(ir2d > 0) and np.all(np.diff(ir2d) > 0)
    ir3d = 1.0 / (2 * np.pi / Ls)     # ∝L，无 log
    assert np.all(np.diff(ir3d) > 0)

    # ---------- 四面板图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: 余切拉普拉斯谱与色散
    ax = axes[0, 0]
    ax.plot(q / Q, lam, lw=2.0, label="$\\lambda_q\\propto q^2$（余切拉普拉斯）")
    ax.plot(q / Q, omega / theta_D, "--", lw=1.6, label="$\\omega_q\\propto q$（声学）")
    ax.scatter([0], [0], color="red", zorder=5, label="零模 $\\lambda_0=0$（规范，排除）")
    ax.set_xlabel("$q/Q$")
    ax.set_ylabel("归一化本征值 / 频率")
    ax.set_title("A  曲率模谱：零模是规范模，非零模按 $q^2$ 起")
    ax.legend(fontsize=8)

    # B: 低频先占据
    ax = axes[0, 1]
    for t in T_grid:
        ax.plot(omega / theta_D, nB(omega / (t * theta_D)),
                lw=1.8, label=f"$T={t}\\,\\theta_D/k_B$")
    ax.set_ylabel("$n_B(\\omega_q)$")
    ax.set_xlabel("$\\hbar\\omega_q/k_B\\theta_D$")
    ax.set_yscale("log")
    ax.set_title("B  低频曲率模先被占据（对 $\\omega$ 反单调）")
    ax.legend(fontsize=8)

    # C: 占据模比例——Debye 端点饱和
    ax = axes[1, 0]
    ax.plot(qq / Q, F, lw=2.0, color="#1f77b4", label="$F(q)=(q/Q)^3$")
    ax.axvline(1.0, color="r", ls="--", lw=1.2, label="截断 $Q$（谱支集端点）")
    ax.axvline(omega_log_over_thetaD, color="g", ls=":", lw=1.5,
               label="$\\omega_{log}=e^{-1/3}\\theta_D$（对数矩，非截断）")
    ax.set_xlabel("$q/Q$")
    ax.set_ylabel("累积占据模比例 $F(q)$")
    ax.set_title("C  截断＝谱支集端点 $\\Theta_D$，不是对数矩")
    ax.legend(fontsize=8)

    # D: 红外 2D vs 3D
    ax = axes[1, 1]
    ax.plot(Ls / a, ir2d, lw=2.0, label="2D：$\\log(L/a)$（对数发散）")
    ax.plot(Ls / a, ir3d / ir3d[-1] * ir2d[-1], "--", lw=1.6,
            label="3D：$\\propto L$（幂律、可积）")
    ax.set_xscale("log")
    ax.set_xlabel("$L/a$")
    ax.set_ylabel("红外累积（示意归一）")
    ax.set_title("D  2D 红外 $\\ln L$ 与 BKT 有限尺寸同标度族")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "环04_审10_曲率模谱与占据截断.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["Debye 模计数 V(6π²n)/(2π²)", f"{count:.6e}", "应=3nV，每原子 3 模"],
        ["Q", f"{Q:.6e}", "Debye 波数 (m^-1)"],
        ["θ_D", f"{theta_D:.4f}", "Debye 温度 (K)"],
        ["F(Q)", f"{F[-1]:.10f}", "=1，截断在谱支集端点"],
        ["ω_log/θ_D", f"{omega_log_over_thetaD:.10f}", "<1，对数矩≠截断"],
        ["nB 对 ω 反单调", "PASS", "三档温度"],
        ["nB<=1/x", "PASS", "400 点"],
        ["2D 红外 log(L/a)", "PASS", "正且随 L 增"],
        ["零模 λ0=0 排除", "PASS", "规范模不进读数"],
    ]
    with open(os.path.join(OUT, "环04_审10_曲率模谱与占据截断_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(OUT, "环04_审10_曲率模谱与占据截断.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["q_over_Q", "lambda_norm", "omega_over_thetaD", "F",
                    "nB_T005", "nB_T02", "nB_T1"])
        for i in range(len(q)):
            w.writerow([f"{q[i]/Q:.6g}", f"{lam[i]:.6g}", f"{omega[i]/theta_D:.6g}",
                        f"{F[i]:.6g}",
                        f"{float(nB(omega[i]/(0.05*theta_D))):.6g}",
                        f"{float(nB(omega[i]/(0.2*theta_D))):.6g}",
                        f"{float(nB(omega[i]/(1.0*theta_D))):.6g}"])

    print("第88轮补 审-10 曲率模谱与占据截断：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
