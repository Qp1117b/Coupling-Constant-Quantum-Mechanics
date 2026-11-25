# -*- coding: utf-8 -*-
"""
V2 第一步：元素超导量级与符号诊断（不拟合、不调参）。

数据：Webb, Marsiglio & Hirsch, arXiv:1502.04724, Table III（Tc, theta_D 实测）。
反解 CQM T* = 1.13 e^{-1/3} theta_D e^{-1/lambda} 的 lambda。
预注册判据：P1 符号(lambda>0)、P2 量级(lambda in (0,2))、P3 Delta(1/lambda)=1/3、P4 不判定。
"""

import csv
import os
from math import log, exp

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "全链_V2元素超导量级.png")
OUT_CSV = os.path.join(HERE, "全链_V2元素超导量级.csv")

# Webb 2015 Table III: (element, Tc[K], theta_D[K])
DATA = [
    ("Nb", 9.25, 275), ("Pb", 7.2, 105), ("Ta", 4.4, 240), ("V", 5.4, 380),
    ("Hg", 4.15, 72), ("Sn", 3.7, 200), ("In", 3.4, 108), ("Tl", 2.4, 78.5),
    ("Re", 1.7, 430), ("Al", 1.18, 428), ("Ga", 1.08, 320), ("Mo", 0.92, 450),
    ("Zn", 0.85, 327), ("Cd", 0.52, 209),
]
A_CQM = 1.13 * exp(-1 / 3)  # = 0.8094
A_BCS = 1.13


def main():
    rows = []
    names, Tcs, thetas = [], [], []
    lams_cqm, lams_bcs = [], []

    print("反解 lambda（CQM: T*=0.8094 theta_D e^{-1/lambda}）")
    print(f"{'元素':<4}{'Tc':>7}{'theta_D':>9}{'lam_CQM':>10}{'lam_BCS':>10}{'Delta(1/lam)':>14}")
    for name, tc, th in DATA:
        inv_cqm = log(A_CQM * th / tc)
        inv_bcs = log(A_BCS * th / tc)
        lc, lb = 1 / inv_cqm, 1 / inv_bcs
        delta = inv_bcs - inv_cqm
        names.append(name); Tcs.append(tc); thetas.append(th)
        lams_cqm.append(lc); lams_bcs.append(lb)
        print(f"{name:<4}{tc:>7.2f}{th:>9.1f}{lc:>10.4f}{lb:>10.4f}{delta:>14.6f}")
        rows.append(("inverse", tc, lc, lb, f"{name}|{th}|{delta:.6f}"))

    lc = np.array(lams_cqm)
    deltas = np.array([log(A_BCS * th / tc) - log(A_CQM * th / tc) for _, tc, th in DATA])

    # 预注册判据
    p1 = bool(np.all(lc > 0))
    p2 = bool(np.all((lc > 0) & (lc < 2)))
    p3 = bool(np.all(np.abs(deltas - 1/3) < 1e-12))
    print(f"\nP1 符号(lambda>0): {'通过' if p1 else '否证'}")
    print(f"P2 量级(lambda∈(0,2)): {'通过' if p2 else '否证'}  "
          f"[min={lc.min():.4f}, max={lc.max():.4f}]")
    print(f"P3 Delta(1/lambda)=1/3: {'通过' if p3 else '否证'}  "
          f"[偏差 max={np.abs(deltas-1/3).max():.2e}]")
    print("P4 绝对精度: 不判定（缺独立 lambda 实测表与 mu*）")

    for key, val, note in [("P1", int(p1), "符号"), ("P2", int(p2), "量级"),
                           ("P3", int(p3), "扇区结构"), ("P4", -1, "不判定")]:
        rows.append(("criterion", 0, val, np.nan, f"{key}|{note}"))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.4, 9.6))

    ax[0, 0].plot(thetas, Tcs, "o", color="tab:blue", ms=6)
    for x, y, t in zip(thetas, Tcs, names):
        ax[0, 0].annotate(t, (x, y), fontsize=8)
    ax[0, 0].set_xlabel(r"$\theta_D$（K）")
    ax[0, 0].set_ylabel(r"$T_c$（K）")
    ax[0, 0].set_title("A  元素超导实测（Webb 2015 Table III）")
    ax[0, 0].grid(alpha=0.3)

    ax[0, 1].plot(lams_bcs, lams_cqm, "o", color="tab:green", ms=6)
    lim = [0, max(lams_bcs) * 1.1]
    ax[0, 1].plot(lim, lim, "--", color="0.5", lw=1.2, label="相等线")
    ax[0, 1].set_xlabel(r"$\lambda_{BCS}$（反解）")
    ax[0, 1].set_ylabel(r"$\lambda_{CQM}$（反解）")
    ax[0, 1].set_title("B  CQM 与 BCS 反解耦合（差 1/3 结构）")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].hist(lc, bins=10, color="tab:purple", alpha=0.85)
    ax[1, 0].axvspan(0, 2, color="tab:green", alpha=0.08)
    ax[1, 0].set_xlabel(r"$\lambda_{CQM}$")
    ax[1, 0].set_ylabel("元素数")
    ax[1, 0].set_title(f"C  反解耦合分布（全在 (0,2)：{p2}）")
    ax[1, 0].grid(alpha=0.3)

    crit_names = ["P1 符号", "P2 量级", "P3 扇区结构", "P4 绝对精度"]
    crit_vals = [1 if p1 else 0, 1 if p2 else 0, 1 if p3 else 0, -1]
    cols = ["tab:green" if v == 1 else ("tab:red" if v == 0 else "tab:gray")
            for v in crit_vals]
    ax[1, 1].barh(crit_names, [max(v, 0) for v in crit_vals], color=cols, alpha=0.85)
    ax[1, 1].set_xlabel("通过=1 / 否证=0 / 不判定=灰")
    ax[1, 1].set_title("D  预注册判据结果")
    ax[1, 1].grid(alpha=0.3, axis="x")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
