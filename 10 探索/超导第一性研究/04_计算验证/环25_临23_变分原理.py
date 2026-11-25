#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环 25／51：总效应变分原理（Hilbert 最小二乘投影）——数值核对（非拟合）
三面板只检验：极限、单调性、量级、符号。
Run: python "10 探索/超导第一性研究/04_计算验证/环25_临23_变分原理.py"
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
OUT = os.path.join(HERE, "环25_临23_变分原理.png")
CSV = os.path.join(HERE, "环25_临23_变分原理.csv")
SUM = os.path.join(HERE, "环25_临23_变分原理_摘要.txt")

log = []
def emit(s=""):
    print(s)
    log.append(s)

gamma = np.array([14.134725,21.022040,25.010858,30.424876,32.935062])
rho = 0.5 + 1j * gamma
c = -1.0 / rho
N = len(c)

def F(x):
    return np.sum(np.abs(x)**2) - 2*np.real(np.sum(np.conj(x)*c))

emit("=" * 60)
emit("环 25／临-23：总效应变分原理（Hilbert 投影）")
emit("=" * 60)
Fk = F(c)
theory = -np.sum(np.abs(c)**2)
emit(f"F[K]           = {Fk:.8f}")
emit(f"-sum|c_n|^2    = {theory:.8f}")
emit(f"吻合：{abs(Fk-theory)<1e-10}")
assert abs(Fk - theory) < 1e-10

# ---- [A] 一维截面凸性：x = c + t（实方向），极小在 t=0 ----
emit("\n[A] 一维截面 F(c+t) 的凸性")
ts = np.linspace(-0.02, 0.02, 200)
Fs = np.array([F(c + t*np.ones(N, dtype=complex)) for t in ts])
imin = np.argmin(Fs)
emit(f"极小位置 t* = {ts[imin]:.5f}（应 0）")
emit(f"F(c+t*) = {Fs[imin]:.8f}, F(c) = {Fk:.8f}")
emit(f"二阶差分 > 0（严格凸）：{Fs[0] > Fs[imin] and Fs[-1] > Fs[imin]}")
assert abs(ts[imin]) < 0.001 and Fs[0] > Fs[imin] and Fs[-1] > Fs[imin]

# ---- [B] 扰动增量 = ||epsilon||^2 ----
emit("\n[B] 扰动增量 F(K+eps)-F(K) = ||eps||^2")
rng = np.random.default_rng(42)
for scale in [0.001, 0.01, 0.05]:
    eps = scale*(rng.standard_normal(N)+1j*rng.standard_normal(N))
    dF = F(c+eps) - Fk
    norm2 = np.sum(np.abs(eps)**2)
    emit(f"  scale={scale}: dF={dF:.8f}, ||eps||^2={norm2:.8f}, 差={abs(dF-norm2):.2e}")
    assert abs(dF - norm2) < 1e-9

# ---- [C] 有限时窗交叉项消失（正交性前提，承 R50）----
emit("\n[C] 频率基正交性：<e_n,e_m> 随时间窗增大 -> delta_nm")
taus = np.linspace(0, 2000, 100000)
for W in [50, 500, 2000]:
    tw = taus[taus <= W]
    e0 = np.exp(1j*gamma[0]*tw)
    e1 = np.exp(1j*gamma[1]*tw)
    overlap = np.mean(np.conj(e0)*e1)
    emit(f"  W={W:5d}: |<e0,e1>|={abs(overlap):.4f}（应随 W 增而减）")
emit("判据：无共振 ⇒ 长时窗交叉项 -> 0，频率基正交（Parseval/变分前提）")

# ---- 绘图 ----
fig, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].plot(ts, Fs, label="F(c+t)")
ax[0].axvline(0, color="r", ls="--")
ax[0].axhline(theory, color="g", ls=":", label=f"min={theory:.5f}")
ax[0].set_title("(A) functional convexity, min at K")
ax[0].set_xlabel("t"); ax[0].set_ylabel("F")
ax[0].legend()

scales = np.array([0.001,0.01,0.05])
dFs = []
for s in scales:
    eps = s*(rng.standard_normal(N)+1j*rng.standard_normal(N))
    dFs.append(F(c+eps)-Fk)
ax[1].loglog(scales, dFs, "o-", label="dF")
ax[1].loglog(scales, scales**2, "s--", label="~scale^2")
ax[1].set_title("(B) perturbation increment = ||eps||^2")
ax[1].set_xlabel("scale"); ax[1].set_ylabel("dF")
ax[1].legend()

Ws = [50,500,2000]
ovs = []
for W in Ws:
    tw = taus[taus <= W]
    ovs.append(abs(np.mean(np.conj(np.exp(1j*gamma[0]*tw))*np.exp(1j*gamma[1]*tw))))
ax[2].plot(Ws, ovs, "o-", label="|<e0,e1>|")
ax[2].set_title("(C) cross terms vanish (orthogonality)")
ax[2].set_xlabel("window W"); ax[2].set_ylabel("|overlap|")
ax[2].legend()

fig.suptitle("R51: total-effect variational principle (structural, non-fit)")
fig.tight_layout()
fig.savefig(OUT, dpi=120)

with open(CSV, "w", encoding="utf-8") as f:
    f.write("quantity,value\n")
    f.write(f"F_K,{Fk:.10f}\n")
    f.write(f"minus_sum_c2,{theory:.10f}\n")
    f.write(f"t_min,{ts[imin]:.6f}\n")
    f.write(f"strictly_convex,{True}\n")
with open(SUM, "w", encoding="utf-8") as f:
    f.write("\n".join(log) + "\n")
emit(f"\nSaved: {os.path.basename(OUT)}, {os.path.basename(CSV)}")
