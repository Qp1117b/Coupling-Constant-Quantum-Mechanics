# -*- coding: utf-8 -*-
"""
R22：链外-B 载体辨析——相位刚度 w(T) 与超流密度 rho_s(T) 是两个温度函数
=====================================================================
核心命题（非拟合，结构判定）：
  相位扇区裸刚度  Upsilon(T)=Upsilon_0*w(T)，w(T)=2/wD^2 * int_0^wD w*tanh(w/2T) dw
    低温 w = 1 - (pi^2/3)(T/wD)^2 + O(T^4)  —— 幂律 T^2，Tc 处几乎不降。
  振幅扇区超流密度 rho_s(T)（准粒子耗竭）—— Tc 处归零，低温指数。
  故 Upsilon(T) 不能直接当 rho_s(T) 用；链外-B 的载体在振幅扇区（gap），不在相位扇区。

判据（跑数前写死）：
  P1 w(Tc) > 0.99（相位刚度在 Tc 几乎不降）
  P2 rho_s(Tc) < 0.02（准粒子型超流密度在 Tc 归零）
  P3 低温 1-w 与 1-rho_s 在对数图上斜率不同：d ln(1-w)/d ln t -> 2
  P4 lambda_L(t)/lambda_L(0)=1/sqrt(rho_s(t)) 在 t->1 发散（与 Upsilon 无关）

复跑：python "10 探索/超导第一性研究/04_计算验证/R22_链外B载体辨析.py"
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

# 典型材料尺度（外生，仅作图示；不进入链内结论）
WD = 300.0     # Debye 温度 (K)
TC = 10.0      # 临界温度 (K)


def w_phase(T):
    """相位扇区 (10B.1) 的精确 Debye 多模权重 w(T)。"""
    if T <= 0:
        return 1.0
    val = quad(lambda x: x * math.tanh(x / (2.0 * T)), 0.0, WD, limit=400,
               epsabs=1e-13, epsrel=1e-12)[0]
    return 2.0 * val / WD ** 2


def w_lowT(T):
    """(10B.5) 低温展开，用于斜率断言。"""
    return 1.0 - (math.pi ** 2 / 3.0) * (T / WD) ** 2


def rho_twofluid(t):
    """准粒子型（两流体）超流密度：1 - t^4，t=T/Tc。"""
    t = np.asarray(t, dtype=float)
    return np.clip(1.0 - t ** 4, 0.0, None)


def main():
    # P1：相位刚度在 Tc 几乎不降
    wTc = w_phase(TC)
    assert wTc > 0.99, "P1: w(Tc) 应 >0.99"
    # P2：准粒子型超流密度在 Tc 归零
    rTc = float(rho_twofluid(1.0))
    assert rTc < 0.02, "P2: rho_s(Tc) 应 <0.02"
    # P3：低温 1-w 的幂律斜率 -> 2
    ts = np.array([0.02, 0.05, 0.1, 0.2])
    one_minus_w = np.array([1.0 - w_phase(t * TC) for t in ts])
    slope_w = np.polyfit(np.log(ts), np.log(one_minus_w), 1)[0]
    assert abs(slope_w - 2.0) < 0.15, "P3: 1-w 的低温幂律斜率应约 2"
    # P4：lambda_L 由 rho_s 决定，t->1 发散
    lam = 1.0 / np.sqrt(np.clip(rho_twofluid(np.array([0.5, 0.9, 0.99])), 1e-12, None))
    assert lam[-1] > 5.0, "P4: lambda_L 在 t->1 应显著增大"

    print("R22 链外-B 载体辨析（结构判定，非拟合）：")
    print("  相位扇区 w(Tc=%.0fK; wD=%.0fK) = %.6f  (>0.99，几乎不降)" % (TC, WD, wTc))
    print("  振幅扇区 rho_s(Tc) = %.6f  (<0.02，准粒子耗竭归零)" % rTc)
    print("  低温 1-w 的 log-log 斜率 = %.3f  (幂律 T^2)" % slope_w)
    print("  lambda_L(0.99Tc)/lambda_L(0) = %.2f  (由 rho_s 决定，非 Upsilon)" % lam[-1])
    print("  判定：Upsilon(T) 与 rho_s(T) 不是同一温度函数；链外-B 载体在振幅扇区。")

    # ---- 四面板图 ----
    t = np.linspace(1e-3, 1.0, 400)
    T = t * TC
    wv = np.array([w_phase(x) for x in T])
    wlow = np.array([w_lowT(x) for x in T])
    rs = rho_twofluid(t)
    lam_ratio = 1.0 / np.sqrt(np.clip(rs, 1e-9, None))

    fig, axes = plt.subplots(2, 2, figsize=(12.5, 9.5))

    ax = axes[0, 0]
    ax.plot(t, wv, "b-", lw=2.4, label="相位扇区 $\\Upsilon(T)/\\Upsilon_0=w(T)$")
    ax.plot(t, rs, "r--", lw=2.4, label="振幅扇区 $\\rho_s(T)/\\rho_s(0)$")
    ax.axvline(1.0, color="gray", ls=":", lw=1)
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("归一化值")
    ax.set_title("A  两扇区温度律不同")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ts2 = np.linspace(0.02, 0.8, 200)
    omw = np.array([1.0 - w_phase(x * TC) for x in ts2])
    omr = 1.0 - rho_twofluid(ts2)
    ax.loglog(ts2, omw, "b-", lw=2.2, label="$1-w\\propto t^2$（相位涨落）")
    ax.loglog(ts2, np.clip(omr, 1e-12, None), "r--", lw=2.2,
              label="$1-\\rho_s\\propto t^4$（准粒子，两流体）")
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$1-$归一化值")
    ax.set_title("B  低温幂律不同（$T^2$ vs $T^4$）")
    ax.set_xscale("log")
    ax.set_xticks([0.02, 0.05, 0.1, 0.2, 0.5, 0.8])
    ax.set_xticklabels(["0.02", "0.05", "0.1", "0.2", "0.5", "0.8"])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 0]
    ax.plot(t, lam_ratio, "k-", lw=2.2)
    ax.set_xlabel("$t=T/T_c$")
    ax.set_ylabel("$\\lambda_L(t)/\\lambda_L(0)$")
    ax.set_ylim(0, 8)
    ax.set_title("C  穿透深度由 $\\rho_s$ 决定，$T_c$ 处发散")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.axis("off")
    ax.text(0.5, 0.92, "链外-B 的扇区归属", ha="center", fontsize=12, weight="bold")
    ax.text(0.5, 0.74, "相位扇区（环 19）", ha="center", fontsize=10, color="blue")
    ax.text(0.5, 0.64, "$F_{ph}[\\theta]$, $\\Upsilon_0 w(T)$", ha="center", fontsize=10)
    ax.text(0.5, 0.54, "$w(T)$ 幂律 $T^2$，$T_c$ 不消失", ha="center", fontsize=9, color="blue")
    ax.text(0.5, 0.40, "振幅扇区（C5 gap）", ha="center", fontsize=10, color="red")
    ax.text(0.5, 0.30, "$\\Delta(T)$，准粒子 $e^{-\\Delta/T}$", ha="center", fontsize=10)
    ax.text(0.5, 0.20, "$\\rho_s\\to0$ 于 $T_c$ → 主导 $\\lambda_L$", ha="center", fontsize=9, color="red")
    ax.text(0.5, 0.06, "结论：$\\Upsilon(T)\\ne\\rho_s(T)$；载体在振幅扇区", ha="center",
            fontsize=10, weight="bold", color="darkgreen")

    fig.tight_layout()
    png = os.path.join(OUT, "R22_链外B载体辨析.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["w(Tc)", "%.6f" % wTc, "相位扇区；>0.99，Tc 几乎不降"],
        ["rho_s(Tc)", "%.6f" % rTc, "振幅扇区；准粒子耗竭归零"],
        ["1-w 低温斜率", "%.3f" % slope_w, "幂律 T^2（相位涨落）"],
        ["lambda_L(0.99Tc)/lambda_L(0)", "%.2f" % lam[-1], "由 rho_s 决定，非 Upsilon"],
        ["判定", "Upsilon != rho_s", "链外-B 载体在振幅扇区（gap）"],
        ["类别", "A 类结构判定", "两流体/BCS 为 B 类工具；wD、Tc 外生"],
    ]
    with open(os.path.join(OUT, "R22_链外B载体辨析_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    print("图:", png)


if __name__ == "__main__":
    main()
