# -*- coding: utf-8 -*-
"""
第 145 轮：环 15 sigma_c 口径的链内判定与两个方差的分离（无拟合，恒等式 + 解析函数）

A 段：相对口径 sigma_c^2=rho*V(T) 使 x= n_cell*rho 恒定、p 恒定（相变消灭）。
B 段：绝对口径反解 x*=barF_nu^{-1}(p_c^{1/t})，sigma_c^2=x* Z / n_cell，二分闭合。
C 段：w(T) 严格减（Debye tanh），s^2=Var(ell) 随 mu>0 严格增——方向相反。
D 段：p 对 V_coh 有弹性 eps=2*x*h(x)、p 对边长标准差 s_ell 恒零（对象错配）。
E 段：(R154.5) 二次解 s=2g/[C(g*a*lambda+2mu)] 与自洽代数一致，可解面四象限符号。
"""
import math
import csv
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import chi2, norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OMEGA_D = 1.0
Z = 1.0
NU = 9                      # = n_cell（chi-square 自由度）
P_C = 0.59274602
T_EXP = 1                   # 粗粒化指数 t
P_STAR = P_C ** (1.0 / T_EXP)

records = []
def record(key, value, note):
    records.append((key, value, note))
    print(f"[{key}] {value} — {note}")

# ------------------------------------------------------------------ 公共函数
def w_of(T):
    """环 10 Debye tanh 相干带宽，omega_D=1：w=2*int_0^1 omega*tanh(omega/2T)d omega。"""
    if T <= 1e-8:
        return 1.0
    val, _ = quad(lambda om: om * math.tanh(om / (2.0 * T)), 0.0, OMEGA_D,
                  epsabs=1e-13, epsrel=1e-13)
    return 2.0 * val / (OMEGA_D ** 2)

def hazard(x, nu=NU):
    """卡方危险率 h=f/sf，用对数稳定计算。"""
    return math.exp(chi2.logpdf(x, nu) - chi2.logsf(x, nu))

def mills(a):
    """逆 Mills 比 lambda(a)=phi(a)/sf(a)，对数稳定。"""
    return math.exp(norm.logpdf(a) - norm.logsf(a))

def barF(x, nu=NU):
    return chi2.sf(x, nu)

# ------------------------------------------------------------------ A 段
print("=== A 段：相对口径消灭相变 ===")
rho = 0.2
T_grid = np.linspace(0.02, 2.0, 60)
x_rel = np.array([NU * rho for _ in T_grid])
p_rel = np.array([barF(x, NU) for x in x_rel])
assert x_rel.std() < 1e-14, x_rel.std()
assert p_rel.std() < 1e-14, p_rel.std()
record("A_相对口径x恒定", f"{x_rel[0]:.6f}±{x_rel.std():.2e}", "x=n_cell*rho 与 T 无关")
record("A_相对口径p恒定", f"{p_rel[0]:.6f}±{p_rel.std():.2e}", "dp/dT=0 ⇒ 无唯一 T_* 交点")
# 也核对绝对口径下 p 确实随 T 变（对照）
p_abs = np.array([barF(NU * rho / w_of(float(T)), NU) for T in T_grid])
assert p_abs.max() - p_abs.min() > 0.05, (p_abs.max(), p_abs.min())

# ------------------------------------------------------------------ B 段
print("=== B 段：绝对口径反解 sigma_c ===")
x_star = brentq(lambda x: barF(x, NU) - P_STAR, 1e-6, 200.0, xtol=1e-13)
sigma2_over_Z = x_star / NU
assert abs(barF(x_star, NU) - P_STAR) < 1e-12, abs(barF(x_star, NU) - P_STAR)
# 把反解值代回：p(T_*)=p* 给 w(T_*)=x*/x(T_*)... 用交点 w*=NU*sigma_c^2/x*=... 恒等
w_star = NU * sigma2_over_Z / x_star
assert abs(w_star - 1.0) < 1e-12, w_star
record("B_反解x星", f"{x_star:.9f}", f"barF_{NU}(x*)=p*={P_STAR:.6f}")
record("B_sigma平方比Z", f"{sigma2_over_Z:.9f}", "sigma_c^2/Z=x*/n_cell；Z 外生")
# 不同 n_cell 下 sigma_c^2/Z（展示 n_cell 仍是外生自由度）
sig_grid = []
for n in [4, 8, 9, 16, 25]:
    xs = brentq(lambda x: chi2.sf(x, n) - P_STAR, 1e-6, 300.0, xtol=1e-13)
    sig_grid.append((n, xs / n))
assert all(sig_grid[i][1] < sig_grid[i + 1][1] for i in range(len(sig_grid) - 1)), sig_grid
record("B_不同n单调", f"{sig_grid[0][1]:.4f}→{sig_grid[-1][1]:.4f}", "n_cell 增时 x*/n→1（chi2 中位数≈n-2/3）")

