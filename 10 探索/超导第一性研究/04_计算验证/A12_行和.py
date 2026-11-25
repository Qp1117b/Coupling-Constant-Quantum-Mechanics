import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# 3-node counterexample: symmetric, diagonal 1, global off-diagonal sum zero,
# but row sums are 0, 3, 0.
C3 = np.array([
    [1.0,  1.0, -2.0],
    [1.0,  1.0,  1.0],
    [-2.0, 1.0,  1.0],
])

# 3-node circulation: non-symmetric, diagonal 1, every row sums to 1,
# global off-diagonal sum zero. This is C = I + A with A skew-symmetric.
C3circ = np.array([
    [1.0,  1.0, -1.0],
    [-1.0, 1.0,  1.0],
    [1.0, -1.0,  1.0],
])

# 4-node oriented plaquette: non-symmetric, C = I + A with A skew-symmetric.
# The positive orientation is 0 -> 1 -> 2 -> 3 -> 0.
C4circ = np.array([
    [1.0,  1.0,  0.0, -1.0],
    [-1.0, 1.0,  1.0,  0.0],
    [0.0, -1.0,  1.0,  1.0],
    [1.0,  0.0, -1.0,  1.0],
])

# 4-node example: symmetric, diagonal 1, every row sums to 1, non-zero off-diagonal.
C4 = np.array([
    [1.0,  1.0,  0.0, -1.0],
    [1.0,  1.0, -1.0,  0.0],
    [0.0, -1.0,  1.0,  1.0],
    [-1.0, 0.0,  1.0,  1.0],
])

def report(name, C):
    offdiag = C.sum() - np.trace(C)
    row_sums = C.sum(axis=1)
    eigs = np.linalg.eigvals(C)
    print(f"{name}: symmetric={bool(np.allclose(C, C.T))}, normal={bool(np.allclose(C @ C.T, C.T @ C))}")
    print(f"  global off-diagonal sum={float(offdiag):.3f}")
    print(f"  row sums={row_sums.tolist()}")
    print(f"  eigenvalues={eigs.tolist()}")
    print(f"  C @ 1={ (C @ np.ones(C.shape[0])).tolist() }")
    return row_sums

r3 = report("C3", C3)
r3c = report("C3circ", C3circ)
r4c = report("C4circ", C4circ)
r4 = report("C4", C4)

fig, axes = plt.subplots(2, 2, figsize=(11.0, 8.0), dpi=160)
axes = axes.ravel()

def panel(ax, rows, colors, title, note):
    idx = np.arange(len(rows))
    bars = ax.bar(idx, rows, color=colors, width=0.55)
    ax.axhline(1.0, color="0.35", linestyle="--", linewidth=1.2, label=r"required $(C\,1)_i=1$")
    ax.set_xticks(idx)
    ax.set_xticklabels([f"row {i}" for i in idx])
    ax.set_ylabel(r"row sum $\sum_j C_{ij}$")
    ax.set_title(title)
    ax.set_ylim(-0.4, 3.4)
    for b, v in zip(bars, rows):
        ax.text(b.get_x() + b.get_width()/2, v + 0.08, f"{v:.0f}", ha="center", va="bottom", fontsize=10)
    ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=11)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", alpha=0.25)

panel(axes[0], r3, ["#1f77b4", "#d62728", "#1f77b4"],
      "N=3 symmetric: global A12 holds, C1=1 fails",
      r"$\sum_{i\ne j}C_{ij}=0$")
panel(axes[1], r3c, ["#9467bd"] * 3,
      "N=3 circulation: C1=1, C not symmetric",
      r"$C=I+A,\ A^{T}=-A$")
panel(axes[2], r4c, ["#ff7f0e"] * 4,
      "N=4 oriented plaquette: C1=1, C not symmetric",
      r"$0\to1\to2\to3\to0$")
panel(axes[3], r4, ["#2ca02c"] * 4,
      "N=4 symmetric: C1=1, but f must be even",
      r"$A=A^{T}$")

fig.text(0.5, 0.005,
         "Matrix-level A12 only; Lean no-go: no single odd monotone f generates a nontrivial C with C1=1.",
         ha="center", va="bottom", fontsize=9)
fig.tight_layout(rect=[0, 0.035, 1, 1])
fig.savefig("A12_行和.png", bbox_inches="tight")
