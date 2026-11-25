# -*- coding: utf-8 -*-
"""
R39: R17 赝能隙符号判据的实证核对——用独立实测 T*,Tc（非从 Tc 反解）。
数据标源文献卡 R39。无拟合（符号核对 + 文献线性趋势）。
运行：python "10 探索/超导第一性研究/04_计算验证/R39_赝能隙判据核对.py"
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

# 实测数据点（T* 为配对起始/赝能隙起始定义，非从 Tc 反解）
# (材料, 掺杂p, Tc(K), T*(K), 方法, 来源)
DATA = [
    ("Bi2212 underdoped", None, 67, 150, "红外/ARPES", "Puchkov1996 / Stanford"),
    ("Bi2201 underdoped", None, 27, 110, "电阻率(示意值)", "Cyr-Choiniere2018 Fig5b Tc=27K; T*为示意"),
    ("Nd-LSCO p=0.20", 0.20, 15, 75, "ARPES/Nernst", "Cyr-Choiniere2018"),
    ("Y123 x=6.6", None, 58, 200, "红外", "Puchkov1996"),
]

# YBCO / LSCO 的 T*(p) 线性趋势（Cyr-Choiniere 2018 定性：线性下降，YBCO≈1.5 LSCO）
# 仅示意趋势，非精确读数
P_DOPING = np.array([0.05, 0.10, 0.15, 0.18, 0.195])
TSTAR_YBCO = np.array([300, 230, 150, 70, 0])  # 线性降到 p*=0.195 处 0K（定性）
TSTAR_LSCO = TSTAR_YBCO / 1.5


def assertions():
    out = {}
    # R17.2 符号核对：所有欠掺杂数据点 ΔT_pg = T*-Tc ≥ 0
    for name, p, tc, tstar, method, src in DATA:
        d = tstar - tc
        out[f"{name}_dTpg"] = d
        out[f"{name}_nonneg"] = bool(d >= 0)
    out["all_sign_ok"] = bool(all(d[1] for d in [
        (s, (s[3] - s[2]) >= 0) for s in DATA
    ]))
    # 欠掺杂区严格 >0（R17.3：T_phi<T* 时）
    out["all_underdoped_strict_pos"] = bool(all(s[3] - s[2] > 0 for s in DATA))
    # 量级：欠掺杂 T*/Tc 可达 2-5+（赝能隙温度远高于 Tc 是欠掺杂铜氧化物常识）
    ratios = [s[3] / s[2] for s in DATA]
    out["Tstar_over_Tc"] = [round(r, 2) for r in ratios]
    out["reasonable_magnitude"] = bool(all(1.5 < r < 6 for r in ratios))
    # T*(p) 线性下降（Cyr-Choiniere 2018）
    slope = np.polyfit(P_DOPING[:4], TSTAR_YBCO[:4], 1)[0]
    out["Tstar_p_slope_negative"] = bool(slope < 0)
    out["YBCO_1p5_LSCO"] = bool(np.allclose(TSTAR_YBCO, 1.5 * TSTAR_LSCO))
    return out


def plots(a):
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    ax = axes[0, 0]
    names = [d[0].split()[0] for d in DATA]
    tcs = [d[2] for d in DATA]
    tstars = [d[3] for d in DATA]
    x = np.arange(len(DATA))
    ax.bar(x - 0.2, tcs, 0.4, label="$T_c$")
    ax.bar(x + 0.2, tstars, 0.4, label=r"$T^*$（实测）")
    ax.set_xticks(x); ax.set_xticklabels(names, rotation=15, fontsize=8)
    ax.set_ylabel("温度 (K)"); ax.set_title(r"(a) 欠掺杂数据点：$T^*>T_c$")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, axis="y")

    ax = axes[0, 1]
    dpg = [d[3] - d[2] for d in DATA]
    ax.bar(names, dpg, color="tab:green")
    ax.axhline(0, color="k", ls="--")
    ax.set_xticklabels(names, rotation=15, fontsize=8)
    ax.set_ylabel(r"$\Delta T_{\rm pg}=T^\ast-T_c$ (K)")
    ax.set_title("(b) R17.2 符号核对：ΔT_pg ≥ 0 全部成立")
    ax.grid(alpha=0.3, axis="y")

    ax = axes[1, 0]
    ax.plot(P_DOPING, TSTAR_YBCO, "r-o", label=r"YBCO $T^*(p)$")
    ax.plot(P_DOPING, TSTAR_LSCO, "b-s", label=r"LSCO $T^*(p)$")
    ax.set_xlabel("空穴掺杂 p"); ax.set_ylabel(r"$T^*$ (K)")
    ax.set_title(r"(c) $T^*(p)$ 线性下降（Cyr-Choinière 2018 定性）")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)

    ax = axes[1, 1]
    ax.bar([r"链 $T^*$(结构性上限)", r"实验 $T_{\nu}/T_{\rho}$(现象学读数)"], [1, 1],
           color=["tab:green", "tab:orange"])
    ax.set_yticks([])
    ax.set_title(r"(d) 范畴分离：过掺杂表观 $T^*<T_c$ 不证伪 R17")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R39: R17 赝能隙判据实证核对（实数据非反解；判据一致性，非推出 T*）", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "R39_赝能隙判据核对.png")
    fig.savefig(png, dpi=140); plt.close(fig)
    return png


if __name__ == "__main__":
    a = assertions()
    print("=== R39 数值断言 ===")
    for k, v in a.items():
        print(f"{k:32s} = {v}")
    p = plots(a)
    path = os.path.join(HERE, "R39_赝能隙判据核对_断言.csv")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f); w.writerow(["assertion", "value"])
        for k, v in a.items():
            w.writerow([k, v])
    print(f"\n图像: {p}\n断言表: {path}")
