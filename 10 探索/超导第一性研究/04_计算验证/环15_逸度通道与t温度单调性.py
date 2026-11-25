# -*- coding: utf-8 -*-
"""
环 15：锁定因子逸度的通道判定、R-158 §四两处笔误修正、t(T) 的温度单调性（R-159）
全部为解析式数值对照，不做拟合。Debye 相干权重 w(T) 用 (10B.4) 精确积分。
运行：python "10 探索/超导第一性研究/04_计算验证/环15_逸度通道与t温度单调性.py"
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.stats import chi2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

P_C = 0.592746          # 2D 方格座渗流阈值
BETA_KT = 0.89294       # k_B T_BKT / Upsilon（方格 XY，arXiv:1210.2403）
TWO_PI = 2.0 * np.pi
NU = 8                  # BCC 星，z=8
res = {}


# ---------- Debye 相干权重 w(T)（(10B.4)，非拟合，精确积分） ----------
def w_debye(tau):
    """tau = T/theta_D；w=8 tau^2 ∫_0^{1/(2 tau)} u tanh u du，w(0)=1。"""
    if tau <= 1e-12:
        return 1.0
    upper = 1.0 / (2.0 * tau)
    val, _ = quad(lambda u: u * np.tanh(u), 0.0, upper, limit=400)
    return 8.0 * tau * tau * val


def y_of_tau(tau, gamma):
    """y = 2*pi*exp[-(pi^2 gamma/2)*(w/tau)]，gamma = Upsilon_0/omega_D。"""
    w = w_debye(tau)
    x = tau / (gamma * w)          # x = k_B T / Upsilon_bare
    return TWO_PI * np.exp(-(np.pi**2 / 2.0) / x)


def fugacity(x):
    """x = k_B T / Upsilon；y = 2*pi*exp(-(pi^2/2)/x)。"""
    x = np.asarray(x, dtype=float)
    return TWO_PI * np.exp(-(np.pi**2 / 2.0) / x)


# ---------- A：R-158 §四 两处笔误的可检性 ----------
y_correct = TWO_PI * np.exp(-(np.pi**2 / (2.0 * BETA_KT)))   # 正确：pi^2/(2 beta)
y_wrong = TWO_PI * np.exp(-(np.pi**2 * BETA_KT / 2.0))       # 笔误：pi^2 beta/2
res["y_crit_correct"] = float(y_correct)
res["y_crit_typo"] = float(y_wrong)
res["typo_ratio"] = float(y_wrong / y_correct)
assert 0.024 < y_correct < 0.026, f"正确式应给≈0.025，实得 {y_correct}"
assert 0.070 < y_wrong < 0.082, f"笔误式应给≈0.0765，实得 {y_wrong}"
assert y_wrong / y_correct > 2.5, "两式必须可明显区分"
# 与脚本既有 y_crit=fugacity(beta_KT) 一致
assert abs(fugacity(BETA_KT) - y_correct) < 1e-15, "正确式与 fugacity(beta) 不一致"
res["y_crit_matches_script"] = bool(abs(fugacity(BETA_KT) - y_correct) < 1e-15)


# ---------- B：裸交点关系（方向核对） ----------
# 正确：k_B T_c = beta_KT * Upsilon_bare  =>  Upsilon_bare/(k_B T_c) = 1/beta_KT
res["upsilon_over_kT_correct"] = float(1.0 / BETA_KT)
res["upsilon_over_kT_typo"] = float(BETA_KT)
# E_c/(k_B T_c) = (pi^2/2)*(Upsilon/(k_B T_c))
EcE_correct = (np.pi**2 / 2.0) * (1.0 / BETA_KT)
EcE_typo = (np.pi**2 / 2.0) * BETA_KT
res["Ec_over_kT_correct"] = float(EcE_correct)
res["Ec_over_kT_typo"] = float(EcE_typo)
assert abs(TWO_PI * np.exp(-EcE_correct) - y_correct) < 1e-15, "正确通道自洽失败"
assert abs(TWO_PI * np.exp(-EcE_typo) - y_wrong) < 1e-15, "笔误通道自洽失败"


# ---------- C：逸度通道（热有效 vs 涡旋重整化） ----------
# 涡旋重整化：Upsilon_R/(k_B T_c)=2/pi  =>  E_c/(k_B T_c)=pi  =>  y_R=2 pi e^{-pi}
EcE_renorm = np.pi
y_renorm = TWO_PI * np.exp(-EcE_renorm)
res["y_renormalized_fixedpoint"] = float(y_renorm)
assert 0.26 < y_renorm < 0.28, f"重整化固定点逸度应≈0.2715，实得 {y_renorm}"
assert y_renorm > 10.0 * y_correct, "重整化逸度应远大于热有效逸度（作为固定点值）"


# ---------- D：t(T) 的温度单调性（精确 w(T) + 卡方尾） ----------
def t_eff(p, y):
    return 1.0 + np.log1p(-np.asarray(y, dtype=float)) / np.log(p)


def solve_tauc(gamma):
    from scipy.optimize import brentq
    f = lambda tau: tau - BETA_KT * gamma * w_debye(tau)
    return brentq(f, 1e-3, 8.0, xtol=1e-12)


def p_pair_tau(tau, sigma2):
    """p_pair=1-F_nu(nu sigma_c^2/(Z w))；sigma2=sigma_c^2/Z。"""
    w = w_debye(tau)
    x = NU * sigma2 / w
    return 1.0 - chi2.cdf(x, NU)


def build_curve(gamma, m=1.0, npts=400):
    tau_c = solve_tauc(gamma)
    # 校准 sigma_c^2/Z，使 p_pair(tau_c)=p_c/(1-y(tau_c))^m（阈值处同步）
    y_c = y_of_tau(tau_c, gamma)
    p_thr = P_C / (1.0 - y_c)**m
    # 1-F_nu(nu sigma2/w_c)=p_thr  =>  x*=F_nu^{-1}(1-p_thr); sigma2=x* w_c/nu
    x_star = chi2.ppf(1.0 - p_thr, NU)
    sigma2 = x_star * w_debye(tau_c) / NU
    taus = np.linspace(1e-2, tau_c, npts)     # 起点 1e-2 避开 y 的浮点下溢
    yv = np.array([y_of_tau(t, gamma) for t in taus])
    pv = np.array([p_pair_tau(t, sigma2) for t in taus])
    tv = 1.0 + np.log1p(-yv) / np.log(pv)
    return tau_c, taus, yv, pv, tv, sigma2


results = {}
for gamma in (1.0, 1.5, 2.0):
    tau_c, taus, yv, pv, tv, sigma2 = build_curve(gamma)
    # 单调性判定（数值差分；y 在可分辨区间 y>1e-10 上判）
    d = np.diff(tv)
    mono_inc = bool(np.all(d > -1e-9))
    ymask = yv > 1e-10
    y_mono = bool(np.all(np.diff(yv[ymask]) > 0))
    results[gamma] = dict(
        tau_c=float(tau_c),
        sigma2=float(sigma2),
        y_at_tauc=float(yv[-1]),
        p_at_tauc=float(pv[-1]),
        t_at_tauc=float(tv[-1]),
        t_min=float(tv.min()), t_max=float(tv.max()),
        t_monotone_increasing=mono_inc,
        t_argmax_tau=float(taus[int(np.argmax(tv))]),
        y_monotone=y_mono,
        p_monotone_decreasing=bool(np.all(np.diff(pv) < 0)),
    )
res["curves"] = results

# 关键断言（以 gamma=1.5 为主）
main = results[1.5]
assert main["y_monotone"], "y(T) 应严格增"
assert main["p_monotone_decreasing"], "p_pair(T) 应严格减"
assert abs(main["t_at_tauc"] - 1.0509) < 0.02, f"阈值处 t 应≈1.0509，实得 {main['t_at_tauc']}"
assert main["t_at_tauc"] <= 1.0509 + 0.02, "阈值处 t 不应显著超过上界"
assert main["t_monotone_increasing"], f"gamma=1.5 时 t(T) 应单调增（否则须回改），实测 {main['t_monotone_increasing']}"


# ---------- E：t 的 log 导数判据核对 ----------
# d(t-1)/dT ∝ delta' * L - delta * L'，其中 delta=|ln(1-y)|, L=|ln p|
tau_c, taus, yv, pv, tv, _ = build_curve(1.5)
delta = -np.log1p(-yv)
L = -np.log(pv)
ddelta = np.gradient(delta, taus)
dL = np.gradient(L, taus)
sign_num = ddelta * L - delta * dL
dt = np.gradient(tv, taus)
# 数值导数与判据同号（在 delta 可分辨、非端点处）
delta = -np.log1p(-yv)
L = -np.log(pv)
ddelta = np.gradient(delta, taus)
dL = np.gradient(L, taus)
sign_num = ddelta * L - delta * dL
dt = np.gradient(tv, taus)
win = (delta > 0.003) & (L > 0.05)
win[:2] = False
win[-2:] = False
agree = float(np.mean(np.sign(dt[win]) == np.sign(sign_num[win])))
res["logderiv_criterion_agreement"] = agree
res["logderiv_window_points"] = int(win.sum())
assert agree > 0.90, f"log 导数判据与数值导数应同号，实测一致率 {agree}"


# ---------- 图（六面板） ----------
fig, axes = plt.subplots(2, 3, figsize=(17.5, 9.4))

# (a) w(tau)
tt = np.linspace(1e-3, 3.0, 300)
ww = np.array([w_debye(t) for t in tt])
ax = axes[0, 0]
ax.plot(tt, ww, lw=2, color="#1f77b4", label=r"$w(T)$（(10B.4) 精确）")
ax.plot(tt, 1 - (np.pi**2 / 3) * tt**2, "--", color="#2ca02c", lw=1, label=r"低温 $1-\frac{\pi^2}{3}T^2$")
ax.plot(tt, 1.0 / (3 * tt), ":", color="#d62728", lw=1, label=r"高温 $\frac{1}{3T}$")
ax.set_ylim(0, 1.05); ax.set_xlabel(r"$\tau=T/\theta_D$"); ax.set_ylabel(r"$w$")
ax.set_title("(a) Debye 相干权重"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# (b) Ec/(kT) 与 y 通道
ax = axes[0, 1]
for gamma, c in [(1.0, "#2ca02c"), (1.5, "#1f77b4"), (2.0, "#ff7f0e")]:
    tc = solve_tauc(gamma)
    ts = np.linspace(1e-3, tc, 200)
    ecE = (np.pi**2 / 2.0) * gamma * np.array([w_debye(t) for t in ts]) / ts
    ax.plot(ts, ecE, lw=2, color=c, label=rf"$\gamma={gamma}$")
ax.axhline(EcE_renorm, ls=":", color="#d62728", lw=1.2, label=r"涡旋重整化 $\pi$")
ax.set_xlabel(r"$\tau$"); ax.set_ylabel(r"$E_c^{\rm eff}/(k_BT)$")
ax.set_title("(b) 热有效核能比（随 T 降）"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# (c) y(tau) 与两条通道水平线
ax = axes[0, 2]
tc, ts, yv, pv, tv, _ = build_curve(1.5)
ax.plot(ts, yv, lw=2, color="#1f77b4", label=r"$y(T)$（热有效）")
ax.axhline(y_correct, ls="--", color="#2ca02c", lw=1.2, label=rf"$y_{{\rm crit}}={y_correct:.4f}$")
ax.axhline(y_renorm, ls=":", color="#d62728", lw=1.2, label=rf"$y_R={y_renorm:.4f}$（固定点）")
ax.set_xlabel(r"$\tau$"); ax.set_ylabel("逸度")
ax.set_title("(c) 逸度通道判定"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# (d) p_pair(tau)
ax = axes[1, 0]
ax.plot(ts, pv, lw=2, color="#9467bd", label=r"$p_{\rm pair}(T)$")
ax.axhline(P_C, ls="--", color="#d62728", lw=1, label=r"$p_c=0.5927$")
ax.set_xlabel(r"$\tau$"); ax.set_ylabel(r"$p_{\rm pair}$")
ax.set_title("(d) 配对比例（随 T 降）"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# (e) t(tau) 与上界
ax = axes[1, 1]
for gamma, c in [(1.0, "#2ca02c"), (1.5, "#1f77b4"), (2.0, "#ff7f0e")]:
    tc, ts2, yv2, pv2, tv2, _ = build_curve(gamma)
    ax.plot(ts2, tv2, lw=2, color=c, label=rf"$t(T)$, $\gamma={gamma}$")
ax.axhline(1.0509, ls="--", color="#d62728", lw=1.2, label=r"上界 $m=1$: 1.0509")
ax.axhline(1.0, ls=":", color="gray", lw=1)
ax.set_xlabel(r"$\tau$"); ax.set_ylabel(r"$t$")
ax.set_title(r"(e) $t(T)$ 的温度形状与上界"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

# (f) 笔误可检性条形
ax = axes[1, 2]
labels = [r"$\pi^2/(2\beta)$（正确）", r"$\pi^2\beta/2$（笔误）"]
vals = [y_correct, y_wrong]
bars = ax.bar(labels, vals, color=["#2ca02c", "#d62728"], alpha=0.8)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.001, f"{v:.4f}", ha="center", fontsize=10)
ax.set_ylabel(r"$y_{\rm crit}$")
ax.set_title("(f) R-158 §四 指数量级的可检性")
ax.grid(alpha=0.3, axis="y")

fig.tight_layout()
fig.savefig("环15_逸度通道与t温度单调性.png", dpi=160)
plt.close(fig)

with open("环15_逸度通道与t温度单调性.json", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=2)

print(json.dumps(res, ensure_ascii=False, indent=2))
print("全部断言通过。")
