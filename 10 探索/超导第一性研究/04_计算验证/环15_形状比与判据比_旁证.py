# -*- coding: utf-8 -*-
"""
环 15 · 第 200 轮旁证：形状比 Phi 与判据比 r —— S' 符号的比值判据
链内命题（Spec v27）：
  Phi(T) = w(T)/tanh(1/(2T)),   r(T) = T^2 |w'(T)| / sech^2(1/(2T))
  S'(T) < 0  <=>  Phi(1+r) < 2 r
  w w'' - (w')^2 = tanh(1/(2T)) sech^2(1/(2T)) [Phi(1+r) - 2r] / T^3   （链内恒等式）
  1 <= r  =>  S' < 0          （r>=1 即 w''<=0 段）
本脚本只做"理论行为的显影"：核对恒等式残差、核对比值判据与数值 S' 同号、
检查 r 的实测值域，不反写任何输入。
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei"]
matplotlib.rcParams["axes.unicode_minus"] = False

Tc = 0.3
T_break = 0.7304390
U = np.linspace(0.0, 1.0, 8001)


def sech2(x):
    return 1.0 / np.cosh(x) ** 2


def w_(T):
    return 2.0 * np.trapezoid(U * np.tanh(U / (2.0 * T)), U)


def wp_(T):
    return -(1.0 / T ** 2) * np.trapezoid(U ** 2 * sech2(U / (2.0 * T)), U)


def wpp_alt(T):
    return wp_(T) / T + sech2(1.0 / (2.0 * T)) / T ** 3


def phi_(T):
    return w_(T) / np.tanh(1.0 / (2.0 * T))


def ratio_(T):
    return T ** 2 * abs(wp_(T)) / sech2(1.0 / (2.0 * T))


def shape_(T):
    return w_(T) / abs(wp_(T))


def shape_deriv(T):
    w, w1, w2 = w_(T), wp_(T), wpp_alt(T)
    return (w * w2 - w1 ** 2) / w1 ** 2


def ratio_crit(T):
    ph, r = phi_(T), ratio_(T)
    return ph * (1.0 + r) - 2.0 * r


Ts = np.linspace(0.05, 1.2, 240)

rows = []
for T in Ts:
    w, w1, w2 = w_(T), wp_(T), wpp_alt(T)
    h = np.tanh(1.0 / (2.0 * T))
    S = sech2(1.0 / (2.0 * T))
    lhs = w * w2 - w1 ** 2
    rhs = h * S * ratio_crit(T) / T ** 3
    rows.append(
        dict(T=float(T), phi=float(phi_(T)), r=float(ratio_(T)), crit=float(ratio_crit(T)),
             Sp=float(shape_deriv(T)), lhs=float(lhs), rhs=float(rhs),
             wpp=float(w2))
    )

phys = [q for q in rows if Tc - 1e-9 <= q["T"] <= T_break + 1e-9]

# 恒等式残差（相对）
scale = max(abs(q["lhs"]) for q in rows) or 1.0
id_err = max(abs(q["lhs"] - q["rhs"]) for q in rows) / scale

# 比值判据与 S' 同号核对（排除 |S'| 极小的极小点邻域）
sign_mismatch = [
    1 for q in rows
    if abs(q["Sp"]) > 1e-6 and np.sign(q["Sp"]) != np.sign(q["crit"])
]

# r 值域与 1/3 下界
r_min = min(q["r"] for q in rows)
r_min_T = min(rows, key=lambda q: q["r"])["T"]
r_lower_bound = 1.0 / 3.0

# r>=1 段（w''<=0）里 S' 是否全负
seg = [q for q in rows if q["r"] >= 1.0]
seg_all_neg = all(q["Sp"] < 0 for q in seg)
seg_Tmax = max((q["T"] for q in seg), default=float("nan"))

# 极小点（S' 变号）
cross = []
prev = rows[0]
for q in rows[1:]:
    if np.sign(q["Sp"]) != np.sign(prev["Sp"]):
        cross.append([round(prev["T"], 6), round(q["T"], 6)])
    prev = q

pairs = [(q["T"], q["phi"], q["r"], q["crit"], q["Sp"]) for q in phys]
T_at_Tc = min(rows, key=lambda q: abs(q["T"] - Tc))
T_at_B = min(rows, key=lambda q: abs(q["T"] - T_break))

out = dict(
    identity_rel_err_max=float(id_err),
    sign_mismatch_count=len(sign_mismatch),
    phi_at_Tc=round(T_at_Tc["phi"], 6),
    ratio_at_Tc=round(T_at_Tc["r"], 6),
    crit_at_Tc=round(T_at_Tc["crit"], 6),
    Sp_at_Tc=round(T_at_Tc["Sp"], 6),
    phi_at_Tbreak=round(T_at_B["phi"], 6),
    ratio_at_Tbreak=round(T_at_B["r"], 6),
    crit_at_Tbreak=round(T_at_B["crit"], 6),
    Sp_at_Tbreak=round(T_at_B["Sp"], 6),
    r_min=round(r_min, 6),
    r_min_T=round(r_min_T, 6),
    r_lower_bound=0.3333333,
    r_ge_one_count=len(seg),
    r_ge_one_all_Sp_neg=bool(seg_all_neg),
    r_ge_one_T_max=round(float(seg_Tmax), 6),
    Sp_sign_changes=cross,
    Sp_at_min=round(min(abs(q["Sp"]) for q in rows), 10),
)

print(json.dumps(out, ensure_ascii=False, indent=2))

fig, ax = plt.subplots(1, 3, figsize=(16.5, 4.9))

ax[0].plot([q["T"] for q in rows], [q["phi"] for q in rows], label=r"$\Phi(T)=w/\tanh\frac{1}{2T}$")
ax[0].plot([q["T"] for q in rows], [q["r"] for q in rows], label=r"$r(T)=T^2|w'|/\mathrm{sech}^2\frac{1}{2T}$")
ax[0].axhline(1.0, color="k", ls="--", lw=0.8)
ax[0].axhline(r_lower_bound, color="r", ls=":", lw=1.0)
ax[0].set_xlabel(r"$T$")
ax[0].set_ylabel("比值")
ax[0].set_title("(a) 形状比 $\\Phi$ 与判据比 $r$")
ax[0].legend(fontsize=9, loc="best")
ax[0].grid(alpha=0.3)

ax[1].plot([q["T"] for q in rows], [q["crit"] for q in rows], label=r"$\Phi(1+r)-2r$")
ax[1].axhline(0.0, color="k", ls="--", lw=0.8)
ax[1].set_xlabel(r"$T$")
ax[1].set_title("(b) 比值判据的差量（判 $S'$ 之符号）")
ax[1].legend(fontsize=9)
ax[1].grid(alpha=0.3)

ax[2].plot([q["T"] for q in rows], [q["Sp"] for q in rows], label=r"$S'(T)$")
ax[2].plot([q["T"] for q in rows], [1e-3 * q["crit"] for q in rows],
           label=r"$10^{-3}[\Phi(1+r)-2r]$（同号参照）")
ax[2].axhline(0.0, color="k", ls="--", lw=0.8)
ax[2].set_xlabel(r"$T$")
ax[2].set_title("(c) $S'$ 与判据同号")
ax[2].legend(fontsize=9)
ax[2].grid(alpha=0.3)

plt.tight_layout()
here = os.path.dirname(os.path.abspath(__file__))
plt.savefig(os.path.join(here, "环15_形状比与判据比_旁证.png"), dpi=150)
plt.close(fig)

with open(os.path.join(here, "环15_形状比与判据比_旁证.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print("saved")
