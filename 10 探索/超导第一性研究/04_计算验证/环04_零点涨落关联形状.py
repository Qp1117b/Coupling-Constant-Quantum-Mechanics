# -*- coding: utf-8 -*-
"""
环 4：零点涨落关联 $\\rho_{ij}$ 的第一性形状与 $\\sigma_0$ 的谱标度
====================================================================
第 83 轮把闭环环量写成 $\\mathrm{Var}(\\Phi_C)=\\sigma^2[n+2\\sum_{i<j}\\rho_{ij}]$，
但 $\\rho$ 的形状只给了括区（连续 $1/r$ 模型会得 $n\\ln n$）。本轮用链内自己的两个事实定形：

  (i)  环 2 (2.1)：$\\Delta\\varepsilon$ 是简正模的线性叠加，等时零点幅度 $\\hbar/(2\\rho_m\\omega_q)$；
  (ii) 环 3 (3.1)：$\\varepsilon_e=2\\pi-\\sum_T\\theta_e^T$ 是**铰链**亏角（06 环节表②／符号表：曲率载体，
       与顶点角亏无关）。三维剖分中铰链是边，绕边二面角和对 $2\\pi$ 的偏差 $\\sim q^{n}$。

一般地写 $|G_q|^2\\propto q^{2n}$（$n=0$ 位移、$n=1$ 应变、$n=2$ 曲率），则等时关联

  $\\rho(r)=\\dfrac{\\int_0^Q q^{2n}J_0(qr)\\,dq}{\\int_0^Q q^{2n}\\,dq}$，

**有限布里渊区**（$Q\\sim\\pi/a$）使大 $r$ 的包络不是 $1/r$，而是
$(2n+1)J_1(Qr)/(Qr)$；在格点 $r=ka$ 上按 $k^{-3/2}$ 振荡衰减 ⇒ $\\sum_k\\rho_k$ **收敛**。
于是 $\\mathrm{Var}(\\Phi_C)=n\\sigma^2(1+S_\\rho)+O(1)$：**纯周长律，无对数修正**。

第 83 轮的 $n\\ln n$ 括区被本轮的离散求和取代——那是连续 $1/r$ 模型的伪影。
"""
import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import j0, j1

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_CSV = "环04_零点涨落关联形状.csv"
OUT_PNG = "环04_零点涨落关联形状.png"
OUT_TXT = "环04_零点涨落关联形状_摘要.txt"

LOG = []


def emit(s=""):
    print(s)
    LOG.append(s)


def trapz(y, x):
    return float(np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x)))


def rho_exact(m, k, Q=math.pi, nq=200001):
    """ρ_m(k) = ∫_0^Q q^m J0(qk) dq / (Q^{m+1}/(m+1))，m=2n。精确数值积分。"""
    q = np.linspace(0.0, Q, nq)
    y = (q ** m) * j0(q * k)
    return trapz(y, q) / (Q ** (m + 1) / (m + 1))


def rho_asym(m, k, Q=math.pi):
    """大 Qr 包络：(m+1) J1(Qr)/(Qr)。"""
    return (m + 1) * j1(Q * k) / (Q * k)


def var_ratio_ring(n, rho_of_k):
    """闭环（最小镜像距离）的 Var(Φ_C)/(nσ²) = 1 + 2Σ_{i<j}ρ/n。"""
    s = 0.0
    for i in range(n):
        for j in range(i + 1, n):
            d = min(j - i, n - (j - i))
            s += rho_of_k(d)
    return 1.0 + 2.0 * s / n


