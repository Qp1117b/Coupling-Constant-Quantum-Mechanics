# -*- coding: utf-8 -*-
"""
M6 键几何的数值核对（环 10）。

1. 3D Debye 关联 rho3d(x)=2(1-cos x)/x^2 与 2D rho2d(x)=2 J1(x)/x；
2. 形状因子 J/J0=(1-rho) cos(s*ell) 随 x 的多条曲线；
3. 尾部 1-rho -> 1（饱和）；
4. 全对求和 S(X)=int_0^X x^(d+1)(1-rho) dx 的增长（发散），对比键局域常数；
5. 小 x 斜率 1/12、1/8 与近邻值。

只用 numpy + matplotlib；J1 用积分表示，不依赖 scipy。
"""

import csv
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PNG = os.path.join(HERE, "环10_M6键几何.png")
OUT_CSV = os.path.join(HERE, "环10_M6键几何.csv")


# ------------------------------------------------------------------ 关联函数
def rho3d(x):
    x = np.asarray(x, dtype=float)
    out = np.ones_like(x)
    nz = np.abs(x) > 1e-12
    out[nz] = 2.0 * (1.0 - np.cos(x[nz])) / x[nz] ** 2
    return out


def bessel_j1(x):
    """J1 的积分表示 J1(x) = (1/pi) int_0^pi cos(theta - x sin theta) dtheta。"""
    x = np.atleast_1d(np.asarray(x, dtype=float))
    th = np.linspace(0.0, np.pi, 4001)
    integrand = np.cos(th[None, :] - x[:, None] * np.sin(th)[None, :])
    return np.trapezoid(integrand, th, axis=1) / np.pi


def rho2d(x):
    x = np.atleast_1d(np.asarray(x, dtype=float))
    out = np.ones_like(x)
    nz = np.abs(x) > 1e-12
    out[nz] = 2.0 * bessel_j1(x[nz]) / x[nz]
    return out


