# -*- coding: utf-8 -*-
"""
R32：临-6 通量归一两种读法的对象辨析
=====================================================================
预注册 R32 的 P1–P5（跑数前写死）：
  P1 原文审计 L469/L451/L471
  P2 外部标准 Phi0(q)=h/q；绕数 n => 总通量 n*Phi0
  P3 两读法对象不同：总通量 ∝ n vs 单位量子 ∝ 1/n；乘积 = 1
  P4 换算因子 n^2/4 依赖未知 q(n) 映射
  P5 Lean 互逆恒等式

复跑：python "10 探索/超导第一性研究/04_计算验证/R32_临6通量归一对象辨析.py"
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
    # ---------- P1：原文审计 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    checks = {
        "绕数读": "n 个磁通量子 $h/2e$" in chain or "n\\,h/2e" in chain,
        "2/n读": "\\frac{\\Phi_n}{\\Phi_2}=\\frac{2}{n}" in chain,
        "临-6自标": "换算未定，两式不擅自改号" in chain,
    }
    assert all(checks.values()), "P1: 原文审计失败 %s" % checks

    # ---------- P2/P3：两对象 ----------
    n = np.arange(2, 21, 2)
    k = n / 2.0
    total_ratio = k                 # 绕数读：总通量 n*h/2e / (h/2e) = n/2
    charge_ratio = 2.0 / n          # 荷量子归一读：h/(ne) / h/(2e) = 2/n
    assert np.all(total_ratio >= 1) and np.all(charge_ratio <= 1), "P3: 方向应相反"
    prod = total_ratio * charge_ratio
    assert np.max(np.abs(prod - 1.0)) < 1e-12, "P3: 应互为倒数"

    # 外部标准：Phi0(q)=h/q
    q_over_e = n.astype(float)       # q = n e
    phi0_charge = 1.0 / q_over_e     # h/(ne) 归一化
    total_flux = n.astype(float)     # n 个 h/2e
    assert abs(phi0_charge[0] - 0.5) < 1e-12, "P2: n=2 给 h/(2e)"

    # ---------- P4：换算因子 ----------
    conv = n.astype(float) ** 2 / 4.0
    # 两种候选映射给不同比值
    ratio_if_pair = total_ratio          # q(n)=2e
    ratio_if_cluster = charge_ratio      # q(n)=ne
    assert np.max(np.abs(ratio_if_pair - ratio_if_cluster)) > 1, "P4: 两映射应给不同比值"
    assert abs(conv[0] - 1.0) < 1e-12 and conv[-1] > 1, "P4: 换算因子随 n 变"

    print("R32 临-6 通量归一对象辨析（结构判定，无拟合）：")
    print("  P1 原文：%s" % checks)
    print("  P2 外部：Phi0(q)=h/q；绕数 n 给总通量 n*Phi0")
    print("  P3 两对象：总通量比 = n/2（升）；单位量子比 = 2/n（降）；乘积恒为 %.1f" % prod[0])
    print("  P4 换算因子 n^2/4：n=2 为 1、n=20 为 %.0f；依赖未知 q(n) 映射" % conv[-1])
    print("  P5 Lean 互逆恒等式")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(n, total_ratio, "b-o", lw=2.2, ms=5, label="绕数读：$\\Phi_n/\\Phi_2=n/2$（总通量）")
    ax.plot(n, charge_ratio, "r-s", lw=2.2, ms=5, label="荷量子读：$\\Phi_n/\\Phi_2=2/n$（单位量子）")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$\\Phi_n/\\Phi_2$")
    ax.set_title("A  一升一降：不是同一对象")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(n, prod, "k-o", lw=2.2, ms=5)
    ax.axhline(1.0, color="gray", ls="--", lw=1.2)
    ax.set_ylim(0.95, 1.05)
    ax.set_xlabel("$n$")
    ax.set_ylabel("$(n/2)\\cdot(2/n)$")
    ax.set_title("B  两读法互为倒数（乘积恒为 1）")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.loglog(q_over_e, phi0_charge, "r--", lw=2.2, label="单位量子 $h/(ne)\\propto1/n$")
    ax.loglog(q_over_e, total_flux, "b-", lw=2.2, label="$n$ 个 $h/2e\\propto n$")
    ax.set_xlabel("电荷标签 $q/e$")
    ax.set_ylabel("通量（归一化）")
    ax.set_title("C  外部标准：$\\Phi_0(q)=h/q$；总量 $=n\\Phi_0$")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1, 1]
    ax.plot(n, conv, "m-o", lw=2.2, ms=5)
    ax.set_yscale("log")
    ax.set_xlabel("$n$")
    ax.set_ylabel("换算因子 $n^2/4$")
    ax.set_title("D  缺的是 $n_{\\zeta}\\mapsto q(n)$ 映射（$\\Phi$ 不能被确定）")
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R32_临6通量归一对象辨析.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "原文三处 %s" % checks, "通过"],
        ["P2", "Phi0(q)=h/q；n*Phi0", "外部标准（B 类）"],
        ["P3", "n/2 升 vs 2/n 降；乘积 = 1", "对象不同"],
        ["P4", "换算因子 n^2/4 依赖 q(n) 映射", "换算仍缺"],
        ["P5", "互逆恒等式（Lean）", "由 Lean 承载"],
        ["结论", "方向相反=对象混淆；临-6 不闭合", "状态不动"],
    ]
    with open(os.path.join(OUT, "R32_临6通量归一对象辨析_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
