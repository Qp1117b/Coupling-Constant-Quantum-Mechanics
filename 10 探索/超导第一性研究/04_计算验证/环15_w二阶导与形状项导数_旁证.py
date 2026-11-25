# -*- coding: utf-8 -*-
"""
环 15 · 第 198 轮旁证：w 的二阶导数 w'' 与形状项 S=w/|w'| 的导数 S'
链内定义（Spec v25）：
  w(T)      = 2 ∫_0^1 u tanh(u/(2T)) du
  w'(T)     = -(1/T^2) ∫_0^1 u^2 sech^2(u/(2T)) du
  w''(T)    = -(2/T) w'(T) - (1/T^4) ∫_0^1 u^3 sech^2(u/(2T)) tanh(u/(2T)) du
  S(T)      = w / |w'| ,  S'(T) = (w w'' - (w')^2) / (w')^2
本脚本只做"理论行为的显影与外部约束"，不参与建模。
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


def wpp_(T):
    B3 = np.trapezoid(U ** 3 * sech2(U / (2.0 * T)) * np.tanh(U / (2.0 * T)), U)
    return -(2.0 / T) * wp_(T) - (1.0 / T ** 4) * B3


def S_(T):
    return w_(T) / abs(wp_(T))


def Sp_(T):
    w, w1, w2 = w_(T), wp_(T), wpp_(T)
    return (w * w2 - w1 ** 2) / w1 ** 2


Tg = np.linspace(0.30, T_break, 61)
h = 1e-4

rows = []
for T in Tg:
    wv, w1v, w2v = w_(T), wp_(T), wpp_(T)
    w2_fd = (wp_(T + h) - wp_(T - h)) / (2 * h)
    Sv, S1v = S_(T), Sp_(T)
    S1_fd = (S_(T + h) - S_(T - h)) / (2 * h)
    rows.append(dict(
        T=float(T), w=float(wv), wp=float(w1v), wpp=float(w2v),
        wpp_fd=float(w2_fd),
        wpp_rel_err=float(abs(w2v - w2_fd) / max(abs(w2v), 1e-300)),
        S=float(Sv), Sp=float(S1v), Sp_fd=float(S1_fd),
        Sp_rel_err=float(abs(S1v - S1_fd) / max(abs(S1v), 1e-300)),
    ))

wpp_rel_max = max(r["wpp_rel_err"] for r in rows)
Sp_rel_max = max(r["Sp_rel_err"] for r in rows)
wpp_pos_all = all(r["wpp"] > 0 for r in rows)

# S 的极小点：先粗网格找符号变号，再二分细化
def dS(T):
    return Sp_(T)

fine = np.linspace(0.30, T_break, 2000)
vals = np.array([dS(t) for t in fine])
sign_changes = []
for i in range(len(fine) - 1):
    if vals[i] * vals[i + 1] < 0:
        sign_changes.append((float(fine[i]), float(fine[i + 1])))

T_min = None
if sign_changes:
    a, b = sign_changes[0]
    for _ in range(80):
        m = 0.5 * (a + b)
        if dS(a) * dS(m) <= 0:
            b = m
        else:
            a = m
    T_min = 0.5 * (a + b)
S_min = S_(T_min) if T_min is not None else float("nan")

# 用链内闭式在 T_min 附近核对极小：w'≠0 处 S'=0 ⇔ w w'' = (w')^2
w_w2_minus_w1sq = (w_(T_min) * wpp_(T_min) - wp_(T_min) ** 2) if T_min else float("nan")

res = dict(
    n_points=int(len(Tg)),
    T_range=[float(Tg[0]), float(Tg[-1])],
    wpp_rel_err_max=float(wpp_rel_max),
    Sp_rel_err_max=float(Sp_rel_max),
    wpp_positive_all=bool(wpp_pos_all),
    Sp_sign_changes=sign_changes,
    T_at_shape_min=float(T_min) if T_min is not None else None,
    shape_min=float(S_min),
    w_wpp_minus_wp_sq_at_min=float(w_w2_minus_w1sq),
    at_Tc=dict(T=Tc, w=w_(Tc), wp=wp_(Tc), wpp=wpp_(Tc), S=S_(Tc), Sp=Sp_(Tc)),
    at_Tbreak=dict(T=T_break, w=w_(T_break), wp=wp_(T_break), wpp=wpp_(T_break),
                   S=S_(T_break), Sp=Sp_(T_break)),
    rows=rows,
)

outdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(outdir, "环15_w二阶导与形状项导数_旁证.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

# 三面板
fig, ax = plt.subplots(1, 3, figsize=(16.5, 4.6))

ax[0].plot(Tg, [r["wpp"] for r in rows], color="#c0392b", lw=2, label=r"$w''$ 闭式")
ax[0].plot(Tg, [r["wpp_fd"] for r in rows], "o", ms=3, mfc="none", color="#2c3e50",
           label=r"$w'$ 中心差分")
ax[0].axhline(0.0, color="gray", lw=0.8, ls=":")
ax[0].set_xlabel("T")
ax[0].set_ylabel(r"$w''(T)$")
ax[0].set_title("(a) 二阶导：闭式与差分")
ax[0].legend(fontsize=9)

ax[1].semilogy(Tg, [max(r["wpp_rel_err"], 1e-18) for r in rows], color="#8e44ad", lw=1.8,
               label=r"$w''$ 相对偏差")
ax[1].semilogy(Tg, [max(r["Sp_rel_err"], 1e-18) for r in rows], color="#16a085", lw=1.8,
               ls="--", label=r"$S'$ 相对偏差")
ax[1].set_xlabel("T")
ax[1].set_ylabel("相对偏差")
ax[1].set_title("(b) 闭式 vs 差分（对数轴）")
ax[1].legend(fontsize=9)

ax[2].plot(Tg, [r["S"] for r in rows], color="#2980b9", lw=2, label=r"$S=w/|w'|$")
ax3 = ax[2].twinx()
ax3.plot(Tg, [r["Sp"] for r in rows], color="#d35400", lw=1.6, label=r"$S'$")
ax3.axhline(0.0, color="gray", lw=0.8, ls=":")
if T_min is not None:
    ax[2].axvline(T_min, color="#7f8c8d", lw=1.0, ls="--")
    ax[2].annotate(rf"$T\approx{T_min:.4f}$", xy=(T_min, S_min),
                   xytext=(T_min + 0.06, S_min + 0.03), fontsize=9,
                   arrowprops=dict(arrowstyle="->", color="#7f8c8d", lw=0.8))
ax[2].set_xlabel("T")
ax[2].set_ylabel(r"$S$")
ax3.set_ylabel(r"$S'$")
ax[2].set_title("(c) 形状项与其导数")
h1, l1 = ax[2].get_legend_handles_labels()
h2, l2 = ax3.get_legend_handles_labels()
ax[2].legend(h1 + h2, l1 + l2, fontsize=9, loc="lower right")

fig.tight_layout()
fig.savefig(os.path.join(outdir, "环15_w二阶导与形状项导数_旁证.png"), dpi=150)
plt.close(fig)

print(json.dumps({k: v for k, v in res.items() if k != "rows"}, ensure_ascii=False, indent=1))
