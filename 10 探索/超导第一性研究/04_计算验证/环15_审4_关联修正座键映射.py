# -*- coding: utf-8 -*-
"""
第90轮补（成果登记 R-99）：审-4——关联修正的座→键映射与阈值位移（非拟合）
============================================================================
检验：
  A cbar(rho)=arcsin(rho)/(2π) 的正性/单调性，线性近似 rho/(2π) 为其下界；
  B 诱导键密度 q=p²+cbar ≥ p²（修正独立映射，正关联上移）；
  C 阈值 p*=sqrt(pc²-cbar) ≤ pc(0)=0.592746，与外部关联渗流同向
    （arXiv:1305.6941 独立 0.5927 → 关联 0.5546，仅作方向对照、非 CQM 数值预言）；
  D 自平均 cbar/n ≤ cbar（临-11 条件与阈值位移同成败）。

图像用于检验单调性/符号/量级，不是用数据拟合曲线——CQM 不拟合渗流阈值数值。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环15_审4_关联修正座键映射.py"
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

PC0 = 0.592746   # 独立座渗流阈值（Ziff 1992），链内已登记


def cbar_exact(rho):
    """阈值取均值的精确座关联：arcsin(rho)/(2π)。"""
    return np.arcsin(rho) / (2.0 * np.pi)


def cbar_linear(rho):
    """小关联首阶：rho/(2π)（≤ 精确式）。"""
    return rho / (2.0 * np.pi)


def main():
    rho = np.linspace(0, 0.9, 500)

    # ---------- A: cbar ----------
    cb = cbar_exact(rho)
    cl = cbar_linear(rho)
    assert cb[0] == 0.0 and np.all(np.diff(cb) > 0), "cbar 非严格单增"
    assert np.all(cl <= cb + 1e-15), "线性近似应 ≤ 精确 arcsin 式"
    assert np.all(cb <= 0.25 + 1e-9), "cbar(0.9)=arcsin(0.9)/2π≈0.1796<0.25"

    # ---------- B: 诱导键密度 ----------
    p = np.linspace(0, 1, 400)
    for r in [0.0, 0.2, 0.5]:
        q = p**2 + cbar_exact(r)
        assert np.all(q >= p**2 - 1e-15), "q≥p² 失效"

    # ---------- C: 阈值位移 ----------
    pstar = np.sqrt(np.maximum(PC0**2 - cb, 0.0))
    assert np.all(pstar <= PC0 + 1e-15), "p*≤pc(0) 失效"
    assert np.all(np.diff(pstar) < 0), "p* 对 rho 非单减"
    first_order = PC0 - cb / (2.0 * PC0)
    assert np.all(pstar <= first_order + 1e-12), "一阶凹性界失效"
    # 外部模拟方向对照（arXiv:1305.6941 最近邻关联给 ~0.5546）
    sim_val = 0.5546
    idx = np.argmin(np.abs(pstar - sim_val))
    rho_at_sim = rho[idx]
    # CQM 只给"关联使阈值下降"的方向与一阶标度，不给该数值的独立预言
    assert pstar[-1] < sim_val < PC0, "外部关联模拟值应落在下降区间"
    shift_pct = 100.0 * (PC0 - min(pstar)) / PC0

    # ---------- D: 自平均 ----------
    n = np.arange(1, 1001)
    c0 = 0.1
    c_over_n = c0 / n
    assert np.all(c_over_n <= c0 + 1e-15), "c/n≤c 失效"
    assert c_over_n[-1] < 1e-3, "大 n 应趋零"

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # A
    ax = axes[0, 0]
    ax.plot(rho, cb, lw=2.2, color="#1f77b4", label="精确 $\\arcsin\\rho/2\\pi$")
    ax.plot(rho, cl, "--", lw=1.6, color="g", label="首阶 $\\rho/2\\pi$（下界）")
    ax.set_xlabel("相关系数 $\\rho$")
    ax.set_ylabel("座关联 $\\bar c$")
    ax.set_title("A  正关联给 $\\bar c>0$（Plackett 导数 $>0$）")
    ax.legend(fontsize=9)

    # B
    ax = axes[0, 1]
    for r, col in zip([0.0, 0.2, 0.5], ["#1f77b4", "orange", "green"]):
        ax.plot(p, p**2 + cbar_exact(r), lw=1.8,
                color=col, label=f"$\\rho={r}$")
    ax.plot(p, p**2, ":", lw=1.2, color="k", label="独立映射 $q=p^2$")
    ax.set_xlabel("座占据 $p$")
    ax.set_ylabel("诱导键密度 $q$")
    ax.set_title("B  关联修正映射 $q=p^2+\\bar c$（正关联上移）")
    ax.legend(fontsize=8)

    # C
    ax = axes[1, 0]
    ax.plot(rho, pstar, lw=2.2, color="#1f77b4",
            label="$p_*=\\sqrt{p_c^2-\\bar c}$（CQM 一阶）")
    ax.plot(rho, first_order, "--", lw=1.4, color="g",
            label="一阶凹性上界 $p_c-\\bar c/2p_c$")
    ax.axhline(PC0, color="k", ls=":", lw=1.0, label="$p_c(0)=0.592746$")
    ax.axhline(sim_val, color="r", ls="--", lw=1.0,
               label="外部关联模拟 $0.5546$（仅方向对照）")
    ax.set_xlabel("相关系数 $\\rho$")
    ax.set_ylabel("座阈值 $p_*$")
    ax.set_title("C  正关联降阈值（与外部关联渗流同向）")
    ax.legend(fontsize=8)

    # D
    ax = axes[1, 1]
    ax.plot(n, c_over_n, lw=2.0, color="#1f77b4", label="$c/n$")
    ax.axhline(c0, color="r", ls="--", lw=1.0, label="独立时 $c$")
    ax.set_xscale("log")
    ax.set_xlabel("样本量 $n$")
    ax.set_ylabel("关联残余")
    ax.set_title("D  自平均 $c/n\\leq c$：与阈值位移同成败（临-11）")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "环15_审4_关联修正座键映射.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    # ---------- CSV ----------
    summary = [
        ["cbar(rho) 严格单增", "PASS", "500 点"],
        ["线性近似 ≤ 精确 arcsin 式", "PASS", "rho∈[0,0.9]"],
        ["q ≥ p²", "PASS", "三档 rho"],
        ["p* ≤ pc(0)", "PASS", "正关联降阈值"],
        ["一阶凹性界", "PASS", "sqrt(pc²-c) ≤ pc-c/2pc"],
        ["CQM 一阶最大降幅", f"{shift_pct:.3f}%", "rho→0.9；外部模拟 6% 仅方向对照"],
        ["外部模拟值落下降区间", "PASS", "0.5546∈(p*(0.9), 0.592746)"],
        ["自平均 c/n ≤ c", "PASS", "n=1..1000，大 n 趋零"],
    ]
    with open(os.path.join(OUT, "环15_审4_关联修正座键映射_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)
    with open(os.path.join(OUT, "环15_审4_关联修正座键映射.csv"),
              "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["rho", "cbar_exact", "cbar_linear", "pstar", "first_order"])
        for i in range(len(rho)):
            w.writerow([f"{rho[i]:.6g}", f"{cb[i]:.6g}", f"{cl[i]:.6g}",
                        f"{pstar[i]:.6g}", f"{first_order[i]:.6g}"])

    print("第90轮补 审-4 关联修正座键映射：全部断言通过（非拟合）")
    for row in summary:
        print("  ", row[0], "=", row[1], "|", row[2])
    print("图:", png)


if __name__ == "__main__":
    main()
