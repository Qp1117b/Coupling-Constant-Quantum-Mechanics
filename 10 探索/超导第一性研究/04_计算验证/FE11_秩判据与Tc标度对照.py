# -*- coding: utf-8 -*-
"""
FE11（候选·未落地）：秩判据 vs T_c 的 lambda 扫描对照。
检验对象：第 164–166 轮遗留读法——"张量秩 / 乘法条数可作相变判据"。

做法（两把尺子，同一 lambda 网格，无拟合）：
  (1) 秩侧：Strassen 2x2 乘法算法（7 条乘法）对 lambda*T 逐点复算残差，
      并给出代数恒等 rank(lambda T)=rank(T)（lambda != 0）的数值旁证；
  (2) 物理侧：BCS 型 T_c = 1.13 * omega_D * exp(-1/lambda)（外部 B 类标准对照），
      omega_D 归一为 1，只看 lambda 依赖的形状与量级；
  (3) 失配度：T_c(lambda)/T_c(lambda_ref) 与秩判据的常数 1 对比。

仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE11_秩判据与Tc标度对照.py"
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
LAM = np.linspace(0.05, 0.9, 400)
LAM_REF = 0.5
RANK_222 = 7  # <2,2,2> 的秩 = 7（Winograd 1971；Strassen 7 乘法算法即上界）


def strassen(A, B):
    """Strassen 7 乘法版 2x2 矩阵乘（纯 python/numpy 标量，逐条计数）。"""
    a11, a12 = A[0, 0], A[0, 1]
    a21, a22 = A[1, 0], A[1, 1]
    b11, b12 = B[0, 0], B[0, 1]
    b21, b22 = B[1, 0], B[1, 1]
    m1 = (a11 + a22) * (b11 + b22)
    m2 = (a21 + a22) * b11
    m3 = a11 * (b12 - b22)
    m4 = a22 * (b21 - b11)
    m5 = (a11 + a12) * b22
    m6 = (a21 - a11) * (b11 + b12)
    m7 = (a12 - a22) * (b21 + b22)
    C = np.array([[m1 + m4 - m5 + m7, m3 + m5],
                  [m2 + m4, m1 - m2 + m3 + m6]], dtype=float)
    return C


def residual_scan():
    """lambda 网格上均用 7 条乘法复算 lambda*(A@B)，取最大残差。"""
    rng = np.random.default_rng(20261125)
    res = []
    for lam in np.linspace(0.05, 4.0, 40):
        worst = 0.0
        for _ in range(8):
            A = rng.normal(size=(2, 2))
            B = rng.normal(size=(2, 2))
            # 把 lambda 折进输入，乘数条数仍为 7（乘法条数不随 lambda 变）
            C = strassen(lam * A, B)
            worst = max(worst, float(np.max(np.abs(C - lam * (A @ B))))
                        / max(1.0, float(np.max(np.abs(lam * (A @ B)))))
                        )
        res.append([float(lam), worst])
    return res


def tc_bcs(lam):
    """BCS 型临界温度（omega_D 归一到 1，只作 lambda 依赖形状的外部对照）。"""
    return 1.13 * np.exp(-1.0 / lam)


def main():
    res = residual_scan()
    lam_res = np.array([r[0] for r in res])
    res_max = np.array([r[1] for r in res])

    tc = tc_bcs(LAM)
    tc_ref = float(tc_bcs(LAM_REF))
    ratio = tc / tc_ref

    sel = [0.10, 0.20, 0.30, 0.50, 0.70, 0.90]
    span_decades = float(abs(np.log10(ratio.min() / ratio.max())))

    fig, ax = plt.subplots(1, 3, figsize=(15.2, 4.6))

    # (a) 秩侧：乘法条数 / 残差
    ax0 = ax[0]
    ax0.semilogy(lam_res, np.maximum(res_max, 1e-18), "o", ms=4.2,
                 color="#1f77b4", label="7 乘法复算的最大相对残差（浮点噪声）")
    ax0.set_ylim(1e-17, 1e-12)
    ax0.set_xlabel(r"耦合缩放 $\lambda$")
    ax0.set_ylabel("相对残差（对数）")
    ax0.set_title("(a) 秩侧：乘法条数恒为 7，与 $\\lambda$ 无关")
    ax0.grid(alpha=0.25, which="both")
    axr = ax0.twinx()
    axr.plot([0.05, 4.0], [RANK_222, RANK_222], "--", color="#d62728", lw=1.8,
             label=r"$\mathrm{rank}(\lambda T)=\mathrm{rank}(T)=7$")
    axr.set_ylim(0, 14)
    axr.set_ylabel("秩 / 乘法条数")
    ax0.legend(loc="upper left", fontsize=8)
    axr.legend(loc="lower right", fontsize=8)

    # (b) 物理侧：T_c(lambda)
    ax1 = ax[1]
    ax1.semilogy(LAM, tc, "-", color="#2ca02c", lw=2,
                 label=r"$T_c/\omega_D=1.13\,e^{-1/\lambda}$（BCS，B 类）")
    ax1.axvline(LAM_REF, color="0.6", ls=":", lw=1)
    ax1.set_xlabel(r"$\lambda$")
    ax1.set_ylabel(r"$T_c/\omega_D$（对数）")
    ax1.set_title("(b) 物理侧：$T_c$ 对 $\\lambda$ 非解析依赖")
    ax1.grid(alpha=0.25, which="both")
    ax1.legend(fontsize=8, loc="upper left")

    # (c) 失配：比值 vs 常数 1
    ax2 = ax[2]
    ax2.semilogy(LAM, ratio, "-", color="#9467bd", lw=2,
                 label=r"$T_c(\lambda)/T_c(0.5)$")
    ax2.axhline(1.0, color="#d62728", ls="--", lw=1.8, label="秩判据预测（常数 1）")
    ax2.set_xlabel(r"$\lambda$")
    ax2.set_ylabel("比值（对数）")
    ax2.set_title(f"(c) 失配 {span_decades:.1f} 个数量级")
    ax2.grid(alpha=0.25, which="both")
    ax2.legend(fontsize=8, loc="upper left")

    fig.suptitle("FE11：以秩/乘法条数为相变判据，则 $T_c$ 应与 $\\lambda$ 无关；实况非解析", fontsize=12)
    fig.tight_layout()
    out_png = os.path.join(HERE, "FE11_秩判据与Tc标度对照.png")
    fig.savefig(out_png, dpi=150)
    plt.close(fig)

    data = {
        "candidate": "FE11",
        "note": "候选层对照检验；不改主链/06/08；物理侧用 BCS 作 B 类外部对照，omega_D 归一为 1",
        "rank_222": RANK_222,
        "rank_identity": "rank(lambda*T)=rank(T) for lambda!=0（代数恒等，非拟合）",
        "residual_max_rel": float(max(res_max)),
        "lambda_residual_span": [float(lam_res.min()), float(lam_res.max())],
        "lambda_grid_span": [float(LAM.min()), float(LAM.max())],
        "tc_over_omegaD": {f"{l:.2f}": float(tc_bcs(l)) for l in sel},
        "ratio_vs_lambda_ref": {f"{l:.2f}": float(tc_bcs(l) / tc_ref) for l in sel},
        "lambda_ref": LAM_REF,
        "span_decades_over_grid": span_decades,
        "verdict": "秩判据在 lambda 上平坦；T_c 跨量级变化 ⇒ 二者不能是同一判据",
    }
    out_json = os.path.join(HERE, "FE11_秩判据与Tc标度对照.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(json.dumps(data, ensure_ascii=False, indent=2))
    print("图片:", out_png)


if __name__ == "__main__":
    main()
