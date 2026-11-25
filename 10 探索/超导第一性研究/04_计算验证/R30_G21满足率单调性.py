# -*- coding: utf-8 -*-
"""
R30：G21 满足率 q(T) 的链内定义与单调性
=====================================================================
预注册 R30 的 P1–P5（跑数前写死）：
  P1 (6G.8) 前件审计
  P2 F(eps,T) 随 T 严格减 ⇒ S(T2)⊆S(T1) ⇒ q 非增
  P3 全域 w(T)（非低温展开）
  P4 两分量谱归一；q(Tc)>q(T*)
  P5 Lean 单调性与子集

复跑：python "10 探索/超导第一性研究/04_计算验证/R30_G21满足率单调性.py"
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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
wD, Tc, Tstar, pc = 300.0, 83.0, 200.0, 0.592746


def w_full(T):
    x = T / wD
    if x <= 0:
        return 1.0
    return 2.0 * quad(lambda y: y * math.tanh(y / (2.0 * x)), 0.0, 1.0,
                      epsabs=1e-13, epsrel=1e-13)[0]


def main():
    # ---------- P1：前件审计 ----------
    card = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "03_推导工作台",
                             "环06_G19容差标定.md"), encoding="utf-8").read()
    assert "J_0\\,A(\\varepsilon)\\,w(T)\\,\\cos" in card, "P1: (6G.8) 缺失"
    assert "非相干" in card, "P1: 热项方向缺失"

    # ---------- P3：全域 w(T) ----------
    Ts = np.linspace(5.0, 260.0, 300)
    ws = np.array([w_full(t) for t in Ts])
    assert np.all(np.diff(ws) < 0), "P3: w 应严格减"
    wc = w_full(Tc)
    assert 0 < wc < 1, "P3: 0<w(Tc)<1"

    # ---------- P2：F(eps,T) 单调 + q 非增 ----------
    # 示意参数（B 类）：A(eps)=1+eps/(2pi)，Lambda=N*eps，s=1/2，J0 定标
    eps = np.linspace(0.0, 2 * math.pi, 1200)
    N, s = 2.0, 0.5
    Aeps = 1.0 + eps / (2 * math.pi)
    cosL = np.cos(s * N * eps)
    J0 = 160.0
    k = 2.0 / math.pi

    def satisfy(T):
        F = J0 * Aeps * w_full(T) * cosL - k * T
        return F >= 0.0

    qs = np.array([satisfy(t).mean() for t in Ts])
    assert np.all(np.diff(qs) <= 1e-12), "P2: q 应非增"
    qc, qstar = satisfy(Tc).mean(), satisfy(Tstar).mean()
    assert qc > qstar, "P4: q(Tc) 应 > q(T*)"

    # 子集包含（在 eps 网格上逐点验证）
    for i in range(len(Ts) - 1):
        assert not np.any(satisfy(Ts[i + 1]) & ~satisfy(Ts[i])), "P2: S(T2) 不是 S(T1) 子集"

    # ---------- P4：两分量谱（B 类形状） ----------
    omega = np.linspace(-1.0, 1.0, 8001)
    delta = 0.03
    def gauss(center, width):
        g = np.exp(-0.5 * ((omega - center) / width) ** 2) / (width * math.sqrt(2 * math.pi))
        g += np.exp(-0.5 * ((omega + center) / width) ** 2) / (width * math.sqrt(2 * math.pi))
        return g / 2.0
    acoh, aincoh = gauss(delta, 0.004), gauss(0.0, 0.08)
    A_c = qc * acoh + (1 - qc) * aincoh
    A_s = qstar * acoh + (1 - qstar) * aincoh
    for A in (A_c, A_s):
        assert abs(float(np.trapezoid(A, omega)) - 1.0) < 1e-12, "P4: 谱未归一"

    # STM 示意局域谱重（toy epsilon 场，B 类）
    xx, yy = np.meshgrid(np.linspace(0, 1, 80), np.linspace(0, 1, 80))
    eps_field = math.pi + 1.3 * np.sin(6 * xx) * np.cos(5 * yy) + 0.9 * np.cos(11 * xx + 7 * yy)
    q_local = (J0 * (1 + eps_field / (2 * math.pi)) * w_full(Tc)
               * np.cos(s * N * eps_field) - k * Tc >= 0).astype(float)

    print("R30 G21 满足率（链内定义＋单调性，参数示意 B 类）：")
    print("  P1 (6G.8) 前件审计通过；热项取非相干 Θ(T)")
    print("  P2 子集包含全链成立；q(T) 非增")
    print("  P3 全域 w(Tc)=%.4f（低温展开在 T*/ωD≈0.67 失效，不用）" % wc)
    print("  P4 q(Tc)=%.4f > q(T*)=%.4f（p_c=%.4f 仅作对照线）" % (qc, qstar, pc))
    print("     两分量谱归一残差 <1e-12；STM 示意局域相干面积分数=%.4f" % q_local.mean())

    # ---------- 四面板 ----------
    fig, axes = plt.subplots(2, 2, figsize=(12.8, 9.6))

    ax = axes[0, 0]
    ax.plot(Ts, ws, "b-", lw=2.2, label="$w(T)$（全域 (10B.1)）")
    ax.plot(Ts, qs / qs.max(), "r--", lw=2.2, label="$q(T)/q(0)$（(6G.8) 满足率）")
    ax.axhline(pc, color="gray", ls=":", lw=1.4, label="$p_c$（对照线）")
    ax.set_xlabel("$T$ (K)")
    ax.set_ylabel("权重")
    ax.set_title("A  $w(T)$ 与 $q(T)$ 同向单调减")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[0, 1]
    for T in [60.0, 100.0, 160.0]:
        Fbar = J0 * Aeps * w_full(T) * cosL - k * T
        ax.plot(eps, Fbar, lw=2.0, label="$T=%.0f$ K" % T)
    ax.axhline(0.0, color="k", ls="--", lw=1.2)
    ax.set_xlabel("局域亏角 $\\varepsilon$")
    ax.set_ylabel("$F(\\varepsilon,T)$")
    ax.set_title("B  $T$ 升 → $F$ 降 → 满足集 $S(T)$ 收缩")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 0]
    ax.plot(omega * 1e3, A_c, "b-", lw=2.2, label="$T=T_c$（$q=%.3f$）" % qc)
    ax.plot(omega * 1e3, A_s, "r--", lw=2.2, label="$T=T^*$（$q=%.3f$）" % qstar)
    ax.set_xlim(-120, 120)
    ax.set_xlabel("$\\omega$ (meV)")
    ax.set_ylabel("$A(\\omega)$（归一）")
    ax.set_title("C  谱重转移：相干峰随 $T$ 降（B 类线形）")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)

    ax = axes[1, 1]
    im = ax.imshow(q_local, origin="lower", cmap="RdYlBu_r")
    ax.set_xlabel("$x$（示意）")
    ax.set_ylabel("$y$（示意）")
    ax.set_title("D  STM 局域相干图（$T=T_c$，toy $\\varepsilon(r)$）")
    fig.colorbar(im, ax=ax, shrink=0.85)

    fig.tight_layout()
    png = os.path.join(OUT, "R30_G21满足率单调性.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)

    rows = [
        ["P1", "(6G.8) 前件齐备", "通过"],
        ["P2", "子集包含全链成立；q 非增", "通过"],
        ["P3", "全域 w(Tc)=%.4f" % wc, "通过"],
        ["P4", "q(Tc)=%.4f > q(T*)=%.4f；归一 <1e-12" % (qc, qstar), "通过（形状层）"],
        ["P5", "单调性／子集（Lean）", "由 Lean 承载"],
        ["结论", "G21 满足率定义与单调性链内；数值外生", "状态不动"],
    ]
    with open(os.path.join(OUT, "R30_G21满足率单调性_摘要.csv"), "w",
              newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["判据", "数值", "判定"])
        wr.writerows(rows)

    print("图:", png)


if __name__ == "__main__":
    main()
