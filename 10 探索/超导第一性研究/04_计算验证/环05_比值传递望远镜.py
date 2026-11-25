# -*- coding: utf-8 -*-
"""
Ring 5 / Shen-1: the telescoping identity of ratio transfer, and the two-layer split of r_ij.

Claim under test (all from chain text, no fit):
  (5.2)  v_{tau,j} = v_{tau,i} r_{ij}          (as an EQUALITY)
  (5.3c) r_{ji} = 1/r_{ij}                     (oriented edge variable)
  (5.3)  prod_C r in {0.177, 0.707, 0.500} != 1  (BCC triangle loops, numeric input)

  If v_tau is a single-valued site field, (5.2) forces prod_C r == 1 identically
  (telescoping).  Hence P & Q => not R.  Three assertions cannot coexist.

Panels:
  A  prod_C r vs ell for an equilateral triangle: the three BCC values invert to
     ell = 4.304 / 1.291 / 2.325 rad  (underdetermined: 3 products, 9 edge values).
  B  antisymmetry residual  lam_+ + lam_- = 1/2 ln(1-x^2)  and its relative size;
     -> "C1=1 automatic under centrosymmetric shells" fails at 19%-55% for these ell.
  C  two-way compatibility: r_ij r_ji - 1 = -x^2 ; v_j = v_j (1-x^2) has only the
     trivial solution v_j = 0 unless x = 0.
  D  the inverse problem is 6-fold underdetermined: ell_3 solved from prod=0.177
     on a grid of (ell_1, ell_2).
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
OUT_PNG = os.path.join(HERE, "环05_比值传递望远镜.png")
OUT_CSV = os.path.join(HERE, "环05_比值传递望远镜.csv")

TWO_PI = 2.0 * math.pi
BCC_PRODUCTS = [0.177, 0.707, 0.500]


def prod_equilateral(ell):
    """prod of r over an equilateral triangle: (1-x)^(3/2), x=ell/2pi."""
    x = ell / TWO_PI
    if x >= 1.0:
        return 0.0
    return (1.0 - x) ** 1.5


def invert_equilateral(target):
    """solve (1-x)^1.5 = target for x in (0,1); returns ell."""
    x = 1.0 - target ** (1.0 / 1.5)
    return x * TWO_PI


def lam_plus(ell):
    x = ell / TWO_PI
    return 0.5 * math.log(1.0 - x) if x < 1.0 else float("-inf")


def lam_minus(ell):
    x = ell / TWO_PI
    return 0.5 * math.log(1.0 + x)


def main():
    rows = []
    print("Ring 5 / Shen-1: telescoping identity and the two-layer split of r_ij")
    print("=" * 72)

    # ---------- A: inversion of the three BCC products ----------
    print("\nA  equilateral-triangle inversion of prod_C r:")
    ell_from_prod = []
    for p in BCC_PRODUCTS:
        ell = invert_equilateral(p)
        ell_from_prod.append(ell)
        print(f"   prod={p:.3f} -> x={ell/TWO_PI:.4f}, ell={ell:.4f} rad, "
              f"check prod={prod_equilateral(ell):.6f}")
        rows.append(("A_inversion", p, ell / TWO_PI, ell, prod_equilateral(ell)))
    print("   NOTE: 3 products constrain 3 sums, not 9 individual edge deficits")
    print("         -> inverse problem has 9 - 3 = 6 degrees of freedom")

    # ---------- B: antisymmetry residual ----------
    print("\nB  antisymmetry residual lam_+ + lam_- = 1/2 ln(1-x^2):")
    ells = [0.25, 0.5, 1.0, 1.291, 2.0, 2.325, 3.0, 4.0, 4.304, 5.0, 6.0]
    for ell in ells:
        x = ell / TWO_PI
        res = 0.5 * math.log(1.0 - x * x)
        lp, lm = lam_plus(ell), lam_minus(ell)
        scale = max(abs(lp), abs(lm))
        rel = abs(res) / scale if scale > 0 else 0.0
        print(f"   ell={ell:6.3f}  x={x:.4f}  residual={res:+.5f}  rel={rel*100:5.2f}%")
        rows.append(("B_residual", ell, x, res, rel))
    print("   -> 'C1=1 automatic' holds only for ell << 2pi; BCC ell are NOT in that domain")

    # ---------- C: two-way compatibility ----------
    print("\nC  two-way transfer: r_ij r_ji = 1 - x^2 < 1 for any x>0")
    for ell in (0.5, 1.291, 2.325, 4.304):
        x = ell / TWO_PI
        print(f"   ell={ell:6.3f}: r_ij*r_ji - 1 = {-x*x:+.6f}  "
              f"=> v_j = v_j(1-x^2) forces v_j=0 for x>0")
        rows.append(("C_twoway", ell, x, -x * x, 1.0 - x * x))

    # ---------- D: inverse problem underdetermination ----------
    print("\nD  solving ell_3 from prod=0.177 on an (ell_1, ell_2) grid:")
    target = 0.177
    grid = np.linspace(0.2, 3.0, 8)
    n_sol = 0
    for e1 in grid:
        for e2 in grid:
            x1, x2 = e1 / TWO_PI, e2 / TWO_PI
            f12 = (1 - x1) * (1 - x2)          # product of (1-x) over two edges
            if f12 <= 0:
                continue
            need = target * target / f12       # need (1-x3)
            if not (0.0 < need < 1.0):
                continue
            e3 = (1.0 - need) * TWO_PI
            n_sol += 1
            if n_sol <= 12:
                print(f"   ell_1={e1:.3f} ell_2={e2:.3f} -> ell_3={e3:.3f} "
                      f"(all in (0,2pi), prod={math.sqrt(f12 * need):.6f})")
            rows.append(("D_inverse", e1, e2, e3, math.sqrt(f12 * need)))
    print(f"   -> {n_sol} admissible triples on an 8x8 grid; the map is many-to-one")

    # ---------- figure ----------
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 8.6))

    # A
    ax = axes[0, 0]
    e = np.linspace(1e-4, TWO_PI * 0.995, 600)
    p = np.array([prod_equilateral(v) for v in e])
    ax.plot(e, p, lw=2, color="#1f4e79", label=r"$\prod_C r=(1-x)^{3/2}$")
    for tgt, col in zip(BCC_PRODUCTS, ["#c00000", "#2e7d32", "#7030a0"]):
        ax.axhline(tgt, ls="--", lw=1, color=col, alpha=0.8)
        ell0 = invert_equilateral(tgt)
        ax.plot([ell0], [tgt], "o", color=col, ms=6)
        ax.annotate(f"{tgt:.3f} @ $\\ell$={ell0:.2f}",
                    xy=(ell0, tgt), xytext=(ell0 + 0.35, tgt + 0.07),
                    fontsize=9, color=col)
    ax.set_xlabel(r"等边三角环的边亏角 $\ell$ (rad)")
    ax.set_ylabel(r"$\prod_C r$")
    ax.set_title("A 三环乘积反解（欠定）", fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(fontsize=9)

    # B
    ax = axes[0, 1]
    e = np.linspace(1e-4, TWO_PI * 0.97, 600)
    res = np.array([0.5 * math.log(1 - (v / TWO_PI) ** 2) for v in e])
    rel = np.array([abs(0.5 * math.log(1 - (v / TWO_PI) ** 2)) /
                    max(abs(lam_plus(v)), abs(lam_minus(v))) for v in e])
    ax.plot(e, res, lw=2, color="#c00000",
            label=r"$\lambda_++\lambda_-=\frac{1}{2}\ln(1-x^2)$")
    ax2 = ax.twinx()
    ax2.plot(e, rel * 100, lw=1.6, ls="--", color="#1f4e79", label="相对破坏 (%)")
    ax2.set_ylabel("相对破坏 (%)", color="#1f4e79")
    for ell0 in ell_from_prod:
        ax.axvline(ell0, ls=":", lw=1, color="gray")
    ax.set_xlabel(r"$\ell$ (rad)")
    ax.set_ylabel(r"反对称残差", color="#c00000")
    ax.set_title(r"B  $C_1=1$ 的自动性在 BCC 亏角下失效", fontsize=11)
    ax.grid(alpha=0.3)
    ax.legend(loc="lower left", fontsize=9)

    # C
    ax = axes[1, 0]
    e = np.linspace(1e-4, TWO_PI * 0.97, 600)
    dev = -np.array([(v / TWO_PI) ** 2 for v in e])
    ax.plot(e, dev, lw=2, color="#2e7d32")
    ax.axhline(0, color="k", lw=0.8)
    ax.fill_between(e, dev, 0, color="#2e7d32", alpha=0.18)
    ax.set_xlabel(r"$\ell$ (rad)")
    ax.set_ylabel(r"$r_{ij}r_{ji}-1=-x^2$")
    ax.set_title(r"C 同边双向等式只有平凡解（$v_j=v_j(1-x^2)$）", fontsize=11)
    ax.grid(alpha=0.3)

    # D
    ax = axes[1, 1]
    E1, E2 = np.meshgrid(np.linspace(0.2, 3.0, 200), np.linspace(0.2, 3.0, 200))
    X1, X2 = E1 / TWO_PI, E2 / TWO_PI
    with np.errstate(invalid="ignore", divide="ignore"):
        need = 0.177 ** 2 / ((1 - X1) * (1 - X2))
        E3 = np.where((need > 0) & (need < 1), (1 - need) * TWO_PI, np.nan)
    cs = ax.contourf(E1, E2, E3, levels=14, cmap="viridis")
    ax.contour(E1, E2, E3, levels=10, colors="w", linewidths=0.5, alpha=0.6)
    fig.colorbar(cs, ax=ax, label=r"$\ell_3$ (rad)")
    ax.set_xlabel(r"$\ell_1$ (rad)")
    ax.set_ylabel(r"$\ell_2$ (rad)")
    ax.set_title(r"D 反问题欠定：$\prod=0.177$ 下 $\ell_3(\ell_1,\ell_2)$", fontsize=11)

    fig.suptitle("环 5：比值传递的望远镜恒等式与 $r_{ij}$ 的两层归属（无拟合）",
                 fontsize=13, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.98))
    fig.savefig(OUT_PNG, dpi=150)
    print(f"\nsaved {OUT_PNG}")

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["panel", "x1", "x2", "x3", "x4"])
        for r_ in rows:
            w.writerow(r_)
    print(f"saved {OUT_CSV}  ({len(rows)} rows)")

    # ---------- assertions (fail loudly if the structural claims break) ----------
    for p_ in BCC_PRODUCTS:
        assert abs(prod_equilateral(invert_equilateral(p_)) - p_) < 1e-12
    for v in e:
        assert 0.5 * math.log(1 - (v / TWO_PI) ** 2) <= 1e-15
    print("\nall structural assertions passed")


if __name__ == "__main__":
    main()
