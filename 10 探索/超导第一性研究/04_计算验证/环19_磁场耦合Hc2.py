#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 19／54：磁场最小耦合与上临界场 H_c2 温度律——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环19_磁场耦合Hc2.py"
"""
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "环19_磁场耦合Hc2.png")
CSV = os.path.join(HERE, "环19_磁场耦合Hc2.csv")
SUM = os.path.join(HERE, "环19_磁场耦合Hc2_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

# 示意参数（材料外生，只作形状检验）
hbar, kB, e = 1.0, 1.0, 1.0
Upsilon0 = 2.0   # 链内刚度（外生归一）
T0 = 10.0
c = Upsilon0 / 2  # R46 梯度系数

emit("=" * 60)
emit("环 19／54：磁场耦合 H_c2（链内前件 + 最小耦合）")
emit("=" * 60)

# ---- [A] H_c2(T) 线性温度律 ----
emit("\n[A] H_c2(T) = hbar kB (T0-T)/(e Upsilon0) 线性")
T = np.linspace(0, T0, 200)
Hc2 = hbar * kB * (T0 - T) / (e * Upsilon0)
emit(f"  T=0: H_c2={Hc2[0]:.4f}; T=T0: H_c2={Hc2[-1]:.4f}（线性趋零）")
slope = np.polyfit(T, Hc2, 1)[0]
emit(f"  斜率 dH_c2/dT = {slope:.6f}; 理论 -hbar kB/(e Upsilon0) = {-hbar*kB/(e*Upsilon0):.6f}")
emit(f"  随 T 增单调减: {bool(np.all(np.diff(Hc2)<0))}")
assert abs(slope + hbar*kB/(e*Upsilon0)) < 1e-9
assert np.all(np.diff(Hc2) < 0)

# ---- [B] 两路径自洽 ----
emit("\n[B] 两路径自洽：Landau vs Phi0/xi^2")
a_abs = 0.5  # |a| 示意
xi2 = c / a_abs               # xi^2 = c/|a|
Hc2_landau = hbar * a_abs / (2 * e * c)         # Landau 能级路径
Phi0 = 2*np.pi*hbar/(2*e)                        # = pi hbar/e
Hc2_xi = Phi0 / (2*np.pi*xi2)                    # 临-19 路径
emit(f"  Landau: hbar|a|/(2ec) = {Hc2_landau:.8f}")
emit(f"  xi路径: Phi0/(2pi xi^2) = {Hc2_xi:.8f}")
emit(f"  相等（相对差）: {abs(Hc2_landau-Hc2_xi)/Hc2_landau:.2e}")
assert abs(Hc2_landau - Hc2_xi)/Hc2_landau < 1e-10

# ---- [C] 与 WHH 弱耦合形状对照 ----
emit("\n[C] 与 WHH 弱耦合 (1-T/Tc) 形状对照")
t_reduced = T/T0
whh = np.clip(1 - t_reduced, 0, 1)  # 弱耦合线性极限
geometry = 1 - t_reduced**2          # 常见经验 Hc2 形状（示意偏离）
emit("  线性区：链内 H_c2 ∝ (T0-T) 与 WHH 弱耦合 (1-T/Tc) 同形")
emit(f"  低温端(t=0.1): 线性={1-0.1:.2f}, 经验(1-t^2)={1-0.1**2:.2f}（偏离属链外强耦合修正）")
emit("  边界：强耦合/轨道限制修正属 WHH 链外部分，本轮只给弱耦合线性律")

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(T, Hc2, label="H_c2 ~ (T0-T)")
ax[0].set_title("(A) linear H_c2 temperature law")
ax[0].set_xlabel("T"); ax[0].set_ylabel("H_c2")
ax[0].legend()

ax[1].bar(["Landau", "Phi0/xi^2"], [Hc2_landau, Hc2_xi], color=["steelblue", "darkorange"])
ax[1].set_title("(B) two paths agree")
ax[1].set_ylabel("H_c2")
ax[1].text(0.5, Hc2_landau, f"{Hc2_landau:.5f}", ha="center", va="bottom", fontsize=8)
ax[1].text(1.5, Hc2_xi, f"{Hc2_xi:.5f}", ha="center", va="bottom", fontsize=8)

ax[2].plot(t_reduced, whh, label="WHH weak-coupling (1-t)")
ax[2].plot(t_reduced, geometry, "--", label="empirical 1-t^2 (deviation)")
ax[2].set_title("(C) shape vs WHH (non-fit)")
ax[2].set_xlabel("t=T/T0"); ax[2].set_ylabel("H_c2 norm")
ax[2].legend()

fig.suptitle("R54: magnetic coupling and H_c2 (chain-inner shape, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"Hc2_slope,{slope:.8f}\n")
    f.write(f"theory_slope,{-hbar*kB/(e*Upsilon0):.8f}\n")
    f.write(f"Hc2_landau,{Hc2_landau:.8f}\n")
    f.write(f"Hc2_via_xi,{Hc2_xi:.8f}\n")
    f.write(f"two_paths_rel_diff,{abs(Hc2_landau-Hc2_xi)/Hc2_landau:.3e}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
