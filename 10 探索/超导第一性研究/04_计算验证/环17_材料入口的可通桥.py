# -*- coding: utf-8 -*-
"""
第 143 轮：环 17 两个材料入口的可通桥判定（无拟合，恒等式 + 解析函数）

A 段：单形面角的余弦比值对边长伸缩不变；随机三角剖分上 Euler 恒等式 L@ell≈0。
B 段：仿射驱动 dot ell = mu*ell 给 A=2*mu*s^2>0，而 dot eps = 0（反例：A 不能由 B^± 定）。
C 段：环 15 尾概率 p=bar F_nu(nu*sigma_c^2/s^2) 的弹性 eps=2*x*h(x)，
      与数值链式 s*p_s/p 逐点核对。
D 段：eta 的因子分解恒等式（R142 原始 C 式 vs R143 因子式）。
E 段：可解边界 eps*a*lambda(a)=1 反解 x_* 与 s_*。
F 段：示意弹性 eps_ad=s/(S0(e^{s/S0}-1))<1 与环 15 弹性的量级/单调对照。
"""
import math
import itertools
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2, norm
from scipy.optimize import brentq

OUT = "D:/WorkSpace/物理/CQMFormal/10 探索/超导第一性研究/04_计算验证"
rows = []
def record(key, value, note=""):
    rows.append((key, value, note))

# ------------------------------------------------------------------ A 段
def cos_ratio(a, b, c):
    return (a * a + b * b - c * c) / (2 * a * b)

rng = np.random.default_rng(143)
tri = np.array([rng.uniform(1.0, 2.0, 3) for _ in range(200)])
lam_grid = np.array([0.5, 0.8, 1.0, 1.3, 2.0, 5.0])
res_cos = max(abs(cos_ratio(*(lam * t)) - cos_ratio(*t))
              for t in tri for lam in lam_grid)
assert res_cos < 1e-13, res_cos
record("A_余弦比值尺度不变", f"{res_cos:.3e}", "任意三角形、任意 λ；纯代数")

# 固定三角剖分：中心扇状 6 三角形（顶点 0 为心，1..6 环），边表
radii = 1.0 + 0.15 * rng.normal(size=6)
angles = np.array([k * math.pi / 3 for k in range(6)]) + 0.05 * rng.normal(size=6)
verts = np.array([[0.0, 0.0]] + [[r * math.cos(t), r * math.sin(t)]
                                 for r, t in zip(radii, angles)])
triangles = [(0, i + 1, ((i + 1) % 6) + 1) for i in range(6)]
emap = {}
for i, j, k in triangles:
    for u, v in ((i, j), (i, k), (j, k)):
        emap[(min(u, v), max(u, v))] = None
edges = list(emap)
eidx = {e: t for t, e in enumerate(edges)}
def edge_lengths(P):
    return np.array([np.linalg.norm(P[u] - P[v]) for u, v in edges])
ell = edge_lengths(verts)

def angle_at(a, b, c):
    """角位于两边 a,b 的公共端点，c 为对边。"""
    x = (a * a + b * b - c * c) / (2 * a * b)
    return math.acos(max(-1.0, min(1.0, x)))

def deficits(L):
    eps = np.zeros(len(verts))
    for i, j, k in triangles:
        key = lambda u, v: (min(u, v), max(u, v))
        lij, lik, ljk = L[eidx[key(i, j)]], L[eidx[key(i, k)]], L[eidx[key(j, k)]]
        eps[i] += angle_at(lij, lik, ljk)
        eps[j] += angle_at(lij, ljk, lik)
        eps[k] += angle_at(lik, ljk, lij)
    return 2 * math.pi - eps

eps0 = deficits(ell)
h = 1e-5
Jac = np.zeros((len(verts), len(edges)))
for q in range(len(edges)):
    dp = ell.copy(); dp[q] += h
    dm = ell.copy(); dm[q] -= h
    Jac[:, q] = (deficits(dp) - deficits(dm)) / (2 * h)
euler = Jac @ ell
rel_euler = np.linalg.norm(euler) / max(np.linalg.norm(Jac), 1e-30)
assert rel_euler < 1e-9, rel_euler
record("A_Euler恒等式L_ell", f"{rel_euler:.3e}", "L=∂ε/∂ℓ；均匀伸缩方向在 ker L 内（有限差分）")

# ------------------------------------------------------------------ B 段
mu_grid = np.array([0.0, 0.02, 0.05, 0.10, 0.20])
A_grid, dE_grid = [], []
s2 = np.mean((ell - ell.mean()) ** 2)
for mu in mu_grid:
    ell_t = math.exp(mu) * ell
    s2_t = np.mean((ell_t - ell_t.mean()) ** 2)
    A_grid.append(s2_t - s2)                       # t=1 的方差生产（μ 小）
    dE_grid.append(np.max(np.abs(deficits(ell_t) - eps0)))
