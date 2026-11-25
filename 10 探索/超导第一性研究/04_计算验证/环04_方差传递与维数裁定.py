"""
环 4→5→6／87：方差传递——维数裁定、sigma_v = sigma_0/(4 pi v_tau) 线性化、OU 积分方差（弹道 t^2 → 扩散 t）
========================================================================================================
第 86 轮把模求和维数 d 登记为"待定"（载体 3D vs 建模对象 2D）。本轮做两件事：

 (1) **维数裁定**：06 §0.2 是 ε 的权威定义（3D Regge 复形、铰链＝边、共维 2），
     故 ε 的载体与其简正模（3D 声学支 1 LA + 2 TA，s=1）都在 3D，模式求和 d=3；
     主链 §0.2 的"二维平面晶格"只承担 p_c=1/2（2D 键渗流）与 BKT（L2 相位连通），
     不进入 (4.1) 的模式求和。两个 d 分属不同扇区（L1 几何／弹性 vs L2 连通／相位），
     不是同一个数、无需"统一到一侧"。据此 **维持第 86 轮的 d=3**：
     m_eff=3、sigma_0^2 ∝ Q^4、S_rho=1/6。

 (2) **方差传递链**（环 4 → 5 → 6）：
     - 环 4→5：dv = -deps/(4 pi v_tau) ⇒ sigma_v^2 = sigma_0^2/[16 pi^2 (1-eps/2pi)]。
     - 环 5→6：节点对速度差 X_ij 为零均值 OU，sigma_X^2=2 sigma_v^2 (1-rho)；
       Var[H_ij] = 2 sigma_X^2 [t tau_g - tau_g^2 (1-e^{-t/tau_g})]
       = 4 sigma_v^2 (1-rho)[...]，**弹道 t^2（t<<tau_g）→ 扩散 t（t>>tau_g）**。
     - M9 桥：<V_vbar> = (N-1)/N · sigma_v^2 (1-rho) ≈ (1-rho) sigma_v^2。

**非拟合**：斜率是 log-log 最小二乘指数；其余是对代数恒等式的 MC／求积核验。

可复跑：
    python "10 探索/超导第一性研究/04_计算验证/环04_方差传递与维数裁定.py"
"""
import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_CSV = "环04_方差传递与维数裁定.csv"
OUT_PNG = "环04_方差传递与维数裁定.png"
OUT_TXT = "环04_方差传递与维数裁定_摘要.txt"
LOG = []
rng = np.random.default_rng(20261123)


def emit(s=""):
    print(s)
    LOG.append(s)


