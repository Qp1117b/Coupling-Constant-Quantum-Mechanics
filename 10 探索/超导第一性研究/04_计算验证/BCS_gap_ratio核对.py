#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""弱耦合 gap ratio 2pi/e^gamma 高精度核对（mpmath，非拟合）"""
import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import mpmath as mp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "BCS_gap_ratio核对.png")
CSV = os.path.join(HERE, "BCS_gap_ratio核对.csv")
SUM = os.path.join(HERE, "BCS_gap_ratio核对_摘要.txt")

mp.mp.dps = 40
exact = 2*mp.pi/mp.e**mp.euler
log = []
def emit(s=""):
    print(s); log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

c5 = mp.mpf("3.528")       # C5 权威表
readme = mp.mpf("3.5278")  # README 565 行
al = mp.mpf("3.53")        # Al 精密实验

emit("=" * 60)
emit("弱耦合 gap ratio 2pi/e^gamma 高精度核对")
emit("=" * 60)
emit(f"  2pi/exp(gamma_E) = {mp.nstr(exact,22)}")
emit(f"  C5 表 3.528 diff   = {mp.nstr(abs(exact-c5),5)} (3位四舍五入)")
emit(f"  README 3.5278 diff = {mp.nstr(abs(exact-readme),5)} (4位)")
emit(f"  Al 实验 3.53 diff  = {mp.nstr(abs(exact-al)/exact*100,5)}%")

check("C1", "C5 表值 3.528 = 3 位四舍五入", abs(exact-c5) < mp.mpf("0.0005"))
check("C2", "README 3.5278 = 4 位正确", abs(exact-readme) < mp.mpf("0.00005"))
check("C3", "与 Al 实验相容 (<0.1%)", abs(exact-al)/exact < mp.mpf("0.001"), f"{mp.nstr(abs(exact-al)/exact*100,4)}%")
check("C4", "弱耦合比 > 3", exact > 3)

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 60)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("结论：C5 gap ratio 数值基础正确；理论3.5278 vs 实验3.53 差0.06%。")
emit("边界：BCS标准结果已标源；CQM C5同形非还原；纯数值核对，不给Tc。")
emit("=" * 60)

fig, ax = plt.subplots(figsize=(8, 4.5))
labels = ["2pi/e^gamma\n(high-precision)", "C5 table\n3.528", "README\n3.5278", "Al experiment\n3.53"]
vals = [float(exact), float(c5), float(readme), float(al)]
cols = ["steelblue","lightblue","lightgreen","darkorange"]
bars = ax.bar(labels, vals, color=cols)
ax.axhline(float(exact), color="r", ls="--", lw=1)
ax.set_ylabel("2 Delta(0)/kB Tc")
ax.set_title(f"BCS weak-coupling gap ratio check: {npass}/{len(checks)} PASS")
ax.set_ylim(3.50, 3.55)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, v, f"{v:.4f}", ha="center", va="bottom", fontsize=8)
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"exact_2pi_over_e_gamma,{mp.nstr(exact,22)}\n")
    f.write(f"C5_table,3.528\n")
    f.write(f"README,3.5278\n")
    f.write(f"Al_experiment,3.53\n")
    f.write(f"exp_dev_pct,{mp.nstr(abs(exact-al)/exact*100,8)}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
