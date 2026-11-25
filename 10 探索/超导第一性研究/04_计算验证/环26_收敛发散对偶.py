#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 26／52：收敛-发散对偶与可读窗口——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环26_收敛发散对偶.py"
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
OUT = os.path.join(HERE, "环26_收敛发散对偶.png")
CSV = os.path.join(HERE, "环26_收敛发散对偶.csv")
SUM = os.path.join(HERE, "环26_收敛发散对偶_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

XI = 0.02309570897
g = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918719,43.327073,
    48.005151,49.773832,52.970321,56.446248,59.347044,60.831779,65.112544,67.079811,
    69.546402,72.067158,75.704691,77.144840,79.337375,82.910381,84.735492,87.425275,
    88.809111,92.491899,94.651344,95.870634,98.831194,101.317851,103.725538,105.446623,
    107.168611,111.029536,111.874659,114.220675,116.958250,121.127905,123.249815,125.729984])

emit("=" * 60)
emit("环 26／52：总效应 vs 总退相干的收敛-发散对偶")
emit("=" * 60)

# ---- [A] M_-2 收敛 ----
emit("\n[A] M_-2 = sum 1/(gamma^2+1/4) 收敛到 Xi")
m2 = np.cumsum(1.0/(g**2+0.25))
Ns = np.arange(1, len(g)+1)
emit(f"  N=1: {m2[0]:.6f}, N=20: {m2[19]:.6f}, N=40: {m2[-1]:.6f}")
emit(f"  Xi(全零点)={XI:.6f}; 收敛方向(递增且<Xi): {bool(np.all(np.diff(m2)>0) and m2[-1]<XI)}")
assert np.all(np.diff(m2) > 0) and m2[-1] < XI

# ---- [B] M_+2 发散 vs 渐近 ----
emit("\n[B] M_+2 = sum gamma^2 发散（渐近 ~ 4pi^2 N^3/(3 ln^2 N)）")
p2 = np.cumsum(g**2)
emit(f"  N=40 部分和 = {p2[-1]:.0f}")
for N in [10, 20, 40]:
    asym = 4*np.pi**2*N**3/(3*np.log(N)**2)
    emit(f"  N={N}: sum={p2[N-1]:.0f}, asym≈{asym:.0f}, ratio={p2[N-1]/asym:.2f}")
emit(f"  单调增且无界趋势: {bool(np.all(np.diff(p2)>0))}")
assert np.all(np.diff(p2) > 0)

# ---- [C] 对偶比 + 可读窗口 ----
emit("\n[C] 对偶比 M_+2/M_-2 随 N 增长（发散压倒收敛）")
ratio = p2 / m2
for N in [10, 20, 40]:
    emit(f"  N={N}: ratio={ratio[N-1]:.3e}")
emit(f"  单调增: {bool(np.all(np.diff(ratio)>0))}")
assert np.all(np.diff(ratio) > 0)

# 可读窗口示意：gamma_n < gamma_* 可读，gamma_* = sigma_v^2 tau_g 决定
gstar = 80.0  # 示意
readable = g[g < gstar]
emit(f"\n  示意 gamma_*={gstar}: 可读零点数={len(readable)}/{len(g)}（低频可读、高频抹掉）")

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(Ns, m2, label="M_-2 partial")
ax[0].axhline(XI, color="r", ls="--", label=f"Xi={XI:.6f}")
ax[0].set_title("(A) total effect M_-2 converges")
ax[0].set_xlabel("N"); ax[0].set_ylabel("M_-2")
ax[0].legend()

ax[1].plot(Ns, p2, label="sum gamma^2")
Ns_asym = Ns[Ns >= 2]  # ln(1)=0 避开渐近式首点
asym_curve = 4*np.pi**2*Ns_asym**3/(3*np.log(Ns_asym)**2)
ax[1].plot(Ns_asym, asym_curve, "--", label="asym ~ N^3/ln^2N")
ax[1].set_title("(B) total decoherence M_+2 diverges")
ax[1].set_xlabel("N"); ax[1].set_ylabel("M_+2")
ax[1].legend()

ax[2].semilogy(Ns, ratio, label="M_+2 / M_-2")
ax[2].axvline(len(readable), color="g", ls=":", label="readable window")
ax[2].set_title("(C) duality: divergence wins")
ax[2].set_xlabel("N"); ax[2].set_ylabel("ratio (log)")
ax[2].legend()

fig.suptitle("R52: convergence-divergence duality (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"Xi,{XI:.11f}\n")
    f.write(f"M_minus2_N40,{m2[-1]:.8f}\n")
    f.write(f"M_plus2_N40,{p2[-1]:.4f}\n")
    f.write(f"ratio_N10,{ratio[9]:.4e}\n")
    f.write(f"ratio_N40,{ratio[-1]:.4e}\n")
    f.write(f"readable_count_gstar80,{len(readable)}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
