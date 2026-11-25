# -*- coding: utf-8 -*-
"""
环 15／`审-4` 的数值核对：环空间一半性质与推 6 撤销。

1. 小图 C4、K4 枚举 GF(2) 环向量，核对每条边占据率 0.5；
2. q=p^2 曲线、诱导键阈值 q_c=0.351348 与朴素 1/2；
3. 阈值对比柱状；
4. 推 6 撤离示意：配对诱导键在 p_pair>0.592746 已渗流。

枚举与解析直接计算，无拟合。
"""

import csv
import itertools
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环15_审4_环空间一半.png")
OUT_CSV = os.path.join(HERE, "环15_审4_环空间一半.csv")

PC_SITE = 0.592746
QC = PC_SITE ** 2


def cycle_space(V, edges):
    """枚举 GF(2) 环空间：每个顶点偶度的边子集。"""
    E = len(edges)
    out = []
    for bits in itertools.product([0, 1], repeat=E):
        deg = [0] * V
        for b, (i, j) in zip(bits, edges):
            deg[i] ^= b
            deg[j] ^= b
        if all(d == 0 for d in deg):
            out.append(bits)
    return np.array(out, dtype=int)


def main():
    rows = []
    graphs = {
        "C4": (4, [(0, 1), (1, 2), (2, 3), (3, 0)]),
        "K4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    }
    print("环空间枚举：每边占据率")
    occ_all = {}
    for name, (V, edges) in graphs.items():
        Z = cycle_space(V, edges)
        occ = Z.mean(axis=0)
        occ_all[name] = occ
        print(f"  {name}: |Z|={len(Z)}, 维数={int(np.log2(len(Z)))}, 每边占据率={np.round(occ, 4)}")
        for e, v in enumerate(occ):
            rows.append((name + "_occupancy", e, float(v), 0.5, np.nan))

    print(f"\n诱导键阈值 q_c = {QC:.6f}, 朴素阈值 1/2 = 0.5")
    for p in (0.5, PC_SITE, 0.707107, 1.0):
        print(f"  p={p:.6f}: q=p^2={p*p:.6f}")
        rows.append(("q_of_p", p, p * p, QC, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A: occupancy
    x_c4 = np.arange(4)
    x_k4 = np.arange(6)
    ax[0, 0].bar(x_c4 - 0.15, occ_all["C4"], 0.3, color="tab:blue", alpha=0.85, label="C4")
    ax[0, 0].bar(x_k4 + 0.15, occ_all["K4"], 0.3, color="tab:orange", alpha=0.85, label="K4")
    ax[0, 0].axhline(0.5, color="tab:red", ls="--", lw=1.6, label="1/2")
    ax[0, 0].set_ylabel("每边占据率")
    ax[0, 0].set_title("A  环空间均匀元素：每边恰占一半")
    ax[0, 0].legend(fontsize=9)
    ax[0, 0].set_ylim(0, 1.1)
    ax[0, 0].grid(alpha=0.3, axis="y")

    # B: q=p^2
    ps = np.linspace(0, 1, 500)
    ax[0, 1].plot(ps, ps ** 2, lw=2.2, color="tab:purple", label=r"$q=p^2$")
    ax[0, 1].axhline(QC, color="tab:green", ls="--", lw=1.6,
                     label=rf"诱导键阈值 $q_c={QC:.3f}$")
    ax[0, 1].axhline(0.5, color="tab:red", ls=":", lw=1.6, label=r"键阈值 $1/2$")
    ax[0, 1].axvline(PC_SITE, color="tab:green", lw=1.0, alpha=0.7)
    ax[0, 1].axvline(0.707107, color="tab:red", lw=1.0, alpha=0.7)
    ax[0, 1].set_xlabel(r"$p_{\rm pair}$（座比例）")
    ax[0, 1].set_ylabel(r"$q$（诱导键比例）")
    ax[0, 1].set_title("B  正确阈值 vs 朴素映射")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C: thresholds
    ax[1, 0].bar(["诱导键 q_c", "键阈值 1/2", "朴素 p=0.707107"],
                 [QC, 0.5, 0.707107], color=["tab:green", "tab:red", "tab:orange"], alpha=0.85)
    ax[1, 0].axhline(PC_SITE, color="tab:blue", ls="--", lw=1.4,
                     label=f"座阈值 {PC_SITE}")
    ax[1, 0].set_ylabel("数值")
    ax[1, 0].set_title("C  推 6 混用了两个不同阈值")
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, axis="y")

    # D: withdrawal
    ax[1, 1].plot(ps, (ps > PC_SITE).astype(float), lw=2.2, color="tab:green",
                  label="配对诱导键渗流（判据 p>p_c^site）")
    ax[1, 1].axvline(PC_SITE, color="tab:blue", ls="--", lw=1.4)
    ax[1, 1].text(0.45, 0.55, r"$p_{\rm loop}=1/2$ 饱和\n不参与配对键渗流判定",
                  fontsize=9, color="tab:red")
    ax[1, 1].set_xlabel(r"$p_{\rm pair}$")
    ax[1, 1].set_ylabel("是否渗流（示意）")
    ax[1, 1].set_title("D  推 6 撤销")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].set_ylim(-0.1, 1.2)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
