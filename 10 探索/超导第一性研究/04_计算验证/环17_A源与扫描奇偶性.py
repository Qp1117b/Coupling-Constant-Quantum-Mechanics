# -*- coding: utf-8 -*-
"""
环 17：A 源的静态 no-go、扫描奇偶性与可解域统一判据（R-157）
六段数值核查，全部为解析式的数值对照，不做拟合。
运行：python "10 探索/超导第一性研究/04_计算验证/环17_A源与扫描奇偶性.py"
"""
import json
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

EPS_NU = 2.5929          # R-155 的尾部弹性，示意值
C_DEN = 1.0              # 自洽方程分母常数，示意值
TWO_PI2_3 = 2.0 * np.pi**2 / 3.0

results = {}

# ---------- 基本函数（无量纲 u = T / omega_D） ----------
def w_of_u(u):
    """w(u) = 2 ∫_0^1 x tanh(x/(2u)) dx，w(0)=1。"""
    if u <= 0:
        return 1.0
    val, _ = quad(lambda x: 2.0 * x * np.tanh(x / (2.0 * u)), 0.0, 1.0,
                  limit=400, epsabs=1e-13, epsrel=1e-12)
    return val

def w_grid(u):
    return np.array([w_of_u(float(x)) for x in np.atleast_1d(u)])

def dlnw_du(u, h_rel=1e-4):
    h = h_rel * u
    return (np.log(w_of_u(u + h)) - np.log(w_of_u(u - h))) / (2.0 * h)

def alpha_ins(u, alpha_dim=1e-5):
    """绝缘体：alpha_V = alpha_dim * u^3（alpha_dim 为无量纲非谐参数）。"""
    return alpha_dim * np.asarray(u, dtype=float)**3

def alpha_metal(u, a1=1e-4, a3=1e-5):
    u = np.asarray(u, dtype=float)
    return a1 * u + a3 * u**3

def alpha_sat(u, alpha_sat_val=1e-5):
    """高温：alpha_V -> const（Dulong-Petit 区）。"""
    return alpha_sat_val * np.ones_like(np.asarray(u, dtype=float))

def r_material(u, alpha_fun):
    u_arr = np.atleast_1d(np.asarray(u, dtype=float))
    a = alpha_fun(u_arr)
    a = np.atleast_1d(np.asarray(a, dtype=float))
    d = np.array([abs(dlnw_du(float(x))) for x in u_arr])
    out = 2.0 * a / (3.0 * EPS_NU * d)
    return float(out[0]) if np.ndim(u) == 0 else out

# ---------- A：w(0)=1 与严格减 ----------
u_w = np.logspace(-3, 1.2, 220)
w_vals = w_grid(u_w)
assert abs(w_of_u(1e-6) - 1.0) < 1e-9, "w(0) 应为 1"
assert np.all(np.diff(w_vals) < 0), "w 应严格减"
results["w0"] = float(w_of_u(1e-9))
results["w_monotone"] = bool(np.all(np.diff(w_vals) < 0))

# ---------- B：|dlnw/du| 两支渐近 ----------
u_lo, u_hi = 0.01, 20.0
ratio_lo = abs(dlnw_du(u_lo)) / (TWO_PI2_3 * u_lo)
ratio_hi = abs(dlnw_du(u_hi)) * u_hi
assert abs(ratio_lo - 1.0) < 0.01, f"低温渐近偏差 {ratio_lo}"
assert abs(ratio_hi - 1.0) < 0.01, f"高温渐近偏差 {ratio_hi}"
results["lowT_slope_ratio"] = float(ratio_lo)
results["highT_slope_ratio"] = float(ratio_hi)

