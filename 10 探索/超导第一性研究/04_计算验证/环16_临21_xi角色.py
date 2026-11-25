#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 16／45：xi 角色的链内判定——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环16_临21_xi角色.py"
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
OUT = os.path.join(HERE, "环16_临21_xi角色.png")
CSV = os.path.join(HERE, "环16_临21_xi角色.csv")
SUM = os.path.join(HERE, "环16_临21_xi角色_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

nu = 4.0 / 3.0
two_nu = 2 * nu
pc = 0.592746
a = 1.0  # 示意：以 a 为单位

emit("=== 2D 渗流指数（外部工具）===")
emit(f"nu = 4/3 = {nu:.6f}")
emit(f"2nu = 8/3 = {two_nu:.6f}")
emit(f"1/nu = 3/4 = {1/nu:.6f}")
assert abs(two_nu - 8/3) < 1e-9
assert abs(1/nu - 0.75) < 1e-9

# ---- [A] 两读法的 n_eff 对 L 的依赖 ----
emit("\n=== [A] n_eff vs L：R1（与 L 无关） vs R2（随 L 发散）===")
Ls = np.logspace(1, 4, 100)
delta = 0.01                      # 固定 p-pc（离临界）
xi_R1 = delta ** (-nu)            # 标准相关长度：与 L 无关
n_R1 = (xi_R1 / a) ** 2           # 有限容量
n_R2 = (Ls / a) ** 2              # R2：xi=L 随系统发散
emit(f"R1: xi={xi_R1:.3f}（与 L 无关）, n_eff={n_R1:.3f}（有限平台）")
emit(f"R2: L=100 -> n={n_R2[0]:.3e}, L=10000 -> n={n_R2[-1]:.3e}（发散）")
emit(f"R1 恒定：{bool(np.all(np.diff(np.full_like(Ls, n_R1)) == 0))}")
assert np.all(np.diff(n_R2) > 0)

# ---- [B] R1 容量标度 n_eff ~ |p-pc|^{-8/3} ----
emit("\n=== [B] R1 容量标度指数 = 8/3 ===")
deltas = np.logspace(-3, -1, 100)
xi = deltas ** (-nu)
n_eff = (xi / a) ** 2
# 双对数斜率
slope = np.polyfit(np.log(deltas), np.log(n_eff), 1)[0]
emit(f"双对数斜率 = {slope:.6f}（目标 -2nu = -8/3 = {-8/3:.6f}）")
emit(f"|误差| = {abs(slope + 8/3):.3e}")
assert abs(slope + 8/3) < 1e-6

# ---- [C] 有限尺寸交叉 xi_eff = min(xi, L) ----
emit("\n=== [C] 读数层 xi_eff = min(xi, L) ===")
xi_fixed = 50.0
xi_eff = np.minimum(xi_fixed, Ls)
idx_cross = np.argmax(Ls > xi_fixed)
emit(f"xi={xi_fixed}: L<xi 时 xi_eff=L（线性增长）, L>xi 时 xi_eff=xi（平台）")
emit(f"交叉点 L≈{Ls[idx_cross]:.2f}（应≈xi=50，logspace 网格上界）")
emit(f"xi_eff 在交叉点两侧：min 前={Ls[idx_cross-1]:.2f}, min 后={xi_eff[idx_cross]:.2f}")
emit(f"Delta p ~ L^{-3/4}: L=100 -> {100**(-0.75):.4f}, L=1000 -> {1000**(-0.75):.4f}")
# logspace 网格上交叉点是第一个 > xi 的 L，落在 [xi, xi*步长] 区间
assert Ls[idx_cross] >= xi_fixed and Ls[idx_cross-1] <= xi_fixed
assert abs(xi_eff[idx_cross] - xi_fixed) < 1e-9

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].loglog(Ls, np.full_like(Ls, n_R1), label="R1: standard xi (L-independent)")
ax[0].loglog(Ls, n_R2, label="R2: global domain (diverges)")
ax[0].set_title("(A) n_eff vs system size L")
ax[0].set_xlabel("L"); ax[0].set_ylabel("n_eff")
ax[0].legend()

ax[1].loglog(deltas, n_eff, label="n_eff ~ delta^{-8/3}")
ax[1].set_title("(B) capacity scaling (slope=-8/3)")
ax[1].set_xlabel("delta = p - p_c"); ax[1].set_ylabel("n_eff")
ax[1].legend()

ax[2].loglog(Ls, xi_eff, label="xi_eff = min(xi, L)")
ax[2].axhline(xi_fixed, color="r", ls="--", label="xi")
ax[2].set_title("(C) finite-size crossover")
ax[2].set_xlabel("L"); ax[2].set_ylabel("xi_eff")
ax[2].legend()

fig.suptitle("R45: xi role in n_eff (ring 16, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"nu,{nu:.8f}\n")
    f.write(f"two_nu,{two_nu:.8f}\n")
    f.write(f"one_over_nu,{1/nu:.8f}\n")
    f.write(f"capacity_slope,{slope:.8f}\n")
    f.write(f"n_eff_R1_at_delta0.01,{n_R1:.6f}\n")
    f.write(f"crossover_L,{Ls[idx_cross]:.4f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
