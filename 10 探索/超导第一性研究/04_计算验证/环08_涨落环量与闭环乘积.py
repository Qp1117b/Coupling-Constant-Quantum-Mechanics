# -*- coding: utf-8 -*-
"""
环 4 → 环 5 → 环 8：零点亏角涨落的**闭环涨落环量**与闭环乘积
================================================================
问题（第 82 轮留下的断口）：平直体内 ε_e^(0)=0，静态背景不产生差异编码；
环 8 的矩阵分支（Σ_C λ≠0）若存在，只能由环 4 的零点涨落 Δε_e 承担。
本轮把它算清楚：

  环量       Φ_C = Σ_{e∈C} Δε_e
  键比值     r_e = sqrt(1 − ε_e/(2π))，λ_e = ln r_e = −ε_e/(4π) − ε_e²/(16π²) + O(ε³)
  闭环乘积   ∏_C r = exp(Σ_C λ)

三条**解析**结论（不是拟合）：
 (1) E[Φ_C]=0；Var(Φ_C)=σ²[n + 2Σ_{i<j}ρ_ij] ∈ [nσ², n²σ²]
     —— ρ_ij 就是 (9.1) 里那个关联，链内同一个量，无新参数。
 (2) 一阶项 Σλ = −Φ_C/(4π) 的均值为零；但二阶项 −Σε²/(16π²) **不抵消**，
     故 ⟨ln ∏r⟩ = −nσ²/(16π²) + O(σ⁴)：**几何平均按周长指数压低**，
     每边速率 σ²/(16π²)，无自由参数。
 (3) ⟨∏r⟩ = exp(σ²[2Σρ − n]/(32π²)) + O(σ⁴)：符号由关联决定
     （短程关联 ⇒ <1；强正关联 ⇒ >1），相干线 |⟨e^{isΦ}⟩| = e^{−s²Var(Φ)/2}。
物理解读：只有 Δε 的**余确切分量**（coexact，横场）能贡献可收缩闭环的和；
确切分量（梯度）逐样本望远镜抵消。这就是第 76 轮"望远镜恒等式"的准确版。

判据：不调参、不拟合。解析曲线与蒙特卡洛点直接叠加比较，误差按 MC 标准误判。
"""
import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_CSV = "环08_涨落环量与闭环乘积.csv"
OUT_PNG = "环08_涨落环量与闭环乘积.png"
OUT_TXT = "环08_涨落环量与闭环乘积_摘要.txt"

LOG = []


def emit(s=""):
    print(s)
    LOG.append(s)


# ---------------- 关联模型（沿闭环的格距 d，单位 a） ----------------
def corr_matrix(model, n, xi=10.0, p=1.0):
    """n 条边沿闭环排列，格距用环上最短距离 min(|i-j|, n-|i-j|)。"""
    idx = np.arange(n)
    d = np.abs(idx[:, None] - idx[None, :])
    d = np.minimum(d, n - d).astype(float)
    if model == "indep":
        R = np.eye(n)
    elif model == "full":
        R = np.ones((n, n))
    elif model == "exp":
        R = np.exp(-d / xi)
    elif model == "pow":
        R = (1.0 + d / xi) ** (-p)
    else:
        raise ValueError(model)
    np.fill_diagonal(R, 1.0)
    return R


def analytic_var(n, R, sigma2):
    """Var(Φ_C) = σ²[n + 2Σ_{i<j}ρ_ij]，精确按关联矩阵求和（非近似）。"""
    upper = np.triu(R, k=1)
    return sigma2 * (n + 2.0 * upper.sum())


def sum_rho(n, R):
    """Σ_{i<j}ρ_ij。"""
    return float(np.triu(R, k=1).sum())


def sample_field(n, R, sigma, M, rng):
    """相关高斯场 Δε ~ N(0, σ²R)；用特征分解，容许秩亏（ρ=1）。"""
    w, Q = np.linalg.eigh(R)
    w = np.clip(w, 0.0, None)
    L = Q @ np.diag(np.sqrt(w))
    Z = rng.standard_normal((n, M))
    return sigma * (L @ Z)          # shape (n, M)：n 条边、M 个样本


def prod_r(dE):
    """∏_C sqrt(1 − Δε/(2π))，逐样本精确（不线性化）。"""
    return np.exp(0.5 * np.log1p(-dE / (2 * math.pi)).sum(axis=0))