def loglog_slope(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = (x > 0) & (y > 0)
    return np.polyfit(np.log(x[m]), np.log(y[m]), 1)[0]


def var_integral_closed(t, tau, sX2):
    """Var[int_0^t X dt]，X 定态 OU：Var[X]=sX2、自协方差 sX2 exp(-|dt|/tau)。"""
    return 2.0 * sX2 * (t * tau - tau ** 2 * (1.0 - np.exp(-t / tau)))


def mc_var_integral(tgrid, tau, sX2, M, batch=2000):
    """分块 MC：返回 Var[H(t)]，H=∫_0^t X dt'（梯形积分），H 的逐时刻均值与二阶矩累积。"""
    dt = tgrid[1] - tgrid[0]
    n = len(tgrid)
    a = math.exp(-dt / tau)
    b = math.sqrt(sX2 * (1.0 - a * a))
    s1 = np.zeros(n); s2 = np.zeros(n); done = 0
    while done < M:
        m = min(batch, M - done)
        X = np.empty((m, n))
        X[:, 0] = rng.normal(0.0, math.sqrt(sX2), m)
        z = rng.normal(0.0, 1.0, (m, n - 1))
        for i in range(1, n):
            X[:, i] = a * X[:, i - 1] + b * z[:, i - 1]
        # 梯形积分（精确到 O(dt^2)，去掉左 Riemann 的 O(dt) 系统偏差）
        H = np.empty_like(X)
        H[:, 0] = 0.0
        H[:, 1:] = np.cumsum(0.5 * (X[:, 1:] + X[:, :-1]), axis=1) * dt
        s1 += H.sum(axis=0)
        s2 += (H * H).sum(axis=0)
        done += m
    mean = s1 / M
    return s2 / M - mean * mean


# ============================================================ [A] OU 积分方差：MC vs 闭式
emit("=" * 70)
emit("[A] OU 积分方差：MC 对比闭式 Var[H]=2 sX2 [t tau - tau^2 (1-e^{-t/tau})]")
emit("=" * 70)
sX2 = 1.0
M_paths = 30000
tmax = 8.0
nsteps = 1600          # dt = 0.005
tgrid = np.linspace(0.0, tmax, nsteps + 1)
taus = [0.5, 1.0, 2.0]
mc_var = {}; closed_curves = {}
for tau in taus:
    mc_var[tau] = mc_var_integral(tgrid, tau, sX2, M_paths)
    closed_curves[tau] = var_integral_closed(tgrid, tau, sX2)
    m = tgrid > 1.0
    rel = np.max(np.abs(mc_var[tau][m] - closed_curves[tau][m]) / closed_curves[tau][m])
    emit(f"  tau={tau:>4}: MC 与闭式最大相对差 (t>1) = {rel:.3e}")
mchk = tgrid > 1.0
A1 = max(np.max(np.abs(mc_var[tau][mchk] - closed_curves[tau][mchk])
                / closed_curves[tau][mchk]) for tau in taus)
emit(f"  断言 A1（MC≡闭式，相对 <2.5%）：{A1:.3e}  {'PASS' if A1 < 0.025 else 'FAIL'}")

# ============================================================ [B] 弹道 t^2 → 扩散 t
emit()
emit("[B] log-log 局部斜率：弹道段 -> 2，扩散段 -> 1，拐点在 t~tau_g")
tau0 = 1.0
tg = np.logspace(-1.5, 2.0, 200)
yv = var_integral_closed(tg, tau0, sX2)
sl = np.gradient(np.log(yv), np.log(tg))
s_bal = loglog_slope(tg[(tg > 0.01) & (tg < 0.05)], yv[(tg > 0.01) & (tg < 0.05)])
s_dif = loglog_slope(tg[(tg > 20) & (tg < 80)], yv[(tg > 20) & (tg < 80)])
emit(f"  弹道段拟合指数 = {s_bal:.3f}（目标 2），扩散段拟合指数 = {s_dif:.3f}（目标 1）")
A2 = abs(s_bal - 2.0); A3 = abs(s_dif - 1.0)
emit(f"  断言 A2（弹道指数≈2）：{A2:.3e}  {'PASS' if A2 < 0.05 else 'FAIL'}")
emit(f"  断言 A3（扩散指数≈1）：{A3:.3e}  {'PASS' if A3 < 0.05 else 'FAIL'}")

# ============================================================ [C] sigma_v = sigma_0/(4 pi v_tau)
emit()
emit("[C] 环 4→5 线性化：v=sqrt(1-eps/2pi)，sigma_v 对比 sigma_0/(4 pi v_tau)")
eps0 = 0.30
vbar = math.sqrt(1.0 - eps0 / (2.0 * math.pi))
sig0_list = np.array([0.002, 0.004, 0.008, 0.016, 0.032])
sigv_meas = []
for s0 in sig0_list:
    eps = eps0 + s0 * rng.normal(0.0, 1.0, 400000)
    v = np.sqrt(1.0 - eps / (2.0 * math.pi))
    sigv_meas.append(v.std())
sigv_analytic = sig0_list / (4.0 * math.pi * vbar)
sigv_meas = np.array(sigv_meas)
ratio_C = sigv_meas / sigv_analytic
A4 = np.max(np.abs(ratio_C - 1.0))
emit(f"  v_tau(eps0={eps0}) = {vbar:.6f}；1/(4 pi v_tau) = {1/(4*math.pi*vbar):.6f}")
emit(f"  实测/解析 = {np.array2string(ratio_C, precision=5)}")
emit(f"  断言 A4（线性化吻合，相对 <1%）：{A4:.3e}  {'PASS' if A4 < 0.01 else 'FAIL'}")

# ============================================================ [D] 空间方差 <-> 时间方差（M9 桥）
emit()
emit("[D] M9 桥：<V_vbar> = (N-1)/N * sigma_v^2 (1-rho)，V_vbar=(1/N) sum_i (v_i-vbar)^2")
Nnodes = 200
sig_v = 0.02
rhos = np.array([0.0, 0.3, 0.6, 0.9])   # 等相关模型 v_i=sqrt(rho)C+sqrt(1-rho)U_i，需 rho>=0
Vmeas = []
for rho in rhos:
    C = rng.normal(0.0, 1.0, 20000)
    U = rng.normal(0.0, 1.0, (20000, Nnodes))
    V = sig_v * (math.sqrt(rho) * C[:, None] + math.sqrt(1.0 - rho) * U)
    Vmeas.append(V.var(axis=1).mean())   # (1/N) sum (v_i-mean)^2
Vmeas = np.array(Vmeas)
Vpred = (Nnodes - 1) / Nnodes * sig_v ** 2 * (1.0 - rhos)
ratio_D = Vmeas / Vpred
A5 = np.max(np.abs(ratio_D - 1.0))
emit(f"  rho 网格 = {np.array2string(rhos, precision=3)}")
emit(f"  实测/预测 = {np.array2string(ratio_D, precision=5)}")
emit(f"  断言 A5（空间↔时间桥，相对 <2%）：{A5:.3e}  {'PASS' if A5 < 0.02 else 'FAIL'}")

# ============================================================ [E] <D> 增长：弹道 t^2 -> 扩散 t
emit()
emit("[E] 环 6：<D>=<H_ij^2>=4 sigma_v^2(1-rho)[t tau_g - tau_g^2(1-e^{-t/tau_g})]")
sig_v2 = 0.02 ** 2
rho_e = 0.0
tau_e = 1.0
D_mc = mc_var_integral(tgrid, tau_e, 2.0 * sig_v2 * (1.0 - rho_e), M_paths)
D_closed = 4.0 * sig_v2 * (1.0 - rho_e) * (
    tgrid * tau_e - tau_e ** 2 * (1.0 - np.exp(-tgrid / tau_e)))
mE = tgrid > 1.0
A6 = np.max(np.abs(D_mc[mE] - D_closed[mE]) / D_closed[mE])
emit(f"  <D> MC 与闭式最大相对差 (t>1) = {A6:.3e}  {'PASS' if A6 < 0.025 else 'FAIL'}")
tg2 = np.logspace(-1.5, 2.0, 200)
Dc = 4.0 * sig_v2 * (1.0 - rho_e) * (tg2 * tau_e - tau_e ** 2 * (1.0 - np.exp(-tg2 / tau_e)))
sE_bal = loglog_slope(tg2[(tg2 > 0.01) & (tg2 < 0.05)], Dc[(tg2 > 0.01) & (tg2 < 0.05)])
sE_dif = loglog_slope(tg2[(tg2 > 20) & (tg2 < 80)], Dc[(tg2 > 20) & (tg2 < 80)])
emit(f"  <D> 弹道指数 = {sE_bal:.3f}（目标 2），扩散指数 = {sE_dif:.3f}（目标 1）")

# ============================================================ [F] 维数裁定：S_rho=1/6、Q^4
emit()
emit("[F] 维数裁定：d=3 模式求和 S_rho=1/6（精确），sigma_0^2 指数 = m_eff+1")
Q = math.pi
Ks = 400
kk = np.arange(1, Ks + 1)
from numpy.polynomial.legendre import leggauss
nodes, wts = leggauss(4000)
qg = 0.5 * Q * (nodes + 1.0)
wg = 0.5 * Q * wts
rho_k = np.empty(Ks)
for idx, k in enumerate(kk):
    integrand = (qg ** 2) * np.sin(qg * k) / k    # rho_3(k)=(4/Q^4)∫q^2 sin(qk)/k dq
    rho_k[idx] = (4.0 / Q ** 4) * np.sum(wg * integrand)
Srho = rho_k.sum()
A7 = abs(Srho - 1.0 / 6.0)
emit(f"  d=3, m=3: sum_k rho_3(k) = {Srho:.6f}（目标 1/6={1/6:.6f}，k<={Ks}）")
emit(f"  断言 A7（S_rho=1/6，|err|<2e-3）：{A7:.3e}  {'PASS' if A7 < 2e-3 else 'FAIL'}")

def sigma0_scaling(d, n=1, s=1, npts=60):
    Qs = np.logspace(-1.0, 0.7, npts)
    p = 2 * n + d - 1 - s
    return Qs, Qs ** (p + 1) / (p + 1)
Q2, v2 = sigma0_scaling(d=2)
Q3, v3 = sigma0_scaling(d=3)
ex2 = loglog_slope(Q2, v2); ex3 = loglog_slope(Q3, v3)
emit(f"  sigma_0^2 的 Q 指数：d=2 -> {ex2:.4f}（=3），d=3 -> {ex3:.4f}（=4）")
A8 = abs(ex3 - 4.0)
emit(f"  断言 A8（d=3 指数=4）：{A8:.3e}  {'PASS' if A8 < 1e-6 else 'FAIL'}")

# ============================================================ 图（六面板）
fig, ax = plt.subplots(2, 3, figsize=(17.5, 9.6))
fig.suptitle("环 4-5-6／第 87 轮：维数裁定（d=3）与方差传递（弹道 t^2 -> 扩散 t）", fontsize=14)

a = ax[0, 0]
colors = ["#1f77b4", "#d62728", "#2ca02c"]
for c, tau in zip(colors, taus):
    a.plot(tgrid, closed_curves[tau], "-", color=c, lw=1.8, label=f"closed tau={tau}")
    a.plot(tgrid[::16], mc_var[tau][::16], "o", color=c, ms=4, mfc="none", label=f"MC tau={tau}")
a.set_xlabel("t"); a.set_ylabel("Var[H_ij]"); a.set_title("(A) OU 积分方差：MC≡闭式")
a.legend(fontsize=7); a.grid(alpha=0.3)

b = ax[0, 1]
b.semilogx(tg, sl, "-", color="#4c72b0")
b.axhline(2.0, ls="--", color="gray", lw=1, label="ballistic=2")
b.axhline(1.0, ls=":", color="gray", lw=1, label="diffusive=1")
b.axvline(tau0, ls="-", color="k", lw=0.8, alpha=0.6)
b.set_xlabel("t/tau_g"); b.set_ylabel("d ln Var / d ln t"); b.set_title("(B) 局部指数：2 -> 1")
b.legend(fontsize=8); b.grid(alpha=0.3)

c = ax[0, 2]
c.plot(sig0_list, sigv_analytic * 1e3, "-", color="#d62728", label="analytic")
c.plot(sig0_list, sigv_meas * 1e3, "o", color="#1f77b4", ms=6, label="numerical")
c.set_xlabel("sigma_0"); c.set_ylabel("sigma_v  [x1e-3]")
c.set_title("(C) 环 4->5：sigma_v = sigma_0/(4 pi v_tau)")
c.legend(fontsize=9); c.grid(alpha=0.3)

d = ax[1, 0]
d.plot(rhos, Vpred * 1e4, "-", color="#d62728", label="(N-1)/N sigma_v^2(1-rho)")
d.plot(rhos, Vmeas * 1e4, "o", color="#1f77b4", ms=6, label="numerical")
d.set_xlabel("rho"); d.set_ylabel("<V_vbar>  [x1e-4]"); d.set_title("(D) M9 桥：空间<->时间方差")
d.legend(fontsize=8); d.grid(alpha=0.3)

e = ax[1, 1]
e.loglog(tg2, Dc, "-", color="#2ca02c", label="closed")
e.loglog(tgrid[::24], D_mc[::24], "o", color="#1f77b4", ms=4, mfc="none", label="MC")
e.loglog(tg2, 4.0 * sig_v2 * (1.0 - rho_e) * tg2 ** 2 / 2.0, "--", color="gray", lw=1, label="~ t^2")
e.loglog(tg2, 4.0 * sig_v2 * (1.0 - rho_e) * tau_e * tg2, ":", color="gray", lw=1, label="~ t")
e.set_xlabel("t"); e.set_ylabel("<D>"); e.set_title("(E) 环 6：<D> 弹道->扩散")
e.legend(fontsize=7); e.grid(alpha=0.3, which="both")

f = ax[1, 2]
cum = np.cumsum(rho_k)
f.plot(kk, cum, "-", color="#9467bd", label="cumulative sum rho")
f.axhline(1/6, ls="--", color="k", lw=1, label="1/6 (exact)")
f.set_xlabel("k"); f.set_ylabel("sum_{k'<=k} rho_3"); f.set_title("(F) 维数裁定：d=3 的 S_rho=1/6")
f.legend(fontsize=9); f.grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(OUT_PNG, dpi=130)
emit()
emit(f"图已保存：{OUT_PNG}")

import csv
with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["panel", "x", "y", "note"])
    for tau in taus:
        for t, vv in zip(tgrid, closed_curves[tau]):
            w.writerow(["A_closed", f"{t:.6f}", f"{vv:.8e}", f"tau={tau}"])
        for t, vv in zip(tgrid[::24], mc_var[tau][::24]):
            w.writerow(["A_mc", f"{t:.6f}", f"{vv:.8e}", f"tau={tau}"])
    for x, y in zip(tg, sl):
        w.writerow(["B_slope", f"{x:.6f}", f"{y:.6f}", ""])
    for s0, sm, sa in zip(sig0_list, sigv_meas, sigv_analytic):
        w.writerow(["C_sigma", f"{s0:.6f}", f"{sm:.8e}", f"analytic={sa:.8e}"])
    for r, vm, vp in zip(rhos, Vmeas, Vpred):
        w.writerow(["D_bridge", f"{r:.6f}", f"{vm:.8e}", f"pred={vp:.8e}"])
    for t, vv in zip(tg2, Dc):
        w.writerow(["E_D_closed", f"{t:.6f}", f"{vv:.8e}", ""])
    for k, cc in zip(kk, cum):
        w.writerow(["F_Srho", f"{k}", f"{cc:.8e}", ""])
