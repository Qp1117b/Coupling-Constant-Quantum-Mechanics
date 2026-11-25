#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 15／44：层 B→C 粗粒化指数 t 的链内判定——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环15_粗粒化指数t.py"
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
OUT = os.path.join(HERE, "环15_粗粒化指数t.png")
CSV = os.path.join(HERE, "环15_粗粒化指数t.csv")
SUM = os.path.join(HERE, "环15_粗粒化指数t_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

# 外部普适指数（2D 座渗流，作工具，不作 CQM 结论）
beta = 5.0 / 36.0   # 序参量指数
nu = 4.0 / 3.0      # 关联长度指数
pc = 0.592746       # 2D 座渗流阈值（项目已用）
tU = 1.3            # 刚度指数 t_Upsilon（项目已用）

emit("=== 2D 座渗流普适指数（外部工具）===")
emit(f"beta = 5/36 = {beta:.6f}")
emit(f"nu   = 4/3  = {nu:.6f}")
emit(f"beta/nu = {beta/nu:.6f} (5/48={5/48:.6f})")
emit(f"1/nu = {1/nu:.6f} (3/4={0.75})")
assert abs(beta/nu - 5/48) < 1e-9
assert abs(1/nu - 0.75) < 1e-9

# ---- [A] 阈值邻域对数斜率：p^t 有限 vs 序参量发散 ----
emit("\n=== [A] 阈值邻域对数斜率 ===")
deltas = np.logspace(-4, -0.5, 200)          # delta = p_pair - p_c
t_guess = 0.5                                # 示意：幂律 p^t 的指数
slope_power = np.full_like(deltas, t_guess)   # p^t 给有限 t
slope_critical = beta / deltas               # 序参量给 beta/delta -> 无穷
emit(f"delta=1e-4: p^t 斜率={slope_power[0]:.3f}, 序参量斜率={slope_critical[0]:.1f}")
emit(f"delta=0.3 : p^t 斜率={slope_power[-1]:.3f}, 序参量斜率={slope_critical[-1]:.3f}")
emit("判据：临界邻域序参量斜率发散，p^t 有限 ⇒ p^t 不能精确，只能远离阈值插值")
assert slope_critical[0] > slope_power[0] * 10

# ---- [B] 链内结构判定 t = ln(pc)/ln(p_thr) > 1（p_thr in (pc,1)）----
emit("\n=== [B] t = ln(p_c)/ln(p_thr) > 1（p_thr > p_c）===")
p_thr = np.linspace(pc + 1e-4, 0.999, 300)
t_struct = np.log(pc) / np.log(p_thr)
emit(f"p_thr=0.60: t={np.log(pc)/np.log(0.60):.6f}")
emit(f"p_thr=0.90: t={np.log(pc)/np.log(0.90):.6f}")
emit(f"p_thr->1^-: t->{np.log(pc)/np.log(0.999):.6f} (发散)")
emit(f"t 恒 > 1：{bool(np.all(t_struct > 1))}")
emit(f"t 随 p_thr 增而增：{bool(np.all(np.diff(t_struct) > 0))}")
assert np.all(t_struct > 1)
assert np.all(np.diff(t_struct) > 0)
teff = t_struct  # 供绘图面板复用

# ---- [C] 普适类区分：t（序参量类）vs t_Upsilon（刚度类）----
emit("\n=== [C] 普适类区分 ===")
emit(f"序参量指数 beta = {beta:.6f}")
emit(f"刚度指数 t_Upsilon = {tU:.6f}")
emit(f"beta < t_Upsilon：{beta < tU}；beta != tU：{abs(beta-tU)>1e-6}")
emit("判据：t 属序参量类（beta=0.139），t_Upsilon 属刚度类（1.3），不同类无等式")
assert beta < tU and abs(beta - tU) > 1e-6

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].loglog(deltas, slope_power, label="p^t: slope=t (finite)")
ax[0].loglog(deltas, slope_critical, label="P_inf: beta/delta (diverges)")
ax[0].set_title("(A) log-slope near threshold")
ax[0].set_xlabel("delta = p_pair - p_c"); ax[0].set_ylabel("log slope")
ax[0].legend()

ax[1].plot(p_thr, teff, label="t=ln(pc)/ln(p_thr)")
ax[1].axhline(1.0, color="r", ls="--", label="t=1 (compression bound)")
ax[1].set_title("(B) structural exponent t > 1")
ax[1].set_xlabel("p_thr"); ax[1].set_ylabel("t")
ax[1].legend()

classes = ["order param\n(beta)", "stiffness\n(t_Upsilon)"]
vals = [beta, tU]
ax[2].bar(classes, vals, color=["steelblue", "darkorange"])
ax[2].set_title("(C) universality classes (no equality)")
ax[2].set_ylabel("exponent value")
for i, v in enumerate(vals):
    ax[2].text(i, v, f"{v:.3f}", ha="center", va="bottom")

fig.suptitle("R44: coarse-graining exponent t (ring 15, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"beta,{beta:.8f}\n")
    f.write(f"nu,{nu:.8f}\n")
    f.write(f"beta_over_nu,{beta/nu:.8f}\n")
    f.write(f"one_over_nu,{1/nu:.8f}\n")
    f.write(f"pc,{pc:.8f}\n")
    f.write(f"t_Upsilon,{tU:.8f}\n")
    f.write(f"t_pthr0.60,{np.log(pc)/np.log(0.60):.6f}\n")
    f.write(f"t_pthr0.90,{np.log(pc)/np.log(0.90):.6f}\n")
    f.write(f"t_min_over_scan,{float(np.min(t_struct)):.6f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
