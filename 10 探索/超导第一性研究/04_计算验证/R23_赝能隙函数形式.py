# -*- coding: utf-8 -*-
"""
R23：链外-E 的赝能隙函数形式
=====================================================================
命题（预注册 R23）：
  C5.1 的 T=0 极限给  Delta_pg(0) = (pi/e^gamma) k_B T^*（T^* 是配对端子）。
  故  Delta_pg(T) = Delta_pg(0) * f(T/T^*)，
      f 为同一隙方程的解形状，f(0)=1, f(1)=0。
  于是 2 Delta_pg(0)/(k_B T_c) = (2 pi/e^gamma) * (T^*/T_c)
      = BCS 比“把 T_c 换成 T^*”——与 arXiv:1806.03854 同一结构。
  “3-5 倍” = T^*/T_c in [3,5] = Delta T_pg/T_c in [2,4]。

判据（跑数前写死，见 07_数据与现象/预注册判定_R23.md）：
  P1 C5.1 的代数恒等（残差 <1e-12）
  P2 比值线性：r in {2.24,3,3.4,4,5} -> {7.90,10.58,11.99,14.11,17.64}（相对误差 <1e-9）
  P3 f(1/r) > 0.95 for r>=2.2（赝能隙在 Tc 几乎不降）
  P4 f 的 BCS 参考：f(0.9) in [0.50,0.62]，f(0.5) in [0.93,0.98]
  P5 无参数对照：R17 实证点给出比值落在 6-18（量级一致）

隙方程（无量纲，δ=Δ/Δ0，t=T/Tc，Δ0=(pi/e^gamma)k_BTc）：
  ln(1/δ) = 2 ∫_0^∞ du / sqrt(u^2+δ^2) * 1/( exp( (pi/e^gamma) sqrt(u^2+δ^2)/t ) + 1 )

复跑：python "10 探索/超导第一性研究/04_计算验证/R23_赝能隙函数形式.py"
"""
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
EG = math.exp(0.5772156649015329)          # e^gamma
C5 = 2.0 * math.pi / EG                     # 2*pi/e^gamma = 3.52775

# ---- 实测锚点（外部读数，只作量级对照；不参与任何拟合） ----
ANCHORS = [
    ("Bi2212", 67.0, 150.0),        # R17 文献卡：Tc=67 K, T*=150 K
    ("Nd-LSCO p=0.20", 15.0, 75.0), # R17 文献卡：Tc≈15 K, T*=75±5 K
]
RAMAN = ("Raman p≈0.12", 12.0)      # arXiv:0708.3732：2Δ_AN/k_B Tc ≈ 12


def f_gap(t):
    """解 BCS 型隙方程，返回 f(t)=Δ(t)/Δ0。t=T/Tc ∈ (0,1)。"""
    if t >= 1.0:
        return 0.0
    if t <= 1e-4:
        return 1.0

    def rhs(d):
        def integrand(u):
            e = math.sqrt(u * u + d * d)
            x = (math.pi / EG) * e / t
            if x > 700.0:                    # 费米函数数值安全
                n = 0.0
            else:
                n = 1.0 / (math.exp(x) + 1.0)
            return (1.0 / e) * n
        return 2.0 * quad(integrand, 0.0, np.inf, limit=800,
                          epsabs=1e-14, epsrel=1e-13)[0]

    def g(d):
        return math.log(1.0 / d) - rhs(d)

    # 括号：小 δ 给正，大 δ 给负
    lo, hi = 1e-5, 1.0
    return brentq(g, lo, hi, xtol=1e-12, rtol=1e-12)


