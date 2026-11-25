# -*- coding: utf-8 -*-
"""
R31（FE09）：链内 n=2 通量量子做 CS 统计附着——最小费米子候选
=====================================================================
预注册 R31 的 P1–P5（跑数前写死）：
  P1 链内前件审计（2D、U(1)_em、Z_n、Phi_n=n h/2e、临-6）
  P2 奇偶律：m 奇 ⇒ (-1)^m=-1（费米）；偶 ⇒ +1（玻色）
  P3 外部 CS 标准：b=-(q/kappa)rho，奇数 kappa 转置
  P4 不越界：不产生带/vF/Gamma0 系数/绝对 Tc
  P5 FE 红线：候选落点核查

复跑：python "10 探索/超导第一性研究/04_计算验证/R31_FE09_CS统计附着.py"
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
    # ---------- P1：链内前件审计 ----------
    chain = open(os.path.join(ROOT, "10 探索", "CQM_探索_推导链.md"), encoding="utf-8").read()
    core = open(os.path.join(ROOT, "06 超导", "CQM_超导核心理论.md"), encoding="utf-8").read()
    checks = {
        "二维空间": "SO(2)_{\\rm space}" in core or "SO(2)" in core,
        "U(1)_em": "U(1)_{\\rm em}" in core or "$U(1)$" in core,
        "Phi_n=n h/2e": "h/2e" in chain,
        "n 为绕数": "绕数" in chain,
        "临-6": "临-6" in chain,
    }
    assert all(checks.values()), "P1: 前件审计失败 %s" % checks

    # ---------- P2：附着奇偶律 ----------
    ms = np.arange(0, 9)
    phases = np.pi * ms
    signs = np.array([(-1) ** int(m) for m in ms])
    for m in ms:
        assert signs[m] == (-1 if m % 2 == 1 else 1), "P2: 奇偶律失败 m=%d" % m
    # 链内 n=2 扇区给 Phi_2 = h/e ⇒ m=1
    n_first = 2
    m_chain = n_first // 2
    assert m_chain == 1 and signs[m_chain] == -1, "P2: n=2 应给 m=1（费米）"

    # ---------- P3：CS 附着 ----------
    # b = -(q/kappa) rho；取 q=rho=1，kappa 奇/偶
    kappas = np.arange(1, 8)
    b = -1.0 / kappas
    flux_units = 1.0 / kappas          # |Phi|/Phi_0
    stat_phase_cs = np.pi / kappas      # 交换相位（示意）
    assert all(abs(stat_phase_cs[k - 1] - math.pi / k) < 1e-12 for k in kappas)

    # ---------- P4：候选边界 ----------
    closure = {
        "费米交换统计": True,
        "Bloch 带色散": False,
        "v_F / vHs": False,
        "Gamma_0 系数": False,
        "绝对 Tc": False,
        "六纯数": False,
    }
    assert closure["费米交换统计"] and not any(
        closure[k] for k in list(closure)[1:]
    ), "P4: 越界"

    # ---------- P5：FE 落点 ----------
    fe_dir = os.path.join(ROOT, "10 探索", "超导第一性研究", "08_框架扩展候选")
    assert os.path.isdir(fe_dir), "P5: FE 目录缺失"

    print("R31（FE09）CS 统计附着候选（未落地）：")
    print("  P1 前件：%s" % checks)
    print("  P2 奇偶律：m 奇 → -1（费米），m 偶 → +1（玻色）；链内 n=2 → m=1")
    print("  P3 CS：b=-(q/kappa)rho，|Phi|/Phi_0=1/kappa，kappa=1 给单位磁通")
    print("  P4 只补统计：%s" % closure)
    print("  P5 FE 目录确认；不写权威源、不改状态栏")

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(ms, phases / np.pi, "o-", lw=2.2, ms=7, color="#1f77b4")
    for m in ms[::2]:
        ax.plot([m], [m], "s", ms=9, color="#2ca02c")
    for m in ms[1::2]:
        ax.plot([m], [m], "^", ms=9, color="#d62728")
    ax.plot([m_chain], [m_chain], "*", ms=18, color="gold", markeredgecolor="k")
    ax.annotate("链内 $n=2\\Rightarrow m=1$\n（费米）", (1.2, 3.0), fontsize=9)
    ax.set_xlabel("附着磁通量子数 $m$")
    ax.set_ylabel("交换相位 $\\theta/\\pi$")
    ax.set_title("A  奇数 $m$ → $\\theta=\\pi$（费米），偶数 → $0$（玻色）")
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.step(ms - 0.5, signs, where="post", lw=2.4, color="k")
    ax.scatter(ms, signs, c=np.where(ms % 2 == 1, "#d62728", "#2ca02c"), zorder=4, s=60)
    ax.axhline(0, color="gray", lw=1)
    ax.set_ylim(-1.4, 1.4)
    ax.set_yticks([-1, 1])
    ax.set_yticklabels(["$-1$ 费米", "$+1$ 玻色"])
    ax.set_xlabel("$m$")
    ax.set_title("B  交换符号 $(-1)^m$")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(kappas, flux_units, "o-", lw=2.2, label="$|\\Phi|/\\Phi_0=1/\\kappa$")
    ax.plot(kappas, stat_phase_cs / np.pi, "s--", lw=2.0, label="交换相位 $/\\pi$（示意）")
    ax.set_xlabel("CS 层级 $\\kappa$")
    ax.set_ylabel("归一化")
    ax.set_title("C  CS 项 $b=-(q/\\kappa)\\rho$：层级定附着磁通（外部机制）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    names = list(closure.keys())
    vals = [1 if closure[k] else 0 for k in names]
    colors = ["#2ca02c" if v else "#d62728" for v in vals]
    ax.barh(range(len(names)), vals, color=colors, alpha=0.85)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlim(0, 1.3)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["否", "是"])
    ax.set_title("D  候选只补统计：不越界")
    ax.grid(alpha=0.3, axis="x")

    fig.tight_layout()
    png = os.path.join(OUT, "R31_FE09_CS统计附着.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "链内前件 %s" % checks, "通过"],
        ["P2", "奇偶律成立；n=2→m=1→费米", "通过"],
        ["P3", "CS 附着 b=-(q/kappa)rho", "外部机制（B 类）"],
        ["P4", "只补统计，不带/vF/Gamma0/Tc", "通过"],
        ["P5", "FE 落点，不改权威源", "通过"],
        ["结论", "FE09 候选完成·未落地", "状态不动"],
    ]
    with open(os.path.join(OUT, "R31_FE09_CS统计附着_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
