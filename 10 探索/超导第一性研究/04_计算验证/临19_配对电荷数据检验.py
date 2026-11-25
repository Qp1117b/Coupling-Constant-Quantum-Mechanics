# -*- coding: utf-8 -*-
"""
R14: 配对电荷 q=2e 的 B_c2 数据一致性检验（Weitzel 2023 NbN）。
只检验代数与区间包含，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/临19_配对电荷数据检验.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
H = 6.62607015e-34
E = 1.602176634e-19
PHI_2E = H / (2 * E)  # q=2e 磁通量子
PHI_E = H / E         # q=e 磁通量子

XI = 6.7e-9        # 实测 xi
XI_ERR = 0.6e-9
BC2_MEAS = 6.1     # 实测 B_c2 (T)
BC2_ERR = 1.7


def bc2(Phi, xi):
    return Phi / (2 * math.pi * xi**2)


def assertions():
    out = {}
    out["Phi_0_2e_Wb"] = PHI_2E
    out["Phi_0_e_Wb"] = PHI_E
    out["flux_ratio_qe_over_q2e"] = PHI_E / PHI_2E
    out["flux_double_exact"] = bool(abs(PHI_E / PHI_2E - 2.0) < 1e-12)

    b2e = bc2(PHI_2E, XI)
    be = bc2(PHI_E, XI)
    out["Bc2_q2e_T"] = float(b2e)
    out["Bc2_qe_T"] = float(be)
    out["Bc2_ratio"] = be / b2e
    out["Bc2_in_measured_2e"] = bool(BC2_MEAS - BC2_ERR <= b2e <= BC2_MEAS + BC2_ERR)
    out["Bc2_outside_measured_e"] = bool(not (BC2_MEAS - BC2_ERR <= be <= BC2_MEAS + BC2_ERR))

    # xi 误差传播 [6.1,7.3] nm
    blo = bc2(PHI_2E, XI - XI_ERR)
    bhi = bc2(PHI_2E, XI + XI_ERR)
    rng_lo, rng_hi = min(blo, bhi), max(blo, bhi)
    out["Bc2_range_q2e_T"] = f"{rng_lo:.2f}-{rng_hi:.2f}"
    out["range_overlaps_measured"] = bool(rng_lo <= BC2_MEAS + BC2_ERR and rng_hi >= BC2_MEAS - BC2_ERR)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) B_c2(xi) 两分支
    ax = axes[0, 0]
    xis = np.linspace(5.5e-9, 9e-9, 200)
    ax.plot(xis * 1e9, np.array([bc2(PHI_2E, x) for x in xis]), "b-", lw=2, label=r"$q=2e$（链选）")
    ax.plot(xis * 1e9, np.array([bc2(PHI_E, x) for x in xis]), "r--", lw=2, label=r"$q=e$（链排除）")
    ax.axhspan(BC2_MEAS - BC2_ERR, BC2_MEAS + BC2_ERR, color="green", alpha=0.2,
               label=f"实测 $B_{{c2}}={BC2_MEAS}\\pm{BC2_ERR}$ T")
    ax.scatter([XI * 1e9], [bc2(PHI_2E, XI)], c="blue", s=70, zorder=5)
    ax.set_xlabel(r"$\xi$ (nm)")
    ax.set_ylabel(r"$B_{c2}$ (T)")
    ax.set_title("(a) B_c2 = Phi_0/(2 pi xi^2) 两分支")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 磁通量子对比
    ax = axes[0, 1]
    ax.bar(["q=2e (链)", "q=e (排除)"], [PHI_2E, PHI_E], color=["tab:blue", "tab:red"])
    ax.set_ylabel(r"$\Phi_0$ (Wb)")
    ax.set_title("(b) 磁通量子：q=e 恰为两倍")
    ax.grid(alpha=0.3, axis="y")

    # (c) B_c2 分支 vs 实测区间
    ax = axes[1, 0]
    ax.bar(["实测", "链 q=2e", "q=e"], [BC2_MEAS, bc2(PHI_2E, XI), bc2(PHI_E, XI)],
           color=["tab:green", "tab:blue", "tab:red"])
    ax.errorbar([0], [BC2_MEAS], yerr=BC2_ERR, fmt="none", ecolor="black", capsize=5)
    ax.set_ylabel(r"$B_{c2}$ (T)")
    ax.set_title("(c) 链 q=2e 落在实测区间；q=e 远离")
    ax.grid(alpha=0.3, axis="y")

    # (d) 独立性审计
    ax = axes[1, 1]
    labels = ["ξ 与 Bc2\n独立测量？", "论文用 GL\n(q=2e)换算"]
    vals = [0, 1]
    ax.bar(labels, vals, color=["tab:red", "tab:gray"])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["否", "是"])
    ax.set_title("(d) 一致性核对，非独立判别")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R14: 临-19 配对电荷数据一致性核对（Weitzel 2023 NbN，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "临19_配对电荷数据检验.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R14 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "临19_配对电荷数据检验_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
