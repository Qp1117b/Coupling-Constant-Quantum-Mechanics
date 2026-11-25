import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Optional Chinese font; fall back silently if unavailable.
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

def debye_integral(x: float) -> float:
    """I(x)=int_0^x u/(exp(u)-1) du, with the removable value at 0 set to 1."""
    if x <= 0.0:
        return 0.0
    u = np.linspace(0.0, x, 30001)
    f = np.ones_like(u)
    f[1:] = u[1:] / np.expm1(u[1:])
    return float(np.trapezoid(f, u))

# Dimensionless units: omega_D = 1, rho_m = 1, g = 1.
# Z = 3g^2/(4 rho_m omega_D) = 3/4.
Z = 0.75
t = np.logspace(-2.0, 1.5, 420)
I = np.array([debye_integral(1.0 / ti) for ti in t])
Theta = 3.0 * t**2 * I
total = Z + Theta

# Thermal velocity variance (linearised), normalized geometry.
sigma_v2 = Theta / (16.0 * np.pi**2 * (1.0 - 0.1 / (2.0 * np.pi)))
# Normalized dephasing; shape only, not a physical rate.
Gamma = 3.0 * sigma_v2
R = np.exp(-Gamma)

# Old threshold probability from total variance; direction is increasing.
threshold = 0.95
p_old = (total > threshold).astype(float)

# External BCS weak-coupling reference: Tc/omega_c = 1.13 exp(-1/lambda).
lam = np.linspace(0.10, 1.0, 500)
Tc_over_omega = 1.13 * np.exp(-1.0 / lam)

fig, axes = plt.subplots(1, 3, figsize=(15.2, 4.6), dpi=160)

ax = axes[0]
ax.plot(t, Z * np.ones_like(t), "--", color="0.45", label=r"$Z$ (zero-point)")
ax.plot(t, Theta, "-", color="#1f77b4", label=r"$\Theta(T)$ (thermal)")
ax.plot(t, total, "-", color="#d62728", label=r"$Z+\Theta(T)$")
ax.set_xscale("log")
ax.set_xlabel(r"$T/\omega_D$")
ax.set_ylabel(r"normalized variance")
ax.set_title("Debye variance decomposition")
ax.legend(frameon=False)
ax.grid(alpha=0.25)

ax = axes[1]
ax.step(t, p_old, where="post", color="#1f77b4", label=r"old $P(T)=1[\mathrm{Var}>\sigma_c]$")
ax.plot(t, R / R[0], "-", color="#ff7f0e", label=r"$R_n(T)$ (thermal dephasing)")
ax.set_xscale("log")
ax.set_xlabel(r"$T/\omega_D$")
ax.set_ylabel("normalized value")
ax.set_title("Direction check: old threshold vs dephasing")
ax.set_ylim(-0.05, 1.08)
ax.legend(frameon=False, loc="center left")
ax.grid(alpha=0.25)

ax = axes[2]
ax.plot(lam, Tc_over_omega, color="#2ca02c")
ax.set_xlabel(r"$\lambda$")
ax.set_ylabel(r"$T_c/\omega_c$")
ax.set_title("External BCS reference: $1.13\\,e^{-1/\\lambda}$")
ax.grid(alpha=0.25)

fig.tight_layout()
fig.savefig("温度架构.png", bbox_inches="tight")

with open("温度架构.csv", "w", encoding="utf-8") as f:
    f.write("T_over_omega_D,Z,Theta,Total,P_old,R_n\n")
    for ti, zi, th, to, po, rn in zip(t, np.full_like(t, Z), Theta, total, p_old, R / R[0]):
        f.write(f"{ti:.8g},{zi:.8g},{th:.8g},{to:.8g},{po:.8g},{rn:.8g}\n")

# Quantitative checks: monotonicity of thermal variance and coherence.
dTheta = np.diff(Theta)
dR = np.diff(R / R[0])
print("min dTheta (should be >= 0):", float(dTheta.min()))
print("max dR (should be <= 0):", float(dR.max()))
print("Z =", Z)
print("Theta at smallest T =", float(Theta[0]), "Theta at largest T =", float(Theta[-1]))
print("threshold crossing T/omega_D =", float(t[np.argmax(total > threshold)]) if np.any(total > threshold) else None)
