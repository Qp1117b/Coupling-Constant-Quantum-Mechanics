# -*- coding: utf-8 -*-
"""
第 146 轮：环 17 R154.5 可解域符号回修 + 约掉 Tdot 的可测失效判据（无拟合，恒等式 + 解析谱积分）

A 段：Debye 相干带宽 w(T)=(2/wD^2)∫ om*tanh(om/2T) dom，w(0)=1、严格减。
B 段：低温 |dlnw/dT| -> (2 pi^2/3) T/wD^2；高温 -> 1/T。
C 段：可解域符号 R155.1：g<0 时 aLam>r 给 s>0，aLam->r+ 发散，aLam<=r 无物理解。
D 段：Tdot 约掉恒等式 R155.3：不同 Tdot 给同一 r=2 alpha_V/(3 eps |dlnw/dT|)。
E 段：r(T) 两支渐近：绝缘体 r ∝ T^2 -> 0、金属 r -> const、高温 r ∝ T。
F 段：超导温区量级：r<<1，aLam(a)-r>0 稳定，失效面不可达；与 A->0 瓶颈互补。
"""
import math
import csv
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.stats import norm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

WD = 1.0                      # Debye 截止（无量纲化，T 以 wD 为单位）
WD_PHYS = 1000.0              # 示意 Debye 温度 K（材料值外生，仅量级）
NU = 9.0                      # chi^2 自由度（R-143/145 口径）
PC = 0.59274602               # 二维方格渗流阈值
EPS = 2.5929                  # R-145：nu=9,p_c,t=1 处尾概率弹性 epsilon_nu
PI2_3 = 2.0 * math.pi ** 2 / 3.0

REC = []
def record(key, value, note):
    REC.append((key, value, note))


# ------------------------------------------------------------------ A 段：w(T)
def w_of(T):
    if T <= 0:
        return 1.0
    val = quad(lambda om: om * math.tanh(om / (2.0 * T)), 0.0, WD,
               epsabs=1e-14, epsrel=1e-14)[0]
    return 2.0 * val / WD ** 2


Tgrid = np.array([1e-3, 3e-3, 1e-2, 3e-2, 0.1, 0.3, 1.0, 3.0, 10.0])
wgrid = np.array([w_of(float(t)) for t in Tgrid])
assert abs(wgrid[0] - 1.0) < 1e-5, wgrid[0]
assert np.all(np.diff(wgrid) < 0), "w 应严格减"
record("A_w端点", f"{wgrid[0]:.6f}→{wgrid[-1]:.6f}", "w(0)=1，升温严格减")


# ------------------------------------------------------------------ B 段：dlnw/dT 两支
def dlnw(T, h=1e-5):
    h = min(h, T * 1e-3)       # 保证小 T 下差分不越界
    return (math.log(w_of(T + h)) - math.log(w_of(T - h))) / (2.0 * h)

low_ratio = [abs(dlnw(float(t))) * WD ** 2 / float(t) for t in Tgrid[:3]]
assert max(abs(x - PI2_3) for x in low_ratio) < 0.01, low_ratio
rec_lo = abs(dlnw(10.0)) * 10.0
assert abs(rec_lo - 1.0) < 0.02, rec_lo
record("B_低温斜率", f"{low_ratio[0]:.5f}", f"理论 2π²/3={PI2_3:.5f}，T/wD=1e-3")
record("B_高温斜率", f"{rec_lo:.5f}", "|dlnw/dT|·T→1，T/wD=10")


# ------------------------------------------------------------------ C 段：可解域符号回修
def s_solution(alam, g, mu, C=1.0):
    den = g * alam + 2.0 * mu
    if abs(den) < 1e-14:
        return math.inf
    return 2.0 * g / (C * den)

g_neg, mu_pos, C0 = -1.0, 0.1, 1.0
r_ex = 2.0 * mu_pos / abs(g_neg)              # =0.2
for al in [0.05, 0.19]:                        # aLam < r
    assert s_solution(al, g_neg, mu_pos, C0) < 0
for al in [0.21, 0.5, 1.0]:                    # aLam > r
    assert s_solution(al, g_neg, mu_pos, C0) > 0
