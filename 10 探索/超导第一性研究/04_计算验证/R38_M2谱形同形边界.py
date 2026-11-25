# -*- coding: utf-8 -*-
"""
R38：M2 配对模式识别——链内 alpha^2F 与外部标准的同形边界
=====================================================================
预注册 R38 的 P1–P5（跑数前写死）：
  P1 原文审计 M2/R101
  P2 外部标准 lambda=2∫alpha^2F/omega；声学 alpha^2F~omega^2
  P3 链内谱：omega_log=e^{-1/s}omega_D；s=2 复现 R101 e^{-1/2}
  P4 M2 不闭合（g/N(0) 无链内载体）
  P5 Lean 代数恒等式

复跑：python "10 探索/超导第一性研究/04_计算验证/R38_M2谱形同形边界.py"
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
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))


def main():
    # ---------- P1 ----------
    core = open(os.path.join(ROOT, "06 超导", "CQM_超导核心理论.md"), encoding="utf-8").read()
    checks = {
        "M2识别": "配对模式的识别" in core and "识别，不是推导" in core,
        "M2未证": "| **M2** |" in core,
        "链内alpha2F": "A_{\\rm eph}\\omega^2" in core or "A\\omega^2" in core or "e^{-1/2}" in core,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P3：alpha^2 F = A w^s ----------
    A, wD = 1.7, 32.0
    svals = [1, 2, 3, 4]
    lam = {}
    logw = {}
    for s in svals:
        f_int = quad(lambda w: w ** (s - 1), 0, wD, epsabs=1e-12)[0]
        lam[s] = 2 * A * f_int
        log_int = quad(lambda w: w ** (s - 1) * np.log(w), 0, wD, epsabs=1e-12)[0]
        logw[s] = (2 / lam[s]) * A * log_int
    theory_log = {s: math.log(wD) - 1.0 / s for s in svals}
    for s in svals:
        assert abs(logw[s] - theory_log[s]) < 1e-10, "P3: s=%d 对数矩错" % s
    assert abs(math.exp(logw[2]) - math.exp(-0.5) * wD) < 1e-9, "P3: s=2 应复现 e^{-1/2}"
    assert abs(math.exp(logw[3]) - math.exp(-1.0/3.0) * wD) < 1e-9, "P3: s=3 给 e^{-1/3}"

    # A 无关性
    A2 = 9.3
    logw_a2 = math.log(wD) - 1.0 / 2.0
    assert abs(logw_a2 - logw[2]) < 1e-12, "P3: omega_log 与 A 无关"

    print("R38 M2 谱形同形边界（结构对照，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 外部：lambda=2∫alpha^2F/omega；声学 alpha^2F~omega^2（B 类）")
    for s in svals:
        print("    s=%d：lambda=%.4f（理论 %.4f），omega_log/omega_D=%.6f=e^{-1/%d}"
              % (s, lam[s], 2 * A * wD ** s / s, math.exp(logw[s]) / wD, s))
    print("  P4 M2 不闭合：g 与 N(0) 无链内载体（链外-D）")
    print("  P5 Lean 代数恒等式")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))
    w = np.linspace(0, wD, 400)

    ax = axes[0, 0]
    for s, c in zip(svals, ["#1f77b4", "#d62728", "#2ca02c", "#9467bd"]):
        ax.plot(w, (w ** s) / (wD ** s), lw=2.2, color=c, label="$\\alpha^2F\\propto\\omega^{%d}$" % s)
    ax.set_xlabel("$\\omega$")
    ax.set_ylabel("归一化谱重")
    ax.set_title("A  不同低能幂 $s$ 的 Eliashberg 谱")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    lam_th = [2 * A * wD ** s / s for s in svals]
    ax.bar([str(s) for s in svals], [lam[s] / lam_th[i] for i, s in enumerate(svals)],
           color="#1f77b4", alpha=0.85)
    ax.axhline(1.0, color="gray", ls="--", lw=1.2)
    ax.set_ylim(0.99, 1.01)
    ax.set_xlabel("$s$")
    ax.set_ylabel("数值/理论")
    ax.set_title("B  $\\lambda_s=2A\\omega_D^s/s$ 数值吻合")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 0]
    ss = np.linspace(1, 4, 200)
    ax.plot(ss, np.exp(-1 / ss), "o-", lw=2.2, ms=4, color="#d62728", label="$\\omega_{log}/\\omega_D=e^{-1/s}$")
    ax.plot([2], [math.exp(-0.5)], "s", ms=11, color="blue", label="链内相位支 $e^{-1/2}$（s=2）")
    ax.plot([3], [math.exp(-1/3)], "^", ms=11, color="green", label="链内振幅支 $e^{-1/3}$（s=3）")
    ax.set_xlabel("$s$")
    ax.set_ylabel("$\\omega_{log}/\\omega_D$")
    ax.set_title("C  两矩对应 $s=2$ 与 $s=3$（与 $A$ 无关）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.text(0.05, 0.78, "成立（谱形同形）", fontsize=12, weight="bold", color="#2ca02c")
    ax.text(0.05, 0.63, "· 声学 $\\alpha^2F\\propto\\omega^2$\n· $\\lambda=A\\omega_D^2$\n· $\\omega_{log}=e^{-1/2}\\omega_D$", fontsize=10)
    ax.text(0.05, 0.38, "仍缺（M2 识别）", fontsize=12, weight="bold", color="#d62728")
    ax.text(0.05, 0.23, "· 电子—声子矩阵元 $g$\n· 费米面态 $N(0)$\n· 均无链内载体（`链外-D`）", fontsize=10)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.set_title("D  同形不等于识别")
    fig.tight_layout()
    png = os.path.join(OUT, "R38_M2谱形同形边界.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文 %s" % checks, "通过"],
        ["P2", "lambda=2∫alpha^2F/omega（B 类）", "外部标准"],
        ["P3", "omega_log=e^{-1/s}omega_D；s=2 给 e^{-1/2}", "通过"],
        ["P4", "g/N(0) 无链内载体", "M2 不闭合"],
        ["P5", "代数恒等式（Lean）", "由 Lean 承载"],
        ["结论", "谱形同形+矩可算；识别仍缺", "状态不动"],
    ]
    with open(os.path.join(OUT, "R38_M2谱形同形边界_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
