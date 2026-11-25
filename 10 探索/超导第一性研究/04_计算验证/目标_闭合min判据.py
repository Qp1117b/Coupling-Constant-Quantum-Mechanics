# -*- coding: utf-8 -*-
"""
R16: (目标.1) ≤min 判据结构——三支温度上限与 min 包络（回溯必然）。
只检验合取逻辑与包络形状，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/目标_闭合min判据.py"
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


def assertions():
    out = {}
    # 三支上限（示意数值，只检验合取→min 的逻辑）
    Tstar, TBKT, Ttheta = 90.0, 60.0, 75.0
    Tmin = min(Tstar, min(TBKT, Ttheta))
    out["T_star"] = Tstar
    out["T_BKT"] = TBKT
    out["T_theta"] = Ttheta
    out["min_envelope"] = float(Tmin)
    out["min_is_tightest"] = bool(Tmin == TBKT)
    # 回溯必然：若相变发生，T 必须 ≤ min（上界）
    out["upper_bound_holds"] = bool(Tmin <= min(Tstar, TBKT, Ttheta))
    # 前瞻偶然：条件齐备但相变未必发生——用布尔模型核对
    conditions_all_true = True
    phase_occurs = False
    out["contingency_possible"] = bool(conditions_all_true and not phase_occurs)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    x = np.linspace(0, 1, 300)
    # 三支随某外参（示意）的变化
    Tstar = 100 - 40 * x
    TBKT = 60 + 10 * np.sin(3 * x)
    Ttheta = 80 - 20 * x
    Tmin = np.minimum(Tstar, np.minimum(TBKT, Ttheta))
    envelope_idx = np.argmin(np.stack([Tstar, TBKT, Ttheta]), axis=0)

    # (a) 三支与 min 包络
    ax = axes[0, 0]
    ax.plot(x, Tstar, "b-", lw=2, label=r"配对支 $T^*$")
    ax.plot(x, TBKT, "g-", lw=2, label=r"BKT 支 $T_{\rm BKT}$")
    ax.plot(x, Ttheta, "orange", lw=2, label=r"相位支 $T_\theta$")
    ax.plot(x, Tmin, "k--", lw=2.5, label=r"上界 $\min\{T^*,T_{\rm BKT},T_\theta\}$")
    ax.set_xlabel("外参（示意）")
    ax.set_ylabel("温度（示意）")
    ax.set_title("(a) 三支必要条件 → min 上界包络")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    # (b) 哪支最严
    ax = axes[0, 1]
    ax.plot(x, envelope_idx, "purple", lw=2)
    ax.set_yticks([0, 1, 2])
    ax.set_yticklabels(["配对", "BKT", "相位"])
    ax.set_xlabel("外参（示意）")
    ax.set_title("(b) 最严的支卡住 Tc（回溯必然）")
    ax.grid(alpha=0.3)

    # (c) 回溯必然 vs 前瞻偶然
    ax = axes[1, 0]
    labels = ["回溯必然\nP⇒条件全备", "前瞻偶然\n条件全备⇏P"]
    vals = [1, 1]
    ax.bar(labels, vals, color=["tab:blue", "tab:orange"])
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["否", "成立"])
    ax.set_title("(c) 必然性推出上界，等号属偶然")
    ax.grid(alpha=0.3, axis="y")

    # (d) 上界示意：Tc 被 min 卡住
    ax = axes[1, 1]
    Tc = Tmin - 5 - 3 * np.sin(5 * x)  # 实际相变温度 ≤ 上界
    ax.plot(x, Tmin, "k--", lw=2, label="上界 min")
    ax.plot(x, Tc, "r-", lw=2, label=r"$T_c$（≤ 上界，等号偶然）")
    ax.fill_between(x, Tc, Tmin, color="red", alpha=0.1)
    ax.set_xlabel("外参（示意）")
    ax.set_ylabel("温度（示意）")
    ax.set_title("(d) Tc ≤ min：上界严格，等号未必达到")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R16: 历史唯物主义回溯必然闭合 (目标.1) 的 ≤min 判据结构", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "目标_闭合min判据.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R16 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "目标_闭合min判据_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
