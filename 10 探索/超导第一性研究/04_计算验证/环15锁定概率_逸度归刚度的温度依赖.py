# -*- coding: utf-8 -*-
"""环 15 / 审-6 重开（第 185 轮）：逸度 y 的温度依赖归还刚度，sigma_theta 只作恒等

登记口径：
- (15L.3) y(T) = 2*pi*exp(-E_c/(k_B T)), E_c = (pi^2/2) * Upsilon（Upsilon 为有效刚度）
- 环 19 (19W.3)/(19W.8)：Upsilon_bare(T) = Upsilon_0 * w(T)，w(T) = 2*int_0^1 u*tanh(u/(2T/w_D)) du
- (15L.5) y(T_c) <= 2*pi*exp(-pi^2/(2*beta_KT)) = 0.02501（与 Upsilon 无关）

本脚本只做：两条 Upsilon_0 分支下的 y(T)、t(T_c)、T_sync(m)，以及 (15L.5) 反解出的 Upsilon_0 下界。
无拟合、无新参数。
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
G = 0.622281
BETA_K = 0.89294
YB = 2.0 * np.pi * np.exp(-np.pi ** 2 / (2.0 * BETA_K))      # 0.02501 上界


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
Phi = lambda p: ((p - PC) / (1 - PC)) ** TU
phic = 1.0 - chi2.cdf(XC, NU)
KAP = G * Phi(phic)
UPS0_KAP = 2.0 * TC / (np.pi ** 2 * WC * KAP)      # 163 轮的两支之一
UPS0_WP = 2.0 * 3.207211 / np.pi ** 2              # 工作点支：2*E_c/pi^2, E_c=3.207211

p_pair = lambda t: 1.0 - chi2.cdf(XC * WC / w(t), NU)


def K_of(ups0, t):
    return ups0 * w(t) / t


def y_of(ups0, t):
    return 2.0 * np.pi * np.exp(-np.pi ** 2 * K_of(ups0, t) / 2.0)


_tm = lambda ups0, t, m: 1.0 + m * np.log(1.0 - y_of(ups0, t)) / np.log(phic)
_ps = lambda ups0, t, m: p_pair(t) * (1.0 - y_of(ups0, t)) ** m

out = {"w_Tc": WC, "p_at_Tc": phic, "y_bound": YB, "Upsilon0_KAP": UPS0_KAP, "Upsilon0_wp": UPS0_WP}

# (15L.5) 反解 Upsilon_0 下界：K(T_c)=Upsilon_0*w(T_c)/T_c >= 1/beta_KT
out["Upsilon0_lower_from_bound"] = TC / (BETA_K * WC)
out["K_Tc_wp"] = K_of(UPS0_WP, TC)
out["K_Tc_KAP"] = K_of(UPS0_KAP, TC)
out["one_over_beta"] = 1.0 / BETA_K

# y(T) 与单调性：y 增 <=> K 减
out["y_Tc_wp"] = y_of(UPS0_WP, TC)
out["y_Tc_KAP"] = y_of(UPS0_KAP, TC)
out["y_Tc_wp_le_bound"] = bool(out["y_Tc_wp"] <= YB + 1e-15)
out["y_Tc_KAP_le_bound"] = bool(out["y_Tc_KAP"] <= YB + 1e-15)

ts = np.linspace(0.10, 1.20, 221)
rows = []
for ups0, tag in ((UPS0_WP, "wp"), (UPS0_KAP, "KAP")):
    Ks = np.array([K_of(ups0, float(t)) for t in ts])
    ysr = np.array([y_of(ups0, float(t)) for t in ts])
    out[f"K_strict_decreasing_{tag}"] = bool(np.all(np.diff(Ks) < 0))
    out[f"y_strict_increasing_{tag}"] = bool(np.all(np.diff(ysr) > 0))
    out[f"y_max_{tag}"] = float(ysr.max())
    out[f"y_argmax_{tag}"] = float(ts[int(np.argmax(ysr))])

for t in (0.3, 0.35, 0.4, 0.45, 0.5, 0.55):
    rows.append({"T": t, "w": w(t), "K_wp": K_of(UPS0_WP, t), "y_wp": y_of(UPS0_WP, t),
                 "y_KAP": y_of(UPS0_KAP, t), "p_pair": p_pair(t),
                 "psync_m1": _ps(UPS0_WP, t, 1), "psync_m2": _ps(UPS0_WP, t, 2)})
out["table"] = rows

out["t_m1_Tc"] = _tm(UPS0_WP, TC, 1)
out["t_m2_Tc"] = _tm(UPS0_WP, TC, 2)


# y=2*pi*exp(-pi^2 K/2) 是逸度小量展开：y>=1 处越出定义域（K<=2*ln(2*pi)/pi^2）
K_BREAK = 2.0 * np.log(2.0 * np.pi) / np.pi ** 2
out["K_break_y_ge_1"] = K_BREAK
T_BREAK = float(brentq(lambda t: K_of(UPS0_WP, t) - K_BREAK, TC, 2.0, xtol=1e-14))
out["T_break_y_ge_1"] = T_BREAK
out["y_at_break"] = float(y_of(UPS0_WP, T_BREAK))


def solve(m):
    return brentq(lambda t: _ps(UPS0_WP, t, m) - PC, TC, T_BREAK - 1e-6, xtol=1e-14)


out["T_sync_m1"] = float(solve(1))
out["T_sync_m2"] = float(solve(2))
out["T_star"] = float(brentq(lambda t: p_pair(t) - PC, TC, 2.0, xtol=1e-13))
out["Tsync_m2_lt_m1"] = bool(out["T_sync_m2"] < out["T_sync_m1"])

# 两侧窗口：由 (19W.8) 的 Upsilon(T)=Upsilon_0 w(T) Phi(T)，0<=Phi<=1，且 (15L.5) y(T_c)<=y_crit
# 取 Phi=1（y 最小、T_sync 最高）与 Phi=const 使 y(T_c)=y_crit（y 最大、T_sync 最低）
_yTc_min = y_of(UPS0_WP, TC)
_lnMin = np.log(2.0 * np.pi / _yTc_min)
_lnMax = np.log(2.0 * np.pi / YB)
out["Phi_for_ycrit"] = float(_lnMax / _lnMin)
PHI_HI = out["Phi_for_ycrit"]
y_phi = lambda phi, t: 2.0 * np.pi * np.exp(-(np.pi ** 2) * (UPS0_WP * w(t) * phi) / (2.0 * t))
ps_phi = lambda phi, t, m: p_pair(t) * (1.0 - y_phi(phi, t)) ** m
out["y_Tc_Phi_hi"] = float(y_phi(PHI_HI, TC))


def solve_phi(phi, m):
    return brentq(lambda t: ps_phi(phi, t, m) - PC, TC, T_BREAK - 1e-6, xtol=1e-14)


out["T_sync_window_m1"] = [float(solve_phi(1.0, 1)), float(solve_phi(PHI_HI, 1))]
out["T_sync_window_m2"] = [float(solve_phi(1.0, 2)), float(solve_phi(PHI_HI, 2))]
out["window_note"] = "下界=Phi=1（y 最小）；上界=Phi 取 y(Tc)=y_crit（y 最大）"

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ax.plot(ts, [y_of(UPS0_WP, float(t)) for t in ts], label=r"$y(T)$, $Upsilon_0$=%.4f（工作点支）" % UPS0_WP)
ax.plot(ts, [y_of(UPS0_KAP, float(t)) for t in ts], "--", label=r"$y(T)$, $Upsilon_0$=%.4f（KAP 支，越界）" % UPS0_KAP)
ax.axhline(YB, color="r", ls=":", lw=1.2, label=r"$y_{\rm crit}$=%.5f" % YB)
ax.axhline(1.0, color="gray", ls="--", lw=0.8)
ax.axvline(T_BREAK, color="gray", ls="--", lw=0.8)
ax.set(xlabel=r"$T/\omega_D$", ylabel="$y$", title="(a) 逸度归刚度后的温度形状", yscale="log")
ax.legend(fontsize=7)

ax = axes[1]
ax.plot(ts, [K_of(UPS0_WP, float(t)) for t in ts], label=r"$K=\Upsilon(T)/T$（工作点支）")
ax.plot(ts, [K_of(UPS0_KAP, float(t)) for t in ts], "--", label=r"$K$（KAP 支）")
ax.axhline(1.0 / BETA_K, color="k", ls=":", label=r"$1/\beta_{\rm KT}$=%.4f" % (1.0 / BETA_K))
ax.set(xlabel=r"$T/\omega_D$", ylabel="$K$", title="(b) 刚度比随 T 严格减，y 随之严格增")
ax.legend(fontsize=7)

ax = axes[2]
tm = ts[ts <= T_BREAK]
ax.plot(tm, [_ps(UPS0_WP, float(t), 1) for t in tm], label="p_sync, m=1")
ax.plot(tm, [_ps(UPS0_WP, float(t), 2) for t in tm], "--", label="p_sync, m=2")
ax.axhline(PC, color="k", ls=":", label=r"$p_c$")
ax.axvline(T_BREAK, color="gray", ls="--", lw=0.8, label=r"$T_{\rm break}$（$y\to1$，定义域端）")
ax.set_xlim(TC, T_BREAK + 0.02)
for v, c in ((out["T_sync_m2"], "C1"), (out["T_sync_m1"], "C0")):
    ax.axvline(v, color=c, lw=0.8)
ax.set(xlabel=r"$T/\omega_D$", ylabel="概率", title="(c) T_sync: %.4f (m=2) < %.4f (m=1) < %.4f" % (out["T_sync_m2"], out["T_sync_m1"], out["T_star"]))
ax.legend(fontsize=7)

fig.tight_layout()
fig.savefig("环15锁定概率_逸度归刚度的温度依赖.png", dpi=150)
with open("环15锁定概率_逸度归刚度的温度依赖.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
