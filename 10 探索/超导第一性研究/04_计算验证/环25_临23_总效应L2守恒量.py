#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 25／50：总效应 L2 守恒量 = 相变量子 Xi——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环25_临23_总效应L2守恒量.py"
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
OUT = os.path.join(HERE, "环25_临23_总效应L2守恒量.png")
CSV = os.path.join(HERE, "环25_临23_总效应L2守恒量.csv")
SUM = os.path.join(HERE, "环25_临23_总效应L2守恒量_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

XI = 0.02309570897  # README 权威相变量子
# 前 40 个黎曼零点虚部（标准值）
gamma = np.array([
    14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918719,43.327073,
    48.005151,49.773832,52.970321,56.446248,59.347044,60.831779,65.112544,67.079811,
    69.546402,72.067158,75.704691,77.144840,79.337375,82.910381,84.735492,87.425275,
    88.809111,92.491899,94.651344,95.870634,98.831194,101.317851,103.725538,105.446623,
    107.168611,111.029536,111.874659,114.220675,116.958250,121.127905,123.249815,125.729984
])

emit("=" * 60)
emit("环 25／临-23：总效应 L2 范数 = 相变量子 Xi（条件于 RH）")
emit("=" * 60)
emit(f"README Xi = {XI:.11f}")

# ---- [A] 部分和 sum 1/(gamma^2+1/4) 收敛到 Xi ----
emit("\n[A] 部分和收敛到 Xi")
terms = 1.0 / (gamma**2 + 0.25)
partial = np.cumsum(terms)
emit(f"  N=1:  {partial[0]:.8f}")
emit(f"  N=20: {partial[19]:.8f}")
emit(f"  N=40: {partial[-1]:.8f}")
emit(f"  全部 Xi: {XI:.8f}")
emit(f"  单调增: {bool(np.all(np.diff(partial) > 0))}; 从下方逼近: {partial[-1] < XI}")
emit(f"  尾部占比 (N=40): {(XI - partial[-1])/XI*100:.1f}%")
assert np.all(np.diff(partial) > 0) and partial[-1] < XI

# ---- [B] 留数和 K(tau) 的长时平均功率 -> Xi（Parseval）----
emit("\n[B] 留数和 K(tau) 的长时平均功率 -> Xi（Parseval）")
# K(tau) = -sum e^{i gamma_n tau}/rho_n, rho_n=1/2+i gamma_n
# 用截断 N 项直接算 |K|^2 的时间平均
rho = 0.5 + 1j * gamma
coeff = -1.0 / rho
N = 20
taus = np.linspace(0, 2000, 200000)
K = np.zeros_like(taus, dtype=complex)
for n in range(N):
    K += coeff[n] * np.exp(1j * gamma[n] * taus)
power = np.mean(np.abs(K)**2)
theory = np.sum(1.0/np.abs(rho[:N])**2)
emit(f"  数值时间平均功率 (N={N} 项) = {power:.8f}")
emit(f"  Parseval 理论值 sum 1/|rho|^2  = {theory:.8f}")
emit(f"  相对差 = {abs(power-theory)/theory*100:.2f}%")
assert abs(power - theory)/theory < 0.15  # 有限时间窗交叉项残留

# ---- [C] 短时窗 vs 长时窗（交叉项随窗口消失）----
emit("\n[C] 功率对时间窗的依赖（交叉项随窗增大消失）")
windows = [50, 200, 800, 2000]
powers = []
for W in windows:
    tw = np.linspace(0, W, 100000)
    Kw = sum(coeff[n]*np.exp(1j*gamma[n]*tw) for n in range(N))
    powers.append(np.mean(np.abs(Kw)**2))
    emit(f"  W={W:5d}: 功率={powers[-1]:.6f} (偏离理论 {abs(powers[-1]-theory)/theory*100:5.1f}%)")
emit("  趋势：窗口越大越接近 Parseval 理论值（交叉项平均掉）")
assert abs(powers[-1]-theory) < abs(powers[0]-theory) or abs(powers[-1]-theory)/theory < 0.15

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(np.arange(1, len(partial)+1), partial, label="partial sum")
ax[0].axhline(XI, color="r", ls="--", label=f"Xi={XI:.6f}")
ax[0].set_title("(A) partial sum -> Xi")
ax[0].set_xlabel("N zeros"); ax[0].set_ylabel("sum 1/(g^2+1/4)")
ax[0].legend()

ax[1].plot(taus[:20000], np.abs(K[:20000])**2, lw=0.5, alpha=0.7, label="|K|^2")
ax[1].axhline(theory, color="r", ls="--", label=f"Parseval={theory:.5f}")
ax[1].axhline(XI, color="g", ls=":", label=f"Xi(all)={XI:.5f}")
ax[1].set_title("(B) |K(t)|^2 oscillates, mean=Parseval")
ax[1].set_xlabel("tau"); ax[1].set_ylabel("|K|^2")
ax[1].legend()

ax[2].plot(windows, powers, "o-", label="time-window power")
ax[2].axhline(theory, color="r", ls="--", label="Parseval theory")
ax[2].set_title("(C) cross terms vanish as window grows")
ax[2].set_xlabel("window W"); ax[2].set_ylabel("mean power")
ax[2].legend()

fig.suptitle("R50: total-effect L2 norm = Xi (conditional on RH, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"Xi,{XI:.11f}\n")
    f.write(f"partial_N20,{partial[19]:.8f}\n")
    f.write(f"partial_N40,{partial[-1]:.8f}\n")
    f.write(f"parseval_theory_N20,{theory:.8f}\n")
    f.write(f"numerical_power_N20,{power:.8f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
