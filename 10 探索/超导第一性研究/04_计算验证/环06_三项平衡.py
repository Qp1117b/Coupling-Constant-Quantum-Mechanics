# -*- coding: utf-8 -*-
"""
环 6／临-25 三项平衡：恒等式、尖锐不等式、反例与不可判定性。

归一化：无量纲；只做代数恒等式、不等式与符号形状核对，不拟合数据，
也不为 D_new 与 Mdot 引入任何新动力学（本轮判定它们在链内不可判定）。

外部对照（只说明"闭合需要额外假设"，不写成 CQM 已证）：
  Boltzmann 分子混沌假设 / H 定理；Mori-Zwanzig 投影（噪声必须另设）；
  Hohenberg-Halperin model A/B（需指定 Langevin 动力学与 Einstein 关系）。
"""

import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环06_三项平衡.png")
OUT_CSV = os.path.join(HERE, "环06_三项平衡.csv")
OUT_SUM = os.path.join(HERE, "环06_三项平衡_摘要.csv")


def centered(x):
    return np.asarray(x, dtype=float) - np.mean(x)


def cov_parts(tau, vel):
    """同归一化的 D, W, B（见推导卡 (T.3)）。"""
    n = len(tau)
    x = centered(tau)
    y = centered(vel)
    c = 2.0 / (n - 1.0)
    D = c * np.sum(x ** 2)
    W = c * np.sum(y ** 2)
    B = 2.0 * c * np.sum(x * y)
    return D, W, B, x, y


def pair_B(tau, vel):
    """(6.7) 的无序对求和：B = (2/M) sum_{i<j} H_ij v_ij。"""
    n = len(tau)
    M = n * (n - 1) / 2.0
    s = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            s += (tau[i] - tau[j]) * (vel[i] - vel[j])
    return 2.0 / M * s


