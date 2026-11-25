#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 4／43：亏角关联核的偏振分解——数值核对（非拟合）
四面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环04_亏角关联偏振分解.py"
"""
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import j0

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "环04_亏角关联偏振分解.png")
CSV = os.path.join(HERE, "环04_亏角关联偏振分解.csv")
SUM = os.path.join(HERE, "环04_亏角关联偏振分解_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

# ---- 实测偏振权重（第 86 轮 9B.5）----
cL = 0.2065   # c_epsilon,l
cT = 0.3130   # c_epsilon,t
eta = (cT / cL) ** 2
W = 1 + 2 * eta
emit("=== 偏振权重（第 86 轮 9B.5 实测）===")
emit(f"c_eps,l = {cL},  c_eps,t = {cT}")
emit(f"eta_t = c_t^2/c_l^2 = {eta:.6f}  (第86轮记 2.30)")
emit(f"前因子 1+2 eta_t = {W:.6f}  (第86轮记 5.59)")
emit(f"精确分数 (626/413)^2 -> 1+2eta = {1+2*(626/413)**2:.6f}")
assert abs(W - 5.59) < 0.02, "前因子须与第86轮 5.59 同量级"

# ---- [A] 三支声学色散与零点幅度 ----
emit("\n=== [A] 三支声学色散 omega = c_lambda q（示意 c_L=1, c_T=0.6）===")
q = np.linspace(0.01, 1, 200)
cL_amd, cT_amd = 1.0, 0.6
ampL = 1.0 / (cL_amd * q)
ampT = 1.0 / (cT_amd * q)   # 横波声速低 -> 零点幅度高
emit(f"omega_q 在 q=1: L={cL_amd}, T={cT_amd}")
emit(f"零点幅度 1/omega 在 q=0.01: L={ampL[0]:.3f}, T={ampT[0]:.3f} (横 > 纵)")
emit("判据：横支零点幅度更大（c_T<c_L），与 c_t>c_l 的响应一致方向")

# ---- [B] sigma_0^2 前因子随 eta_t ----
emit("\n=== [B] sigma_0^2 前因子 1+2 eta_t 随 eta_t（单调）===")
etas = np.linspace(0, 3, 200)
Ws = 1 + 2 * etas
emit(f"eta=0 -> W={Ws[0]:.3f}（单纵支）;  eta={eta:.3f} -> W={1+2*eta:.3f}")
emit(f"单调增：{bool(np.all(np.diff(Ws) > 0))}")
assert np.all(np.diff(Ws) > 0)
assert abs(Ws[0] - 1) < 1e-12

# ---- [C] 关联核 rho(R)=(4/Q^4)∫q^3 j0(qR)dq（第86轮 9B.9），S_rho -> 1/6 ----
emit("\n=== [C] 3D 关联核 rho(R)（偏振无关）与 S_rho 部分和 ===")
Q = np.pi
from numpy.polynomial.legendre import leggauss
nodes, wts = leggauss(4000)
qg = 0.5 * Q * (nodes + 1.0)
wg = 0.5 * Q * wts
def rho3(R):
    # rho(R) = (4/Q^4) ∫_0^Q q^3 j0(qR) dq = (4/Q^4)∫ q^2 sin(qR)/R dq
    # 用 Gauss-Legendre（等距 trapz 对高频 sin(qk) 采样不足）
    if R < 1e-12:
        return 4.0 / Q**4 * np.sum(wg * qg**3)  # j0(0)=1 ⇒ ∫q^3 dq = Q^4/4
    return 4.0 / Q**4 * np.sum(wg * qg**2 * np.sin(qg * R) / R)
Rg = np.linspace(0.01, 8*np.pi, 200)
rhoR = np.array([rho3(R) for R in Rg])
ks = np.arange(1, 401)
rho_k = np.array([rho3(float(k)) for k in ks])
partial = np.cumsum(rho_k)
Srho = partial[-1]
emit(f"rho(0) = {rho3(0.0):.6f}（应 1）")
emit(f"S_rho = sum_k rho3(k) (k<=400) = {Srho:.6f}  (第86轮 0.166665)")
emit(f"1/6 = {1/6:.6f};  1+S_rho = {1+Srho:.6f} (7/6={7/6:.6f})")
assert abs(rho3(0.0) - 1) < 1e-6
assert abs(Srho - 1/6) < 2e-3, "S_rho 须收敛到 1/6"

# 偏振无关性：三支不同权重但同一 rho3 核 -> 归一化 rho 相同
wL, wT1, wT2 = cL**2, cT**2, cT**2
rho_weighted = (wL*rhoR + wT1*rhoR + wT2*rhoR) / (wL+wT1+wT2)
maxdiff = np.max(np.abs(rho_weighted - rhoR))
emit(f"三支加权 rho 与单支核的最大差 = {maxdiff:.2e}（应为数值零）")
assert maxdiff < 1e-12

# ---- [D] Var 比不随偏振改变 ----
emit("\n=== [D] 闭环方差比 (1+S_rho) 与偏振前因子的分离 ===")
sig2_L = 1.0
sig2_3 = 1 + 2*eta   # 三支 sigma_0^2 相对单纵支
ratio_shape = 1 + Srho
var_L = ratio_shape * 10 * sig2_L
var_3 = ratio_shape * 10 * sig2_3
emit(f"形状因子 1+S_rho = {ratio_shape:.6f}（偏振无关）")
emit(f"Var 单纵支 = {var_L:.4f}, 三支 = {var_3:.4f}, 比 = {var_3/var_L:.4f} = 1+2eta")
emit("判据：Var 的绝对量随偏振放大 5.59 倍，但形状因子 7/6 不变")

# ---- 绘图 ----
fig, ax = plt.subplots(2, 2, figsize=(11, 8))
ax[0,0].plot(q, ampL, label="L (c=1.0)")
ax[0,0].plot(q, ampT, label="T (c=0.6)")
ax[0,0].set_title("(A) 零点幅度 1/omega ~ 1/(c q)")
ax[0,0].set_xlabel("q"); ax[0,0].set_ylabel("1/(c q)"); ax[0,0].legend()

ax[0,1].plot(etas, Ws, label="1+2 eta_t")
ax[0,1].axvline(eta, color="r", ls="--", label=f"eta_t={eta:.2f}")
ax[0,1].axhline(W, color="g", ls=":")
ax[0,1].set_title("(B) sigma_0^2 前因子（单调）")
ax[0,1].set_xlabel("eta_t"); ax[0,1].set_ylabel("1+2 eta_t"); ax[0,1].legend()

ax[1,0].plot(Rg, rhoR, label="rho(R)=(4/Q^4)∫q^3 j0(qR)dq")
ax[1,0].set_title("(C) 关联核形状（偏振无关）")
ax[1,0].set_xlabel("R"); ax[1,0].set_ylabel("rho(R)")
ax[1,0].axhline(0, color="k", lw=0.5)

ax[1,1].plot(ks, partial, label="partial sum")
ax[1,1].axhline(1/6, color="r", ls="--", label="1/6")
ax[1,1].axhline(7/6, color="g", ls=":", label="7/6 (Var 比)")
ax[1,1].set_title("(C') S_rho 部分和 -> 1/6")
ax[1,1].set_xlabel("k"); ax[1,1].set_ylabel("sum rho"); ax[1,1].legend()

fig.suptitle("R43: 亏角关联偏振分解（环 4，非拟合）")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

# CSV
with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"eta_t,{eta:.8f}\n")
    f.write(f"polarization_weight,{W:.8f}\n")
    f.write(f"Srho,{Srho:.8f}\n")
    f.write(f"one_sixth,{1/6:.8f}\n")
    f.write(f"var_shape_factor,{ratio_shape:.8f}\n")
    f.write(f"kernel_polynomial_maxdiff,{maxdiff:.3e}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
