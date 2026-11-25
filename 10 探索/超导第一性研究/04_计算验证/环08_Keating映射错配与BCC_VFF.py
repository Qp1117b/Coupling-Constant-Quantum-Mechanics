# -*- coding: utf-8 -*-
r"""
Ring 8 / M5 x Shen-19/20: the Keating lattice mismatch and the BCC VFF.

Rounds 79/80 used (8B.3)/(8B.9)

    U = 3a/(16 r0^2) sum (r_ij^2 - r0^2)^2 + 3b/(8 r0^2) sum (r_ij.r_ik + r0^2/3)^2
    c11 = (al + 3 be)/a,  c12 = (al - be)/a,  c44 = 4 al be/(a (al + be))

That is the DIAMOND (tetrahedral, 4-coordinated) Keating formula.  Its
bond-bending equilibrium is cos(theta) = -1/3.  BCC has 8 nearest neighbours
with equilibrium angles {70.5, 109.5, 180} degrees, so the formula is a
lattice mismatch for BCC.

This script
  1. validates the diamond formula on Si (c44 79.2 vs 79.6 GPa, 0.5%),
  2. derives the correct BCC two-parameter VFF by exact enumeration,
  3. tests the resulting falsifiable identity  c44 = (4 c11 + 5 c12)/9,
  4. recomputes beta/alpha, r_circ and prod_C r for five BCC metals,
  5. reports the robust band and the coupling ratio g = alpha_u/beta_u
     required by the 06 values 0.177 / 0.707 / 0.500.

Everything is direct evaluation of the stated formulas: no fitting.

Run:  python "10 探索/超导第一性研究/04_计算验证/环08_Keating映射错配与BCC_VFF.py"
"""
import csv
import math
import os
from fractions import Fraction as F

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环08_Keating映射错配与BCC_VFF.png")
OUT_CSV = os.path.join(HERE, "环08_Keating映射错配与BCC_VFF.csv")

# BCC metals: (c11, c12, c44) in GPa, standard room-temperature values.
BCC = {
    "Nb": (246.0, 134.0, 28.7),
    "V": (228.0, 119.0, 42.6),
    "Ta": (260.0, 157.0, 87.4),
    "Mo": (464.0, 167.0, 110.0),
    "W": (523.0, 203.0, 160.0),
}
# Diamond-structure validation point.
SI = (165.7, 63.9, 79.6, 5.431)  # GPa, GPa, GPa, Angstrom

DIRS = [(a, b, c) for a in (1, -1) for b in (1, -1) for c in (1, -1)]


# ---------------------------------------------------------------- exact BCC VFF
def q_stretch(eps):
    """sum_{8 bonds} (n.eps.n)^2  (the 8 <111> directions, one per cell bond)."""
    t = F(0)
    for n in DIRS:
        v = sum(F(n[i] * n[j], 3) * eps[i][j] for i in range(3) for j in range(3))
        t += v * v
    return t


def q_bend(eps):
    """sum_{28 pairs per atom} (d cos theta)^2 * 9/8  (sin^2 theta0 = 8/9)."""
    t = F(0)
    for i in range(8):
        for j in range(i + 1, 8):
            nj, nk = DIRS[i], DIRS[j]
            c = F(sum(nj[a] * nk[a] for a in range(3)), 3)

            def nd(a, b):
                return F(sum(a[x] * b[y] * eps[x][y] for x in range(3) for y in range(3)), 3)

            dc = 2 * nd(nj, nk) - c * (nd(nj, nj) + nd(nk, nk))
            if abs(c) == 1:  # antipodal pair: no bending
                assert dc == 0
                continue
            t += dc * dc
    return F(9, 8) * t


def diag(a, b, c):
    return [[F(a), F(0), F(0)], [F(0), F(b), F(0)], [F(0), F(0), F(c)]]


def shear(i, j):
    e = [[F(0)] * 3 for _ in range(3)]
    e[i][j] = F(1)
    e[j][i] = F(1)
    return e


def bcc_coefficients():
    """Return (p_s, q_s, r_s, p_b, q_b, r_b) with U^cell = al/2*Qs + be*Qb."""
    p_s, q_s, r_s = q_stretch(diag(1, 0, 0)), None, q_stretch(shear(0, 1)) / 4
    q_s = (q_stretch(diag(1, 1, 0)) - 2 * p_s) / 2
    p_b, r_b = q_bend(diag(1, 0, 0)), q_bend(shear(0, 1)) / 4
    q_b = (q_bend(diag(1, 1, 0)) - 2 * p_b) / 2
    return p_s, q_s, r_s, p_b, q_b, r_b


