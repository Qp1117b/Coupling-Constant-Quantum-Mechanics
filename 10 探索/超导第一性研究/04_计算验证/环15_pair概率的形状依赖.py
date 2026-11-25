# -*- coding: utf-8 -*-
r"""
第 140 轮：环 15 的 $p_{\rm pair}$ 对分布形状的依赖——无假设界与 Edgeworth 修正
=================================================================================
前件：R148 判「环 15 的 $p_{\rm pair}$ 完全依赖 $\varepsilon$ 的分布族」。

(15.1) $p_{\rm pair}=\Pr[\sigma_\ell>\sigma_c]$，其中 $\sigma_\ell^2$ 是**局域方差估计**
（$n$ 个独立模的样本方差），不是 $\varepsilon$ 本身。故形状依赖来自
「样本方差的分布」，由 $\varepsilon$ 的三阶、四阶矩控制。

本轮给两层结论：

  A. **分布无关的界**（Cantelli）：对任何 $E[X]=1$、$\mathrm{Var}(X)=v$ 的正变量，
     $$\Pr[X\ge 1+k\sqrt v]\le\frac{1}{1+k^2}.$$
     故 $p_{\rm pair}$ 有不需要分布族的上界；与高斯尾的差就是「形状税」。

  B. **形状依赖的定量**（Edgeworth）：$p_{\rm pair}(r)$ 对偏度 $\gamma_1$ 的
     一阶修正为
     $$\delta p=-\frac{\gamma_1}{6}(z^2-1)\phi(z),\qquad z=\Phi^{-1}(1-p),$$
     故要达到 $p_c$ 的 $\epsilon$ 精度，需 $\gamma_1$ 精确到 $6\epsilon/[|(z^2-1)\phi(z)|]$。

  C. 数值：四种分布（高斯／Gamma／对数正态／Beta）同 $(\mu,\sigma^2)$ 下的
     $p_{\rm pair}$ 与样本方差分布，与 A、B 对照。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环15_pair概率的形状依赖.py"
"""
import csv
import math
import os

import numpy as np
from scipy import stats
from scipy.integrate import quad
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))


def cantelli_upper(r, v):
    """Cantelli：Pr[X >= r] <= v/(v+(r-1)^2)，E[X]=1，Var=v，r>1。"""
    if r <= 1:
        return 1.0
    return v / (v + (r - 1) ** 2)


