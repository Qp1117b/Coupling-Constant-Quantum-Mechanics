# -*- coding: utf-8 -*-
"""
环 15 · 第 199 轮旁证：w'' 的端点闭式与条件式正性判据
链内命题（Spec v26）：
  w''(T) = w'(T)/T + sech^2(1/(2T))/T^3                      （端点闭式，与 v25 的积分式同值）
  w''>0  <=>  T^2 |w'(T)| < sech^2(1/(2T))
本脚本只做"理论行为的显影与外部约束"：核对两式同值、找出判据失效的温区。
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


def wpp_C(T):
    B3 = np.trapezoid(U ** 3 * sech2(U / (2.0 * T)) * np.tanh(U / (2.0 * T)), U)
    return -(2.0 / T) * wp_(T) - (1.0 / T ** 4) * B3


def wpp_alt(T):
    return wp_(T) / T + sech2(1.0 / (2.0 * T)) / T ** 3


def ratio(T):
    return T ** 2 * abs(wp_(T)) / sech2(1.0 / (2.0 * T))


def S_(T):
    return w_(T) / abs(wp_(T))


def Sp_(T):
    wv, w1, w2 = w_(T), wp_(T), wpp_alt(T)
    return (wv * w2 - w1 ** 2) / w1 ** 2


# (1) 两式同值（物理窗口）
Tg = np.linspace(0.30, T_break, 61)
rows = []
for T in Tg:
    wc, wa = wpp_C(T), wpp_alt(T)
    rows.append(dict(T=float(T), wpp_C=float(wc), wpp_alt=float(wa),
                     rel=float(abs(wa - wc) / max(abs(wc), 1e-300))))

alt_rel_max = max(r["rel"] for r in rows)

# (2) 判据全域扫描：r(T) = T^2|w'| / sech^2(1/(2T))
Ts = np.linspace(0.02, 1.20, 1200)
rs = np.array([ratio(t) for t in Ts])
cross = []
for i in range(len(Ts) - 1):
    if (rs[i] - 1.0) * (rs[i + 1] - 1.0) < 0:
        a, b = Ts[i], Ts[i + 1]
        for _ in range(80):
            m = 0.5 * (a + b)
            if (ratio(a) - 1.0) * (ratio(m) - 1.0) <= 0:
                b = m
            else:
                a = m
        cross.append(float(0.5 * (a + b)))

# 判据成立的温区（r<1）
mask = rs < 1.0
hold_ranges = []
if mask.any():
    start = None
    for i, ok in enumerate(mask):
        if ok and start is None:
            start = Ts[i]
        if (not ok) and start is not None:
            hold_ranges.append([float(start), float(Ts[i - 1])])
            start = None
    if start is not None:
        hold_ranges.append([float(start), float(Ts[-1])])

res = dict(
    alt_vs_C_rel_err_max=float(alt_rel_max),
    ratio_min=float(rs.min()), ratio_max=float(rs.max()),
    ratio_at_Tc=float(ratio(Tc)), ratio_at_Tbreak=float(ratio(T_break)),
    ratio_one_crossings=[float(c) for c in cross],
    criterion_holds_ranges=hold_ranges,
    wpp_at_Tc=float(wpp_alt(Tc)), wpp_at_Tbreak=float(wpp_alt(T_break)),
    wpp_sign_at_0p1=float(wpp_alt(0.1)), wpp_sign_at_0p2=float(wpp_alt(0.2)),
    wpp_sign_at_0p25=float(wpp_alt(0.25)),
    S_at_Tc=float(S_(Tc)), Sp_at_Tc=float(Sp_(Tc)),
    S_min=float(S_(0.343858)), Sp_at_min=float(Sp_(0.343858)),
    rows=rows,
)

outdir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(outdir, "环15_w二阶导端点闭式_旁证.json"), "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=1)

fig, ax = plt.subplots(1, 3, figsize=(16.5, 4.6))

ax[0].plot(Tg, [r["wpp_C"] for r in rows], color="#c0392b", lw=2, label="积分式 (v25)")
ax[0].plot(Tg, [r["wpp_alt"] for r in rows], "o", ms=3, mfc="none", color="#2c3e50",
           label="端点闭式 (v26)")
ax[0].set_xlabel("T"); ax[0].set_ylabel(r"$w''(T)$")
ax[0].set_title("(a) 两式同值（物理窗口）"); ax[0].legend(fontsize=9)

ax[1].semilogy(Ts, rs, color="#8e44ad", lw=1.8, label=r"$r(T)=T^2|w'|/\mathrm{sech}^2\frac{1}{2T}$")
ax[1].axhline(1.0, color="#c0392b", lw=1.0, ls="--", label=r"$r=1$（$w''=0$）")
for c in cross:
    ax[1].axvline(c, color="#7f8c8d", lw=0.9, ls=":")
ax[1].set_xlabel("T"); ax[1].set_ylabel("r")
ax[1].set_title("(b) 正性判据的全域失效/成立")
ax[1].legend(fontsize=8, loc="lower right")

ax[2].plot(Tg, [S_(t) for t in Tg], color="#2980b9", lw=2, label=r"$S=w/|w'|$")
ax2 = ax[2].twinx()
ax2.plot(Tg, [Sp_(t) for t in Tg], color="#d35400", lw=1.5, label=r"$S'$")
ax2.axhline(0.0, color="gray", lw=0.8, ls=":")
ax[2].axvline(0.343858, color="#7f8c8d", lw=1.0, ls="--")
ax[2].set_xlabel("T"); ax[2].set_ylabel("S"); ax2.set_ylabel("S'")
ax[2].set_title("(c) 形状项与其导数（判据numerator）")
h1, l1 = ax[2].get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax[2].legend(h1 + h2, l1 + l2, fontsize=9, loc="lower right")

fig.tight_layout()
fig.savefig(os.path.join(outdir, "环15_w二阶导端点闭式_旁证.png"), dpi=150)
plt.close(fig)

print(json.dumps({k: v for k, v in res.items() if k != "rows"}, ensure_ascii=False, indent=1))