def numeric_energy(eps, alpha=1.0, beta=1.0):
    """Direct finite-strain energy of one cell: stretch over 8 bonds, bend over
    2 x 28 pairs.  Used only to validate the exact quadratic forms."""
    A = np.eye(3) + np.array(eps, dtype=float)
    us = 0.0
    for n in DIRS:
        r = A @ np.array(n, dtype=float)
        d0 = math.sqrt(3.0)
        us += 0.5 * alpha * ((np.linalg.norm(r) - d0) / d0) ** 2
    ub = 0.0
    for i in range(8):
        for j in range(i + 1, 8):
            ri = A @ np.array(DIRS[i], dtype=float)
            rj = A @ np.array(DIRS[j], dtype=float)
            c0 = np.dot(DIRS[i], DIRS[j]) / 3.0
            if abs(c0) > 0.999:
                continue
            c1 = np.dot(ri, rj) / (np.linalg.norm(ri) * np.linalg.norm(rj))
            ub += 0.5 * beta * (c1 - c0) ** 2 * (9.0 / 8.0)
    return us + 2.0 * ub


# ---------------------------------------------------------------- elastic maps
def diamond_c44(c11, c12):
    """Keating diamond formula.  With al = c11 + 3 c12, be = c11 - c12
    (the dimensionless combinations of (8B.9)), c44 = al be/(al + be).
    Equivalent to the textbook form c44 = 4 al' be'/(a (al' + be')) with
    dimensionful al' = a al/4, be' = a be/4."""
    al = 3.0 * c12 + c11
    be = c11 - c12
    return al * be / (al + be)


def diamond_beta_over_alpha(c11, c12):
    return (c11 - c12) / (c11 + 3.0 * c12)


def bcc_beta_over_alpha(c11, c12):
    return (c11 - c12) / (12.0 * (c11 + 2.0 * c12))


def bcc_c44_pred(c11, c12):
    return (4.0 * c11 + 5.0 * c12) / 9.0


def rcirc_of(b_a, g=1.0):
    return g * b_a ** 0.25


def prod_of(r):
    return (1.0 + r) ** (-1.5)


def g_required(b_a, target):
    r_need = target ** (-2.0 / 3.0) - 1.0
    return r_need / b_a ** 0.25


