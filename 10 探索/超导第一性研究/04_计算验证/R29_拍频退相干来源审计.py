# -*- coding: utf-8 -*-
"""
R29：tau_dec ~ hbar/|lambda_m-lambda_n| 的来源审计
=====================================================================
预注册 R29 的 P1–P5（跑数前写死）：
  P1 确定两模拍频：|rho12(t)| 恒定（无衰减）
  P2 展宽包络：|C(t)|=|mean exp(-i d t/hbar)| 小 t 展开高斯，系数误差<1e-6
  P3 高模非零 ⇒ Tc 处 sigma>0、tau 有界；w4=0 才发散
  P4 恢复 tau~1/|Δλ| 需 sigma=kappa|Δλ|（kappa 外生）
  P5 Lean 承载结构 no-go

复跑：python "10 探索/超导第一性研究/04_计算验证/R29_拍频退相干来源审计.py"
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
hbar = 1.0   # 仅看结构，取 ħ=1


def main():
    # ---------- P1：确定两模无衰减 ----------
    t = np.linspace(0, 20, 4000)
    w1, w2, dlam = 0.7, 0.3, 0.45
    rho = math.sqrt(w1 * w2) * np.exp(-1j * dlam * t / hbar)
    amp = np.abs(rho)
    amp_dev = float(np.max(np.abs(amp - math.sqrt(w1 * w2))))
    assert amp_dev < 1e-12, "P1: 幅度应恒定，偏差 %.3g" % amp_dev

    # ---------- P2：展宽包络 ----------
    sigma = 0.35
    norm = sigma * math.sqrt(2 * math.pi)
    def envelope(tt):
        re = quad(lambda d: math.exp(-0.5 * (d / sigma) ** 2) * math.cos(d * tt / hbar),
                  -10 * sigma, 10 * sigma, epsabs=1e-13, epsrel=1e-13)[0]
        im = quad(lambda d: math.exp(-0.5 * (d / sigma) ** 2) * math.sin(d * tt / hbar),
                  -10 * sigma, 10 * sigma, epsabs=1e-13, epsrel=1e-13)[0]
        return math.hypot(re, im) / norm
    tsmall = 0.005
    c_num = envelope(tsmall)
    coef_num = (1.0 - c_num) / tsmall ** 2
    coef_exp = sigma ** 2 / (2 * hbar ** 2)
    rel = abs(coef_num - coef_exp) / coef_exp
    assert rel < 1e-6, "P2: 二阶系数相对误差 %.3g" % rel
    tau_1e = math.sqrt(2) * hbar / sigma

    # ---------- P3：高模非零 ⇒ sigma 不消失 ----------
    L4_minus_L1 = 20.0
    def sigma_pair(d, w4):
        ws = np.array([1.0 - w4, w4])
        ds = np.array([d, L4_minus_L1])
        p = ws / ws.sum()
        mean = float(np.sum(p * ds))
        var = float(np.sum(p * (ds - mean) ** 2))
        return math.sqrt(var)

    dgrid = np.linspace(0, 3, 400)
    sig_zero = np.array([sigma_pair(d, 0.0) for d in dgrid])
    sig_w4 = np.array([sigma_pair(d, 0.1) for d in dgrid])
    assert sig_zero[0] == 0.0, "P3: w4=0 时 Tc 处无展宽"
    assert sig_w4[0] > 0.0, "P3: w4>0 时 Tc 处仍有展宽"
    tau_w4_tc = math.sqrt(2) * hbar / sig_w4[0]
    assert math.isfinite(tau_w4_tc), "P3: tau 应有限"

    # ---------- P4：kappa 外生 ----------
    kappas = [0.2, 0.7]
    tau_curves = {k: np.array([math.sqrt(2) * hbar / (k * d) if d > 0 else np.inf
                               for d in dgrid[1:]]) for k in kappas}

    print("R29 拍频退相干来源审计（结构 no-go，无拟合）：")
    print("  P1 确定两模：|rho12| 恒为 %.3f，偏差 %.2e（无衰减）" % (math.sqrt(w1 * w2), amp_dev))
    print("  P2 展宽包络：小 t 展开相对误差 %.2e；tau_1/e=sqrt(2)hbar/sigma=%.3f" % (rel, tau_1e))
    print("  P3 w4=0：sigma(Tc)=0；w4=0.1：sigma(Tc)=%.3f ⇒ tau(Tc)=%.3f（有限）" % (sig_w4[0], tau_w4_tc))
    print("  P4 恢复 tau~1/|Δλ| 需 sigma=kappa|Δλ|；kappa=%.1f/%.1f 给不同曲线（外生）" % tuple(kappas))

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(t, np.real(rho), "b-", lw=1.8, label="$\\mathrm{Re}\\,\\rho_{12}(t)$（振荡）")
    ax.plot(t, amp, "r--", lw=2.4, label="$|\\rho_{12}(t)|$（恒定）")
    ax.set_xlabel("$t$")
    ax.set_ylabel("相干项")
    ax.set_title("A  单一确定拍频：相位振荡，但相干幅度不衰减")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    tt = np.linspace(0, 6, 300)
    c_num_curve = np.array([envelope(v) for v in tt])
    ax.plot(tt, c_num_curve, "k-", lw=2.4, label="系综平均 $|\\overline{e^{-i\\Delta\\lambda t/\\hbar}}|$")
    ax.plot(tt, np.exp(-0.5 * (sigma * tt / hbar) ** 2), "r--", lw=2.0,
            label="高斯近似 $\\exp[-\\frac{1}{2}(\\sigma t/\\hbar)^2]$")
    ax.plot([tau_1e], [math.exp(-1)], "o", ms=8, color="b")
    ax.annotate("$\\tau_{1/e}=\\sqrt{2}\\hbar/\\sigma$", (tau_1e + 0.2, 0.55), fontsize=9)
    ax.set_xlabel("$t$")
    ax.set_ylabel("包络 $|C(t)|$")
    ax.set_title("B  展宽给 $T_2^*$ 型退相位（可逆）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(dgrid, sig_zero, "g-", lw=2.4, label="$w_4=0$（高模截断）")
    ax.plot(dgrid, sig_w4, "r--", lw=2.2, label="$w_4=0.1$（12.A3 压制但非零）")
    ax.plot([0], [sig_w4[0]], "o", ms=9, color="r")
    ax.annotate("$\\sigma(T_c)>0$ ⇒ $\\tau$ 有限", (0.35, 0.5), fontsize=9)
    ax.set_xlabel("$\\Delta\\lambda=|\\lambda_2-\\lambda_1|$")
    ax.set_ylabel("拍频展宽 $\\sigma$")
    ax.set_title("C  拍频消失 → 发散，须高模严格为零")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    for k, curve in tau_curves.items():
        ax.loglog(dgrid[1:], curve, lw=2.2, label="$\\kappa=%.1f$" % k)
    ax.set_xlabel("$\\Delta\\lambda$")
    ax.set_ylabel("$\\tau_{1/e}$")
    ax.set_title("D  $\\tau\\propto1/|\\Delta\\lambda|$ 需 $\\sigma=\\kappa|\\Delta\\lambda|$（$\\kappa$ 外生）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R29_拍频退相干来源审计.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "确定两模 |rho12| 恒定，偏差 %.2e" % amp_dev, "no-go 1"],
        ["P2", "展宽包络高斯，误差 %.2e；tau=%.3f" % (rel, tau_1e), "通过"],
        ["P3", "w4=0.1 ⇒ sigma(Tc)=%.3f，tau=%.3f 有限" % (sig_w4[0], tau_w4_tc), "no-go 3"],
        ["P4", "kappa=0.2/0.7 给不同 tau", "no-go 2（外生）"],
        ["P5", "结构 no-go（Lean）", "由 Lean 承载"],
        ["结论", "L1350 关系按字面不成立；登记替代结构", "状态不动"],
    ]
    with open(os.path.join(OUT, "R29_拍频退相干来源审计_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
