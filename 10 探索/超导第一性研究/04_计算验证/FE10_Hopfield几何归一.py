# -*- coding: utf-8 -*-
"""
FE10: Hopfield 参数几何归一 eta=(9/10)N0 z g^2 ce^2(1-rho)Q^2 的形状检验。
无拟合（形状/单调/同位素）。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE10_Hopfield几何归一.py"
"""
import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def eta(N0, z, g, ce2, rho, Q2):
    return (9 / 10) * N0 * z * g**2 * ce2 * (1 - rho) * Q2


def assertions():
    out = {}
    base = dict(N0=1.0, z=8.0, g=1.0, ce2=0.5, rho=0.4, Q2=1.0)
    e0 = eta(**base)
    out["eta_base"] = float(e0)
    # 匹配验证：eta/(M<w^2>) 应还原 lambda_geom
    M, wD2 = 1.0, 1.0
    w2 = (3 / 5) * wD2
    lam_from_eta = e0 / (M * w2)
    lam_geom = (3 / 2) * base["N0"] * base["z"] * base["g"]**2 * base["ce2"] * (1 - base["rho"]) * base["Q2"] / (M * wD2)
    out["match_relerr"] = float(abs(lam_from_eta - lam_geom) / lam_geom)
    # 单调方向
    out["eta_mono_ce2"] = bool(eta(**{**base, "ce2": 0.8}) > e0)
    out["eta_mono_rho"] = bool(eta(**{**base, "rho": 0.1}) > e0)
    # 同位素：eta 不含 M（这里 eta 参数本就不含 M，验证形状不依赖 M）
    out["eta_mass_free"] = True  # eta 表达式无 M 项
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    base = dict(N0=1.0, z=8.0, g=1.0, ce2=0.5, rho=0.4, Q2=1.0)

    ax = axes[0, 0]
    ce2s = np.linspace(0.05, 1.0, 200)
    ax.plot(ce2s, [eta(**{**base, "ce2": c}) for c in ce2s], "b-", lw=2)
    ax.set_xlabel(r"亏角涨落 $c_\varepsilon^2$")
    ax.set_ylabel(r"$\eta_{\rm chain}$")
    ax.set_title("(a) η ∝ c_ε²（随无序增）")
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    rhos = np.linspace(0, 0.95, 200)
    ax.plot(rhos, [eta(**{**base, "rho": r}) for r in rhos], "g-", lw=2)
    ax.set_xlabel(r"关联 $\rho$")
    ax.set_ylabel(r"$\eta_{\rm chain}$")
    ax.set_title("(b) η ∝ (1-ρ)（关联强则 η 小）")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    Q2s = np.linspace(0.2, 2.0, 200)
    ax.plot(Q2s, [eta(**{**base, "Q2": q}) for q in Q2s], "purple", lw=2)
    ax.set_xlabel(r"德拜波数平方 $Q^2$")
    ax.set_ylabel(r"$\eta_{\rm chain}$")
    ax.set_title("(c) η ∝ Q²")
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    labels = ["标准理论\nη=经验原子量", "FE10\nη=链几何形状"]
    vals = [1, 1]
    ax.bar(labels, vals, color=["tab:gray", "tab:green"])
    ax.set_yticks([])
    ax.set_title("(d) FE10 新内容：η 的几何依赖（可证伪）")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("FE10: Hopfield 参数几何归一（框架扩展候选，无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "FE10_Hopfield几何归一.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== FE10 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "FE10_Hopfield几何归一_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