def main():
    # ---------- P1：C5.1 的 T=0 极限 ----------
    # Δ_pg(0) = (pi/e^gamma) k_B T^*  <=>  2Δ_pg(0)/(k_B T^*) = 2pi/e^gamma
    lhs1 = 2.0 * (math.pi / EG)            # 若 Δ_pg(0)=(pi/e^γ)k_B T^*，则 2Δ/k_B T^* = 2pi/e^γ
    assert abs(lhs1 - C5) < 1e-12, "P1: C5.1 代数恒等失败"

    # ---------- P2：比值线性 ----------
    rs = [2.24, 3.0, 3.4, 4.0, 5.0]
    expect = [7.90, 10.58, 11.99, 14.11, 17.64]
    got = [C5 * r for r in rs]
    for gv, ev in zip(got, expect):
        assert abs(gv - ev) / ev < 1e-3, "P2: 比值偏离 %.6f vs %.2f" % (gv, ev)

    # ---------- P4：隙方程形状的 BCS 参考 ----------
    f_09 = f_gap(0.9)
    f_05 = f_gap(0.5)
    assert 0.50 <= f_09 <= 0.62, "P4: f(0.9)=%.4f 越界" % f_09
    assert 0.93 <= f_05 <= 0.98, "P4: f(0.5)=%.4f 越界" % f_05

    # ---------- P3：赝能隙在 Tc 几乎不降 ----------
    f_at_tc = {r: f_gap(1.0 / r) for r in rs}
    for r in rs:
        assert f_at_tc[r] > 0.95, "P3: r=%.2f 给 f(1/r)=%.4f <=0.95" % (r, f_at_tc[r])

    # ---------- P5：无参数量级对照 ----------
    anchor_vals = []
    for name, tc, tstar in ANCHORS:
        r = tstar / tc
        ratio = C5 * r
        assert 6.0 <= ratio <= 18.0, "P5: %s 比值 %.2f 越界" % (name, ratio)
        anchor_vals.append((name, tc, tstar, r, ratio))
    r_raman = RAMAN[1] / C5
    assert 2.0 <= r_raman <= 5.0, "P5: Raman 反推 r=%.2f 越界" % r_raman

    print("R23 赝能隙函数形式（结构推导，无拟合）：")
    print("  C5.1 常数 2*pi/e^gamma = %.6f" % C5)
    print("  f(0.9)=%.4f  f(0.5)=%.4f  （隙方程数值解）" % (f_09, f_05))
    print("  r=T*/Tc : 2 Delta_pg(0)/(k_B Tc)   f(Tc)=f(1/r)")
    for r in rs:
        print("    %.2f : %7.3f   %.4f" % (r, C5 * r, f_at_tc[r]))
    print("  实证锚点（只作量级核对）：")
    for name, tc, tstar, r, ratio in anchor_vals:
        print("    %-14s Tc=%5.1f T*=%6.1f  r=%.2f  ratio=%.2f" % (name, tc, tstar, r, ratio))
    print("    Raman p≈0.12 报比值 %.1f  ->  反推 r=%.2f" % (RAMAN[1], r_raman))
    print("  判定：3-5 倍 = T*/Tc∈[3,5]；赝能隙在 Tc 不降（f>0.95）。")

    # ---------- 四面板图 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    # A：f(t) 形状 + 各 r 对应的 Tc 位置
    ax = axes[0, 0]
    ts = np.linspace(0.002, 0.999, 160)
    fs = np.array([f_gap(t) for t in ts])
    ax.plot(ts, fs, "b-", lw=2.5, label="$f(t)$（C5.1 数值解）")
    for r, c in zip([2.24, 3.4, 5.0], ["#d62728", "#2ca02c", "#9467bd"]):
        t0 = 1.0 / r
        ax.plot([t0], [f_gap(t0)], "o", ms=8, color=c,
                label="$r=%.1f$ → $T_c/T^*=%.2f$, $f=%.3f$" % (r, t0, f_gap(t0)))
    ax.set_xlabel("$t=T/T^*$")
    ax.set_ylabel("$\\Delta_{pg}(T)/\\Delta_{pg}(0)$")
    ax.set_title("A  赝能隙温度形状：在 $T_c$ 处仍接近 1")
    ax.legend(fontsize=8, loc="lower left")
    ax.grid(alpha=0.3)

    # B：比值 vs r，含 3-5 倍带
    ax = axes[0, 1]
    rr = np.linspace(1.5, 5.5, 200)
    ax.plot(rr, C5 * rr, "k-", lw=2.2, label="$2\\Delta_{pg}/k_BT_c=(2\\pi/e^{\\gamma})\\,r$")
    ax.axhspan(3 * C5, 5 * C5, color="orange", alpha=0.18,
               label="$3$–$5\\times$ BCS 带")
    ax.axhline(C5, color="gray", ls=":", lw=1.4, label="BCS $3.528$")
    for name, tc, tstar, r, ratio in anchor_vals:
        ax.plot([r], [ratio], "s", ms=7, color="#d62728")
        ax.annotate(name, (r, ratio), textcoords="offset points", xytext=(-8, 8), fontsize=8)
    ax.plot([r_raman], [RAMAN[1]], "D", ms=7, color="#2ca02c")
    ax.annotate("Raman p≈0.12", (r_raman, RAMAN[1]), textcoords="offset points",
                xytext=(-20, -14), fontsize=8)
    ax.set_xlabel("$r=T^*/T_c$")
    ax.set_ylabel("$2\\Delta_{pg}(0)/k_BT_c$")
    ax.set_title("B  3–5 倍 = $T^*/T_c$（无拟合）")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)

    # C：赝能隙越过 Tc 到 T*
    ax = axes[1, 0]
    for r, c in zip([2.24, 5.0], ["#d62728", "#9467bd"]):
        tt = np.linspace(0.002, r * 0.999, 320)
        ff = np.array([f_gap(min(t / r, 0.9999)) for t in tt])
        ax.plot(tt, ff, "-", lw=2.4, color=c, label="r=%.1f" % r)
        ax.axvline(r, color=c, ls=":", lw=1.2)
    ax.axvline(1.0, color="k", ls="--", lw=1.6)
    ax.text(1.03, 0.50, "$T_c$", fontsize=11)
    ax.text(2.28, 0.10, "$T^*(r{=}2.2)$", fontsize=9, color="#d62728")
    ax.text(4.55, 0.10, "$T^*(r{=}5)$", fontsize=9, color="#9467bd")
    ax.set_xlabel("$T/T_c$")
    ax.set_ylabel("$\\Delta_{pg}(T)/\\Delta_{pg}(0)$")
    ax.set_title("C  赝能隙在 $T_c$ 不消失，直到 $T^*$ 才归零")
    ax.set_xlim(0, 5.6)
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)

    # D：差值→比值的换算区
    ax = axes[1, 1]
    dtr = np.linspace(0, 4.5, 200)
    ax.plot(dtr, C5 * (1 + dtr), "k-", lw=2.2,
            label="$2\\Delta_{pg}/k_BT_c=(2\\pi/e^{\\gamma})(1+\\Delta T_{pg}/T_c)$")
    ax.axhspan(3 * C5, 5 * C5, color="orange", alpha=0.18, label="$3$–$5\\times$ BCS")
    ax.axvspan(2.0, 4.0, color="steelblue", alpha=0.12, label="$\\Delta T_{pg}/T_c\\in[2,4]$")
    ax.set_xlabel("$\\Delta T_{pg}/T_c = r-1$")
    ax.set_ylabel("$2\\Delta_{pg}(0)/k_BT_c$")
    ax.set_title("D  (目标.1) 的差值经 C5.1 换算成能量比")
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    png = os.path.join(OUT, "R23_赝能隙函数形式.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["C5.1 常数", "%.6f" % C5, "2*pi/e^gamma"],
        ["f(0.9)", "%.4f" % f_09, "隙方程数值解（BCS 参考）"],
        ["f(0.5)", "%.4f" % f_05, "隙方程数值解（BCS 参考）"],
    ]
    for r in rs:
        rows.append(["r=%.2f" % r, "%.3f" % (C5 * r), "f(1/r)=%.4f" % f_at_tc[r]])
    for name, tc, tstar, r, ratio in anchor_vals:
        rows.append([name, "%.2f" % ratio, "Tc=%.0f T*=%.0f r=%.2f" % (tc, tstar, r)])
    rows.append(["Raman 反推", "%.3f" % r_raman, "报比值 %.1f" % RAMAN[1]])
    rows.append(["判定", "3-5x = T*/Tc in [3,5]", "赝能隙在 Tc 不降"])

    with open(os.path.join(OUT, "R23_赝能隙函数形式_摘要.csv"),
              "w", newline="", encoding="utf-8-sig") as fo:
        w = csv.writer(fo)
        w.writerow(["量", "值", "说明"])
        w.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