emit(f"CSV 已保存：{OUT_CSV}")

emit()
emit("=" * 70)
emit("结论摘要（第 87 轮）")
emit("=" * 70)
emit("1) 维数裁定：ε 载体由 06 §0.2 定为 3D Regge（铰链＝边、共维 2），")
emit("   简正模为 3D 声学支（1 LA+2 TA，s=1）⇒ 模式求和 d=3；")
emit("   主链 §0.2 的 2D 只承担 p_c=1/2 与 BKT（L2 相位连通），不进 (4.1)。")
emit("   ⇒ 维持第 86 轮 d=3：m_eff=3、sigma_0^2∝Q^4、S_rho=1/6（F）。")
emit("2) 环 4→5：sigma_v^2 = sigma_0^2/[16 pi^2 (1-eps/2pi)]（C）。")
emit("3) 环 5→6：Var[H_ij]=4 sigma_v^2(1-rho)[t tau_g - tau_g^2(1-e^{-t/tau_g})]，")
emit("   弹道 t^2 → 扩散 t，拐点 t~tau_g（A,B）。")
emit("4) 环 6：<D>=Var[H_ij] 同形，弹道→扩散（E）。")
emit("5) M9：<V_vbar>≈(1-rho) sigma_v^2，空间↔时间方差需各态历经（D）。")
emit(f"6) 断言：A1={A1:.2e} A2={A2:.2e} A3={A3:.2e} A4={A4:.2e} A5={A5:.2e} "
     f"A6={A6:.2e} A7={A7:.2e} A8={A8:.2e}")
emit(f"   全部 PASS：{all([A1<0.025, A2<0.05, A3<0.05, A4<0.01, A5<0.02, A6<0.025, A7<2e-3, A8<1e-6])}")

with open(OUT_TXT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(LOG) + "\n")
emit(f"摘要已保存：{OUT_TXT}")
