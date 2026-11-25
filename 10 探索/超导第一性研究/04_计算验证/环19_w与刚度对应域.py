# -*- coding: utf-8 -*-
"""环 19：$w(T)$ 与实验超流刚度的对应域判据（第 151 轮，R-160）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_w与刚度对应域.py"（本目录）
输出：环19_w与刚度对应域.png、环19_w与刚度对应域.json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------- 物理常量（SI，CODATA 2018） ----------------
hb = 1.054571817e-34
mu0 = 4.0 * np.pi * 1e-7
e = 1.602176634e-19
kB = 1.380649e-23

# $\\Upsilon_{2D}=C_{\\Upsilon}\\,d\\,\\lambda_L^{-2}=C_{\\Upsilon}\\,2\\Lambda^{-1}$
C_ups = hb**2 / (2.0 * mu0 * e**2)            # J*m
# $\\Lambda(T_c^-)=C_{\\Lambda}/T_c$
C_lam = np.pi * hb**2 / (4.0 * mu0 * e**2 * kB)   # m*K
# $\\lambda_L^{-2}(T_c^-)=C_{l2}\\,T_c/d$
C_l2 = 8.0 * mu0 * e**2 * kB / (np.pi * hb**2)    # m^-2/(K/m)

# ---------------- Debye 相干权重 ----------------
def w_debye(x, n=4001):
    """x = T/omega_D；w = 2∫_0^1 u tanh(u/(2x)) du（(10B.1)/(10B.4)）"""
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))

def w_arr(x):
    return np.array([w_debye(float(v)) for v in np.ravel(x)])

# ---------------- 断言 ----------------
checks = {}

# A1 常量与解析极限
checks["C_lam_reference"] = C_lam
checks["C_lam_over_0p019613"] = C_lam / 0.019613
checks["C_ups"] = C_ups
assert abs(C_lam / 0.019613 - 1.0) < 5e-3, "C_Lambda 与 19.61 mm*K 不符"

# A2 低温 $1-w$ 的 $T^2$ 标度
xs = np.logspace(-2.0, -1.0, 60)
one_m_w = 1.0 - w_arr(xs)
slope = np.polyfit(np.log(xs), np.log(one_m_w), 1)[0]
checks["lowT_slope_1mw"] = slope
checks["lowT_quadratic_coeff"] = (1.0 - w_debye(0.02)) / 0.02**2
assert 1.95 < slope < 2.05, "1-w 的低温幂次应为 2"
assert abs(checks["lowT_quadratic_coeff"] - np.pi**2 / 3.0) / (np.pi**2 / 3.0) < 5e-3

# A3 Pearl 字典的两种读法之比 = 2x/d（第 152 轮按 c_Lambda=2 更正）
C_london = C_ups / 2.0                    # hbar^2/(4 mu0 e^2)
for d_nm, lam_nm in [(3.0, 529.0), (10.0, 300.0), (5.0, 400.0)]:
    d, lam = d_nm * 1e-9, lam_nm * 1e-9
    ups_pearl = C_ups / lam            # 把报告值读作 Pearl 长度 Lambda
    ups_london = C_london * d / lam**2 # 把报告值读作 London 长度 lambda_L
    checks[f"ratio_pearl_over_london_d{d_nm:.0f}"] = ups_pearl / ups_london
assert abs(checks["ratio_pearl_over_london_d3"] - 2.0 * 529.0 / 3.0) < 1e-9

# A4 BKT 下限：Lambda(0) <= C_lam/T_c；等价 B = T_c*Lambda(0)/C_lam <= 1
B_vals = []
for Tc, Lam_mm in [(1.0, 19.61), (5.0, 3.92), (10.0, 1.96), (10.0, 0.5), (7.0, 5.29e-4)]:
    Lam = Lam_mm * 1e-3
    B = Tc * Lam / C_lam
    B_vals.append(B)
    assert B <= 1.0 + 1e-9, "BKT 下限被违反"
checks["B_examples"] = B_vals
checks["B_critical"] = 1.0 * (C_lam / 1.0) / C_lam

# A5 归一化刚度的带：w(T) >= (T/T_c) w(T_c)（w 凹性推论）
band = {}
for ratio in [3.0, 10.0, 30.0]:
    tc = 1.0 / ratio                       # 以 omega_D=1 为单位，T_c=1/ratio
    ts = np.linspace(0.0, tc, 401)
    wv = w_arr(ts)
    floor = ts / tc * w_debye(tc)
    resid = float(np.min(wv - floor))
    band[str(ratio)] = {"min_margin": resid, "w_Tc": w_debye(tc)}
    assert resid >= -1e-12, "带为空：w 未能在全区间压住下限"
checks["band"] = band

# A6 线性耗竭窗口：c*T <= (pi^2/3) T^2/omega_D^2  <=>  T <= 3 c omega_D^2/pi^2
window = {}
for ratio in [3.0, 10.0, 30.0]:
    om = ratio                             # T_c=1
    for c in [0.02, 0.05, 0.1, 0.2]:
        Tstar = 3.0 * c * om**2 / np.pi**2
        ts = np.linspace(1e-4, Tstar * 1.2, 200)
        lhs = c * ts
        rhs = (np.pi**2 / 3.0) * ts**2 / om**2
        n_lo = np.searchsorted(ts, Tstar * 0.98)
        assert np.all(lhs[:n_lo] >= rhs[:n_lo] - 1e-15)   # T<T*：线性耗竭不低于二次下限
        assert lhs[-1] < rhs[-1]                          # T>T*：线性耗竭低于下限，矛盾
        window[f"om{ratio:.0f}_c{c}"] = float(Tstar)
checks["window"] = window

# ---------------- 图 ----------------
fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.2))

# (a) 普适线 Lambda(Tc)
Tc = np.logspace(-0.3, 1.7, 200)
ax[0, 0].loglog(Tc, C_lam / Tc * 1e3, "k-", lw=2, label=r"$\Lambda(T_c^-)=19.61\,$mm$\cdot$K$/T_c$")
ax[0, 0].fill_between(Tc, C_lam / Tc * 1e3, 1e5, color="red", alpha=0.10, label="违反 BKT 下限")
ax[0, 0].fill_between(Tc, 1e-2, C_lam / Tc * 1e3, color="steelblue", alpha=0.10, label="振幅主导区")
ax[0, 0].set_xlabel(r"$T_c$ [K]")
ax[0, 0].set_ylabel(r"$\Lambda(0)$ [mm]")
ax[0, 0].set_title("(a) Pearl 长度与 $T_c$ 的普适线")
ax[0, 0].legend(fontsize=8, loc="upper right")
ax[0, 0].grid(True, which="both", alpha=0.25)

# (b) 1-w 的标度
xx = np.logspace(-2.2, 0.3, 120)
ax[0, 1].loglog(xx, 1.0 - w_arr(xx), "k-", lw=2, label=r"$1-w$（精确 Debye）")
ax[0, 1].loglog(xx, (np.pi**2 / 3.0) * xx**2, "r--", lw=1.2, label=r"$\frac{\pi^2}{3}x^2$")
ax[0, 1].loglog(xx, 0.12 * xx, "b:", lw=1.2, label=r"$x$（线性参照）")
ax[0, 1].loglog(xx, 0.35 * xx**3, "g:", lw=1.2, label=r"$x^3$（中性 2D 参照）")
ax[0, 1].set_xlabel(r"$x=T/\omega_D$")
ax[0, 1].set_title(r"(b) $w$ 的低温耗竭是 $T^2$")
ax[0, 1].legend(fontsize=8)
ax[0, 1].grid(True, which="both", alpha=0.25)

# (c) 带：w_c*T/Tc <= Upsilon_R/Upsilon_0 <= w(T)
for ratio, col in [(3.0, "C0"), (10.0, "C1"), (30.0, "C2")]:
    tc = 1.0 / ratio
    ts = np.linspace(1e-4, tc, 400)
    up = w_arr(ts)
    lo = ts / tc * w_debye(tc)
    ax[0, 2].plot(ts / tc, lo, col + "-", lw=1.4)
    ax[0, 2].plot(ts / tc, up, col + "--", lw=1.4, label=r"$\omega_D/T_c=%g$" % ratio)
ax[0, 2].set_xlabel(r"$T/T_c$")
ax[0, 2].set_ylabel(r"$\Upsilon_R(T)/\Upsilon_0$")
ax[0, 2].set_title(r"(c) 容许带（实线=下限，虚线=$w$ 上限）")
ax[0, 2].legend(fontsize=8)
ax[0, 2].grid(True, alpha=0.25)

# (d) 线性窗口上界 T_lin*(c)
cc = np.logspace(-2.3, -0.3, 100)
for ratio, col in [(3.0, "C0"), (10.0, "C1"), (30.0, "C2")]:
    ax[1, 0].loglog(cc, 3.0 * cc * ratio**2 / np.pi**2, col + "-", lw=1.6,
                    label=r"$\omega_D/T_c=%g$" % ratio)
ax[1, 0].set_xlabel(r"$c$ [K$^{-1}$]（$1-\Upsilon_R/\Upsilon_0=cT$）")
ax[1, 0].set_ylabel(r"$T_{\rm lin}^*/T_c$")
ax[1, 0].set_title(r"(d) 线性区上界 $T^*=3c\omega_D^2/\pi^2$")
ax[1, 0].legend(fontsize=8)
ax[1, 0].grid(True, which="both", alpha=0.25)

# (e) 两种字典读法的比 2x/d（第 152 轮更正）
dd = np.logspace(-9, -7.5, 100)
ax[1, 1].semilogy(dd * 1e9, 2.0 * 500e-9 / dd, "k-", lw=2)
ax[1, 1].set_xlabel(r"$d$ [nm]")
ax[1, 1].set_ylabel(r"$\Upsilon_{\Lambda}/\Upsilon_{\lambda}$（$=2x/d$，取 $x=500$ nm）")
ax[1, 1].set_title(r"(e) 报告值读作 $\Lambda$ 与读作 $\lambda_L$ 的比")
ax[1, 1].grid(True, which="both", alpha=0.25)

# (f) B = T_c*Lambda(0)/C_lam 的分域
Tc2 = np.logspace(-0.3, 1.7, 100)
for Bv, col in [(1.0, "k"), (0.1, "C1"), (1e-2, "C2"), (1e-3, "C3")]:
    ax[1, 2].loglog(Tc2, Bv * C_lam / Tc2 * 1e3, col + "--", lw=1.3, label=r"$\mathcal{B}=%g$" % Bv)
ax[1, 2].set_xlabel(r"$T_c$ [K]")
ax[1, 2].set_ylabel(r"$\Lambda(0)$ [mm]")
ax[1, 2].set_title(r"(f) BKT 相关度 $\mathcal{B}=T_c\Lambda(0)/19.61$")
ax[1, 2].legend(fontsize=8)
ax[1, 2].grid(True, which="both", alpha=0.25)

plt.tight_layout()
plt.savefig("环19_w与刚度对应域.png", dpi=150)

with open("环19_w与刚度对应域.json", "w", encoding="utf-8") as f:
    json.dump(checks, f, ensure_ascii=False, indent=2)

print(json.dumps(checks, ensure_ascii=False, indent=2))
print("全部断言通过")
