import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv

# Proper-time history H_ij = tau_i - tau_j (06 convention)
tau = np.array([0.30, -0.20, 0.10])
H = np.array([[tau[i] - tau[j] for j in range(3)] for i in range(3)])
H_loop = H[0, 1] + H[1, 2] + H[2, 0]

# U(1) phase connection on directed three- and four-cycles
alpha = 1.0
a = np.linspace(0.0, 1.0, 101)
theta3_loop = 3.0 * alpha * a
theta4_loop = 4.0 * alpha * a

# Edge values at a = 1 for C3
a0 = 1.0
theta3 = np.array([
    [0.0, alpha * a0, -alpha * a0],
    [-alpha * a0, 0.0, alpha * a0],
    [alpha * a0, -alpha * a0, 0.0],
])
H3 = H

fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
plt.rcParams.update({"font.size": 10})

ax = axes[0, 0]
edge_labels = ["0->1", "1->2", "2->0"]
edge_H = [H3[0, 1], H3[1, 2], H3[2, 0]]
ax.bar(range(3), edge_H, color="#4c78a8", width=0.55, label="H along loop edges")
ax.axhline(0.0, color="k", lw=0.8, ls="--")
ax.set_xticks(range(3))
ax.set_xticklabels(edge_labels)
ax.set_ylabel("edge value")
ax.set_title("Proper-time H: gradient edges sum to zero")
ax.text(0.5, 0.92, r"$\sum_{\rm loop} H = 0$", transform=ax.transAxes,
        ha="center", fontsize=11)
ax.grid(axis="y", alpha=0.25)

ax = axes[0, 1]
ax.plot(a, theta3_loop, color="#54a24b", lw=2.2, label=r"$C_3^{\rm circ}$: $3\alpha a$")
ax.plot(a, theta4_loop, color="#f58518", lw=2.2, label=r"$C_4^{\rm circ}$: $4\alpha a$")
ax.axhline(0.0, color="k", lw=0.8, ls="--")
ax.set_xlabel(r"edge amplitude $a$")
ax.set_ylabel("loop holonomy")
ax.set_title(r"U(1) phase connection $\theta=\alpha\lambda$: nonzero holonomy")
ax.legend(frameon=False, loc="upper left")
ax.grid(alpha=0.25)

ax = axes[1, 0]
x = np.arange(6)
labels = ["0->1", "1->2", "2->0", "1->0", "2->1", "0->2"]
H_edges = [H3[0, 1], H3[1, 2], H3[2, 0], H3[1, 0], H3[2, 1], H3[0, 2]]
T_edges = [theta3[0, 1], theta3[1, 2], theta3[2, 0],
           theta3[1, 0], theta3[2, 1], theta3[0, 2]]
width = 0.35
ax.bar(x - width/2, H_edges, width, color="#4c78a8", label="proper-time H")
ax.bar(x + width/2, T_edges, width, color="#54a24b", label=r"phase $\theta$")
ax.axhline(0.0, color="k", lw=0.8, ls="--")
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=30, ha="right")
ax.set_ylabel("edge value")
ax.set_title("Same edges: H is a gradient, theta is a circulation")
ax.legend(frameon=False, loc="upper left")
ax.grid(axis="y", alpha=0.25)

ax = axes[1, 1]
ax.plot(a, np.cos(theta3_loop), color="#54a24b", lw=2.2,
        label=r"$\cos(3\alpha a)$")
ax.plot(a, np.cos(theta4_loop), color="#f58518", lw=2.2,
        label=r"$\cos(4\alpha a)$")
ax.axhline(1.0, color="k", lw=0.8, ls="--")
ax.set_xlabel(r"$\alpha a$")
ax.set_ylabel(r"$\cos\theta$")
ax.set_title("DM.9 phase factor (illustrative, not data)")
ax.legend(frameon=False, loc="lower left")
ax.grid(alpha=0.25)

fig.text(0.5, 0.008,
         r"Proper-time history $H_{ij}=\tau_i-\tau_j$ is a pure gradient; "
         r"the phase connection $\theta=\alpha\lambda$ can carry nonzero loop holonomy. "
         r"Numerical illustration only; $\alpha$ is not fixed.",
         ha="center", fontsize=8.5)

fig.tight_layout(rect=[0, 0.03, 1, 1])
out_png = "相位连接审计.png"
fig.savefig(out_png, dpi=180)
plt.close(fig)

with open("相位连接审计.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["a", "theta3_loop", "theta4_loop", "cos_theta3", "cos_theta4"])
    for ai, t3, t4 in zip(a, theta3_loop, theta4_loop):
        w.writerow([f"{ai:.3f}", f"{t3:.6f}", f"{t4:.6f}",
                    f"{np.cos(t3):.6f}", f"{np.cos(t4):.6f}"])

with open("相位连接审计_边缘.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["edge", "H_proper_time", "theta_phase"])
    for lab, hh, tt in zip(labels, H_edges, T_edges):
        w.writerow([lab, f"{hh:.6f}", f"{tt:.6f}"])

print("H_loop =", H_loop)
print("theta3_loop(a=1) =", theta3_loop[-1])
print("theta4_loop(a=1) =", theta4_loop[-1])
print("H3 =")
print(H3)
print("theta3 =")
print(theta3)
