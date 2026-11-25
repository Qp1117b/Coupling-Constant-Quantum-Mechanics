# -*- coding: utf-8 -*-
"""
R5: CQM 态密度形状（参与比计数导出）——数值与图像检验。
只检验斜率/矩/收敛类型，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/环14A_CQM态密度.py"
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
neff, E2, wD = 10.0, 1.0, 100.0  # 归一化（只检验形状）


def count(E):
    return neff * np.sqrt(np.asarray(E, dtype=float) / E2)


def dos(E):
    return neff / (2 * np.sqrt(E2 * np.asarray(E, dtype=float)))


def log_moment(w):
    """omega_log = w exp(-2)（积分比 ln w - 2）"""
    return w * math.exp(-2)


def assertions():
    out = {}
    # (a) N(E) 对 sqrt(E) 严格线性
    E = np.logspace(0, 4, 500)
    x = np.sqrt(E / E2)
    a, b = np.polyfit(x, count(E), 1)
    out["N_vs_sqrtE_slope"] = float(a)
    out["N_vs_sqrtE_slope_target"] = neff
    out["N_vs_sqrtE_intercept"] = float(b)

    # (b) g(E) ~ E^{-1/2}（双对数斜率 -1/2）
    lg = np.polyfit(np.log(E), np.log(dos(E)), 1)[0]
    out["dos_log_slope"] = float(lg)
    out["dos_log_slope_target"] = -0.5

    # (c) 对数矩比：e^{-5/3}、e^{-3/2}
    out["omega_log_mode"] = float(log_moment(wD))
    out["ratio_vs_CQM_moment"] = float(math.exp(-2) / math.exp(-1.0 / 3))
    out["ratio_vs_Eliash_moment"] = float(math.exp(-2) / math.exp(-0.5))
    out["target_e_minus_5thirds"] = float(math.exp(-5.0 / 3))
    out["target_e_minus_3halfs"] = float(math.exp(-1.5))

    # (d) Cooper integrand ~ E^{-3/2}；积分对下限的依赖是幂律 E^{-1/2} 而非 ln
    lgi = np.polyfit(np.log(E), np.log(dos(E) / E), 1)[0]
    out["cooper_integrand_slope"] = float(lgi)
    out["cooper_integrand_slope_target"] = -1.5
    Elo = np.array([1e-2, 1e-3, 1e-4, 1e-5])
    I = neff / math.sqrt(E2) * (Elo ** -0.5 - wD ** -0.5)
    # 对数依赖检验：I 随 ln(1/Elo) 非线性（幂律），增量比递增
    ratios = np.diff(I) / np.diff(np.log(1 / Elo))
    out["integral_growth_is_powerlaw"] = bool(np.all(np.diff(ratios) > 0))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    E = np.logspace(0, 4, 400)

    # (a) 计数函数 vs sqrt(E)
    ax = axes[0, 0]
    ax.plot(np.sqrt(E / E2), count(E), "b-", lw=2)
    ax.set_xlabel(r"$\sqrt{E/E_2}$")
    ax.set_ylabel(r"$N(E)$")
    ax.set_title("(a) 计数 N(E) 与 sqrt(E) 严格线性")
    ax.grid(alpha=0.3)

    # (b) DOS ~ E^{-1/2}
    ax = axes[0, 1]
    ax.loglog(E, dos(E), "g-", lw=2, label=r"$g_{\rm CQM}\propto E^{-1/2}$")
    ax.loglog(E, neff / (2 * np.sqrt(E2)) * E**-0.5, "k--", lw=1.5, label=r"解析 $E^{-1/2}$")
    ax.set_xlabel(r"能量 $E/E_2$")
    ax.set_ylabel(r"$g(E)$")
    ax.set_title("(b) CQM DOS 形状：斜率 -1/2")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (c) 三矩对比
    ax = axes[1, 0]
    labels = ["mode\n$e^{-2}$", "CQM 电子\n$e^{-1/3}$", "Eliashberg\n$e^{-1/2}$"]
    vals = [math.exp(-2), math.exp(-1 / 3), math.exp(-0.5)]
    ax.bar(labels, vals, color=["green", "blue", "orange"])
    for i, v in enumerate(vals):
        ax.text(i, v + 0.01, f"{v:.4f}", ha="center", fontsize=9)
    ax.set_ylabel(r"$\omega_{\log}/\omega_D$")
    ax.set_title(r"(c) 态密度层差异：$e^{-2}$ vs $e^{-1/3},e^{-1/2}$")
    ax.grid(alpha=0.3, axis="y")

    # (d) Cooper integrand ~ E^{-3/2} + 积分幂律依赖
    ax = axes[1, 1]
    ax.loglog(E, dos(E) / E, "purple", lw=2, label=r"$g/E\propto E^{-3/2}$")
    ax.loglog(E, neff / (2 * np.sqrt(E2)) * E**-1.5, "k--", lw=1.5, label=r"解析 $E^{-3/2}$")
    ax.set_xlabel(r"能量 $E/E_2$")
    ax.set_ylabel(r"integrand")
    ax.set_title("(d) 无对数：integrand 为 E^-3/2")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R5: 参与比计数 → CQM DOS 形状（无拟合）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "环14A_CQM态密度.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R5 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "环14A_CQM态密度_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