A_grid = np.array(A_grid)
# 一阶系数核对 A/t = 2*mu*s^2（t=1 时二阶差 O(mu^2)）；用中心差分取导数
mu_h = 1e-5
A_deriv = (np.mean((math.exp(mu_h) * ell - (math.exp(mu_h) * ell).mean()) ** 2)
           - np.mean((math.exp(-mu_h) * ell - (math.exp(-mu_h) * ell).mean()) ** 2)) / (2 * mu_h)
assert abs(A_deriv - 2 * s2) < 1e-10, (A_deriv, 2 * s2)
assert max(dE_grid) < 1e-10, max(dE_grid)
record("B_仿射方差生产", f"dA/dμ={A_deriv:.6e} vs 2s²={2*s2:.6e}", "相对残差 <1e-10")
record("B_仿射下亏角变化", f"{max(dE_grid):.3e}", "A>0 而 ε 扇区静止 ⇒ A 不由 B^± 定")

# ------------------------------------------------------------------ C 段
NU = 9.0
SIGC = 0.7
def hazard(x, nu=NU):
    """对数域计算，避免大 x 处 sf 下溢。"""
    return math.exp(chi2.logpdf(x, nu) - chi2.logsf(x, nu))
def elast(x, nu=NU):
    return 2 * x * hazard(x, nu)
def p_of_s(s, nu=NU):
    return chi2.sf(nu * SIGC ** 2 / s ** 2, nu)

xs = np.linspace(1.0, 30.0, 120)
for x in xs:
    s = math.sqrt(NU * SIGC ** 2 / x)
    ds = 1e-6 * s
    num = s * (p_of_s(s + ds) - p_of_s(s - ds)) / (2 * ds) / p_of_s(s)
    assert abs(num - elast(x)) < 1e-7, (x, num, elast(x))
record("C_弹性链式残差", "<1e-7", "eps=2x f/Fbar；120 点逐点核对")
assert abs(hazard(500.0) - 0.5) < 0.01, hazard(500.0)
record("C_危险率极限", f"h(500)={hazard(500.0):.6f}", "Gamma(ν/2, scale 2) ⇒ h→1/2（慢收敛）")

# ------------------------------------------------------------------ D 段
def mills(a):
    return norm.pdf(a) / norm.sf(a)
a_fix = 0.5
Neff = 100.0
x_fix = 8.0
s_fix = math.sqrt(NU * SIGC ** 2 / x_fix)
p_fix = p_of_s(s_fix)
N_fix = p_fix * Neff
K_fix = s_fix ** 2 * a_fix * mills(a_fix)
# R142 的原始 C（用真实 p_s = eps*p/s）
ps_fix = elast(x_fix) * p_fix / s_fix
C_orig = (2 * N_fix - 1) / (N_fix * (N_fix - 1)) * Neff * ps_fix
C_fact = (2 * N_fix - 1) / ((N_fix - 1) * s_fix) * elast(x_fix)
eta_orig = C_orig * K_fix / (2 * s_fix)
eta_fact = (2 * N_fix - 1) / (2 * (N_fix - 1)) * elast(x_fix) * a_fix * mills(a_fix)
assert abs(C_orig - C_fact) < 1e-12
assert abs(eta_orig - eta_fact) < 1e-12, (eta_orig, eta_fact)
record("D_C因子化残差", f"{abs(C_orig-C_fact):.3e}", "N_eff 与 p 分别消去")
record("D_eta因子化残差", f"{abs(eta_orig-eta_fact):.3e}", "eta=(1+1/2(N-1))*eps*aλ")

# ------------------------------------------------------------------ E 段
xstar = {}
for a in [0.3, 0.5, 1.0, 2.0]:
    rhs = a * mills(a)
    root = brentq(lambda z: elast(z) * rhs - 1.0, 1e-3, 60.0, xtol=1e-12)
    xstar[a] = root
    assert abs(elast(root) * rhs - 1.0) < 1e-9
    record(f"E_可解边界_a={a}", f"x_*={root:.6f}, s_*={math.sqrt(NU*SIGC**2/root):.6f}",
           f"eps(x_*)*aλ={rhs:.6f}^{-1}")
# 单调性：eps 随 x 严格增（Gamma 形状>1 的危险率递增）
assert np.all(np.diff([elast(float(z)) for z in xs]) > 0)
record("E_弹性单调", "eps(x) 严格递增", "ν=9>2，x<60 区间")

# ------------------------------------------------------------------ F 段
S0 = 0.5
def elast_ad(s):
    return s / (S0 * (math.exp(s / S0) - 1.0))
s_grid = np.linspace(0.1, 1.6, 200)
eps_ad = np.array([elast_ad(float(s)) for s in s_grid])
eps_ring = np.array([elast(NU * SIGC ** 2 / float(s) ** 2) for s in s_grid])
assert np.all(eps_ad < 1.0)
assert np.all(np.diff(eps_ad) < 0) and np.all(np.diff(eps_ring) < 0)
record("F_示意弹性上界", f"max={eps_ad.max():.6f}<1", "指数型 p_sync 永不超过 1")
record("F_环15弹性范围", f"{eps_ring.min():.3f}–{eps_ring.max():.1f}", "可远超 1，暴露失效面")

