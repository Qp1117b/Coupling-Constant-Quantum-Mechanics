# -*- coding: utf-8 -*-
"""环 15 / 审-6 重开（第 187 轮）：配对阈值与粗粒化指数的两条写法等价（$t\\to x_\\ast$ 接口）

登记口径（不新引参数）：
- (15L.7)：$p_{\\rm pair}^{\\rm thr}=p_c/(1-y)^m$，$t=\\ln p_c/\\ln p_{\\rm pair}^{\\rm thr}$
- (15L.4)：$t=1+m\\ln(1-y)/\\ln p_{\\rm pair}$
- R-158 ⑥：$x_\\ast=\\bar F_\\nu^{-1}(p_c^{1/t})$

本脚本只做三件事（无拟合）：
1. 两条写法在同步点同值（$p_{\\rm pair}=p_{\\rm pair}^{\\rm thr}$），在同步点之外不同值（说明为何交接表必须写 $p_c^{1/t}$）；
2. 结构化天花板 $y_{\\deg}=1-p_c^{1/m}$：$y>y_{\\deg}$ 时 $p_{\\rm pair}^{\\rm thr}>1$，任何配对阈值都无法补回锁损失 ⇒ 同步不可能；
3. $y(T_{\\rm sync})$ 与 $y_{\\deg}$ 的余量（$m=1,2$），以及 $y$ 触及 $y_{\\deg}$ 的温度。
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PC = 0.592746
NU = 9.0
TC = 0.3
XC = 4.5
UPS0 = 2.0 * 3.207211 / np.pi ** 2


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
p_pair = lambda T: 1.0 - chi2.cdf(XC * WC / w(T), NU)
y_of = lambda T: 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0 * w(T)) / (2.0 * T))
t_of = lambda T, m: 1.0 + m * np.log(1.0 - y_of(T)) / np.log(p_pair(T))
pThr = lambda T, m: PC / (1.0 - y_of(T)) ** m

K_BREAK = 2.0 * np.log(2.0 * np.pi) / np.pi ** 2
T_BREAK = float(brentq(lambda T: UPS0 * w(T) / T - K_BREAK, TC, 2.0, xtol=1e-14))

out = {"w_Tc": WC, "p_at_Tc": p_pair(TC), "Upsilon0_wp": UPS0, "T_break": T_BREAK}

# ---- 1. 结构化天花板 y_deg = 1 - p_c^(1/m) ----
for m in (1, 2, 3, 8):
    ydeg = 1.0 - PC ** (1.0 / m)
    out[f"y_deg_m{m}"] = float(ydeg)
    try:
        Tdeg = float(brentq(lambda T: y_of(T) - ydeg, TC, T_BREAK - 1e-6, xtol=1e-14))
    except ValueError:
        Tdeg = None
    out[f"T_ydeg_m{m}"] = Tdeg
    out[f"pThr_at_Tc_m{m}"] = float(pThr(TC, m))

# ---- 2. 同步点：两条写法同值 ----
Tsync = {}
for m in (1, 2):
    Tsync[m] = float(brentq(lambda T: p_pair(T) * (1.0 - y_of(T)) ** m - PC, TC, T_BREAK - 1e-6, xtol=1e-14))
    yv, pv, tv = y_of(Tsync[m]), p_pair(Tsync[m]), t_of(Tsync[m], m)
    out[f"T_sync_m{m}"] = Tsync[m]
    out[f"y_at_sync_m{m}"] = yv
    out[f"p_pair_at_sync_m{m}"] = pv
    out[f"p_thr_at_sync_m{m}"] = float(pThr(Tsync[m], m))
    out[f"p_c_rpow_at_sync_m{m}"] = float(PC ** (1.0 / tv))
    out[f"two_writings_diff_m{m}"] = abs(float(PC ** (1.0 / tv)) - float(pThr(Tsync[m], m)))
    out[f"p_sync_check_m{m}"] = pv * (1.0 - yv) ** m
    out[f"y_margin_to_ydeg_m{m}"] = float(1.0 - PC ** (1.0 / m)) - yv

# 同步点之外（T=Tc）两写法不同值：T_c 的 "阈值写法" 只是一条曲线，不是阈值
out["T_tc_mismatch_m1"] = [float(PC ** (1.0 / t_of(TC, 1))), float(pThr(TC, 1))]
out["T_tc_mismatch_m2"] = [float(PC ** (1.0 / t_of(TC, 2))), float(pThr(TC, 2))]

# ---- 3. 图 ----
fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
Ts = np.linspace(TC, T_BREAK - 1e-4, 400)

ax = axes[0]
ax.plot(Ts, [y_of(float(T)) for T in Ts], label="$y(T)$（工作点）")
ax.axhline(1.0 - PC, color="C3", ls="--", lw=1.0, label=r"$y_{\deg}$, $m{=}1$ = %.4f" % (1.0 - PC))
ax.axhline(1.0 - np.sqrt(PC), color="C1", ls=":", lw=1.2, label=r"$y_{\deg}$, $m{=}2$ = %.4f" % (1.0 - np.sqrt(PC)))
for m, c in ((1, "C0"), (2, "C2")):
    ax.axvline(Tsync[m], color=c, lw=0.8)
ax.set(xlabel=r"$T/\omega_D$", ylabel="$y$", title="(a) 逸度与结构化天花板（竖线=同步点）")
ax.legend(fontsize=7)

ax = axes[1]
ax.plot(Ts, [p_pair(float(T)) for T in Ts], label="$p_{\\rm pair}(T)$（实际配对尾）")
ax.plot(Ts, [pThr(float(T), 1) for T in Ts], "--", label="$p_{\\rm pair}^{\\rm thr}=p_c/(1-y)$（$m{=}1$）")
ax.plot(Ts, [pThr(float(T), 2) for T in Ts], ":", label="$p_{\\rm pair}^{\\rm thr}=p_c/(1-y)^2$（$m{=}2$）")
ax.axhline(PC, color="k", ls=":", lw=1.0)
ax.set(xlabel=r"$T/\omega_d$".replace("omega_d", "omega_D"), ylabel="概率",
       title="(b) 阈值曲线在同步点与 $p_{\\rm pair}$ 相交；$p_{\\rm pair}^{\\rm thr}>1$ 处同步不可能")
ax.legend(fontsize=7)
ax.set_ylim(0.4, 1.05)

fig.tight_layout()
fig.savefig("环15配对阈值与t两写法.png", dpi=150)
with open("环15配对阈值与t两写法.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