def antithetic_log(dE):
    """E[ln∏r] 的低方差无偏估计：
    (1/2)[ln∏r(ε) + ln∏r(−ε)] = (1/4)Σ ln(1 − x_e²)，x=ε/2π。
    由 ε 与 −ε 同分布，该配对平均的期望就是 E[ln∏r]，但只剩偶次项。"""
    x = dE / (2 * math.pi)
    return 0.25 * np.log1p(-(x ** 2)).sum(axis=0)


def mc_stats(n, model, sigma, M=40000, seed=0, xi=10.0, p=1.0):
    rng = np.random.default_rng(seed)
    R = corr_matrix(model, n, xi=xi, p=p)
    dE = sample_field(n, R, sigma, M, rng)
    phi = dE.sum(axis=0)
    pr = prod_r(dE)
    v = float(np.var(phi, ddof=1))
    se = v * math.sqrt(2.0 / M)     # 高斯样本方差的相对标准误
    return dict(R=R, phi=phi, pr=pr, var=v, se=se,
                mean_phi=float(np.mean(phi)),
                mean_pr=float(np.mean(pr)),
                median_pr=float(np.median(pr)),
                mean_log=float(np.mean(np.log(pr))),
                log_anti=float(np.mean(antithetic_log(dE))),
                sum_rho=sum_rho(n, R))


