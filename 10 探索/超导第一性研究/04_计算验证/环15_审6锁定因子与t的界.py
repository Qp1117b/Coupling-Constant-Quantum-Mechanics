# -*- coding: utf-8 -*-
"""
环 15：审-6 同步概率的锁定因子、审-4 三量（Z、n_cell、t）的界（R-158）
七段数值核查，全部为解析式的数值对照，不做拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/环15_审6锁定因子与t的界.py"
"""
import json
import numpy as np
from scipy.stats import chi2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

P_C = 0.592746          # 2D 方格座渗流阈值（L31）
BETA_KT = 0.89294       # k_B T_BKT / Upsilon（方格 XY 标准）
TWO_PI = 2.0 * np.pi
res = {}

# ---------- 基本函数 ----------
def fugacity(x):
    """x = k_B T / Upsilon；y = 2*pi*exp(-(pi^2/2)/x)。"""
    x = np.asarray(x, dtype=float)
    return TWO_PI * np.exp(-(np.pi**2 / 2.0) / x)

def t_eff(p, y):
    """(15L.4)：t = 1 + ln(1-y)/ln p。"""
    return 1.0 + np.log1p(-np.asarray(y, dtype=float)) / np.log(p)

def t_from_threshold(p_c, y, m=1.0):
    """(15L.7)：t = ln p_c / (ln p_c - m ln(1-y))。"""
    return np.log(p_c) / (np.log(p_c) - m * np.log1p(-np.asarray(y, dtype=float)))

def p_pair_thr(p_c, y, m=1.0):
    return p_c / (1.0 - np.asarray(y, dtype=float))**m

def eps_nu(nu, t):
    """epsilon_nu = 2 x f_nu(x)/p，x 由 1-F_nu(x)=p_c^(1/t) 解出。"""
    p_star = P_C**(1.0 / t)
    x = chi2.ppf(1.0 - p_star, nu)
    f = chi2.pdf(x, nu)
    p = 1.0 - chi2.cdf(x, nu)
    return x, f, p, 2.0 * x * f / p

# ---------- A：y(T) 形状 ----------
x_scan = np.linspace(0.10, 1.60, 400)
y_scan = fugacity(x_scan)
assert np.all(np.diff(y_scan) > 0), "y(T) 应严格增"
assert fugacity(0.05) < 1e-15, "y(0+) 应趋于 0"
assert np.all((y_scan > 0) & (y_scan < 1)), "0<y<1"
res["y_strict_increasing"] = bool(np.all(np.diff(y_scan) > 0))
res["y_at_small_x"] = float(fugacity(0.05))

# ---------- B：y_crit 与 Upsilon 无关 ----------
y_crit = fugacity(BETA_KT)
y_ups = []
for U in (0.5, 1.0, 3.0, 10.0):
    E_c = (np.pi**2 / 2.0) * U          # XY 核能
    kT_bkt = BETA_KT * U                # k_B T_BKT
    y_ups.append(TWO_PI * np.exp(-E_c / kT_bkt))
y_ups = np.array(y_ups)
assert np.max(np.abs(y_ups - y_crit)) < 1e-15, "y_crit 应与 Upsilon 无关"
assert 0.02 < y_crit < 0.03, f"y_crit 量级异常 {y_crit}"
res["y_crit"] = float(y_crit)
res["y_crit_upsilon_spread"] = float(np.max(np.abs(y_ups - y_crit)))
res["p_lock_at_Tc"] = float(1.0 - y_crit)

# ---------- C：指数恒等式 ----------
worst = 0.0
for p in np.linspace(0.30, 0.90, 25):
    for y in np.linspace(0.0, 0.05, 21):
        tt = 1.0 + np.log1p(-y) / np.log(p)
        lhs = np.exp(tt * np.log(p))
        rhs = p * (1.0 - y)
        worst = max(worst, abs(lhs - rhs) / abs(rhs))
assert worst < 1e-13, f"指数恒等式残差 {worst}"
res["exponent_identity_residual"] = float(worst)

# ---------- D：t 的性质与上界 ----------
assert abs(t_eff(0.6, 0.0) - 1.0) < 1e-15, "t(0) 应为 1"
y_sweep = np.linspace(1e-8, 0.2, 300)
for p in (0.5, 0.6, 0.7, 0.8):
    tv = t_eff(p, y_sweep)
    assert np.all(tv >= 1.0), "t 应 >= 1"
    assert np.all(np.diff(tv) > 0), "t 应随 y 严格增"
