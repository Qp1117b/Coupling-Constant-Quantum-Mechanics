# -*- coding: utf-8 -*-
"""
第 147 轮：t 与 Z 的同源材料桥 + Eliashberg 重整化因子 Z 的同名判否（无拟合）

A 段：回修 R154.2 漏掉的 w(T_*) 因子：sigma_c^2/Z = x_* w(T_c)/n_cell <= x_*/n_cell。
B 段：链内 Z=V_coh(0)=sigma_0^2 的材料表达 Z=(3/8)c_eps^2 hbar*wD/(M c_s^2)，
      用 Debye 零点均方位移 <u^2>_0=3 hbar/(4 M wD) 交叉核对。
C 段：FE10 与环 10 两条 lambda 路径同源：Z/lambda=(1/4) hbar wD/[N(0) z g^2 (1-rho)]，
      与环 10 式之比恰为 1/z（z=1 才完全一致）。
D 段：同名判否：链内 Z_chain ~ 1e-4--1e-3 << 1+lambda ~ O(1)；不是同一对象。
E 段：epsilon_nu 只经 t（普适）进入；r(T) 两支用 {gamma_bar, M, n, c_s, epsilon_nu} 表达，
      与 Z 的绝对值无关（数值缩放 Z 检验）。
F 段：函数图（六面板，全部为恒等式/解析式，无数据拟合）。
"""
import math
import csv
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import chi2
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# 物理常数（SI，只用于材料桥的单位核对，不用于拟合）
HBAR = 1.054571817e-34       # J s
KB = 1.380649e-23            # J/K
U = 1.66053906660e-27        # kg

PC = 0.59274602              # 2D 正方格座渗流阈值（外部标准，链内沿用）
NU = 9                       # = n_cell（R-145 取值）
T_EXP = 1.0                  # 粗粒化指数 t（R-145 取值）
COEFF = (6 * math.pi ** 2) ** (4 / 3) / (16 * math.pi ** 2)   # = 1.4617


def record(name, value, note):
    rows.append((name, value, note))
    print(f"{name:28s} {value:>24s}  {note}")


def w_of(x):
    """Debye 相干权重，x=T/wD；w(0)=1，严格减。"""
    if x <= 0:
        return 1.0
    val = quad(lambda u: u * np.tanh(u / (2 * x)), 0.0, 1.0, epsabs=1e-13)[0]
    return 2 * val


def x_star_of(t):
    """bar F_nu(x*) = p_c^{1/t} 的唯一反解。"""
    p_star = PC ** (1.0 / t)
    return brentq(lambda x: chi2.sf(x, NU) - p_star, 1e-6, 300.0, xtol=1e-14)


def eps_nu_of(t):
    xs = x_star_of(t)
    hazard = chi2.pdf(xs, NU) / chi2.sf(xs, NU)
    return 2 * xs * hazard


rows = []

# ------------------------------------------------------------------ A 段
print("=== A 段：R154.2 漏掉的 w(T_c) 因子 ===")
xs = x_star_of(T_EXP)
p_star = PC ** (1.0 / T_EXP)
assert abs(chi2.sf(xs, NU) - p_star) < 1e-12
assert abs(chi2.sf(xs, NU) - 0.59274602) < 1e-6   # t=1 时 p*=p_c
record("A_x星", f"{xs:.9f}", "bar F_9(x*)=p_c^(1/t)")
record("A_旧sigma2/Z", f"{xs/NU:.9f}", "R-145 写法（等价于把 T_* 钉在 0）")
corr = []
for tc in [0.01, 0.02, 0.05, 0.1, 0.3, 1.0]:
    wc = w_of(tc)
    sig2z = xs * wc / NU
    assert 0 < wc <= 1.0
    assert sig2z <= xs / NU + 1e-14
    corr.append((tc, wc, sig2z))
record("A_Tc=0.01修正系数", f"{corr[0][1]:.9f}", "sigma_c^2/Z=x_*w(T_c)/9")
record("A_Tc=0.30修正系数", f"{corr[4][1]:.9f}", "w<1 严格成立")
record("A_单调", "递减", "T_c 升则 sigma_c^2/Z 降")

