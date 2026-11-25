# -*- coding: utf-8 -*-
"""
R6: 元素实验数据检验链的两条 A 类形状——gap ratio 3.528 与同位素端点 0.5。
预注册判据见 07_数据与现象/预注册判定_R6.md；不拟合、不反解、不调参。
仅用标准库 + numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/数据对照_能隙比与同位素.py"
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
DATA = os.path.join(os.path.dirname(HERE), "06_数据对照", "实验数据_元素.csv")
KB_EV_K = 8.617333262e-5  # 玻尔兹曼常数 eV/K（CODATA 外部常数）
RATIO_PRED = 2 * math.pi / math.exp(0.5772156649015329)  # 2pi/e^gamma ≈ 3.528
WEAK_THRESHOLD = 0.02  # 预注册写死的弱耦合代理阈值


def load():
    rows = []
    with open(DATA, "r", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            Tc = float(r["Tc_K"])
            thD = float(r["thetaD_K"])
            d2 = float(r["twoDelta_meV"])  # meV
            ratio = (d2 * 1e-3) / (KB_EV_K * Tc)
            alpha = float(r["alpha_measured"]) if r["alpha_measured"] else None
            rows.append(dict(el=r["element"], Tc=Tc, thD=thD,
                             tc_th=Tc / thD, ratio=ratio, alpha=alpha))
    return rows


def verify(rows):
    out = {}
    weak = [r for r in rows if r["tc_th"] < WEAK_THRESHOLD]
    strong = [r for r in rows if r["tc_th"] >= WEAK_THRESHOLD]
    out["weak_n"] = len(weak)
    out["strong_n"] = len(strong)
    out["weak_elements"] = ",".join(r["el"] for r in weak)
    out["strong_elements"] = ",".join(r["el"] for r in strong)

    ratios_weak = np.array([r["ratio"] for r in weak])
    out["weak_mean_ratio"] = float(np.mean(ratios_weak))
    out["weak_std_ratio"] = float(np.std(ratios_weak))
    out["weak_relerr_vs_3p528"] = float(abs(np.mean(ratios_weak) - RATIO_PRED) / RATIO_PRED)
    out["weak_pass_8pct"] = bool(out["weak_relerr_vs_3p528"] <= 0.08)
    out["ratio_pred"] = float(RATIO_PRED)

    # 强耦合预注册允许偏离（仅记录，不判失败）
    out["strong_mean_ratio"] = float(np.mean([r["ratio"] for r in strong])) if strong else float("nan")

    # 同位素端点
    alphas = [(r["el"], r["alpha"]) for r in rows if r["alpha"] is not None]
    out["alpha_n"] = len(alphas)
    out["alpha_mean"] = float(np.mean([a for _, a in alphas]))
    highTc = [a for el, a in alphas if next(r["Tc"] for r in rows if r["el"] == el) >= 2.0]
    out["alpha_highTc_mean"] = float(np.mean(highTc))
    out["alpha_endpoint_pass"] = bool(0 < out["alpha_highTc_mean"] <= 0.55)
    return out, rows, weak, strong


def plots(rows, weak, strong, out):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) gap ratio vs Tc/thetaD（Webb Fig 6 口径）
    ax = axes[0, 0]
    ax.scatter([r["tc_th"] for r in rows], [r["ratio"] for r in rows],
               c=["tab:red" if r in strong else "tab:blue" for r in rows], s=55, zorder=5)
    for r in rows:
        ax.annotate(r["el"], (r["tc_th"], r["ratio"]), fontsize=7,
                    xytext=(3, 3), textcoords="offset points")
    ax.axhline(RATIO_PRED, color="k", ls="--", lw=1.5, label=r"链 C5：$2\pi/e^\gamma\approx3.528$")
    ax.axvline(WEAK_THRESHOLD, color="gray", ls=":", lw=1.5, label="弱耦合代理阈值 0.02")
    ax.set_xlabel(r"$T_c/\theta_D$")
    ax.set_ylabel(r"$2\Delta(0)/k_BT_c$")
    ax.set_title("(a) gap ratio vs Tc/thetaD（Webb Fig6 口径）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 弱耦合子集柱状
    ax = axes[0, 1]
    names = [r["el"] for r in weak]
    vals = [r["ratio"] for r in weak]
    ax.bar(names, vals, color="tab:blue")
    ax.axhline(RATIO_PRED, color="k", ls="--", lw=1.5, label="3.528")
    ax.axhspan(RATIO_PRED * 0.92, RATIO_PRED * 1.08, color="green", alpha=0.12, label="±8% 判据窗")
    ax.set_ylabel(r"$2\Delta/k_BT_c$")
    ax.set_title("(b) 弱耦合子集：均值 %.3f（偏差 %.1f%%）"
                 % (out["weak_mean_ratio"], 100 * out["weak_relerr_vs_3p528"]))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    # (c) 同位素 alpha vs Tc
    ax = axes[1, 0]
    alphas = [(r["el"], r["Tc"], r["alpha"]) for r in rows if r["alpha"] is not None]
    ax.scatter([t for _, t, _ in alphas], [a for _, _, a in alphas],
               c="tab:green", s=55, zorder=5)
    for el, t, a in alphas:
        ax.annotate(el, (t, a), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.axhline(0.5, color="k", ls="--", lw=1.5, label=r"链端点 $\alpha=1/2$")
    ax.axhline(0.0, color="gray", ls=":", lw=1.5, label=r"另一端点 $\alpha=0$")
    ax.set_xlabel(r"$T_c$ (K)")
    ax.set_ylabel(r"实测 $\alpha$")
    ax.set_title("(c) 同位素端点：高 Tc 聚 0.5，低 Tc 趋 0")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (d) 判据对弱耦合阈值的稳健性（扫描阈值只显示稳健性，不用于选参）
    ax = axes[1, 1]
    thr = np.linspace(0.005, 0.06, 100)
    means = []
    for t in thr:
        sub = [r["ratio"] for r in rows if r["tc_th"] < t]
        means.append(np.mean(sub) if sub else float("nan"))
    ax.plot(thr, means, "purple", lw=2)
    ax.axhline(RATIO_PRED, color="k", ls="--", lw=1.5)
    ax.axvline(WEAK_THRESHOLD, color="gray", ls=":", lw=1.5)
    ax.set_xlabel(r"弱耦合代理阈值 $T_c/\theta_D$")
    ax.set_ylabel(r"子集均值 gap ratio")
    ax.set_title("(d) 判据稳健性（阈值 0.02 预注册固定）")
    ax.grid(alpha=0.3)

    fig.suptitle("R6: 元素实验数据检验链的两条 A 类形状（无拟合、无反解）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "数据对照_能隙比与同位素.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    rows = load()
    out, rows, weak, strong = verify(rows)
    print("=== R6 数据对照（预注册判据） ===")
    for k, v in out.items():
        print(f"{k:32s} = {v}")
    p = plots(rows, weak, strong, out)
    path = os.path.join(HERE, "数据对照_能隙比与同位素_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in out.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n判定表: {path}")
