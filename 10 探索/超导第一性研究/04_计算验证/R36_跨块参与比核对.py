# -*- coding: utf-8 -*-
"""
R36: 跨块兼容性核对——R31 调和权重 vs R35 几何权重的参与比标度。
同一 n_eff 下反解支撑规模，检验可区分性。无拟合（解析标度核对）。
运行：python "10 探索/超导第一性研究/04_计算验证/R36_跨块参与比核对.py"
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
ZETA2 = math.pi ** 2 / 6


def k_harm_exact(n):
    """调和权重 n_eff=H_K²/H_{K,2}，数值反解最小 K 使 n_eff>=n。"""
    H1 = H2 = 0.0
    for k in range(1, 10_000_000):
        H1 += 1.0 / k
        H2 += 1.0 / (k * k)
        ne = H1 * H1 / H2
        if ne >= n:
            return k
    return None


def k_harm_asym(n):
    """渐近 K ≈ exp(sqrt(n ζ(2)))。"""
    return math.exp(math.sqrt(n * ZETA2))


def k_geom(n):
    """几何权重 n_eff=coth t，有效模数 ≈ n（第一档占比 2/(n+1)）。"""
    return n


def q_from_n(n):
    return (n - 1) / (n + 1)


def assertions():
    out = {}
    # 几何反解：nEff(q(n)) = n
    for n in [1.5, 3.0, 10.0]:
        q = q_from_n(n)
        neff = (1 + q) / (1 - q)
        out[f"geom_inverse_n{n}"] = bool(abs(neff - n) < 1e-9)
    # q 范围 0<q<1
    out["q_range"] = bool(0 < q_from_n(3) < 1)
    # 第一档占比 2/(n+1)
    out["p1_formula"] = bool(abs((1 - q_from_n(10)) - 2 / 11) < 1e-12)
    # 调和精确 vs 渐近：渐近式只在 n 大时成立（小 n 有欧拉常数偏移，高估）
    for n in [10, 50, 200]:
        ke = k_harm_exact(n)
        ka = k_harm_asym(n)
        out[f"harm_exact_n{n}"] = ke
        out[f"K_harm_asym_n{n}"] = round(ka, 1)
    # 渐近适用域：用含欧拉常数的高精度近似 H_K≈ln K+γ+1/(2K), H_{K,2}≈ζ(2)-1/K
    GAMMA = 0.5772156649
    def ne_asym(K):
        H1 = math.log(K) + GAMMA + 1 / (2 * K)
        H2 = ZETA2 - 1 / K
        return H1 * H1 / H2
    err10 = abs(ne_asym(k_harm_asym(10)) - 10) / 10
    err200 = abs(ne_asym(k_harm_asym(200)) - 200) / 200
    out["asym_rel_err_n10"] = round(err10, 4)
    out["asym_rel_err_n200"] = round(err200, 4)
    out["asym_improves_with_n"] = bool(err200 < err10)
    # 可区分比用精确调和反解（渐近式小 n 失真）
    ratios = [k_harm_exact(n) / k_geom(n) for n in [1.5, 3, 10, 50]]
    out["separation_ratios_exact"] = [round(r, 2) for r in ratios]
    # 小 n（近单档）两标度不可区分（1-4 档），大 n 才分叉——这是真实物理结论
    out["small_n_indistinguishable"] = bool(abs(ratios[0] - ratios[1]) < 0.2)
    out["large_n_separable"] = bool(ratios[-1] > 50)
    out["separation_monotone_large_n"] = bool(ratios[2] < ratios[3])  # n=10 < n=50
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    ns = np.linspace(1.1, 50, 300)

    ax = axes[0, 0]
    ax.plot(ns, [k_harm_asym(n) for n in ns], "orange", lw=2, label=r"调和 $e^{\sqrt{n\zeta(2)}}$")
    ax.plot(ns, [k_geom(n) for n in ns], "b-", lw=2, label="几何 ≈ n")
    ax.set_xlabel(r"参与比 $n_{\rm eff}$"); ax.set_ylabel("所需支撑规模 K")
    ax.set_title("(a) 同 n_eff 下两权重标度分叉")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ns_disc = np.array([1.5, 2, 3, 5, 10, 20, 50])
    ratios_exact = np.array([k_harm_exact(n) / k_geom(n) for n in ns_disc])
    ax.semilogy(ns_disc, ratios_exact, "purple", marker="o", lw=2)
    ax.set_xlabel(r"$n_{\rm eff}$"); ax.set_ylabel(r"$K_{\rm harm}/K_{\rm geom}$")
    ax.set_title("(b) 可区分比（精确反解）随 n_eff 增长"); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    for n in [1.5, 3, 10, 50]:
        q = q_from_n(n)
        ks = np.arange(1, 30)
        w = (1 - q) * q ** (ks - 1)
        ax.plot(ks, w, marker="o", ms=3, label=f"n={n}, q={q:.2f}")
    ax.set_xlabel("档序 k"); ax.set_ylabel("归一权重 $p_k$")
    ax.set_title("(c) 几何权重分布（第一档占比 2/(n+1)）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ns2 = np.array([1.5, 3, 10, 50])
    ke = [k_harm_exact(n) for n in ns2]
    ka = [k_harm_asym(n) for n in ns2]
    x = np.arange(len(ns2))
    ax.bar(x - 0.2, ke, 0.4, label="调和精确")
    ax.bar(x + 0.2, ka, 0.4, label="调和渐近")
    ax.set_xticks(x); ax.set_xticklabels([str(n) for n in ns2])
    ax.set_ylabel("K"); ax.set_title("(d) 调和权重：精确 vs 渐近")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R36: 跨块兼容性核对——R31 调和 vs R35 几何参与比标度（非拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R36_跨块参与比核对.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R36 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R36_跨块参与比核对_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
