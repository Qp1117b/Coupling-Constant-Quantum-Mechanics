import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def A3(a):
    return np.array([
        [0.0,  a, -a],
        [-a, 0.0,  a],
        [ a, -a, 0.0],
    ])


def A4(a):
    return np.array([
        [0.0,  a, 0.0, -a],
        [-a, 0.0,  a, 0.0],
        [0.0, -a, 0.0,  a],
        [ a, 0.0, -a, 0.0],
    ])


def C_of(A):
    return np.eye(A.shape[0]) + A


def laplacian_complete(n):
    L = -np.ones((n, n))
    np.fill_diagonal(L, n - 1.0)
    return L


def helmholtz(A):
    """Discrete Helmholtz decomposition on the complete graph.

    A_ij = (phi_j - phi_i) + omega_ij, with sum_j omega_ij = 0.
    The graph Laplacian is singular; pin phi_0 = 0.
    """
    n = A.shape[0]
    b = A.sum(axis=1)
    L = laplacian_complete(n)
    Lp = L.copy()
    bp = b.copy()
    # pin the zero mode by replacing the first row with phi_0 = 0
    Lp[0, :] = 0.0
    Lp[0, 0] = 1.0
    bp[0] = 0.0
    phi = np.linalg.solve(Lp, -bp)
    grad = phi[None, :] - phi[:, None]  # phi_j - phi_i
    circ = A - grad
    return phi, grad, circ, b


def loop_sum(A, cycle):
    return sum(A[cycle[k], cycle[(k + 1) % len(cycle)]] for k in range(len(cycle)))


def report(name, A):
    C = C_of(A)
    phi, grad, circ, div = helmholtz(A)
    row_sums = C.sum(axis=1)
    offdiag = C.sum() - np.trace(C)
    eigs = np.linalg.eigvals(C)
    print(f"{name}:")
    print(f"  diag={np.diag(C).tolist()}")
    print(f"  row sums={np.round(row_sums, 12).tolist()}")
    print(f"  global off-diagonal sum={offdiag:.3e}")
    print(f"  divergence of A={np.round(div, 12).tolist()}")
    print(f"  ||A_grad||={np.linalg.norm(grad):.3e}, ||A_circ||={np.linalg.norm(circ):.3e}")
    print(f"  eigenvalues={np.round(eigs, 8).tolist()}")
    return C, phi, grad, circ


def skew_constraint_rank(n):
    """Rank of the N row-sum constraints on independent skew entries."""
    pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    R = np.zeros((n, len(pairs)))
    for k, (i, j) in enumerate(pairs):
        R[i, k] += 1.0
        R[j, k] -= 1.0
    return np.linalg.matrix_rank(R), len(pairs)


# fixed representative matrices
A3c = A3(1.0)
A4c = A4(1.0)
C3c, phi3, grad3, circ3 = report("C3circ(a=1)", A3c)
C4c, phi4, grad4, circ4 = report("C4circ(a=1)", A4c)

# a pure gradient control: A_ij = phi_j - phi_i
phi_test = np.array([0.0, 1.2, -0.7])
A_grad = phi_test[None, :] - phi_test[:, None]
Cg, phig, gradg, circg = report("gradient control", A_grad)

print("skew row-sum solution space:")
for n in [3, 4, 5, 6]:
    rank, m = skew_constraint_rank(n)
    print(f"  N={n}: independent skew entries={m}, rank={rank}, "
          f"nullity={m-rank}, formula={(n-1)*(n-2)//2}")

fig = plt.figure(figsize=(15.0, 9.0), dpi=165)
gs = fig.add_gridspec(2, 3, hspace=0.32, wspace=0.28)

# Panel 1: complex spectrum of C3circ as a varies
ax1 = fig.add_subplot(gs[0, 0])
avals = np.linspace(0.0, 1.0, 101)
lam3p = 1.0 + 1j * np.sqrt(3.0) * avals
lam3m = 1.0 - 1j * np.sqrt(3.0) * avals
ax1.plot(lam3p.real, lam3p.imag, color="#1f77b4", lw=2.0, label=r"$1+i\sqrt{3}a$")
ax1.plot(lam3m.real, lam3m.imag, color="#1f77b4", lw=2.0, ls="--", label=r"$1-i\sqrt{3}a$")
ax1.scatter([1.0], [0.0], color="#d62728", zorder=5, label=r"uniform mode $1$")
for aa in [0.25, 0.5, 1.0]:
    z = 1.0 + 1j * np.sqrt(3.0) * aa
    ax1.scatter([z.real], [z.imag], color="#1f77b4", s=18, zorder=4)
    off = (-36, 7) if aa == 1.0 else (6, 7)
    ax1.annotate(f"a={aa:g}", (z.real, z.imag), textcoords="offset points",
                 xytext=off, fontsize=8)