assert math.isinf(s_solution(r_ex, g_neg, mu_pos, C0))
# 降温相 g>0：恒可解
for al in [0.05, 0.2, 0.5, 2.0]:
    assert s_solution(al, 1.0, mu_pos, C0) > 0
# 与 R155.7 的 2/[C(aLam-r)] 等价
for al in [0.21, 0.5, 1.0]:
    assert abs(s_solution(al, g_neg, mu_pos, C0) - 2.0 / (C0 * (al - r_ex))) < 1e-12
record("C_可解域", f"r={r_ex:.3f}", "aLam<r⇒s<0；aLam>r⇒s>0；aLam↓r+⇒s→∞（回修 R154.5）")
record("C_降温相", "g>0 恒 s>0", "无失效面，与 R-154 卡该结论一致")


# ------------------------------------------------------------------ D 段：Tdot 约掉
def r_from_rates(alpha_V, T, Tdot, eps=EPS):
    mu = alpha_V * Tdot / 3.0
    g = eps * dlnw(T) * Tdot
    return 2.0 * mu / abs(g)

def r_material(alpha_V, T, eps=EPS):
    return 2.0 * alpha_V / (3.0 * eps * abs(dlnw(T)))

for td in [1e-3, 0.1, 1.0, 37.0, 1e4]:
    a = r_from_rates(1e-6, 0.01, td)
    b = r_material(1e-6, 0.01)
    assert abs(a - b) < 1e-12, (td, a, b)
record("D_Tdot约掉", "5 个 Tdot 同值", "r=2α_V/(3ε|dlnw/dT|)，残差<1e-12")


# ------------------------------------------------------------------ E 段：r(T) 两支
# 单位约定：r_material 内 T 以 wD 为单位，故传入的 alpha 需为
# alpha_ratio = d ln V / d(T/wD) = wD * alpha_phys。物理 r 无量纲、两单位制同值。
alpha0_phys = 1e-5            # /K，高温 Debye 膨胀系数量级
alpha0_ratio = alpha0_phys * WD_PHYS
# 绝缘体：alpha_V ∝ T^3 ⇒ r ∝ T^2（低温）
r_ins = np.array([r_material(alpha0_ratio * float(t) ** 3, float(t)) for t in Tgrid[:3]])
slopes_ins = np.diff(np.log(r_ins)) / np.diff(np.log(Tgrid[:3]))
assert all(abs(sl - 2.0) < 0.05 for sl in slopes_ins), slopes_ins
# 金属：alpha_V = a1*T ⇒ r -> const（低温）
a1_phys = 1e-8
a1_ratio = a1_phys * WD_PHYS
r_met = np.array([r_material(a1_ratio * float(t), float(t)) for t in Tgrid[:3]])
assert max(r_met) / min(r_met) < 1.02, r_met
# 高温：alpha_V -> const，|dlnw/dT|=1/T ⇒ r ∝ T（需 T/wD >> 1 才进渐近）
Thi = np.array([3.0, 10.0, 30.0])
r_hi = np.array([r_material(alpha0_ratio, float(t)) for t in Thi])
slopes_hi = np.diff(np.log(r_hi)) / np.diff(np.log(Thi))
assert all(abs(sl - 1.0) < 0.02 for sl in slopes_hi), slopes_hi
record("E_绝缘体", f"斜率 {slopes_ins[0]:.4f}", "ln r–ln T 斜率=2（r∝T²→0）")
record("E_金属", f"r≈{r_met[0]:.3e}", "低温 r→a1·wD²/(επ²) 常数")
record("E_高温", f"斜率 {slopes_hi[0]:.4f}", "ln r–ln T 斜率=1（r∝T）")


# ------------------------------------------------------------------ F 段：超导温区量级
Tc_ratio = 1e-2                                # T/wD ~ 0.01（超导温区）
alpha_Tc_ratio = alpha0_ratio * Tc_ratio ** 3  # 绝缘体 Debye 律外推（ratio 单位）
r_Tc = r_material(alpha_Tc_ratio, Tc_ratio)    # r 无量纲，两单位制同值
a_test = 0.5
aLam = a_test * norm.pdf(a_test) / norm.sf(a_test)
s_Tc = 2.0 / (C0 * (aLam - r_Tc))
assert 1e-9 < r_Tc < 1e-6, r_Tc
assert s_Tc > 0 and np.isfinite(s_Tc)
record("F_超导温区r", f"{r_Tc:.3e}", "wD=1000K,T=10K,α0=1e-5/K→α=1e-11/K（仅量级）")
record("F_可解稳定", f"s={s_Tc:.3f}", "a=0.5 时 aλ=0.571≫r，反馈发散不可达")


