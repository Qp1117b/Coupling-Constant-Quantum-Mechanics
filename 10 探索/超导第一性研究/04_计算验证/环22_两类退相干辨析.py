#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 22／26／53：空间退相干 vs 时间退相干辨析——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环22_两类退相干辨析.py"
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
OUT = os.path.join(HERE, "环22_两类退相干辨析.png")
CSV = os.path.join(HERE, "环22_两类退相干辨析.csv")
SUM = os.path.join(HERE, "环22_两类退相干辨析_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

# 示意参数（材料外生，只作形状检验）
sa = 0.1        # sigma_a（空间偏移展宽）
sv = 0.2        # sigma_v（固有时涨落）
tg = 1.0        # tau_g（关联时间）

emit("=" * 60)
emit("环 22／53：空间退相干（高斯、静态）vs 时间退相干（指数、动态）")
emit("=" * 60)

ga = 1.0 / sa                      # 空间截止 gamma_*^a
emit(f"空间截止 gamma_*^a = 1/sigma_a = {ga:.2f}（静态，与 t 无关）")
emit("时间截止 gamma_*^v(t) = 1/sqrt(2 sigma_v^2 tau_g t)（随 t 收缩）")

# ---- [A] 两类退相干在 gamma 谱上的截止 ----
emit("\n[A] gamma 谱上的两个退相干因子")
gv = np.linspace(0.1, 60, 500)
Rs = np.exp(-0.5*(gv*sa)**2)                    # 空间：高斯，静态
t0 = 5.0
Rt = np.exp(-gv**2 * sv**2 * tg * t0)           # 时间：指数，某时刻 t0
emit(f"  空间因子 R_n=exp(-g^2 sa^2/2): g={ga:.1f} 时 R={np.exp(-0.5*(ga*sa)**2):.3f}")
gt_v = 1/np.sqrt(2*sv**2*tg*t0)
emit(f"  时间因子 exp(-Gamma t0): g={gt_v:.2f} 时 exp(-1/2)=0.607")
emit(f"  数学型不同：高斯 vs 指数（主链1095行'不可混用'）")

# ---- [B] 交叉时刻 t_x ----
emit("\n[B] 交叉时刻 t_x = sigma_a^2/(2 sigma_v^2 tau_g)（已回改）")
tx = sa**2/(2*sv**2*tg)
emit(f"  t_x = {tx:.3f}")
for t in [tx*0.2, tx, tx*5]:
    gv_t = 1/np.sqrt(2*sv**2*tg*t)
    dom = "空间" if gv_t > ga else "时间"
    emit(f"  t={t:.3f}: gamma_*^v={gv_t:.2f}, gamma_*^a={ga:.2f} ⇒ {dom}主导")
assert tx > 0

# ---- [C] 可读窗口 gamma_* = min(ga, gv(t)) 随 t ----
emit("\n[C] 可读窗口 gamma_*(t) = min(空间截止, 时间截止)")
ts = np.logspace(-3, 4, 300)
gv_t = 1/np.sqrt(2*sv**2*tg*ts)
gstar = np.minimum(ga, gv_t)
cross_idx = np.argmax(gv_t < ga)
emit(f"  短时 t={ts[0]:.1e}: gamma_*={gstar[0]:.2f}（空间平台 1/sigma_a）")
emit(f"  长时 t={ts[-1]:.1e}: gamma_*={gstar[-1]:.3f}（时间支 ~ t^-1/2）")
emit(f"  交叉发生在 t≈{ts[cross_idx]:.3f}（理论 t_x={tx:.3f}）")
emit("  形状：平台 → t^-1/2 下降（N_eff 随之收缩，与 R23 同向）")
# logspace 网格分辨率有限，验证交叉点两侧确实发生主导切换（定性正确）
assert gstar[cross_idx-1] == ga and gstar[cross_idx] < ga
assert np.min(np.abs(np.log(ts/tx))) < np.log(3)  # 网格覆盖 t_x 附近

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(gv, Rs, label="spatial (Gaussian, static)")
ax[0].plot(gv, Rt, label=f"temporal (exp, t={t0})")
ax[0].axvline(ga, color="steelblue", ls="--", alpha=0.6, label="gamma_*^a")
ax[0].set_title("(A) two decoherence factors")
ax[0].set_xlabel("gamma_n"); ax[0].set_ylabel("fidelity factor")
ax[0].legend()

t_scan = np.logspace(-3, 4, 200)
gv_scan = 1/np.sqrt(2*sv**2*tg*t_scan)
ax[1].plot(t_scan, np.full_like(t_scan, ga), label="gamma_*^a (static)")
ax[1].plot(t_scan, gv_scan, label="gamma_*^v(t) ~ t^-1/2")
ax[1].axvline(tx, color="k", ls=":", label=f"t_x={tx:.2f}")
ax[1].set_title("(B) crossover at t_x")
ax[1].set_xlabel("t"); ax[1].set_ylabel("cutoff gamma_*")
ax[1].legend()

ax[2].loglog(ts, gstar, label="gamma_*(t)=min")
ax[2].axvline(tx, color="k", ls=":", label="crossover")
ax[2].set_title("(C) readable window: platform -> t^-1/2")
ax[2].set_xlabel("t"); ax[2].set_ylabel("gamma_*")
ax[2].legend()

fig.suptitle("R53: spatial vs temporal decoherence (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"gamma_star_a,{ga:.6f}\n")
    f.write(f"t_cross,{tx:.6f}\n")
    f.write(f"gamma_star_short,{gstar[0]:.6f}\n")
    f.write(f"gamma_star_long,{gstar[-1]:.6f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
