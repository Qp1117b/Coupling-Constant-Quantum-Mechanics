#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 8／49：闭环平均乘积判据的 3D 核统一——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环08_闭环乘积3D核.py"
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
OUT = os.path.join(HERE, "环08_闭环乘积3D核.png")
CSV = os.path.join(HERE, "环08_闭环乘积3D核.csv")
SUM = os.path.join(HERE, "环08_闭环乘积3D核_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

Srho_3d = 1.0 / 6.0
Srho_2d = -0.0226
emit("=== 关联和 S_rho（R45 3D / 第84轮 2D）===")
emit(f"S_rho(3D) = 1/6 = {Srho_3d:.6f}")
emit(f"S_rho(2D, J0核) = {Srho_2d:.6f}")
emit(f"S_rho(3D) - 1 = {Srho_3d - 1:.6f} < 0")
assert Srho_3d - 1 < 0

# ---- [A] 平均闭环乘积 <prod r> = exp[n sigma^2 (S-1)/(32 pi^2)] ----
emit("\n=== [A] <prod r> = exp[n sigma^2 (S_rho-1)/(32 pi^2)] < 1 ===")
ns = np.arange(2, 513, 2)
for sig2 in [0.0025, 0.01, 0.04]:   # sigma = 0.05, 0.1, 0.2
    exponent = ns * sig2 * (Srho_3d - 1) / (32 * np.pi**2)
    prod = np.exp(exponent)
    emit(f"sigma^2={sig2}: n=2 -> {prod[0]:.6f}, n=512 -> {prod[-1]:.6f}（恒<1，随n减）")
    assert np.all(prod < 1) and np.all(np.diff(prod) < 0)

# ---- [B] 符号判据：2D 与 3D 都 <0，翻转分支需 S>1 ----
emit("\n=== [B] 符号判据 S_rho - 1 ===")
emit(f"2D: S-1 = {Srho_2d - 1:.6f} < 0")
emit(f"3D: S-1 = {Srho_3d - 1:.6f} < 0")
emit(f"翻转需 S_rho > 1；链内 3D = {Srho_3d:.4f} << 1 ⇒ 不可达")
emit("回改：第83轮'强正关联可翻转>1'分支标为链外假设，非 CQM 可实现")
assert Srho_2d - 1 < 0 and Srho_3d - 1 < 0 and Srho_3d < 1

# ---- [C] 对数正态平均 vs 几何平均（二阶一致）----
emit("\n=== [C] <prod r> vs exp<ln prod r>（对数正态 vs 几何平均）===")
n0 = 128
sig2 = 0.0025
exponent_prod = n0 * sig2 * (Srho_3d - 1) / (32 * np.pi**2)
mean_prod = np.exp(exponent_prod)
mean_log = -n0 * sig2 / (16 * np.pi**2)   # (8F.7) 二阶负偏移
geom_mean = np.exp(mean_log)
emit(f"n={n0}, sigma^2={sig2}: <prod r>={mean_prod:.8f}")
emit(f"exp<ln prod r>={geom_mean:.8f}（几何平均，<1）")
emit(f"两者都 <1：{mean_prod<1 and geom_mean<1}；且 <prod r> > 几何平均（Jensen）：{mean_prod>geom_mean}")
assert mean_prod < 1 and geom_mean < 1 and mean_prod > geom_mean

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
for sig2, col in zip([0.0025, 0.01, 0.04], ["b", "g", "r"]):
    exponent = ns * sig2 * (Srho_3d - 1) / (32 * np.pi**2)
    ax[0].semilogx(ns, np.exp(exponent), color=col, label=f"sigma^2={sig2}")
ax[0].axhline(1, color="k", ls="--", label="1 (flat static)")
ax[0].set_title("(A) <prod r> < 1 always (3D kernel)")
ax[0].set_xlabel("n (loop length)"); ax[0].set_ylabel("<prod r>")
ax[0].legend()

ax[1].bar(["2D (J0)", "3D (j0)"], [Srho_2d - 1, Srho_3d - 1], color=["steelblue", "darkorange"])
ax[1].axhline(0, color="k", lw=0.5)
ax[1].set_title("(B) S_rho - 1 < 0 (both kernels)")
ax[1].set_ylabel("S_rho - 1")
ax[1].text(1, Srho_3d - 1, f"flip needs S>1;\nchain S={Srho_3d:.3f}", ha="center", va="top", fontsize=8)

ax[2].bar(["<prod r>", "exp<ln prod r>"], [mean_prod, geom_mean], color=["steelblue", "lightgreen"])
ax[2].axhline(1, color="k", ls="--")
ax[2].set_title("(C) arithmetic > geometric (Jensen)")
ax[2].set_ylabel("value")

fig.suptitle("R49: closed-loop product with 3D kernel (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"Srho_3D,{Srho_3d:.8f}\n")
    f.write(f"Srho_minus_one,{Srho_3d - 1:.8f}\n")
    f.write(f"mean_prod_n128_s0.05,{mean_prod:.10f}\n")
    f.write(f"geom_mean_n128_s0.05,{geom_mean:.10f}\n")
    f.write(f"always_lt_one,{True}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
