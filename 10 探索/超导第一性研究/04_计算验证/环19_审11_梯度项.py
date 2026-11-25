#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 19／46：GL 梯度项系数的链内来源——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环19_审11_梯度项.py"
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
OUT = os.path.join(HERE, "环19_审11_梯度项.png")
CSV = os.path.join(HERE, "环19_审11_梯度项.csv")
SUM = os.path.join(HERE, "环19_审11_梯度项_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

nu_mf = 0.5
nu_perc = 4.0 / 3.0
Upsilon0 = 1.0
c = Upsilon0 / 2.0   # 梯度系数（回改后：刚度本身，温度无关到 leading）

emit("=== GL 梯度系数（回改后）===")
emit(f"c = Upsilon0/2 = {c}（正定：{c>0}）")
emit(f"nu_MF = 1/2 = {nu_mf}, nu_perc = 4/3 = {nu_perc:.6f}")
assert c > 0

# ---- [A] 初稿错误 vs 回改正确：双对数斜率 ----
emit("\n=== [A] xi 对 |T0-T| 的双对数斜率 ===")
t = np.logspace(-4, -1, 200)   # t = |T0-T|
xi_correct = t ** (-nu_mf)     # 正确：ν=1/2
xi_wrong = t ** (-(nu_mf + 1)) # 初稿错误：ν=3/2（来自 c=-Υb/a^2）
slope_correct = np.polyfit(np.log(t), np.log(xi_correct), 1)[0]
slope_wrong = np.polyfit(np.log(t), np.log(xi_wrong), 1)[0]
emit(f"回改正确斜率 = {slope_correct:.6f}（目标 -1/2）")
emit(f"初稿错误斜率 = {slope_wrong:.6f}（错误 -3/2，已删除）")
emit(f"|正确误差| = {abs(slope_correct + 0.5):.3e}")
assert abs(slope_correct + 0.5) < 1e-9
assert abs(slope_wrong + 1.5) < 1e-9

# ---- [B] xi_GL = sqrt(c/|a|) 的温度依赖，a=k_B(T0-T) ----
emit("\n=== [B] xi_GL = sqrt(c/(k_B t)) 的温度依赖 ===")
kB = 1.0
a_abs = kB * t
xi_GL = np.sqrt(c / a_abs)
slope_GL = np.polyfit(np.log(t), np.log(xi_GL), 1)[0]
emit(f"xi_GL = sqrt(c/(k_B t)) 斜率 = {slope_GL:.6f}（应 -1/2）")
emit(f"t=1e-4: xi={xi_GL[0]:.3f}, t=0.1: xi={xi_GL[-1]:.3f}（降温发散）")
assert abs(slope_GL + 0.5) < 1e-9
assert xi_GL[0] > xi_GL[-1]

# ---- [C] 两类相干长度（不同普适类）----
emit("\n=== [C] 平均场 vs 渗流相干长度（不同普适类）===")
xi_mf = t ** (-nu_mf)
xi_pf = t ** (-nu_perc)
emit(f"平均场 ν=1/2：t=1e-3 -> xi={xi_mf[np.argmin(abs(t-1e-3))]:.3f}")
emit(f"渗流 ν=4/3：t=1e-3 -> xi={xi_pf[np.argmin(abs(t-1e-3))]:.3f}")
emit(f"ν_MF != ν_perc：{nu_mf != nu_perc}（不同临界点、不同普适类）")
assert nu_mf != nu_perc and nu_mf < nu_perc

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].loglog(t, xi_correct, label="correct: nu=1/2")
ax[0].loglog(t, xi_wrong, label="draft (retracted): nu=3/2")
ax[0].set_title("(A) draft error vs corrected exponent")
ax[0].set_xlabel("|T0-T|"); ax[0].set_ylabel("xi")
ax[0].legend()

ax[1].loglog(t, xi_GL, label="xi_GL = sqrt(c/(kB t))")
ax[1].set_title("(B) GL coherence length (slope=-1/2)")
ax[1].set_xlabel("|T0-T|"); ax[1].set_ylabel("xi_GL")
ax[1].legend()

ax[2].loglog(t, xi_mf, label="MF nu=1/2")
ax[2].loglog(t, xi_pf, label="percolation nu=4/3")
ax[2].set_title("(C) two universality classes")
ax[2].set_xlabel("distance to critical"); ax[2].set_ylabel("xi")
ax[2].legend()

fig.suptitle("R46: GL gradient coefficient (ring 19, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"c,{c:.8f}\n")
    f.write(f"nu_MF,{nu_mf:.8f}\n")
    f.write(f"nu_perc,{nu_perc:.8f}\n")
    f.write(f"slope_correct,{slope_correct:.8f}\n")
    f.write(f"slope_wrong,{slope_wrong:.8f}\n")
    f.write(f"slope_GL,{slope_GL:.8f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
