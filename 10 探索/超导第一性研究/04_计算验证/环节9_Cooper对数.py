# -*- coding: utf-8 -*-
"""
环节⑨ R2：12.A 权重 + 审-15 谱阶梯 -> Cooper 对数核 rho(E) ~ 1/E。
只检验极限/渐近/单调/分支对比，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环节9_Cooper对数.py"
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
GAMMA = 0.5772156649015329  # Euler-Mascheroni（外部数学常数）


def H(K):
    """调和数 H_K = sum_{j=1}^K 1/j"""
    K = np.asarray(K, dtype=np.int64)
    return np.cumsum(1.0 / np.arange(1, K.max() + 1))[K - 1]


def W_charge(E, E2=1.0):
    """荷量子分支 w_k=1/k 的累积权重 W(E)=H_{sqrt(E/E2)}"""
    K = np.sqrt(np.asarray(E, dtype=float) / E2)
    idx = np.clip(np.floor(K).astype(np.int64), 1, 10_000_000)
    return H(idx)


def W_winding(E, E2=1.0):
    """绕数分支 w_k=k 的累积权重 W = K(K+1)/2"""
    K = np.sqrt(np.asarray(E, dtype=float) / E2)
    return K * (K + 1) / 2


def assertions():
    out = {}
    # (a) H_K 渐近 ln K + gamma 的残差随 K 衰减
    Ks = np.array([10, 100, 1000, 10000, 100000])
    resid = H(Ks) - (np.log(Ks.astype(float)) + GAMMA)
    out["H_asymptotic_resid_max"] = float(np.max(np.abs(resid)))
    out["H_resid_at_1e5"] = float(abs(resid[-1]))

    # (b)(c) 分支对比：荷分支在大 E 的对数系数 dW/dlnE -> 1/2；绕分支密度 -> 常数
    # 用对数十进网格（每十倍频一个区间），避开阶梯函数的逐点梯度噪声
    Es = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
    coeff = np.diff(W_charge(Es)) / np.diff(np.log(Es))
    out["charge_log_coeff"] = float(coeff[-1])
    out["charge_log_coeff_target"] = 0.5
    out["charge_coeff_within_1pct"] = bool(abs(coeff[-1] - 0.5) < 0.005)
    Euni = np.linspace(1e4, 1e5, 20000)
    rho_wind = np.gradient(W_winding(Euni), Euni)
    out["winding_rho_rel_dev_from_const"] = float(np.max(np.abs(rho_wind * 2 - 1.0)))

    # (d) 非解析指数 E_lo/E_hi = exp(-2/lambda)
    lams = np.array([0.1, 0.3, 0.5, 1.0])
    out["exp_ratio_lambda0.5"] = float(np.exp(-2 / 0.5))
    out["exp_ratio_lambda1.0"] = float(np.exp(-2 / 1.0))
    out["exp_monotone_increasing"] = bool(np.all(np.diff(np.exp(-2 / lams)) > 0))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) 调和数渐近
    ax = axes[0, 0]
    Ks = np.unique(np.logspace(1, 6, 400).astype(np.int64))
    ax.plot(Ks, H(Ks), "b-", lw=2, label=r"离散 $W=H_K$")
    ax.plot(Ks, np.log(Ks.astype(float)) + GAMMA, "r--", lw=1.5,
            label=r"渐近 $\ln K+\gamma$")
    ax.set_xscale("log")
    ax.set_xlabel(r"档数 $K$")
    ax.set_ylabel(r"累积权重 $W$")
    ax.set_title("(a) W(K) 的调和渐近")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 加权模密度 rho(E) ~ 1/(2E)（对数十进制分箱粗粒化，避开阶梯梯度尖峰）
    ax = axes[0, 1]
    Ebin = np.logspace(2, 6, 41)
    Wbin = W_charge(Ebin)
    rho_bin = np.diff(Wbin) / np.diff(Ebin)
    Ecenter = np.sqrt(Ebin[:-1] * Ebin[1:])
    ax.loglog(Ecenter, rho_bin, "go", ms=4, label=r"粗粒化 $\Delta W/\Delta E$")
    ax.loglog(Ebin, 1 / (2 * Ebin), "k--", lw=1.5, label=r"$1/(2E)$")
    ax.set_xlabel(r"能量 $E/E_2$")
    ax.set_ylabel(r"加权模密度 $\rho$")
    ax.set_title("(b) 核 rho ~ 1/E（斜率 -1）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) 分支对比：荷分支对数增长 vs 绕分支线性增长
    ax = axes[1, 0]
    Es = np.logspace(2, 6, 300)
    ax.plot(Es, W_charge(Es), "b-", lw=2, label=r"荷分支 $w=1/k$：$W\sim\ln E$")
    ax.plot(Es, 0.5 * np.log(Es) + GAMMA, "b:", lw=1.5)
    ax.set_xscale("log")
    ax.set_xlabel(r"能量 $E/E_2$")
    ax.set_ylabel(r"累积权重 $W$")
    ax2 = ax.twinx()
    ax2.plot(Es, W_winding(Es), "r-", lw=2, label=r"绕分支 $w=k$：$W\sim E$")
    ax2.set_ylabel(r"绕分支 $W_{\rm wind}$", color="red")
    ax.set_title("(c) 临-6 分支：只有荷分支给对数")
    ax.legend(loc="upper left", fontsize=8)
    ax2.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 非解析指数
    ax = axes[1, 1]
    lams = np.linspace(0.1, 1.5, 300)
    ax.plot(lams, np.exp(-2 / lams), "purple", lw=2)
    ax.set_xlabel(r"耦合 $\lambda$")
    ax.set_ylabel(r"$E_{\rm lo}/E_{\rm hi}$")
    ax.set_yscale("log")
    ax.set_title("(d) 非解析能标 exp(-2/lambda)")
    ax.grid(alpha=0.3)

    fig.suptitle("R2: 12.A + 审-15 -> Cooper 对数核（无拟合）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环节9_Cooper对数.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


def write_csv(a):
    path = os.path.join(HERE, "环节9_Cooper对数_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    return path


if __name__ == "__main__":
    a = assertions()
    print("=== R2 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    c = write_csv(a)
    print(f"\n图像: {p}")
    print(f"断言表: {c}")
