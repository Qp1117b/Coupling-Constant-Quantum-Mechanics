# -*- coding: utf-8 -*-
"""
R23: FE10 判别实验预注册图——两条竞争预言（FE10 上升 vs 标准平坦）。
这是设计示意，不是数据拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/FE10_判别实验.py"
"""
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ce = np.linspace(0.3, 1.0, 200)  # 几何曲率 RMS（归一化示意）
    K = 2.0
    eta_fe10 = K * ce**2            # FE10 预言
    eta_std = np.full_like(ce, K * 0.5**2)  # 标准理论：atomic property 恒定

    # (a) 两条竞争预言
    ax = axes[0, 0]
    ax.plot(ce, eta_fe10, "b-", lw=2.5, label=r"FE10：$\eta\propto c_\varepsilon^2$")
    ax.plot(ce, eta_std, "r--", lw=2, label=r"标准：$\eta$=atomic（恒定）")
    ax.set_xlabel(r"几何曲率 $c_\varepsilon$（独立测）")
    ax.set_ylabel(r"$\eta$（隧穿 $\alpha^2F$ 独立测）")
    ax.set_title("(a) 判别：上升(FE10) vs 平坦(标准)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    # (b) 判别区（斜率）
    ax = axes[0, 1]
    slope_fe10 = 2 * K * ce
    ax.plot(ce, slope_fe10, "b-", lw=2)
    ax.axhline(0, color="r", ls="--", lw=1.5, label="标准斜率=0")
    ax.fill_between(ce, 0, slope_fe10, color="blue", alpha=0.15)
    ax.set_xlabel(r"$c_\varepsilon$")
    ax.set_ylabel(r"$d\eta/d(c_\varepsilon^2)$ 符号")
    ax.set_title("(b) 判据：斜率>0 支持 FE10，=0 支持标准")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    # (c) 测量链（协议示意）
    ax = axes[1, 0]
    steps = ["应变/压力\n改几何曲率", "XRD/EXAFS\n测 $c_\\varepsilon$", "隧穿 dI/dV", "McMillan-Rowell\n反演 $\\alpha^2F$", "$\\eta=\\lambda\\langle\\omega^2\\rangle M$"]
    ys = np.arange(len(steps))
    ax.barh(ys, np.ones_like(ys), color=["tab:blue", "tab:blue", "tab:green", "tab:green", "tab:orange"])
    ax.set_yticks(ys); ax.set_yticklabels(steps, fontsize=8)
    ax.set_xticks([])
    ax.set_title("(c) 独立测量链（无循环）")
    ax.grid(alpha=0.3, axis="x")

    # (d) 循环禁令
    ax = axes[1, 1]
    labels = ["隧穿独立测\n(合法)", "$T_c$ 反推 $\\lambda$\n(循环·禁止)"]
    vals = [1, 0]
    ax.bar(labels, vals, color=["tab:green", "tab:red"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["否", "是"])
    ax.set_title("(d) 预注册：禁止 Tc 反推（R6 循环判据）")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R23: FE10 判别实验预注册（设计示意，非数据拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "FE10_判别实验.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    print(f"图像: {png}")


if __name__ == "__main__":
    main()
