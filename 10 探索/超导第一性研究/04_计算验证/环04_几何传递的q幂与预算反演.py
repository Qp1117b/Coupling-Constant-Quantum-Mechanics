# -*- coding: utf-8 -*-
"""
R74：几何传递的 q-幂 = 2（不是 1）——R71 的 |G_q|^2∝q^2 订正为 q^4，并反演振幅预算
================================================================================
第 74 轮。三件事：
  (1) 内禀平面波扰动 -> 亏角：拟合 eps(q)/eta 的 q-幂，三个方向；
      理论预期 2（均匀模被平直性杀死 => A(0)=0；中心对称 => A 偶 => 首项 q^2）。
  (2) 由此 |G_q|^2 = c^2 q^4，sigma_eps = 0.775 c a Q eta（白噪声约定，显式），
      把 R71 的 sigma ~ c_eps*(lq/a)^2 换成"单一未知 eta"。
  (3) 反演振幅预算：形变势窗口 g in [1,30] eV 对应 eta 的允许窗口。

只用链内量与外部标准工具；不拟合（指数是推出来的，数值只作核验）。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_几何传递的q幂与预算反演.py"
"""
import csv
import itertools
import math
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))

# 复用 R73 的几何工具（只取函数，不跑 main）
_src = open(os.path.join(OUT, "环04_亏角对位移不变性与内禀传递.py"), encoding="utf-8").read()
exec(_src.split("def main()")[0])

HBAR = 1.054571817e-34
KB = 1.380649e-23
EV = 1.602176634e-19


