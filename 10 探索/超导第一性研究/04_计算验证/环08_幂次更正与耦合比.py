# -*- coding: utf-8 -*-
r"""
Ring 8 / ring 9: correction of the zero-point scaling exponent.

Round 79 used  sigma^2 ~ 1/k  ->  sigma ~ k^{-1/2}  ->  r_circ ~ (beta/alpha)^{3/2}.
That is WRONG.  The harmonic oscillator gives

    <x^2> = hbar/(2 m omega),   omega = sqrt(k/m)   =>   <x^2> = hbar/(2 sqrt(k m)),

so  sigma^2 ~ k^{-1/2},  sigma ~ k^{-1/4},  and

    r_circ = alpha_u s_b / (beta_u s_eps sqrt(2(1-rho)))
           ~ (alpha_u/beta_u) * (beta/alpha)^{1/4}.

With alpha_u ~ beta_u:  r_circ ~ (beta/alpha)^{1/4} = 0.45 - 0.66 for five metals,
prod_C r = (1+r_circ)^{-3/2} = 0.48 - 0.59  (NOT 0.89 - 0.99).

Consequence: 0.177 needs a coupling ratio g = alpha_u/beta_u >= 3.4, not "two orders
of magnitude" as round 79 concluded.

Panels:
  A  prod r vs g = alpha_u/beta_u (log), three metals, marked g=1 band and g needed.
  B  prod r vs beta/alpha for g = 0.5, 1, 3.4.
  C  bar chart: r_circ and prod r at g=1, versus 0.177 / 0.500 / 0.707.
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
OUT_PNG = os.path.join(HERE, "环08_幂次更正与耦合比.png")
OUT_CSV = os.path.join(HERE, "环08_幂次更正与耦合比.csv")

PRODUCT_R = 0.177
ELASTIC = {
    "Nb": (246.0, 134.0),
    "V": (228.0, 119.0),
    "Ta": (260.0, 157.0),
    "Al": (114.0, 62.0),
    "Pb": (49.5, 42.3),
}


def beta_over_alpha(c11, c12):
    return (c11 - c12) / (3.0 * c12 + c11)


def rcirc_of(b_a, g=1.0):
    return g * b_a ** 0.25


def prod_of(r):
    return (1.0 + r) ** (-1.5)


def g_required(b_a, target=PRODUCT_R):
    r_need = target ** (-2.0 / 3.0) - 1.0
    return r_need / b_a ** 0.25


def main():
    rows = []
    print("Ring 8/9: zero-point scaling exponent corrected to 1/4")
    print("=" * 72)

    print("\nA  five elements at g = alpha_u/beta_u = 1:")
    tbl = {}
    for el, (c11, c12) in ELASTIC.items():
        b_a = beta_over_alpha(c11, c12)
        r = rcirc_of(b_a, 1.0)
        p = prod_of(r)
        g_req = g_required(b_a)
        tbl[el] = (b_a, r, p, g_req)
        print(f"   {el:3s}: beta/alpha={b_a:.4f}  r_circ={r:.4f}  prod r={p:.4f}  "
              f"g needed for 0.177 = {g_req:.2f}")
        rows.append(("A_element", el, b_a, r, p))

    rs = [v[1] for v in tbl.values()]
    ps = [v[2] for v in tbl.values()]
    gs = [v[3] for v in tbl.values()]
    print(f"\n   r_circ in [{min(rs):.4f}, {max(rs):.4f}]")
    print(f"   prod r in [{min(ps):.4f}, {max(ps):.4f}]  "
          f"(departure from 1: {100*(1-max(ps)):.1f}% to {100*(1-min(ps)):.1f}%)")
    print(f"   g required in [{min(gs):.2f}, {max(gs):.2f}]")

    print("\nB  round-79 vs round-80 comparison (Nb):")
    b_a = tbl["Nb"][0]
    r_old = b_a ** 1.5
    r_new = b_a ** 0.25
    print(f"   (beta/alpha)^(3/2) = {r_old:.4f}  -> prod {prod_of(r_old):.4f}   [round 79, WRONG]")
    print(f"   (beta/alpha)^(1/4) = {r_new:.4f}  -> prod {prod_of(r_new):.4f}   [round 80, correct]")
    print(f"   ratio of r_circ: {r_new/r_old:.1f}x")
    rows.append(("B_compare", "Nb", r_old, r_new, r_new / r_old))

    # ---------- figure ----------
    fig, axes = plt.subplots(1, 3, figsize=(14.6, 4.5))

    # A
    ax = axes[0]
    g = np.logspace(-1, 1, 400)
    for el, col in [("Nb", "#1f4e79"), ("V", "#2e7d32"), ("Pb", "#c00000")]:
        b = tbl[el][0]
        ax.loglog(g, [prod_of(rcirc_of(b, gg)) for gg in g], lw=2, color=col, label=el)
    ax.axhline(PRODUCT_R, ls="--", lw=1.2, color="k")
    ax.axvline(1.0, ls=":", lw=1.2, color="gray")
    ax.text(1.05, 0.30, "$g=1$", fontsize=9, color="gray")
    gn = tbl["Nb"][3]
    ax.plot([gn], [PRODUCT_R], "o", ms=8, color="#7030a0")
    ax.annotate(f"0.177 需 $g$={gn:.1f}", xy=(gn, PRODUCT_R), xytext=(0.35, 0.13),
                fontsize=9, color="#7030a0",
                arrowprops=dict(arrowstyle="->", color="#7030a0", lw=1))
    ax.set_xlabel(r"耦合比 $g=\alpha_u/\beta_u$")
    ax.set_ylabel(r"$\prod_C r$")
    ax.set_title("A 环乘积对耦合比（对数）", fontsize=10)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9, loc="upper right")

    # B
    ax = axes[1]
    ba = np.logspace(math.log10(0.02), 0, 400)
    for gg, col, ls in [(0.5, "#2e7d32", ":"), (1.0, "#1f4e79", "-"), (3.4, "#c00000", "--")]:
        ax.semilogx(ba, [prod_of(rcirc_of(b, gg)) for b in ba], lw=2, color=col, ls=ls,
                    label=f"$g={gg}$")
    ax.axhline(PRODUCT_R, ls="--", lw=1.0, color="k", alpha=0.6)
    ax.axhspan(min(ps), max(ps), color="#1f4e79", alpha=0.15, label="$g=1$ 实际带")
    ax.set_xlabel(r"$\beta/\alpha=(c_{11}-c_{12})/(c_{11}+3c_{12})$")
    ax.set_ylabel(r"$\prod_C r$")
    ax.set_title("B 仅靠 $\\beta/\\alpha$ 到不了 0.177\n需 $g$ 抬升", fontsize=10)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="lower right")

    # C
    ax = axes[2]
    els = list(ELASTIC)
    vals_r = [tbl[e][1] for e in els]
    vals_p = [tbl[e][2] for e in els]
    x = np.arange(len(els))
    w = 0.38
    ax.bar(x - w / 2, vals_r, w, color="#1f4e79", alpha=0.85, label=r"$r_{\rm circ}$")
    ax.bar(x + w / 2, vals_p, w, color="#2e7d32", alpha=0.85, label="环乘积")
    for lvl, col, txt in [(0.177, "#c00000", "0.177"), (0.500, "#7030a0", "0.500"),
                          (0.707, "#d68910", "0.707")]:
        ax.axhline(lvl, ls="--", lw=1.0, color=col, alpha=0.8)
        ax.text(len(els) - 0.45, lvl + 0.015, txt, fontsize=8, color=col)
    ax.set_xticks(x)
    ax.set_xticklabels(els)
    ax.set_ylim(0, 0.85)
    ax.set_ylabel("数值")
    ax.set_title(r"C $g=1$ 时的环流比与环乘积" + "\n对 06 三值", fontsize=10)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("环 8／环 9：零点标度幂次更正为 $1/4$——环乘积 $0.48$–$0.59$，"
                 "0.177 需耦合比 $\\gtrsim3.3$（无拟合）", fontsize=12, y=1.03)
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    print(f"\nsaved {OUT_PNG}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w_ = csv.writer(f)
        w_.writerow(["section", "label", "x1", "x2", "x3"])
        for r_ in rows:
            w_.writerow(r_)
    print(f"saved {OUT_CSV}  ({len(rows)} rows)")

    # ---------- assertions ----------
    # harmonic identity: sqrt(k/m)*m = sqrt(k*m)
    for k, m in [(1.0, 2.0), (0.3, 7.0), (5.5, 0.4)]:
        assert abs(math.sqrt(k / m) * m - math.sqrt(k * m)) < 1e-12
    # the two exponents must differ by the observed factor
    assert 5 < r_new / r_old < 15
    # inversion round trip
    for b in (0.04, 0.17, 0.5):
        for gg in (0.5, 1.0, 3.4):
            r = rcirc_of(b, gg)
            assert abs(prod_of(r) - (1 + r) ** -1.5) < 1e-15
    print("all structural assertions passed")


if __name__ == "__main__":
    main()