# ------------------------------------------------------------------ C 段
print("=== C 段：两个方差的升温方向相反 ===")
w_grid = np.array([w_of(float(T)) for T in T_grid])
assert np.all(np.diff(w_grid) < 0), "w(T) 必须严格减"
# s^2 仿射支：dot s^2 / s^2 = 2 mu，mu>0 ⇒ s^2=s0^2 exp(2 mu (T-T0))
mu = 0.01     # 示意膨胀率（每单位 Tdot），用于图(a)展示方向；E 段另扫材料率比
s2_grid = np.exp(2.0 * mu * (T_grid - T_grid[0])) * 1.0
assert np.all(np.diff(s2_grid) > 0), "s^2 必须严格增"
record("C_w严格减", f"{w_grid[0]:.5f}→{w_grid[-1]:.5f}", "Debye tanh：升温破坏相干")
record("C_s2严格增", f"{s2_grid[0]:.5f}→{s2_grid[-1]:.5f}", "Gruneisen：升温膨胀")
record("C_方向相反", "dw/dT<0, ds2/dT>0", "V_coh 与 Var(ell) 不是同一对象")

# ------------------------------------------------------------------ D 段
print("=== D 段：弹性挂对对象 ===")
V0 = Z * w_of(0.5)
x0 = NU * sigma2_over_Z / V0
p0 = barF(x0, NU)
# p 对 V_coh 的弹性（对 sqrt(V_coh)）：eps = 2*x*h(x)
eps_formula = 2.0 * x0 * hazard(x0, NU)
h = 1e-6
p_plus = barF(NU * sigma2_over_Z / (V0 + h), NU)
p_minus = barF(NU * sigma2_over_Z / (V0 - h), NU)
# 对 sqrt(V) 的弹性：d ln p / d ln sqrt(V) = 2 * d ln p / d ln V
dlnp_dlnV = (math.log(p_plus) - math.log(p_minus)) / (math.log(V0 + h) - math.log(V0 - h))
eps_numeric = 2.0 * dlnp_dlnV
assert abs(eps_numeric - eps_formula) / eps_formula < 1e-5, (eps_numeric, eps_formula)
assert eps_formula > 0, eps_formula
# p 对边长标准差 s_ell 恒零：p 的公式只含 V_coh，不含 s_ell
def p_of(Vcoh, s_ell):
    return barF(NU * sigma2_over_Z / Vcoh, NU)
s_ell = 0.3
dp_ds = (p_of(V0, s_ell + h) - p_of(V0, s_ell - h)) / (2 * h)
assert abs(dp_ds) < 1e-15, dp_ds
record("D_对Vcoh弹性", f"{eps_formula:.6f}", "eps=2*x*h(x)，数值链式残差<1e-5")
record("D_对边长s恒零", f"{dp_ds:.3e}", "R152 的 p_s=eps*p/s 挂错对象，链内恒零")

# ------------------------------------------------------------------ E 段
print("=== E 段：可解面从自洽反馈降为外生率竞争 ===")
a_grid = np.linspace(1e-4, 6.0, 400)
alam = np.array([a * mills(float(a)) for a in a_grid])
# 低温交点处的 eps 与 |d ln w/dT|
eps_star = 2.0 * x_star * hazard(x_star, NU)
T_s = 0.5
# d ln w/dT 数值
dw = (math.log(w_of(T_s + 1e-5)) - math.log(w_of(T_s - 1e-5))) / 2e-5
g_over_Tdot = eps_star * dw         # g/Ṫ = eps * d ln w/dT，升温为负
mu_over_Tdot = mu                   # mu/Ṫ（mu=0.01 已是每单位 Tdot 的率）
assert g_over_Tdot < 0, g_over_Tdot
# 失效面：|g|*a*lambda = 2mu ⇒ a*lambda = r ≡ 2mu/|g|（材料率比，非普适常数）
# 扫描若干材料率比 r，反解对应 a*，展示阈值随 r 移动
r_grid = [0.05, 0.15, 0.4, 1.0, 2.0]
a_star_of_r = []
for r in r_grid:
    ast = brentq(lambda a: a * mills(float(a)) - r, 1e-6, 12.0, xtol=1e-12)
    a_star_of_r.append(ast)
