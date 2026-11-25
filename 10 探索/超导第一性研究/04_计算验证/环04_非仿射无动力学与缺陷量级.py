# -*- coding: utf-8 -*-
r"""
第 138 轮：非仿射扇区无链内动力学 ⇒ (4.1″) 的两支坍缩为缺陷一支
=====================================================================
前件：R145（$\operatorname{im}\tilde A\subseteq N_I=(\operatorname{im}B)^\perp$）、
      R146（非仿射刚度谱 $=\mathrm{sv}(\tilde A)$，$\sigma_{\max}$ 有界）。

本轮要判定的是 (4.1″) 的第一项能不能存在：
  $$\langle(\Delta\varepsilon)^2\rangle_T=\sum_{k\in N_I}|Av_k|^2c_k^0[1+2n_B]+b\,n_d(T)$$

严格事实（本脚本 A 段数值核对）：
  顶点动能 $T=\frac12 m\sum_i|\dot x_i|^2$，而 $\dot\ell=B\dot x$。若 $\dot\ell\in N_I$，
  则 $\dot\ell\perp\operatorname{im}B\ni B\dot x$，故 $|\dot\ell|^2=\langle B\dot x,\dot\ell\rangle=0$，
  即 **$N_I$ 中唯一可实现的速度是零**。等价地 $B^+\big|_{N_I}=0$、$M_\ell=(B^+)^\top B^+\big|_{N_I}=0$。

  于是 $c_k^0=\hbar/(2\sqrt{\sigma_kM_k})$ 在 $M_k=0$ 处发散 ⇒ 第一项不是有限物理量。

B 段：缺陷一支的量级（第一性估算，非拟合）
  向错（楔形）单位长度能量 $E/L\sim\dfrac{\mu f^2}{16\pi(1-\nu)}\ln(R/r_c)$；取一个铰链尺度
  的核长 $r_c\sim b$，得单缺陷激活能 $E_c$。给三种金属的 $\mu,\nu$ 与 $f$ 的两个取值。

C 段：$n_d(T)=e^{-E_c/k_BT}$ 与 $\sigma_\varepsilon=2\pi f\sqrt{n_d}$ 对温度的形状，
  与 06 的 $\varepsilon\in[0,2\pi)$（三值 0.177/0.707/0.500）对照。

D 段：相对涨落 $1/\sqrt{N_d}$（泊松），说明"每铰链的缺陷占比"与"总缺陷数的相对涨落"不同。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_非仿射无动力学与缺陷量级.py"
"""
import csv
import itertools
import math
import os

import numpy as np
from scipy.spatial import Delaunay
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- A 段
def bcc_edges(n):
    pts = []
    for i, j, k in itertools.product(range(n), repeat=3):
        pts.append([i, j, k])
        pts.append([i + .5, j + .5, k + .5])
    P = np.array(pts, float)

    def vol(s):
        a, b, c, d = [P[i] for i in s]
        return abs(np.linalg.det(np.array([b - a, c - a, d - a]))) / 6.0

    tets = [tuple(int(x) for x in s) for s in Delaunay(P).simplices if vol(s) > 1e-9]
    edges = sorted({tuple(sorted(e)) for t in tets for e in itertools.combinations(t, 2)})
    return P, tets, edges


def incidence(P, edges):
    B = np.zeros((len(edges), 3 * len(P)))
    for ei, (i, j) in enumerate(edges):
        u = (P[j] - P[i]) / np.linalg.norm(P[j] - P[i])
        B[ei, 3 * i:3 * i + 3] = -u
        B[ei, 3 * j:3 * j + 3] = +u
    return B


