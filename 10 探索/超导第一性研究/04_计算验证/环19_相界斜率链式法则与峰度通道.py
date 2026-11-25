# -*- coding: utf-8 -*-
"""
第 141 轮：相界斜率的链式法则修正 + 峰度→自由度→温度导数通道

A 段：M8 的 dp_pair/ddelta 若读作偏导则漏项；隐函数定理给严格分母 p_*'-dT p_pair。
B 段：非高斯样本方差等效自由度 DF_n = 2n/[k-(n-3)/(n-1)]（O'Neill 2014），
      峰度 k 进入 ∂T p_pair。
C 段：修正因子 r = p_*'/(p_*'-∂T p_pair) 的形状敏感度。
D 段：与第 140 轮"阈值处值敏感 1.5%"对比——导数是放大还是缩小。
无拟合：所有曲线由解析式直接计算。
"""
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import brentq

OUT = "D:/WorkSpace/物理/CQMFormal/10 探索/超导第一性研究/04_计算验证"
PC = 0.592746
T_BKT = 0.15
T_EXP = 1.3
NCELL = 10
SIGC0 = 0.70

# ---------------------------------------------------------------- A. 基准模型
def w(T):
    """Debye 低温抑制因子（环 10），w(0)=1, w'<0。"""
    return 1.0 - (math.pi ** 2 / 3.0) * T * T

def wp(T):
    return -(2.0 * math.pi ** 2 / 3.0) * T

def Vcoh(T):
    """环 10 (10B.16)：sigma_l^2 = Z w(T)，Z=1 归一。"""
    return w(T)

def x_of(T, sigc, nu):
    return nu * sigc ** 2 / Vcoh(T)

def ppair(T, sigc, nu):
    """环 15 (15D.1)，用有效自由度 nu 的 chi-square 尾。"""
    return 1.0 - chi2.cdf(x_of(T, sigc, nu), nu)

def pstar(T):
    return PC + (1.0 - PC) * (T / T_BKT) ** (1.0 / T_EXP)

def pstar_p(T):
    return (1.0 - PC) * (1.0 / T_EXP) * (T / T_BKT) ** (1.0 / T_EXP) / T

def dT_ppair(T, sigc, nu):
    """解析 ∂T p_pair = f_nu(x) * x/V * V'(T)；V'<0 ⇒ ∂T p_pair<0。"""
    x = x_of(T, sigc, nu)
    return chi2.pdf(x, nu) * (x / Vcoh(T)) * wp(T)

def dSig_ppair(T, sigc, nu):
    """解析 ∂_{sigma_c} p_pair = -f_nu(x) * 2x/sigma_c。"""
    x = x_of(T, sigc, nu)
    return -chi2.pdf(x, nu) * 2.0 * x / sigc

def Tc_of(sigc, nu):
    f = lambda T: ppair(T, sigc, nu) - pstar(T)
    return brentq(f, 1e-6, T_BKT * 0.999, xtol=1e-13)

def df_nu(n, kappa):
    """O'Neill (2014) 有效自由度：kappa=3 给 n-1（正态精确）。"""
    return 2.0 * n / (kappa - (n - 3.0) / (n - 1.0))

# ---------------------------------------------------------------- A 段
print("=" * 78)
print("A. 链式法则：M8 的偏导读法 vs 隐函数定理的严格读法")
print("=" * 78)
nu3 = df_nu(NCELL, 3.0)
assert abs(nu3 - (NCELL - 1)) < 1e-12
Tc = Tc_of(SIGC0, nu3)
p_at = ppair(Tc, SIGC0, nu3)
pt = dT_ppair(Tc, SIGC0, nu3)
ps = pstar_p(Tc)

