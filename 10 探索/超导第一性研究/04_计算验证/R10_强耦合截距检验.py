# -*- coding: utf-8 -*-
"""
预注册判定 R10：链内 R1=3.528 作为强耦合通用曲线弱耦合截距（B 类诚实标注）
================================================================================
用外部 Mitrović 式，只取链内 R1=2pi/e^gamma 作截距。
核心 P1：链内 R1 是正确弱耦合截距（实测 gap ratio 与预言偏差小）。
辅助 P2：实测 gap ratio 随 Tc/omega_log 严格单调不减 —— 诚实报告结果。
边界：omega_log/theta_D 实测散布，链内 e^{-1/2} 不可套实验 theta_D。

复跑：python "10 探索/超导第一性研究/04_计算验证/R10_强耦合截距检验.py"
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
kB = 8.617333262e-2  # meV/K
GAMMA_E = 0.5772156649015329
R1 = 2 * math.pi / math.exp(GAMMA_E)   # 3.5278
C_MIT = 12.5                            # 外部 Eliashberg 拟合常数（不拟合、不调）

# 独立数据：SCDFT suppl. (Tcexp, omega_log meV) + Kittel 元素表 (2Delta meV)
data = {
    "Al": (1.18, 24.5, 0.34),
    "In": (3.39, 6.2, 1.05),
    "Sn": (3.75, 6.1, 1.15),
    "Ta": (4.45, 13.2, 1.40),
    "Pb": (7.2, 5.1, 2.73),
    "Nb": (9.1, 11.9, 3.05),
}
weak = ["Al", "Ta"]
strong = ["Pb", "Nb"]


def mitrovic(x):
    """x = Tc/omega_log；修正项 12.5 x^2 ln(1/(2x))，仅 0<x<1/2 有效。"""
    if x <= 0 or 2 * x >= 1:
        return float("nan")
    return R1 * (1 + C_MIT * x * x * math.log(1 / (2 * x)))


def rankdata(a):
    order = sorted(range(len(a)), key=lambda i: a[i])
    r = [0] * len(a)
    for pos, i in enumerate(order):
        r[i] = pos + 1
    return r


def main():
    rows = []
    for k, (tc, wmev, gap2) in data.items():
        wlog = wmev / kB
        x = tc / wlog
        gr = gap2 / (kB * tc)
        pred = mitrovic(x)
        dev = abs(pred - gr) / gr
        rows.append({"el": k, "tc": tc, "wlog_K": wlog, "x": x,
                     "gr": gr, "pred": pred, "dev": dev})

    # ---- P1：弱耦合截距判据（预注册：弱 <=8%、强 <=12%）----
    dev_weak = max(r["dev"] for r in rows if r["el"] in weak)
    dev_strong = max(r["dev"] for r in rows if r["el"] in strong)
    p1 = (dev_weak <= 0.08) and (dev_strong <= 0.12)
    assert p1, "P1：链内 R1 弱耦合截距判据应通过"

    # ---- P2：严格单调（预注册判据）—— 诚实计算，不伪造 ----
    srt = sorted(rows, key=lambda r: r["x"])
    gr_seq = [r["gr"] for r in srt]
    strict_mono = all(gr_seq[i + 1] >= gr_seq[i] for i in range(len(gr_seq) - 1))
    rx = rankdata([r["x"] for r in rows])
    rg = rankdata([r["gr"] for r in rows])
    n = len(rows)
    d2 = sum((rx[i] - rg[i]) ** 2 for i in range(n))
    spearman = 1 - 6 * d2 / (n * (n * n - 1))
    # P2 严格单调失败是诚实发现（弱耦合段实验散布主导），不 assert。

    print("R10 强耦合截距检验（B 类）：")
    for r in rows:
        print("  %-3s Tc/wlog=%.4f gap=%.3f Mitrovic=%.3f dev=%.1f%%" %
              (r["el"], r["x"], r["gr"], r["pred"], 100 * r["dev"]))
    print("P1 弱耦合最大偏差=%.1f%% 强耦合最大偏差=%.1f%% -> %s" %
          (100 * dev_weak, 100 * dev_strong, "PASS" if p1 else "FAIL"))
    print("P2 严格单调=%s  Spearman r=%.3f" %
          ("PASS" if strict_mono else "FAIL", spearman))

    # ---- 图 ----
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    xs = np.linspace(0.0001, 0.30, 400)
    ax.plot(xs, [mitrovic(x) for x in xs], "k-", lw=1.8,
            label="Mitrović 曲线（截距 $R_1=2\\pi/e^\\gamma$）")
    ax.axhline(R1, color="blue", ls="--", lw=1.2, label="弱耦合截距 $R_1=%.3f$" % R1)
    for r in rows:
        c = "green" if r["el"] in weak else ("red" if r["el"] in strong else "orange")
        ax.scatter([r["x"]], [r["gr"]], s=70, color=c, zorder=5)
        ax.annotate(r["el"], (r["x"], r["gr"]), textcoords="offset points",
                    xytext=(5, 4), fontsize=9)
    ax.set_xlabel("$T_c/\\omega_{log}$")
    ax.set_ylabel("$2\\Delta_0/k_B T_c$")
    ax.set_title("A  实测 gap ratio vs 强耦合曲线（链内截距）")
    ax.legend(fontsize=8)

    ax = axes[0, 1]
    preds = [r["pred"] for r in rows]
    grs = [r["gr"] for r in rows]
    ax.plot([3.3, 4.6], [3.3, 4.6], "k--", lw=1.0)
    for r in rows:
        ax.scatter([r["pred"]], [r["gr"]], s=70,
                   color="green" if r["el"] in weak else ("red" if r["el"] in strong else "orange"))
        ax.annotate(r["el"], (r["pred"], r["gr"]), textcoords="offset points",
                    xytext=(5, 4), fontsize=9)
    ax.set_xlabel("Mitrović 预言")
    ax.set_ylabel("实测 gap ratio")
    ax.set_title("B  预言 vs 实测（对角线=一致）")

    ax = axes[1, 0]
    els = [r["el"] for r in sorted(rows, key=lambda r: r["x"])]
    devs = [100 * r["dev"] for r in sorted(rows, key=lambda r: r["x"])]
    ax.bar(els, devs, color=["green" if e in weak else ("red" if e in strong else "orange") for e in els])
    ax.axhline(8, color="blue", ls=":", lw=1.0, label="弱耦合 8%")
    ax.axhline(12, color="red", ls=":", lw=1.0, label="强耦合 12%")
    ax.set_ylabel("相对偏差 (%)")
    ax.set_title("C  P1 截距偏差（全元素 < 8%）")
    ax.legend(fontsize=8)

    ax = axes[1, 1]
    # omega_log/theta_D 实测散布（Semenok 2025 表 S1+S5，单位 K）——口径错配边界
    ratio_data = {"Nb": 163 / 277, "Hg": 86 / 72, "Nb$_3$Sn": 142 / 270}
    ax.bar(list(ratio_data.keys()), list(ratio_data.values()), color="gray")
    ax.axhline(math.exp(-0.5), color="blue", ls="--", lw=1.4,
               label="链内新 $e^{-1/2}=%.3f$" % math.exp(-0.5))
    ax.axhline(math.exp(-1 / 3), color="red", ls="--", lw=1.4,
               label="旧口径 $e^{-1/3}=%.3f$" % math.exp(-1 / 3))
    ax.set_ylabel("$\\omega_{log}/\\theta_D$")
    ax.set_title("D  边界：实测散布 0.53–1.19，$e^{-1/2}$ 不可套实验 $\\theta_D$")
    ax.legend(fontsize=8)

    fig.tight_layout()
    png = os.path.join(OUT, "R10_强耦合截距检验.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    summary = [
        ["截距 R1", "%.6f" % R1, "$2\\pi/e^\\gamma$（C5，链内）"],
        ["P1 弱耦合最大偏差", "%.1f%%" % (100 * dev_weak), "判据 <=8%"],
        ["P1 强耦合最大偏差", "%.1f%%" % (100 * dev_strong), "判据 <=12%"],
        ["P1 结论", "PASS", "链内 R1 是强耦合曲线正确弱耦合截距"],
        ["P2 严格单调", "PASS" if strict_mono else "FAIL", "弱耦合段实验散布主导（诚实报告）"],
        ["P2 Spearman r", "%.3f" % spearman, "正相关，强耦合端上扬明确"],
        ["口径边界", "登记", "$\\omega_{log}/\\theta_D$ 实测散布，$e^{-1/2}$ 不可套实验 $\\theta_D$"],
        ["类别", "B 类", "外部 Mitrović 式 + 链内一个输入 R1，不升格第一性"],
    ]
    with open(os.path.join(OUT, "R10_强耦合截距检验_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(summary)

    print("图:", png)
    print("R10 完成：P1 通过；P2 严格单调未通过（诚实报告），Spearman r=%.3f。" % spearman)


if __name__ == "__main__":
    main()
