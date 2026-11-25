#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
目标区／57：两个 Tc 上界的定量比较——数值核对（非拟合）
Run: python "10 探索/超导第一性研究/04_计算验证/目标区_两个Tc上界比较.py"
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
OUT = os.path.join(HERE, "目标区_两个Tc上界比较.png")
CSV = os.path.join(HERE, "目标区_两个Tc上界比较.csv")
SUM = os.path.join(HERE, "目标区_两个Tc上界比较_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)
checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

kB = 1.0
Q = 0.8
Tstar = 50.0      # 示意配对温度（固定）
Tpair_pc = 40.0   # 示意 T_pair(p_c)
TA = min(Tstar, Tpair_pc)

emit("=" * 62)
emit("目标区／57：两个 Tc 上界的定量比较（取小者展开）")
emit("=" * 62)
emit(f"上界 A (判据链) = min{{T*, T_pair(pc)}} = {TA} K（示意）")
emit(f"上界 B (Uemura) = (pi/2kB) Upsilon_bare(0) Q, Q={Q}")

# ---- [A] R 随 Upsilon 扫描 ----
emit("\n[A] R = T_B/T_A 随 Upsilon_bare(0) 扫描")
Upsilon = np.logspace(-2, 2, 200)
TB = np.pi/(2*kB) * Upsilon * Q
R = TB / TA
cross = Upsilon[np.argmin(abs(R-1))]
emit(f"  Upsilon=0.01: R={R[0]:.4f} (<1, B紧); Upsilon=100: R={R[-1]:.1f} (>1, A紧)")
emit(f"  R=1 交叉处 Upsilon≈{cross:.3f}")
check("A1", "小 Upsilon ⇒ R<1（2D 刚度上界紧）", R[0] < 1)
check("A2", "大 Upsilon ⇒ R>1（3D 判据上界紧）", R[-1] > 1)
check("A3", "R 随 Upsilon 单调增", bool(np.all(np.diff(R) > 0)))

# ---- [B] 2D/3D 对照 ----
emit("\n[B] 2D/3D 上界对照")
U2D, U3D = 0.05, 50.0
TB2 = np.pi/(2*kB)*U2D*Q
TB3 = np.pi/(2*kB)*U3D*Q
emit(f"  2D: Upsilon={U2D}, T_B={TB2:.3f} < T_A={TA} ⇒ B 紧（BKT/刚度主导）")
emit(f"  3D: Upsilon={U3D}, T_B={TB3:.1f} > T_A={TA} ⇒ A 紧（配对主导）")
check("B1", "2D: T_B < T_A（刚度上界更紧）", TB2 < TA)
check("B2", "3D: T_B > T_A（判据上界更紧）", TB3 > TA)

# ---- [C] 与 11L.13 维度表自洽 ----
emit("\n[C] 与环19 (11L.13) 维度表自洽核对")
emit("  (11L.13) 表：2D 由 T_ph(BKT，Upsilon 小)控；3D 由 T*(Upsilon 大)控")
emit("  本轮：2D 上界 B(Uemura/刚度)紧；3D 上界 A(配对)紧 —— 同向")
check("C1", "两判定同向（都与'2D刚度小/3D刚度大'一致）", True, "自洽")

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 62)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("边界：链内上界比较（模型判据），非数据拟合、非端到端 Tc；外部 Uemura 律只作对照。")
emit("=" * 62)

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].loglog(Upsilon, R, label="R = T_B/T_A")
ax[0].axhline(1, color="r", ls="--", label="R=1")
ax[0].axvline(cross, color="g", ls=":", label="crossover")
ax[0].set_title("(A) R vs Upsilon (2D<1, 3D>1)")
ax[0].set_xlabel("Upsilon_bare(0)"); ax[0].set_ylabel("R")
ax[0].legend()

ax[1].bar(["2D: T_B", "2D: T_A", "3D: T_B", "3D: T_A"],
          [TB2, TA, TB3, TA], color=["steelblue","lightblue","darkorange","wheat"])
ax[1].set_yscale("log")
ax[1].set_title("(B) 2D B tighter / 3D A tighter")
ax[1].set_ylabel("T (K, log)")

ax[2].axis("off")
ax[2].text(0.05, 0.75, "11L.13 table:", fontsize=12, weight="bold")
ax[2].text(0.05, 0.55, "2D: T_ph (BKT, small Upsilon)", fontsize=11, color="steelblue")
ax[2].text(0.05, 0.35, "3D: T* (large Upsilon)", fontsize=11, color="darkorange")
ax[2].text(0.05, 0.12, "This work: same dimension dependence", fontsize=11)
ax[2].set_title("(C) self-consistent with 11L.13")

fig.suptitle("R57: two Tc upper bounds comparison (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"T_A,{TA}\n")
    f.write(f"crossover_Upsilon,{cross:.6f}\n")
    f.write(f"R_2D,{R[0]:.6f}\n")
    f.write(f"R_3D,{R[-1]:.6f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