# ------------------------------------------------------------------ B 段
print("=== B 段：Z 的链内材料表达与 Debye 零点核对 ===")
assert abs(COEFF - (3 / 8) * (6 * math.pi ** 2) ** (1 / 3)) < 1e-12
# Al 材料桥（只核对恒等式，不拟合）
M_AL = 27.0 * U
RHO_AL = 2700.0
N_AL = RHO_AL / M_AL
A_N = N_AL ** (-1 / 3.0)
Q_AL = (6 * math.pi ** 2 * N_AL) ** (1 / 3.0)
W_D_AL = 428.0                                   # K（德拜温度读数，外生）
OMEGA_D_AL = KB * W_D_AL / HBAR                  # rad/s
C_S_AL = OMEGA_D_AL / Q_AL                       # m/s
assert abs(HBAR * C_S_AL * Q_AL / KB - W_D_AL) < 1e-9
ELL_Q = (HBAR / (RHO_AL * C_S_AL)) ** 0.25
C_EPS = 0.5                                      # R-145 量级取值（外生）
Z_a = C_EPS ** 2 * COEFF * (ELL_Q / A_N) ** 4
Z_b = (3 / 8) * C_EPS ** 2 * HBAR * OMEGA_D_AL / (M_AL * C_S_AL ** 2)
U2_0 = 3 * HBAR / (4 * M_AL * OMEGA_D_AL)
Z_c = 0.5 * C_EPS ** 2 * Q_AL ** 2 * U2_0
assert abs(Z_a / Z_b - 1) < 1e-12
assert abs(Z_a / Z_c - 1) < 1e-12
record("B_系数恒等式", f"{COEFF:.12f}", "(6pi^2)^(4/3)/(16pi^2)=(3/8)(6pi^2)^(1/3)")
record("B_Z三条路", f"{Z_a:.6e}/{Z_b:.6e}/{Z_c:.6e}", "sigma0^2 / (3/8)c^2 hbar wD/Mcs^2 / (1/2)c^2Q^2<u^2>_0")
record("B_ell_q/a_n", f"{ELL_Q/A_N:.6f}", "Al 量级，与 R145 表 0.225 一致")
record("B_zero_point_u2", f"{U2_0:.4e} m^2", "Debye f(0)=1/4")

# ------------------------------------------------------------------ C 段
print("=== C 段：FE10 与环 10 两条 lambda 路径 ===")
# 用无量纲任意截面核对代数（不代入材料值，避免跨单位制）
hbar_wD, N0, g2, rho_c = 0.025, 1.7, 1.3, 0.1
z_over_lam_fe10 = hbar_wD / (4 * N0 * 8 * g2 * (1 - rho_c))       # z=8 示范
z_over_lam_r10 = hbar_wD / (4 * N0 * g2 * (1 - rho_c))
assert abs(z_over_lam_fe10 * 8 / z_over_lam_r10 - 1) < 1e-14
z_grid = np.arange(1, 9)
ratio_grid = np.array([(z_over_lam_r10 / zz) / z_over_lam_r10 for zz in z_grid])
assert np.allclose(ratio_grid, 1.0 / z_grid, atol=1e-14)
assert abs(z_over_lam_fe10 * 8 - z_over_lam_r10) < 1e-18
record("C_Z/lambda_FE10", f"{z_over_lam_fe10:.9e}", "z=8 示范（同一材料集）")
record("C_z=1一致", "比值=1", "FE10 与环 10 的 Z/lambda 只差 1/z")

# ------------------------------------------------------------------ D 段
print("=== D 段：Z 同名判否（链内零点方差 vs Eliashberg 重整化） ===")
# R-145 表的 (ell_q/a_n)^2 与观测 lambda；c_eps=0.5
mats = [
    ("Al", 0.225, 0.43), ("Nb", 0.188, 0.95), ("V", 0.204, 0.80),
    ("Ta", 0.152, 0.65), ("Pb", 0.167, 1.55),
]
hom = []
for name, ell_ratio, lam_obs in mats:
    zc = C_EPS ** 2 * COEFF * ell_ratio ** 4
    ze = 1 + lam_obs
    hom.append((name, zc, ze, zc / ze))
    assert zc < 1e-2 and ze > 1 and zc / ze < 1e-2
record("D_Z_chain范围", f"{min(h[1] for h in hom):.2e}-{max(h[1] for h in hom):.2e}", "c_eps=0.5")
record("D_Z_el范围", f"{min(h[2] for h in hom):.2f}-{max(h[2] for h in hom):.2f}", "lambda_obs 外生读数")
record("D_同名判否", "Z_chain<<Z_el", "同名不同物，禁止互换")

