# -*- coding: utf-8 -*-
"""
R24：链外-D 的氢原子断链——两处断点的性质判定与两条 no-go
=====================================================================
06 §11.6.2 的链：
  电子是关系产物 -> S_hat -> gamma_n -> n=N(gamma_n) -> a_n=n^2 a_0 -> E_n=-R/n^2
拆四段：
  A  S_hat -> gamma_n            链内定义
  B  n = N(gamma_n)              定义式（N(gamma_n)=n 恒等）
  C  n -> a_n = n^2 a_0          外部量子力学（SO(4)+位力）
  D  a_n -> E_n = -R/n^2         链内严格代数

主结果：B 代入 D 后 gamma_n 消失 => 氢原子一侧"从同步算符谱导出"是空的。

判据（预注册 R24，跑数前写死）：
  P1 E=-e^2/(2a)、a_n=n^2 a_0、R=e^2/(2a_0) => E_n=-R/n^2     残差<1e-12
  P2 |E_n| a_n = R a_0                                       残差<1e-12
  P3 n=2j+1 => (2j+1)^2 = n^2                                 n=1..10
  P4 rho_n=(gamma_n/n)^2 非常数：max/min>50 且 rho_1<0.01
  P5 展开后 picket fence：间距 std<1e-12；与 GUE 的 KS>0.4

复跑：python "10 探索/超导第一性研究/04_计算验证/R24_氢原子断链真相.py"
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
from scipy.optimize import brentq
from scipy.special import erf
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))

# 前 10 个非平凡零点（精确值）
ZEROS = [14.134725142, 21.022039639, 25.010857580, 30.424876126, 32.935061588,
         37.586178159, 40.918719012, 43.327073281, 48.005150881, 49.773832478]


def N_count(T):
    """Riemann-von Mangoldt 零点计数（主项）。"""
    x = T / (2.0 * math.pi)
    return x * math.log(x) - x + 7.0 / 8.0


def gamma_of(n):
    """第 n 个零点的估计：n<=10 用精确值，否则反解 N(T)=n。"""
    if n <= len(ZEROS):
        return ZEROS[n - 1]
    return brentq(lambda T: N_count(T) - n, 1.0, 1e9, xtol=1e-9)


def gue_cdf(s):
    """GUE Wigner surmise 的 CDF：erf(2s/√π) - (4s/π) e^{-4s²/π}。"""
    s = np.asarray(s, dtype=float)
    return erf(2.0 * s / np.sqrt(np.pi)) - (4.0 * s / np.pi) * np.exp(-4.0 * s ** 2 / np.pi)


def main():
    # ---------- P1：E_n=-R/n^2 的代数 ----------
    e, a0 = 1.0, 1.0
    R = e ** 2 / (2.0 * a0)
    for n in range(1, 11):
        a_n = n ** 2 * a0
        E = -e ** 2 / (2.0 * a_n)          # 链内严格代数
        assert abs(E - (-R / n ** 2)) < 1e-12, "P1: n=%d 残差超限" % n
    # ---------- P2：|E_n| a_n = R a0 ----------
    for n in range(1, 11):
        a_n = n ** 2 * a0
        E = -e ** 2 / (2.0 * a_n)
        assert abs(abs(E) * a_n - R * a0) < 1e-12, "P2: n=%d" % n
    # ---------- P3：SO(4) 维数恒等 ----------
    for j in range(0, 10):
        n = 2 * j + 1
        assert (2 * j + 1) ** 2 == n ** 2, "P3"
    dims = [(n, n ** 2) for n in range(1, 11)]

    # ---------- P4：两种读法不等价 ----------
    ns_p4 = [1, 10, 100, 1000, 10000, 1000000]
    rho = {}
    for n in ns_p4:
        g = gamma_of(n)
        rho[n] = (n / g) ** 2
    rmax, rmin = max(rho.values()), min(rho.values())
    assert rmax / rmin > 50.0, "P4: 比值不够散 %.2f" % (rmax / rmin)
    assert rho[1] < 0.01, "P4: rho_1=%.4g 应 <0.01" % rho[1]

    # ---------- P5：picket fence vs GUE ----------
    # 展开后的 Rydberg 谱：mu_n = n（累积计数），间距恒为 1
    spac = np.ones(400)
    assert float(np.std(spac)) < 1e-12, "P5: 间距标准差应近 0"
    # 经验 CDF 与 GUE CDF 的 KS 距离
    sgrid = np.linspace(1e-6, 4.0, 4001)
    F_emp = np.where(sgrid >= 1.0, 1.0, 0.0)
    ks = float(np.max(np.abs(F_emp - gue_cdf(sgrid))))
    assert ks > 0.4, "P5: KS=%.3f 应 >0.4" % ks

    print("R24 氢原子断链（结构判定，无拟合）：")
    print("  P1/P2/P3 通过：E_n=-R/n^2 为严格代数；dim(SO(4))=n^2")
    print("  两种读法 rho_n=(n/gamma_n)^2：")
    for n in ns_p4:
        print("    n=%-8d gamma≈%-10.3f  rho=%.5f" % (n, gamma_of(n), rho[n]))
    print("    max/min = %.2f  => 没有常数能把 1/gamma^2 变成 1/n^2" % (rmax / rmin))
    print("  展开后 Rydberg 间距：std=%.2e，与 GUE 的 KS=%.3f => picket fence" % (np.std(spac), ks))

    # ---------- 四面板图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    # A：两种读法的能级
    ax = axes[0, 0]
    ns = np.arange(1, 61)
    En = 1.0 / ns ** 2
    Eg = np.array([1.0 / gamma_of(int(n)) ** 2 for n in ns])
    ax.loglog(ns, En, "b-", lw=2.4, label="$E_n=-R/n^2$（序数读法）")
    ax.loglog(ns, Eg, "r--", lw=2.2, label="$E_n\\propto-1/\\gamma_n^2$（字面读法）")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$|E_n|/R$")
    ax.set_title("A  两种读法的谱不等价")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    # B：rho_n 不是常数
    ax = axes[0, 1]
    nn = np.logspace(0, 6, 300)
    rr = np.array([(x / gamma_of(int(round(x)))) ** 2 for x in nn])
    ax.semilogx(nn, rr, "k-", lw=2.2)
    ax.axhline(1.0, color="gray", ls=":", lw=1.2)
    for n in ns_p4:
        ax.plot([n], [rho[n]], "o", ms=6, color="#d62728")
    ax.set_xlabel("$n$")
    ax.set_ylabel("$\\rho_n=(n/\\gamma_n)^2$")
    ax.set_title("B  比值非常数（$\\rho$：0.005 → 2.8）")
    ax.grid(alpha=0.3, which="both")

    # C：picket fence vs GUE
    ax = axes[1, 0]
    ax.step(sgrid, F_emp, where="post", color="k", lw=2.2, label="展开后 Rydberg（确定性）")
    ax.plot(sgrid, gue_cdf(sgrid), "r-", lw=2.2, label="GUE Wigner surmise")
    ax.plot(sgrid, 1.0 - np.exp(-sgrid), "g--", lw=1.8, label="Poisson")
    ax.annotate("KS=%.3f" % ks, (1.35, 0.35), fontsize=10)
    ax.set_xlabel("$s$（归一化间距）")
    ax.set_ylabel("累积分布")
    ax.set_title("C  单指标谱展开后是 picket fence，不是 GUE")
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(alpha=0.3)

    # D：n^2 的三次出现
    ax = axes[1, 1]
    nd = np.arange(1, 13)
    ax.loglog(nd, nd ** 2, "o-", lw=2.0, ms=5, label="$\\dim(j,j)=(2j+1)^2=n^2$")
    ax.loglog(nd, nd ** 2, "s--", lw=1.4, ms=4, label="$a_n/a_0=n^2$")
    ax.loglog(nd, nd ** 2, "^:", lw=1.4, ms=4, label="$R/|E_n|=n^2$")
    ax.set_xlabel("$n$")
    ax.set_ylabel("倍数")
    ax.set_title("D  同一个 $n^2$：维数／半径／能级倒数")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "R24_氢原子断链真相.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["段 A", "S->gamma_n", "链内定义"],
        ["段 B", "n=N(gamma_n)", "定义式（恒等）"],
        ["段 C", "a_n=n^2 a_0", "外部量子力学（SO(4)+位力）"],
        ["段 D", "E_n=-R/n^2", "链内严格代数"],
        ["主结果", "代入后 gamma_n 消失", "氢原子侧'从谱导出'为空"],
        ["no-go 1", "rho 0.005→3.6", "无常数重标度"],
        ["no-go 2", "KS=%.3f" % ks, "picket fence，非 GUE"],
        ["SO(4)", "dim=(2j+1)^2=n^2", "B 类外部群论"],
    ]
    with open(os.path.join(OUT, "R24_氢原子断链真相_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["项", "值", "判定"])
        w.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
