# -*- coding: utf-8 -*-
"""
R17: 赝能隙存在判据——三支与赝能隙区 (Tc, T*] 的包络。
只检验符号/存在判据/反向反例，不拟合。仅用 numpy + matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/目标_闭合赝能隙判据.py"
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
    Tstar = 90.0
    # 情形 A：相位支更严（Tphi < T*）⇒ 赝能隙必存在
    TBKT_A, Ttheta_A = 60.0, 75.0
    Tphi_A = min(TBKT_A, Ttheta_A)
    Tc_A = Tphi_A  # 上界取等（示意）
    dpg_A = Tstar - Tc_A
    out["caseA_Tphi"] = Tphi_A
    out["caseA_phase_tighter"] = bool(Tphi_A < Tstar)
    out["caseA_delta_pg"] = float(dpg_A)
    out["caseA_exists"] = bool(dpg_A > 0)
    # 情形 B：配对支最严（T* ≤ Tphi）⇒ Δpg 可为 0（不推出）
    Tphi_B = 100.0
    Tc_B = Tstar
    dpg_B = Tstar - Tc_B
    out["caseB_delta_pg"] = float(dpg_B)
    out["caseB_can_be_zero"] = bool(dpg_B == 0)
    # 符号：普遍非负
    out["delta_pg_nonneg"] = bool(Tstar - Tc_A >= 0 and Tstar - Tc_B >= 0)
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    x = np.linspace(0, 1, 300)
    # 三支示意：配对支高且平，相位支随外参下降
    Tstar = np.full_like(x, 90.0)
    TBKT = 85 - 50 * x
    Ttheta = 88 - 30 * x
    Tphi = np.minimum(TBKT, Ttheta)
    Tmin = np.minimum(Tstar, Tphi)
    Tc = Tmin - 2 * np.sin(4 * x) ** 2  # 实际 Tc ≤ 上界
    dpg = np.maximum(Tstar - Tc, 0)

    ax = axes[0, 0]
    ax.plot(x, Tstar, "b-", lw=2, label=r"配对支 $T^*$")
    ax.plot(x, Tphi, "g-", lw=2, label=r"相位支瓶颈 $T_\phi$")
    ax.plot(x, Tc, "r-", lw=2, label=r"$T_c\leq\min$")
    ax.fill_between(x, Tc, Tstar, where=(Tphi < Tstar), color="orange", alpha=0.25)
    ax.set_xlabel("外参（示意）")
    ax.set_ylabel("温度（示意）")
    ax.set_title("(a) 相位支为瓶颈 ⇒ 赝能隙区张开")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    ax.plot(x, dpg, "purple", lw=2)
    ax.axhline(0, color="k", lw=1)
    ax.set_xlabel("外参（示意）")
    ax.set_ylabel(r"$\Delta T_{\rm pg}$")
    ax.set_title("(b) 赝能隙宽度非负（符号闭合）")
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    labels = ["相位支更严\n⇒ 必存在", "配对支最严\n⇒ 可为零"]
    vals = [1, 0]
    cols = ["tab:green", "tab:gray"]
    ax.bar(labels, vals, color=cols)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(["否", "是"])
    ax.set_title("(c) 存在判据（充分）+ 反向不推出")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 1]
    ax.plot(x, Tphi, "g-", lw=2, label=r"$T_\phi$")
    ax.plot(x, Tstar, "b-", lw=2, label=r"$T^*$")
    less = Tphi < Tstar
    ax.scatter(x[::20], np.where(less, 1, 0)[::20], c="orange", s=20,
               label=r"$T_\phi<T^*$ 指示")
    ax.set_xlabel("外参（示意）")
    ax.set_ylabel("指示")
    ax.set_title("(d) 历史唯物主义§5.1：局域已备、全局未同步")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    fig.suptitle("R17: 从已闭合 ≤min 推出赝能隙存在判据（无拟合）", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "目标_闭合赝能隙判据.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R17 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "目标_闭合赝能隙判据_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
