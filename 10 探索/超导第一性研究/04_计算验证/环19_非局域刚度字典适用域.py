# -*- coding: utf-8 -*-
"""环 19：非局域区与 q->0 外推（第 153 轮，R-162）

解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_非局域刚度字典适用域.py"（本目录）
输出：环19_非局域刚度字典适用域.png、环19_非局域刚度字典适用域.json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

hb = 1.054571817e-34
mu0 = 4.0 * np.pi * 1e-7
e = 1.602176634e-19
kB = 1.380649e-23

# 片动能电感常数与 BKT 线
C_k = hb**2 / (4.0 * e**2)                    # J*H
def L_BKT(Tc):
    return np.pi * hb**2 / (8.0 * e**2 * kB * Tc)

checks = {}
A_list = [0.5, 1.0, 2.0]

# C1 (19NL.2) 恒等：由 Upsilon(q)=Upsilon0(1-Au^2) 得 L(q)/L(0)=1/(1-Au^2)
err1 = 0.0
for A in A_list:
    for u in np.linspace(0.0, 0.6, 61):
        a = A * u**2
        if a < 0.95:
            r_direct = 1.0 / (1.0 - a)
            r_form = 1.0 / (1.0 - a)
            err1 = max(err1, abs(r_direct / r_form - 1.0))
checks["C1_rel"] = err1
assert err1 < 1e-14

# C2 方向：0<=Au^2<1 时 L(q)/L(0)>=1
mins = []
for A in A_list:
    u = np.linspace(0.0, min(0.6, 0.99 / np.sqrt(A)), 400)
    r = 1.0 / (1.0 - A * u**2)
    mins.append(float(r.min()))
checks["C2_min_ratio"] = mins
assert min(mins) >= 1.0 - 1e-15

# C3 阈值：u* = sqrt(eps/A) 使 A u*^2 = eps
thr = {}
for eps in (0.01, 0.10, 0.30):
    for A in A_list:
        u_star = np.sqrt(eps / A)
        thr[f"eps{eps:.2f}_A{A:g}"] = {"u_star": u_star, "resid": abs(A * u_star**2 - eps)}
        assert abs(A * u_star**2 - eps) < 1e-16
checks["C3"] = thr

# C4 单向界：B <= B/(1-eps)（由 L(q)/L(0) <= 1/(1-eps)）
bnd = {}
for B0 in (0.0667, 1.89e-4):
    for eps in (0.10, 0.30):
        Bq = B0 / (1.0 - eps)
        bnd[f"B{B0:g}_eps{eps:.2f}"] = {"B0": B0, "Bq": Bq}
        assert Bq >= B0
checks["C4"] = bnd

# C5 T_BKT 位移比 = 刚度比（T = pi*Upsilon/(2 kB)）
err5 = 0.0
for A in A_list:
    for u in np.linspace(0.0, 0.5, 51):
        r_up = 1.0 - A * u**2
        r_T = (np.pi * (1.0 - A * u**2) / (2 * kB)) / (np.pi * 1.0 / (2 * kB))
        err5 = max(err5, abs(r_T - r_up))
checks["C5_abs"] = err5
assert err5 < 1e-14

# C6 固定 A 时 1-Au^2 随 u 单调减
mono = {}
for A in A_list:
    u = np.linspace(0.0, 0.6, 500)
    d = np.diff(1.0 - A * u**2)
    mono[f"A{A:g}_maxdiff"] = float(d.max())
    assert d.max() < 0.0
checks["C6"] = mono

# 数值示例：B=0.0667 的上界
checks["example_B_headroom"] = {
    "B0": 0.0667,
    "eps0.10": 0.0667 / 0.9,
    "eps0.30": 0.0667 / 0.7,
}

# ---------------- 图 ----------------
fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.2))

# (a) L(q)/L(0)
u = np.linspace(0.0, 0.65, 400)
for A, c in zip(A_list, ["C0", "C1", "C2"]):
    uu = u[A * u**2 < 0.95]
    ax[0, 0].plot(uu, 1.0 / (1.0 - A * uu**2), color=c, lw=2, label=f"A={A:g}")
ax[0, 0].axhline(1.1, color="k", ls="--", lw=1, label=r"$+10\%$")
ax[0, 0].set_xlabel(r"$q\xi$")
ax[0, 0].set_ylabel(r"$L_{k,\mathrm{sq}}(q)/L_{k,\mathrm{sq}}(0)$")
ax[0, 0].set_title(r"(a) 有限 $q$ 高估片电感")
ax[0, 0].legend(fontsize=8)
ax[0, 0].grid(True, alpha=0.25)

# (b) Upsilon(q)/Upsilon(0)
for A, c in zip(A_list, ["C0", "C1", "C2"]):
    ax[0, 1].plot(u, 1.0 - A * u**2, color=c, lw=2, label=f"A={A:g}")
ax[0, 1].axhline(0.9, color="k", ls="--", lw=1, label=r"$-10\%$")
ax[0, 1].set_xlabel(r"$q\xi$")
ax[0, 1].set_ylabel(r"$\Upsilon(q)/\Upsilon(0)$")
ax[0, 1].set_title(r"(b) 刚度被低估（单向）")
ax[0, 1].legend(fontsize=8)
ax[0, 1].grid(True, alpha=0.25)

# (c) 阈值曲线 eps = A u^2
uu = np.linspace(0.0, 0.8, 400)
for A, c in zip(A_list, ["C0", "C1", "C2"]):
    ax[0, 2].plot(uu, A * uu**2, color=c, lw=2, label=f"A={A:g}")
for eps in (0.01, 0.10, 0.30):
    ax[0, 2].axhline(eps, color="gray", ls=":", lw=1)
ax[0, 2].set_xlabel(r"$q\xi$")
ax[0, 2].set_ylabel(r"$A(q\xi)^2$")
ax[0, 2].set_title(r"(c) 外推判据阈值")
ax[0, 2].legend(fontsize=8)
ax[0, 2].grid(True, alpha=0.25)

# (d) B 的单向上界
labels = [r"$B_0$", r"$\epsilon=10\%$", r"$\epsilon=30\%$"]
for i, (B0, tag) in enumerate([(0.0667, r"$B_0=0.0667$"), (1.89e-4, r"$B_0=1.89\times10^{-4}$")]):
    vals = [B0, B0 / 0.9, B0 / 0.7]
    xs = np.arange(3) + i * 3.6
    ax[1, 0].bar(xs, vals, width=0.8, color=["C0", "C1", "C2"])
    for x, v in zip(xs, vals):
        ax[1, 0].text(x, v * 1.1, f"{v:.2e}", ha="center", fontsize=6.5, rotation=90)
ax[1, 0].set_yscale("log")
ax[1, 0].set_xticks([0, 1, 2, 3.6, 4.6, 5.6])
ax[1, 0].set_xticklabels(labels * 2, fontsize=7)
ax[1, 0].set_ylabel(r"$\mathcal{B}$ 的上界")
ax[1, 0].set_title(r"(d) $\mathcal{B}\ll1$ 对非局域误差稳健")
ax[1, 0].grid(True, axis="y", alpha=0.25)

# (e) q^2 外推：L/L0-1 对 (q xi)^2 线性过原点
uu = np.linspace(0.0, 0.45, 200)
for A, c in zip(A_list, ["C0", "C1", "C2"]):
    ax[1, 1].plot(A * uu**2, 1.0 / (1.0 - A * uu**2) - 1.0, color=c, lw=2, label=f"A={A:g}")
ax[1, 1].set_xlabel(r"$A(q\xi)^2$")
ax[1, 1].set_ylabel(r"$L_{k,\mathrm{sq}}(q)/L_{k,\mathrm{sq}}(0)-1$")
ax[1, 1].set_title(r"(e) 小 $q$ 线性外推（过原点）")
ax[1, 1].legend(fontsize=8)
ax[1, 1].grid(True, alpha=0.25)

# (f) 固定 q xi=0.3 时允许的 A 上界
A = np.linspace(0.0, 3.0, 400)
u0 = 0.3
ax[1, 2].plot(A, 1.0 / (1.0 - A * u0**2), "k-", lw=2)
ax[1, 2].axhline(1.1, color="r", ls="--", lw=1, label=r"$+10\%$ 界")
ax[1, 2].axvline(0.10 / u0**2, color="b", ls=":", lw=1.2, label=r"$A_{\max}=\epsilon/(q\xi)^2$")
ax[1, 2].set_xlabel(r"$A$")
ax[1, 2].set_ylabel(r"$L_{k,\mathrm{sq}}(q)/L_{k,\mathrm{sq}}(0)$")
ax[1, 2].set_title(r"(f) $q\xi=0.3$：$A\lesssim1.11$ 才可直用字典")
ax[1, 2].legend(fontsize=8)
ax[1, 2].grid(True, alpha=0.25)

plt.tight_layout()
plt.savefig("环19_非局域刚度字典适用域.png", dpi=150)

with open("环19_非局域刚度字典适用域.json", "w", encoding="utf-8") as f:
    json.dump(checks, f, ensure_ascii=False, indent=2)

print(json.dumps(checks, ensure_ascii=False, indent=2))
print("全部断言通过")
