#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M1 判别子核对：零点相邻比（非拟合）"""
import os, sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "M1_零点判别子核对.png")
CSV = os.path.join(HERE, "M1_零点判别子核对.csv")
SUM = os.path.join(HERE, "M1_零点判别子核对_摘要.txt")

log = []
def emit(s=""):
    print(s); log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

g = np.array([14.134725, 21.022040, 25.010858, 30.424876, 32.935062])
g1 = g[0]
ratios = g[1:4]/g1  # gamma_2/gamma_1, gamma_3/gamma_1, gamma_4/gamma_1（主链登记3个）
registered = np.array([1.4873, 1.7695, 2.1525])  # 主链第634行登记值

emit("=" * 60)
emit("M1 判别子核对：零点相邻比 gamma_{n+1}/gamma_1")
emit("=" * 60)
emit(f"gamma_1 = {g1}")
for i, r in enumerate(ratios, start=2):
    emit(f"  gamma_{i}/gamma_1 = {r:.6f}")
emit(f"主链登记: {registered}")

for i, (calc, reg) in enumerate(zip(ratios, registered), start=2):
    check(f"R{i}", f"gamma_{i}/gamma_1 吻合登记值(4位)", abs(calc-reg) < 5e-5, f"{calc:.6f} vs {reg}")

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 60)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("结论：主链第634行的M1判别子数值正确（4位有效数字）。")
emit("边界：判别子数学正确性核对，非M1物理证实；零点虚部是标准数学常数，不改缺口、不给Tc。")
emit("=" * 60)

fig, ax = plt.subplots(figsize=(8, 4.5))
x = np.arange(2, 5)
ax.plot(x, ratios, "o-", label="computed gamma_n/gamma_1")
ax.plot(x, registered, "s--", label="registered (main chain)")
for i, (c, r) in enumerate(zip(ratios, registered)):
    ax.annotate(f"{c:.4f}", (x[i], ratios[i]), textcoords="offset points", xytext=(0,8), ha="center", fontsize=8)
ax.set_xlabel("n"); ax.set_ylabel("gamma_n / gamma_1")
ax.set_title(f"M1 discriminant check: {npass}/{len(checks)} PASS (non-fit)")
ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("n,computed,registered,abs_diff\n")
    for i, (c, r) in enumerate(zip(ratios, registered), start=2):
        f.write(f"{i},{c:.8f},{r:.8f},{abs(c-r):.2e}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
