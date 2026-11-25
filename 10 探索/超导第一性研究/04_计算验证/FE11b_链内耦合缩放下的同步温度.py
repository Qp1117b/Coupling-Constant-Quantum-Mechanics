# -*- coding: utf-8 -*-
"""
FE11b（候选·未落地）：链内耦合缩放扫描——秩判据 vs 逸度 vs 同步温度（第 168 轮）
检验对象：把 FE11 的教科书对照（BCS）换成环 15 自己的模型后，"秩即判据"在哪一层被否证。

链内机制（不改方程，只扫一个已存在的参数）：
  锁定概率   p_sync(t,m) = p_pair(t) * (1 - y(t))^m
  逸度       y(t)        = 2*pi*exp(-E_c/t)
  E_c        = pi^2 * Upsilon_0 / 2（刚度幅度，∝ 配对耦合）
  耦合缩放   lambda:  E_c -> lambda*E_c，其余不动

三层对照：
  (i)   T_sync(m,lambda)：解 p_sync = p_c，看下游量对 lambda 的**实际**灵敏度；
  (ii)  y(T_c,lambda)：固定 T，看逸度对 lambda 的**指数**灵敏度；
  (iii) 秩：rank(lambda*T)=rank(T)=7，lambda 无关。

局限（明写）：环 15 的 T_c 在此参数化里是标定输入（由 Upsilon(T_c)=2T_c/(pi*w) 反解 Upsilon_0），
故本扫描不重解 T_c 本身；T_c 的重解须在环 15 方程层做，属后续。

仅用 numpy + scipy + matplotlib。
运行：python "FE11b_链内耦合缩放下的同步温度.py"
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))

PC = 0.592746
NU = 9.0
TU = 1.3
TC = 0.3
XC = 4.5
G = 0.622281
BETA_K = 0.89294
RANK_222 = 7


def w(x, n=20001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
Phi = lambda p: ((p - PC) / (1 - PC)) ** TU
phic = 1.0 - chi2.cdf(XC, NU)
KAP = G * Phi(phic)
UPS0 = 2.0 * TC / (np.pi * WC * KAP)
EC = np.pi ** 2 * UPS0 / 2.0

p_pair = lambda t: 1.0 - chi2.cdf(XC * WC / w(t), NU)


def y_of(t, lam=1.0):
    return 0.0 if t <= 0 else 2.0 * np.pi * np.exp(-lam * EC / t)


def p_sync(t, m, lam=1.0):
    return p_pair(t) * (1.0 - y_of(t, lam)) ** m


def solve_tsync(m, lam):
    f = lambda t: p_sync(t, m, lam) - PC
    return float(brentq(f, 0.02, 1.30, xtol=1e-13))


LAMS = np.linspace(0.60, 1.60, 121)
TS1 = np.array([solve_tsync(1, l) for l in LAMS])
TS2 = np.array([solve_tsync(2, l) for l in LAMS])
TSTAR = float(brentq(lambda t: p_pair(t) - PC, 0.02, 1.4, xtol=1e-13))
YY = np.array([y_of(TC, l) for l in LAMS])

base1 = solve_tsync(1, 1.0)
base2 = solve_tsync(2, 1.0)
ratio1 = TS1 / base1
y_ratio = YY / y_of(TC, 1.0)

sel = [0.60, 0.70, 0.85, 1.00, 1.15, 1.30, 1.60]
rows = [{"lambda": l,
         "T_sync_m1": solve_tsync(1, l),
         "T_sync_m2": solve_tsync(2, l),
         "ratio_Tsync_m1": solve_tsync(1, l) / base1,
         "y_at_Tc": y_of(TC, l),
         "ratio_y": y_of(TC, l) / y_of(TC, 1.0)} for l in sel]

dl = 0.02
elast = (np.log(solve_tsync(1, 1.0 + dl)) - np.log(solve_tsync(1, 1.0 - dl))) / (2 * dl)
elast_y = (np.log(y_of(TC, 1.0 + dl)) - np.log(y_of(TC, 1.0 - dl))) / (2 * dl)

fig, ax = plt.subplots(1, 3, figsize=(15.2, 4.6))

ax[0].plot(LAMS, TS1, "-", color="#1f77b4", lw=2, label=r"$T_{\rm sync}(m{=}1)$")
ax[0].plot(LAMS, TS2, "--", color="#ff7f0e", lw=2, label=r"$T_{\rm sync}(m{=}2)$")
ax[0].axhline(TSTAR, color="k", ls=":", lw=1.4, label=r"$T_*$（$\lambda$ 无关）")
ax[0].axvline(1.0, color="0.6", ls=":", lw=1)
ax[0].plot([1.0], [base1], "o", color="#1f77b4", ms=5)
ax[0].plot([1.0], [base2], "o", color="#ff7f0e", ms=5)
ax[0].annotate(f"{base1:.4f}", (1.0, base1), textcoords="offset points",
               xytext=(6, 8), fontsize=8)
ax[0].set(xlabel=r"耦合缩放 $\lambda$（$E_c\to\lambda E_c$）",
          ylabel=r"$T_{\rm sync}$（单位 $\omega_D$）",
          title=r"(a) 下游量 $T_{\rm sync}$：仅 1.23 倍，近饱和")
ax[0].legend(fontsize=8)
ax[0].grid(alpha=0.25)

ax[1].semilogy(LAMS, YY, "-", color="#2ca02c", lw=2, label=r"$y(T_c;\lambda)=2\pi e^{-\lambda E_c/T_c}$")
ax[1].axvline(1.0, color="0.6", ls=":", lw=1)
ax[1].set(xlabel=r"$\lambda$", ylabel=r"$y$（对数）",
          title=r"(b) 逸度 $y$：4.6 个数量级（指数依赖）")
ax[1].legend(fontsize=8)
ax[1].grid(alpha=0.25, which="both")

ax[2].semilogy(LAMS, y_ratio, "-", color="#2ca02c", lw=2, label=r"$y(\lambda)/y(1)$")
ax[2].semilogy(LAMS, ratio1, "-", color="#1f77b4", lw=2, label=r"$T_{\rm sync}(\lambda)/T_{\rm sync}(1)$")
ax[2].semilogy([LAMS.min(), LAMS.max()], [1.0, 1.0], "--", color="#d62728", lw=1.8,
               label="秩判据预测（常数 1）")
ax[2].set(xlabel=r"$\lambda$", ylabel="归比值（对数）",
          title="(c) 秩与 $T_{\\rm sync}$ 数值接近，但那不是它该量的东西")
ax[2].legend(fontsize=8)
ax[2].grid(alpha=0.25, which="both")

fig.suptitle("FE11b：链内三层对照——秩恒为 7；$y$ 指数变 4.6 量级；$T_{\\rm sync}$ 仅 1.23 倍", fontsize=12)
fig.tight_layout()
out_png = os.path.join(HERE, "FE11b_链内耦合缩放下的同步温度.png")
fig.savefig(out_png, dpi=150)
plt.close(fig)

data = {
    "candidate": "FE11b",
    "note": "环 15 模型内扫描；不改方程/Spec；T_c 为标定输入，故只扫 y/T_sync 层",
    "workpoint": {"lambda": 1.0, "T_sync_m1": base1, "T_sync_m2": base2,
                  "registered": [0.627385, 0.609230],
                  "matches_registered": bool(abs(base1 - 0.627385) < 5e-4
                                             and abs(base2 - 0.609230) < 5e-4)},
    "E_c": float(EC), "T_star": TSTAR,
    "lambda_span": [float(LAMS.min()), float(LAMS.max())],
    "table": rows,
    "Tsync_ratio_span": float(ratio1.max() / ratio1.min()),
    "Tsync_ratio_span_decades": float(np.log10(ratio1.max() / ratio1.min())),
    "y_ratio_span_decades": float(np.log10(y_ratio.max() / y_ratio.min())),
    "elasticity_dlnTsync_dlambda_at_1": float(elast),
    "elasticity_dln_y_dlambda_at_1": float(elast_y),
    "rank_222": RANK_222,
    "verdict_levels": {
        "y_layer": "秩恒 7 与 y 的指数依赖（每单位 lambda 约 10.69 的指数）不可兼容 -> 秩不可承载 y",
        "Tsync_layer": "T_sync 已近饱和于 T_*，对 lambda 仅 1.23 倍（弹性 0.17）-> 数值上秩与它接近，属语义不同而数值偶然接近",
        "tc_layer": "T_c 在此参数化中为标定输入，未参与扫描 -> 本卡不断言 T_c",
    },
}
out_json = os.path.join(HERE, "FE11b_链内耦合缩放下的同步温度.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))
print("图片:", out_png)
