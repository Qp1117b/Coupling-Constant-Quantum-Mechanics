# -*- coding: utf-8 -*-
"""
审-1 no-go 的函数图像核对：对若干 f 族，检查 C_ij=f(tau_i-tau_j)
在 N=3 时逐行和是否可能恒为 1。

结论：只有常数 f 能让行和对任意 tau 不变；而常数 f 又与 C_ii=1 或 C1=1 冲突。
只做形状核对，不拟合。
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
OUT_PNG = os.path.join(HERE, "环07_审1no-go.png")
OUT_CSV = os.path.join(HERE, "环07_审1no-go.csv")

rng = np.random.default_rng(20261122)
TAUS = rng.normal(size=(400, 3))


def f_const(x, c):
    return np.full_like(np.asarray(x, dtype=float), c)


def f_linear(x, k):
    return k * np.asarray(x, dtype=float)


def f_tanh(x, k):
    return np.tanh(k * np.asarray(x, dtype=float))


def f_rational(x, a):
    return 1.0 / (1.0 + a * np.asarray(x, dtype=float) ** 2)


def row_residual(f):
    """返回 max_i |sum_j f(tau_i-tau_j) - 1| 在 400 组随机 tau 上的最大值。"""
    out = []
    for tau in TAUS:
        D = tau[:, None] - tau[None, :]
        M = f(D)
        out.append(np.max(np.abs(M.sum(axis=1) - 1.0)))
    return float(np.max(out))


def main():
    rows = []

    # A: 常数族（唯一能让行和对 tau 不变的候选）
    cs = np.unique(np.concatenate([np.linspace(0.2, 1.6, 100), [1.0 / 3.0]]))
    const_res = [row_residual(lambda x, c=c: f_const(x, c)) for c in cs]
    for c, r in zip(cs, const_res):
        rows.append(("const", c, r))

    # B: 非常数族
    ks = np.linspace(0.1, 3.0, 100)
    for name, fun in [("linear", f_linear), ("tanh", f_tanh), ("rational", f_rational)]:
        res = [row_residual(lambda x, k=k, fun=fun: fun(x, k)) for k in ks]
        for k, r in zip(ks, res):
            rows.append((name, k, r))

    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["family", "param", "max_row_residual"])
        wr.writerows(rows)

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    ax[0].plot(cs, const_res, lw=2.0, color="tab:green", label="常数 $f=c$")
    ax[0].axvline(1.0 / 3.0, color="k", ls="--", lw=1.0,
                  label=r"$c=1/3$（N=3 行和=1）")
    ax[0].set_xlabel("$c$")
    ax[0].set_ylabel("行和残差的最大值")
    ax[0].set_title("A  常数族：只在 $c=1/3$ 行和为 1")
    ax[0].legend(fontsize=8)
    ax[0].grid(alpha=0.3)

    for name, fun in [("linear", f_linear), ("tanh", f_tanh), ("rational", f_rational)]:
        res = [row_residual(lambda x, k=k, fun=fun: fun(x, k)) for k in ks]
        ax[1].semilogy(ks, res, lw=1.8, label=name)
    ax[1].set_xlabel("形状参数")
    ax[1].set_ylabel("行和残差的最大值")
    ax[1].set_title("B  非常数族：残差恒非零（无解）")
    ax[1].legend(fontsize=8)
    ax[1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)

    print(f"constant family min residual = {min(const_res):.6e} at c={cs[int(np.argmin(const_res))]:.4f}")
    for name, fun in [("linear", f_linear), ("tanh", f_tanh), ("rational", f_rational)]:
        res = [row_residual(lambda x, k=k, fun=fun: fun(x, k)) for k in ks]
        print(f"{name}: min residual = {min(res):.6e}")


if __name__ == "__main__":
    main()