ax1.axhline(0, color="0.75", lw=0.8)
ax1.axvline(1, color="0.75", lw=0.8)
ax1.set_xlabel(r"$\mathrm{Re}\,\lambda$")
ax1.set_ylabel(r"$\mathrm{Im}\,\lambda$")
ax1.set_title(r"$C_3^{\rm circ}$: eigenvalues $1,\ 1\pm i\sqrt{3}a$")
ax1.set_xlim(0.4, 1.6)
ax1.set_ylim(-1.9, 1.9)
ax1.legend(frameon=False, loc="upper left", fontsize=8)
ax1.grid(alpha=0.22)

# Panel 2: complex spectrum of C4circ as a varies
ax2 = fig.add_subplot(gs[0, 1])
lam4p = 1.0 + 2.0j * avals
lam4m = 1.0 - 2.0j * avals
ax2.plot(lam4p.real, lam4p.imag, color="#ff7f0e", lw=2.0, label=r"$1+2ia$")
ax2.plot(lam4m.real, lam4m.imag, color="#ff7f0e", lw=2.0, ls="--", label=r"$1-2ia$")
ax2.scatter([1.0, 1.0], [0.0, 0.0], color="#d62728", zorder=5,
            label=r"uniform mode $1$ (double)")
for aa in [0.25, 0.5, 1.0]:
    z = 1.0 + 2.0j * aa
    ax2.scatter([z.real], [z.imag], color="#ff7f0e", s=18, zorder=4)
    off = (-36, 7) if aa == 1.0 else (6, 7)
    ax2.annotate(f"a={aa:g}", (z.real, z.imag), textcoords="offset points",
                 xytext=off, fontsize=8)
ax2.axhline(0, color="0.75", lw=0.8)
ax2.axvline(1, color="0.75", lw=0.8)
ax2.set_xlabel(r"$\mathrm{Re}\,\lambda$")
ax2.set_ylabel(r"$\mathrm{Im}\,\lambda$")
ax2.set_title(r"$C_4^{\rm circ}$: eigenvalues $1,1,\ 1\pm 2ia$")
ax2.set_xlim(0.4, 1.6)
ax2.set_ylim(-2.2, 2.2)
ax2.legend(frameon=False, loc="upper left", fontsize=8)
ax2.grid(alpha=0.22)

# Panel 3: Helmholtz decomposition fractions
ax3 = fig.add_subplot(gs[0, 2])
names = [r"$C_3^{\rm circ}$", r"$C_4^{\rm circ}$", "gradient control"]
grad_frac = [np.linalg.norm(grad3) / np.linalg.norm(A3c),
             np.linalg.norm(grad4) / np.linalg.norm(A4c),
             np.linalg.norm(gradg) / np.linalg.norm(A_grad)]
circ_frac = [np.linalg.norm(circ3) / np.linalg.norm(A3c),
             np.linalg.norm(circ4) / np.linalg.norm(A4c),
             np.linalg.norm(circg) / np.linalg.norm(A_grad)]
x = np.arange(len(names))
w = 0.34
ax3.bar(x - w / 2, grad_frac, w, color="#1f77b4", label=r"$\|A_{\rm grad}\|/\|A\|$")
ax3.bar(x + w / 2, circ_frac, w, color="#2ca02c", label=r"$\|A_{\rm circ}\|/\|A\|$")
for i, (g, c) in enumerate(zip(grad_frac, circ_frac)):
    ax3.text(i - w / 2, g + 0.03, f"{g:.2f}", ha="center", fontsize=9)
    ax3.text(i + w / 2, c + 0.03, f"{c:.2f}", ha="center", fontsize=9)
ax3.set_xticks(x)
ax3.set_xticklabels(names)
ax3.set_ylabel("fraction of Frobenius norm")
ax3.set_title("Helmholtz: gradient vs circulation", pad=20)
ax3.set_ylim(0, 1.12)
ax3.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, 1.0),
           ncol=2, fontsize=8)
ax3.grid(axis="y", alpha=0.22)

# Panel 4: loop holonomy and row sums
ax4 = fig.add_subplot(gs[1, 0])
a_plot = np.linspace(0.0, 1.0, 100)
ax4.plot(a_plot, 3.0 * a_plot, color="#1f77b4", lw=2.0,
         label=r"$C_3^{\rm circ}$: $A_{01}+A_{12}+A_{20}=3a$")
ax4.plot(a_plot, 4.0 * a_plot, color="#ff7f0e", lw=2.0,
         label=r"$C_4^{\rm circ}$: $A_{01}+A_{12}+A_{23}+A_{30}=4a$")
