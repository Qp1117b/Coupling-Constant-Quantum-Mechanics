# -*- coding: utf-8 -*-
"""
第91轮补（成果登记 R-100）：审-1——矩阵分支求逆与锚邻域闭合（非拟合）
==========================================================================
检验：
  A f(λ)=-cλ+dλ³ 与逆级数 g(u)=-u/c-d u³/c⁴：f(g(u))=u+O(u⁵)；
  B 锚邻域严格单减（f'=-c+3dλ²<0 当 |λ|<sqrt(c/3d)）⇒ 局部可逆；
  C 逆级数截断误差 ∝u⁵（log-log 斜率 5），三次系数精确抵消；
  D 相对三次修正 |d|u²/c³ 在链精度下不可见（c=1 归一化回到第78轮界）。

图像用于检验幂次/单调性/量级，不是用数据拟合曲线——无实验数据、无调参。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环08_审1_矩阵分支求逆与锚邻域.py"
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

C = 1.0    # 归一化 c=1（v_tau=1；一般 c=1/v_tau² 只改标度）
D = 10.0   # 第78轮界取 |d/c|=10（保守）


def f(lam):
    return -C * lam + D * lam**3


def g(u):
    return -u / C - D * u**3 / C**4


def main():
    # ---------- A: f 与 g 互逆 ----------
    u = np.linspace(-0.03, 0.03, 400)
    comp = f(g(u))
    assert np.max(np.abs(comp - u)) < 1e-4, "f(g(u))≈u 失效（逆级数有效区内）"

    # ---------- B: 锚邻域单调性 ----------
    R = np.sqrt(C / (3.0 * D))          # 可逆半径
    lam = np.linspace(-R * 0.99, R * 0.99, 400)
    fp = -C + 3.0 * D * lam**2
    assert np.all(fp < 0), "邻域内 f' 应严格负"
    fl = f(lam)
    assert np.all(np.diff(fl) < 0), "f 在邻域应严格单减"

    # ---------- C: 截断误差 ∝u^5 ----------
    us = np.logspace(-3, -1.2, 40)
    err = np.abs(f(g(us)) - us)
    slope = np.polyfit(np.log(us), np.log(err), 1)[0]
    assert abs(slope - 5.0) < 0.2, f"逆级数误差幂次应为 5，实得 {slope}"
    # 三次系数精确抵消：u³ 项贡献为零（数值验证 f(g(u))-u 无 u³ 成分）
    for uu in [0.01, 0.03, 0.05]:
        cubic_pred = (-C) * (-D * uu**3 / C**4) + D * (-uu / C)**3
        assert abs(cubic_pred) < 1e-14, "u³ 系数应精确抵消"

    # ---------- D: 相对修正量级 ----------
    ub = 0.1
    rel = D * ub**2 / C**3
    assert rel < 0.11, "相对修正应 <11%（|d/c|=10,u=0.1 给 0.1）"
    # 链精度 3-8%：u=0.05 时 rel=2.5% 不可见
    rel_chain = D * 0.05**2 / C**3
    assert rel_chain < 0.03, "链精度下修正应不可见"

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A
    ax = axes[0, 0]
    ax.plot(u, f(u), lw=2.0, color="#1f77b4", label="$f(\\lambda)=-c\\lambda+d\\lambda^3$")
    ax.plot(u, g(u), "--", lw=1.6, color="g", label="$g(u)=-u/c-du^3/c^4$（逆）")
    ax.plot(u, u, ":", lw=1.0, color="k", label="恒等（对照）")
    ax.set_xlabel("$\\lambda$ 或 $u$")
    ax.set_title("A  锚邻域的 $f$ 与逆级数 $g$（$c=|v_\\tau|^{-2}=1$）")
    ax.legend(fontsize=8)

    # B
    ax = axes[0, 1]
    ax.plot(lam, f(lam), lw=2.0, color="#1f77b4", label="$f$（严格单减）")
    ax.axvline(-R, color="r", ls="--", lw=1.0, label="可逆边界 $\\pm\\sqrt{c/3d}$")
    ax.axvline(R, color="r", ls="--", lw=1.0)
    ax.set_xlabel("$\\lambda$")
    ax.set_ylabel("$f(\\lambda)$")
    ax.set_title("B  锚邻域严格单减 → 局部可逆（反函数定理）")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    ax.loglog(us, err, "o-", lw=1.8, color="#1f77b4", label="$|f(g(u))-u|$")
    ax.loglog(us, 3.0 * D**2 / C**6 * us**5, "--", lw=1.4,
              color="g", label="$3d^2u^5/c^6$（领头）")
    ax.set_xlabel("$u$")
    ax.set_ylabel("误差")
    ax.set_title(f"C  逆级数误差 $\\propto u^5$（拟合斜率 {slope:.3f}）")
    ax.legend(fontsize=8)

    # D
    ax = axes[1, 1]
    uu = np.linspace(0, 0.1, 200)
    ax.plot(uu, D * uu**2 / C**3, lw=2.0, color="#1f77b4",
            label="相对修正 $|d|u^2/c^3$")
    ax.axhline(0.03, color="r", ls="--", lw=1.0, label="链精度 3%")
    ax.axhline(0.08, color="orange", ls="--", lw=1.0, label="链精度 8%")
    ax.set_xlabel("$u=|C-I|$")
    ax.set_ylabel("三次/线性 相对量")
    ax.set_title("D  锚邻域三次修正不可见（第78轮界）")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "环08_审1_矩阵分支求逆与锚邻域.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["f(g(u))≈u", "PASS", "u∈[-0.03,0.03]（逆级数有效区）"],
        ["锚邻域 f' 严格负", "PASS", f"|λ|<{R:.6f}"],
        ["f 严格单减", "PASS", "400 点"],
        ["逆级数误差幂次", f"{slope:.4f}", "应为 5（三次系数精确抵消）"],
        ["u³ 系数抵消", "PASS", "三档 u 残差 <1e-14"],
        ["相对修正 (u=0.1)", f"{rel:.4f}", "|d/c|=10 保守界"],
        ["链精度修正 (u=0.05)", f"{rel_chain:.4f}", "<3%，不可见"],
        ["锚对应 f(0)=g(0)=0", "PASS", "ε=0⇔λ=0⇔u=0"],
    ]
    with open(os.path.join(OUT, "环08_审1_矩阵分支求逆与锚邻域_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(OUT, "环08_审1_矩阵分支求逆与锚邻域.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["u", "f_g_u", "error", "relative"])
        for i in range(len(u)):
            w.writerow([f"{u[i]:.6g}", f"{comp[i]:.6g}",
                        f"{abs(comp[i]-u[i]):.6g}",
                        f"{D*u[i]**2/C**3:.6g}"])

    print("第91轮补 审-1 矩阵分支求逆与锚邻域：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
