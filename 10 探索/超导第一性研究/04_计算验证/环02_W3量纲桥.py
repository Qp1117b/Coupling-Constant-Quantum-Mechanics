# -*- coding: utf-8 -*-
"""
环 2  W-3 量纲桥：L 本征值 -> omega_q^2，以及角量/位移量分离
================================================================
第 71 轮（R71）。只用链内已登记的量与外部标准工具，不拟合。

四个子图：
  (1) 正三角网格 cot 拉普拉斯的色散：lambda(q)/(A_v q^2) -> 1（纯数 K=1 的数值核）
  (2) omega(q) = c_s sqrt(lambda/A_v) 与连续声学支 c_s q 的重合（长波极限）
  (3) Debye 恒等式 theta_D = (hbar/k_B) v_D (6 pi^2 n)^{1/3} 与实验 theta_D 的对照
  (4) 振幅预算：sigma_eps/c_eps = 1.21 (l_q/a)^2；以及由观测 lambda 反解的 g

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环02_W3量纲桥.py"
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

HBAR = 1.054571817e-34      # J s
KB = 1.380649e-23           # J/K
EV = 1.602176634e-19        # J

OUT = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------
# 1. 正三角网格：cot 拉普拉斯 L_ij = -(1/2)(cot a + cot b) = -1/sqrt(3)
#    (Lu)_i = (1/sqrt(3)) (6 u_i - sum_6 u_j)
#    Voronoi 面积（每顶点）A_v = sqrt(3)/2 * l^2
#    无量纲本征值 lambda(q) = (1/sqrt(3))(6 - sum_6 cos(q.delta))
# ----------------------------------------------------------------------
def lam_tri(ql, theta=0.0):
    """三角网格 cot 拉普拉斯在平面波上的 Rayleigh 商（无量纲）。"""
    s = 0.0
    for k in range(6):
        phi = k * math.pi / 3.0
        s += math.cos(ql * math.cos(phi - theta))
    return (6.0 - s) / math.sqrt(3.0)


A_V_OVER_L2 = math.sqrt(3.0) / 2.0     # A_v / l^2


def panel1():
    ql = np.linspace(1e-3, 2.0, 400)
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for theta, lab in ((0.0, r"$q\parallel\Gamma M$"), (math.pi / 6.0, r"$q$ 沿 $30^\circ$")):
        ratio = np.array([lam_tri(x, theta) / (A_V_OVER_L2 * x * x) for x in ql])
        ax.plot(ql, ratio, lw=1.8, label=lab)
    ax.axhline(1.0, color="k", ls="--", lw=1.2, label=r"$K=1$（声学极限）")
    ax.set_xlabel(r"$q\ell$")
    ax.set_ylabel(r"$\lambda_q/(A_v q^2)$")
    ax.set_title(r"cot 拉普拉斯无量纲本征值的声学标度（$K=1$ 精确）")
    ax.set_ylim(0, 1.25)
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUT, "环02_W3_色散标度.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def panel2():
    ql = np.linspace(1e-2, 1.2, 300)
    fig, ax = plt.subplots(figsize=(6.0, 4.2))
    for cs, lab in ((3624.0, "Al ($v_D=3.62$ km/s)"), (1277.0, "Pb ($v_D=1.28$ km/s)")):
        # 取 l = 1（只画归一化色散），频率单位任意
        w = np.array([cs * math.sqrt(lam_tri(x) / A_V_OVER_L2) / 1.0 for x in ql])
        ax.plot(ql, w, lw=1.8, label=lab + r"：$\omega=c_s\sqrt{\lambda/A_v}$")
        ax.plot(ql, cs * ql, "k--", lw=1.0)
    ax.set_xlabel(r"$q\ell$")
    ax.set_ylabel(r"$\omega$（相对单位）")
    ax.set_title("长波极限与连续声学支重合（虚线 $c_sq$）")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUT, "环02_W3_声学极限.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


# ----------------------------------------------------------------------
# 2. 材料数据（标准文献值；c11/c44 单位 GPa，a 单位 Å）
#    n = 每胞原子数 / a^3；v_D = [3/(1/v_l^3 + 2/v_t^3)]^{1/3}
#    N(0) = gamma/2.355  （states/eV/atom，含自旋）
# ----------------------------------------------------------------------
MAT = [
    # 名称, 结构, c11, c44, rho, a[A], thetaD_exp, gamma[mJ/mol/K^2], lambda_obs
    ("Al", 4, 107.0, 28.3, 2700.0, 4.0495, 428.0, 1.35, 0.43),
    ("Nb", 2, 246.0, 28.7, 8570.0, 3.3004, 275.0, 7.80, 0.95),
    ("V",  2, 228.0, 42.6, 6110.0, 3.0240, 380.0, 9.30, 0.80),
    ("Ta", 2, 261.0, 82.5, 16650.0, 3.3060, 240.0, 5.90, 0.65),
    ("Pb", 4, 49.5, 14.9, 11340.0, 4.9508, 105.0, 3.00, 1.55),
]

C_EPS = 0.5      # c_eps = kappa * RMS(eps^(0))，kappa≈0.53（第 86 轮）；取 RMS=1 rad 的保守值
ONE_MINUS_RHO = 0.9   # (1 - rho_ij) 的 O(1) 取值；预算只到量级


def material_budget():
    rows = []
    for name, nat, c11, c44, rho, aA, thD, gamma, lam in MAT:
        a = aA * 1e-10
        v_l = math.sqrt(c11 * 1e9 / rho)
        v_t = math.sqrt(c44 * 1e9 / rho)
        v_D = (3.0 / (1.0 / v_l ** 3 + 2.0 / v_t ** 3)) ** (1.0 / 3.0)
        n = nat / a ** 3
        thD_pred = (HBAR / KB) * v_D * (6.0 * math.pi ** 2 * n) ** (1.0 / 3.0)
        Q = (6.0 * math.pi ** 2 * n) ** (1.0 / 3.0)
        lq = (HBAR / (rho * v_D)) ** 0.25
        # 节点测度尺度 a_n = Omega^{1/3} = n^{-1/3}（不是晶格常数 a_lat！）
        a_n = n ** (-1.0 / 3.0)
        ratio = lq / a_n
        # sigma_0^2 = c_eps^2 * (6 pi^2)^{4/3}/(16 pi^2) * (lq/a)^4
        coef = (6.0 * math.pi ** 2) ** (4.0 / 3.0) / (16.0 * math.pi ** 2)
        sig0sq = (C_EPS ** 2) * coef * ratio ** 4
        sig_eps = math.sqrt(sig0sq)
        # 振幅预算（统一用 eV）：lambda = 4 N(0) g^2 sigma^2 (1-rho) / (hbar omega)
        hw_eV = KB * thD_pred / EV
        N0 = gamma / 2.355          # states/eV/atom（含自旋）
        g_eV = math.sqrt(lam * hw_eV / (4.0 * N0 * sig0sq * ONE_MINUS_RHO))
        # 声子能标与量子长度
        rows.append(dict(
            材料=name, a_lat_nm=a * 1e9, a_n_nm=a_n * 1e9, n_1e28=n / 1e28,
            v_l=v_l, v_t=v_t, v_D=v_D,
            thetaD_pred=thD_pred, thetaD_exp=thD, thetaD_ratio=thD_pred / thD,
            Q_1e10=Q / 1e10, lq_nm=lq * 1e9, lq_over_a=ratio, coef=coef,
            sigma0sq_over_ceps2=sig0sq / C_EPS ** 2,
            sigma_eps_over_ceps=sig_eps / C_EPS,
            N0=N0, lambda_obs=lam, g_eV=g_eV,
            # R43 已登记三支偏振前因子 1+2*eta_t = 5.59；并入后 g 乘 1/sqrt(5.59)
            g_eV_pol= g_eV / math.sqrt(5.59),
        ))
    return rows


def panel3(rows):
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    xs = [r["thetaD_exp"] for r in rows]
    ys = [r["thetaD_pred"] for r in rows]
    ax.plot([80, 460], [80, 460], "k--", lw=1.2, label="y = x")
    ax.plot([80, 460], [0.75 * np.array([80, 460]), 0.75 * np.array([80, 460])], ":", color="gray", lw=1)
    ax.plot([80, 460], [1.25 * np.array([80, 460]), 1.25 * np.array([80, 460])], ":", color="gray", lw=1)
    for r in rows:
        ax.plot(r["thetaD_exp"], r["thetaD_pred"], "o", ms=6)
        ax.annotate(r["材料"], (r["thetaD_exp"], r["thetaD_pred"]),
                    textcoords="offset points", xytext=(6, 4), fontsize=9)
    ax.set_xlabel(r"实验 $\Theta_D$ (K)")
    ax.set_ylabel(r"$\Theta_D=(\hbar v_D/k_B)(6\pi^2n)^{1/3}$ (K)")
    ax.set_title("Debye–声速恒等式（点线为 ±25%，与 Debye 模型自身误差同量级）")
    ax.legend(frameon=False, fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    path = os.path.join(OUT, "环02_W3_Debye恒等式.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def panel4(rows):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.6, 4.2))
    xs = [r["lq_over_a"] ** 2 for r in rows]
    ys = [r["sigma_eps_over_ceps"] for r in rows]
    ax1.loglog(xs, ys, "o", ms=6)
    xx = np.linspace(min(xs) * 0.8, max(xs) * 1.2, 50)
    ax1.loglog(xx, 1.21 * xx, "k--", lw=1.2, label=r"$\sigma_\varepsilon/c_\varepsilon=1.209(\ell_q/a_n)^2$")
    for r in rows:
        ax1.annotate(r["材料"], (r["lq_over_a"] ** 2, r["sigma_eps_over_ceps"]),
                     textcoords="offset points", xytext=(5, 4), fontsize=9)
    ax1.set_xlabel(r"$(\ell_q/a_n)^2$")
    ax1.set_ylabel(r"$\sigma_\varepsilon/c_\varepsilon$")
    ax1.set_title("无量纲小参数")
    ax1.legend(frameon=False, fontsize=8)
    ax1.grid(alpha=0.3, which="both")

    names = [r["材料"] for r in rows]
    gs = [r["g_eV"] for r in rows]
    ax2.bar(names, gs, color="#4a90d9")
    ax2.axhspan(1.0, 30.0, color="orange", alpha=0.18, label="形变势典型区间 1–30 eV")
    ax2.set_ylabel(r"由观测 $\lambda$ 反解的 $g$ (eV)")
    ax2.set_title("振幅预算：环 10 的 $g$ 必要量级")
    ax2.legend(frameon=False, fontsize=8)
    ax2.grid(alpha=0.3, axis="y")
    fig.tight_layout()
    path = os.path.join(OUT, "环02_W3_振幅预算.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


def main():
    # --- 断言 1：长波极限 K = 1 ---
    for theta in (0.0, math.pi / 6.0, math.pi / 12.0):
        for ql in (1e-3, 1e-4):
            r = lam_tri(ql, theta) / (A_V_OVER_L2 * ql * ql)
            assert abs(r - 1.0) < 2e-3, (theta, ql, r)
    # --- 断言 2：lam 在 ql 小时 ~ ql^2（比值单调趋 1）---
    ratios = [lam_tri(x) / (A_V_OVER_L2 * x * x) for x in (1e-1, 1e-2, 1e-3)]
    assert ratios[0] < ratios[1] < ratios[2] < 1.0005, ratios

    p1 = panel1()
    p2 = panel2()
    rows = material_budget()
    p3 = panel3(rows)
    p4 = panel4(rows)

    # --- 断言 3：Debye 恒等式偏差在 ±25% 内 ---
    for r in rows:
        assert 0.7 < r["thetaD_ratio"] < 1.3, r
    # --- 断言 4：小参数 < 0.1（线性响应自洽的最低要求）---
    for r in rows:
        assert r["sigma_eps_over_ceps"] < 0.1, r
    # --- 断言 5：反解 g 落在 0.5–30 eV（形变势量级；下沿被偏振前因子压低）---
    for r in rows:
        assert 0.5 < r["g_eV"] < 30.0, r
        assert 0.2 < r["g_eV_pol"] < 30.0, r

    csv_path = os.path.join(OUT, "环02_W3_量纲桥.csv")
    keys = list(rows[0].keys())
    with open(csv_path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in r.items()})

    print("=== 环 02 W-3 量纲桥 ===")
    print("K(2D 三角网格，Voronoi 测度) = 1（解析；数值核见 环02_W3_色散标度.png）")
    print("(6pi^2)^{4/3}/(16pi^2) = %.4f" % rows[0]["coef"])
    head = ("材料 a_lat a_n n[1e28] vD[m/s] ThD_pred ThD_exp 比 Q[1e10] lq[nm] lq/a_n "
            "sig0^2/c^2 sig/c g[eV] g[eV]@5.59")
    print(head)
    for r in rows:
        print("%-3s %.3f %.3f %.3f %7.0f %7.1f %6.1f %5.3f %5.3f %5.3f %6.3f %6.3f %.3f %.2f %.2f" % (
            r["材料"], r["a_lat_nm"], r["a_n_nm"], r["n_1e28"], r["v_D"],
            r["thetaD_pred"], r["thetaD_exp"], r["thetaD_ratio"], r["Q_1e10"],
            r["lq_nm"], r["lq_over_a"], r["sigma0sq_over_ceps2"],
            r["sigma_eps_over_ceps"], r["g_eV"], r["g_eV_pol"]))
    print("图：", os.path.basename(p1), os.path.basename(p2),
          os.path.basename(p3), os.path.basename(p4))
    print("表：", os.path.basename(csv_path))


if __name__ == "__main__":
    main()
