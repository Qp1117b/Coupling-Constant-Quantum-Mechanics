# -*- coding: utf-8 -*-
r"""
第 144 轮：两个 mu 的分离与热膨胀材料入口（无拟合，恒等式 + 解析函数）

A 段：任意顶点位移 dot x 下 dot eps = Atilde @ B @ dot x ≈ 0（强化 R147）。
B 段：径向位移 dot ell = mu*ell 给 A=2*mu*s^2>0 而 dot eps=0（R143 反例升级为真实过程）。
C 段：delta ell = dot ell - mu*ell 仍在 im(B)，Atilde@delta ell≈0（上一轮桥恒零）。
D 段：量纲分离 mu_(16)=d lambda/d n vs mu_(17)=dot ell/ell（量纲指数向量不可约）。
E 段：Gruneisen 膨胀率 mu=gamma*Cv*dotT/(3*K_T*V) 与有限差分 dot ell/ell 一致。
F 段：Debye 低温 Cv∝T^3 ⇒ mu∝T^3（log-log 斜率 → 3）。
G 段：绝对/相对阈值下 p(T) 的相反单调性（口径分叉）。
"""
import csv
import importlib.util
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.integrate import quad

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

rows = []
def record(key, value, note=""):
    rows.append((key, value, note))

# 复用环 04 的复形与矩阵构造（不重复实现，保证与 R145/R147 同口径）
_s = importlib.util.spec_from_file_location("h04", os.path.join(HERE, "环04_内禀扇区自由度归属.py"))
h04 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(h04)

P, tets, edges, faces = h04.bcc_complex(3)
B = h04.incidence(P, edges)
A_rel, lens = h04.deficit_jacobian(P, tets, edges, h=1e-6)
At = A_rel / lens[None, :]          # At[e,e'] = d eps_e / d ell_e'
E = len(edges)
V = len(P)
# 内部铰链：绕边四面体数 >=4（凸包边属读数层，与 R145/R147 同口径）
n_adj = np.array([len([t for t in tets if set(e) <= set(t)]) for e in edges])
mask = n_adj >= 4
AtI = At[mask]
record("复形", f"n=3 V={V} E={E} 内部={int(mask.sum())}", "BCC Delaunay");
print(f"[复形] V={V} E={E} 内部边={int(mask.sum())}")

# ------------------------------------------------------------------ A 段
rng = np.random.default_rng(20261125)
rel_errs = []
for _ in range(24):
    xdot = rng.normal(size=3 * V)
    # 去掉整体平移（B 的零空间），保留可实现的边长速度
    ell_dot = B @ xdot
    eps_dot = AtI @ ell_dot
    denom = np.linalg.norm(AtI, ord=2) * np.linalg.norm(ell_dot)
    rel_errs.append(np.linalg.norm(eps_dot) / denom if denom > 0 else 0.0)
rel_errs = np.array(rel_errs)
assert rel_errs.max() < 1e-9, rel_errs.max()
record("A_任意位移降 eps", f"max={rel_errs.max():.3e}", f"24 次随机 dot x；||At@B@x||/(||At|| ||Bx||)")
print(f"[A] 任意顶点位移下 dot eps 相对残差 max={rel_errs.max():.3e}")

# ------------------------------------------------------------------ B 段
xdot_rad = P.flatten().copy()      # dot x_i = x_i（以顶点位置为径向速度）
ell_dot_rad = B @ xdot_rad
mu_rad = float(np.dot(ell_dot_rad, lens) / np.dot(lens, lens))
res_rad = np.linalg.norm(ell_dot_rad - mu_rad * lens) / np.linalg.norm(lens)
assert abs(mu_rad - 1.0) < 1e-9, mu_rad
assert res_rad < 1e-9, res_rad
A_var = 2.0 * mu_rad * float(np.var(lens))
eps_dot_rad = AtI @ ell_dot_rad
rel_eps_rad = np.linalg.norm(eps_dot_rad) / (np.linalg.norm(AtI, ord=2) * np.linalg.norm(ell_dot_rad))
assert A_var > 0
assert rel_eps_rad < 1e-9, rel_eps_rad
record("B_径向 mu", f"{mu_rad:.12f}", "dot x_i=x_i ⇒ dot ell=ell（1% 精度内）")
record("B_A仿射", f"{A_var:.6e}", f"2*mu*s^2>0；s^2={np.var(lens):.6e}")
record("B_dot_eps", f"{rel_eps_rad:.3e}", "径向驱动下 eps 瞬时静止")
print(f"[B] 径向 mu={mu_rad:.12f}, A={A_var:.6e}>0, dot eps 残差={rel_eps_rad:.3e}")

