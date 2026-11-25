# -*- coding: utf-8 -*-
"""
R3: R1(lambda 几何) + R2(Cooper 对数) -> T* 形状拉通。
只检验代数恒等、单调方向、同位素标度，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/全链R1R2拉通.py"
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
L113_E = 1.13 * math.exp(-1.5)  # 链登记前因子 1.13 e^{-3/2} ≈ 0.2528


def lambda_geom(N0, z, g, cE, rho, Q, M, omegaD):
    """R1 (CQM-L3)"""
    return 1.5 * N0 * z * g**2 * cE**2 * (1 - rho) * Q**2 / (M * omegaD**2)


def exponent_r31(M, c, N0, z, g, cE, rho):
    """R3.1: 2/lambda_geom = 4 M c^2 / (3 N0 z g^2 cE^2 (1-rho))"""
    return 4 * M * c**2 / (3 * N0 * z * g**2 * cE**2 * (1 - rho))


def tc_shape(p, omegaD, M, c, N0, z, g, cE, rho):
    """R3.2: T* = p hbar omegaD/kB exp[-exponent]（取 hbar/kB=1 的归一化形状）"""
    return p * omegaD * np.exp(-exponent_r31(M, c, N0, z, g, cE, rho))


def tc_chain(lam_chain, omegaD):
    """链登记形状 T* = 1.13 e^{-3/2} omegaD exp(-1/lambda_chain)"""
    return L113_E * omegaD * np.exp(-1 / lam_chain)


def assertions():
    out = {}
    base = dict(N0=1.0, z=8.0, g=1.0, cE=1.0, rho=0.4, Q=1.0, M=1.0, c=3.0)
    omD = base["c"] * base["Q"]
    lam = lambda_geom(N0=base["N0"], z=base["z"], g=base["g"], cE=base["cE"],
                      rho=base["rho"], Q=base["Q"], M=base["M"], omegaD=omD)
    out["lambda_geom"] = float(lam)

    # (R3.1) 数值恒等
    lhs = 2 / lam
    rhs = exponent_r31(base["M"], base["c"], base["N0"], base["z"],
                       base["g"], base["cE"], base["rho"])
    out["R31_relerr"] = float(abs(lhs - rhs) / abs(lhs))

    # (R3.3) 归一映射
    out["normalization_map_relerr"] = float(abs(2 / (2 * lam) - 1 / lam) / abs(1 / lam))

    # 归一映射后两式逐因子一致
    t1 = tc_shape(L113_E, omD, base["M"], base["c"], base["N0"],
                  base["z"], base["g"], base["cE"], base["rho"])
    t2 = tc_chain(lam / 2, omD)
    out["shape_match_relerr"] = float(abs(t1 - t2) / abs(t2))

    # 同位素：T(M)/T(M0) = (M/M0)^(-1/2)（c ~ M^{-1/2}, omegaD ~ M^{-1/2}）
    Ms = np.array([1.0, 2.0, 4.0])
    ratios = []
    for m in Ms:
        cm = base["c"] / np.sqrt(m)
        omm = cm * base["Q"]
        ratios.append(tc_shape(L113_E, omm, m, cm, base["N0"], base["z"],
                               base["g"], base["cE"], base["rho"]) / t1)
    out["isotope_exponent"] = float(np.log(ratios[-1]) / np.log(Ms[-1]))
    out["isotope_target"] = -0.5

    # 单调方向
    cE2s = np.array([0.3, 0.5, 0.7, 0.9])
    tc_cE = [tc_shape(L113_E, omD, base["M"], base["c"], base["N0"], base["z"],
                      base["g"], c, base["rho"]) for c in cE2s]
    out["tc_increasing_in_cE2"] = bool(np.all(np.diff(tc_cE) > 0))
    rhos = np.array([0.1, 0.4, 0.7, 0.9])
    tc_rho = [tc_shape(L113_E, omD, base["M"], base["c"], base["N0"], base["z"],
                       base["g"], base["cE"], r) for r in rhos]
    out["tc_decreasing_in_rho"] = bool(np.all(np.diff(tc_rho) < 0))
    return out


def plots(a):
    base = dict(N0=1.0, z=8.0, g=1.0, cE=1.0, rho=0.4, Q=1.0, M=1.0, c=3.0)
    omD = base["c"] * base["Q"]
    lam0 = lambda_geom(N0=base["N0"], z=base["z"], g=base["g"], cE=base["cE"],
                       rho=base["rho"], Q=base["Q"], M=base["M"], omegaD=omD)
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) T* vs lambda_geom（指数灵敏度）+ 链形状对照
    ax = axes[0, 0]
    lams = np.linspace(0.5, 3.0, 300)
    t_shape = L113_E * omD * np.exp(-2 / lams)
    t_chain = tc_chain(lams / 2, omD)
    ax.plot(lams, t_shape, "b-", lw=2.5, label=r"拉通形状 $e^{-2/\lambda_{\rm geom}}$")
    ax.plot(lams, t_chain, "r--", lw=1.5, label=r"链 (目标.2) $e^{-1/\lambda_{\rm chain}}$")
    ax.set_yscale("log")
    ax.set_xlabel(r"$\lambda_{\rm geom}$")
    ax.set_ylabel(r"$T^\ast$（归一化）")
    ax.set_title("(a) 指数灵敏度：归一映射后两式重合")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) T* vs c_eps^2（亏角涨落）
    ax = axes[0, 1]
    cEs = np.linspace(0.3, 1.0, 300)
    tcE = [tc_shape(L113_E, omD, base["M"], base["c"], base["N0"], base["z"],
                    base["g"], ce, base["rho"]) for ce in cEs]
    ax.plot(cEs**2, tcE, "g-", lw=2)
    ax.set_yscale("log")
    ax.set_xlabel(r"$c_\varepsilon^2$（亏角涨落强度）")
    ax.set_ylabel(r"$T^\ast$（归一化）")
    ax.set_title("(b) T* 随亏角涨落指数上升")
    ax.grid(alpha=0.3)

    # (c) T* vs rho（关联）
    ax = axes[1, 0]
    rhos = np.linspace(0.0, 0.95, 300)
    trho = [tc_shape(L113_E, omD, base["M"], base["c"], base["N0"], base["z"],
                     base["g"], base["cE"], r) for r in rhos]
    ax.plot(rhos, trho, "purple", lw=2)
    ax.set_yscale("log")
    ax.set_xlabel(r"关联 $\rho$")
    ax.set_ylabel(r"$T^\ast$（归一化）")
    ax.set_title("(c) T* 随关联 rho -> 1 而趋零")
    ax.grid(alpha=0.3)

    # (d) 同位素
    ax = axes[1, 1]
    M = np.linspace(1, 4, 300)
    ratio = []
    for m in M:
        cm = base["c"] / np.sqrt(m)
        omm = cm * base["Q"]
        ratio.append(tc_shape(L113_E, omm, m, cm, base["N0"], base["z"],
                              base["g"], base["cE"], base["rho"]) / a["ref"])
    ax.loglog(M, ratio, "orange", lw=2, label=r"$T^\ast(M)/T^\ast(M_0)$")
    ax.loglog(M, M**-0.5, "k--", lw=1.5, label=r"$M^{-1/2}$")
    ax.set_xlabel(r"$M/M_0$")
    ax.set_ylabel(r"$T^\ast$ 比")
    ax.set_title("(d) 同位素端点 alpha = 1/2")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R3: 环 4→10→12→14→环节⑨ 拉通（无拟合）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "全链R1R2拉通.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    base = dict(N0=1.0, z=8.0, g=1.0, cE=1.0, rho=0.4, Q=1.0, M=1.0, c=3.0)
    a["ref"] = tc_shape(L113_E, base["c"] * base["Q"], base["M"], base["c"],
                        base["N0"], base["z"], base["g"], base["cE"], base["rho"])
    print("=== R3 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "全链R1R2拉通_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
