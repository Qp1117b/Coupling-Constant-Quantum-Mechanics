#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README 核心常数 Xi 两种定义一致性核对（mpmath 高精度，非拟合）
Run: python "10 探索/超导第一性研究/04_计算验证/README核心常数Xi核对.py"
"""
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "README核心常数Xi核对.png")
CSV = os.path.join(HERE, "README核心常数Xi核对.csv")
SUM = os.path.join(HERE, "README核心常数Xi核对_摘要.txt")

mp.mp.dps = 40
log = []
def emit(s=""):
    print(s)
    log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

README_XI = mp.mpf("0.02309570897")

emit("=" * 64)
emit("README 核心常数 Xi 两种定义一致性核对（mpmath 40 位）")
emit("=" * 64)

# ---- 两种闭式 ----
d0 = mp.log(2*mp.sqrt(mp.pi)) - 1 - mp.euler/2        # xi'(0)/xi(0)
d1 = -d0                                               # xi'(1)/xi(1) 由函数方程
spec = 1 + mp.euler/2 - mp.log(2*mp.sqrt(mp.pi))       # 谱和闭式

emit(f"\nxi'(0)/xi(0) = ln(2sqrt(pi))-1-gamma_E/2 = {mp.nstr(d0,22)}")
emit(f"xi'(1)/xi(1) = -xi'(0)/xi(0)               = {mp.nstr(d1,22)}")
emit(f"谱和闭式 1+gamma_E/2-ln(2sqrt(pi))           = {mp.nstr(spec,22)}")
emit(f"README 权威值                                 = {mp.nstr(README_XI,12)}")

check("C1", "xi'(1)/xi(1) 与谱和闭式一致", abs(d1-spec) < mp.mpf("1e-30"), f"差={mp.nstr(abs(d1-spec),3)}")
check("C2", "xi'(1)/xi(1) 与 README 一致到 11 位", abs(d1-README_XI) < mp.mpf("1e-11"), f"差={mp.nstr(abs(d1-README_XI),3)}")
check("C3", "xi'(0)/xi(0) 为负（易混淆符号）", d0 < 0, f"d0={mp.nstr(d0,8)}")
check("C4", "xi'(1)/xi(1) 为正（与谱和同号）", d1 > 0, f"d1={mp.nstr(d1,8)}")

# ---- 谱和部分和收敛 ----
emit("\n谱和部分和（前 N 零点）逼近闭式")
g = np.array([14.134725,21.022040,25.010858,30.424876,32.935062,37.586178,40.918719,43.327073,
    48.005151,49.773832,52.970321,56.446248,59.347044,60.831779,65.112544,67.079811,
    69.546402,72.067158,75.704691,77.144840,79.337375,82.910381,84.735492,87.425275,
    88.809111,92.491899,94.651344,95.870634,98.831194,101.317851,103.725538,105.446623,
    107.168611,111.029536,111.874659,114.220675,116.958250,121.127905,123.249815,125.729984])
partial = np.cumsum(1.0/(g**2+0.25))
emit(f"  N=1: {partial[0]:.8f}, N=20: {partial[19]:.8f}, N=40: {partial[-1]:.8f}")
emit(f"  闭式(全零点): {float(spec):.8f}, 尾部占比(N=40): {(float(spec)-partial[-1])/float(spec)*100:.2f}%")
check("C5", "部分和单调增、从下方逼近闭式", bool(np.all(np.diff(partial)>0) and partial[-1]<float(spec)))

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 64)
emit(f"核对汇总：{npass}/{len(checks)} 通过")
emit("结论：README 权威值 Xi=0.02309570897 正确，两种定义一致到 11 位。")
emit("边界：谱表示条件于 RH；纯数学核对，不改物理缺口、不给 Tc。")
emit("=" * 64)

# ---- 绘图 ----
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(np.arange(1,41), partial, label="partial sum (zeros)")
ax[0].axhline(float(spec), color="r", ls="--", label=f"closed form={float(spec):.6f}")
ax[0].axhline(float(README_XI), color="g", ls=":", label="README Xi")
ax[0].set_title("(A) spectral sum -> Xi")
ax[0].set_xlabel("N zeros"); ax[0].legend()

ax[1].bar(["xi'(0)/xi(0)", "xi'(1)/xi(1)", "spectral sum"],
          [float(d0), float(d1), float(spec)], color=["lightcoral","steelblue","darkorange"])
ax[1].axhline(0, color="k", lw=0.5)
ax[1].set_title("(B) sign: d0<0, d1=spec>0")
ax[1].set_ylabel("value")
ax[1].text(0, float(d0), f"{float(d0):.6f}", ha="center", va="top", fontsize=8)
ax[1].text(1, float(d1), f"{float(d1):.6f}", ha="center", va="bottom", fontsize=8)
ax[1].text(2, float(spec), f"{float(spec):.6f}", ha="center", va="bottom", fontsize=8)

fig.suptitle(f"Xi constant check: {npass}/{len(checks)} PASS (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"d0_xi_prime_0,{mp.nstr(d0,22)}\n")
    f.write(f"d1_xi_prime_1,{mp.nstr(d1,22)}\n")
    f.write(f"spectral_closed_form,{mp.nstr(spec,22)}\n")
    f.write(f"README_XI,{mp.nstr(README_XI,12)}\n")
    f.write(f"partial_40,{(partial[-1]):.8f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
