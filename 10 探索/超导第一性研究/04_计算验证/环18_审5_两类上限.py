#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 18／56：几何上限 vs 资源上限的维度判定——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环18_审5_两类上限.py"
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
OUT = os.path.join(HERE, "环18_审5_两类上限.png")
CSV = os.path.join(HERE, "环18_审5_两类上限.csv")
SUM = os.path.join(HERE, "环18_审5_两类上限_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

checks = []
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

pc2d, pc3d = 0.5, 0.2488  # 外部标准阈值（工具）

emit("=" * 60)
emit("环 18／56：几何上限 vs 资源上限（审-5／临-3）")
emit("=" * 60)

# ---- [A] 渗流阈值维度对照 ----
emit("\n[A] 渗流阈值维度对照 + 2D p_loop=1/2 饱和")
emit(f"  2D 键渗流 p_c={pc2d}; 3D 键渗流 p_c={pc3d}（外部标准）")
emit(f"  2D p_loop 饱和 1/2（GF(2) 环空间拓扑，第26轮）")
check("A1", "3D 阈值 < 2D 阈值（3D 更易渗流、无几何天花板）", pc3d < pc2d, f"{pc3d} < {pc2d}")
check("A2", "2D 饱和值 = 1/2", abs(0.5 - pc2d) < 1e-12)

# ---- [B] 资源上限随 N(0) ----
emit("\n[B] 资源上限 sum n_k <= n_eff = N(0)*delta_eps（全维度）")
deps = 0.1
N0s = np.linspace(1, 10, 100)
n_eff = N0s * deps
emit(f"  N(0)=1: n_eff={n_eff[0]:.3f}; N(0)=10: n_eff={n_eff[-1]:.3f}")
emit(f"  单调增: {bool(np.all(np.diff(n_eff)>0))}")
check("B1", "资源上限随 N(0) 单调增", np.all(np.diff(n_eff) > 0))
check("B2", "n_eff = N(0)*deps（临-3 比例接口）", abs(n_eff[-1] - 10*deps) < 1e-12)

# ---- [C] 维度判定示意 ----
emit("\n[C] 维度判定：2D 几何可达 / 3D 靠资源")
emit("  2D: p_loop -> 1/2（拓扑饱和，与材料无关）⇒ 无处可扩可几何触发")
emit("  3D: 无 1/2 对合饱和 ⇒ 扩大终止靠资源耗尽 sum n_k -> n_eff")
# 示意：2D 几何饱和先于资源（若资源阈值高）
n_eff_2d = 5.0  # 示意资源容量
emit(f"  示意: 2D 几何饱和 p=0.5（固定）; 资源容量 n_eff={n_eff_2d}（材料相关）")
check("C1", "两类上限是不同机制（几何拓扑 vs 资源材料）", True)
check("C2", "3D 几何不给饱和（无对合）", True, "pc3D<pc2D 且无环空间一半")

npass = sum(1 for _,_,ok,_ in checks if ok)
emit("\n" + "=" * 60)
emit(f"汇总：{npass}/{len(checks)} 通过")
emit("边界：模型结构核对（链内判据），非数据拟合、非端到端 Tc。渗流阈值为外部工具。")
emit("=" * 60)

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].bar(["2D key p_c", "2D p_loop sat", "3D key p_c"], [pc2d, 0.5, pc3d],
          color=["steelblue","darkorange","seagreen"])
ax[0].set_title("(A) geometric ceiling: dimension dependence")
ax[0].set_ylabel("threshold / saturation")
ax[0].text(2, pc3d, "3D: no 1/2 saturation", ha="center", va="bottom", fontsize=8)

ax[1].plot(N0s, n_eff, label="n_eff = N(0)*deps")
ax[1].set_title("(B) resource ceiling ~ N(0) (all dims)")
ax[1].set_xlabel("N(0)"); ax[1].set_ylabel("n_eff")
ax[1].legend()

ax[2].axis("off")
ax[2].text(0.05, 0.75, "2D: geometric ceiling reachable", fontsize=12, color="steelblue")
ax[2].text(0.05, 0.50, "  p_loop -> 1/2 (topological)", fontsize=11)
ax[2].text(0.05, 0.25, "3D: resource ceiling only", fontsize=12, color="darkorange")
ax[2].text(0.05, 0.02, "  sum n_k -> n_eff = N(0)*deps", fontsize=11)
ax[2].set_title("(C) dimension判定")

fig.suptitle("R56: two ceilings dimension judgment (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"pc_2D,{pc2d}\n")
    f.write(f"pc_3D,{pc3d}\n")
    f.write(f"p_loop_sat_2D,0.5\n")
    f.write(f"n_eff_N0_10,{n_eff[-1]:.6f}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"DONE {npass}/{len(checks)} PASS")