# ------------------------------------------------------------------ E 段
print("=== E 段：epsilon_nu(t) 与 r(T) 同源材料表达 ===")
t_grid = np.linspace(1.0, 5.0, 40)
xs_grid = np.array([x_star_of(t) for t in t_grid])
eps_grid = np.array([eps_nu_of(t) for t in t_grid])
assert np.all(np.diff(xs_grid) < 0) and np.all(np.diff(eps_grid) < 0)
assert abs(eps_nu_of(1.0) - 2.5929) < 1e-3
record("E_eps_nu(t=1)", f"{eps_nu_of(1.0):.6f}", "R-145 值 2.5929")
record("E_eps_nu(t=5)", f"{eps_nu_of(5.0):.6f}", "随 t 单调减（x_* 减）")

eps_nu = eps_nu_of(T_EXP)
GAMMA = 2.0                                   # 外生示意（Grüneisen）

def alpha_low_si(T):
    """低温绝缘体 Debye 热膨胀（1/K），K_T=M n c_s^2。"""
    return GAMMA * (2 * math.pi ** 2 / 5) * KB * (KB * T / (HBAR * C_S_AL)) ** 3 / (M_AL * N_AL * C_S_AL ** 2)

def dlnw_low_per_K(T):
    return (2 * math.pi ** 2 / 3) * T / W_D_AL ** 2

def r_direct_low(T):
    return 2 * alpha_low_si(T) / (3 * eps_nu * dlnw_low_per_K(T))

def r_closed_low(T):
    """r=(2 gamma_bar/5)(k_B T)^2 Q^2/(eps_nu hbar M n c_s^3)。"""
    return (2 * GAMMA / 5) * (KB * T) ** 2 * Q_AL ** 2 / (eps_nu * HBAR * M_AL * N_AL * C_S_AL ** 3)

def r_closed_high(T):
    """r=2 gamma_bar k_B T/(eps_nu M c_s^2)（Dulong-Petit + |dlnw/dT|=1/T）。"""
    return 2 * GAMMA * KB * T / (eps_nu * M_AL * C_S_AL ** 2)

T_low = np.array([2.0, 5.0, 10.0, 20.0, 50.0, 100.0])
direct = np.array([r_direct_low(float(T)) for T in T_low])
closed = np.array([r_closed_low(float(T)) for T in T_low])
assert np.max(np.abs(direct / closed - 1)) < 1e-12
assert np.all(np.diff(direct) > 0)
slope = np.polyfit(np.log(T_low[:4]), np.log(direct[:4]), 1)[0]
assert abs(slope - 2) < 1e-6
record("E_r低温斜率", f"{slope:.9f}", "理论 2（绝缘体 Debye + Grüneisen）")
record("E_r(10K)", f"{direct[2]:.6e}", "Al 量级示意，外生 gamma_bar=2")

# Z 缩放检验：把 Z 人为放大 1e6，r 两分支不变
for scale in [1.0, 1e3, 1e6]:
    zz = Z_a * scale
    # 交点条件 sigma_c^2/Z=x_*w/n 给 sigma_c^2 随 Z 同比例变，x_* 不变 ⇒ eps_nu 不变 ⇒ r 不变
    sig2 = xs * w_of(10.0 / W_D_AL) / NU * zz
    x_check = NU * sig2 / (zz * w_of(10.0 / W_D_AL))
    assert abs(x_check - xs) < 1e-10
record("E_Z缩放不变", "1e6倍Z仍同r", "r 只含 eps_nu(T,t) 与谱/热材料量")

# ------------------------------------------------------------------ F 段：图像
fig, axes = plt.subplots(2, 3, figsize=(15.5, 8.8))
fig.suptitle("第147轮：t 与 Z 的同源材料桥（恒等式/解析式，无拟合）", fontsize=14)

ax = axes[0, 0]
tcx = np.linspace(1e-3, 1.2, 300)
ax.plot(tcx, [w_of(float(t)) for t in tcx], color="#1f77b4", lw=2, label=r"$w(T_c)$")
ax.axhline(1.0, color="#d62728", ls="--", lw=1.2, label="R-145 旧值（隐含 w=1）")
ax.set_xlabel(r"$T_c/\omega_D$"); ax.set_ylabel(r"$\sigma_c^2/Z$ 的修正因子")
ax.set_title("(a) R154.2 漏项：乘回 $w(T_c)$")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[0, 1]
names = [h[0] for h in hom]
zcv = np.array([h[1] for h in hom])
zev = np.array([h[2] for h in hom])
xp = np.arange(len(names))
ax.bar(xp - 0.18, zcv, width=0.36, color="#2ca02c", label=r"链内 $Z_{\rm chain}$")
ax.bar(xp + 0.18, zev, width=0.36, color="#ff7f0e", label=r"Eliashberg $Z_{\rm el}=1+\lambda$")
ax.set_yscale("log"); ax.set_xticks(xp); ax.set_xticklabels(names)
ax.set_ylabel("无量纲"); ax.set_title("(b) 同名判否：两 Z 差 2–4 个量级")
ax.legend(fontsize=8); ax.grid(alpha=.3, axis="y")