t_m1 = t_from_threshold(P_C, y_crit, m=1.0)
t_m2 = t_from_threshold(P_C, y_crit, m=2.0)
A = abs(np.log(P_C))
d = abs(np.log1p(-y_crit))
bound1 = A / (A - d)
bound2 = A / (A - 2.0 * d)
assert abs(t_m1 - bound1) < 1e-12 and abs(t_m2 - bound2) < 1e-12, "上界式不自洽"
# 线性项与精确值之差应为 (d/A)^2 量级
lead1 = 1.0 + d / A
assert 0.0 < bound1 - lead1 < 0.005, "线性项偏差量级异常"
assert 1.0 < t_m1 < 1.1 and 1.0 < t_m2 < 1.2, "t 上界量级异常"
res["t_at_Tc_m1"] = float(t_m1)
res["t_at_Tc_m2"] = float(t_m2)
res["t_zero"] = float(t_eff(0.6, 0.0))

# ---------- E：阈值关系 ----------
for m in (1.0, 2.0):
    p_thr = p_pair_thr(P_C, y_crit, m=m)
    tt = t_from_threshold(P_C, y_crit, m=m)
    assert p_thr >= P_C, "p_pair^thr 应 >= p_c"
    # 自洽：p_thr^t == p_c
    resid = abs(np.exp(tt * np.log(p_thr)) - P_C)
    assert resid < 1e-12, f"阈值自洽残差 {resid}"
    res[f"p_pair_thr_m{int(m)}"] = float(p_thr)
    res[f"threshold_residual_m{int(m)}"] = float(resid)

# ---------- F：n_cell 的界 ----------
def neff_from_corr(rho):
    z = rho.shape[0]
    return z**2 / np.sum(rho**2)

rng = np.random.default_rng(20261125)
samples = []
# (i) 因子模型：rho_ij = lam_i lam_j（秩 1，正定）
for _ in range(2000):
    lam = rng.uniform(0.0, 1.0, 8)
    rho = np.outer(lam, lam)
    np.fill_diagonal(rho, 1.0)
    samples.append(neff_from_corr(rho))
# (ii) 随机正定矩阵归一为相关矩阵
for _ in range(2000):
    A = rng.normal(size=(8, 8))
    S = A @ A.T
    d = np.sqrt(np.diag(S))
    rho = S / np.outer(d, d)
    np.fill_diagonal(rho, 1.0)
    samples.append(neff_from_corr(rho))
samples = np.array(samples)
assert np.all(samples >= 1.0 - 1e-12), "n_cell 应 >= 1"
assert np.all(samples <= 8.0 + 1e-12), "n_cell 应 <= z = 8"
assert samples.mean() > 1.0, "n_cell 不应恒为 1"
# 等相相关闭式：n = z/(1+(z-1)r^2)
r_eq = np.linspace(-1.0 / 7.0, 1.0, 201)
n_eq = 8.0 / (1.0 + 7.0 * r_eq**2)
assert np.all(n_eq >= 1.0 - 1e-12) and np.all(n_eq <= 8.0 + 1e-12), "等相相关界失败"
res["neff_min"] = float(samples.min())
res["neff_max"] = float(samples.max())
res["neff_mean"] = float(samples.mean())
res["nu9_violates_bcc"] = bool(9 > 8)

# ---------- G：epsilon_nu 表与 Z 的代数等价 ----------
rows = []
for nu, tt in [(9, 1.0), (8, 1.0), (8, t_m1), (8, t_m2)]:
    x, f, p, eps = eps_nu(nu, tt)
    rows.append(dict(nu=int(nu), t=float(tt), x=float(x), eps=float(eps)))
eps_ref = rows[0]["eps"]
assert rows[1]["eps"] < eps_ref, "nu=8 应给更小 epsilon"
assert rows[2]["eps"] < rows[1]["eps"], "t>1 应继续压低 epsilon"
assert rows[3]["eps"] < rows[2]["eps"], "t 更大 epsilon 更小"
for r in rows:
    r["rel_vs_ref"] = (r["eps"] - eps_ref) / eps_ref
# r ∝ 1/epsilon：相对移动
for r in rows:
    r["r_rel_shift"] = eps_ref / r["eps"] - 1.0
res["eps_rows"] = rows