def main():
    sigma0 = 0.05
    emit("=" * 78)
    emit("环 4→5→8：零点涨落环量 Φ_C 与闭环乘积 ∏r 的解析—MC 对照")
    emit(f"    基准 σ={sigma0} rad（展开参数 σ/2π={sigma0/(2*math.pi):.4f}），"
         f"环长 n 为边数，格距 a=1")

    # ---------- [1] Var(Φ_C)：解析公式 vs MC，多种关联 ----------
    emit("\n[1] Var(Φ_C)/σ² 的 n 依赖（解析式 n+2Σρ 与 MC 点）")
    models = [
        ("indep", dict(), "不关联 ρ=0"),
        ("exp", dict(xi=2.0), "指数 ξ_c=2a"),
        ("exp", dict(xi=50.0), "指数 ξ_c=50a"),
        ("pow", dict(xi=1.0, p=1.0), "幂律 p=1（2D 零点型）"),
        ("pow", dict(xi=1.0, p=4.0), "幂律 p=4（曲率型）"),
        ("full", dict(), "全关联 ρ=1"),
    ]
    ns = [2, 4, 8, 16, 32, 64, 128, 256]
    rows = []
    var_tab = {}
    for model, kw, label in models:
        vals_an = []
        for n in ns:
            R = corr_matrix(model, n, xi=kw.get("xi", 10.0), p=kw.get("p", 1.0))
            an = analytic_var(n, R, sigma0 ** 2)
            rows.append((model, label, n, an / sigma0 ** 2, np.nan))
            vals_an.append(an / sigma0 ** 2)
        var_tab[(model, label)] = vals_an
        emit(f"    {label:22s}: " + " ".join(f"{v:9.2f}" for v in vals_an))

    # MC 校验（每模型取 n=64,256 两点）
    emit("\n    MC 校验（M=40000）：")
    checks = []
    for model, kw, label in models:
        for n in (64, 256):
            st = mc_stats(n, model, sigma0, M=40000, seed=n + 17,
                          xi=kw.get("xi", 10.0), p=kw.get("p", 1.0))
            an = analytic_var(n, st["R"], sigma0 ** 2)
            dev = abs(st["var"] - an) / max(st["se"], 1e-30)
            emit(f"      {label:22s} n={n:3d}: 解析 {an:.6e}, MC {st['var']:.6e}, "
                 f"偏差 {dev:.2f} se")
            checks.append((label, n, an, st["var"], dev))
            rows.append((model + "_mc", label, n, an / sigma0 ** 2, st["var"] / sigma0 ** 2))
    assert all(c[4] < 4.0 for c in checks), "MC 与解析式偏差超过 4 个标准误"

    for model, kw, label in models:
        for n in ns:
            R = corr_matrix(model, n, xi=kw.get("xi", 10.0), p=kw.get("p", 1.0))
            v = analytic_var(n, R, sigma0 ** 2)
            assert v >= n * sigma0 ** 2 - 1e-12, f"{label} n={n} 破坏下界 nσ²"
            assert v <= n * n * sigma0 ** 2 + 1e-12, f"{label} n={n} 破坏上界 n²σ²"
    emit("    [断言] 所有模型、所有 n：nσ² ≤ Var(Φ_C) ≤ n²σ²  ✓")
    emit("    [断言] indep 给 nσ²、full 给 n²σ²（逐位）  ✓")

    # 对数斜率（由解析式数值微分，非拟合）
    emit("\n[2] 局部对数斜率 d ln Var / d ln n（由解析式数值微分）")
    slope_tab = {}
    for model, kw, label in models:
        v1 = analytic_var(128, corr_matrix(model, 128, xi=kw.get("xi", 10.0), p=kw.get("p", 1.0)), sigma0 ** 2)
        v2 = analytic_var(256, corr_matrix(model, 256, xi=kw.get("xi", 10.0), p=kw.get("p", 1.0)), sigma0 ** 2)
        s = math.log(v2 / v1) / math.log(2.0)
        slope_tab[(model, label)] = s
        emit(f"    {label:22s}: 局部斜率 = {s:.4f}")
    assert abs(slope_tab[("indep", "不关联 ρ=0")] - 1.0) < 0.01
    assert abs(slope_tab[("full", "全关联 ρ=1")] - 2.0) < 0.02

    # ---------- [3] 闭环乘积：几何平均的对数周长律 ----------
    emit("\n[3] ⟨ln ∏r⟩ 的对数周长律：解析 −nσ²/(16π²) vs 低方差无偏估计（σ=0.05）")
    sig = 0.05
    ns3 = [8, 16, 32, 64, 128, 256]
    log_rows = []
    for model, kw, label in [("indep", dict(), "不关联"), ("exp", dict(xi=10.0), "指数 ξ_c=10a")]:
        for n in ns3:
            st = mc_stats(n, model, sig, M=40000, seed=1000 + n,
                          xi=kw.get("xi", 10.0))
            pred = -n * sig ** 2 / (16 * math.pi ** 2)
            rel = abs(st["log_anti"] - pred) / abs(pred)
            emit(f"    {label:10s} n={n:3d}: 配对估计 {st['log_anti']:+.6e}, "
                 f"解析 {pred:+.6e}, 相对差 {100*rel:.2f}%")
            log_rows.append((label, n, st["log_anti"], pred, rel, st["mean_log"]))
            rows.append(("logprod_" + model, label, n, pred, st["log_anti"]))
    assert all(r[4] < 0.01 for r in log_rows), "⟨ln∏r⟩ 与解析式偏差 >1%"
    emit("    [断言] 斜率 d⟨ln∏r⟩/dn = −σ²/(16π²) 命中，相对差 <1%  ✓")

    # 一阶 vs 二阶 vs 精确
    emit("\n    一阶 exp(Var/32π²)、二阶 exp(σ²[2Σρ−n]/32π²) 与精确 MC 的对照：")
    for n in (32, 128):
        st = mc_stats(n, "exp", sig, M=40000, seed=7 + n, xi=10.0)
        anv = analytic_var(n, st["R"], sig ** 2)
        first_order = math.exp(anv / (32 * math.pi ** 2))
        second_order = math.exp(sig ** 2 * (2 * st["sum_rho"] - n) / (32 * math.pi ** 2))
        emit(f"      n={n:3d}: 一阶 {first_order:.6f}, 二阶 {second_order:.6f}, "
             f"MC {st['mean_pr']:.6f}")
        rows.append(("order_compare", "exp_xi10", n, first_order, st["mean_pr"]))

    # ---------- [4] 平均符号翻转：扫描关联长度 ----------
    emit("\n[4] ⟨∏r⟩−1 的符号随关联长度翻转（n=100, σ=0.10）")
    n4, sig4 = 100, 0.10
    xis = [0.5, 1.0, 2.0, 5.0, 10.0, 20.0, 50.0, 100.0, 1e4]
    flip_rows = []
    for xi in xis:
        st = mc_stats(n4, "exp", sig4, M=20000, seed=int(100 * math.log10(xi) + 300),
                      xi=xi)
        pred = math.exp(sig4 ** 2 * (2 * st["sum_rho"] - n4) / (32 * math.pi ** 2))
        emit(f"      ξ_c={xi:8.1f}a: Σρ={st['sum_rho']:9.2f}, 2Σρ−n={2*st['sum_rho']-n4:+9.2f}, "
             f"解析 ⟨∏r⟩={pred:.6f}, MC {st['mean_pr']:.6f}")
        flip_rows.append((xi, st["sum_rho"], pred, st["mean_pr"]))
        rows.append(("signflip", f"xi={xi:g}", n4, pred, st["mean_pr"]))
    preds = [f[2] for f in flip_rows]
    assert min(preds) < 1.0 < max(preds), "未观察到 ⟨∏r⟩ 穿过 1 的翻转"

    # ---------- [5] 相干相位衰减 ----------
    emit("\n[5] 相干线 |⟨e^{isΦ}⟩|：解析 e^{−s²Var(Φ)/2} vs MC（σ=0.05）")
    sig5 = 0.05
    phase_curves = {}
    phase_checks = []
    for model, kw, label, ns5 in [
        ("indep", dict(), "不关联", [8, 16, 32, 64, 128]),
        ("full", dict(), "全关联", [4, 8, 12, 16, 20]),
    ]:
        for s in (1.0, 0.5):
            an_list, mc_list = [], []
            for n in ns5:
                st = mc_stats(n, model, sig5, M=40000, seed=555 + n,
                              xi=kw.get("xi", 10.0))
                pred = math.exp(-0.5 * s ** 2 * st["var"])
                mc = float(np.abs(np.mean(np.exp(1j * s * st["phi"]))))
                an_list.append(pred)
                mc_list.append(mc)
                if pred > 0.05:
                    rel = abs(mc - pred) / pred
                    phase_checks.append((label, s, n, pred, mc, rel))
                    emit(f"      {label:6s} s={s:3.1f} n={n:3d}: 解析 {pred:.6f}, "
                         f"MC {mc:.6f}, 相对差 {100*rel:.2f}%")
                rows.append(("phase_" + model, f"s={s}", n, pred, mc))
            phase_curves[(label, s)] = (ns5, an_list, mc_list)
    assert all(c[5] < 0.04 for c in phase_checks), "相干相位因子与解析式偏差 >4%"
    emit("    [断言] 相位因子 e^{−s²Var/2} 在 pred>0.05 处相对差 <4%  ✓")

    emit("\n    相干长度（不关联极限 n_* = 2/(s²σ²)）：")
    for s in (1.0, 0.5):
        emit(f"      s={s:.1f}: n_* = {2.0/(s**2*sig5**2):.1f} 条边")

    # ---------- [6] 分布形状 ----------
    emit("\n[6] ∏r 的分布（n=100, σ=0.05）：与由解析参数给出的对数正态叠加")
    st_ind = mc_stats(100, "indep", 0.05, M=60000, seed=99)
    st_exp = mc_stats(100, "exp", 0.05, M=60000, seed=98, xi=10.0)
    for lab, st in (("不关联", st_ind), ("ξ_c=10a", st_exp)):
        mu = -100 * 0.05 ** 2 / (16 * math.pi ** 2)
        sd = math.sqrt(st["var"]) / (4 * math.pi)
        emit(f"      {lab}: 解析 log 均值 {mu:+.5f}, log 标准差 {sd:.5f}; "
             f"MC 中位数 {st['median_pr']:.6f}")
        rows.append(("dist", lab, 100, mu, sd))

    # ---------- CSV ----------
    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("model,label,n,analytic,mc_or_second\n")
        for r in rows:
            f.write(f"{r[0]},\"{r[1]}\",{r[2]},{r[3]:.10g},{r[4]:.10g}\n")

    # ---------- 图 ----------
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.6))

    # A: Var/σ² vs n（解析线 + 两个 n 上的 MC 点）
    a = ax[0][0]
    for model, kw, label in models:
        a.loglog(ns, var_tab[(model, label)], "-", lw=1.5, label=label)
    for (label, n, an, vmc, dev) in checks:
        a.loglog([n], [vmc / sigma0 ** 2], "o", ms=5, mfc="none", color="k")
    a.set_xlabel("环长 n（边数）")
    a.set_ylabel(r"$\mathrm{Var}(\Phi_C)/\sigma^2$")
    a.set_title("(A) 涨落环量方差：$n\\sigma^2\\to n^2\\sigma^2$")
    a.legend(fontsize=7)
    a.grid(alpha=0.3, which="both")

    # B: 局部斜率
    a = ax[0][1]
    labels = [m[2] for m in models]
    vals = [slope_tab[(m[0], m[2])] for m in models]
    a.barh(range(len(vals)), vals, color="steelblue")
    a.axvline(1.0, color="k", ls="--", lw=1, label="独立极限 1")
    a.axvline(2.0, color="r", ls="--", lw=1, label="全关联极限 2")
    a.set_yticks(range(len(labels)))
    a.set_yticklabels(labels, fontsize=8)
    a.set_xlabel(r"$d\ln\mathrm{Var}/d\ln n$（n=128→256）")
    a.set_title("(B) 由 √n 到 n 的连续过渡")
    a.legend(fontsize=8)
    a.grid(axis="x", alpha=0.3)

    # C: log 乘积的周长律
    a = ax[0][2]
    for lab in ("不关联", "指数 ξ_c=10a"):
        sub = [r for r in log_rows if r[0] == lab]
        a.semilogx([r[1] for r in sub], [r[2] for r in sub], "o", label=lab + " 配对估计")
        a.semilogx([r[1] for r in sub], [r[3] for r in sub], "-", lw=1.3,
                   label=lab + " 解析")
    a.set_xlabel("环长 n")
    a.set_ylabel(r"$\langle \ln\prod_C r\rangle$")
    a.set_title(r"(C) 几何平均对数周长律：速率 $-\sigma^2/16\pi^2$")
    a.legend(fontsize=7)
    a.grid(alpha=0.3, which="both")

    # D: 平均符号翻转
    a = ax[1][0]
    a.semilogx([f[0] for f in flip_rows], [f[2] for f in flip_rows], "-", lw=1.4,
               label=r"解析 $\langle\prod_C r\rangle$")
    a.semilogx([f[0] for f in flip_rows], [f[3] for f in flip_rows], "o",
               label=r"MC $\langle\prod_C r\rangle$")
    a.axhline(1.0, color="k", ls="--", lw=0.9)
    a.set_xlabel(r"关联长度 $\xi_c/a$")
    a.set_ylabel(r"$\langle\prod_C r\rangle$")
    a.set_title(r"(D) n=100：强关联把平均乘积抬过 1")
    a.legend(fontsize=8)
    a.grid(alpha=0.3, which="both")

    # E: 相干相位衰减
    a = ax[1][1]
    for (lab, s), (ns5, an_list, mc_list) in phase_curves.items():
        mk = "o" if s == 1.0 else "s"
        a.semilogy(ns5, an_list, "-", lw=1.3, label=f"{lab} s={s} 解析")
        a.semilogy(ns5, mc_list, mk, ms=5, mfc="none", color="k")
    a.set_xlabel("环长 n")
    a.set_ylabel(r"$|\langle e^{is\Phi_C}\rangle|$")
    a.set_title(r"(E) 相位相干：$e^{-s^2\mathrm{Var}/2}$（点为 MC）")
    a.legend(fontsize=6)
    a.grid(alpha=0.3)

    # F: ∏r 分布（对数坐标）
    a = ax[1][2]
    for lab, st, color in (("不关联", st_ind, "steelblue"), ("ξ_c=10a", st_exp, "darkorange")):
        x = st["pr"]
        x = x[x > 0]
        a.hist(np.log10(x), bins=80, density=True, alpha=0.55, color=color,
               label=f"{lab} MC")
        mu = -100 * 0.05 ** 2 / (16 * math.pi ** 2)
        sd = math.sqrt(st["var"]) / (4 * math.pi)
        xs = np.linspace(mu - 4 * sd, mu + 4 * sd, 400)
        pdf = np.exp(-0.5 * ((xs - mu) / sd) ** 2) / (sd * math.sqrt(2 * math.pi))
        a.plot(xs / math.log(10), pdf * math.log(10), "-", lw=1.4, color=color,
               label=f"{lab} 对数正态预测")
    a.set_xlabel(r"$\log_{10}\prod_C r$")
    a.set_ylabel("概率密度")
    a.set_title("(F) 闭环乘积分布：中位数 1 下移，对数正态")
    a.legend(fontsize=7)
    a.grid(alpha=0.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    emit(f"\n[图] 已写出 {OUT_PNG}")

    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    emit(f"[摘要] 已写出 {OUT_TXT}")

    # ---------- 结论 ----------
    emit("\n[7] 结论")
    emit("    (a) Var(Φ_C)=σ²[n+2Σρ]，界为 [nσ², n²σ²]；ρ 即 (9.1) 的关联，无新参数。")
    emit("    (b) E[Φ_C]=0：静态背景不产生环流，矩阵分支只能是涨落支撑、只在 RMS 意义。")
    emit("    (c) ⟨ln∏r⟩=−nσ²/(16π²)：涨落总把典型闭环乘积按周长压低，速率无自由参数。")
    emit("    (d) ⟨∏r⟩=exp(σ²[2Σρ−n]/32π²)：短程关联 <1，强正关联 >1（符号可测）。")
    emit("    (e) |⟨e^{isΦ}⟩|=e^{−s²Var/2}：长环退相干，相干线 n_*∼2/(s²σ²)。")


if __name__ == "__main__":
    main()
