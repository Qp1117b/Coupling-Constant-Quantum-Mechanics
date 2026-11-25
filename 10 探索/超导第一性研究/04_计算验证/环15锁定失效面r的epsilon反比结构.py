# -*- coding: utf-8 -*-
"""环 15 / 审-6 重开（第 188 轮）：epsilon_nu -> r 的反比结构与失效面 a_*lambda = r

登记口径（不新引参数，全部取自已登记式）：
- 环 17 侧：r(T) = 2*alphaV*w(T)/(3*eps_nu(T)*|w'(T)|)，s = 2/[C(a*lambda - r)]，失效面 a_*lambda = r
- (15L.3)+(19W.3)：w(T) 由环 19 积分式，eps_nu 由 x_* = Fbar_nu^{-1}(p_c^{1/t}) 与
  eps_nu = 2 x_* f_nu(x_*)/Fbar_nu(x_*) 给（(15L.4) 的 t(T)）
- 本轮定理（Spec v15）：TargetPropROfEps（eps 越小 r 越大，纯反比结构）、
  TargetPropSFail（s>0 <=> r < a*lambda，只要求 C>0）

本脚本只做三件事（属理论自显影，不做数据对照）：
1. r(T)/r(T_c) 的三因子分解：w/|w'|（进一步变冷/变热的刚度形状） × 1/eps_nu（反比）；
2. 失效面 a_*lambda = r 的温度移动（r 单调性数值侧，登记为 G-188 若未证）；
3. T -> T_break 时 r 的发散侧（x_* -> 0 => eps_nu -> 0 => r -> inf）。
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
UPS0_WP = 2.0 * 3.207211 / np.pi ** 2


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
y_of = lambda t: 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0_WP * w(t)) / (2.0 * t))
p_pair = lambda t: 1.0 - chi2.cdf(XC * WC / w(t), NU)
t_of = lambda T, m: 1.0 + m * np.log(1.0 - y_of(T)) / np.log(p_pair(T))

K_BREAK = 2.0 * np.log(2.0 * np.pi) / np.pi ** 2
T_BREAK = float(brentq(lambda T: UPS0_WP * w(T) / T - K_BREAK, TC, 2.0, xtol=1e-14))


def wprime(T, h=1e-4):
    """w'(T) 中心差分（w 的解析式是积分，无法直接给导数，故用中心差分；仅数值显影用）。"""
    return (w(T + h) - w(T - h)) / (2.0 * h)


def x_star(nu, t):
    q = PC ** (1.0 / t)
    return float(brentq(lambda x: chi2.sf(x, nu) - q, 1e-10, 200.0, xtol=1e-15))


def eps_nu(nu, t):
    x = x_star(nu, t)
    return float(2.0 * x * chi2.pdf(x, nu) / chi2.sf(x, nu))


def r_ratio(nu, m, T):
    """r(T)/r(T_c)：alphaV 与 C 全部约掉，只剩 w/|w'| 与 1/eps_nu 两个显式因子。"""
    eps = eps_nu(nu, t_of(T, m))
    eps_c = eps_nu(nu, t_of(TC, m))
    wfac = (w(T) / WC) * (abs(wprime(TC)) / abs(wprime(T)))
    return wfac * (eps_c / eps), wfac, eps_c / eps, eps


out = {"w_Tc": WC, "w_prime_Tc": wprime(TC), "T_break": T_BREAK,
       "eps_nu_Tc_nu8": eps_nu(8, t_of(TC, 1)), "eps_nu_Tc_nu9": eps_nu(9, t_of(TC, 1))}

# ---- 1. 三因子分解与温度移动 ----
rows = []
Ts = np.linspace(TC, T_BREAK - 1e-3, 300)
for T in Ts:
    T = float(T)
    for m in (1, 2):
        rr, wf, ef, e = r_ratio(8, m, T)
        rows.append({"T": T, "m": m, "r_rel": rr, "w_factor": wf, "eps_factor": ef, "eps_nu8": e})

