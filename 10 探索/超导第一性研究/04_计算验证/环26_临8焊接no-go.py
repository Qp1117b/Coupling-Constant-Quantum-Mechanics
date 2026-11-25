# -*- coding: utf-8 -*-
"""
环 26／`临-8` 焊接 no-go 的数值核对。

1. 逐模滤波器 W_n(t)=exp(-Γ_n t)，Γ_n=γ_n² σ_v²τ_g；
2. 物理逐模率 α+Γ_n vs ζ 形式的统一率 1/2；
3. 截断实核 K_N(t)=-Σ[cos(γt)+2γ sin(γt)]/(1/4+γ²) 的振荡；
4. no-go 区域：(σ_v²τ_g, |Δγ²|) 平面只有两轴可对齐。

零点纵坐标取外部已引数值（文献基线 L14–L16 的数值来源页），
只作示意；定理只用 γ_n²≠γ_m²，不依赖具体数值。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环26_临8焊接no-go.png")
OUT_CSV = os.path.join(HERE, "环26_临8焊接no-go.csv")

# 前三个非平凡零点纵坐标（外部数值，仅示意）
GAMMAS = np.array([14.134725141, 21.022039639, 25.010857580])
SVTAU = 1.0e-3          # σ_v² τ_g 的示意值（>0 即可触发 no-go）
ALPHA = 0.5             # 取理想时钟率，仍因 Γ_n 不同而无法对齐


def real_mode_kernel(t, gam):
    """共轭零点对给的实时核贡献：-[cos(γt)+2γ sin(γt)]/(1/4+γ²)。"""
    t = np.asarray(t, dtype=float)
    return -(np.cos(gam * t) + 2.0 * gam * np.sin(gam * t)) / (0.25 + gam ** 2)


def main():
    rows = []
    gs = GAMMAS ** 2 * SVTAU
    print("零点 gamma_n   Gamma_n=gamma_n^2*svtg  物理率 alpha+Gamma_n")
    for g, G in zip(GAMMAS, gs):
        print(f"  {g:12.9f}   {G:10.6f}        {ALPHA + G:10.6f}")
        rows.append(("damping", g, float(G), ALPHA + float(G), 0.5))

    # ---- 截断实核在 t=0 的值（仅前三模；全零点按链约定为 -1）
    t0 = np.array([0.0])
    K3_0 = sum(real_mode_kernel(t0, g)[0] for g in GAMMAS)
    print(f"\n截断前三模 K_3(0) = {K3_0:.6f}（全零点和按链约定为 -1）")
    rows.append(("K3_zero", 0.0, K3_0, -1.0, np.nan))

    # ---- 两两 gamma^2 差
    print("\n两两 |Delta gamma^2|：")
    for i in range(len(GAMMAS)):
        for j in range(i + 1, len(GAMMAS)):
            d = abs(GAMMAS[i] ** 2 - GAMMAS[j] ** 2)
            print(f"  gamma{i+1}^2 - gamma{j+1}^2: {d:.4f}")
            rows.append((f"gamma_sq_diff_{i+1}_{j+1}", d, SVTAU * d, np.nan, np.nan))

    # ---- 保存 CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.2))

    # A 滤波器
    tt = np.linspace(0, 8, 600)
    for i, (g, G) in enumerate(zip(GAMMAS, gs)):
        ax[0, 0].plot(tt, np.exp(-G * tt), lw=2.0,
                      label=rf"$n={i+1}:\ \Gamma_n={G:.3f}$")
    ax[0, 0].axhline(1.0, color="0.35", ls=":", lw=1.2, label=r"$\zeta$ 形式：$W=1$")
    ax[0, 0].set_xlabel(r"$t$")
    ax[0, 0].set_ylabel(r"$W_n(t)=e^{-\Gamma_n t}$")
    ax[0, 0].set_title("A  逐模滤波器：三条不同衰减")
    ax[0, 0].set_ylim(0.0, 1.08)
    ax[0, 0].legend(fontsize=8, loc="upper right")
    ax[0, 0].grid(alpha=0.3)

    # B 逐模率
    tt2 = np.linspace(0, 8, 200)
    for i, (g, G) in enumerate(zip(GAMMAS, gs)):
        ax[0, 1].plot(tt2, np.full_like(tt2, ALPHA + G), lw=2.2,
                      label=rf"$\alpha+\Gamma_{i+1}={ALPHA+G:.3f}$")
    ax[0, 1].axhline(0.5, color="tab:red", ls="--", lw=2.0,
                     label=r"$\zeta$ 统一率 $1/2$")
    ax[0, 1].set_xlabel(r"$t$")
    ax[0, 1].set_ylabel("衰减率")
    ax[0, 1].set_title(r"B  物理率逐模不同，$\zeta$ 率模无关")
    ax[0, 1].set_ylim(0.35, 1.25)
    ax[0, 1].legend(fontsize=8, loc="center right")
    ax[0, 1].grid(alpha=0.3)

    # C 截断实核
    tc = np.linspace(0, 1.5, 3000)
    K3 = sum(real_mode_kernel(tc, g) for g in GAMMAS)
    ax[1, 0].plot(tc, K3, lw=1.8, color="tab:blue", label=r"前三模 $K_3(t)$")
    ax[1, 0].axhline(0.0, color="0.35", lw=0.9)
    ax[1, 0].set_xlabel(r"$t=\ln x$")
    ax[1, 0].set_ylabel(r"$K_3(t)$")
    ax[1, 0].set_title(r"C  截断核振荡（变号 => 非正定型形状）")
    ax[1, 0].legend(fontsize=9)
    ax[1, 0].grid(alpha=0.3)

    # D no-go 区域
    svals = np.logspace(-6, 0, 400)
    dvals = np.logspace(0, 4, 400)
    S, D = np.meshgrid(svals, dvals)
    prod = S * D
    ax[1, 1].contourf(np.log10(S), np.log10(D), np.log10(prod), levels=30, cmap="Reds")
    ax[1, 1].contour(np.log10(S), np.log10(D), np.log10(prod),
                     levels=[np.log10(1e-3)], colors="black", linewidths=1.2)
    for i in range(len(GAMMAS)):
        for j in range(i + 1, len(GAMMAS)):
            d = abs(GAMMAS[i] ** 2 - GAMMAS[j] ** 2)
            ax[1, 1].plot(np.log10(SVTAU), np.log10(d), "o", color="tab:blue", ms=7)
    ax[1, 1].text(-5.7, 3.2, r"可对齐仅两轴：$\sigma_v^2\tau_g=0$ 或 $\Delta\gamma^2=0$",
                  fontsize=9, color="white",
                  bbox=dict(facecolor="black", alpha=0.45, edgecolor="none"))
    ax[1, 1].set_xlabel(r"$\log_{10}(\sigma_v^2\tau_g)$")
    ax[1, 1].set_ylabel(r"$\log_{10}|\Delta\gamma^2|$")
    ax[1, 1].set_title(r"D  $(\gamma_n^2-\gamma_m^2)\sigma_v^2\tau_g\ne0$ 全禁")
    ax[1, 1].grid(alpha=0.25)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("\nsaved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
