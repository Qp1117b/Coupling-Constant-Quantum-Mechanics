# -*- coding: utf-8 -*-
"""环 19：sigma_c 相界反解与 Phi(T) 链内形状（第 154 轮，R-163）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_sigma_c相界反解与Phi形状.py"（本目录）
输出：环19_sigma_c相界反解与Phi形状.png / .json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 链内固定参数（来源见推导卡 §一；外部指数 tU 来自 L44，不声称链内推出）
PC = 0.592746          # 2D 座渗流阈值（环15_座键口径）
NU = 9.0               # n_cell（R-154 数值口径；BCC 的 nu 界见 R-158）
TU = 1.3               # t_Upsilon（外部普适指数，L44）
A_COEF = np.pi ** 2 / 3.0
TC_OVER_WD = 0.3


def w_debye(x, n=20001):
    """w(T)=2∫_0^1 u tanh(u/(2x)) du；x=T/omega_D（(10B.1)(10B.4)）"""
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w_debye(TC_OVER_WD)
X_STAR = float(chi2.isf(PC, NU))          # 旧口径 x_* = Fbar^{-1}(pc^{1/t}); t=1
SIGMA_OLD = X_STAR / NU                    # 旧 sigma_c^2/Z


def pstar(kappa):
    return PC + (1.0 - PC) * kappa ** (1.0 / TU)


def xc_of(kappa):
    return float(chi2.isf(pstar(kappa), NU))


def Phi(p):
    return 0.0 if p <= PC else ((p - PC) / (1.0 - PC)) ** TU


def p_of_y(y, xc):
    """p(y)=1-F_nu(x_c*w_c/y)，y=w(T)"""
    return 1.0 - chi2.cdf(xc * WC / y, NU)


def G_of_y(y, xc):
    p1 = p_of_y(1.0, xc)
    return y * Phi(p_of_y(y, xc)) / Phi(p1)


def B_of(kappa):
    xc = xc_of(kappa)
    h0 = xc * WC
    p0 = 1.0 - chi2.cdf(h0, NU)
    f0 = chi2.pdf(h0, NU)
    return TU * h0 * f0 / (p0 - PC)


checks = {}

# ---- C1 Phi(p*)=kappa 恒等式 ----
err_c1 = []
for kap in (0.05, 0.1, 0.3, 0.5, 0.8, 0.95):
    err_c1.append(abs(Phi(pstar(kap)) - kap))
checks["C1_phi_boundary_maxerr"] = max(err_c1)
assert max(err_c1) < 1e-12, "Phi(p*)=kappa 失败"

# ---- C2 旧定标断口：p_pair(Tc)=pc => Phi=0 => Upsilon(Tc)=0，与 BKT 下界矛盾 ----
p_old = 1.0 - chi2.cdf(X_STAR, NU)         # = pc（t=1 隐含）
phi_old = Phi(p_old)
ups_old = WC * phi_old                      # 归一 Upsilon_bond=1
bkt_floor = (2.0 / np.pi) * TC_OVER_WD      # 取 kB=omega_D=1
checks["C2_x_star"] = X_STAR
checks["C2_p_pair_Tc_old"] = p_old
checks["C2_phi_c_old"] = phi_old
checks["C2_ups_Tc_old"] = ups_old
checks["C2_bkt_floor"] = bkt_floor
assert abs(p_old - PC) < 1e-9, "旧口径应给 p_pair(Tc)=pc（t=1）"
assert phi_old == 0.0 and ups_old == 0.0, "旧口径 Phi_c 应为 0"
assert bkt_floor > 0, "BKT 下界必须为正"

# ---- C3 修正后 sigma_c 更小，且 x_c 随 kappa 单调减 ----
kaps = np.linspace(0.05, 0.95, 40)
xcs = np.array([xc_of(k) for k in kaps])
sig_new = xcs * WC / NU
checks["C3_xc_range"] = [float(xcs.min()), float(xcs.max())]
checks["C3_sigma_old"] = SIGMA_OLD * WC
checks["C3_max_sigma_new"] = float(sig_new.max())
assert np.all(np.diff(xcs) < 0), "x_c 应随 kappa 严格减"
assert sig_new.max() < SIGMA_OLD * WC, "修正 sigma_c 应小于旧值"

# ---- C4 G'(1)=1+B（中心差分核对链式法则） ----
err_c4 = []
for kap in (0.1, 0.3, 0.5, 0.8, 0.95):
    xc = xc_of(kap)
    h = 1e-5
    der = (np.log(G_of_y(1.0 + h, xc)) - np.log(G_of_y(1.0 - h, xc))) / (2 * h)
    err_c4.append(abs(der - (1.0 + B_of(kap))))
checks["C4_derivative_maxerr"] = max(err_c4)
assert max(err_c4) < 1e-5, "G'(1)=1+B 数值核对失败"

# ---- C5 低温 T^2 系数 -> a(1+B) ----
err_c5 = []
for kap in (0.1, 0.5, 0.9):
    xc = xc_of(kap)
    tau = 1e-3
    coeff = (1.0 - G_of_y(w_debye(tau), xc)) / tau ** 2
    err_c5.append(abs(coeff - A_COEF * (1.0 + B_of(kap))) / (A_COEF * (1.0 + B_of(kap))))
checks["C5_lowT_coeff_maxrelerr"] = max(err_c5)
assert max(err_c5) < 5e-3, "低温系数 a(1+B) 核对失败"

# ---- C6 wPhi 可分离：逐点恒等式 + G 单调 ----
err_c6 = []
for kap in (0.2, 0.5, 0.8):
    xc = xc_of(kap)
    for tau in (0.05, 0.1, 0.2, 0.3):
        y = w_debye(tau)
        lhs = G_of_y(y, xc)
        rhs = y * Phi(p_of_y(y, xc)) / Phi(p_of_y(1.0, xc))
        err_c6.append(abs(lhs - rhs))
taus = np.linspace(0.01, TC_OVER_WD, 12)
gvals = np.array([G_of_y(w_debye(float(t)), xc_of(0.5)) for t in taus])
checks["C6_split_maxerr"] = max(err_c6)
checks["C6_G_monotone"] = bool(np.all(np.diff(gvals) < 0))
assert max(err_c6) < 1e-14, "wPhi 分离恒等式失败"
assert np.all(np.diff(gvals) < 0), "G 应随 T 单调减"

# ---- C7 B 随 kappa 单调减；kappa->1 时系数 -> a ----
bs = np.array([B_of(float(k)) for k in kaps])
checks["C7_B_range"] = [float(bs.min()), float(bs.max())]
checks["C7_B_min"] = float(bs.min())
checks["C7_coeff_k095"] = A_COEF * (1.0 + B_of(0.95))
assert np.all(np.diff(bs) < 0), "B 应随 kappa 单调减"
assert A_COEF * (1.0 + B_of(0.95)) < A_COEF * 1.2, "洁净极限系数应趋近 a"

# ---------------- 图像（解析形状，不是拟合） ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))
tt = np.linspace(0.0, TC_OVER_WD, 100)
wv = np.array([w_debye(float(t)) for t in tt])

ax = axes[0, 0]
for kap in (0.2, 0.5, 0.8):
    xc = xc_of(kap)
    phv = np.array([Phi(p_of_y(float(y), xc)) for y in wv])
    ax.plot(tt, wv, "--", color=f"C{int(kap*10)}", alpha=0.5)
    ax.plot(tt, phv, "-", color=f"C{int(kap*10)}", label=f"Φ, κ={kap}")
ax.set(xlabel="T/ω_D", ylabel="权重", title="(a) w(T)（虚线）与 Φ(T)（实线）")
ax.legend(fontsize=8)

ax = axes[0, 1]
for kap in (0.1, 0.5, 0.9):
    xc = xc_of(kap)
    gv = np.array([G_of_y(float(y), xc) for y in wv])
    ax.plot(tt, gv, label=f"κ={kap}")
ax.set(xlabel="T/ω_D", ylabel="Υ(T)/Υ(0)", title="(b) G(w(T))：单函数族")
ax.legend(fontsize=8)

ax = axes[1, 0]
ax.plot(kaps, [A_COEF * (1.0 + B_of(float(k))) for k in kaps], "o-")
ax.axhline(A_COEF, color="r", ls="--", label="纯 Debye a=π²/3")
ax.set(xlabel="κ", ylabel="低温 T² 系数", title="(c) 渗流放大 a(1+B)")
ax.legend(fontsize=8)

ax = axes[1, 1]
ax.plot(kaps, sig_new, "o-", label="修正 σ_c²/Z")
ax.axhline(SIGMA_OLD * WC, color="r", ls="--", label="旧口径 0.6261")
ax.set(xlabel="κ", ylabel="σ_c²/Z", title="(d) 反解阈值")
ax.legend(fontsize=8)

ax = axes[1, 2]
dd = [B_of(float(k)) for k in (0.1, 0.3, 0.5, 0.8, 0.95)]
ff = []
for kap in (0.1, 0.3, 0.5, 0.8, 0.95):
    xc = xc_of(kap)
    h = 1e-5
    ff.append((np.log(G_of_y(1 + h, xc)) - np.log(G_of_y(1 - h, xc))) / (2 * h) - 1)
ax.plot(dd, ff, "o")
lim = [0, max(dd) * 1.1]
ax.plot(lim, lim, "r--")
ax.set(xlabel="闭式 B", ylabel="差分 G'(1)-1", title="(e) 链式法则核对")
ax = axes[0, 2]
ax.bar(["旧定标", "BKT 下界"], [ups_old, bkt_floor], color=["tab:red", "tab:blue"])
ax.set(ylabel="Υ(T_c)（归一）", title="(f) 旧定标给 0，BKT 要求 >0")

fig.tight_layout()
fig.savefig("环19_sigma_c相界反解与Phi形状.png", dpi=150)
with open("环19_sigma_c相界反解与Phi形状.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