for m in (1, 2):
    seq = [r["r_rel"] for r in rows if r["m"] == m]
    wseq = [r["w_factor"] for r in rows if r["m"] == m]
    Ts_m = [r["T"] for r in rows if r["m"] == m]
    out[f"r_rel_strict_increasing_m{m}"] = bool(np.all(np.diff(seq) > 0))
    out[f"r_rel_at_domain_end_m{m}"] = float(seq[-1])
    i_min = int(np.argmin(seq))
    out[f"r_rel_min_m{m}"] = {"value": float(seq[i_min]), "T": float(Ts_m[i_min]),
                              "dip_depth": float(1.0 - seq[i_min])}
    j_min = int(np.argmin(wseq))
    out[f"w_factor_min_m{m}"] = {"value": float(wseq[j_min]), "T": float(Ts_m[j_min])}

# 同步点（m=1/2）处的 r 相对值：T_sync 由 p_sync = p_c 定，这里直接用 185 轮登记值
T_SYNC = {1: 0.5066509607326937, 2: 0.470706768695635}
for m in (1, 2):
    for nu in (8, 9):
        rr, wf, ef, e = r_ratio(nu, m, T_SYNC[m])
        out[f"r_rel_at_Tsync_m{m}_nu{nu}"] = {"r_rel": rr, "w_factor": wf, "eps_factor": ef, "eps_nu": e}
    rr, _, _, _ = r_ratio(8, m, TC)
    out[f"r_rel_at_Tc_m{m}_nu8"] = float(rr)

# 1/eps 单独看（不含 w/|w'| 因子）
out["one_over_eps_at_Tsync_m1_nu8"] = 1.0 / r_ratio(8, 1, T_SYNC[1])[3]
out["one_over_eps_at_Tc_m1_nu8"] = 1.0 / r_ratio(8, 1, TC)[3]

# ---- 2. T -> T_break 的发散侧 ----
eps_near = {}
for frac in (0.5, 0.2, 0.05, 0.01):
    T = T_BREAK - frac * (T_BREAK - TC)
    eps_near[f"{frac}"] = {"T": T, "t_m1": t_of(T, 1), "eps_nu8": eps_nu(8, t_of(T, 1)),
                           "r_rel_m1_nu8": r_ratio(8, 1, T)[0]}
out["near_break"] = eps_near

# ---- 3. 失效面 a_*lambda = r 的形状（只报 r 的相对值，a*lambda 的量纲由 alphaV 外部定） ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
for m, ls in ((1, "-"), (2, "--")):
    seq = [r["r_rel"] for r in rows if r["m"] == m]
    ax.plot(Ts, seq, ls, label=f"r/r(Tc), m={m} ($\\nu$=8)")
ax.axhline(1.0, color="k", ls=":", lw=1.0)
for m in (1, 2):
    ax.axvline(T_SYNC[m], color="C%d" % (m - 1), ls=":", lw=0.8)
ax.set(xlabel="$T/\\omega_D$", ylabel="$r/r(T_c)$",
       title="(a) 失效面 $r(T)/r(T_c)$（含 $w/|w'|$ 形状项）：近 $T_c$ 有 4e-4 凹陷")
ax.set_yscale("log")
ax.legend(fontsize=8)

ax = axes[1]
for m, c in ((1, "C0"), (2, "C1")):
    ax.plot(Ts, [r["w_factor"] for r in rows if r["m"] == m], c, label=f"$w/|w'|$ 因子, m={m}")
ax2 = ax.twinx()
for m, c in ((1, "C0"), (2, "C1")):
    ax2.plot(Ts, [r["eps_factor"] for r in rows if r["m"] == m], c, ls="--", label=f"$1/\\epsilon$ 因子, m={m}")
ax.set(xlabel="$T/\\omega_D$", ylabel="w 因子", title="(b) 三因子拆解：形状项 vs 反比项")
ax2.set_ylabel("1/eps 因子")
ax.legend(fontsize=7, loc="upper left")
ax2.legend(fontsize=7, loc="lower right")

ax = axes[2]
tt = np.linspace(1.0, 1.35, 200)
for nu, c in ((8, "C0"), (9, "C1")):
    ax.plot(tt, [eps_nu(nu, float(t)) for t in tt], c, label=f"$\\epsilon_\\nu$, $\\nu$={nu}")
    ax.set_yscale("log")
ax.set(xlabel="t", ylabel="$\\epsilon_\\nu$", title="(c) $\\epsilon_\\nu(t)$ 单调下降（$r\\propto1/\\epsilon$ 的反比前提）")
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig("环15锁定失效面r的epsilon反比结构.png", dpi=150)
with open("环15锁定失效面r的epsilon反比结构.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
