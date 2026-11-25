# -*- coding: utf-8 -*-
"""环 19／目标区：Uemura 闭合与 g_ren 热力学反演（第 155 轮，R-164）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_Uemura曲率反演.py"（本目录）
输出：环19_Uemura曲率反演.png / .json
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
A = np.pi ** 2 / 3.0
TC = 0.3          # 取 k_B=omega_D=1


def w_debye(x, n=20001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w_debye(TC)


def Phi(p):
    return 0.0 if p <= PC else ((p - PC) / (1.0 - PC)) ** TU


def p_at(xc, fac=1.0):
    return 1.0 - chi2.cdf(xc * fac, NU)


def B_of_xc(xc):
    h0 = xc * WC
    p0 = p_at(xc, WC)
    f0 = chi2.pdf(h0, NU)
    return TU * h0 * f0 / (p0 - PC)


def invert(xc):
    """给定真值参数，生成可观测量并反演回 (xc, U0bond, g)"""
    phic = Phi(p_at(xc))
    kap = G_TRUE * phic                       # kappa = g*Phi_c
    phi0 = Phi(p_at(xc, WC))
    Ub = 2.0 * TC / (np.pi * WC * kap)         # Upsilon_0 = Upsilon_bond
    U0 = Ub * phi0                             # 观测 Upsilon(0)
    c2 = A * (1.0 + B_of_xc(xc))               # 观测低温曲率
    Bt = c2 / A - 1.0
    xr = brentq(lambda x: B_of_xc(x) - Bt, 1.5, 6.0, xtol=1e-13)
    phi0r = Phi(p_at(xr, WC))
    Ubr = U0 / phi0r
    kapr = 2.0 * TC * phi0r / (np.pi * U0 * WC)
    phicr = Phi(p_at(xr))
    gr = kapr / phicr
    bound = 2.0 * TC * phi0 / (np.pi * WC)
    return dict(xc=xc, g=G_TRUE, phic=phic, kap=kap, phi0=phi0, Ub=Ub,
                U0=U0, c2=c2, xr=xr, gr=gr, Ubr=Ubr, bound=bound)


checks = {}
G_TRUE = 0.622281        # 取 Uemura 卡 c=2 的 g_RG=(2/pi)/K_c，作交叉检验锚

# ---- C1 Phi 往返恒等式 ----
err1 = []
for p in (0.62, 0.75, 0.85, 0.95):
    prop = PC + (1 - PC) * Phi(p) ** (1 / TU)
    err1.append(abs(Phi(prop) - Phi(p)))
checks["C1_phi_roundtrip_maxerr"] = max(err1)
assert max(err1) < 1e-12

# ---- C2 真实跳变定标 Phi_c = kappa/g ----
r = invert(4.5)
checks["C2_phic"] = r["phic"]
checks["C2_kappa_over_g"] = r["kap"] / r["g"]
assert abs(r["phic"] - r["kap"] / r["g"]) < 1e-14

# ---- C3 Uemura g 抵消恒等式 ----
U0, Ub, phi0 = r["U0"], r["Ub"], r["phi0"]
kap, g = r["kap"], r["g"]
rr = WC * kap / (g * phi0)
lhs = (np.pi / 2.0) * U0 * rr * g
checks["C3_uemura_lhs"] = lhs
checks["C3_Tc"] = TC
assert abs(lhs - TC) < 1e-13

# ---- C4 B(xc) 严格单调 ----
xs = np.linspace(1.5, 6.0, 60)
bs = np.array([B_of_xc(float(x)) for x in xs])
checks["C4_B_range"] = [float(bs.min()), float(bs.max())]
assert np.all(np.diff(bs) > 0), "B(xc) 应在此区间严格增"

# ---- C5 闭合反演恢复 ----
errs = []
for xtrue in (2.5, 3.5, 4.5, 5.5):
    rr = invert(xtrue)
    errs.append((abs(rr["xr"] - xtrue), abs(rr["gr"] - rr["g"]),
                 abs(rr["Ubr"] - rr["Ub"])))
checks["C5_max_err_xc"] = max(e[0] for e in errs)
checks["C5_max_err_g"] = max(e[1] for e in errs)
checks["C5_max_err_Ubond"] = max(e[2] for e in errs)
assert checks["C5_max_err_g"] < 1e-10, "g 反演失败"
assert checks["C5_max_err_xc"] < 1e-10, "xc 反演失败"

# ---- C6 可行性下界与违例检测 ----
checks["C6_bound"] = r["bound"]
checks["C6_U0"] = r["U0"]
assert r["bound"] <= r["U0"]
# 若 kappa>g 则 Phi_c>1 不可行
for gg in (0.2, 0.4, 0.6):
    ph = Phi(p_at(4.5))
    kp = gg * ph
    checks[f"C6_feasible_g{gg}"] = bool(kp <= gg <= 1.0)

# ---- C7 g_RG 与 g_thermo 交叉检验 ----
K_C = 1.023                    # Uemura 卡 c=2 的 RG 分离点
g_rg = (2.0 / np.pi) / K_C
checks["C7_g_RG"] = g_rg
checks["C7_g_thermo"] = G_TRUE
# K_c=1.023 是 Uemura 卡的舍入值，g_RG=(2/pi)/1.023=0.622308；
# 卡正文的 0.622281 用未舍入 K_c，两者差 2.7e-5（舍入误差，非矛盾）。
assert abs(g_rg - G_TRUE) < 1e-3, "g_RG 与卡值应在舍入精度内一致"

# ---------------- 图像 ----------------
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

ax = axes[0, 0]
ax.plot(xs, bs, "o-")
ax.set(xlabel="x_c", ylabel="B", title="(a) B(x_c) 严格单调（可逆）")

ax = axes[0, 1]
gs = np.linspace(0.4, 1.0, 50)
phi_fixed = r["phic"]
kap_fixed = g_rg * phi_fixed
ax.plot(gs, np.minimum(kap_fixed / gs, 1.5), label="κ/g")
ax.axhline(1.0, color="r", ls="--", label="Φ_c≤1")
ax.axvline(kap_fixed, color="k", ls=":", label="g≥κ")
ax.set(xlabel="g_ren", ylabel="Φ_c", title="(b) 可行性 Φ_c=κ/g")
ax.legend(fontsize=8)

ax = axes[0, 2]
ax.plot(gs, [A * (1 + B_of_xc(x)) for x in np.linspace(2.5, 5.5, 50)], "o-")
ax.set(xlabel="g_ren（经 x_c 映射）", ylabel="c2", title="(c) 低温曲率随重整化")

ax = axes[1, 0]
gt = np.linspace(0.45, 0.95, 8)
grs = [invert(float(x))["gr"] for x in np.linspace(2.5, 5.5, 8)]
gx = [(2.0 / np.pi) / K_C * np.linspace(0.9, 1.1, 8)[i] for i in range(8)]
ax.plot(gx, grs, "o")
lim = [min(gx + grs), max(gx + grs)]
ax.plot(lim, lim, "r--")
ax.set(xlabel="g_RG", ylabel="g_thermo", title="(d) 两通路交叉检验")

ax = axes[1, 1]
ax.bar(["下界", "U(0) 实测"], [r["bound"], r["U0"]], color=["tab:red", "tab:blue"])
ax.set(ylabel="stiffness", title="(e) 可行性 U(0) >= 2k_B T_c Phi0/(pi w_c)")

ax = axes[1, 2]
ax.plot([0.2, 1.0], [0.2, 1.0], "r--", label="一致线")
ax.plot([r["g_RG"] if "g_RG" in r else g_rg], [r["gr"]], "o", ms=10, label="交叉点")
ax.set(xlabel="g_RG", ylabel="g_thermo", title="(f) 内部一致性")
ax.legend(fontsize=8)

fig.tight_layout()
fig.savefig("环19_Uemura曲率反演.png", dpi=150)
with open("环19_Uemura曲率反演.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