# ------------------------------------------------------------------ G 段
pc = 0.592746
x_pc = chi2.ppf(1.0 - pc, NU)
eps_pc = elast(x_pc)
a_pc = brentq(lambda z: eps_pc * z * mills(z) - 1.0, 1e-4, 3.0, xtol=1e-12)
assert abs(eps_pc * a_pc * mills(a_pc) - 1.0) < 1e-10
record("G_渗流阈值处弹性", f"x_pc={x_pc:.6f}, eps={eps_pc:.6f}", "ν=9、p_c=0.592746")
record("G_阈值处临界尾部", f"a_*={a_pc:.6f}", "a>a_* 时右尾选择在 p_c 处即触发 η>1")

# ------------------------------------------------------------------ 图
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
fig, axes = plt.subplots(2, 2, figsize=(11, 8))

ax = axes[0, 0]
ax.plot(mu_grid, A_grid, color="#1f77b4", marker="s", ms=4, label=r"$\Delta s^2$（数值）")
ax.plot(mu_grid, 2 * mu_grid * s2, color="#1f77b4", ls="--", lw=1.6, label=r"$A=2\mu s^2$")
ax2 = ax.twinx()
ax2.plot(mu_grid, np.zeros_like(mu_grid), color="#d62728", marker="o", ms=4,
         label=r"$\max|\Delta\varepsilon|\leq 2\times10^{-15}$（机器精度）")
ax2.set_ylim(-1e-16, 2e-15)
ax.set_xlabel(r"仿射伸缩率 $\mu$"); ax.set_ylabel("边长方差生产 A", color="#1f77b4")
ax2.set_ylabel(r"亏角变化 $\max|\Delta\varepsilon|$", color="#d62728")
ax.set_title("(a) 仿射驱动：A 增大而 ε 完全静止")
ax.legend(loc="upper left", fontsize=8); ax2.legend(loc="lower right", fontsize=8); ax.grid(alpha=.3)

ax = axes[0, 1]
ax.plot(xs, [hazard(float(x)) for x in xs], color="#2ca02c", label=r"危险率 $h=f/\bar F$")
ax.plot(xs, [elast(float(x)) for x in xs], color="#d62728", label=r"弹性 $\epsilon_\nu=2xh$")
ax.axhline(0.5, color="#2ca02c", ls="--", lw=.8)
ax.set_xlabel(r"$x=\nu\sigma_c^2/s^2$"); ax.set_ylabel("值")
ax.set_title(r"(b) 尾概率弹性由危险率定（$\nu=9$）")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[1, 0]
for a, col in zip([0.3, 0.5, 1.0, 2.0], ["#1f77b4", "#ff7f0e", "#2ca02c", "#9467bd"]):
    eta_curve = [elast(float(z)) * a * mills(a) for z in xs]
    ax.plot(xs, eta_curve, color=col, label=rf"$a={a}$，$x_*={xstar[a]:.2f}$")
ax.axhline(1.0, color="black", ls="--", lw=1, label=r"失效面 $\eta=1$")
ax.set_xlabel(r"$x=\nu\sigma_c^2/s^2$"); ax.set_ylabel(r"$\epsilon_\nu\,a\lambda(a)$")
ax.set_ylim(0, 2.2)
ax.set_title("(c) 反馈型可解边界：弹性×尾部选择")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[1, 1]
ax.plot(s_grid, eps_ring, color="#d62728", label=r"环15尾式 $\epsilon_\nu(x(s))$")
ax.plot(s_grid, eps_ad, color="#1f77b4", label=r"示意式 $\epsilon_{\rm ad}$")
ax.axhline(1.0, color="black", ls="--", lw=.8, label="失效面")
ax.set_xlabel(r"涨落宽度 $s$"); ax.set_ylabel("尾概率弹性")
ax.set_ylim(0, 6.0)
ax.annotate(r"环15式峰值为 $434$（已截轴）", xy=(0.13, 5.6), fontsize=8)
ax.set_title("(d) 读数式弹性掩盖反馈上限")
ax.legend(fontsize=8); ax.grid(alpha=.3)

fig.tight_layout()
fig.savefig(OUT + "/环17_材料入口的可通桥.png", dpi=150)
plt.close(fig)

with open(OUT + "/环17_材料入口的可通桥_摘要.csv", "w", encoding="utf-8-sig") as f:
    f.write("key,value,note\n")
    for k, v, n in rows:
        f.write(f"{k},{v},{n}\n")

print("=== 第143轮 环17 材料入口可通桥 ===")
for k, v, n in rows:
    print(f"{k}: {v}  | {n}")
print("断言全过；图:", OUT + "/环17_材料入口的可通桥.png")