# ---------- C：r 的两支斜率 ----------
u_fit_lo = np.logspace(np.log10(0.008), np.log10(0.04), 24)
u_fit_hi = np.logspace(np.log10(4.0), np.log10(20.0), 24)
r_ins_lo = r_material(u_fit_lo, alpha_ins)
r_ins_hi = r_material(u_fit_hi, alpha_sat)
r_met_lo = r_material(u_fit_lo, alpha_metal)
slope_ins_lo = np.polyfit(np.log(u_fit_lo), np.log(r_ins_lo), 1)[0]
slope_ins_hi = np.polyfit(np.log(u_fit_hi), np.log(r_ins_hi), 1)[0]
assert abs(slope_ins_lo - 2.0) < 0.02, f"绝缘体低温斜率 {slope_ins_lo}"
assert abs(slope_ins_hi - 1.0) < 0.02, f"绝缘体高温斜率 {slope_ins_hi}"
metal_flat = r_met_lo[-1] / r_met_lo[0]
assert abs(metal_flat - 1.0) < 0.05, f"金属低温 r 应近常数，比 {metal_flat}"
results["slope_ins_low"] = float(slope_ins_lo)
results["slope_ins_high"] = float(slope_ins_hi)
results["metal_low_flat_ratio"] = float(metal_flat)

# ---------- D/E：扫描奇偶与统一式 ----------
def s_raw(u, alam, alpha_fun, Tdot):
    a = alpha_fun(u)
    g = EPS_NU * (dlnw_du(u) * Tdot)  # dlnw_du = w'/w，故 g = eps*(w'/w)*Tdot
    mu = a * Tdot / 3.0
    return 2.0 * g / (C_DEN * (g * alam + 2.0 * mu))

def s_unified(u, alam, alpha_fun):
    return 2.0 / (C_DEN * (alam - r_material(u, alpha_fun)))

parity_res, unified_res = [], []
for u in [0.02, 0.05, 0.1, 0.3, 0.8]:
    for alam in [0.05, 0.2, 0.571]:
        s_plus = s_raw(u, alam, alpha_ins, +1.0)
        s_minus = s_raw(u, alam, alpha_ins, -1.0)
        parity_res.append(abs(s_plus - s_minus) / max(abs(s_plus), 1e-30))
        su = s_unified(u, alam, alpha_ins)
        unified_res.append(abs(s_plus - su) / max(abs(su), 1e-30))
assert max(parity_res) < 1e-12, f"扫描奇偶残差 {max(parity_res)}"
assert max(unified_res) < 1e-13, f"统一式残差 {max(unified_res)}"
results["parity_max_rel_res"] = float(max(parity_res))
results["unified_max_rel_res"] = float(max(unified_res))

# ---------- F：s(T) 低温极限与 T_x 发散（强非谐示意） ----------
alpha_dim_strong = 0.5
def alpha_strong(u):
    return alpha_dim_strong * np.asarray(u, dtype=float)**3

u_lo_test = 1e-3
u_fine = u_lo_test + np.arange(6) * 2e-4
# 低温极限：r→0，s→2/(C alam)
alam_lim = 0.571
s_lo = np.array([s_unified(u, alam_lim, alpha_strong) for u in u_fine])
lim_val = 2.0 / (C_DEN * alam_lim)
rel_lim = np.max(np.abs(s_lo - lim_val) / lim_val)
assert rel_lim < 1e-4, f"低温极限相对偏差 {rel_lim}"
results["lowT_limit_rel_err"] = float(rel_lim)
results["lowT_limit_value"] = float(lim_val)

# 找 T_x：r(u) = alam（强非谐、alam 较小）
alam_tx = 0.02
u_grid = np.logspace(-3, 1.0, 600)
r_grid = r_material(u_grid, alpha_strong)
idx = np.where(r_grid >= alam_tx)[0]
assert len(idx) > 0, "强非谐示意下应存在 T_x"
u_tx = brentq(lambda u: r_material(u, alpha_strong) - alam_tx, u_grid[idx[0]-1], u_grid[idx[0]])
s_near_tx = s_unified(u_tx * (1.0 - 2e-4), alam_tx, alpha_strong)
assert s_near_tx > 1e5, f"T_x^- 发散不足：{s_near_tx}"
results["Tx_u_strong"] = float(u_tx)
results["s_near_Tx"] = float(s_near_tx)

