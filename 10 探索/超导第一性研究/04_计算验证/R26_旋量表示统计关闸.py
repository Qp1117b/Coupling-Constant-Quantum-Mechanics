# -*- coding: utf-8 -*-
"""
R26：Spin(6) 旋量表示能否给出电子费米统计——前提关闸检验
=====================================================================
预注册 R26 的 P1–P5（跑数前写死）：
  P1 Spin(6)~SU(4) 半旋量 4 的权重 m=±1/2 各两个；tr exp(2πiJ)=-4
  P2 辫群标量表示 e^{iθ} 对任意 θ 满足辫关系；η²=1 仅 θ∈{0,π}
  P3 文本审计：06 与主链 Lorentz/boost/微因果 出现次数均为 0
  P4 自旋 0 可构造反对称两体态（Slater 行列式），同时可构造对称态
  P5 Lean PhaseVsBand2（链内逻辑承载）

复跑：python "10 探索/超导第一性研究/04_计算验证/R26_旋量表示统计关闸.py"
"""
import csv
import math
import os
import re
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
    # ---------- P1：半旋量权重与 2π 旋转号 ----------
    # SU(4) 基本表示 4 的权重 e_1..e_4；旋转嵌入 J=diag(1/2,-1/2,1/2,-1/2)
    m = np.array([0.5, -0.5, 0.5, -0.5])
    assert set(np.round(m, 12)) == {0.5, -0.5}, "P1: 权重不是 ±1/2"
    assert np.sum(m == 0.5) == 2 and np.sum(m == -0.5) == 2, "P1: 不是两个二重态"
    rot = np.exp(2j * np.pi * m)
    tr = float(np.real(np.sum(rot)))
    assert abs(tr - (-4.0)) < 1e-12, "P1: tr=-4 失败 %.6g" % tr

    # ---------- P2：辫群标量表示 ----------
    thetas = [0.0, math.pi / 2, math.pi, 0.37 * math.pi]
    braid_res = []
    perm_sq = []
    for th in thetas:
        eta = np.exp(1j * th)
        braid_res.append(abs(eta ** 3 - eta ** 3))     # 一维表示下辫关系自动成立
        perm_sq.append(abs(eta ** 2 - 1.0))
    assert max(braid_res) < 1e-12, "P2: 辫关系残差"
    only_pm = [th for th, v in zip(thetas, perm_sq) if v < 1e-12]
    assert set(only_pm) == {0.0, math.pi}, "P2: η²=1 只在 θ=0,π"

    # ---------- P3：链内前提文本审计 ----------
    files = [os.path.join(ROOT, "06 超导", "CQM_超导核心理论.md"),
             os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md")]
    counts = {}
    pattern = re.compile(r"Lorentz|洛伦兹|boost|微因果|microcausality", re.I)
    for p in files:
        txt = open(p, encoding="utf-8").read()
        counts[os.path.basename(p)] = len(pattern.findall(txt))
    assert all(v == 0 for v in counts.values()), "P3: 出现 Lorentz 类前提 %s" % counts

    # ---------- P4：自旋 0 的费米／玻色两体波函数 ----------
    r = np.linspace(0.2, 3.0, 180)
    phi1 = np.exp(-(r - 0.8) ** 2)
    phi2 = np.exp(-(r - 1.9) ** 2)
    psi_anti = (np.outer(phi1, phi2) - np.outer(phi2, phi1)) / math.sqrt(2)
    psi_sym = (np.outer(phi1, phi2) + np.outer(phi2, phi1)) / math.sqrt(2)
    anti_err = float(np.max(np.abs(psi_anti + psi_anti.T)))
    sym_err = float(np.max(np.abs(psi_sym - psi_sym.T)))
    assert anti_err < 1e-12, "P4: 反对称残差 %.3g" % anti_err
    assert sym_err < 1e-12, "P4: 对称残差 %.3g" % sym_err

    print("R26 Spin(6) 旋量表示统计关闸（结构判定，无拟合）：")
    print("  P1 权重 m=±1/2 各两个；tr exp(2πiJ)=%.0f ⇒ 半整数自旋（2π 转 -I）" % tr)
    print("  P2 辫关系残差 %.2e；η²=1 只在 θ∈{0,π}（θ=π/2 任意子也合法）" % max(braid_res))
    print("  P3 文本审计：%s（均为 0 ⇒ 自旋—统计定理前提不全）" % counts)
    print("  P4 自旋 0 反对称残差 %.2e、对称残差 %.2e ⇒ 统计与自旋表示无关" % (anti_err, sym_err))
    print("  P5 Lean 承载：旋量号 -1 与 η=±1 均相容")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.bar(range(4), m, color=["#1f77b4", "#d62728", "#1f77b4", "#d62728"], alpha=0.85)
    ax.axhline(0.5, color="gray", ls=":", lw=1.0)
    ax.axhline(-0.5, color="gray", ls=":", lw=1.0)
    ax.set_xticks(range(4))
    ax.set_xticklabels(["$e_1$", "$e_2$", "$e_3$", "$e_4$"])
    ax.set_ylabel("旋转权重 $m$")
    ax.set_title("A  Spin(6) 半旋量 $\\mathbf{4}$：$m=\\pm1/2$ 各二重\n$\\mathrm{tr}\\,e^{2\\pi iJ}=-4$（$2\\pi$ 转 $-I$）", fontsize=10)
    ax.grid(alpha=0.3, axis="y")

    ax = axes[0, 1]
    th = np.linspace(0, 2 * np.pi, 500)
    eta2 = np.abs(np.exp(2j * th) - 1)
    ax.plot(th / np.pi, eta2, "k-", lw=2.2)
    for t, c, lab in [(0.0, "#2ca02c", "玻色 $\\theta=0$"),
                      (1.0, "#d62728", "费米 $\\theta=\\pi$"),
                      (0.5, "#9467bd", "任意子 $\\theta=\\pi/2$")]:
        ax.plot([t], [abs(np.exp(2j * t * np.pi) - 1)], "o", ms=9, color=c)
        ax.annotate(lab, (t, 1.45), fontsize=9, ha="center")
    ax.set_xlabel("交换相位 $\\theta/\\pi$")
    ax.set_ylabel("$|\\eta^2-1|$（置换群额外约束）")
    ax.set_title("B  辫群 $d=2$：$\\theta$ 任意；只有 $d>2$ 才逼出 $\\eta=\\pm1$")
    ax.set_ylim(0, 2.2)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    im = ax.imshow(psi_anti, extent=[0, 1, 0, 1], origin="lower", cmap="RdBu_r")
    ax.annotate("$\\Psi(r_2,r_1)=-\\Psi(r_1,r_2)$\n残差 %.1e" % anti_err,
                (0.05, 0.88), fontsize=9, color="white")
    ax.set_xlabel("$r_1$")
    ax.set_ylabel("$r_2$")
    ax.set_title("C  自旋 0 的反对称两体态（Slater 行列式）")
    fig.colorbar(im, ax=ax, shrink=0.85)

    ax = axes[1, 1]
    ax.axhline(-1.0, color="k", lw=2.2, ls="--")
    for t, c, lab in [(0.0, "#2ca02c", "玻色"), (1.0, "#d62728", "费米"), (0.5, "#9467bd", "任意子")]:
        ax.plot([t], [-1.0], "o", ms=11, color=c)
        ax.annotate(lab + "\n（同一旋量号）", (t, -0.86), fontsize=9, ha="center")
    ax.set_xlim(-0.2, 2.2)
    ax.set_ylim(-1.5, -0.6)
    ax.set_xticks([0, 0.5, 1])
    ax.set_xticklabels(["$0$", "$\\pi/2$", "$\\pi$"])
    ax.set_xlabel("交换相位 $\\theta$")
    ax.set_ylabel("$2\\pi$ 旋转号 $s$")
    ax.set_title("D  同一个旋量号 $s=-1$ 兼容三种统计\n旋量表示不能挑出 $\\theta=\\pi$")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    png = os.path.join(OUT, "R26_旋量表示统计关闸.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "权重 ±1/2 各二；tr=-4", "通过"],
        ["P2", "辫关系残差 %.2e；η²=1 仅 θ=0,π" % max(braid_res), "通过"],
        ["P3", "Lorentz 类前提 %s" % counts, "通过（均 0）"],
        ["P4", "反对称残差 %.2e；对称残差 %.2e" % (anti_err, sym_err), "通过"],
        ["P5", "旋量号与交换号独立（Lean）", "由 Lean 承载"],
        ["结论", "旋量表示单独不给出费米统计", "06 L1695 保持开放"],
    ]
    with open(os.path.join(OUT, "R26_旋量表示统计关闸_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