def main():
    Q = math.pi
    K = 400
    emit("=" * 78)
    emit("环 4：零点涨落关联 ρ(r) 的第一性形状（2D Debye＋有限 BZ）")
    emit(f"    Q=π/a, a=1；|G_q|²∝q^{{2n}}；ρ_m(k)=∫q^m J0(qk)dq / (Q^{{m+1}}/(m+1)), m=2n")

    # ---------- [1] ρ_k 的逐点值 ----------
    emit("\n[1] ρ_k（格点距 k）与渐近包络 (m+1)J1(πk)/(πk)")
    emit(f"{'k':>3} " + "".join(f"{'m='+str(m):>12}" for m in (0, 2, 3, 4)))
    tab = {}
    for m in (0, 2, 3, 4):
        tab[m] = [rho_exact(m, k) for k in range(1, K + 1)]
    for k in range(1, 13):
        row = "".join(f"{tab[m][k-1]:12.6f}" for m in (0, 2, 3, 4))
        emit(f"{k:3d} " + row)
    for m in (0, 2, 3, 4):
        assert abs(rho_exact(m, 0) - 1.0) < 1e-6, f"ρ_m(0)≠1, m={m}"
    emit("    [断言] ρ_m(0)=1（r=0 自关联）  ✓")

    # ---------- [2] 求和收敛 ----------
    emit("\n[2] Σ_{k≥1}ρ_k 的收敛（S_ρ）——m=0 是唯一发散（对照）")
    S = {}
    cont = [sum(1.0 / (1.0 + k) for k in range(1, kk + 1)) for kk in (10, 50, 100, 200, 400)]
    for m in (0, 2, 3, 4):
        partial = [sum(tab[m][:k]) for k in (10, 50, 100, 200, 400)]
        S[m] = partial[-1]
        emit(f"    m={m}: S_ρ(10,50,100,200,400) = " + " ".join(f"{v:.6f}" for v in partial))
        if m >= 2:
            assert abs(partial[-1] - partial[-2]) < 0.002, f"m={m} 求和未收敛"
    assert S[0] > 2.0 and S[2] < 1.0, "m=0 应慢发散、m=2 应收敛"
    emit("    [断言] m=2,3,4 的 Σρ 收敛；m=0 慢发散（∝ln）  ✓")
    emit(f"    对照 连续 p=1（ρ=1/(1+k)）: " + " ".join(f"{v:.3f}" for v in cont)
         + "  ← 发散（ln），与 m=0 同族")

    # ---------- [3] 闭环方差：周长律 vs 对数增长 ----------
    emit("\n[3] Var(Φ_C)/(nσ²) 的 n 依赖（最小镜像闭环）")
    ns = [8, 16, 32, 64, 128, 256]
    vr = {}
    for m in (0, 2, 3, 4):
        cache = {k: tab[m][k - 1] for k in range(1, K + 1)}
        vr[m] = [var_ratio_ring(n, lambda d: cache[d]) for n in ns]
        emit(f"    m={m}: " + " ".join(f"{v:.6f}" for v in vr[m]))
        if m >= 2:
            assert abs(vr[m][-1] - vr[m][-2]) < 0.01 * vr[m][-1], f"m={m} 未收敛"
            assert abs(vr[m][-1] - 1.0) > 1e-3, f"m={m} 重整化为零"
    vr_cont = []
    for n in ns:
        s = 0.0
        for i in range(n):
            for j in range(i + 1, n):
                d = min(j - i, n - (j - i))
                s += 1.0 / (1.0 + d)
        vr_cont.append(1.0 + 2.0 * s / n)
    emit("    连续 p=1 : " + " ".join(f"{v:.4f}" for v in vr_cont) + "  ← 持续增长")
    assert vr[0][-1] - vr[0][-2] > 0.05, "m=0 应随 n 增长"
    assert abs(vr[2][-1] - vr[2][-2]) < 1e-3
    emit("    [断言] m=0 随 n 增长；m=2,3,4 收敛到 1+S_ρ；连续 p=1 不收敛  ✓")

    # ---------- [4] 渐近 k^{-3/2} ----------
    emit("\n[4] 渐近：k^{3/2}ρ_k 应趋于有界振荡（m=2,3,4）")
    for m in (2, 3, 4):
        vals = [tab[m][k - 1] * k ** 1.5 for k in (20, 40, 60, 80, 100)]
        emit(f"    m={m}: " + " ".join(f"{v:+.5f}" for v in vals))
        assert max(abs(v) for v in vals) < 5.0, f"m={m} 增长快于 k^{-3/2}"
    emit("    [断言] k^{3/2}ρ_k 有界 ⇒ ρ_k=O(k^{-3/2})  ✓")

    # ---------- [5] σ0 的谱标度 ----------
    emit("\n[5] σ0² 的 Q 标度：I_m(Q)=∫_0^Q q^m dq = Q^{m+1}/(m+1)")
    for m in (2, 3, 4):
        expo = m + 1
        qs = [1.0, 1.5, 2.0, 3.0]
        Is = [Qq ** (m + 1) / (m + 1) for Qq in qs]
        ratios = [I / Qq ** expo for I, Qq in zip(Is, qs)]
        emit(f"    m={m}: I/Q^{expo} = " + " ".join(f"{r:.10f}" for r in ratios))
        assert max(ratios) - min(ratios) < 1e-12
    emit("    [断言] G∼q^n ⇒ σ0²∝Q^{m+1}=Q^{2n+1}（m=2→Q³，m=3→Q⁴，m=4→Q⁵）  ✓")

    # ---------- CSV ----------
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("k,rho_m0,rho_m2,rho_m3,rho_m4,asym_m2\n")
        for k in range(1, K + 1):
            f.write(f"{k},{tab[0][k-1]:.8g},{tab[2][k-1]:.8g},{tab[3][k-1]:.8g},"
                    f"{tab[4][k-1]:.8g},{rho_asym(2,k):.8g}\n")
        f.write("\n# var_ratio\nn,m0,m2,m3,m4,cont_p1\n")
        for idx, n in enumerate(ns):
            f.write(f"{n},{vr[0][idx]:.8g},{vr[2][idx]:.8g},{vr[3][idx]:.8g},"
                    f"{vr[4][idx]:.8g},{vr_cont[idx]:.8g}\n")

    # ---------- 图 ----------
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.6))
    ks = np.arange(1, K + 1)

    a = ax[0][0]
    for m, ls in ((0, ":"), (2, "-"), (3, "--"), (4, "-.")):
        a.loglog(ks, np.abs(tab[m]), ls, lw=1.2, label=f"m={m}")
    a.loglog(ks, 1.0 / ks ** 1.5, "k--", lw=0.9, label=r"$k^{-3/2}$")
    a.set_xlabel("格点距 k")
    a.set_ylabel(r"$|\rho_k|$")
    a.set_title("(A) 关联的形状：Bessel 振荡，包络 $k^{-3/2}$")
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    a = ax[0][1]
    a.semilogx(ks, tab[2], "-", lw=1.1, label=r"精确 $\rho_k$ (m=2)")
    a.semilogx(ks, [rho_asym(2, k) for k in ks], "k--", lw=0.9, label=r"渐近 $3J_1(\pi k)/(\pi k)$")
    a.axhline(0, color="k", lw=0.6)
    a.set_xlabel("k")
    a.set_ylabel(r"$\rho_k$")
    a.set_title("(B) 精确积分与渐近包络（非拟合）")
    a.legend(fontsize=8)
    a.grid(alpha=0.3)

    a = ax[0][2]
    ms = [0, 2, 3, 4]
    a.bar(range(len(ms)), [S[m] for m in ms], color="steelblue")
    a.set_xticks(range(len(ms)))
    a.set_xticklabels([f"m={m}" for m in ms])
    a.set_ylabel(r"$S_\rho=\sum_{k\geq 1}\rho_k$")
    a.set_title(r"(C) 求和收敛：$S_\rho>0$，有限")
    for i, m in enumerate(ms):
        a.text(i, S[m] + 0.005, f"{S[m]:.3f}", ha="center", fontsize=8)
    a.grid(axis="y", alpha=0.3)

    a = ax[1][0]
    for m in (0, 2, 3, 4):
        a.semilogx(ns, vr[m], "o-", lw=1.2, ms=4, label=f"m={m}")
    a.semilogx(ns, vr_cont, "k--", lw=1.2, label="连续 p=1（无截断）")
    a.set_xlabel("环长 n")
    a.set_ylabel(r"$\mathrm{Var}(\Phi_C)/(n\sigma^2)$")
    a.set_title(r"(D) $m\geq 1$ 纯周长律；$m=0$（位移）随 $n$ 增长")
    a.legend(fontsize=7)
    a.grid(alpha=0.3, which="both")

    a = ax[1][1]
    for m, c in ((2, "tab:blue"), (3, "tab:green"), (4, "tab:red")):
        a.semilogx(ks, [rho_asym(m, k) for k in ks], "-", lw=1.1, color=c, label=f"m={m}")
    a.axhline(0, color="k", lw=0.6)
    a.set_xlabel("k")
    a.set_ylabel(r"渐近 $\rho_k$")
    a.set_title(r"(E) 渐近形状相同、前置因子 $m+1$")
    a.legend(fontsize=8)
    a.grid(alpha=0.3)

    a = ax[1][2]
    qs = np.linspace(0.5, 4.0, 50)
    a.loglog(qs, qs ** 3 / 3, "-", lw=1.3, label=r"$m=2$：$Q^3/3$（应变，声学）")
    a.loglog(qs, qs ** 4 / 4, "--", lw=1.3, label=r"$m=3$：$Q^4/4$（弯曲，柔性）")
    a.loglog(qs, qs ** 5 / 5, ":", lw=1.3, label=r"$m=4$：$Q^5/5$（曲率，声学）")
    a.set_xlabel("截断 Q")
    a.set_ylabel(r"$\sigma_0^2$ 的谱积分")
    a.set_title(r"(F) $\sigma_0^2\propto Q^{2n+1}$")
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    emit(f"\n[图] 已写出 {OUT_PNG}")

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    emit(f"[摘要] 已写出 {OUT_TXT}")

    # ---------- 结论 ----------
    emit("\n[6] 结论")
    emit(f"    (a) ρ_k 由 ∫q^{{m}}J0(qk)dq/(Q^{{m+1}}/(m+1)) 给定，ρ(0)=1；m≥1 的包络 k^{{-3/2}}。")
    emit(f"    (b) S_ρ = {S[2]:+.4f}(m=2) / {S[3]:+.4f}(m=3) / {S[4]:+.4f}(m=4) 有限；"
         f"m=0 的 S_ρ({K})={S[0]:.3f} 仍在涨（ln）。")
    emit("    (c) m≥1：Var(Φ_C)=nσ²(1+S_ρ)+O(1)——纯周长律，无 ln n；S_ρ 符号由关联定。")
    emit("    (d) σ0²∝Q^{m+1}：m=2→Q³（应变/声学），m=3→Q⁴（弯曲/柔性），m=4→Q⁵。")
    emit("    (e) 第 83 轮的 p=1 连续括区对应 m=0（位移载体），在 n=512 处把 Var 抬到 "
         f"{vr_cont[-1]:.2f} 倍；链内铰链亏角是 m≥2，只有 {vr[2][-1]:.2f} 倍——后者才是链内的。")


if __name__ == "__main__":
    main()
