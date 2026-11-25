# -*- coding: utf-8 -*-
"""环 15 / 审-6 重开（第 189 轮）：Phi 是否进入 (15L.3) —— 逸度窗口的授权域与 BKT 钉住的冲突

登记口径（不新引参数）：
- (15L.3)：y = 2*pi*exp(-E_c/(k_B T))，E_c = (pi^2/2)*Upsilon，Upsilon = Upsilon_0*w(T)*Phi(T)（185 轮写法）
- (15L.5)：y(T_c) <= y_crit = 2*pi*exp(-pi^2/(2*beta_KT)) = 0.02501（beta_KT=0.89294）
- (19P.24)/(154.2)：Phi(p_pair(T_c)) = Phi_c = kappa = 2*k_B*T_c/(pi*Upsilon_bond*w_c)
- (19W.1)：Upsilon_0 = Upsilon(0) = Upsilon_bond（T->0 时 w(0)=1、Phi(1)=1），故 kappa 用 Upsilon_0 表示

本脚本只做四件事（理论自显影，不做数据对照）：
1. y(Phi) 的单调性（Phi 只能抬高逸度；核对 TargetPropPhiMono）；
2. (15L.5) 反解出的 Phi 下界闭式 Phi_min（核对 TargetPropPhiMinEq）；
3. BKT 钉住处 y 的普适值 2*pi*exp(-pi)=0.27150（核对 TargetPropPhiBktVal）；
4. 两者的比值 = 2*beta_KT/pi = K_BKT = 0.5685 < 1（核对 TargetPropPhiConflict），并给 T_sync 的塌缩。
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
BETA_K = 0.89294
UPS0_WP = 2.0 * 3.207211 / np.pi ** 2      # 0.6499168


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
Y_CRIT = 2.0 * np.pi * np.exp(-np.pi ** 2 / (2.0 * BETA_K))
Y_R = 2.0 * np.pi * np.exp(-np.pi)
K_BKT_JUMP = 2.0 * BETA_K / np.pi          # 普适跳变（同一单位制）

fug = lambda Phi: 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0_WP * WC * Phi) / (2.0 * TC))

# ---- 1. y(Phi) 单调（Phi 增 => y 减）----
PHI_MIN = (2.0 * TC / (np.pi ** 2 * UPS0_WP * WC)) * np.log(2.0 * np.pi / Y_CRIT)
Phis = np.linspace(0.30, 1.10, 200)
ys = np.array([fug(float(p)) for p in Phis])
out = {"y_crit": Y_CRIT, "y_R": Y_R, "K_BKT_jump": K_BKT_JUMP,
       "y_strict_decreasing_in_Phi": bool(np.all(np.diff(ys) < 0)),
       "y_at_Phi_1": fug(1.0), "y_at_Phi_min": fug(PHI_MIN)}

# ---- 2. Phi 下界闭式（(15L.5) 反解）----
out["phi_min"] = PHI_MIN
out["y_at_phi_min_byself"] = float(2.0 * np.pi * np.exp(
    -np.pi ** 2 * (UPS0_WP * WC * PHI_MIN) / (2.0 * TC)))
out["phi_min_matches_185"] = bool(abs(PHI_MIN - 0.6813472) < 1e-6)

# ---- 3. BKT 钉住：Phi_BKT = kappa，y 的普适值 ----
PHI_BKT = 2.0 * TC / (np.pi * UPS0_WP * WC)
out["phi_bkt_kappa"] = PHI_BKT
out["y_at_phi_bkt"] = float(2.0 * np.pi * np.exp(
    -np.pi ** 2 * (UPS0_WP * WC * PHI_BKT) / (2.0 * TC)))
out["y_at_phi_bkt_is_yR"] = bool(abs(out["y_at_phi_bkt"] - Y_R) < 1e-12)
out["phi_bkt_lt_phi_min"] = bool(PHI_BKT < PHI_MIN)
out["ratio_phi_bkt_over_phi_min"] = PHI_BKT / PHI_MIN
out["ratio_identity_2beta_over_pi"] = K_BKT_JUMP

# ---- 4. no-go：beta_KT < pi/2 <=> y(1/beta) < y(2/pi) ----
y_at_inv_beta = float(2.0 * np.pi * np.exp(-np.pi ** 2 * (1.0 / BETA_K) / 2.0))
y_at_2_over_pi = float(2.0 * np.pi * np.exp(-np.pi ** 2 * (2.0 / np.pi) / 2.0))
out["beta_lt_half_pi"] = bool(BETA_K < np.pi / 2)
out["y_inv_beta"] = y_at_inv_beta
out["y_2_over_pi"] = y_at_2_over_pi
out["no_go_holds"] = bool(y_at_inv_beta < y_at_2_over_pi)

# ---- T_sync 随 Phi 的塌缩（Phi 从 Phi_min 到 1）----
p_pair = lambda T: 1.0 - chi2.cdf(XC * WC / w(T), NU)


def t_of(T, m, Phi):
    y = 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0_WP * w(T) * Phi) / (2.0 * T))
    return 1.0 + m * np.log(1.0 - y) / np.log(p_pair(T))


def solve_tsync(m, Phi):
    f = lambda T: p_pair(T) * (1.0 - 2.0 * np.pi * np.exp(
        -np.pi ** 2 * (UPS0_WP * w(T) * Phi) / (2.0 * T))) ** m - PC
    try:
        return float(brentq(f, 1e-6, 0.75, xtol=1e-12))
    except ValueError:
        return None


Tsync = {}
for lab, Phi in (("Phi_min", PHI_MIN), ("Phi=1", 1.0)):
    for m in (1, 2):
        Tsync[f"{lab}_m{m}"] = solve_tsync(m, Phi)
out["Tsync_Phi_min"] = [Tsync["Phi_min_m1"], Tsync["Phi_min_m2"]]
out["Tsync_Phi_1"] = [Tsync["Phi=1_m1"], Tsync["Phi=1_m2"]]

# ---- 图：三面板 ----
fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
ax = axes[0]
ax.plot(Phis, ys, "C0", label="$y(\\Phi)$（工作点）")
ax.axhline(Y_CRIT, color="C3", ls="--", lw=1.0, label="$y_{\\rm crit}=0.02501$（(15L.5)）")
ax.axhline(Y_R, color="C2", ls=":", lw=1.2, label="$y_R=2\\pi e^{-\\pi}=0.2715$（BKT）")
ax.axvline(PHI_MIN, color="C3", ls=":", lw=0.8)
ax.axvline(PHI_BKT, color="C2", ls=":", lw=0.8)
ax.axvline(1.0, color="k", ls=":", lw=0.8)
ax.set(xlabel="$\\Phi$", ylabel="$y$", title="(a) $\\Phi$ 只能抬高逸度；(15L.5) 反解出 $\\Phi$ 下界")
ax.set_yscale("log")
ax.legend(fontsize=7)

ax = axes[1]
bars = [PHI_MIN, PHI_BKT]
ax.bar([0, 1], bars, color=["C3", "C2"], width=0.55)
ax.axhline(1.0, color="k", ls=":")
for i, v in enumerate(bars):
    ax.text(i, v + 0.02, f"{v:.4f}", ha="center", fontsize=9)
ax.set_xticks([0, 1])
ax.set_xticklabels(["$\\Phi_{\\min}$（(15L.5)）", "$\\Phi_{\\rm BKT}=\\kappa$（(154.2)）"], fontsize=8)
ax.set(ylabel="$\\Phi$", title="(b) 比值 $=2\\beta_{\\rm KT}/\\pi=K_{\\rm BKT}=0.5685<1$")
ax.set_ylim(0, 1.45)

ax = axes[2]
phi_grid = np.linspace(PHI_MIN, 1.0, 60)
for m, c in ((1, "C0"), (2, "C1")):
    ts = [solve_tsync(m, float(p)) for p in phi_grid]
    ax.plot(phi_grid, [t if t is not None else np.nan for t in ts], c, label=f"$T_{{\\rm sync}}$, m={m}")
ax.axvline(PHI_MIN, color="C3", ls=":", lw=0.8)
ax.axvline(1.0, color="k", ls=":", lw=0.8)
ax.set(xlabel="$\\Phi$", ylabel="$T_{\\rm sync}/\\omega_D$", title="(c) $\\Phi$ 进逸度才成窗口；$\\Phi=1$ 处塌成点")
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig("环15锁定概率_Φ授权域与BKT钉住冲突.png", dpi=150)
with open("环15锁定概率_Φ授权域与BKT钉住冲突.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