def main():
    rows = []
    print("Ring 8 / M5 x Shen-19/20: Keating lattice mismatch and BCC VFF")
    print("=" * 78)

    # ---- 0. exact coefficients -------------------------------------------
    p_s, q_s, r_s, p_b, q_b, r_b = bcc_coefficients()
    print("\n0  exact BCC VFF coefficients (per cell, V = a^3/2):")
    print(f"   stretch: p={p_s}  q={q_s}  r={r_s}")
    print(f"   bend   : p={p_b}  q={q_b}  r={r_b}")

    # clean closed forms (per a^3)
    def C11(al, be):
        return 16 * al / 9 + 128 * be / 3

    def C12(al, be):
        return 16 * al / 9 - 64 * be / 3

    def C44(al, be):
        return 16 * (al + 4 * be) / 9

    # matching U^cell = (a^3/4)[c11 sum eii^2 + 2 c12 sum eii ejj + 4 c44 sum eij^2]
    for al, be in [(1.0, 0.0), (0.0, 1.0), (2.0, 3.0)]:
        assert abs(C11(al, be) - 4 * (al / 2 * float(p_s) + be * float(p_b))) < 1e-9
        assert abs(C12(al, be) - 4 * (al / 2 * float(q_s) + be * float(q_b))) < 1e-9
        assert abs(C44(al, be) - 4 * (al / 2 * float(r_s) + be * float(r_b))) < 1e-9
    print("   closed forms: c11=16al/9+128be/3, c12=16al/9-64be/3, c44=16(al+4be)/9  (x 1/a^3)")

    # ---- 1. finite-strain validation of the quadratic forms --------------
    print("\n1  finite-strain validation of the exact quadratic forms:")
    h = F(1, 10000)

    def scale(m, s):
        return [[F(v) * s for v in row] for row in m]

    cases = [("e11", diag(h, 0, 0)),
             ("e11+e22", diag(h, h, 0)),
             ("e12", scale(shear(0, 1), h))]
    for name, eps in cases:
        num = numeric_energy(eps)
        ana = 0.5 * float(q_stretch(eps)) + float(q_bend(eps))
        ratio = num / ana
        print(f"   {name:8s}: numeric={num:.6e}  analytic={ana:.6e}  ratio={ratio:.8f}")
        assert abs(ratio - 1.0) < 1e-3, "quadratic form does not match finite strain"
        rows.append(("validate", name, num, ana, ratio))

    # ---- 2. diamond formula is validated on Si ---------------------------
    c11, c12, c44, a = SI
    pred = diamond_c44(c11, c12)
    err = 100.0 * (pred - c44) / c44
    print(f"\n2  diamond Keating validated on Si: c44 pred={pred:.1f} exp={c44:.1f} GPa "
          f"({err:+.1f}%)")
    assert abs(err) < 2.0, "diamond formula does not reproduce Si"
    rows.append(("Si", "diamond_c44", pred, c44, err))

    # ---- 3. the BCC identity fails for every BCC metal -------------------
    print("\n3  BCC identity  c44 = (4 c11 + 5 c12)/9  (the falsification):")
    print(f"   {'el':3s} {'c44_exp':>8s} {'c44_vff':>8s} {'ratio':>6s} "
          f"{'Cauchy_exp':>10s} {'Cauchy_vff':>10s}")
    fails = []
    for el, (c11, c12, c44) in BCC.items():
        cp = bcc_c44_pred(c11, c12)
        ratio = cp / c44
        fails.append(ratio)
        print(f"   {el:3s} {c44:8.1f} {cp:8.1f} {ratio:6.2f} "
              f"{c12 - c44:10.1f} {c12 - cp:10.1f}")
        rows.append(("falsify", el, c44, cp, ratio))
    print(f"   -> VFF over-predicts c44 by {min(fails):.1f}x to {max(fails):.1f}x; "
          f"Cauchy pressure sign is WRONG for all five.")
    assert min(fails) > 2.0, "identity unexpectedly holds"

    # ---- 4. beta/alpha under the two mappings ----------------------------
    print("\n4  beta/alpha: diamond (wrong lattice) vs BCC (right lattice):")
    print(f"   {'el':3s} {'(diamond)':>10s} {'(BCC)':>10s} {'ratio':>7s} "
          f"{'r_circ':>8s} {'prod r':>8s} {'g(0.177)':>9s}")
    tbl = {}
    for el, (c11, c12, c44) in BCC.items():
        bd = diamond_beta_over_alpha(c11, c12)
        bb = bcc_beta_over_alpha(c11, c12)
        r = rcirc_of(bb, 1.0)
        p = prod_of(r)
        g177 = g_required(bb, 0.177)
        tbl[el] = (bd, bb, r, p, g177)
        print(f"   {el:3s} {bd:10.4f} {bb:10.4f} {bd / bb:7.2f} "
              f"{r:8.4f} {p:8.4f} {g177:9.2f}")
        rows.append(("ratios", el, bd, bb, bd / bb))
    rs = [v[2] for v in tbl.values()]
    ps = [v[3] for v in tbl.values()]
    print(f"   -> r_circ in [{min(rs):.4f}, {max(rs):.4f}]  (round 80 said 0.45-0.66)")
    print(f"   -> prod_C r in [{min(ps):.4f}, {max(ps):.4f}]  (round 80 said 0.47-0.57)")

    # ---- 5. what g does each 06 value need -------------------------------
    print("\n5  coupling ratio g = alpha_u/beta_u required by the 06 values:")
    print(f"   {'el':3s} {'g(0.177)':>9s} {'g(0.707)':>9s} {'g(0.500)':>9s}")
    for el, (bd, bb, r, p, g177) in tbl.items():
        g707 = g_required(bb, 0.707)
        g500 = g_required(bb, 0.500)
        print(f"   {el:3s} {g177:9.2f} {g707:9.2f} {g500:9.2f}")
        rows.append(("g_req", el, g177, g707, g500))

    # ---- 6. the 1/4-power robustness band --------------------------------
    print("\n6  robustness of the 1/4 power (beta/alpha from 0.015 to 0.6):")
    band = []
    for b in (0.015, 0.03, 0.1, 0.2, 0.6):
        r = rcirc_of(b)
        band.append((b, r, prod_of(r)))
        print(f"   beta/alpha={b:5.3f} -> r_circ={r:.3f}  prod r={prod_of(r):.3f}")
        rows.append(("band", f"{b:.3f}", b, r, prod_of(r)))

    # ---------- figure ----------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(15.0, 4.6), layout="constrained")

    # A: c44 falsification
    ax = axes[0]
    els = list(BCC)
    x = np.arange(len(els))
    w = 0.38
    ax.bar(x - w / 2, [BCC[e][2] for e in els], w, color="#1f4e79", label="实验 $c_{44}$")
    ax.bar(x + w / 2, [bcc_c44_pred(*BCC[e][:2]) for e in els], w,
           color="#c00000", alpha=0.85, label="BCC VFF 预测")
    for i, e in enumerate(els):
        ax.text(i, max(BCC[e][2], bcc_c44_pred(*BCC[e][:2])) + 8,
                f"{bcc_c44_pred(*BCC[e][:2]) / BCC[e][2]:.1f}×", ha="center", fontsize=8,
                color="#c00000")
    ax.set_xticks(x)
    ax.set_xticklabels(els)
    ax.set_ylabel("GPa")
    ax.set_title("A  两参数 VFF 的 $c_{44}=(4c_{11}+5c_{12})/9$\n对五个 BCC 金属全部失败", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3, axis="y")

    # B: prod r vs g
    ax = axes[1]
    g = np.logspace(-1, 1.2, 400)
    for el, col in [("Nb", "#1f4e79"), ("Ta", "#2e7d32"), ("W", "#c00000")]:
        bb = tbl[el][1]
        ax.loglog(g, [prod_of(rcirc_of(bb, gg)) for gg in g], lw=2, color=col, label=el)
    for lvl, ls in [(0.177, "--"), (0.500, ":"), (0.707, "-.")]:
        ax.axhline(lvl, ls=ls, lw=1.1, color="k", alpha=0.7)
        ax.text(0.11, lvl * 1.02, f"{lvl}", fontsize=8)
    ax.axvspan(0.6, 1.8, color="gray", alpha=0.15, label="$g\\sim1$ 带")
    ax.set_xlabel(r"$g=\alpha_u/\beta_u$")
    ax.set_ylabel(r"$\Pi_C\, r$", labelpad=6)
    ax.set_title("B  环乘积对耦合比\n$0.707/0.500$ 对应 $g\\sim1$，$0.177$ 需 $g\\gtrsim5$", fontsize=10)
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=8, loc="lower left")

    # C: beta/alpha under three mappings
    ax = axes[2]
    maps = ["diamond\n(错配)", "BCC VFF", "C'/B\n(无几何因子)"]
    for i, el in enumerate(els):
        bd, bb = tbl[el][0], tbl[el][1]
        cb = (BCC[el][0] - BCC[el][1]) / 2.0 / ((BCC[el][0] + 2 * BCC[el][1]) / 3.0)
        ax.bar(i + np.array([-0.25, 0.0, 0.25]), [bd, bb, cb], 0.22,
               color=["#c00000", "#1f4e79", "#2e7d32"])
    ax.set_yscale("log")
    ax.set_xticks(np.arange(len(els)))
    ax.set_xticklabels(els)
    ax.set_ylabel(r"$\beta/\alpha$")
    ax.set_title("C  $\\beta/\\alpha$ 的三种口径\n错配公式系统性高 $\\gtrsim9$ 倍", fontsize=10)
    ax.grid(alpha=0.3, axis="y")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#c00000", label=maps[0]),
                       Patch(color="#1f4e79", label=maps[1]),
                       Patch(color="#2e7d32", label=maps[2])], fontsize=7)

    fig.suptitle("环 8／`M5`×`审-19/20`：Keating 映射是金刚石的，BCC 需另立；"
                 "$r_{\\rm circ}$ 降至 $0.35$–$0.42$，$\\prod_Cr$ 升至 $0.59$–$0.64$",
                 fontsize=11.5, y=1.04)
    fig.savefig(OUT_PNG, dpi=150, bbox_inches="tight")
    print(f"\nsaved {OUT_PNG}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["section", "label", "x1", "x2", "x3"])
        for r_ in rows:
            wr.writerow(r_)
    print(f"saved {OUT_CSV}  ({len(rows)} rows)")

    # ---------- structural assertions ------------------------------------
    # the exact coefficients are the rationals derived by hand
    assert (p_s, q_s, r_s) == (F(8, 9), F(8, 9), F(8, 9))
    assert (p_b, q_b, r_b) == (F(32, 3), F(-16, 3), F(16, 9))
    # the BCC identity holds identically for the closed forms
    for al, be in [(1, 0), (0, 1), (2, 3), (-1, 5)]:
        assert abs(9 * C44(al, be) - (4 * C11(al, be) + 5 * C12(al, be))) < 1e-12
    # the diamond formula reproduces its own Keating identity
    for c11_, c12_ in [(165.7, 63.9), (246.0, 134.0)]:
        c44_ = diamond_c44(c11_, c12_)
        assert abs(2 * c44_ * (c11_ + c12_) - (c11_ - c12_) * (c11_ + 3 * c12_)) < 1e-9
    # the diamond/BCC ratio is at least 9 for c11 >= c12 > 0
    for c11_, c12_ in [(246.0, 134.0), (523.0, 203.0), (49.5, 42.3)]:
        assert diamond_beta_over_alpha(c11_, c12_) >= 9 * bcc_beta_over_alpha(c11_, c12_) - 1e-12
    print("all structural assertions passed")


if __name__ == "__main__":
    main()