def main():
    rng = np.random.default_rng(20261122)
    rows = []

    # --- A: 三点反例（06 §0.6 原文组态）
    tau3 = np.array([1.0, -1.0, 0.0])
    vel3 = np.array([0.0, 0.0, 1.0])
    D3, W3, B3, x3, y3 = cov_parts(tau3, vel3)
    Bpair3 = pair_B(tau3, vel3)

    # --- B: 协方差恒等式随机核对与 Cauchy 不等式
    n_list = [3, 4, 6, 10, 20]
    ident_err = []
    bound_ratio = []
    for n in n_list:
        for _ in range(400):
            tau = rng.normal(size=n)
            vel = rng.normal(size=n)
            D, W, B, _, _ = cov_parts(tau, vel)
            Bp = pair_B(tau, vel)
            ident_err.append(abs(B - Bp))
            if D > 0 and W > 0:
                bound_ratio.append(B ** 2 / (4.0 * D * W))
            rows.append(("B", n, D, W, B, Bp))

    # --- C: 测试函数 y = lam(t) x（不是 CQM 动力学！），展示 B 的符号可翻转
    x = centered(np.array([3.0, 1.0, -2.0, -2.0]))
    lam_grid = np.linspace(-1.0, 1.0, 401)
    c4 = 2.0 / 3.0
    B_lam = np.array([2.0 * c4 * np.sum(x * (lam * x)) for lam in lam_grid])
    D_x = c4 * np.sum(x ** 2)

    # --- D: 扩大项抵消生产：Ddot = B + Mdot/M (Dnew-D) 的零线
    M, Mdot, D0, Dnew = 3.0, 1.0, 1.0, 0.0
    B_grid = np.linspace(-0.2, 0.8, 401)
    expansion = Mdot / M * (Dnew - D0)
    Ddot = B_grid + expansion
    B_star = -expansion

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "n", "D", "W", "B_cov", "B_pair"])
        wr.writerows(rows)

    with open(OUT_SUM, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["quantity", "value", "note"])
        wr.writerow(["three_point_D", D3, "tau=(1,-1,0)"])
        wr.writerow(["three_point_W", W3, "vel=(0,0,1), W>0"])
        wr.writerow(["three_point_B", B3, "must be 0"])
        wr.writerow(["three_point_B_pair", Bpair3, "(6.7) unordered-pair sum"])
        wr.writerow(["max_identity_error", max(ident_err), "B_cov - B_pair"])
        wr.writerow(["max_B2_over_4DW", max(bound_ratio), "must be <= 1"])
        wr.writerow(["expansion_offset", expansion, "Mdot=1, M=3, Dnew=0, D=1"])
        wr.writerow(["B_star", B_star, "Ddot=0 crossing"])

    # ---------------------------------------------------------------- figure
    fig, ax = plt.subplots(2, 2, figsize=(12.5, 10.0))

    # A: three-point geometry
    ax[0, 0].scatter([0, 1, 2], tau3, s=70, label=r"$\tau$")
    ax[0, 0].scatter([0, 1, 2], vel3, s=70, marker="x", label=r"$v$")
    ax[0, 0].axhline(0, color="k", lw=0.8)
    ax[0, 0].set_xlabel("节点")
    ax[0, 0].set_ylabel("值")
    ax[0, 0].set_title(f"A  三点反例：$W={W3:.3f}>0$，$B={B3:.1f}$（06 §0.6）")
    ax[0, 0].legend(fontsize=8)
    ax[0, 0].grid(alpha=0.3)

    # B: identity + bound
    ax[0, 1].plot(ident_err, "o", ms=2, alpha=0.3, label="恒等式误差")
    ax[0, 1].plot(bound_ratio, "s", ms=2, alpha=0.3, label=r"$B^2/(4DW)$")
    ax[0, 1].axhline(1.0, color="k", ls="--", lw=1.0)
    ax[0, 1].set_yscale("symlog", linthresh=1e-12)
    ax[0, 1].set_xlabel("随机样本序号")
    ax[0, 1].set_ylabel("值")
    ax[0, 1].set_title("B  协方差恒等式与 Cauchy 不等式 $B^2\\leq4DW$")
    ax[0, 1].legend(fontsize=8)
    ax[0, 1].grid(alpha=0.3)

    # C: sign flip under test function
    ax[1, 0].plot(lam_grid, B_lam, lw=2.0)
    ax[1, 0].axhline(0, color="k", ls=":", lw=1.0)
    ax[1, 0].axvline(0, color="gray", ls="--", lw=1.0)
    ax[1, 0].set_xlabel(r"测试函数参数 $\lambda$（$y=\lambda x$）")
    ax[1, 0].set_ylabel(r"$B$")
    ax[1, 0].set_title(f"C  $B$ 随协方差符号翻转（$D_x={D_x:.3f}$ 固定；非动力学）")
    ax[1, 0].grid(alpha=0.3)

    # D: expansion offset
    ax[1, 1].plot(B_grid, Ddot, lw=2.0, label=r"$\dot{\mathcal{D}}$")
    ax[1, 1].axhline(0, color="k", ls=":", lw=1.0)
    ax[1, 1].axvline(B_star, color="tab:red", ls="--", lw=1.2,
                     label=fr"$B_*={B_star:.3f}$")
    ax[1, 1].fill_between(B_grid, Ddot, 0, where=Ddot <= 0, alpha=0.2, color="tab:green")
    ax[1, 1].set_xlabel(r"生产项 $B$")
    ax[1, 1].set_ylabel(r"$\dot{\mathcal{D}}$")
    ax[1, 1].set_title("D  扩大项可抵消正生产：$\\dot{\\mathcal{D}}<0$ 仍可能")
    ax[1, 1].legend(fontsize=8)
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print(f"three-point: D={D3:.6f}, W={W3:.6f}, B={B3:.12f}, B_pair={Bpair3:.12f}")
    print(f"max identity error = {max(ident_err):.3e}")
    print(f"max B^2/(4DW) = {max(bound_ratio):.12f} (<= 1)")
    print(f"expansion offset = {expansion:.6f}, B_star = {B_star:.6f}")
    print("note: panel C is a test function, not a claimed CQM dynamics")


if __name__ == "__main__":
    main()