assert all(a_star_of_r[i] < a_star_of_r[i + 1] for i in range(len(a_star_of_r) - 1))
# 当前示意 mu 对应的率比与 a*
r_now = 2.0 * mu / abs(g_over_Tdot)
a_crit = brentq(lambda a: a * mills(float(a)) - r_now, 1e-6, 12.0, xtol=1e-12)
# 核对二次解：取 a=0.5（升温配支、可解侧），直接联立与解析解一致
a_test = 0.5
C_coef = 0.1
g = g_over_Tdot * 1.0              # 取 Ṫ=1
mu_rate = mu
s_sol = 2.0 * g / (C_coef * (g * a_test * mills(a_test) + 2 * mu_rate))
resid_self = g * (2 * s_sol - C_coef * (a_test * mills(a_test)) * s_sol ** 2) - C_coef * 2 * mu_rate * s_sol ** 2
assert abs(resid_self) < 1e-10, resid_self
# R152 旧判据 a_*=0.3686 对照：旧判据是普适常数，新判据随 r 移动
a_old = 0.3686
assert abs(r_now - a_old * mills(a_old)) > 1e-3, (r_now, a_old * mills(a_old))
record("E_率比r", f"{r_now:.6f}", "r=2mu/|g| 由材料外生率定，非普适")
record("E_临界a随r", " ".join(f"{r:.2f}→{a:.3f}" for r, a in zip(r_grid, a_star_of_r)),
       "a* 随材料率比移动；R152 旧值 0.3686（普适）撤销")
record("E_二次解残差", f"{abs(resid_self):.3e}", "自洽代数与解析解一致")
record("E_四象限", "升温×右尾:竞争; 升温×左尾:同号; 降温×右尾:同号; 降温×左尾:竞争", "尾部符号依赖 sgn(Tdot)*sgn(a)")

# ------------------------------------------------------------------ 图
fig, axs = plt.subplots(2, 2, figsize=(12, 9))

ax = axs[0, 0]
ax.plot(T_grid, w_grid, color="#1f77b4", label=r"$w(T)/w(0)$：相干矩（减）")
ax.plot(T_grid, s2_grid, color="#d62728", label=r"$s^2(T)/s^2_0$：边长方差（增）")
ax.set_xlabel(r"温度 $T/\omega_D$"); ax.set_ylabel("归一化")
ax.set_title("(a) 两个方差随升温方向相反")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[0, 1]
xs = np.linspace(0.5, 30, 300)
ax.plot(xs, chi2.sf(xs, NU), color="#1f77b4", label=rf"$\bar F_{{ {NU} }}(x)$")
ax.axhline(P_STAR, color="#d62728", ls="--", lw=1.2, label=rf"$p_\ast=p_c^{{1/t}}$={P_STAR:.4f}")
ax.axvline(x_star, color="#2ca02c", ls=":", lw=1.5, label=rf"$x_\ast$={x_star:.3f}")
ax.set_xlabel(r"$x=n_{\rm cell}\sigma_c^2/V_{\rm coh}$"); ax.set_ylabel(r"$p_{\rm pair}$")
ax.set_title(r"(b) 绝对口径反解 $\sigma_c^2/Z=x_\ast/n_{\rm cell}$")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[1, 0]
Vs = np.linspace(0.2, 1.2, 200)
eps_curve = np.array([2.0 * (NU * sigma2_over_Z / V) * hazard(NU * sigma2_over_Z / V, NU) for V in Vs])
ax.plot(Vs, eps_curve, color="#1f77b4", label=r"对 $V_{\rm coh}$：$\epsilon=2xh(x)$")
ax.axhline(0.0, color="#d62728", lw=2, label=r"对边长 $s_\ell$：$\partial p/\partial s_\ell=0$")
ax.set_xlabel(r"$V_{\rm coh}$"); ax.set_ylabel("弹性")
ax.set_title("(c) 弹性挂对对象：R152 挂错为恒零")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[1, 1]
ax.plot(a_grid, alam, color="#1f77b4", lw=2, label=r"$a\lambda(a)$（解析）")
colors = plt.cm.autumn(np.linspace(0.05, 0.95, len(r_grid)))
for r, ast, c in zip(r_grid, a_star_of_r, colors):
    ax.axhline(r, color=c, ls="--", lw=1, alpha=.85)
    ax.plot(ast, r, "o", color=c, ms=5)
ax.annotate(r"交点 $a_\ast$ 随材料率比 $r$ 移动", xy=(a_star_of_r[2], r_grid[2]),
            xytext=(2.2, 0.9), fontsize=8, arrowprops=dict(arrowstyle="->", color="#555555"))
ax.annotate(r"R152 旧 $a_\ast=0.369$ 是普适常数，已撤销", xy=(0.3686, 0.3686 * mills(0.3686)),
            xytext=(1.6, 2.4), fontsize=8, arrowprops=dict(arrowstyle="->", color="#7f7f7f"))
ax.set_xlabel(r"尾部选择 $a$（右尾 $a>0$）"); ax.set_ylabel(r"$a\lambda(a)$")
ax.set_xlim(0, 6); ax.set_ylim(0, 3)
ax.set_title("(d) 失效面=外生率竞争（阈值非普适）")
ax.legend(fontsize=8, loc="upper left"); ax.grid(alpha=.3)

fig.tight_layout()
fig.savefig("环15_sigma_c口径与两个方差.png", dpi=150)
plt.close(fig)

with open("环15_sigma_c口径与两个方差_摘要.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["核查项", "数值", "说明"])
    for r in records:
        w.writerow(r)

print("DONE: 图与摘要已写出")