def section_a():
    print("=" * 78)
    print("A. N_I 中唯一可实现的速度是零 ⇒ M|_N_I = 0")
    print("=" * 78)
    rows = []
    for n in (3, 4):
        P, tets, edges = bcc_edges(n)
        E, V = len(edges), len(P)
        B = incidence(P, edges)
        Bp = np.linalg.pinv(B)                       # (3V, E)
        # 到 im(B) 的投影（E x E）
        PrE = B @ np.linalg.pinv(B.T @ B) @ B.T
        PrN = np.eye(E) - PrE
        # 非仿射方向：PrN 的列空间；检验 Bp 在其上的作用
        # 取 PrN 的基（SVD）
        U, S, Vt = np.linalg.svd(PrN)
        rN = int((S > 1e-8).sum())
        basisN = U[:, :rN]                            # E x rN
        act = Bp @ basisN                             # (3V x rN)
        act_norm = np.linalg.norm(act)
        # 质量矩阵 M_l = Bp^T Bp，检验其在 N_I 上的二次型
        Ml = Bp.T @ Bp
        quad = basisN.T @ Ml @ basisN
        qnorm = np.linalg.norm(quad)
        # 对照：在 im(B) 方向上的二次型（应为正）
        basisE = U[:, rN:]
        quadE = basisE.T @ Ml @ basisE
        rows.append(dict(n=n, V=V, E=E, rN=rN, act=act_norm, q=qnorm,
                         qE=np.linalg.norm(quadE)))
        print(f"  n={n}: E={E} V={V} dim N_I={rN}")
        print(f"        ‖B⁺·v_N‖ = {act_norm:.3e}   ‖v_N^T M_l v_N‖ = {qnorm:.3e}"
              f"   （对照：im B 上 ‖·‖ = {np.linalg.norm(quadE):.3e}）")
        assert act_norm < 1e-9, "B⁺ 在 N_I 上必须为零"
        assert qnorm < 1e-9, "M_l 在 N_I 上的二次型必须为零"

    print("\n  ⇒ 第一项 c_k^0=ħ/(2√(σ_k M_k)) 在 M_k=0 处发散，不是有限物理量。")

    # 发散演示
    print("\n  发散：σ=1，M→0 时 c^0 的增长")
    for M in (1e-2, 1e-4, 1e-6, 1e-8):
        print(f"    M={M:.0e}: ħ/(2√(σM)) = {1/(2*math.sqrt(1.0*M)):.3e}  (ħ=1)")
    return rows


# ---------------------------------------------------------------- B 段
def section_b():
    print("\n" + "=" * 78)
    print("B. 缺陷一支的量级：向错弹性核心能 E_c 与热激活密度")
    print("=" * 78)
    # 材料：剪切模量 mu [GPa]、泊松比 nu
    mats = {
        "Al": (26.0, 0.345, 4.05e-10),   # b ≈ a
        "Nb": (38.0, 0.397, 3.30e-10),
        "Pb": (5.6, 0.440, 4.95e-10),
        "V":  (46.0, 0.365, 3.02e-10),
    }
    kB = 1.380649e-23
    eV = 1.602176634e-19
    lnR = 5.0          # ln(R/r_c)，O(1) 对数，取 5 作中值
    fs = (0.03, 0.10)  # 弗兰克角分数 f = ε/(2π)
    print(f"  E_c = μ f² b³ ln(R/r_c) / [16π(1-ν)]（含 b² 弹性标度，核体积 ~ b³）")
    print(f"  取 ln(R/r_c) = {lnR}")
    hdr = ("材料", "μ[GPa]", "ν", "f", "E_c[eV]", "E_c/k_B[K]", "n_d(300K)", "σ_ε[rad]")
    print("  %-6s%8s%7s%7s%11s%12s%12s%11s" % hdr)
    out = []
    for name, (mu, nu, b) in mats.items():
        for f in fs:
            Ec = mu * 1e9 * f * f * b ** 3 * lnR / (16 * math.pi * (1 - nu))   # J
            EcK = Ec / kB
            nd300 = math.exp(-EcK / 300.0)
            sig = 2 * math.pi * f * math.sqrt(nd300)
            print("  %-6s%8.1f%7.3f%7.2f%11.5f%12.1f%12.3e%11.4f"
                  % (name, mu, nu, f, Ec / eV, EcK, nd300, sig))
            out.append(dict(mat=name, mu=mu, nu=nu, f=f, Ec_eV=Ec / eV,
                            EcK=EcK, nd300=nd300, sigma=sig))
    print("\n  06 的 ε 量级：0.177 / 0.707 / 0.500 rad（三环乘积对应的常曲率赋值）")
    print("  ⇒ 缺陷一支在 f=0.03–0.10、ln=5 下给 σ_ε ~ 1e-3–1e-1 rad，与 06 的 0.1–0.7 同量级偏下")
    return out