def main():
    P, tets, edges = bcc_complex(4)
    allE = sorted({tuple(sorted((t[a], t[b]))) for t in tets for (a, b) in PAIRS})
    mid = {e: (P[e[0]] + P[e[1]]) / 2.0 for e in allE}
    eta = 1e-4
    qs_small = [0.02, 0.02 * 2.5, 0.1]        # 0.02, 0.05, 0.1：小 q（避开格点色散）
    qs_all = [0.02, 0.05, 0.1, 0.2, 0.4]

    print("=== 1. q-幂（内禀平面波 -> 亏角）===")
    slopes, coeffs = {}, {}
    for name, qd in (("[100]", [1, 0, 0]), ("[110]", [1, 1, 0]), ("[111]", [1, 1, 1])):
        qh = np.array(qd, float); qh /= np.linalg.norm(qh)
        vals = []
        for q in qs_all:
            sc = {e: 1.0 + eta * math.cos(q * float(np.dot(qh, mid[e]))) for e in allE}
            eps = np.array([hinge_eps_scaled(P, tets, e, sc) for e in edges])
            vals.append(float(np.sqrt((eps ** 2).mean()) / eta))
        sl = float(np.polyfit(np.log(qs_small), np.log(vals[:3]), 1)[0])
        c = vals[0] / qs_all[0] ** 2        # eps = c q^2 (delta l / l=eta)
        slopes[name], coeffs[name] = sl, c
        print("  q∥%-5s rms(eps)/eta = %s  slope(q<=0.1) = %.4f  c/a = %.4f"
              % (name, ["%.3e" % v for v in vals], sl, c))
    assert max(abs(v - 2.0) for v in slopes.values()) < 0.05, slopes
    c_rms = float(np.mean(list(coeffs.values())))
    print("  → 指数 2.00（三方向），c_rms/a = %.4f" % c_rms)
    print("  理由：均匀缩放给 0（R73 的 C 面板）⇒ A(0)=0；中心对称 ⇒ A 偶 ⇒ 首项 q^2")

    print("\n=== 2. sigma_eps 与 eta（白噪声约定）===")
    Qa = (6 * math.pi ** 2) ** (1.0 / 3.0)     # Q a
    coef = 0.775 * c_rms * Qa                  # sigma_eps = coef * eta
    print("  Qa = %.4f，sigma_eps = %.4f * eta" % (Qa, coef))
    for et in (1e-3, 1e-2, 3.7e-2, 0.1):
        print("    eta=%.1e -> sigma_eps=%.4f" % (et, coef * et))

    # ------------------------------------------------------------------
    # 3. 反演振幅预算（材料数据同 R71）
    # ------------------------------------------------------------------
    MAT = [
        ("Al", 428.0, 0.43, 1.35),
        ("Nb", 275.0, 0.95, 7.80),
        ("V", 380.0, 0.80, 9.30),
        ("Ta", 240.0, 0.65, 5.90),
        ("Pb", 105.0, 1.55, 3.00),
    ]
    ONE_MINUS_RHO = 0.9
    etas = np.logspace(-4, -0.5, 60)
    gcurves = {}
    for nm, thD, lam, gam in MAT:
        hw = KB * thD / EV
        N0 = gam / 2.355
        sig = coef * etas
        g = np.sqrt(lam * hw / (4 * N0 * sig ** 2 * ONE_MINUS_RHO))
        gcurves[nm] = g
    # 允许窗口：所有材料都落在 1–30 eV
    ok = np.ones_like(etas, dtype=bool)
    for nm in gcurves:
        ok &= (gcurves[nm] > 1.0) & (gcurves[nm] < 30.0)
    eta_lo, eta_hi = float(etas[ok].min()), float(etas[ok].max())
    print("\n=== 3. 预算反演：g∈[1,30] eV ⇒ eta ∈ [%.2e, %.2e] ===" % (eta_lo, eta_hi))
    for nm in gcurves:
        print("  %-3s g(eta=3.7e-2) = %.2f eV" % (nm, np.interp(3.7e-2, etas, gcurves[nm])))
    assert eta_lo < 3.7e-2 < eta_hi

    # ------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.2))

    ax = axes[0]
    qh = np.array([1.0, 0, 0])
    vals = []
    for q in qs_all:
        sc = {e: 1.0 + eta * math.cos(q * float(np.dot(qh, mid[e]))) for e in allE}
        eps = np.array([hinge_eps_scaled(P, tets, e, sc) for e in edges])
        vals.append(float(np.sqrt((eps ** 2).mean()) / eta))
    ax.loglog(qs_all, vals, "o-", label=r"$q\parallel[100]$")
    qq = np.logspace(-2, -0.3, 50)
    ax.loglog(qq, c_rms * qq ** 2, "k--", lw=1, label=r"$c\,q^2$，$c=%.3f$" % c_rms)
    ax.loglog(qq, c_rms * qq ** 2 / (qq[-1] / qs_all[0]), ":", lw=0)
    ax.set_xlabel(r"$qa$")
    ax.set_ylabel(r"$\mathrm{rms}(\varepsilon)/\eta$")
    ax.set_title("几何传递的 q-幂 = 2（不是 1）")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3, which="both")

    ax = axes[1]
    ax.loglog(etas, coef * etas, lw=2)
    ax.axhline(0.1, color="r", ls="--", lw=1, label="线性响应上界 $\\sigma_\\varepsilon<0.1$")
    ax.axvline(3.7e-2, color="gray", ls=":", lw=1, label=r"$\eta=3.7\%$（R71 的 $c_\varepsilon=0.5$）")
    ax.set_xlabel(r"内禀长度噪声 $\eta$")
    ax.set_ylabel(r"$\sigma_\varepsilon$")
    ax.set_title(r"$\sigma_\varepsilon=%.2f\,\eta$" % coef)
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.3, which="both")

    ax = axes[2]
    for nm in gcurves:
        ax.loglog(etas, gcurves[nm], lw=1.6, label=nm)
    ax.axhspan(1.0, 30.0, color="orange", alpha=0.18, label="形变势 1–30 eV")
    ax.axvspan(eta_lo, eta_hi, color="green", alpha=0.10, label=r"$\eta\in[%.1e,%.1e]$" % (eta_lo, eta_hi))
    ax.set_xlabel(r"$\eta$")
    ax.set_ylabel(r"反解 $g$ (eV)")
    ax.set_title("振幅预算反演：唯一未知是 $\\eta$")
    ax.legend(frameon=False, fontsize=7)
    ax.grid(alpha=0.3, which="both")

    fig.tight_layout()
    png = os.path.join(OUT, "环04_几何传递的q幂.png")
    fig.savefig(png, dpi=150)
    plt.close(fig)

    csv_path = os.path.join(OUT, "环04_几何传递的q幂.csv")
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["量", "值", "说明"])
        for nm in slopes:
            w.writerow(["斜率 " + nm, "%.4f" % slopes[nm], "小 q 拟合，S=2（推导值）"])
        w.writerow(["c_rms/a", "%.4f" % c_rms, "eps = c q^2 (delta l/l)"])
        w.writerow(["Qa", "%.4f" % Qa, "(6 pi^2)^{1/3}"])
        w.writerow(["sigma/eta", "%.4f" % coef, "白噪声约定"])
        w.writerow(["eta 窗口下", "%.2e" % eta_lo, "g=30 eV"])
        w.writerow(["eta 窗口上", "%.2e" % eta_hi, "g=1 eV"])
    print("\n图：", os.path.basename(png))
    print("表：", os.path.basename(csv_path))


if __name__ == "__main__":
    main()
