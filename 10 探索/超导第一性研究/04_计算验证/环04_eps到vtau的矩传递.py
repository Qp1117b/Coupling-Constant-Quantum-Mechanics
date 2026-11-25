# -*- coding: utf-8 -*-
r"""
第 139 轮：环 4→5→9 的接口——$\varepsilon$ 的矩到 $v_\tau$ 的矩，链路对载体细节的鲁棒性
=======================================================================================
前件：R147 判 $\varepsilon$ 的统计归 FG／材料（链内无载体）。于是链只能通过
      $(\bar\varepsilon,\ \sigma^2=\mathrm{Var}\,\varepsilon)$ 与空间关联 $\rho$ 见到 $\varepsilon$。

本轮给出（纯代数，无拟合、无载体细节）：

  (5.1) 是 $v_\tau=\sqrt{1-\varepsilon/2\pi}$。用有理化恒等式
      $$\sqrt a-\sqrt b=\frac{a-b}{\sqrt a+\sqrt b}$$
  得**精确**的一阶传递：
      $$v_\tau(\varepsilon_0+\delta)-v_\tau(\varepsilon_0)
        =-\frac{\delta/2\pi}{v_\tau(\varepsilon_0+\delta)+v_\tau(\varepsilon_0)}$$
  故 $v_\tau'(\varepsilon_0)=-1/(4\pi v_0)$ 精确（不是近似），二阶项由分母的变化给。

  由此：
    * $\mathrm{Var}(v_\tau)=\kappa_f^2v_0^2\,\sigma^2+O(\sigma^4)$，
      $\kappa_f=-\partial_\varepsilon\ln v_\tau=1/(4\pi v_0^2)$（与 R-… 审-2 的式子一致）；
    * $\mathrm{Var}(\lambda_{ij})=\mathrm{Var}(\ln v_{\tau,j}-\ln v_{\tau,i})
      =2\kappa_f^2\sigma^2(1-\rho)\ \Rightarrow$ 正是环 9 的 (9.1)；
    * **Jensen**：$\langle v_\tau\rangle\le v_0$，涨落使平均钟速变慢，
      减慢量 $\approx \sigma^2/(32\pi^2v_0^3)$。

  最后检验下游对分布形状的依赖：用三种分布（截断高斯、均匀、Beta）在相同
  $(\bar\varepsilon,\sigma^2)$ 下算 $\langle v_\tau\rangle$ 与 $\mathrm{Var}(v_\tau)$，
  看二阶公式是否与形状无关。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_eps到vtau的矩传递.py"
"""
import csv
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
TWOPI = 2 * math.pi


def vtau(eps):
    return np.sqrt(np.clip(1.0 - eps / TWOPI, 1e-12, None))


def _pdf(kind, m, s):
    """返回密度函数 p(ε)，用于高精度数值积分（去掉抽样噪声）。"""
    if kind == "truncnorm":
        norm = s * math.sqrt(2 * math.pi)
        return lambda x: math.exp(-0.5 * ((x - m) / s) ** 2) / norm
    if kind == "uniform":
        w = math.sqrt(3.0) * s
        return lambda x: (1.0 / (2 * w)) if abs(x - m) <= w else 0.0
    if kind == "beta":
        from scipy.stats import beta as beta_dist
        mu = m / TWOPI
        var = (s / TWOPI) ** 2
        k = mu * (1 - mu) / var - 1
        a, b = mu * k, (1 - mu) * k
        return lambda x: beta_dist.pdf(x / TWOPI, a, b) / TWOPI
    raise ValueError(kind)


def moments_exact(kind, m, s):
    """⟨v⟩、Var(v) 用求积算（无抽样噪声；区间限制 + 重归一化 + 峰点）。"""
    from scipy.integrate import quad
    p = _pdf(kind, m, s)
    if kind == "uniform":
        w = math.sqrt(3.0) * s
        lo, hi = max(1e-12, m - w), min(TWOPI - 1e-12, m + w)
    else:
        lo, hi = max(1e-12, m - 10 * s), min(TWOPI - 1e-12, m + 10 * s)
    kw = dict(limit=500)
    if lo < m < hi:
        kw["points"] = [m]
    Z, _ = quad(p, lo, hi, **kw)
    m1, _ = quad(lambda x: vtau(np.array([x]))[0] * p(x), lo, hi, **kw)
    m2, _ = quad(lambda x: vtau(np.array([x]))[0] ** 2 * p(x), lo, hi, **kw)
    mu = m1 / Z
    return float(mu), float(m2 / Z - mu ** 2)