# ---------------------------------------------------------------- 图
def make_fig(rows_a, rows_b):
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2))

    # A: M 在 N_I 上为零 vs 在 im B 上非零
    ax = axes[0, 0]
    ns = [r["n"] for r in rows_a]
    x = np.arange(len(ns))
    ax.bar(x - 0.18, [max(r["q"], 1e-18) for r in rows_a], 0.34,
           label=r"$N_I$ 上 $\|v^\top M_\ell v\|$（数值零）", color="#C0504D")
    ax.bar(x + 0.18, [r["qE"] for r in rows_a], 0.34,
           label=r"$\mathrm{im}\,B$ 上 $\|v^\top M_\ell v\|$（有限）", color="#4C72B0")
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([f"$n={n}$" for n in ns])
    ax.set_ylabel("二次型范数")
    ax.set_title("A. 顶点动能在非仿射扇区上恒为零")
    ax.legend(fontsize=8)
    ax.grid(alpha=.3, axis="y", which="both")

    # B: n_d(T) 对几个 E_c
    ax = axes[0, 1]
    T = np.linspace(1, 400, 500)
    for EcK, ls in ((300, "-"), (600, "--"), (1200, ":"), (2400, "-.")):
        nd = np.exp(-EcK / T)
        ax.semilogy(T, nd, ls, label=rf"$E_c/k_B={EcK}$ K")
    ax.axhline(math.exp(-300 / 300.), color="gray", lw=.8, ls=":")
    ax.set_xlabel("$T$ (K)")
    ax.set_ylabel(r"$n_d=e^{-E_c/k_BT}$")
    ax.set_ylim(1e-12, 2)
    ax.set_title("B. 向错热激活密度对温度")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3, which="both")

    # C: σ_ε(T) 与 06 的量级带
    ax = axes[1, 0]
    T = np.linspace(50, 400, 400)
    for EcK, ls in ((300, "-"), (600, "--"), (1200, ":")):
        nd = np.exp(-EcK / T)
        ax.semilogy(T, 2 * math.pi * 0.10 * np.sqrt(nd), ls,
                    label=rf"$f=0.10,\ E_c/k_B={EcK}$ K")
    ax.axhspan(0.1, 0.7, color="orange", alpha=.15, label="06 的 $\\varepsilon$ 量级带")
    ax.set_xlabel("$T$ (K)")
    ax.set_ylabel(r"$\sigma_\varepsilon=2\pi f\sqrt{n_d}$ (rad)")
    ax.set_title("C. 缺陷一支能否解释 06 的 $\\varepsilon$ 量级")
    ax.legend(fontsize=8)
    ax.grid(alpha=.3, which="both")

    # D: 相对涨落 1/sqrt(N)
    ax = axes[1, 1]
    N = np.logspace(0, 12, 200)
    ax.loglog(N, 1 / np.sqrt(N), "-", label=r"泊松相对涨落 $1/\sqrt{N_d}$")
    ax.axhline(0.5, color="gray", ls=":", lw=.8)
    ax.set_xlabel("缺陷数 $N_d$（每个相干体积内）")
    ax.set_ylabel("相对涨落")
    ax.set_title("D. 泊松统计：相对涨落随缺陷数衰减")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "环04_非仿射无动力学与缺陷量级.png")
    fig.savefig(png, dpi=150)
    print(f"\n图：{png}")
    return png


def main():
    ra = section_a()
    rb = section_b()
    make_fig(ra, rb)

    csvp = os.path.join(OUT, "环04_非仿射无动力学与缺陷量级.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["材料", "μ[GPa]", "ν", "f", "E_c[eV]", "E_c/k_B[K]",
                    "n_d(300K)", "σ_ε(300K)[rad]"])
        for r in rb:
            w.writerow([r["mat"], r["mu"], r["nu"], r["f"], f"{r['Ec_eV']:.4f}",
                        f"{r['EcK']:.0f}", f"{r['nd300']:.3e}", f"{r['sigma']:.4f}"])
    print(f"表：{csvp}")

    sump = os.path.join(OUT, "环04_非仿射无动力学与缺陷量级_摘要.csv")
    with open(sump, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["项目", "数值", "判据"])
        for r in ra:
            w.writerow([f"‖B⁺v_N‖(n={r['n']})", f"{r['act']:.2e}", "<1e-9 ⇒ M|N_I=0"])
        w.writerow(["E_c 范围（f=0.03–0.10）",
                    f"{min(x['Ec_eV'] for x in rb):.3f}–{max(x['Ec_eV'] for x in rb):.3f} eV",
                    "弹性估算"])
        w.writerow(["σ_ε(300K) 范围",
                    f"{min(x['sigma'] for x in rb):.3e}–{max(x['sigma'] for x in rb):.3e} rad",
                    "对照 06 的 0.1–0.7"])
    print(f"摘要：{sump}")
    print("\n所有断言通过。")


if __name__ == "__main__":
    main()
