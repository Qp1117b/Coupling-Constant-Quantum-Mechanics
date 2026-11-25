# -*- coding: utf-8 -*-
"""环 15 / 审-6 重开（第 186 轮）：粗粒化指数 t 对逸度 y 的方向与下界，及 epsilon_nu 交接

登记口径（不新引参数）：
- R-158 ④：t(T) = 1 + m*ln(1-y(T))/ln p_pair(T)
- (15L.3)：y(T) = 2*pi*exp(-E_c/(k_B T))，E_c = (pi^2/2)*Upsilon，Upsilon = Upsilon_0*w(T)（185 轮）
- 下游：x_* = Fbar_nu^{-1}(p_c^{1/t})，eps_nu = 2 x_* f_nu(x_*)/pbar_nu(x_*)，r ∝ 1/eps_nu

本脚本只做三件事：
1. t(T) 在 T 上严格增（与 y 同向）——数值侧核对 186 轮定理 TargetPropTEffMMono；
2. t(T) >= 1 且等号只在 y=0——核对 TargetPropTEffMGeOne；
3. 由新 t(T_c) 重算 x_*、eps_nu 交接表，给出 r 的相对移动（r 的结构不变，只随 eps_nu 反比移动）。
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
TU = 1.3
TC = 0.3
XC = 4.5
BETA_K = 0.89294
UPS0_WP = 2.0 * 3.207211 / np.pi ** 2      # 185 轮工作点支 0.6499168


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
phic = 1.0 - chi2.cdf(XC, NU)
p_pair = lambda t: 1.0 - chi2.cdf(XC * WC / w(t), NU)
y_of = lambda t: 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0_WP * w(t)) / (2.0 * t))
t_of = lambda T, m: 1.0 + m * np.log(1.0 - y_of(T)) / np.log(p_pair(T))

K_BREAK = 2.0 * np.log(2.0 * np.pi) / np.pi ** 2
T_BREAK = float(brentq(lambda T: UPS0_WP * w(T) / T - K_BREAK, TC, 2.0, xtol=1e-14))

out = {"w_Tc": WC, "p_at_Tc": phic, "Upsilon0_wp": UPS0_WP, "T_break": T_BREAK}

# ---- 1. 方向：t(T) 对 T（随 y 增）——数值核对 TargetPropTEffMMono ----
Ts = np.linspace(TC, T_BREAK - 1e-4, 400)
rows = []
for T in Ts:
    rows.append({"T": float(T), "w": w(float(T)), "y": y_of(float(T)),
                 "p_pair": p_pair(float(T)), "t_m1": t_of(float(T), 1), "t_m2": t_of(float(T), 2)})
t1 = np.array([r["t_m1"] for r in rows])
t2 = np.array([r["t_m2"] for r in rows])
out["t_m1_strict_increasing"] = bool(np.all(np.diff(t1) > 0))
out["t_m2_strict_increasing"] = bool(np.all(np.diff(t2) > 0))
out["t_min_over_domain_m1"] = float(t1.min())
out["t_min_over_domain_m2"] = float(t2.min())
out["t_at_Tc_m1"] = t_of(TC, 1)
out["t_at_Tc_m2"] = t_of(TC, 2)
out["t_at_domain_end_m1"] = float(t1[-1])
out["t_at_domain_end_m2"] = float(t2[-1])

# ---- 2. 下界：t>=1（y in [0,1)），等号只在 y=0（T=0 侧，w(0)=1、y→0） ----
out["t_ge_one_all"] = bool(np.all(t1 >= 1.0 - 1e-15) and np.all(t2 >= 1.0 - 1e-15))
T0 = 1e-6
out["t_at_T0_m1"] = t_of(T0, 1)
out["y_at_T0"] = y_of(T0)

# ---- 3. epsilon_nu 交接：x_* 由 p_c^{1/t} 定，eps_nu = 2x f/pbar ----
def x_star(nu, t):
    q = PC ** (1.0 / t)                      # = pbar_nu(x_*)
    return float(brentq(lambda x: chi2.sf(x, nu) - q, 1e-8, 200.0, xtol=1e-14))


def eps_nu(nu, t):
    x = x_star(nu, t)
    f = float(chi2.pdf(x, nu))
    pb = float(chi2.sf(x, nu))
    return x, 2.0 * x * f / pb


cases = []
for nu in (9, 8):
    for lab, t in (("t=1", 1.0), ("t(Tc),m=1", t_of(TC, 1)), ("t(Tc),m=2", t_of(TC, 2)),
                   ("t_ub,m=1 (15L.6)", 1.0509), ("t_ub,m=2 (15L.6)", 1.1072)):
        x, e = eps_nu(nu, t)
        cases.append({"nu": nu, "case": lab, "t": float(t), "x_star": x, "eps_nu": e})
out["cases"] = cases

# r ∝ 1/eps_nu：相对基线（nu=9,t=1 登记值 eps=2.5929；nu=8,t=1 = 2.4293）
base9 = [c for c in cases if c["nu"] == 9 and c["case"] == "t=1"][0]["eps_nu"]
base8 = [c for c in cases if c["nu"] == 8 and c["case"] == "t=1"][0]["eps_nu"]
out["eps_nu_baseline_nu9_t1"] = base9
out["eps_nu_baseline_nu8_t1"] = base8
for c in cases:
    c["r_rel_to_nu9_t1"] = base9 / c["eps_nu"]
    c["r_rel_to_same_nu_t1"] = (base8 if c["nu"] == 8 else base9) / c["eps_nu"]

# ---- 图：三面板（a) t(T)；(b) y(T)；(c) eps_nu 随 t 与 r 相对 ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ax.plot(Ts, t1, label="t, m=1")
ax.plot(Ts, t2, "--", label="t, m=2")
ax.axhline(1.0, color="k", ls=":", lw=1.0, label="t=1（y=0 处等号）")
ax.set(xlabel=r"$T/\omega_D$", ylabel="$t$", title="(a) 粗粒化指数 t(T) 随 T 严格增（与 y 同向）")
ax.legend(fontsize=8)
ax2 = ax.twinx()
ax2.plot(Ts, [r["y"] for r in rows], color="C3", lw=0.8, alpha=0.6)
ax2.set_ylabel("$y$", color="C3")

ax = axes[1]
tgrid = np.linspace(1.0, 1.16, 120)
for nu, c in ((8, "C0"), (9, "C1")):
    ax.plot(tgrid, [eps_nu(nu, float(t))[1] for t in tgrid], c, label=r"$\epsilon_\nu$, $\nu$=%d" % nu)
for nu, c in ((8, "C0"), (9, "C1")):
    for tt, ls in ((1.0, ":"), (t_of(TC, 1), "--")):
        ax.axvline(tt, color=c, ls=ls, lw=0.8)
ax.set(xlabel="t", ylabel=r"$\epsilon_\nu$", title="(b) $\\epsilon_\\nu$ 随 t（竖线：t=1 与 t(Tc)）")
ax.legend(fontsize=8)

ax = axes[2]
plt_ = [c for c in cases if c["nu"] == 8]
labs = ["t=1", "t(Tc),m=1", "t(Tc),m=2", "ub,m=1", "ub,m=2"]
vals = [c["r_rel_to_same_nu_t1"] for c in plt_]
ax.bar(range(len(vals)), vals, color=["C7"] + ["C0"] * 4)
ax.set_xticks(range(len(vals)))
ax.set_xticklabels(labs, fontsize=8)
ax.axhline(1.0, color="k", ls=":")
ax.set(ylabel=r"$r/r_{t=1}$", title="(c) $r\\propto 1/\\epsilon_\\nu$ 的相对移动（$\\nu$=8）")

fig.tight_layout()
fig.savefig("环15粗粒化指数t_方向与下界.png", dpi=150)
with open("环15粗粒化指数t_方向与下界.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