def main():
    print("=" * 78)
    print("A. Cantelli 界（分布无关）vs 高斯尾")
    print("=" * 78)
    print(f"  {'r=σc²/σ²':>10}{'高斯 Pr[X>r]':>16}{'Cantelli 上界':>16}{'形状税':>12}")
    rows_a = []
    for r in (1.5, 2.0, 3.0, 5.0, 10.0):
        # 高斯样本方差 n=10：X ~ chi2_10/10，Pr[X>r]
        pg = float(stats.chi2.sf(10 * r, 10))
        v = 2.0 / 10.0                      # Var(chi2_n/n) = 2/n
        cb = cantelli_upper(r, v)
        print(f"  {r:>10.2f}{pg:>16.3e}{cb:>16.3e}{cb/max(pg,1e-300):>12.2e}")
        rows_a.append(dict(r=r, gauss=pg, cantelli=cb, ratio=cb / pg))
    assert all(x["cantelli"] >= x["gauss"] for x in rows_a), "Cantelli 必须是上界"

    print("\n" + "=" * 78)
    print("B. 四种分布同 (μ,σ²)：样本方差分布与 p_pair")
    print("=" * 78)
    mu, sig = 0.30, 0.05
    ncell = 10
    print(f"  μ={mu}, σ={sig}, n_cell={ncell}")
    print(f"  {'分布':<10}{'偏度':>9}{'峰度':>9}{'r=1.5':>12}{'r=2.0':>12}{'r=3.0':>12}")
    dists = {}
    # 高斯
    dists["高斯"] = stats.norm(mu, sig)
    # Gamma（同均值方差）
    k = mu ** 2 / sig ** 2
    th = sig ** 2 / mu
    dists["Gamma"] = stats.gamma(k, scale=th)
    # 对数正态（同均值方差）
    s2 = math.log(1 + sig ** 2 / mu ** 2)
    dists["对数正态"] = stats.lognorm(s=math.sqrt(s2), scale=mu / math.sqrt(1 + sig ** 2 / mu ** 2))
    # Beta on [0,1] 缩放到 [0, 2π]
    twopi = 2 * math.pi
    mm, vv = mu / twopi, (sig / twopi) ** 2
    kk = mm * (1 - mm) / vv - 1
    dists["Beta"] = stats.beta(mm * kk, (1 - mm) * kk, scale=twopi)

    res_b = []
    for name, d in dists.items():
        # 用蒙特卡洛算样本方差超过阈值的概率（n_cell 个独立样本）
        rng = np.random.default_rng(42)
        xs = d.rvs(size=2000000, random_state=rng)
        xs = xs.reshape(200000, ncell)
        s2s = xs.var(axis=1, ddof=1)
        sk = float(d.stats("s"))
        ku = float(d.stats("k"))
        ps = []
        for r in (1.5, 2.0, 3.0):
            ps.append(float((s2s > r * sig ** 2).mean()))
        print(f"  {name:<10}{sk:>9.3f}{ku:>9.3f}{ps[0]:>12.4e}{ps[1]:>12.4e}{ps[2]:>12.4e}")
        res_b.append(dict(name=name, skew=sk, kurt=ku, p15=ps[0], p20=ps[1], p30=ps[2]))

    # 形状依赖的离散度（对 r=2.0）
    ps20 = [x["p20"] for x in res_b]
    spread = (max(ps20) - min(ps20)) / (sum(ps20) / len(ps20))
    print(f"\n  r=2.0 时四种分布的 p_pair 相对离散：{spread*100:.1f}%")
    print("  （高斯是 chi-square 基准；Gamma 与它同族，故最接近；对数正态偏度大，偏离最大）")

    print("\n" + "=" * 78)
    print("C. Edgeworth：p 对偏度的一阶修正")
    print("=" * 78)
    print("  δp = -(γ₁/6)(z²-1)φ(z)，z=Φ⁻¹(1-p)")
    print(f"  {'p':>8}{'z':>9}{'(z²-1)φ(z)':>14}{'每单位偏度的 δp':>18}")
    rows_c = []
    for p in (0.592746, 0.9, 0.5, 0.3, 0.1, 0.05, 0.01):
        z = stats.norm.ppf(1 - p)
        sens = -(z ** 2 - 1) * stats.norm.pdf(z) / 6
        print(f"  {p:>8.4f}{z:>9.4f}{(z**2-1)*stats.norm.pdf(z):>14.4f}{sens:>18.4f}")
        rows_c.append(dict(p=p, z=z, sens=sens))

    # 达到 p_c 的 1% 精度所需的偏度精度
    pc = 0.592746
    zc = stats.norm.ppf(1 - pc)
    sens_c = abs(-(zc ** 2 - 1) * stats.norm.pdf(zc) / 6)
    need = 0.01 * pc / sens_c
    print(f"\n  在 p_c={pc} 处：每单位偏度改变 p 的 {sens_c:.4f}")
    print(f"  要使 p 的误差 ≤1%（即 {0.01*pc:.4f}），需 |γ₁| 精确到 {need:.3f}")
    print(f"  实测偏度：Gamma {res_b[1]['skew']:.3f}、对数正态 {res_b[2]['skew']:.3f}、"
          f"Beta {res_b[3]['skew']:.3f}")
    print("  （Edgeworth 是**右尾** z>0 的展开；p_c 处 z<0，需看 D 段的反解）")


    print("\n" + "=" * 78)
    print("D. 反解：固定 p_c=0.592746，四种分布要求的阈值 r=σ_c²/σ²")
    print("=" * 78)
    print(f"  {'分布':<10}{'r(p=p_c)':>12}{'相对高斯':>12}{'σ_c 相对位移':>14}")
    rs = {}
    for name, d in dists.items():
        rng = np.random.default_rng(7)
        xs = d.rvs(size=2000000, random_state=rng).reshape(200000, ncell)
        s2s = np.sort(xs.var(axis=1, ddof=1)) / sig ** 2
        # r 使 Pr[s2>r σ²] = p_c
        idx = int((1 - 0.592746) * len(s2s))
        rs[name] = float(s2s[idx])
    base = rs["高斯"]
    for name, r in rs.items():
        print(f"  {name:<10}{r:>12.4f}{r/base:>12.4f}{(math.sqrt(r/base)-1)*100:>13.1f}%")
    shift = max(abs(math.sqrt(r / base) - 1) for r in rs.values())
    print(f"\n  最大 σ_c 相对位移 {shift*100:.1f}%")
    print("  注意：p_c 处 r≈0.82<1，是**左尾**；而 B 段的 28% 离散在 r=2（右尾）。")
    print("  ⇒ 阈值处形状敏感度被压到 ~1.5%，与 1% 精度同量级 ⇒ **边缘**，非决定性。")
    assert shift < 0.02

    # ---------------------------------------------------------------- 图
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2))

    ax = axes[0, 0]
    xs = np.linspace(mu - 4 * sig, mu + 4 * sig, 500)
    for name, d in dists.items():
        ax.plot(xs, d.pdf(xs), "-", lw=1.6, label=f"{name}（$\\gamma_1$={float(d.stats('s')):.2f}）")
    ax.set_xlabel(r"$\varepsilon$")
    ax.set_ylabel("概率密度")
    ax.set_title("A. 同均值同方差的四种分布")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[0, 1]
    rr = np.linspace(1.05, 5, 120)
    ax.semilogy(rr, stats.chi2.sf(ncell * rr, ncell), "-", label="高斯（$\\chi^2_{10}$）")
    ax.semilogy(rr, [cantelli_upper(r, 2.0 / ncell) for r in rr], "--", color="k",
                label="Cantelli 上界（无分布假设）")
    ax.set_xlabel(r"$r=\sigma_c^2/\sigma^2$")
    ax.set_ylabel(r"$p_{\rm pair}$")
    ax.set_title("B. 分布无关的上界与高斯尾")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3, which="both")

    ax = axes[1, 0]
    names = list(rs.keys())
    rel = [(math.sqrt(rs[n] / base) - 1) * 100 for n in names]
    ax.bar(names, rel, color=["#4C72B0", "#DD8452", "#55A868", "#C44E52"], alpha=.8)
    ax.axhline(0, color="k", lw=.6)
    ax.set_ylabel(r"$\sigma_c$ 相对高斯的位移 (%)")
    ax.set_title("C. 固定 $p_c=0.593$ 时的阈值位移")
    ax.grid(alpha=.3, axis="y")

    ax = axes[1, 1]
    zs = np.linspace(-3, 3, 300)
    ax.plot(zs, -(zs ** 2 - 1) * stats.norm.pdf(zs) / 6, "-",
            label=r"$-(z^2-1)\phi(z)/6$（每单位 $\gamma_1$）")
    ax.axvline(zc, color="r", ls=":", label=rf"$z_c$(p_c)={zc:.3f}")
    ax.axhline(0, color="k", lw=.6)
    ax.set_xlabel("$z$")
    ax.set_ylabel(r"$\partial p/\partial\gamma_1$")
    ax.set_title("D. 偏度对 $p$ 的灵敏度")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    fig.tight_layout()
    png = os.path.join(OUT, "环15_pair概率的形状依赖.png")
    fig.savefig(png, dpi=150)
    print(f"\n图：{png}")

    csvp = os.path.join(OUT, "环15_pair概率的形状依赖.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["分布", "偏度", "峰度", "p(r=1.5)", "p(r=2.0)", "p(r=3.0)"])
        for r in res_b:
            w.writerow([r["name"], f"{r['skew']:.4f}", f"{r['kurt']:.4f}",
                        f"{r['p15']:.4e}", f"{r['p20']:.4e}", f"{r['p30']:.4e}"])
    print(f"表：{csvp}")

    sump = os.path.join(OUT, "环15_pair概率的形状依赖_摘要.csv")
    with open(sump, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["项目", "数值", "判据"])
        w.writerow(["p_pair 相对离散（r=2）", f"{spread*100:.1f}%", ">10% ⇒ 需分布族"])
        w.writerow(["p_c 处 ∂p/∂γ1", f"{sens_c:.4f}", "每单位偏度"])
        w.writerow(["1% 精度所需 γ1 容差", f"{need:.3f}", "实测偏度远超"])
        w.writerow(["固定 p_c 的 σ_c 最大位移", f"{shift*100:.1f}%", "<2% ⇒ 边缘，非决定性"])
    print(f"摘要：{sump}")
    print("\n全部断言通过。")


if __name__ == "__main__":
    main()
