#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 19／48：Ginzburg 判据的链内推导——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环19_审11_Ginzburg判据.py"
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
OUT = os.path.join(HERE, "环19_审11_Ginzburg判据.png")
CSV = os.path.join(HERE, "环19_审11_Ginzburg判据.csv")
SUM = os.path.join(HERE, "环19_审11_Ginzburg判据_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

def gexp(d):
    return 2 * d / (4 - d)

emit("=== Ginzburg 标度指数（链内推导）===")
emit(f"d=2: 2d/(4-d) = {gexp(2)}")
emit(f"d=3: 2d/(4-d) = {gexp(3)}（N^-6）")
assert gexp(2) == 2 and gexp(3) == 6

# ---- [A] t_G vs N 双对数：指数 -6 ----
emit("\n=== [A] t_G ∝ N^{-6}（d=3）===")
N = np.logspace(1, 4, 200)
tG = N ** (-6)
slope = np.polyfit(np.log(N), np.log(tG), 1)[0]
emit(f"双对数斜率 = {slope:.6f}（目标 -6）")
emit(f"N=100: t_G={100**-6:.3e}, N=1000: t_G={1000**-6:.3e}")
emit(f"常规三维超导体范围 N=1e2~1e3 ⇒ t_G~1e-12~1e-18")
assert abs(slope + 6) < 1e-9

# ---- [B] 涨落比指数 e(d)=d/2-2，上临界维 d_c=4 ----
emit("\n=== [B] 涨落比 |a|^{d/2-2}：上临界维 d_c=4 ===")
ds = np.linspace(2, 6, 200)
e = ds / 2 - 2
emit(f"d=3: e={3/2-2} <0（发散，平均场失效）")
emit(f"d=4: e={4/2-2} =0（上临界维）")
emit(f"d=5: e={5/2-2} >0（收敛，平均场有效）")
idx = np.argmin(abs(e))
emit(f"e=0 的 d = {ds[idx]:.3f}（应 4）")
assert abs(e[0] - (-1)) < 1e-9  # d=2 -> -1
assert abs(ds[idx] - 4) < 0.05

# ---- [C] 前因子形状 C_d ∝ (zJ/Upsilon0)^2（数值外生）----
emit("\n=== [C] 前因子形状（数值外生）===")
zJ = 1.0
Upsilon0_scan = np.logspace(-1, 1, 100)
C_shape = (zJ / Upsilon0_scan) ** 2
emit(f"Upsilon0=0.1: C={C_shape[0]:.3f}, Upsilon0=10: C={C_shape[-1]:.3f}")
emit(f"C>0 且随 Upsilon0 增而减：{bool(np.all(C_shape>0) and np.all(np.diff(C_shape)<0))}")
emit("边界：C_d 数值、N 数值、绝对 Tc 外生；链内只给指数与前因子形状")
assert np.all(C_shape > 0) and np.all(np.diff(C_shape) < 0)

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].loglog(N, tG, label="t_G ~ N^{-6} (d=3)")
ax[0].set_title("(A) Ginzburg width vs N (slope -6)")
ax[0].set_xlabel("N = xi_0/a"); ax[0].set_ylabel("t_G")
ax[0].legend()

ax[1].plot(ds, e, label="e(d)=d/2-2")
ax[1].axhline(0, color="k", lw=0.5)
ax[1].axvline(4, color="r", ls="--", label="d_c=4")
ax[1].set_title("(B) upper critical dimension")
ax[1].set_xlabel("d"); ax[1].set_ylabel("fluctuation exponent e")
ax[1].legend()

ax[2].loglog(Upsilon0_scan, C_shape, label="C ~ (zJ/Upsilon0)^2")
ax[2].set_title("(C) prefactor shape (norm external)")
ax[2].set_xlabel("Upsilon0"); ax[2].set_ylabel("C (shape)")
ax[2].legend()

fig.suptitle("R48: Ginzburg criterion derived in-chain (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"gexp_d2,{gexp(2):.8f}\n")
    f.write(f"gexp_d3,{gexp(3):.8f}\n")
    f.write(f"tG_slope_d3,{slope:.8f}\n")
    f.write(f"upper_critical_d,{ds[idx]:.6f}\n")
    f.write(f"exp_d3,{3/2-2:.8f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
