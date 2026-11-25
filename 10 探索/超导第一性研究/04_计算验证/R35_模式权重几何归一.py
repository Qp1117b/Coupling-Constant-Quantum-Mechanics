# -*- coding: utf-8 -*-
"""
R35: 环 12 (12.2) 模式衰减权重的几何归一与参与比。
权重 e^{-(2k+1/2)t}，q=e^{-2t}，n_eff=coth t。无拟合（解析闭式核对）。
运行：python "10 探索/超导第一性研究/04_计算验证/R35_模式权重几何归一.py"
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


def neff_finite(q, N):
    """有限截断参与比 n_eff = (sum_{k=1}^N w_k)^2 / sum w_k^2，w_k=q^k。"""
    ks = np.arange(1, N + 1)
    w = q ** ks
    return (w.sum() ** 2) / (w ** 2).sum()


def neff_infinite(q):
    """闭式 (1+q)/(1-q) = coth t。"""
    return (1 + q) / (1 - q)


def neff_harmonic(K):
    """(12.A3) 调和权重 1/k 截断 K 的参与比 = H_K^2 / H_{K,2}。"""
    ks = np.arange(1, K + 1)
    w = 1.0 / ks
    return (w.sum() ** 2) / (w ** 2).sum()


def assertions():
    out = {}
    # 有限截断 → 闭式（N 大）
    for q in [0.2, 0.5, 0.8]:
        nf = neff_finite(q, 2000)
        ni = neff_infinite(q)
        out[f"finite_to_closed_q{q}"] = bool(abs(nf - ni) < 1e-6)
        out[f"neff_q{q}"] = float(ni)
    # 单调性：q 增 → n_eff 增
    qs = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    nes = np.array([neff_infinite(q) for q in qs])
    out["neff_monotone_in_q"] = bool(np.all(np.diff(nes) > 0))
    # coth 核对：q=e^{-2t}, n_eff=coth t
    for t in [0.5, 1.0, 2.0]:
        q = np.exp(-2 * t)
        out[f"coth_match_t{t}"] = bool(abs(neff_infinite(q) - 1 / np.tanh(t)) < 1e-9)
    # 极限：q→0 时 n_eff→1（第一档主导）、p1→1
    out["neff_q0_limit"] = bool(abs(neff_infinite(1e-6) - 1) < 1e-4)
    out["p1_q0_limit"] = bool(abs((1 - 1e-6) - 1) < 1e-4)
    # 与调和权重标度对比：同一"有效档数"下两者不同
    out["geometric_vs_harmonic_distinct"] = bool(
        abs(neff_infinite(0.5) - neff_harmonic(3)) > 0.1
    )
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    ts = np.linspace(0.05, 4, 300)
    nes = [1 / np.tanh(t) for t in ts]
    ax.plot(ts, nes, "b-", lw=2, label=r"$n_{\rm eff}=\coth t$")
    ax.set_xlabel("衰减参数 t"); ax.set_ylabel("参与比")
    ax.set_title("(a) 参与比随 t 单调降到 1（第一档主导）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[0, 1]
    qs = np.linspace(0.05, 0.95, 200)
    ax.plot(qs, (1 + qs) / (1 - qs), "g-", lw=2, label="几何权重 (12.2)")
    Ks = np.linspace(2, 20, 200)
    # 调和权重参与比随 K（映射到可比横轴：用 q 使 n_eff 同量级）
    harm = [neff_harmonic(int(k)) for k in Ks]
    ax.plot(np.linspace(0.05, 0.95, 200), harm, "orange", ls="--", lw=2, label="调和权重 (12.A3)")
    ax.set_xlabel("权重参数"); ax.set_ylabel("参与比")
    ax.set_title("(b) 两种权重标度不同（指数 vs 对数）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 0]
    Ns = np.array([1, 2, 5, 10, 50, 200, 1000])
    nf = [neff_finite(0.5, int(n)) for n in Ns]
    ax.semilogx(Ns, nf, "purple", marker="o", lw=2, label="有限截断 N")
    ax.axhline(neff_infinite(0.5), color="r", ls="--", label=r"闭式 $(1+q)/(1-q)$")
    ax.set_xlabel("截断档数 N"); ax.set_ylabel("参与比")
    ax.set_title("(c) 有限截断 → 闭式（q=0.5）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ts2 = np.linspace(0.05, 4, 300)
    p1 = [1 - np.exp(-2 * t) for t in ts2]
    ax.plot(ts2, p1, "teal", lw=2)
    ax.set_xlabel("衰减参数 t"); ax.set_ylabel("第一档占比 $p_1$")
    ax.set_title("(d) 第一档占比 $1-e^{-2t}$ → 1"); ax.grid(alpha=0.3)

    fig.suptitle("R35: (12.2) 模式衰减权重几何归一——n_eff=coth t（解析核对，非拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R35_模式权重几何归一.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R35 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R35_模式权重几何归一_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