# ------------------------------------------------------------------ 主程序
def main():
    rows = []

    # ---- 小 x 斜率
    for name, rho, target in [("3d", rho3d, 1.0 / 12.0), ("2d", rho2d, 1.0 / 8.0)]:
        for xv in (1e-3, 1e-2, 0.1):
            val = (1.0 - rho(np.array([xv]))[0]) / xv ** 2
            rows.append((f"small_x_{name}", xv, val, target, np.nan))
            print(f"{name}: x={xv:g}  (1-rho)/x^2={val:.6f}  target={target:.6f}")

    # ---- 近邻值
    x_sphere = (6.0 * np.pi ** 2) ** (1.0 / 3.0)
    for label, xv in [("sphere", x_sphere), ("zone", np.pi)]:
        r = rho3d(np.array([xv]))[0]
        rows.append((f"nn_{label}", xv, r, 1.0 - r, np.nan))
        print(f"NN {label}: x={xv:.5f}  rho={r:.5f}  1-rho={1.0-r:.5f}")

    # ---- 尾部
    for xv in (5.0, 10.0, 20.0, 50.0):
        rows.append(("tail_3d", xv, rho3d(np.array([xv]))[0], 1.0 - rho3d(np.array([xv]))[0], np.nan))
        rows.append(("tail_2d", xv, rho2d(np.array([xv]))[0], 1.0 - rho2d(np.array([xv]))[0], np.nan))
    print("tail 3d x=50: 1-rho =", 1.0 - rho3d(np.array([50.0]))[0])
    print("tail 2d x=50: 1-rho =", 1.0 - rho2d(np.array([50.0]))[0])

    # ---- 全对求和 S(X)
    xs = np.linspace(0.05, 20.0, 2000)
    f3 = xs ** 4 * (1.0 - rho3d(xs))
    f2 = xs ** 3 * (1.0 - rho2d(xs))
    S3 = np.concatenate([[0.0], np.cumsum(0.5 * (f3[1:] + f3[:-1]) * np.diff(xs))])
    S2 = np.concatenate([[0.0], np.cumsum(0.5 * (f2[1:] + f2[:-1]) * np.diff(xs))])
    for xv in (5.0, 10.0, 20.0):
        i = int(np.argmin(np.abs(xs - xv)))
        rows.append(("S3", xs[i], S3[i], xs[i] ** 5 / 5.0, np.nan))
        rows.append(("S2", xs[i], S2[i], xs[i] ** 4 / 4.0, np.nan))
    print(f"S3(20)={S3[-1]:.3f}  X^5/5={20**5/5:.3f}")
    print(f"S2(20)={S2[-1]:.3f}  X^4/4={20**4/4:.3f}")

    # ---- 写 CSV
    with open(OUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        wr = csv.writer(f)
        wr.writerow(["kind", "x", "y", "y_ref", "extra"])
        wr.writerows(rows)

    # ---- 画图
    fig, ax = plt.subplots(2, 2, figsize=(13.2, 9.4))

    # A: rho 与 1-rho
    xx = np.linspace(0.05, 20.0, 2000)
    ax[0, 0].plot(xx, rho3d(xx), lw=2.0, color="tab:blue", label=r"$\rho_{3d}=2(1-\cos x)/x^2$")
    ax[0, 0].plot(xx, rho2d(xx), lw=2.0, color="tab:orange", label=r"$\rho_{2d}=2J_1(x)/x$")
    ax[0, 0].plot(xx, 1.0 - rho3d(xx), lw=1.4, ls="--", color="tab:blue", alpha=0.75,
                  label=r"$1-\rho_{3d}$")
    ax[0, 0].plot(xx, 1.0 - rho2d(xx), lw=1.4, ls="--", color="tab:orange", alpha=0.75,
                  label=r"$1-\rho_{2d}$")
    ax[0, 0].axhline(1.0, color="0.35", lw=0.9, ls=":")
    ax[0, 0].axhline(0.0, color="0.35", lw=0.9, ls=":")
    ax[0, 0].set_xlabel(r"$x=k_D d$")
    ax[0, 0].set_ylabel("关联 / 形状因子")
    ax[0, 0].set_title("A  零点关联与差方差因子")
    ax[0, 0].set_ylim(-0.35, 1.35)
    ax[0, 0].legend(fontsize=7, loc="upper right")
    ax[0, 0].grid(alpha=0.3)

    # B: J/J0 随相位
    phases = [(0.0, r"$s\ell=0$"), (np.pi / 4, r"$\pi/4$"),
              (np.pi / 2, r"$\pi/2$"), (3 * np.pi / 4, r"$3\pi/4$"),
              (np.pi, r"$\pi$")]
    for ph, lab in phases:
        ax[0, 1].plot(xx, (1.0 - rho3d(xx)) * np.cos(ph), lw=1.8, label=lab)
    ax[0, 1].axhline(0.0, color="0.3", lw=0.9)
    ax[0, 1].set_xlabel(r"$x=k_D d$")
    ax[0, 1].set_ylabel(r"$J/J_0$")
    ax[0, 1].set_title(r"B  形状因子 $J/J_0=(1-\rho_{3d})\cos(s\ell)$")
    ax[0, 1].set_ylim(-1.15, 1.15)
    ax[0, 1].legend(fontsize=7, loc="lower right", ncol=2)
    ax[0, 1].grid(alpha=0.3)

    # C: 尾部 1-rho 双对数
    xt = np.logspace(0.0, 2.5, 800)
    ax[1, 0].loglog(xt, 1.0 - rho3d(xt), lw=2.0, color="tab:blue", label=r"$1-\rho_{3d}$")
    ax[1, 0].loglog(xt, 1.0 - rho2d(xt), lw=2.0, color="tab:orange", label=r"$1-\rho_{2d}$")
    ax[1, 0].axhline(1.0, color="0.35", lw=1.0, ls=":")
    ax[1, 0].text(1.2, 1.02, r"饱和值 $1$", fontsize=8, color="0.35")
    ax[1, 0].set_xlabel(r"$x=k_D d$")
    ax[1, 0].set_ylabel(r"$1-\rho$")
    ax[1, 0].set_title("C  差方差因子饱和（双对数）")
    ax[1, 0].set_ylim(0.4, 2.2)
    ax[1, 0].legend(fontsize=8)
    ax[1, 0].grid(alpha=0.3, which="both")

    # D: 全对求和 vs 键局域
    ax[1, 1].loglog(xs, S3, lw=2.2, color="tab:blue", label=r"3D: $\int_0^X x^4(1-\rho_{3d})dx$")
    ax[1, 1].loglog(xs, S2, lw=2.2, color="tab:orange", label=r"2D: $\int_0^X x^3(1-\rho_{2d})dx$")
    ax[1, 1].loglog(xs, xs ** 5 / 5.0, lw=1.0, ls=":", color="tab:blue", alpha=0.8,
                    label=r"$X^5/5$")
    ax[1, 1].loglog(xs, xs ** 4 / 4.0, lw=1.0, ls=":", color="tab:orange", alpha=0.8,
                    label=r"$X^4/4$")
    ax[1, 1].axhline(4.6, color="tab:green", lw=1.8, ls="--",
                     label="键局域常数（示意 $zJ a^2$）")
    ax[1, 1].set_xlabel(r"$X$（以 $1/k_D$ 为单位）")
    ax[1, 1].set_ylabel("累计求和（形状单位）")
    ax[1, 1].set_title("D  全对求和发散 vs 键局域有限")
    ax[1, 1].legend(fontsize=7, loc="upper left")
    ax[1, 1].grid(alpha=0.3, which="both")

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    plt.close(fig)
    print("saved:", OUT_PNG)
    print("saved:", OUT_CSV)


if __name__ == "__main__":
    main()