# 真实弱非谐：r_max 与 alam 比较（alpha_V 在 u>1 饱和，Debye 示意）
def alpha_real(u):
    u = np.asarray(u, dtype=float)
    return 1e-5 * np.minimum(u**3, 1.0)

r_real = r_material(u_grid, alpha_real)
r_real_max = float(np.max(r_real))
assert r_real_max < 0.571, f"弱非谐 r_max 应远小于 alam，得 {r_real_max}"
results["r_real_max"] = r_real_max

# ---------- G：静态分量 no-go ----------
t = np.linspace(0.0, 2.0 * np.pi, 400)
sdyn2 = 1.0 + 0.1 * np.sin(t)
c_static = 0.37
d_sdyn = np.gradient(sdyn2, t)
d_total = np.gradient(sdyn2 + c_static, t)
static_res = float(np.max(np.abs(d_total - d_sdyn)))
assert static_res < 1e-10
results["static_component_deriv_diff"] = static_res

# ---------- H：缺陷激活率 vs 仿射率 ----------
E_act = 100.0  # K，示意
def act_rate(T):
    return (E_act / T**2) * np.exp(-E_act / T)
def aff_rate(T):
    return T**3  # |A|/s^2 = 2|mu| ∝ alpha_V ∝ T^3（绝缘体低温）
T_list = np.array([3.0, 10.0, 50.0])
ratio_act = np.array([act_rate(T) / aff_rate(T) for T in T_list])
assert ratio_act[0] < 1e-5 * float(np.max(ratio_act)), f"激活支应指数冻结：{ratio_act}"
results["activation_affine_ratio"] = ratio_act.tolist()

# ---------- I：降温 A<0 与斜率 A/g ----------
u_a = np.logspace(np.log10(0.01), np.log10(0.05), 20)
A_over_s2 = np.array([2.0 * abs(alpha_ins(u) * (-1.0) / 3.0) for u in u_a])  # |2 mu|, Tdot=-1
g_over_dotT = np.array([EPS_NU * abs(dlnw_du(u)) / w_of_u(u) for u in u_a])
slope_A = np.polyfit(np.log(u_a), np.log(A_over_s2), 1)[0]
slope_g = np.polyfit(np.log(u_a), np.log(g_over_dotT), 1)[0]
assert abs(slope_A - 3.0) < 0.02, f"A 斜率 {slope_A}"
assert abs(slope_g - 1.0) < 0.02, f"g 斜率 {slope_g}"
mu_cool = alpha_ins(0.05) * (-1.0) / 3.0
assert mu_cool < 0.0, "降温 mu 应为负"
results["A_slope"] = float(slope_A)
results["g_slope"] = float(slope_g)
results["mu_cooling_sign"] = float(np.sign(mu_cool))

# ---------- 作图 ----------
fig, axes = plt.subplots(2, 3, figsize=(16.5, 9.0))

ax = axes[0, 0]
ax.semilogx(u_w, w_vals, color="#1f77b4", lw=2, label=r"$w(u)$")
ax.set_xlabel(r"$u=T/\omega_D$")
ax.set_ylabel(r"$w$")
ax.set_title("(a) 相干权重 $w(u)$：$w(0)=1$，严格减")
ax.axhline(1.0, color="gray", ls=":", lw=1)
ax.legend()
ax.grid(alpha=0.3)

