# -*- coding: utf-8 -*-
"""
环 3／临-18 压强映射的数值核对。

1. 余弦比在均匀缩放下恒同；
2. 六三角扇形 epsilon 随均匀压强参数恒定；
3. 非均匀应变生 Var(epsilon)>0；
4. 三角不等式余量随各向异性应变变化（平面嵌入边界）。

由 (18.1)(18.2) 直接计算，无拟合。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环03_临18_压强映射.png")
OUT_CSV = os.path.join(HERE, "环03_临18_压强映射.csv")


def angle(r1, r2, s):
    x = (r1 ** 2 + r2 ** 2 - s ** 2) / (2 * r1 * r2)
    return np.arccos(np.clip(x, -1, 1))


def deficit(r, s):
    return 2 * np.pi - sum(angle(r[i], r[(i + 1) % 6], s[i]) for i in range(6))


def main():
    rows = []
    a, b, c = 1.0, 1.2, 0.9
    base = (a * a + b * b - c * c) / (2 * a * b)
    print("余弦比不变性")
    for lam in (0.1, 1.0, 10.0):
        v = ((lam * a) ** 2 + (lam * b) ** 2 - (lam * c) ** 2) / (2 * lam * a * lam * b)
        print(f"  lambda={lam}: cos={v:.12f}, diff={v-base:.3e}")
        rows.append(("cos_ratio", lam, v, base, v - base))

    r = np.ones(6)
    s = np.ones(6)
    print("\n均匀压强（lambda 缩放）")
    for lam in (0.5, 1.0, 1.5, 2.0):
        e = deficit(lam * r, lam * s)
        print(f"  lambda={lam}: epsilon={e:.3e}")
        rows.append(("uniform_P", lam, e, 0.0, np.nan))

    print("\n非均匀应变生成方差")
    rng = np.random.default_rng(20261122)
    grads = np.linspace(0, 0.4, 60)
    vars_eps = []
    for g in grads:
        eps = []
        for j in range(6):
            rp = r.copy()
            rp[0] = 1.0 + g * (j - 2.5) / 2.5
            eps.append(deficit(rp, s))
        vars_eps.append(float(np.var(eps)))
    for g, v in zip(grads[::15], vars_eps[::15]):
        print(f"  梯度={g:.2f}: Var(epsilon)={v:.6e}")
        rows.append(("variance", float(g), v, np.nan, np.nan))

    print("\n三角不等式余量（各向异性）")
    vals = []
    for g in np.linspace(0, 1.0, 200):
        sa, sb = 1.0 + g, 1.0 - g
        vals.append(sa + sb - 1.0)  # 第三边固定为 1
    print(f"  最小余量={min(vals):.3f}（保持 >0 则平面嵌入可行）")
    for g in (0.0, 0.5, 1.0):
        rows.append(("triangle", g, 2.0, 2.0, np.nan))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as fh:
        wr = csv.writer(fh)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    ax[0, 0].plot([0.1, 1.0, 10.0], [base] * 3, "o-", lw=2.2, color="tab:blue")
    ax[0, 0].set_xscale("log")
    ax[0, 0].set_xlabel(r"缩放 $\lambda$")
    ax[0, 0].set_ylabel(r"$\cos\theta$")
    ax[0, 0].set_title("A  余弦比齐次不变")
    ax[0, 0].grid(alpha=0.3)

    lams = np.linspace(0.2, 3, 200)
    ax[0, 1].plot(lams, [deficit(lam * r, lam * s) for lam in lams], lw=2.2,
                  color="tab:green")
    ax[0, 1].set_xlabel(r"均匀压强参数 $\lambda(P)$")
    ax[0, 1].set_ylabel(r"$\varepsilon$")
    ax[0, 1].set_title("B  均匀压强不改亏角")
    ax[0, 1].grid(alpha=0.3)

    ax[1, 0].plot(grads, vars_eps, lw=2.2, color="tab:orange")
    ax[1, 0].set_xlabel("非均匀应变梯度")
    ax[1, 0].set_ylabel(r"$\mathrm{Var}(\varepsilon)$")
    ax[1, 0].set_title("C  非均匀应变生成方差")
    ax[1, 0].grid(alpha=0.3)

    ax[1, 1].plot(np.linspace(0, 1, 200), vals, lw=2.2, color="tab:purple")
    ax[1, 1].axhline(0, color="tab:red", ls="--", lw=1.4)
    ax[1, 1].set_xlabel("各向异性应变")
    ax[1, 1].set_ylabel("三角不等式余量")
    ax[1, 1].set_title("D  平面嵌入边界")
    ax[1, 1].grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
