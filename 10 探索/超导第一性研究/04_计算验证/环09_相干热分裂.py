import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

# Dimensionless units: omega_D = 1, rho_m = 1, g = 1, hbar = k_B = 1.
Z = 0.75

def debye_integral(x: float) -> float:
    """I(x)=int_0^x u/(exp(u)-1) du, with the removable value at 0 set to 1."""
    if x <= 0.0:
        return 0.0
    u = np.linspace(0.0, x, 40001)
    f = np.ones_like(u)
    f[1:] = u[1:] / np.expm1(u[1:])
    return float(np.trapezoid(f, u))

def coherent_integral(x: float) -> float:
    """J(x)=int_0^x u*tanh(u/2) du, the coherent spectral integral."""
    if x <= 0.0:
        return 0.0
    u = np.linspace(0.0, x, 40001)
    f = u * np.tanh(0.5 * u)
    return float(np.trapezoid(f, u))

T = np.logspace(-2.0, 1.5, 360)
Theta = np.array([3.0 * ti * ti * debye_integral(1.0 / ti) for ti in T])
Vcoh = np.array([1.5 * ti * ti * coherent_integral(1.0 / ti) for ti in T])
Vinc = Theta.copy()
Vtot = Z + Vinc

# Node-only normalized stiffness: J/J0 = Vcoh/Z when sigma_omega = 0.
Jnorm = Vcoh / Z
Gnorm = Vinc / Z

# Single-mode exact check: Z=1, omega=1, n_B at T.
T_single = np.logspace(-2.0, 1.2, 220)
nB = 1.0 / np.expm1(1.0 / T_single)
Vtot_s = 1.0 * (1.0 + 2.0 * nB)
Vcoh_s = 1.0 / (1.0 + 2.0 * nB)
Vinc_s = 2.0 * nB
prod_res = Vcoh_s * Vtot_s - 1.0

fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.2), dpi=160)

ax = axes[0, 0]
ax.plot(T, Vtot / Z, "-", color="#d62728", label=r"$V_{\rm tot}/Z$")
ax.plot(T, Vcoh / Z, "-", color="#1f77b4", label=r"$V_{\rm coh}/Z$")
ax.plot(T, Vinc / Z, "-", color="#2ca02c", label=r"$V_{\rm inc}/Z$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$T/\omega_D$")
ax.set_ylabel("normalized second moment")
ax.set_title("Total / coherent / incoherent (log scale)")
ax.legend(frameon=False)
ax.grid(alpha=0.25)

ax = axes[0, 1]
ax.plot(T, Jnorm, "-", color="#1f77b4", label=r"$J/J_0=V_{\rm coh}/Z$")
ax.plot(T, Gnorm, "-", color="#2ca02c", label=r"$\Gamma$ proxy $=V_{\rm inc}/Z$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$T/\omega_D$")
ax.set_ylabel("normalized value")
ax.set_title("Stiffness down, dephasing up (log scale)")
ax.legend(frameon=False)
ax.grid(alpha=0.25)

ax = axes[1, 0]
ax.plot(T_single, Vcoh_s / Vtot_s, "-", color="#9467bd", label=r"$V_{\rm coh}/V_{\rm tot}=1/(1+2n_B)^2$")
ax.plot(T_single, np.sqrt(Vcoh_s / Vtot_s), "--", color="#ff7f0e", label=r"amplitude fraction $=1/(1+2n_B)$")
ax.set_xscale("log")
ax.set_xlabel(r"$T/\omega$")
ax.set_ylabel("ratio")
ax.set_title("Single mode: coherent fraction")
ax.legend(frameon=False)
ax.grid(alpha=0.25)

ax = axes[1, 1]
ax.plot(T, Vcoh / Z, "-", color="#1f77b4", label=r"Debye continuum $V_{\rm coh}/Z$")
ax.plot(T_single, Vcoh_s, "--", color="#ff7f0e", label=r"single mode $Z/(Z+\Theta)$")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel(r"$T/\omega$")
ax.set_ylabel(r"$V_{\rm coh}/Z$")
ax.set_title("Debye vs single mode: no simple product identity")
ax.legend(frameon=False)
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("环09_相干热分裂.png", bbox_inches="tight")

with open("环09_相干热分裂.csv", "w", encoding="utf-8") as f:
    f.write("T_over_omega_D,Z,Theta,Vinc,Vtot,Vcoh,Jnorm,Gnorm\n")
    for ti, th, vi, vt, vc, jn, gn in zip(T, Theta, Vinc, Vtot, Vcoh, Jnorm, Gnorm):
        f.write(f"{ti:.8g},{Z:.8g},{th:.8g},{vi:.8g},{vt:.8g},{vc:.8g},{jn:.8g},{gn:.8g}\n")

print("Z =", Z)
print("Vcoh at smallest T =", float(Vcoh[0]), "Vcoh at largest T =", float(Vcoh[-1]))
print("Vinc at smallest T =", float(Vinc[0]), "Vinc at largest T =", float(Vinc[-1]))
print("min dVcoh (should be <= 0):", float(np.diff(Vcoh).min()))
print("max dVinc (should be >= 0):", float(np.diff(Vinc).max()))
print("max |Vtot-(Z+Vinc)| =", float(np.max(np.abs(Vtot - (Z + Vinc)))))
print("single-mode max |Vcoh*Vtot-Z^2| =", float(np.max(np.abs(prod_res))))
print("single-mode Vcoh(0)/Z =", float(Vcoh_s[0]), "with Z=1")