# ------------------------------------------------------------------ 图
fig, axs = plt.subplots(2, 2, figsize=(11, 8))

ax = axs[0, 0]
tplot = np.logspace(-3, 1, 200)
ax.plot(tplot, [w_of(float(t)) for t in tplot], color="#1f77b4", lw=2, label=r"$w(T)$")
ax.set_xscale("log"); ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$w=V_{\rm coh}/Z$")
ax.set_title("(a) 链内相干带宽：升温单调减")
ax.legend(fontsize=9); ax.grid(alpha=.3)

ax = axs[0, 1]
dl = np.array([abs(dlnw(float(t))) for t in tplot])
ax.plot(tplot, dl, color="#1f77b4", lw=2, label=r"$|d\ln w/dT|$")
ax.plot(tplot, (PI2_3 / WD**2) * tplot, "--", color="#d62728", lw=1.2,
        label=rf"低温 $2\pi^2 T/3\omega_D^2$")
ax.plot(tplot, 1.0 / tplot, ":", color="#2ca02c", lw=1.2, label=r"高温 $1/T$")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$|d\ln w/dT|$")
ax.set_title("(b) 导数两支渐近")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[1, 0]
alam_grid = np.linspace(0.02, 2.0, 400)
ax.plot(alam_grid, 2.0 / (C0 * (alam_grid - r_ex)), color="#1f77b4",
        lw=2, label=rf"$s=2/[C(a\lambda-r)]$, $r={r_ex}$")
ax.axhline(0, color="k", lw=.8)
ax.axvline(r_ex, color="#d62728", ls="--", lw=1.2, label="发散失效面 $a\\lambda=r$")
ax.set_ylim(-20, 20); ax.set_xlabel(r"$a\lambda(a)$"); ax.set_ylabel(r"$s$")
ax.set_title("(c) 符号回修：$a\\lambda>r$ 才可解")
ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axs[1, 1]
tshow = np.logspace(-3, 1, 120)
dl_show = np.array([abs(dlnw(float(t))) for t in tshow])
r_ins_show = 2.0 * (alpha0_ratio * tshow ** 3) / (3.0 * EPS * dl_show)
r_met_show = 2.0 * (a1_ratio * tshow) / (3.0 * EPS * dl_show)
r_hi_show = 2.0 * alpha0_ratio / (3.0 * EPS * dl_show)
ax.plot(tshow, r_ins_show, color="#1f77b4", lw=2, label="绝缘体 $r\\propto T^2$")
ax.plot(tshow, r_met_show, color="#2ca02c", lw=2, label="金属 $r\\to$常数")
ax.plot(tshow, r_hi_show, color="#d62728", lw=1.5, ls="--", label="常规 $r\\propto T$（高温α常值外推）")
ax.axhline(aLam, color="#7f7f7f", ls=":", lw=1.2, label=rf"$a\lambda(0.5)={aLam:.3f}$")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$r=2\mu/|g|$")
ax.set_title("(d) 可测失效判据 $a\\lambda(a)=r(T)$")
ax.legend(fontsize=8); ax.grid(alpha=.3)

fig.suptitle("第146轮：可解域符号回修与约掉 $\\dot T$ 的可测失效判据", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig("环17_可测失效判据.png", dpi=150)

with open("环17_可测失效判据_摘要.csv", "w", newline="", encoding="utf-8-sig") as f:
    wr = csv.writer(f)
    wr.writerow(["检验项", "数值", "说明"])
    for k, v, note in REC:
        wr.writerow([k, v, note])

for k, v, note in REC:
    print(f"[{k}] {v} — {note}")
print("图已保存：环17_可测失效判据.png；摘要：环17_可测失效判据_摘要.csv")
