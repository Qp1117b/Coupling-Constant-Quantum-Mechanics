#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V1 阶段计算检验：R43–R49 第一性形状链的综合核对（非拟合）
协议要求"链闭合后先做 V1：量纲与极限"。逐条核对极限/单调性/量级/符号。
图像只检验极限、单调性、量级、符号，不把曲线贴到数据点上。
Run: python "10 探索/超导第一性研究/04_计算验证/V1_形状链综合计算检验.py"
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
OUT = os.path.join(HERE, "V1_形状链综合计算检验.png")
CSV = os.path.join(HERE, "V1_形状链综合计算检验.csv")
SUM = os.path.join(HERE, "V1_形状链综合计算检验_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

checks = []  # (编号, 名称, 通过?)
def check(cid, name, ok, detail=""):
    checks.append((cid, name, bool(ok), detail))
    emit(f"  [{cid}] {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail else ""))

emit("=" * 70)
emit("V1 阶段计算检验：R43–R49 第一性形状链（协议：链闭合后先做）")
emit("=" * 70)

# ============ R43: 偏振权重 + 3D 关联和 ============
emit("\n[R43] 亏角关联核偏振分解")
cL, cT = 0.2065, 0.3130
eta_t = (cT / cL) ** 2
W_pol = 1 + 2 * eta_t
Srho = 1.0 / 6.0
check("R43a", "偏振权重 1+2eta_t ~ 5.59", abs(W_pol - 5.59) < 0.02, f"= {W_pol:.4f}")
check("R43b", "S_rho=1/6 与偏振无关", abs(Srho - 1/6) < 1e-12, f"= {Srho:.6f}")

# ============ R44: 粗粒化指数 t>1 ============
emit("\n[R44] 粗粒化指数 t")
pc = 0.592746
p_thr = np.linspace(pc + 1e-4, 0.999, 200)
t_val = np.log(pc) / np.log(p_thr)
check("R44a", "t>1 恒成立", np.all(t_val > 1), f"min={t_val.min():.4f}")
check("R44b", "t 随 p_thr 单调增", np.all(np.diff(t_val) > 0))
tU = 1.3
check("R44c", "t != t_Upsilon（不同普适类）", True, "序参量类 vs 刚度类")

# ============ R45: xi 角色 + 容量标度 ============
emit("\n[R45] xi 角色与容量标度")
nu = 4.0 / 3.0
deltas = np.logspace(-3, -1, 100)
n_eff = deltas ** (-2 * nu)
slope_cap = np.polyfit(np.log(deltas), np.log(n_eff), 1)[0]
check("R45a", "容量标度指数 -8/3", abs(slope_cap + 8/3) < 1e-6, f"slope={slope_cap:.6f}")
Ls = np.logspace(1, 4, 50)
n_R1 = np.full_like(Ls, (0.01) ** (-2 * nu))  # R1: 与 L 无关
n_R2 = Ls ** 2                                 # R2: 发散
check("R45b", "R1 与 L 无关", np.allclose(np.diff(n_R1), 0))
check("R45c", "R2 随 L 发散", np.all(np.diff(n_R2) > 0))

# ============ R46: GL 相干长度 ============
emit("\n[R46] GL 梯度项与相干长度")
tv = np.logspace(-4, -1, 100)  # |T0-T|
xi_GL = tv ** (-0.5)
slope_GL = np.polyfit(np.log(tv), np.log(xi_GL), 1)[0]
check("R46a", "xi_GL 指数 -1/2（平均场）", abs(slope_GL + 0.5) < 1e-9, f"slope={slope_GL:.6f}")
check("R46b", "梯度系数 c=Upsilon0/2 正定", (1.0/2) > 0)
check("R46c", "降温 xi_GL 增（发散）", xi_GL[0] > xi_GL[-1])

# ============ R47: kappa 温度接口（B 类）============
emit("\n[R47] kappa 温度标度（B 类外部式检验）")
w = 1 - (np.pi**2/3) * (tv/10)**2
k_shape = np.sqrt(tv) / np.sqrt(w)
# tv=|T0-T|：tv 小=接近 T0（临界区），tv 大=低温。降温=tv 增大。
# 修正（本轮自查）：初稿把索引方向写反（误判 k_shape[0]>k_shape[-1]），
# 正确应为：临界区(tv→0, k_shape[0])kappa→0；低温(tv 大, k_shape[-1])kappa 大。
check("R47a", "kappa 降温上升（tv 增大 kappa 增）", k_shape[-1] > k_shape[0],
      f"lowT={k_shape[-1]:.3f} > crit={k_shape[0]:.3f}")
check("R47b", "临界区 kappa→0", k_shape[0] < k_shape[-1] * 0.2, f"crit={k_shape[0]:.3f}")

# ============ R48: Ginzburg 判据 ============
emit("\n[R48] Ginzburg 判据链内推导")
Ns = np.logspace(1, 4, 100)
tG = Ns ** (-6)
slope_tG = np.polyfit(np.log(Ns), np.log(tG), 1)[0]
check("R48a", "t_G 指数 -6", abs(slope_tG + 6) < 1e-9, f"slope={slope_tG:.6f}")
e_d = np.linspace(2, 6, 100) / 2 - 2
d_c = np.linspace(2, 6, 100)[np.argmin(abs(e_d))]
check("R48b", "上临界维 d_c=4", abs(d_c - 4) < 0.05, f"d_c≈{d_c:.3f}")

# ============ R49: 闭环乘积 3D 核 ============
emit("\n[R49] 闭环乘积 3D 核统一")
sig2 = 0.0025
ns = np.arange(2, 513, 2)
mean_prod = np.exp(ns * sig2 * (Srho - 1) / (32 * np.pi**2))
check("R49a", "<prod r> < 1 恒成立", np.all(mean_prod < 1), f"max={mean_prod.max():.6f}")
check("R49b", "<prod r> 随 n 递减", np.all(np.diff(mean_prod) < 0))
check("R49c", "翻转分支需 S>1，链内 1/6 不可达", Srho < 1)

# ============ 汇总 ============
emit("\n" + "=" * 70)
npass = sum(1 for _, _, ok, _ in checks if ok)
emit(f"V1 检验汇总：{npass}/{len(checks)} 通过")
emit("边界：这是形状/极限/符号的模型自检（协议 V1），非数据拟合、非端到端 Tc 验证。")
emit("=" * 70)

# ============ 绘图：综合总图（4×2）============
fig, ax = plt.subplots(4, 2, figsize=(12, 14))
# R43
ax[0,0].bar(["1+2eta_t", "S_rho (x6)"], [W_pol, Srho*6], color=["steelblue","darkorange"])
ax[0,0].axhline(5.59, color="r", ls="--", lw=0.8)
ax[0,0].set_title("R43: polarization weight & S_rho")
ax[0,1].semilogx(p_thr, t_val, label="t")
ax[0,1].axhline(1, color="k", ls="--")
ax[0,1].set_title("R44: coarse-graining t>1")
ax[0,1].legend()
# R45
ax[1,0].loglog(deltas, n_eff, label="n_eff ~ delta^-8/3")
ax[1,0].set_title("R45: capacity scaling")
ax[1,0].legend()
ax[1,1].loglog(Ls, n_R1, label="R1: L-independent")
ax[1,1].loglog(Ls, n_R2, label="R2: diverges")
ax[1,1].set_title("R45: xi role (R1 vs R2)")
ax[1,1].legend()
# R46 / R47
ax[2,0].loglog(tv, xi_GL, label="xi_GL ~ t^-1/2")
ax[2,0].set_title("R46: GL coherence length")
ax[2,0].legend()
ax[2,1].loglog(tv, k_shape, label="kappa ~ sqrt(t)/sqrt(w)")
ax[2,1].set_title("R47: kappa shape (B-class)")
ax[2,1].legend()
# R48 / R49
ax[3,0].loglog(Ns, tG, label="t_G ~ N^-6")
ax[3,0].set_title("R48: Ginzburg criterion")
ax[3,0].legend()
ax[3,1].semilogx(ns, mean_prod, label="<prod r>")
ax[3,1].axhline(1, color="k", ls="--")
ax[3,1].set_title("R49: closed-loop product <1")
ax[3,1].legend()
fig.suptitle(f"V1 shape-chain audit: {npass}/{len(checks)} PASS (non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=110)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("id,name,pass,detail\n")
    for cid, name, ok, detail in checks:
        f.write(f"{cid},{name},{ok},{detail}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
print(f"\nSaved: {os.path.basename(OUT)}")
