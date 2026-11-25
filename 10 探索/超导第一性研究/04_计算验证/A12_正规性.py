# -*- coding: utf-8 -*-
"""A12 normality numerical check.

Any odd elementwise f of an antisymmetric edge matrix yields C = I + B with
Bᵀ = -B, hence C is normal.  The plot checks two consequences numerically:
  * eigenvalues of C lie on Re = 1;
  * the normal residual ||C Cᵀ - Cᵀ C|| is at machine precision.
It is a check of the Lean theorem, not a fit to data.
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

rng = np.random.default_rng(20261121)
N = 5
L = rng.normal(size=(N, N))
L = L - L.T
L = L / np.max(np.abs(L))

fs = [
    ("f(x)=x", lambda x: x),
    ("f(x)=tanh(x)", np.tanh),
    ("f(x)=x/(1+|x|)", lambda x: x / (1.0 + np.abs(x))),
    ("f(x)=arctan(x)", np.arctan),
    ("f(x)=sin(x)", np.sin),
]

fig, axes = plt.subplots(1, 3, figsize=(15.5, 4.8))

# Panel 1: spectra for all f at full amplitude.
ax = axes[0]
colors = ["#4c78a8", "#f58518", "#54a24b", "#b279a2", "#e45756"]
for (label, f), color in zip(fs, colors):
    B = f(L)
    C = np.eye(N) + B
    eig = np.linalg.eigvals(C)
    ax.scatter(eig.real, eig.imag, s=48, color=color, alpha=0.8, label=label, zorder=3)
ax.axvline(1.0, color="k", lw=1.0, ls="--")
ax.set_xlabel("Re λ(C)")
ax.set_ylabel("Im λ(C)")
ax.set_title("Spectra of C = I + f(λ): all on Re = 1")
ax.legend(fontsize=8, loc="upper left")
ax.grid(alpha=0.25)
ax.set_xlim(0.90, 1.10)

# Panel 2: normal residual vs amplitude.
ax = axes[1]
amps = np.linspace(0.05, 1.0, 20)
for (label, f), color in zip(fs, colors):
    residuals = []
    for a in amps:
        B = f(a * L)
        C = np.eye(N) + B
        residuals.append(np.max(np.abs(C @ C.T - C.T @ C)))
    ax.semilogy(amps, residuals, marker="o", ms=3, color=color, label=label)
ax.set_xlabel("edge amplitude a")
ax.set_ylabel(r"$\max |CC^T-C^TC|$")
ax.set_title("Normal residual: machine precision for every f")
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=8)

# Panel 3: max deviation of Re λ(C) from 1.
ax = axes[2]
for (label, f), color in zip(fs, colors):
    deviations = []
    for a in amps:
        B = f(a * L)
        C = np.eye(N) + B
        deviations.append(np.max(np.abs(np.linalg.eigvals(C).real - 1.0)))
    ax.semilogy(amps, deviations, marker="s", ms=3, color=color, label=label)
ax.set_xlabel("edge amplitude a")
ax.set_ylabel(r"$\max |\mathrm{Re}\,\lambda(C)-1|$")
ax.set_title("Spectral real part: deviation from 1")
ax.grid(alpha=0.25, which="both")
ax.legend(fontsize=8)

fig.suptitle("A12 matrix branch: normality is exact, not a numerical coincidence", fontsize=13)
fig.text(0.5, 0.01,
         "Lean: A12Normality.lean. Numerical check only; f and λ are illustrative, not material data.",
         ha="center", fontsize=9)
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig("A12_正规性.png", dpi=180)
plt.close()

# CSV: summary at full amplitude.
with open("A12_正规性.csv", "w", encoding="utf-8-sig") as fh:
    fh.write("f,normal_residual,max_abs_Re_eig_minus_1,eig_real_min,eig_real_max\n")
    for label, f in fs:
        C = np.eye(N) + f(L)
        eig = np.linalg.eigvals(C)
        residual = np.max(np.abs(C @ C.T - C.T @ C))
        dev = np.max(np.abs(eig.real - 1.0))
        fh.write(f"{label},{residual:.6e},{dev:.6e},{eig.real.min():.6e},{eig.real.max():.6e}\n")

print("N =", N)
for label, f in fs:
    C = np.eye(N) + f(L)
    eig = np.linalg.eigvals(C)
    residual = np.max(np.abs(C @ C.T - C.T @ C))
    dev = np.max(np.abs(eig.real - 1.0))
    print(f"{label:20s} normal_residual={residual:.3e} max|Re-1|={dev:.3e}")