# 掺杂取 sigma_c(sigma) = SIGC0*(1+sigma)，故 d sigma_c/d sigma = SIGC0
dsc = SIGC0
partial_d = dSig_ppair(Tc, SIGC0, nu3) * dsc   # 偏导（固定 T）
# 注意：sigma_c 升 ⇒ 阈值升 ⇒ p_pair 降 ⇒ partial_d < 0
slope_M8 = partial_d / ps                        # 若 dp_pair/ddelta 读作偏导
slope_exact = partial_d / (ps - pt)              # 隐函数定理：分母 ps - pt
# 数值差分验证（用中心差分求 dTc/dsig）
h = 1e-6
Tcp = Tc_of(SIGC0 * (1 + h), nu3)
Tcm = Tc_of(SIGC0 * (1 - h), nu3)
slope_num = (Tcp - Tcm) / (2 * h)

print(f"  n={NCELL}, kappa=3 ⇒ nu={nu3:.1f}; Tc={Tc:.6f}, p_pair(Tc)={p_at:.6f}")
print(f"  p_*' = {ps:.6f} > 0,  dT p_pair = {pt:.6f} < 0  (升温配对减少)")
print(f"  d_sigma p_pair = {partial_d:.6f}")
print(f"  M8 偏导读法 dTc/dsig = {slope_M8:+.6f}")
print(f"  严格（隐函数）     = {slope_exact:+.6f}")
print(f"  数值中心差分       = {slope_num:+.6f}")
print(f"  偏导读法相对误差   = {abs(slope_M8/slope_num-1)*100:.2f}%")
print(f"  严格读法相对误差   = {abs(slope_exact/slope_num-1)*100:.2e}%")
assert abs(slope_exact / slope_num - 1) < 1e-5
assert abs(slope_M8 / slope_num - 1) > 0.05, "偏导读法必须显著失准，否则本轮无意义"
assert pt < 0 < ps

# ---------------------------------------------------------------- B 段
print("\n" + "=" * 78)
print("B. 峰度 -> 有效自由度 -> 温度导数（固定同一交点 T_c，反解 sigma_c）")
print("=" * 78)
kappas = {"正态": 3.0, "均匀": 1.8, "指数": 9.0, "重尾(k=12)": 12.0}
print(f"  {'分布':<10}{'kappa':>7}{'nu':>9}{'sigma_c':>10}{'dT p_pair':>13}{'dSig p_pair':>13}")

def sigc_for_Tc(tic, nu):
    """反解 sigma_c 使交点恰好落在 tic：p_pair(tic,sigma_c,nu)=pstar(tic)。"""
    target = pstar(tic)
    return brentq(lambda sc: ppair(tic, sc, nu) - target, 1e-4, 5.0, xtol=1e-13)

rows = []
for name, k in kappas.items():
    nu = df_nu(NCELL, k)
    assert nu > 1.0
    sc = sigc_for_Tc(Tc, nu)
    dv = dT_ppair(Tc, sc, nu)
    ds = dSig_ppair(Tc, sc, nu)
    rows.append(dict(name=name, kappa=k, nu=nu, sigc=sc, dTp=dv, dSp=ds))
    print(f"  {name:<10}{k:>7.1f}{nu:>9.3f}{sc:>10.5f}{dv:>13.6f}{ds:>13.6f}")

# ---------------------------------------------------------------- C 段
print("\n" + "=" * 78)
print("C. 修正因子 r = p_*'/(p_*'-dT p_pair) 的形状敏感度（同一 T_c）")
print("=" * 78)
print("  %-10s%9s%11s%11s%9s" % ("分布", "nu", "p_*'", "-dT p", "r"))
rs = []
for row in rows:
    psp = pstar_p(Tc)
    neg = -row["dTp"]
    r = psp / (psp + neg)
    rs.append((row["name"], r))
    print("  %-10s%9.3f%11.4f%11.4f%9.4f" % (row["name"], row["nu"], psp, neg, r))
spread = max(r for _, r in rs) - min(r for _, r in rs)
print(f"\n  r 的分布离散 = {spread*100:.2f}%  （对比第 140 轮值敏感 1.5%）")
assert 0.0 < min(r for _, r in rs) < max(r for _, r in rs) < 1.0

