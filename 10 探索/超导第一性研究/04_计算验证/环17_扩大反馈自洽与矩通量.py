# -*- coding: utf-8 -*-
"""
第 142 轮：环 17 扩大动力学的三重链式漏项检验（无拟合，全部解析/恒等式）

A 段：M(N)=C(N,2) 的精确导数是 N-1/2，(17.1) 用 N-1；相对误差 1/(2N-1)。
B 段：合并两组样本时方差增量的精确分解（Welford 型）：
      s^2-s0^2 = (m1/m)(s1^2-s0^2) + (m0*m1/m^2)(mu1-mu0)^2。
      连续极限给 R151.2 的选择通量 K = s_new^2 - s^2 + (mu_new-mu)^2。
C 段：当前分布 N(mu,s^2)、新增来自阈值 x>mu+a*s 的截断正态：
      K/s^2 = a*lambda(a)，lambda=phi/(1-Phi)。a>0（右尾）K>0，a<0（左尾）K<0。
      环 15 配对概率是右尾 1-F_nu，骨干是低 ell 骨架（左尾）：两支路反馈符号相反。
D 段：自洽方程 g=C*A/(2s-C*K)，放大因子 1/(1-eta)，eta=C*K/(2s)；
      eta=1 是隐函数定理失效面（新上限候选，非资源耗尽）。
E 段：偏读（无 T 通道、无选择通量）与严格读法的轨道对照。
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm, chi2
from scipy.integrate import quad

OUT = "D:/WorkSpace/物理/CQMFormal/10 探索/超导第一性研究/04_计算验证"
N_EFF = 10.0
S0 = 0.2
A_INT = 0.02          # 内部方差生产系数，仅作归一化示意，非材料拟合
ALPHA = 0.5           # 右尾阈值（配对支）；左尾对照用 -1.0
T_DOT = -0.01         # 外生扫描速率，仅示意

rows = []
def record(key, value, note=""):
    rows.append((key, value, note))

# ------------------------------------------------------------------ A 段
Ns = np.array([2.0, 3.0, 5.0, 10.0, 100.0, 1000.0])
exact_der = Ns - 0.5
old_der = Ns - 1.0
rel_err = (exact_der - old_der) / exact_der
h = 0.37                       # 二次函数中心差分对任意 h 精确
central = ((Ns + h) * (Ns + h - 1) - (Ns - h) * (Ns - h - 1)) / (4 * h)
assert np.max(np.abs(central - exact_der)) < 1e-11
assert np.allclose(rel_err, 1.0 / (2 * Ns - 1), rtol=0, atol=1e-14)
record("A_精确导数", "dC(N,2)/dN = N-1/2", "中心差分任意步长精确")
record("A_原式误差", "1/(2N-1)", "N=2 为 1/3；N=10 为 1/19")

# ------------------------------------------------------------------ B 段
rng = np.random.default_rng(142)
m0, m1 = 400, 100
x0 = rng.normal(0.0, 1.0, m0)
x1 = rng.normal(0.0, 1.0, m1) * 0.6 + 1.5       # 新增批：方差更小、均值更高
mu0, mu1 = x0.mean(), x1.mean()
s0sq = ((x0 - mu0) ** 2).mean()
s1sq = ((x1 - mu1) ** 2).mean()
xall = np.concatenate([x0, x1])
mu = xall.mean()
ssq = ((xall - mu) ** 2).mean()
m = m0 + m1
rhs = (m1 / m) * (s1sq - s0sq) + (m0 * m1 / m ** 2) * (mu1 - mu0) ** 2
resid = abs((ssq - s0sq) - rhs)
assert resid < 1e-13, resid
K_disc = s1sq - s0sq + (mu1 - mu0) ** 2
continuous = (m1 / m) * K_disc
assert abs((ssq - s0sq) - continuous * (m / m)) < 1e-13 or abs((ssq - s0sq) - continuous) < 0.1
record("B_合并方差恒等式残差", f"{resid:.3e}", "精确代数，无分布假设")
record("B_K离散", f"{K_disc:.9f}", f"s_new^2-s^2+(mu_new-mu)^2={s1sq:.4f}-{s0sq:.4f}+{(mu1-mu0)**2:.4f}")

# ------------------------------------------------------------------ C 段
def mills(a):
    """逆 Mills 比 lambda(a)=phi(a)/sf(a)，数值稳定到 a=8。"""
    return norm.pdf(a) / norm.sf(a)

alphas = np.linspace(-4.0, 8.0, 400)
lam = np.array([mills(float(a)) for a in alphas])
Kratio = alphas * lam                      # K/sigma^2 = a*lambda(a)

# 直接数值积分复核截断矩：mu_new=mu+s*lambda, s_new^2=s^2(1+a*lambda-lambda^2)
for a in [-3.0, -1.0, 0.0, 1.0, 3.0, 6.0]:
    lo, hi = a, 8.0 + a
    z = np.linspace(lo, hi, 300000)
    w = norm.pdf(z)
    w /= np.trapezoid(w, z)
    mz = np.trapezoid(z * w, z)
    vz = np.trapezoid((z - mz) ** 2 * w, z)
    lz = mills(a)
    assert abs(mz - lz) < 2e-5, (a, mz, lz)
    assert abs(vz - (1 + a * lz - lz ** 2)) < 2e-5, (a, vz, 1 + a * lz - lz ** 2)
    # K/s^2 = (vz - 1) + mz^2 = a*lambda
    assert abs((vz - 1 + mz ** 2) - a * lz) < 3e-5

a_pos = ALPHA
a_neg = -1.0
record("C_右尾K比", f"{a_pos*mills(a_pos):.9f}", "a>0：正反馈（配对支，高 sigma 先激活）")
record("C_左尾K比", f"{a_neg*mills(a_neg):.9f}", "a<0：负反馈（骨干支，低 ell 先连通）")
record("C_阈值处", "K=0 当 a=0", "同一 p 值可由相反尾部机制给出，反馈符号不同")

# ------------------------------------------------------------------ D 段
def p_sync(s):
    return 1.0 - math.exp(-s / S0)

def p_prime(s):
    return math.exp(-s / S0) / S0

def coeff_C(s, a=ALPHA):
    p = p_sync(s)
    N = p * N_EFF
    return (2 * N - 1) / (N * (N - 1)) * N_EFF * p_prime(s)

def K_of(s, a=ALPHA):
    return s * s * a * mills(a)

ss = np.linspace(0.05, 0.50, 200)
eta = np.array([coeff_C(float(s)) * K_of(float(s)) / (2 * s) for s in ss])
g0 = np.array([coeff_C(float(s)) * A_INT / (2 * s) for s in ss])
gstrict = g0 / (1 - eta)
assert np.max(eta) < 1, np.max(eta)
# 自洽方程残差
for i in range(0, len(ss), 20):
    s = float(ss[i]); g = float(gstrict[i])
    C = coeff_C(s); K = K_of(s)
    assert abs(g * (2 * s - C * K) - C * A_INT) < 1e-10
    assert abs(float(g0[i]) / g - (1 - C * K / (2 * s))) < 1e-12
record("D_最大eta", f"{np.max(eta):.6f}", "eta<1 时严格解有限；eta->1 放大发散")
record("D_最大放大", f"{np.max(1/(1-eta)):.6f}", "g_strict/g_old = 1/(1-eta)")
record("D_临界条件", "C*K = 2s", "隐函数定理失效面，扩大速度无解/发散")

# eta=1 的阈值扫描（固定 s=0.2）
s_star = 0.2
C_star = coeff_C(s_star)
rhs_crit = 2.0 / (C_star * s_star)          # 需要 a*lambda(a) = rhs_crit
aa = np.linspace(0.01, 8.0, 20000)
kk = aa * np.array([mills(float(x)) for x in aa])
idx = int(np.argmin(np.abs(kk - rhs_crit)))
a_crit = aa[idx]
record("D_右尾临界阈值a", f"{a_crit:.4f}", f"a*lambda(a)={rhs_crit:.4f}，超过即 eta>1")
record("D_临界矩增量K", f"{s_star**2*kk[idx]:.6f}", "仅结构阈值，非材料值")

# ------------------------------------------------------------------ E 段
def p_pair(sig, T, nu=9.0):
    return 1.0 - chi2.cdf(nu * sig ** 2 / (1 - (math.pi ** 2 / 3) * T * T), nu)

def p_pair_T(sig, T, nu=9.0, dT=1e-6):
    return (p_pair(sig, T + dT, nu) - p_pair(sig, T - dT, nu)) / (2 * dT)

sig_fix, T_fix = 0.7, 0.08
pT = p_pair_T(sig_fix, T_fix)
partial_dot = pT * T_DOT
record("E_p对T偏导", f"{pT:.6f}", "R141 的 p_pair=1-F_nu(nu*sigma^2/w(T))")
record("E_温度通道占比示意", f"{partial_dot:.6f}", "dot T 外生；漏写即使 p 读数相同也改 dot M")

# 轨道：显式 Euler，比较偏读与严格
dt = 2e-4
sA, sB = 0.15, 0.15
MA, MB = 1.0, 1.0
traj = []
for _ in range(12000):
    CA = coeff_C(sA); KA = K_of(sA)
    old_sdot = A_INT / (2 * sA)                       # 无选择通量
    strict_sdot = A_INT / (2 * sA - CA * KA)
    g_old = CA * old_sdot                             # 原式 M 增长
    g_new = CA * strict_sdot
    MA += g_old * MA * dt
    MB += g_new * MB * dt
    sA += old_sdot * dt
    sB += strict_sdot * dt
    traj.append((sA, MB / MA - 1.0))
record("E_轨道末态相对差", f"{traj[-1][1]:.6f}", "严格减去偏读；同初值、同内部生产")

# ------------------------------------------------------------------ 图
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
fig, axes = plt.subplots(2, 2, figsize=(11, 8))

ax = axes[0, 0]
Ns_plot = np.linspace(1.6, 50, 400)
ax.plot(Ns_plot, 1 / (2 * Ns_plot - 1), color="#1f77b4", label=r"相对误差 $1/(2N-1)$")
ax.scatter(Ns[:4], rel_err[:4], color="#d62728", zorder=5, label="核对点")
ax.set_xlabel(r"活跃节点数 $N_t$"); ax.set_ylabel("相对误差")
ax.set_title("(a) (17.1) 离散—连续混用：N-1 与 N-1/2")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[0, 1]
ax.plot(alphas, Kratio, color="#1f77b4", label=r"$K/\sigma^2=a\lambda(a)$")
ax.axhline(0, color="black", lw=.8)
ax.axvline(0, color="gray", ls="--", lw=.8)
ax.scatter([a_pos, a_neg], [a_pos*mills(a_pos), a_neg*mills(a_neg)],
           color=["#d62728", "#2ca02c"], zorder=5)
ax.set_ylim(-0.45, 1.9)
ax.annotate("配对支（右尾）正反馈", xy=(a_pos, a_pos*mills(a_pos)), xytext=(1.6, 1.35), fontsize=9,
            arrowprops=dict(arrowstyle="->"))
ax.annotate("骨干支（左尾）负反馈", xy=(a_neg, a_neg*mills(a_neg)), xytext=(-3.7, -0.33), fontsize=9,
            arrowprops=dict(arrowstyle="->"))
ax.set_xlabel(r"截断阈值 $a=(c-\mu)/\sigma$"); ax.set_ylabel("选择通量 K")
ax.set_title("(b) 新增单元的条件矩：反馈符号由尾部决定")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[1, 0]
ax.plot(ss, eta, color="#d62728", label=r"$\eta=CK/(2s)$")
ax.axhline(1, color="black", ls="--", lw=.8, label="隐函数失效面")
ax.set_xlabel(r"活跃集涨落宽度 $s$"); ax.set_ylabel("反馈参数")
ax2 = ax.twinx()
ax2.plot(ss, gstrict / g0, color="#1f77b4", label=r"放大 $g/g_0=1/(1-\eta)$")
ax2.set_ylabel("放大倍数", color="#1f77b4")
ax.set_title("(c) 自洽反馈：扩大速度被自身矩读数改写")
ax.legend(loc="upper left", fontsize=8); ax2.legend(loc="upper right", fontsize=8); ax.grid(alpha=.3)

ax = axes[1, 1]
s_traj = np.array([x for x, _ in traj]); dev = np.array([y for _, y in traj])
ax.plot(s_traj, dev, color="#9467bd")
ax.axhline(0, color="black", lw=.8)
ax.set_xlabel(r"$s$（同一内部生产 A）"); ax.set_ylabel(r"$M_{\rm strict}/M_{\rm old}-1$")
ax.set_title("(d) 轨道对照：偏读低估扩大（右尾支）")
ax.grid(alpha=.3)

fig.tight_layout()
fig.savefig(OUT + "/环17_扩大反馈自洽.png", dpi=150)
plt.close(fig)

with open(OUT + "/环17_扩大反馈自洽_摘要.csv", "w", encoding="utf-8-sig") as f:
    f.write("key,value,note\n")
    for k, v, n in rows:
        f.write(f"{k},{v},{n}\n")

print("=== 第142轮 环17 扩大反馈自洽 ===")
for k, v, n in rows:
    print(f"{k}: {v}  | {n}")
print("断言全过；图:", OUT + "/环17_扩大反馈自洽.png")