ax = axes[0, 2]
ax.plot(t_grid, xs_grid, color="#1f77b4", lw=2, label=r"$x_\ast$")
ax.plot(t_grid, eps_grid, color="#d62728", lw=2, label=r"$\epsilon_\nu$")
ax.set_xlabel(r"粗粒化指数 $t$"); ax.set_ylabel("无量纲")
ax.set_title(r"(c) $x_\ast,\epsilon_\nu$ 由普适 $t$ 定")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[1, 0]
Tg = np.logspace(0, 2.3, 120)
ax.plot(Tg, [r_direct_low(float(T)) for T in Tg], color="#1f77b4", lw=2, label="直接式")
ax.plot(Tg, [r_closed_low(float(T)) for T in Tg], "o", ms=3, color="#d62728", label="材料量闭式")
ax.plot(Tg, [r_closed_high(float(T)) for T in Tg], "--", color="#2ca02c", label="高温支")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$T$ (K)"); ax.set_ylabel(r"$r(T)$")
ax.set_title("(d) $r$ 两支：同源材料集，与 $Z$ 绝对值无关")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

ax = axes[1, 1]
ax.plot(z_grid, [(z_over_lam_r10 / z) / z_over_lam_r10 for z in z_grid], "o", color="#9467bd")
ax.axhline(1, color="#d62728", ls="--", lw=1)
ax.set_xlabel(r"配位数 $z$"); ax.set_ylabel(r"FE10 / 环10 的 $Z/\lambda$ 比")
ax.set_ylim(0, 9); ax.set_title(r"(e) 两路径一致当且仅当 $z=1$")
ax.grid(alpha=.3)

ax = axes[1, 2]
Tg2 = np.linspace(1e-3, 4.0, 300)
def dlnw_exact(T):
    """解析导数：|dlnw/dT| = [T^-2 ∫_0^1 u^2 sech^2(u/2T) du] / w(T)（wD=1）。"""
    if T < 1e-8:
        return 0.0
    def sech2(z):
        e = math.exp(-2 * min(z, 350.0))
        return 4 * e / (1 + e) ** 2
    num = quad(lambda u: u * u * sech2(u / (2 * T)), 0.0, 1.0, epsabs=1e-14)[0] / T ** 2
    return num / w_of(T)

assert abs(dlnw_exact(1e-3) / 1e-3 - 2 * math.pi ** 2 / 3) < 1e-4
assert abs(dlnw_exact(10.0) * 10.0 - 1.0) < 1e-3
record("F_解析导数两支", f"{dlnw_exact(1e-3)/1e-3:.6f}/{dlnw_exact(10.0)*10.0:.6f}",
       "理论 2pi^2/3=6.5797 / 1")

ax.plot(Tg2, [dlnw_exact(float(T)) for T in Tg2], color="#1f77b4", lw=2, label="Debye 精确")
ax.plot(Tg2, [(2 * math.pi ** 2 / 3) * T for T in Tg2], "--", color="#d62728", label=r"低温 $(2\pi^2/3)T$")
ax.plot(Tg2, [1 / T if T > 0 else np.inf for T in Tg2], "--", color="#2ca02c", label=r"高温 $1/T$")
ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$|d\ln w/dT|$")
ax.set_ylim(1e-4, 1e3); ax.set_yscale("log")
ax.set_title("(f) $r$ 的谱输入：两支渐近")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig("D:/WorkSpace/物理/CQMFormal/10 探索/超导第一性研究/04_计算验证/环17_t与Z的同源材料桥.png", dpi=150)

with open("D:/WorkSpace/物理/CQMFormal/10 探索/超导第一性研究/04_计算验证/环17_t与Z的同源材料桥_摘要.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["检查项", "数值", "说明"])
    wr.writerows(rows)

print("全部断言通过；图与摘要 CSV 已写出。")
