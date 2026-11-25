#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""端到端 Tc: 用 CQM 自身 T* 式 (含 e^{-1/6}, 无 mu*) 直接检验（非拟合）"""
import os, sys, math
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "端到端_CQM自身T星判定.png")
CSV = os.path.join(HERE, "端到端_CQM自身T星判定.csv")
SUM = os.path.join(HERE, "端到端_CQM自身T星判定_摘要.txt")

log = []
def emit(s=""):
    print(s); log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

def cqm_tstar(lam, wlog_K):
    return 1.13*math.exp(-1/6)*wlog_K*math.exp(-(1+lam)/lam)

def ad_Tc(lam, wlog_K, mus):
    lam_eff = lam - mus*(1+0.62*lam)
    if lam_eff <= 0: return 0.0
    return (wlog_K/1.2)*math.exp(-1.04*(1+lam)/lam_eff)

systems = [
    ("Mo2NF2-CDW", 0.40, 219, 1.0),
    ("Mo2NF2-strain", 0.53, 272, 4.0),
    ("MgB2(iso)", 0.61, 737, 19.0),
]

emit("=" * 68)
emit("端到端 Tc: CQM 自身 T* 式直接检验（独立参数，非反解）")
emit("=" * 68)

names, cqm_vals, exp_vals, ad_vals, ratios = [], [], [], [], []
for name, lam, wlog, exp in systems:
    cqm = cqm_tstar(lam, wlog)
    ad = ad_Tc(lam, wlog, 0.10)
    ratio = cqm/exp
    names.append(name); cqm_vals.append(cqm); exp_vals.append(exp); ad_vals.append(ad); ratios.append(ratio)
    emit(f"\n{name}: lambda={lam}, wlog={wlog}K, exp={exp}K")
    emit(f"  CQM T* (no mu*) = {cqm:.2f}K, CQM/exp = {ratio:.2f}x")
    emit(f"  AD(mu*=0.10)    = {ad:.2f}K, AD/exp  = {ad/exp:.2f}x")
    check(f"O-{name}", f"{name}: CQM 高估 (ratio>1)", ratio > 1, f"{ratio:.2f}x")
    check(f"F-{name}", f"{name}: mu* 压制后落实验 (0.7-1.3x)", 0.7 <= ad/exp <= 1.3, f"{ad/exp:.2f}x")

emit("\n" + "=" * 68)
emit(f"汇总：{sum(1 for _,_,ok,_ in checks if ok)}/{len(checks)} 通过")
emit("结论：CQM 自身式高估 2.65-6.33x；mu* 压制决定性，落到实验 0.92-1.03x。")
emit("诚实边界：审-14 (mu*) 是决定性链外缺口；绝对 Tc 需能标+mu* 两外生输入；不给新Tc。")
emit("=" * 68)

fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
x = np.arange(len(names))
w = 0.25
ax[0].bar(x-w, cqm_vals, w, label="CQM T* (no mu*)", color="lightcoral")
ax[0].bar(x, exp_vals, w, label="experiment", color="steelblue")
ax[0].bar(x+w, ad_vals, w, label="AD(mu*=0.10)", color="seagreen")
ax[0].set_yscale("log")
ax[0].set_xticks(x); ax[0].set_xticklabels(names, fontsize=8)
ax[0].set_ylabel("Tc (K, log)"); ax[0].set_title("(A) CQM self-formula vs experiment")
ax[0].legend()

ax[1].bar(x, ratios, color=["lightcoral","darkorange","seagreen"])
ax[1].axhline(1, color="k", ls="--", label="experiment")
ax[1].set_xticks(x); ax[1].set_xticklabels(names, fontsize=8)
ax[1].set_ylabel("CQM/exp ratio"); ax[1].set_title("(B) overestimate 2.65-6.33x")
ax[1].legend()
for i, r in enumerate(ratios):
    ax[1].text(i, r, f"{r:.2f}x", ha="center", va="bottom", fontsize=8)

fig.suptitle("R67: end-to-end Tc via CQM's own T* (non-fit, independent params)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("system,lambda,wlog_K,exp_K,cqm_Tstar,cqm_over_exp,ad_mu010,ad_over_exp\n")
    for (name, lam, wlog, exp), c, a, r in zip(systems, cqm_vals, ad_vals, ratios):
        f.write(f"{name},{lam},{wlog},{exp},{c:.4f},{r:.4f},{a:.4f},{a/exp:.4f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {sum(1 for _,_,ok,_ in checks if ok)}/{len(checks)} PASS")
