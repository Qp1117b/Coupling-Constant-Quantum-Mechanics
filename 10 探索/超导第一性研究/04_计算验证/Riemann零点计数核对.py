#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Riemann-von Mangoldt 计数公式核对（MathWorld OEIS A072080 数据，非拟合）"""
import os, sys, math
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Riemann零点计数核对.png")
CSV = os.path.join(HERE, "Riemann零点计数核对.csv")
SUM = os.path.join(HERE, "Riemann零点计数核对_摘要.txt")

log = []
def emit(s=""):
    print(s); log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

# MathWorld OEIS A072080: zeros with imag < T (multiplicity)
T = np.array([1e2, 1e3, 1e4, 1e5, 1e6])
N = np.array([29, 649, 10142, 138069, 1747146])
asym = T/(2*np.pi)*np.log(T/(2*np.pi))
ratio = N/asym

emit("=" * 62)
emit("Riemann-von Mangoldt N(T) ~ T/(2pi) ln(T/(2pi)) 核对")
emit("数据源: MathWorld OEIS A072080 (webfetch)")
emit("=" * 62)
for Ti, Ni, ai, ri in zip(T, N, asym, ratio):
    emit(f"  T={Ti:.0e}: N={Ni:>8}, asym={ai:>12.1f}, ratio={ri:.4f}")

check("C1", "比值单调趋向 1", bool(np.all(np.diff(ratio) > 0)), f"{ratio[0]:.3f}->{ratio[-1]:.3f}")
check("C2", "最大 T 处比值 > 0.9（收敛方向正确）", ratio[-1] > 0.9, f"{ratio[-1]:.4f}")
# 次领头修正: N = T/(2pi)ln(T/(2pi)) - T/(2pi) + O(ln T)
asym2 = T/(2*np.pi)*np.log(T/(2*np.pi)) - T/(2*np.pi)
ratio2 = N/asym2
emit("\n含次领头项 -T/(2pi):")
for Ti, Ni, ri2 in zip(T, N, ratio2):
    emit(f"  T={Ti:.0e}: ratio2={ri2:.4f}")
check("C3", "含次领头项后比值更接近 1", np.mean(abs(ratio2-1)) < np.mean(abs(ratio-1)),
      f"|err| {np.mean(abs(ratio-1)):.3f}->{np.mean(abs(ratio2-1)):.3f}")

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 62)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("结论：主链使用的 Riemann-von Mangoldt 计数公式正确（比值趋向1）。")
emit("对CQM: 确认 R50 Xi收敛/R52 对偶/可读窗口的计数基础；计数公式是外部标准，非CQM推出。")
emit("=" * 62)

fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
ax[0].loglog(T, N, "o-", label="N_exact (OEIS A072080)")
ax[0].loglog(T, asym, "s--", label="T/(2pi) ln(T/(2pi))")
ax[0].loglog(T, asym2, "^:", label="with -T/(2pi) term")
ax[0].set_xlabel("T"); ax[0].set_ylabel("N(T)")
ax[0].set_title("(A) zero counting vs asymptotic")
ax[0].legend()

ax[1].semilogx(T, ratio, "o-", label="N/asym (leading)")
ax[1].semilogx(T, ratio2, "s--", label="N/asym with subleading")
ax[1].axhline(1, color="k", ls="--")
ax[1].set_xlabel("T"); ax[1].set_ylabel("ratio")
ax[1].set_title("(B) ratio -> 1 (non-fit)")
ax[1].legend()

fig.suptitle(f"R62: Riemann-von Mangoldt check {npass}/{len(checks)} PASS")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("T,N_exact,asym_leading,ratio,asym_subleading,ratio2\n")
    for Ti, Ni, ai, ri, a2, r2 in zip(T, N, asym, ratio, asym2, ratio2):
        f.write(f"{Ti:.0f},{Ni},{ai:.2f},{ri:.4f},{a2:.2f},{r2:.4f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
