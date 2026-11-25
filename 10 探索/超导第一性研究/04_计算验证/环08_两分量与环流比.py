# -*- coding: utf-8 -*-
"""
Ring 8 / ring 9 / Shen-19: two-component deficit split and the circulation ratio.

Chain inputs:
  DM.4 / DM.5 : dC_ij = kappa_f * (d eps_i - d eps_j)   (pure node difference — one limit)
  (3.1)       : eps_e = 2 pi - sum_T theta_e^T          (Regge, per-bond)
  Keating     : U = (3a/16r0^2) sum (r^2-r0^2)^2 + (3b/8r0^2) sum (r_ij.r_ik + r0^2/3)^2
                => bond-stretching (alpha, bond-specific) + bond-bending (beta, node-local)
  c11 = (alpha+3 beta)/a,  c12 = (alpha - beta)/a

Two-component split (8B.4):
  d ell_ij = beta_u (d eps_i - d eps_j) + alpha_u d b_ij
Variance (8B.5):
  <(dC)^2> = kappa_f^2 [ beta_u^2 * 2 s_eps^2 (1-rho_ij) + alpha_u^2 s_b^2 ]
Circulation ratio (8B.6):
  r_circ = alpha_u s_b / (beta_u s_eps sqrt(2(1-rho)))
Zero-point scaling (8B.7): s_b^2 ~ 1/alpha, s_eps^2 ~ 1/beta  =>  r_circ ~ (beta/alpha)^{3/2}

Then  prod_C r = (1 + r_circ)^{-3/2}   (equilateral triangle, uniform bond component).

Panels:
  A  prod r vs r_circ (log x): actual band 0.008-0.09, prediction, and what 0.177 requires.
  B  J/J0 ~ (1-rho) + r_circ^2 (1-rho) vs bond distance, three r_circ: shape survival.
  C  bar chart of r_circ for five elements from (c11, c12), with the R-required level.

No fit. The only "model" input is the harmonic zero-point scaling exponent, which is
stated explicitly; the constant prefactor is unknown (registered as Shen-20).
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环08_两分量与环流比.png")
OUT_CSV = os.path.join(HERE, "环08_两分量与环流比.csv")

TWO_PI = 2.0 * math.pi
PRODUCT_R = 0.177

# cubic elastic constants, GPa (standard tables; used only to size beta/alpha)
ELASTIC = {
    "Nb": (246.0, 134.0),
    "V": (228.0, 119.0),
    "Ta": (260.0, 157.0),
    "Al": (114.0, 62.0),
    "Pb": (49.5, 42.3),
}


def beta_over_alpha(c11, c12):
    """Keating: c11=(a+3b)/a_len, c12=(a-b)/a_len -> beta/alpha = (c11-c12)/(3c12+c11)."""
    return (c11 - c12) / (3.0 * c12 + c11)


def prod_r_from_rcirc(r):
    """prod_C r = (1 - eps_bs/2pi)^{3/2} with eps_bs/2pi = r/(1+r)  ->  (1+r)^{-3/2}."""
    return (1.0 + r) ** (-1.5)


def rcirc_required(prod):
    """inverse: r = prod^{-2/3} - 1."""
    return prod ** (-2.0 / 3.0) - 1.0


def main():
    rows = []
    print("Ring 8/9: two-component deficit split and circulation ratio")
    print("=" * 74)

    # ---------- C first (numbers), then A complement ----------
    print("\nC  Keating ratio and r_circ for five elements (rho -> 0):")
    rc = {}
    for el, (c11, c12) in ELASTIC.items():
        r = beta_over_alpha(c11, c12)
        rc[el] = r ** 1.5
        pr = prod_r_from_rcirc(rc[el])
        print(f"   {el:3s}: c11={c11:6.1f} c12={c12:6.1f}  beta/alpha={r:.4f}  "
              f"r_circ={rc[el]:.4f}  prod r={pr:.4f}")
        rows.append(("C_element", el, c11, c12, rc[el]))

    rs = np.array(list(rc.values()))
    print(f"\n   actual band: r_circ in [{rs.min():.4f}, {rs.max():.4f}]")
    print(f"   => prod r in [{prod_r_from_rcirc(rs.max()):.4f}, {prod_r_from_rcirc(rs.min()):.4f}]")
    print(f"   i.e. departure from 1 is {100*(1-prod_r_from_rcirc(rs.min())):.1f}%"
          f" to {100*(1-prod_r_from_rcirc(rs.max())):.1f}%")

    # ---------- A: what does 0.177 need? ----------
    req = rcirc_required(PRODUCT_R)
    print(f"\nA  prod r = {PRODUCT_R} requires r_circ = {req:.4f}")
    print(f"   ratio to the largest actual r_circ ({rs.max():.4f}): {req/rs.max():.1f}x")
    print(f"   ratio to the smallest ({rs.min():.4f}): {req/rs.min():.0f}x")
    rows.append(("A_required", "r_circ", req, PRODUCT_R, req / rs.max()))

    # ---------- B: shape survival ----------
    print("\nB  J/J0 ~ (1-rho) + r_circ^2 (1-rho): shape survives only for r_circ << 1")
    for r in (0.05, 0.5, 5.0):
        eps_floor = r * r          # relative size of the constant floor at rho -> 0
        print(f"   r_circ={r:4.2f}: constant floor / peak = {eps_floor:.4f} ({100*eps_floor:.1f}%)")
        rows.append(("B_floor", r, eps_floor, 100 * eps_floor, 0.0))

    # ---------- figure ----------
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 4.5))

    # A
    ax = axes[0]
    r = np.logspace(-3, 1, 500)
    ax.loglog(r, prod_r_from_rcirc(r), lw=2.2, color="#1f4e79")
    ax.axvspan(rs.min(), rs.max(), color="#2e7d32", alpha=0.22, label="实际带宽（5 元素）")
    ax.axhline(PRODUCT_R, ls="--", lw=1.2, color="#c00000")
    ax.plot([req], [PRODUCT_R], "o", ms=8, color="#c00000")
    ax.annotate(f"0.177 需 $r$={req:.2f}", xy=(req, PRODUCT_R), xytext=(0.35, 0.30),
                fontsize=9, color="#c00000",
                arrowprops=dict(arrowstyle="->", color="#c00000", lw=1))
    ax.set_xlabel(r"环流比 $r_{\rm circ}$")
    ax.set_ylabel(r"环乘积 $(1+r_{\rm circ})^{-3/2}$")
    ax.set_title(r"A 环乘积对环流比", fontsize=10)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="upper right")

    # B
    ax = axes[1]
    d = np.linspace(0, 6, 400)
    rho = np.exp(-d)      # exponential decay of the node correlation
    for r_, col, ls in [(0.05, "#2e7d32", "-"), (0.5, "#d68910", "--"), (5.0, "#c00000", ":")]:
        y = ((1 - rho) + r_ * r_) / (1 + r_ * r_)
        ax.plot(d, y, lw=1.9, color=col, ls=ls, label=f"$r_{{\\rm circ}}={r_}$")
    ax.set_xlabel(r"键距 $d/\xi$")
    ax.set_ylabel(r"$J_{ij}$（归一化）")
    ax.set_title("B 非零底项：$r_{\\rm circ}$ 大时 $(1-\\rho)$ 形状被淹没", fontsize=10)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    # C
    ax = axes[2]
    els = list(ELASTIC)
    vals = [rc[e] for e in els]
    cols = ["#1f4e79" if v < 0.2 else "#c00000" for v in vals]
    ax.bar(els, vals, color=cols, alpha=0.85)
    ax.axhline(req, ls="--", lw=1.3, color="#c00000")
    ax.text(0.02, req * 1.15, f"R 需要 {req:.2f}", fontsize=9, color="#c00000")
    ax.set_yscale("log")
    ax.set_ylabel(r"$r_{\rm circ}=(\beta/\alpha)^{3/2}$")
    ax.set_title("C 五元素的 $r_{\\rm circ}$ 与 R 所需值", fontsize=10)
    for i, v in enumerate(vals):
        ax.text(i, v * 1.15, f"{v:.3f}", ha="center", fontsize=8)
    ax.set_ylim(1e-3, 10)
    ax.grid(alpha=0.3, which="both", axis="y")

    fig.suptitle("环 8／环 9：亏角两分量分解与环流比——环乘积只能偏离 1 的 1%–11%（无拟合）",
                 fontsize=12, y=1.03)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    print(f"\nsaved {OUT_PNG}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["section", "label", "x1", "x2", "x3"])
        for r_ in rows:
            w.writerow(r_)
    print(f"saved {OUT_CSV}  ({len(rows)} rows)")

    # ---------- assertions ----------
    # inversion round-trip must be exact
    for p in (0.177, 0.5, 0.707, 0.99):
        assert abs(prod_r_from_rcirc(rcirc_required(p)) - p) < 1e-12
    # (8B.9) round-trip: recover c11, c12 from alpha, beta
    for el, (c11, c12) in ELASTIC.items():
        a_len = 1.0
        alpha = a_len * (3 * c12 + c11) / 4
        beta = a_len * (c11 - c12) / 4
        assert abs((alpha + 3 * beta) / a_len - c11) < 1e-12
        assert abs((alpha - beta) / a_len - c12) < 1e-12
    print("all structural assertions passed")


if __name__ == "__main__":
    main()