def main():
    print("=" * 78)
    print("A. 精确的一阶传递：有理化恒等式")
    print("=" * 78)
    eps0 = 0.30
    v0 = math.sqrt(1 - eps0 / TWOPI)
    kappa = 1.0 / (4 * math.pi * v0 ** 2)
    print(f"  取 ε0={eps0:.2f}, v0={v0:.6f}, κ_f=1/(4πv0²)={kappa:.6f}")
    print(f"  {'δ':>10}{'精确Δv':>16}{'一阶 -δκ_f v0':>18}{'相对偏差':>12}")
    rows = []
    for d in (1e-3, 1e-2, 5e-2, 1e-1, 2e-1):
        de = vtau(np.array([eps0 + d]))[0] - v0
        lin = -d * kappa * v0
        rel = abs(de - lin) / abs(de)
        print(f"  {d:>10.4f}{de:>16.8e}{lin:>18.8e}{rel:>12.3e}")
        rows.append(dict(delta=d, exact=de, lin=lin, rel=rel))
    # 断言：小 δ 下一阶精确
    assert rows[0]["rel"] < 1e-3

    print("\n" + "=" * 78)
    print("B. 二阶公式与三种分布（同均值同方差，不同形状）")
    print("=" * 78)
    m0 = 0.30
    v0 = math.sqrt(1 - m0 / TWOPI)
    print(f"  ε0={m0}, v0={v0:.6f}")
    print(f"  {'分布':<12}{'σ':>7}{'⟨v⟩数值':>14}{'二阶 v0-σ²/(32π²v0³)':>22}"
          f"{'偏差':>11}{'Var(v)数值':>14}{'κ²v0²σ²':>13}{'偏差':>11}")
    res = []
    for kind in ("truncnorm", "uniform", "beta"):
        for s in (0.02, 0.05, 0.10):
            mean_v, var_v = moments_exact(kind, m0, s)
            second = v0 - s ** 2 / (32 * math.pi ** 2 * v0 ** 3)
            var_pred = kappa ** 2 * v0 ** 2 * s ** 2
            res.append(dict(kind=kind, sigma=s, mean=mean_v, mean_pred=second,
                            var=var_v, var_pred=var_pred))
            print(f"  {kind:<12}{s:>7.3f}{mean_v:>14.7f}{second:>22.7f}"
                  f"{abs(mean_v-second):>11.2e}{var_v:>14.3e}{var_pred:>13.3e}"
                  f"{abs(var_v-var_pred)/var_pred:>11.2e}")

    # 鲁棒性判据：同 σ 下，三种分布的 Var(v) 的相对差
    print("\n  同 σ 下三种分布的 Var(v) 相对离散（判是否形状无关）：")
    for s in (0.02, 0.05, 0.10):
        vs = [r["var"] for r in res if abs(r["sigma"] - s) < 1e-9]
        spread = (max(vs) - min(vs)) / np.mean(vs)
        print(f"    σ={s:.2f}: 离散 {spread*100:.2f}%")
    assert max(abs(r["var"] - r["var_pred"]) / r["var_pred"] for r in res) < 0.15

    print("\n" + "=" * 78)
    print("C. Jensen：涨落使平均钟速变慢")
    print("=" * 78)
    print(f"  {'σ':>8}{'⟨v⟩':>14}{'v0':>14}{'减慢量':>14}{'σ²/(32π²v0³)':>16}")
    jen = []
    for s in (0.005, 0.01, 0.02, 0.035, 0.05, 0.10, 0.20):
        mean_v, _ = moments_exact("truncnorm", m0, s)
        pred = s ** 2 / (32 * math.pi ** 2 * v0 ** 3)
        jen.append(dict(sigma=s, mean=mean_v, slow=v0 - mean_v, pred=pred))
        print(f"  {s:>8.3f}{mean_v:>14.7f}{v0:>14.7f}{v0-mean_v:>14.3e}{pred:>16.3e}")
    # 断言：减慢量随 σ 严格增；σ≤0.05 时二阶公式误差 <2%
    assert all(jen[i]["slow"] < jen[i + 1]["slow"] for i in range(len(jen) - 1))
    small = [j for j in jen if j["sigma"] <= 0.05]
    worst = max(abs(j["slow"] / j["pred"] - 1) for j in small)
    print(f"\n  σ≤0.05 时二阶公式的最大相对偏差：{worst*100:.2f}%")
    assert worst < 0.02

    # ---------------------------------------------------------------- 图
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2))

    ax = axes[0, 0]
    e = np.linspace(0, 2 * math.pi * 0.98, 400)
    ax.plot(e, vtau(e), "-", color="#4C72B0", label=r"$v_\tau=\sqrt{1-\varepsilon/2\pi}$")
    ax.plot([m0], [v0], "o", color="k", ms=5)
    ee = np.array([m0 - 0.6, m0 + 0.6])
    ax.plot(ee, vtau(ee), "s--", color="#C0504D", ms=4,
            label="割线（Jensen：弦在图像下方）")
    ax.plot([m0], [v0 - 0.05], "v", color="#55A868", ms=6, label=r"$\langle v_\tau\rangle$（减慢）")
    ax.set_xlim(0.10, 0.60)
    ax.set_ylim(0.960, 1.002)
    ax.set_xlabel(r"$\varepsilon$ (rad)，放大区")
    ax.set_ylabel(r"$v_\tau$")
    ax.set_title("A. 凹性：曲线在弦上方（Jensen）")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[0, 1]
    ss = np.logspace(-3, -0.3, 60)
    for kind, c, mk in (("truncnorm", "#4C72B0", "o"), ("uniform", "#DD8452", "s"),
                        ("beta", "#55A868", "^")):
        errs = []
        for s in ss:
            mv, _ = moments_exact(kind, m0, s)
            pred = v0 - s ** 2 / (32 * math.pi ** 2 * v0 ** 3)
            errs.append(abs(mv - pred) / v0)
        ax.loglog(ss, errs, mk, ms=3, alpha=.6, color=c, label=kind)
    ax.loglog(ss, (ss / v0) ** 4, "k--", lw=1, label=r"$\propto\sigma^4$")
    ax.set_xlabel(r"$\sigma_\varepsilon$ (rad)")
    ax.set_ylabel("二阶公式相对误差")
    ax.set_title("B. 误差：二阶项形状无关，三阶以上分道")
    ax.legend(fontsize=8)
    ax.grid(alpha=.3, which="both")

    ax = axes[1, 0]
    sg = np.array([j["sigma"] for j in jen])
    sl = np.array([j["slow"] for j in jen])
    ax.semilogx(sg, sl / sg ** 2, "o-", label="数值 $\\langle v_0-v_\\tau\\rangle/\\sigma^2$")
    ax.axhline(1 / (32 * math.pi ** 2 * v0 ** 3), color="k", ls="--",
               label=r"$1/(32\pi^2v_0^3)$（二阶）")
    ax.set_xlabel(r"$\sigma_\varepsilon$ (rad)")
    ax.set_ylabel(r"减慢量 $/\sigma^2$")
    ax.set_title("C. $\sigma\\to0$ 时减慢系数趋于常数")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3, which="both")

    ax = axes[1, 1]
    labels = [r"$\mathrm{Var}(v_\tau)$", r"$\mathrm{Var}(\lambda_{ij})$",
              "Jensen 位移（一阶）", "Jensen 位移（三阶修正）", r"环 15 尾概率"]
    kinds = [r"二阶矩", r"二阶矩", r"二阶矩", r"需 $\mu_3$", r"需分布族"]
    vals = [1.0, 1.0, 1.0, 0.0, 0.0]
    colors = ["#4C72B0", "#4C72B0", "#4C72B0", "#DD8452", "#C0504D"]
    ax.barh(labels, vals, color=colors, alpha=.75)
    for i, k in enumerate(kinds):
        ax.text(0.02, i, k, va="center", fontsize=9,
                color="white" if vals[i] > 0.5 else "black")
    ax.set_xlim(0, 1.15)
    ax.set_xticks([])
    ax.set_title("D. 下游对 $\\varepsilon$ 输入的依赖度")
    ax.grid(alpha=.3, axis="x")

    fig.tight_layout()
    png = os.path.join(OUT, "环04_eps到vtau的矩传递.png")
    fig.savefig(png, dpi=150)
    print(f"\n图：{png}")

    csvp = os.path.join(OUT, "环04_eps到vtau的矩传递.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["分布", "sigma", "⟨v⟩数值", "二阶预测", "偏差",
                    "Var(v)数值", "κ²v0²σ²", "相对偏差"])
        for r in res:
            w.writerow([r["kind"], r["sigma"], f"{r['mean']:.8f}",
                        f"{r['mean_pred']:.8f}", f"{abs(r['mean']-r['mean_pred']):.2e}",
                        f"{r['var']:.6e}", f"{r['var_pred']:.6e}",
                        f"{abs(r['var']-r['var_pred'])/r['var_pred']:.2e}"])
    print(f"表：{csvp}")

    sump = os.path.join(OUT, "环04_eps到vtau的矩传递_摘要.csv")
    with open(sump, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["项目", "数值", "判据"])
        w.writerow(["一阶传递偏差（δ=1e-3）", f"{rows[0]['rel']:.2e}", "<1e-3 ⇒ 一阶精确"])
        w.writerow(["Var(v) 二阶公式最大偏差",
                    f"{max(abs(r['var']-r['var_pred'])/r['var_pred'] for r in res):.2e}",
                    "<0.15 ⇒ 形状无关"])
        w.writerow(["Jensen 减慢（σ=0.2）", f"{jen[-1]['slow']:.3e}",
                    f"预测 {jen[-1]['pred']:.3e}"])
        w.writerow(["κ_f", f"{kappa:.6f}", "=1/(4πv0²)，环 9 用同一量"])
    print(f"摘要：{sump}")
    print("\n全部断言通过。")


if __name__ == "__main__":
    main()
