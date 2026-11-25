# -*- coding: utf-8 -*-
"""环 19：Pearl–London 口径统一（第 152 轮，R-161）

只做解析式的数值核对与函数图像，不做任何数据拟合。
运行：python "环19_PearlLondon口径统一.py"（本目录）
输出：环19_PearlLondon口径统一.png、环19_PearlLondon口径统一.json
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

# ---------------- 物理常量（SI，CODATA 2018） ----------------
hb = 1.054571817e-34
mu0 = 4.0 * np.pi * 1e-7
e = 1.602176634e-19
kB = 1.380649e-23
Phi0 = 2.067833848e-15

# $C_\Upsilon=\hbar^2/(4\mu_0e^2)$；$\Upsilon=C_\Upsilon d\lambda^{-2}=C_\Upsilon c_\Lambda/\Lambda$
C_ups = hb**2 / (4.0 * mu0 * e**2)          # J*m
C_lam = np.pi * hb**2 / (4.0 * mu0 * e**2 * kB)   # m*K（=19.612 mm*K）
C_k = hb**2 / (4.0 * e**2)                  # J*H（片动能电感常数）

checks = {}


def ups_london(lam, d):
    """把报告值当 London 长度：Upsilon = hbar^2 d/(4 mu0 e^2 lam^2)"""
    return hb**2 * d / (4.0 * mu0 * e**2 * lam**2)


def ups_pearl(Lam, c):
    """把报告值当 Pearl 长度（约定因子 c）：Upsilon = C_ups*c/Lam"""
    return C_ups * c / Lam


# B1 约定因子：同一 Lambda 下 c=2 与 c=1 的刚度比恰为 2
checks["B1_factor"] = ups_pearl(1e-6, 2) / ups_pearl(1e-6, 1)
assert abs(checks["B1_factor"] - 2.0) < 1e-14, "约定因子应为 2"

# B2 第 151 轮两种约定下的读法比 c*x/d
pairs = [(3.0, 529.0), (5.0, 400.0), (10.0, 300.0)]
ratios = {}
for d_nm, x_nm in pairs:
    d, x = d_nm * 1e-9, x_nm * 1e-9
    for c in (2, 1):
        got = ups_pearl(x, c) / ups_london(x, d)
        ratios[f"d{d_nm:.0f}_c{c}"] = got
        assert abs(got - c * x_nm / d_nm) < 1e-9, f"读法比应为 {c}*x/d"
checks["B2_ratios"] = ratios

# B3 片动能电感恒等式：Upsilon = hbar^2/(4 e^2 L_k)
for d_nm, lam_nm in pairs:
    d, lam = d_nm * 1e-9, lam_nm * 1e-9
    Lk = mu0 * lam**2 / d
    u1 = hb**2 / (4.0 * e**2 * Lk)
    u2 = ups_london(lam, d)
    checks[f"B3_rel_d{d_nm:.0f}"] = abs(u1 / u2 - 1.0)
    assert abs(u1 / u2 - 1.0) < 1e-12, "L_k 恒等式不成立"
# Phi0 形式
checks["B3_phi0_rel"] = abs(hb**2 / (4.0 * e**2) / (Phi0**2 / (4.0 * np.pi**2)) - 1.0)
assert checks["B3_phi0_rel"] < 1e-9, "Phi0^2/(4 pi^2) 与 hbar^2/(4e^2) 不符"

# B4 BKT 线的无约定形式：L_k(Tc) = pi hbar^2/(8 e^2 kB Tc)
b4 = {}
for Tc in (1.0, 7.0, 10.0):
    Lk_BKT = np.pi * hb**2 / (8.0 * e**2 * kB * Tc)
    Lam_round = 2.0 * Lk_BKT / mu0
    rel = abs(Lam_round / (C_lam / Tc) - 1.0)
    b4[str(Tc)] = {"Lk_BKT_nH_sq": Lk_BKT * 1e9, "Lam_round_mm": Lam_round * 1e3, "rel": rel}
    assert rel < 1e-12, "BKT 线换算不一致"
checks["B4"] = b4

# B5 简并：(lam,d) -> (s*lam, s^2*d) 刚度不变
b5 = {}
lam0, d0 = 529e-9, 3e-9
for s in (0.5, 2.0, 10.0):
    rel = abs(ups_london(s * lam0, s**2 * d0) / ups_london(lam0, d0) - 1.0)
    b5[str(s)] = rel
    assert rel < 1e-14, "简并轨道上刚度应不变"
checks["B5"] = b5

# B6 无约定的 B：L_k(0)/L_k^BKT(Tc) 与 Tc*Lambda/C_lam 一致
b6 = {}
for Tc, Lam in [(7.0, 529e-9), (7.0, 2.0 * (529e-9) ** 2 / 3e-9)]:
    B_lam = Tc * Lam / C_lam
    Lk = mu0 * Lam / 2.0
    Lk_BKT = np.pi * hb**2 / (8.0 * e**2 * kB * Tc)
    B_lk = Lk / Lk_BKT
    rel = abs(B_lk / B_lam - 1.0)
    b6[f"Lam={Lam*1e9:.3f}nm_c2"] = {"B_Lam": B_lam, "B_Lk": B_lk, "rel": rel}
    assert rel < 1e-12, "B 的无约定读法不一致"
checks["B6"] = b6

# ---------------- 图 ----------------
fig, ax = plt.subplots(2, 3, figsize=(16.5, 9.2))

# (a) Upsilon(x) 两种读法（d=3 nm）
x = np.logspace(-8, -6, 200)
d0 = 3e-9
ax[0, 0].loglog(x * 1e9, ups_pearl(x, 2), "k-", lw=2, label=r"读作 $\Lambda$（$c_\Lambda=2$）")
ax[0, 0].loglog(x * 1e9, ups_london(x, d0), "r--", lw=2, label=r"读作 $\lambda_L$（$d=3$ nm）")
ax[0, 0].loglog(x * 1e9, ups_pearl(x, 1), "b:", lw=1.4, label=r"读作 $\Lambda$（$c_\Lambda=1$）")
ax[0, 0].set_xlabel(r"报告长度 $x$ [nm]")
ax[0, 0].set_ylabel(r"$\Upsilon$ [J]")
ax[0, 0].set_title(r"(a) 同一报告值的两种读出")
ax[0, 0].legend(fontsize=8)
ax[0, 0].grid(True, which="both", alpha=0.25)

# (b) 读法比 vs d（x=529 nm）
dd = np.logspace(-9, -8, 200)
ax[0, 1].loglog(dd * 1e9, 2 * 529e-9 / dd, "k-", lw=2, label=r"$c_\Lambda=2$：$2x/d$")
ax[0, 1].loglog(dd * 1e9, 529e-9 / dd, "b:", lw=1.5, label=r"$c_\Lambda=1$：$x/d$")
for d_nm in (3.0, 5.0, 10.0):
    ax[0, 1].plot([d_nm], [2 * 529e-9 / (d_nm * 1e-9)], "ro", ms=5)
ax[0, 1].set_xlabel(r"$d$ [nm]")
ax[0, 1].set_ylabel(r"$\Upsilon_\Lambda/\Upsilon_\lambda$")
ax[0, 1].set_title(r"(b) 读法比随厚度（$x=529$ nm，红点 $d=3/5/10$）")
ax[0, 1].legend(fontsize=8)
ax[0, 1].grid(True, which="both", alpha=0.25)

# (c) BKT 线：L_k(Tc)
Tc = np.logspace(-0.3, 1.7, 200)
Lk_line = np.pi * hb**2 / (8.0 * e**2 * kB * Tc)
ax[0, 2].loglog(Tc, Lk_line * 1e9, "k-", lw=2, label=r"$L_{k,\mathrm{sq}}(T_c)=\pi\hbar^2/(8e^2k_BT_c)$")
for T0 in (1.0, 7.0, 10.0):
    ax[0, 2].plot([T0], [np.pi * hb**2 / (8.0 * e**2 * kB * T0) * 1e9], "ro", ms=5)
ax[0, 2].set_xlabel(r"$T_c$ [K]")
ax[0, 2].set_ylabel(r"$L_{k,\mathrm{sq}}$ [nH/$\mathrm{sq}$]")
ax[0, 2].set_title(r"(c) BKT 线的无约定形式")
ax[0, 2].legend(fontsize=8)
ax[0, 2].grid(True, which="both", alpha=0.25)

# (d) 简并轨道：lam^2/d = const
lam = np.logspace(-8, -5.5, 200)
const = lam0**2 / d0
ax[1, 0].loglog(lam * 1e9, lam**2 / const * 1e9, "k-", lw=2, label=r"$\lambda_L^2/d=$ 常数")
for s in (0.5, 1.0, 2.0, 10.0):
    ax[1, 0].plot([s * lam0 * 1e9], [s**2 * d0 * 1e9], "ro", ms=5)
ax[1, 0].set_xlabel(r"$\lambda_L$ [nm]")
ax[1, 0].set_ylabel(r"$d$ [nm]")
ax[1, 0].set_title(r"(d) 简并轨道：红点同 $\Upsilon$")
ax[1, 0].legend(fontsize=8)
ax[1, 0].grid(True, which="both", alpha=0.25)

# (e) B 的两种算法一致性
bl = []
for Tc0, Lam in [(7.0, 529e-9), (7.0, 2 * (529e-9) ** 2 / 3e-9), (10.0, 0.5e-3), (1.0, 19.61e-3)]:
    B_lam = Tc0 * Lam / C_lam
    Lk = mu0 * Lam / 2.0
    Lk_BKT = np.pi * hb**2 / (8.0 * e**2 * kB * Tc0)
    bl.append((B_lam, Lk / Lk_BKT))
bl = np.array(bl)
ax[1, 1].loglog(bl[:, 0], bl[:, 1], "ko", ms=6)
lims = [min(bl.min(), 1e-5) * 0.5, max(bl.max(), 1e-1) * 2]
ax[1, 1].loglog(lims, lims, "r--", lw=1.2, label=r"$y=x$")
ax[1, 1].set_xlabel(r"$\mathcal{B}=T_c\Lambda/C_\Lambda$")
ax[1, 1].set_ylabel(r"$L_{k,\mathrm{sq}}(0)/L_{k,\mathrm{sq}}^{\rm BKT}(T_c)$")
ax[1, 1].set_title(r"(e) $\mathcal{B}$ 的无约定读法")
ax[1, 1].legend(fontsize=8)
ax[1, 1].grid(True, which="both", alpha=0.25)

# (f) Lambda 与 Upsilon：两种约定相差因子 2
Lam = np.logspace(-7, -3, 200)
ax[1, 2].loglog(Lam * 1e3, ups_pearl(Lam, 2), "k-", lw=2, label=r"$c_\Lambda=2$")
ax[1, 2].loglog(Lam * 1e3, ups_pearl(Lam, 1), "b--", lw=1.6, label=r"$c_\Lambda=1$")
ax[1, 2].fill_between(Lam * 1e3, ups_pearl(Lam, 1), ups_pearl(Lam, 2), color="orange", alpha=0.15)
ax[1, 2].set_xlabel(r"$\Lambda$ [mm]")
ax[1, 2].set_ylabel(r"$\Upsilon$ [J]")
ax[1, 2].set_title(r"(f) 约定因子 $c_\Lambda$ 只改常数")
ax[1, 2].legend(fontsize=8)
ax[1, 2].grid(True, which="both", alpha=0.25)

plt.tight_layout()
plt.savefig("环19_PearlLondon口径统一.png", dpi=150)

with open("环19_PearlLondon口径统一.json", "w", encoding="utf-8") as f:
    json.dump(checks, f, ensure_ascii=False, indent=2)

print(json.dumps(checks, ensure_ascii=False, indent=2))
print("全部断言通过")
