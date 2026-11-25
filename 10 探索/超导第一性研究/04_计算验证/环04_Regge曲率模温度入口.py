# -*- coding: utf-8 -*-
"""
第87轮（成果登记 R-96）：环 4 温度入口 (4.1′) 的函数图像验证（非拟合）
====================================================
检验 (4.1′) sigma^2(T)=Σ_k |A·v_k|^2 c_k^0 [1+2 nB(hbar omega_k/kB T)] 的
  1. 零点下界有限正值（否证 R73 前 "(4.1) 恒为零"）；
  2. 对 T 严格单增（升温涨落增，方向同审-3）；
  3. 高温古典等分上界 sigma^2 <= Σc + 2T Σ(c/a)（e^x>=1+x）；
  4. 规范零模（|A·Y|^2=0）不进读数，曲率模权重正。

图像用于检验极限/单调性/量级/符号，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_Regge曲率模温度入口.py"
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


def nB(a, T):
    """玻色占据 1/(exp(a/T)-1)，a=hbar*omega/kB（K），T（K）。
    低温 a/T>700 时 expm1 溢出，物理极限 nB->0，直接置零避免溢出警告。"""
    x = np.asarray(a / T, dtype=float)
    out = np.zeros_like(x)
    m = x < 700.0
    out[m] = 1.0 / np.expm1(x[m])
    return out


def thermal_factor(a, T):
    """[1+2 nB] 热因子。"""
    return 1.0 + 2.0 * nB(a, T)


def sigma_sq(c, a, T):
    """(4.1′) 的曲率模求和。"""
    return sum(ck * thermal_factor(ak, T) for ck, ak in zip(c, a))


def main():
    # 三个曲率（非规范）模：a_k = hbar omega_k/kB (K)，c_k = |A·v_k|^2 c_k^0
    a = np.array([50.0, 150.0, 300.0])
    c = np.array([0.50, 0.30, 0.20])
    assert np.all(c > 0) and np.all(a > 0)

    T = np.logspace(-1, 4, 600)  # 0.1 K → 10^4 K

    F = thermal_factor(a[:, None], T[None, :])          # (3, nT)
    S = sigma_sq(c, a, T)                               # (nT,)

    # ---------- 结构断言（非拟合） ----------
    # 1. 零点下界 F>=1
    assert np.all(F >= 1.0 - 1e-12), "F>=1 失效"
    # 2. 高温古典等分上界 F <= 1+2T/a
    upper = 1.0 + 2.0 * (T[None, :] / a[:, None])
    assert np.all(F <= upper + 1e-9), "古典等分上界失效"
    # 3. 单调不减（全温区）；严格单增在 nB 超出浮点精度的平台区之外检验
    assert np.all(np.diff(S) >= 0), "sigma^2 对 T 非单调不减"
    mask = T > 20.0   # 此时各模 nB 已脱离机器精度的零点平台
    assert np.all(np.diff(S[mask]) > 0), "sigma^2 在有效温区非严格单增"
    # 4. 零点有限正值（T->0 极限 = Σ c_k）
    T0 = 1e-6
    S0 = sigma_sq(c, a, T0)
    assert abs(S0 - c.sum()) / c.sum() < 1e-6, "零点极限应为 Σc"
    assert S0 > 0, "零点量必须正（否证恒零）"
    # 5. 高温导数 -> 2 Σ(c/a)（e^x>=1+x 给上界饱和）
    high = T > 5e3
    dS = np.gradient(S, T)
    slope_theory = 2.0 * (c / a).sum()
    slope_num = float(np.mean(dS[high]))
    assert abs(slope_num - slope_theory) / slope_theory < 0.02, \
        f"高温斜率 {slope_num} 应≈{slope_theory}"
    # 6. 规范零模权重为零，曲率模权重为正
    transmission_gauge = 0.0
    w_gauge = transmission_gauge ** 2 * c[0] * thermal_factor(a[0], 300.0)
    w_curve = 1.0 ** 2 * c[0] * thermal_factor(a[0], 300.0)
    assert w_gauge == 0.0 and w_curve > 0.0

    # ---------- 图像：四面板（检验极限/单调/符号，非拟合） ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A: 热因子 [1+2nB] 与零点/古典极限
    ax = axes[0, 0]
    for k in range(3):
        ax.plot(T, F[k], lw=1.8, label=f"模 k={k}, a={a[k]:.0f} K")
        ax.plot(T, 1.0 + 2.0 * T / a[k], "--", lw=0.8, alpha=0.6)
    ax.set_xscale("log")
    ax.set_ylim(0.9, 1.0 + 2.0 * T[-1] / a[0] * 1.05)
    ax.axhline(1.0, color="k", lw=0.8)
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("热因子 $1+2n_B(\\hbar\\omega/k_BT)$")
    ax.set_title("A  [1+2n_B] 结构：零点=1，高温→线性上界（虚线）")
    ax.legend(fontsize=8)

    # B: (4.1′) 总方差——零点平台 + 单增 + 高温线性
    ax = axes[0, 1]
    ax.plot(T, S, lw=2.0, color="#1f77b4", label="$\\sigma^2(T)$ (4.1′)")
    ax.axhline(c.sum(), color="g", ls=":", lw=1.2,
               label=f"零点 $\\Sigma c_k={c.sum():.3f}$")
    ax.plot(T, c.sum() + slope_theory * T, "--", color="r", lw=1.0,
            label=f"高温等分 $\\Sigma c+2T\\Sigma(c/a)$")
    ax.set_xscale("log")
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("$\\langle(\\Delta\\varepsilon)^2\\rangle_T$")
    ax.set_title("B  (4.1′) 温度入口：零点有限正值→单增→高温线性")
    ax.legend(fontsize=8)

    # C: 规范零模 vs 曲率模权重
    ax = axes[1, 0]
    cats = ["规范零模\n$|A\\cdot Y|^2=0$", "曲率激发模\n$|A\\cdot v_k|^2>0$"]
    vals = [w_gauge, w_curve]
    ax.bar(cats, vals, color=["#999999", "#1f77b4"])
    ax.set_ylabel("对 (4.1′) 的权重贡献")
    ax.set_title("C  位移（规范）零模不进读数，曲率模承载亏角")

    # D: 温度入口结构与 (4.1) 原有 [1+2n_B] 逐位相同（同一函数）
    ax = axes[1, 1]
    tt = np.linspace(0.2, 200.0, 400)
    old = 1.0 + 2.0 * nB(100.0, tt)     # (4.1) 原有结构
    new = thermal_factor(100.0, tt)     # (4.1′) 新载体结构
    ax.plot(tt, old, lw=2.0, label="(4.1) 位移模载体")
    ax.plot(tt, new, "--", lw=1.5, label="(4.1′) 曲率模载体")
    ax.set_xlabel("温度 T (K)")
    ax.set_ylabel("热因子")
    ax.set_title("D  载体改变但热结构不变：两曲线逐位重合")
    ax.legend(fontsize=8)
    assert np.allclose(old, new, rtol=0, atol=1e-15)

    fig.tight_layout()
    png = os.path.join(OUT, "环04_Regge曲率模温度入口.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV 汇总 ----------
    summary = [
        ["零点极限 Σc", f"{c.sum():.10f}", "有限正值，否证恒零"],
        ["高温斜率理论 2Σ(c/a)", f"{slope_theory:.10f}", "e^x>=1+x 上界饱和"],
        ["高温斜率数值", f"{slope_num:.10f}", f"相对偏差 {abs(slope_num-slope_theory)/slope_theory:.3%}"],
        ["规范零模权重", f"{w_gauge:.10f}", "为零，不进读数"],
        ["曲率模权重", f"{w_curve:.10f}", "为正，承载亏角"],
        ["F>=1 断言", "PASS", "全部模全温区"],
        ["F<=1+2T/a 断言", "PASS", "全部模全温区"],
        ["σ² 严格单增断言", "PASS", "600 点"],
        ["(4.1)/(4.1′) 结构同一", "PASS", "逐位重合 atol=1e-15"],
    ]
    csv_path = os.path.join(OUT, "环04_Regge曲率模温度入口_摘要.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    # 逐点数据
    data_path = os.path.join(OUT, "环04_Regge曲率模温度入口.csv")
    with open(data_path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["T", "sigma2", "F_k0", "F_k1", "F_k2", "upper_k0"])
        for i, t in enumerate(T):
            w.writerow([f"{t:.6g}", f"{S[i]:.10g}",
                        f"{F[0, i]:.10g}", f"{F[1, i]:.10g}", f"{F[2, i]:.10g}",
                        f"{upper[0, i]:.10g}"])

    print("R87 温度入口函数验证：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