# ------------------------------------------------------------------ C 段
# 用一般随机位移（径向位移给 delta ell≈0，纯噪声无法测投影）
xdot_c = rng.normal(size=3 * V)
ell_dot_c = B @ xdot_c
mu_c = float(np.dot(ell_dot_c, lens) / np.dot(lens, lens))
delta_ell = ell_dot_c - mu_c * lens        # ell = B@P ∈ im(B)，故 delta ell ∈ im(B)
# im(B) 的正交投影（用 SVD 伪逆）
Ub, sb, Vbt = np.linalg.svd(B, full_matrices=False)
rank_b = int((sb > sb.max() * 1e-10).sum())
Pb_delta = Ub[:, :rank_b] @ (Ub[:, :rank_b].T @ delta_ell)
res_im = np.linalg.norm(delta_ell - Pb_delta) / np.linalg.norm(delta_ell)
At_delta = AtI @ delta_ell
rel_delta = np.linalg.norm(At_delta) / (np.linalg.norm(AtI, ord=2) * np.linalg.norm(delta_ell))
ell_in_im = np.linalg.norm(lens - Ub[:, :rank_b] @ (Ub[:, :rank_b].T @ lens)) / np.linalg.norm(lens)
assert ell_in_im < 1e-9, ell_in_im
assert res_im < 1e-9, res_im
assert rel_delta < 1e-9, rel_delta
record("C_ell在imB", f"{ell_in_im:.3e}", "ell=B@P（径向位移），故 ell∈im(B)")
record("C_delta在imB", f"{res_im:.3e}", "delta ell=dot ell-mu ell 仍在 im(B)")
record("C_At_delta", f"{rel_delta:.3e}", "上一轮 dot eps=tilde L delta ell 在链内恒零")
print(f"[C] ell∈im(B) 残差={ell_in_im:.3e}; delta ell∈im(B) 残差={res_im:.3e}; At@delta ell={rel_delta:.3e}")

# ------------------------------------------------------------------ D 段
# 量纲指数向量：M, L, T, Theta, N(点数)
dim = {"M": 0, "L": 1, "T": 2, "TH": 3, "N": 4}
def dvec(**kw):
    v = np.zeros(5)
    for k, val in kw.items():
        v[dim[k]] = val
    return v
# 耦合强度 λ 无量纲（一个标量）；点数 N 计数 ⇒ mu_(16) 量纲 1/N
mu16_dim = dvec(N=-1)
# dot ell/ell ⇒ (L/T)/L = 1/T
mu17_dim = dvec(T=-1)
assert not np.allclose(mu16_dim, mu17_dim)
record("D_量纲(16)", str(mu16_dim.astype(int).tolist()), "1/[点数]")
record("D_量纲(17)", str(mu17_dim.astype(int).tolist()), "1/[时间]")
print(f"[D] mu16 量纲={mu16_dim.astype(int).tolist()} != mu17 量纲={mu17_dim.astype(int).tolist()}")

# ------------------------------------------------------------------ E 段
# 材料参数（Nb 量级，只作量级核对，非拟合）
GAMMA = 2.0          # 平均 Grüneisen（无量纲）
KT = 1.70e11         # Pa
VM = 1.08e-5         # m^3/mol
TD = 275.0           # K
R_GAS = 8.314462618
DOTT = 1.0           # K/s

def cv_debye(T):
    """每 mol 定容热容（Debye，忽略电子项）。"""
    if T <= 0:
        return 0.0
    xD = TD / T
    integ, _ = quad(lambda x: x**4 * np.exp(x) / (np.exp(x) - 1.0)**2, 1e-12, xD,
                    limit=200)
    return 9.0 * R_GAS * (T / TD)**3 * integ

alpha_V = GAMMA * cv_debye(300.0) / (KT * VM)
mu_th = alpha_V * DOTT / 3.0
# 有限差分：ell(t)=ell0*(1+alpha*dotT*t)^(1/3)，t=0 处 dot ell/ell
h = 1e-6
ell0 = 1.0
ell_p = ell0 * (1.0 + alpha_V * DOTT * h)**(1.0 / 3.0)
ell_m = ell0 * (1.0 - alpha_V * DOTT * h)**(1.0 / 3.0)
mu_fd = (ell_p - ell_m) / (2.0 * h) / ell0
assert abs(mu_fd - mu_th) / mu_th < 1e-4, (mu_fd, mu_th)
record("E_alpha300", f"{alpha_V:.4e}", "K^-1；gamma*Cv/(KT*V)")
record("E_mu热膨胀", f"{mu_th:.4e}", "s^-1；=alpha*dotT/3")
record("E_有限差分", f"{mu_fd:.4e}", "与解析式逐点一致 <1e-4（二阶截断）")
print(f"[E] alpha(300K)={alpha_V:.4e} K^-1, mu_th={mu_th:.4e} s^-1, fd={mu_fd:.4e}")

