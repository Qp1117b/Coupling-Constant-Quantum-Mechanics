#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Morel-Anderson 形状对 R67 经验 mu*=0.10 的解释（非拟合，链内形状+标准工具）"""
import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "审14_MorelAnderson解释.png")
CSV = os.path.join(HERE, "审14_MorelAnderson解释.csv")
SUM = os.path.join(HERE, "审14_MorelAnderson解释_摘要.txt")

log = []
def emit(s=""):
    print(s); log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

def mu_star(mu, L):
    return mu / (1 + mu*L)

emit("=" * 68)
emit("Morel-Anderson 形状对 R67 经验 mu* 的解释（审-14 定量推进）")
emit("=" * 68)
emit("mu* = mu/(1+mu*L), L = ln(eps_F/hbar omega_D), 链内 R25 给 L 的来源")
emit("")

# 表1：典型 L 下裸 mu=0.2 的 mu*
emit("表1: mu* vs L (裸 mu=0.2)")
emit("-" * 50)
Lvals = [2.0, 3.0, 4.0, 5.0]
mus02 = [mu_star(0.2, L) for L in Lvals]
for L, ms in zip(Lvals, mus02):
    emit(f"  L={L:.1f}: mu*={ms:.4f}")
check("T1", "裸mu=0.2 给 mu* 落在 0.10-0.15 (典型L)", all(0.10 <= ms <= 0.15 for ms in mus02))

# 表2：达 mu*=0.10 需裸 mu
emit("")
emit("表2: 达 mu*=0.10 所需裸 mu = 0.10/(1-0.10 L)")
emit("-" * 50)
bare_mus = []
for L in Lvals:
    bm = 0.10/(1 - 0.10*L)
    bare_mus.append(bm)
    emit(f"  L={L:.1f}: bare mu={bm:.4f}")
check("T2", "反解裸 mu 落常规金属范围 [0.1, 0.25]", all(0.10 <= bm <= 0.25 for bm in bare_mus))

# 表3：验证 mu* 被压制成普适小（mu 越大压制越强）
emit("")
emit("表3: 压制比 mu*/mu（L=4）")
emit("-" * 50)
for mu in [0.2, 0.3, 0.4, 0.5]:
    ms = mu_star(mu, 4.0)
    emit(f"  bare mu={mu:.1f}: mu*={ms:.4f}, 压制比={ms/mu:.3f}")
check("T3", "mu* < mu（对数压制成立）", all(mu_star(m, 4.0) < m for m in [0.2,0.3,0.4,0.5]))

# 核心：R67 经验 mu*=0.10 有形状来源
check("CORE", "R67经验mu*=0.10 落在裸mu=0.1-0.2 的形状范围",
      any(abs(mu_star(mu, L) - 0.10) < 0.03
          for L in Lvals for mu in [0.10, 0.125, 0.15, 0.20]),
      "裸mu=0.125-0.20 在 L=2-5 给 mu*=0.10-0.14")

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("")
emit("=" * 68)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("结论：Morel-Anderson 对数压制把裸mu(0.1-0.2)化为普适小mu*(~0.10)，")
emit("        R67经验值有链内形状来源；仍不闭合审-14（裸mu/z_v/m外生）。")
emit("边界：不给mu*精确数值、不给新Tc、不改缺口状态。")
emit("=" * 68)

# 图：两条面板
fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
L = np.linspace(1.5, 6.0, 200)
for mu, col in [(0.125,"steelblue"),(0.15,"seagreen"),(0.2,"darkorange"),(0.3,"lightcoral")]:
    ax[0].plot(L, mu_star(mu, L), label=f"bare mu={mu}", color=col, lw=1.8)
ax[0].axhline(0.10, color="k", ls="--", lw=1, label="R67 empirical mu*=0.10")
ax[0].set_xlabel("L = ln(eps_F / hbar omega_D)")
ax[0].set_ylabel("mu* (Morel-Anderson)")
ax[0].set_title("(A) logarithmic suppression -> universal small mu*")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)
ax[0].set_xlim(1.5, 6.0); ax[0].set_ylim(0.05, 0.20)

# 面板B：反解裸 mu vs L
ax[1].plot(Lvals, bare_mus, "o-", color="steelblue", label="bare mu needed")
ax[1].axhspan(0.10, 0.25, color="lightgreen", alpha=0.4, label="conventional metal range")
ax[1].set_xlabel("L = ln(eps_F / hbar omega_D)")
ax[1].set_ylabel("bare mu needed for mu*=0.10")
ax[1].set_title("(B) R67 mu*=0.10 needs ordinary bare mu")
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
for Lv, bm in zip(Lvals, bare_mus):
    ax[1].annotate(f"{bm:.3f}", (Lv, bm), textcoords="offset points", xytext=(0,7), ha="center", fontsize=8)

fig.suptitle("R68: Morel-Anderson shape explains R67 empirical mu* (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("L,mu_star_bare_0p2,bare_mu_for_0p10\n")
    for L, ms, bm in zip(Lvals, mus02, bare_mus):
        f.write(f"{L},{ms:.6f},{bm:.6f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