ax = axes[0, 1]
ax.loglog(u_fit_lo, r_ins_lo, "o", ms=4, color="#d62728", label="绝缘体 低温")
ax.loglog(u_fit_lo, r_ins_lo[0] * (u_fit_lo / u_fit_lo[0])**2, "k--", lw=1.2, label=r"$\propto u^2$")
ax.loglog(u_fit_hi, r_ins_hi, "s", ms=4, color="#2ca02c", label="绝缘体 高温")
ax.loglog(u_fit_hi, r_ins_hi[0] * (u_fit_hi / u_fit_hi[0]), "k:", lw=1.2, label=r"$\propto u$")
ax.loglog(u_fit_lo, r_met_lo, "^", ms=4, color="#9467bd", label="金属 低温（近常）")
ax.set_xlabel(r"$u$"); ax.set_ylabel(r"$r(T)$")
ax.set_title("(b) 材料率比两支斜率：2 / 常数 / 1")
ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")

ax = axes[0, 2]
for alam, color in zip([0.02, 0.05, 0.2], ["#d62728", "#ff7f0e", "#2ca02c"]):
    uu = np.linspace(1e-3, 1.0, 600)
    rr = r_material(uu, alpha_strong)
    ss = 2.0 / (C_DEN * (alam - rr))
    mask = ss > 0
    ax.plot(uu[mask], np.minimum(ss[mask], 50), color=color, lw=2, label=fr"$a\lambda={alam}$")
ax.set_ylim(0, 50)
ax.set_xlabel(r"$u$"); ax.set_ylabel(r"$s$")
ax.set_title(r"(c) $s=2/[C(a\lambda-r)]$：$T_x^-$ 发散（强非谐示意）")
ax.legend(); ax.grid(alpha=0.3)

ax = axes[1, 0]
uu = np.linspace(0.02, 0.9, 120)
for alam in [0.05, 0.2, 0.571]:
    sp = np.array([s_raw(u, alam, alpha_ins, +1.0) for u in uu])
    sm = np.array([s_raw(u, alam, alpha_ins, -1.0) for u in uu])
    ax.plot(uu, sp, "-", lw=2.5, label=fr"$+\dot T$, $a\lambda={alam}$")
    ax.plot(uu, sm, "--", lw=1.2, label=fr"$-\dot T$, $a\lambda={alam}$")
ax.set_xlabel(r"$u$"); ax.set_ylabel(r"$s$")
ax.set_title(r"(d) 扫描奇偶：$s(+\dot T)=s(-\dot T)$")
ax.legend(fontsize=7); ax.grid(alpha=0.3)

ax = axes[1, 1]
ax.loglog(u_a, A_over_s2, "o-", ms=4, color="#d62728", label=r"$|A|/s^2=2|\mu|$")
ax.loglog(u_a, g_over_dotT, "s-", ms=4, color="#1f77b4", label=r"$|g|/|\dot T|$")
ax.loglog(u_a, A_over_s2[0] * (u_a / u_a[0])**3, "k--", lw=1.2, label=r"$\propto u^3$")
ax.loglog(u_a, g_over_dotT[0] * (u_a / u_a[0]), "k:", lw=1.2, label=r"$\propto u$")
ax.set_xlabel(r"$u$"); ax.set_ylabel("rate")
ax.set_title(r"(e) 降温 $A<0$；$|A|/s^2\propto u^3$，$|g|\propto u$")
ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")

ax = axes[1, 2]
ax.semilogy(T_list, ratio_act, "o-", color="#9467bd", lw=2)
ax.set_xlabel(r"$T$ (K)"); ax.set_ylabel("激活率 / 仿射率")
ax.set_title("(f) 静态 no-go：缺陷激活支指数冻结")
ax.grid(alpha=0.3, which="both")

fig.suptitle("R-157：A 源静态判否、扫描奇偶性与统一可解域", fontsize=14)
fig.tight_layout(rect=[0, 0, 1, 0.96])
out_png = "10 探索/超导第一性研究/04_计算验证/环17_A源与扫描奇偶性.png"
fig.savefig(out_png, dpi=160)
plt.close(fig)

out_json = "10 探索/超导第一性研究/04_计算验证/环17_A源与扫描奇偶性.json"
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("R-157 分段核查全部通过")
for k, v in results.items():
    print(f"  {k}: {v}")
print(f"  图: {out_png}")
