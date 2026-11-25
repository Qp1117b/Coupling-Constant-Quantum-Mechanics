#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标区／47：GL 参数 kappa 温度标度接口——数值核对（B 类·外部式检验，非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/目标区_GL参数kappa.py"
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
OUT = os.path.join(HERE, "目标区_GL参数kappa.png")
CSV = os.path.join(HERE, "目标区_GL参数kappa.csv")
SUM = os.path.join(HERE, "目标区_GL参数kappa_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

T0 = 1.0
omega_D = 10.0
kappa_c = 1.0 / np.sqrt(2.0)

emit("=== B 类接口（外部 London + CQM 链内量）===")
emit(f"kappa_c = 1/sqrt(2) = {kappa_c:.6f}（外部判据，不作 CQM 结论）")

# ---- [A] w(T) 与 lambda_L ----
emit("\n=== [A] Debye 权重 w(T) 与 lambda_L ∝ 1/sqrt(w) ===")
T = np.linspace(0.01, 0.99 * T0, 200)   # 低温侧 T<T0
t_ratio = T / omega_D
w = 1 - (np.pi**2 / 3) * t_ratio**2      # 低温形状（T<<omega_D 适用）
w = np.clip(w, 1e-6, None)
lambda_L = 1 / np.sqrt(w)
emit(f"w(T=0.01)={w[0]:.6f}, w(T=0.99)={w[-1]:.6f}（随 T 升而降）")
emit(f"lambda_L 随 T 升而增：{bool(np.all(np.diff(lambda_L) > 0))}")
assert np.all(np.diff(w) < 0) and np.all(np.diff(lambda_L) > 0)

# ---- [B] kappa(T) ∝ |T0-T|^{1/2}/sqrt(w) ----
emit("\n=== [B] kappa(T) ∝ |T0-T|^{1/2}/sqrt(w) 温度标度 ===")
delta = T0 - T
kappa_shape = np.sqrt(delta) / np.sqrt(w)
emit(f"kappa(T=0.01)={kappa_shape[0]:.4f}, kappa(T=0.99)={kappa_shape[-1]:.4f}")
emit(f"降温（T↓）kappa 上升：{bool(np.all(np.diff(kappa_shape[::-1]) > 0))}")
emit(f"临界区 T→T0^- kappa→0：{kappa_shape[-1]:.2e}")
assert kappa_shape[-1] < kappa_shape[0]   # 临界区 < 低温

# ---- [C] 第一/第二类边界（B 类，归一化外生）----
emit("\n=== [C] kappa_c 参考线（绝对值外生，链外-B 未闭合）===")
# 示意归一：取某个材料归一常数 A 使低温 kappa 跨越 kappa_c
A = kappa_c / kappa_shape[0] * 1.5   # 选 A 让低温 kappa > kappa_c（第二类示意）
kappa_abs = A * kappa_shape
cross_idx = np.argmax(kappa_abs < kappa_c)
emit(f"低温 kappa_abs={kappa_abs[0]:.4f} (>kappa_c? {kappa_abs[0]>kappa_c})")
emit(f"临界区 kappa_abs={kappa_abs[-1]:.4f} (<kappa_c? {kappa_abs[-1]<kappa_c})")
emit(f"示意交叉温度 T≈{T[cross_idx]:.3f}（绝对值依赖外生 A，非 CQM 预言）")
emit("边界：kappa 绝对值、材料第一/第二类归属均属链外-B，本轮只给温度形状")

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(T, w, label="w(T) ≈ 1-(pi^2/3)(T/wD)^2")
ax[0].set_title("(A) Debye coherence weight")
ax[0].set_xlabel("T"); ax[0].set_ylabel("w"); ax[0].legend()

ax[1].plot(T, kappa_shape, label="kappa ~ |T0-T|^{1/2}/sqrt(w)")
ax[1].set_title("(B) kappa shape (increases on cooling)")
ax[1].set_xlabel("T"); ax[1].set_ylabel("kappa (shape)")
ax[1].legend()

ax[2].plot(T, kappa_abs, label="kappa (illustrative norm)")
ax[2].axhline(kappa_c, color="r", ls="--", label="kappa_c=1/sqrt2 (external)")
ax[2].set_title("(C) type I/II boundary (B-class, norm external)")
ax[2].set_xlabel("T"); ax[2].set_ylabel("kappa")
ax[2].legend()

fig.suptitle("R47: GL kappa temperature scaling (B-class interface, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"kappa_c,{kappa_c:.8f}\n")
    f.write(f"kappa_shape_lowT,{kappa_shape[0]:.8f}\n")
    f.write(f"kappa_shape_critical,{kappa_shape[-1]:.8f}\n")
    f.write(f"increases_on_cooling,{bool(np.all(np.diff(kappa_shape[::-1]) > 0))}\n")
    f.write(f"classification_norm_external,{A:.8f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