# Z 三式前两式的代数等价（任意输入）
c_eps, omega_D, M, c_s = 0.34, 600.0, 4.5e-26, 4.0e3
hbar = 1.054571817e-34
Q = omega_D / c_s
u2 = 3.0 * hbar / (4.0 * M * omega_D)
Z_a = 0.375 * c_eps**2 * hbar * omega_D / (M * c_s**2)
Z_b = 0.5 * c_eps**2 * Q**2 * u2
assert abs(Z_a - Z_b) / Z_a < 1e-15, "Z 两式不代数等价"
res["Z_identity_residual"] = float(abs(Z_a - Z_b) / Z_a)

# ---------- 图 ----------
fig, axes = plt.subplots(2, 2, figsize=(12.4, 9.0))

ax = axes[0, 0]
ax.plot(x_scan, y_scan, lw=2, color="#1f77b4", label=r"$y=2\pi e^{-(\pi^2/2)\Upsilon/(k_BT)}$")
ax.plot(x_scan, 1.0 - y_scan, lw=2, color="#d62728", label=r"$p_{\rm lock}=1-y$")
ax.axvline(BETA_KT, ls="--", color="gray", lw=1)
ax.text(BETA_KT + 0.02, 0.05, r"$k_BT_{\rm BKT}/\Upsilon$", color="gray")
ax.set_xlabel(r"$x=k_BT/\Upsilon$")
ax.set_ylabel("概率")
ax.set_title("(a) 涡旋逸度与锁定因子")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

ax = axes[0, 1]
y_line = np.linspace(1e-6, 0.08, 300)
for p, c in [(0.5, "#2ca02c"), (0.6, "#1f77b4"), (0.7, "#ff7f0e")]:
    ax.plot(y_line, t_eff(p, y_line), lw=2, color=c, label=rf"$p_{{\rm pair}}={p}$")
ax.axhline(bound1, ls="--", color="#d62728", lw=1, label=rf"上界 $m=1$: {bound1:.4f}")
ax.axhline(bound2, ls=":", color="#8c564b", lw=1, label=rf"上界 $m=2$: {bound2:.4f}")
ax.axvline(y_crit, ls="-.", color="gray", lw=1)
ax.text(y_crit + 0.002, 1.002, r"$y_{\rm crit}$", color="gray", fontsize=9)
ax.set_xlabel("$y$")
ax.set_ylabel("$t$")
ax.set_ylim(0.995, 1.20)
ax.set_title(r"(b) 指数 $t$ 的温度依赖与普适上界")
ax.legend(fontsize=8)
ax.grid(alpha=0.3)

ax = axes[1, 0]
pp = np.linspace(0.0, 1.0, 400)
for yy, c, lab in [(0.0, "gray", r"$y=0$（$t=1$）"), (y_crit, "#1f77b4", rf"$y=y_{{\rm crit}}={y_crit:.4f}$")]:
    ax.plot(pp, pp * (1 - yy), lw=2, color=c, label=lab)
ax.axhline(P_C, ls="--", color="#d62728", lw=1)
ax.axvline(P_C, ls="--", color="#d62728", lw=1)
ax.plot([P_C], [P_C], "o", color="#d62728", ms=6)
ax.annotate(r"$T_{\rm sync}$", xy=(P_C, P_C), xytext=(P_C + 0.04, P_C - 0.10),
            arrowprops=dict(arrowstyle="->", color="#d62728"), color="#d62728")
ax.set_xlabel(r"$p_{\rm pair}$")
ax.set_ylabel(r"$p_{\rm sync}$")
ax.set_title("(c) 两阶段：同步曲线恒在配对曲线下方")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

ax = axes[1, 1]
ax.hist(samples, bins=40, color="#1f77b4", alpha=0.75, edgecolor="k", lw=0.3)
ax.axvline(8.0, ls="--", color="#d62728", lw=2, label=r"$z=8$（BCC 上界）")
ax.axvline(9.0, ls=":", color="#8c564b", lw=2, label=r"$\nu=9$（越界）")
ax.set_xlabel(r"$n_{\rm cell}=z^2/\sum_{ee'}\rho_{ee'}^2$")
ax.set_ylabel("计数")
ax.set_title("(d) 局域读出的有效自由度")
ax.legend(fontsize=9)
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("环15_审6锁定因子与t的界.png", dpi=160)
plt.close(fig)

with open("环15_审6锁定因子与t的界.json", "w", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=2)

print(json.dumps(res, ensure_ascii=False, indent=2))
print("全部七段断言通过。")