# 纯导数敏感度：同一 T_c、各自 sigma_c，与正态基准比
base_dv = rows[0]["dTp"]; base_ds = rows[0]["dSp"]
print(f"\n  {'分布':<10}{'dT p_pair 相对正态':>20}{'dSig p_pair 相对正态':>22}")
pure_d, pure_s = [], []
for row in rows:
    rd = abs(row["dTp"] / base_dv - 1)
    rsg = abs(row["dSp"] / base_ds - 1)
    pure_d.append(rd); pure_s.append(rsg)
    print(f"  {row['name']:<10}{rd*100:>19.1f}%{rsg*100:>21.1f}%")
print(f"  最大相对变化：dT p_pair {max(pure_d)*100:.1f}%，dSig p_pair {max(pure_s)*100:.1f}%")
assert max(pure_d) > 0.05, "峰度应显著改变温度导数（否则通道不存在）"

# ---------------------------------------------------------------- D 段
print("\n" + "=" * 78)
print("D. 斜率 dT_c/dsigma 的形状敏感度（固定同一交点）")
print("=" * 78)
print(f"  {'分布':<10}{'dTc/dsig(严格)':>17}{'相对正态':>12}{'M8偏读':>12}{'偏读误差':>11}")
slopes = []
for row in rows:
    psp = pstar_p(Tc)
    sl = row["dSp"] / (psp - row["dTp"])
    sl_m8 = row["dSp"] / psp
    rel = abs(sl / (base_ds / (psp - base_dv)) - 1)
    err = abs(sl_m8 / sl - 1)
    slopes.append((row["name"], sl, rel, err))
    print(f"  {row['name']:<10}{sl:>17.6f}{rel*100:>11.1f}%{sl_m8:>12.6f}{err*100:>10.1f}%")
sl_spread = max(s for _, s, _, _ in slopes) / min(s for _, s, _, _ in slopes) - 1
print(f"\n  严格斜率的分布离散 = {sl_spread*100:.1f}%")
# 严格恒等式：偏读斜率/严格斜率 = 1/r ⇒ 偏读误差 = 1/r - 1
print("  恒等式核对：偏读误差 == 1/r - 1")
for (name, _, _, err), (_, r) in zip(slopes, rs):
    pred = 1.0 / r - 1.0
    print(f"    {name:<10}实测 {err*100:6.2f}%  1/r-1 {pred*100:6.2f}%  差 {abs(err-pred):.2e}")
    assert abs(err - pred) < 1e-9
print("  物理读法：r 越接近 1（重尾）偏读越好；r 偏离 1 越多（均匀）偏读越坏。")
assert max(e for _, _, _, e in slopes) > 0.10, "至少一种分布下偏读误差 >10%"

# ---------------------------------------------------------------- 图
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
fig, axes = plt.subplots(2, 2, figsize=(13, 9))

# A: 三条斜率柱状
ax = axes[0, 0]
vals = [slope_M8, slope_exact, slope_num]
labels = ["M8 偏导读法", "隐函数定理", "数值差分"]
bars = ax.bar(labels, vals, color=["#C0504D", "#4C9F70", "#4C72B0"], alpha=.8)
ax.axhline(0, color="k", lw=.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v, f"{v:.4f}", ha="center",
            va="bottom" if v > 0 else "top", fontsize=9)
ax.set_ylabel(r"$dT_c/d\delta$")
ax.set_title("A. 斜率：偏导读法失准，隐函数定理与数值一致")
ax.grid(alpha=.3, axis="y")

# B: 不同峰度的 p_pair(T)
ax = axes[0, 1]
Ts = np.linspace(1e-4, T_BKT * 0.95, 400)
for row, c in zip(rows, ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]):
    ax.plot(Ts, [ppair(t, row["sigc"], row["nu"]) for t in Ts],
            color=c, label=f"{row['name']} ($\\nu$={row['nu']:.1f})")