# ------------------------------------------------------------------ F 段
Ts = np.geomspace(1.0, 30.0, 40)
mus = np.array([GAMMA * cv_debye(T) * DOTT / (3.0 * KT * VM) for T in Ts])
slope = float(np.polyfit(np.log(Ts[:12]), np.log(mus[:12]), 1)[0])
assert abs(slope - 3.0) < 0.2, slope
record("F_Debye斜率", f"{slope:.4f}", "log mu vs log T 低温段 → 3")
print(f"[F] 低温 log-log 斜率={slope:.4f}（→3）")

# ------------------------------------------------------------------ G 段
NU = 9.0
s0 = 1.0
x0 = 7.4271                       # 阈值处卡方分位（R143 G 段）
sig_c = s0 * math.sqrt(x0 / NU)
p0 = chi2.sf(x0, NU)
assert abs(p0 - 0.592746) < 1e-3, p0
eps_grid = np.linspace(0.0, 0.20, 60)
p_abs = np.array([chi2.sf(NU * sig_c**2 / ((s0 * (1.0 + e))**2), NU) for e in eps_grid])
p_rel = np.full_like(eps_grid, p0)   # sigma_c∝ell ⇒ x 不变
assert np.all(np.diff(p_abs) > 0), "绝对阈值下 p 应随膨胀单调上升"
assert np.allclose(p_rel, p0)
record("G_p0", f"{p0:.6f}", "chi2_9 上尾在 x=7.4271")
record("G_绝对阈值", f"{p_abs[0]:.4f}→{p_abs[-1]:.4f}", "应变 0→20%，p 单调上升")
record("G_相对阈值", f"{p_rel[0]:.4f}→{p_rel[-1]:.4f}", "sigma_c∝ell，p 不变")
print(f"[G] p0={p0:.6f}; 绝对阈值 p: {p_abs[0]:.4f}→{p_abs[-1]:.4f}（上升）; 相对阈值不变")

# ------------------------------------------------------------------ 图
fig, axs = plt.subplots(2, 2, figsize=(12, 9))

ax = axs[0, 0]
ax.bar(np.arange(len(rel_errs)), rel_errs, color="#1f77b4", alpha=.7)
ax.axhline(1e-9, color="#d62728", ls="--", lw=1.2, label="1e-9 判据（数值零）")
ax.set_yscale("log")
ax.set_xlabel("随机顶点位移序号")
ax.set_ylabel(r"$\|\dot\varepsilon\|/(\|\tilde A\|\|\dot\ell\|)$")
ax.set_title("(a) 任意位移下亏角不变（强化否证）")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

ax = axs[0, 1]
ax.plot(Ts, mus, color="#1f77b4", lw=2, label=r"$\mu(T)=\gamma C_V\dot T/(3K_TV)$")
ax.plot(Ts, mus[0] * (Ts / Ts[0])**3, color="#d62728", ls="--", lw=1.4,
        label=r"$\propto T^3$（低温）")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("温度 T [K]"); ax.set_ylabel(r"$\mu$ [s$^{-1}$]")
ax.set_title("(b) 热膨胀率的低温冻结")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

ax = axs[1, 0]
ax.plot(100 * eps_grid, p_abs, color="#d62728", lw=2, label="绝对阈值 $\\sigma_c$=const")
ax.plot(100 * eps_grid, p_rel, color="#1f77b4", lw=2, ls="--", label="相对阈值 $\\sigma_c\\propto\\ell$")
ax.set_xlabel("均匀应变 [%]"); ax.set_ylabel(r"$p_{\rm pair}$")
ax.set_title("(c) 阈值口径决定热膨胀是否进 p")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[1, 1]
Tv = np.geomspace(2.0, 300.0, 100)
cv = np.array([cv_debye(T) for T in Tv])
muv = GAMMA * cv * DOTT / (3.0 * KT * VM)
A_aff = 2.0 * muv * float(np.var(lens))
nd0, EC_K = 1e-3, 150.0
nd = nd0 + np.exp(-EC_K / Tv)
ax.plot(Tv, A_aff / A_aff.max(), color="#1f77b4", lw=2, label=r"$A_{\rm aff}$（归一化）")
ax.plot(Tv, nd / nd.max(), color="#2ca02c", lw=2, ls="--", label="预存缺陷 $n_d$（归一化）")
ax.set_xscale("log")
ax.set_xlabel("温度 T [K]"); ax.set_ylabel("归一化强度")
ax.set_title("(d) 两支生产在低温同向熄灭")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

fig.tight_layout()
fig.savefig(os.path.join(OUT, "环17_两个mu与热膨胀入口.png"), dpi=150)
plt.close(fig)

with open(os.path.join(OUT, "环17_两个mu与热膨胀入口_摘要.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f)
    w.writerow(["检查项", "数值", "说明"])
    for r in rows:
        w.writerow(r)

print("\n全部断言通过。图与 CSV 已写。")