ax4.axhline(0.0, color="0.35", lw=1.1, ls="--", label="gradient loop (zero holonomy)")
ax4.set_xlabel("edge amplitude $a$")
ax4.set_ylabel("loop holonomy")
ax4.set_title("Nonzero loop holonomy = non-gradient circulation")
ax4.legend(frameon=False, loc="upper left", fontsize=8)
ax4.grid(alpha=0.22)

# Panel 5: dimension of the C1=1 skew solution space
ax5 = fig.add_subplot(gs[1, 1])
Nvals = np.arange(2, 9)
nullity = np.array([(n - 1) * (n - 2) // 2 for n in Nvals])
grad_dim = Nvals - 1
total_skew = Nvals * (Nvals - 1) // 2
ax5.plot(Nvals, total_skew, "o-", color="0.55", label=r"all skew: $N(N-1)/2$")
ax5.plot(Nvals, nullity, "o-", color="#2ca02c",
         label=r"divergence-free: $(N-1)(N-2)/2$")
ax5.plot(Nvals, grad_dim, "s--", color="#1f77b4", label=r"gradient: $N-1$")
for n in [3, 4, 5]:
    ax5.annotate(f"N={n}: {((n-1)*(n-2)//2)}", (n, (n-1)*(n-2)//2),
                 textcoords="offset points", xytext=(8, -14), fontsize=8)
ax5.set_xlabel("number of nodes $N$")
ax5.set_ylabel("dimension")
ax5.set_title(r"$C1=1$ solution space: circulation dominates")
ax5.legend(frameon=False, loc="upper left", fontsize=8)
ax5.grid(alpha=0.22)

# Panel 6: sector dimensions for N=3,4,5
ax6 = fig.add_subplot(gs[1, 2])
Ns = np.array([3, 4, 5])
gd = Ns - 1
cd = (Ns - 1) * (Ns - 2) // 2
td = Ns * (Ns - 1) // 2
xx = np.arange(len(Ns))
w6 = 0.25
ax6.bar(xx - w6, gd, w6, color="#1f77b4", label="gradient")
ax6.bar(xx, cd, w6, color="#2ca02c", label="circulation")
ax6.bar(xx + w6, td, w6, color="0.65", label="all skew")
for i, n in enumerate(Ns):
    ax6.text(i - w6, gd[i] + 0.15, str(gd[i]), ha="center", fontsize=8)
    ax6.text(i, cd[i] + 0.15, str(cd[i]), ha="center", fontsize=8)
    ax6.text(i + w6, td[i] + 0.15, str(td[i]), ha="center", fontsize=8)
ax6.set_xticks(xx)
ax6.set_xticklabels([f"N={n}" for n in Ns])
ax6.set_ylabel("dimension")
ax6.set_title("Gradient sector vs circulation sector")
ax6.set_ylim(0, 12)
ax6.legend(frameon=False, loc="upper left", fontsize=8)
ax6.grid(axis="y", alpha=0.22)

fig.text(0.5, 0.008,
         "Matrix route: $C=I+f(a)$, $a_{ij}=-a_{ji}$ is an oriented edge connection; "
         "$C1=1$ iff $A=C-I$ is divergence-free. The gradient sector has dimension $N-1$; "
         "the circulation sector has dimension $(N-1)(N-2)/2$. Numerical examples only; "
         "no physical $C$ claimed.",
         ha="center", va="bottom", fontsize=8.5)
fig.savefig("A12_矩阵化.png", bbox_inches="tight")

# compact CSV of the representative cases
with open("A12_矩阵化.csv", "w", encoding="utf-8") as f:
    f.write("name,a,row_sum_min,row_sum_max,global_offdiag,loop_holonomy,"
            "grad_fraction,circ_fraction\n")
    for name, A, cycle in [
        ("C3circ", A3c, [0, 1, 2]),
        ("C4circ", A4c, [0, 1, 2, 3]),
        ("gradient_control", A_grad, [0, 1, 2]),
    ]:
        C = C_of(A)
        rs = C.sum(axis=1)
        _, grad, circ, _ = helmholtz(A)
        hol = loop_sum(A, cycle)
        denom = np.linalg.norm(A)
        f.write(f"{name},1.0,{rs.min():.6f},{rs.max():.6f},"
                f"{C.sum()-np.trace(C):.6e},{hol:.6e},"
                f"{np.linalg.norm(grad)/denom:.6e},{np.linalg.norm(circ)/denom:.6e}\n")

with open("A12_矩阵化_维度.csv", "w", encoding="utf-8") as f:
    f.write("N,skew_dim,row_constraint_rank,divergence_free_dim,"
            "gradient_dim,circulation_dim\n")
    for n in range(2, 9):
        rank, m = skew_constraint_rank(n)
        f.write(f"{n},{m},{rank},{m-rank},{n-1},{(n-1)*(n-2)//2}\n")