ax.plot(Ts, [pstar(t) for t in Ts], "k--", lw=1.4, label=r"$p_*(T)$")
ax.axhline(PC, color="gray", ls=":", lw=1, label=r"$p_c$")
for row, c in zip(rows, ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]):
    ax.plot(Tc, pstar(Tc), "o", color=c, ms=7)
ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$p_{\rm pair}$")
ax.set_title("B. 峰度移动整条配对曲线与交点")
ax.legend(fontsize=8); ax.grid(alpha=.3)

# C: 修正因子随 T
ax = axes[1, 0]
for row, c in zip(rows, ["#4C72B0", "#DD8452", "#55A868", "#C44E52"]):
    rr = []
    for t in Ts:
        psp = pstar_p(t); neg = -dT_ppair(t, SIGC0, row["nu"])
        rr.append(psp / (psp - dT_ppair(t, row["sigc"], row["nu"])))
    ax.semilogx(Ts, rr, color=c, label=f"{row['name']}")
ax.set_ylim(0, 1.05)
ax.set_xlabel(r"$T/\omega_D$"); ax.set_ylabel(r"$r=p_*'/(p_*'-\partial_T p_{\rm pair})$")
ax.set_title("C. 修正因子 <1：M8 偏导读法高估斜率")
ax.legend(fontsize=8); ax.grid(alpha=.3, which="both")

# D: 值与导数的形状敏感度
ax = axes[1, 1]
names = [r["name"] for r in rows]
ax.bar([name for name, _, _, _ in slopes],
      [rel * 100 for _, _, rel, _ in slopes], color="#C0504D", alpha=.65)
ax.set_ylabel(r"严格斜率相对正态的变化 (%)")
ax.set_title("D. 同一交点下斜率仍有形状依赖")
for i, (_, _, rel, err) in enumerate(slopes):
    ax.text(i, rel * 100, f"偏读误差{err*100:.0f}%", ha="center", va="bottom", fontsize=8)
ax.legend(fontsize=8); ax.grid(alpha=.3, axis="y")

fig.tight_layout()
fig.savefig(f"{OUT}/环19_相界斜率与峰度通道.png", dpi=150)
print("\n图已存：环19_相界斜率与峰度通道.png")

# ---------------------------------------------------------------- 摘要
import csv
with open(f"{OUT}/环19_相界斜率与峰度通道_摘要.csv", "w", newline="", encoding="utf-8-sig") as f:
    wcsv = csv.writer(f)
    wcsv.writerow(["量", "值", "判据"])
    wcsv.writerow(["p_*'", f"{ps:.6f}", ">0"])
    wcsv.writerow(["dT p_pair", f"{pt:.6f}", "<0（升温配对减少）"])
    wcsv.writerow(["M8 偏导读法斜率", f"{slope_M8:.6f}", f"相对误差 {abs(slope_M8/slope_num-1)*100:.2f}%"])
    wcsv.writerow(["隐函数定理斜率", f"{slope_exact:.6f}", f"相对误差 {abs(slope_exact/slope_num-1)*100:.2e}%"])
    wcsv.writerow(["数值中心差分", f"{slope_num:.6f}", "基准"])
    for row in rows:
        wcsv.writerow([f"nu（{row['name']}, kappa={row['kappa']:.1f}）", f"{row['nu']:.4f}", "kappa=3 ⇒ n-1"])
    wcsv.writerow(["修正因子 r 的分布离散", f"{spread*100:.2f}%", "对比值敏感 1.5%"])
    wcsv.writerow(["固定交点下 dT p_pair 最大变化", f"{max(pure_d)*100:.1f}%", ">5% ⇒ 峰度通道存在"])
    wcsv.writerow(["固定交点下严格斜率离散", f"{sl_spread*100:.1f}%", "斜率仍依赖形状"])
    wcsv.writerow(["偏读误差范围", f"{min(e for _,_,_,e in slopes)*100:.1f}%–{max(e for _,_,_,e in slopes)*100:.1f}%", "恒等于 1/r-1，系统性高估"])
    wcsv.writerow(["严格恒等式", "slope_M8/slope_exact = 1/r", "数值误差 <1e-9"])
print("摘要已存。")
