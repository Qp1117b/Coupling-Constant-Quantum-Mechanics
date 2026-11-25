# 环 15 / 审-6（第 181 轮）：O(σ²) 非线性修正——λ = ln√(1−ε/2π) 的二阶项
# 结论口径：相对方差修正 = 2σ_ε²/(2π−ε₀)² = σ_θ²/(2π² s²)（用 α=-4πs、σ_ε/(2π−ε₀)=2σ_θ/|α|）
# 等价于把 E_c/k_BT 除以 (1+c)，c = 相对修正 ⇒ 直接复用基准脚本的 y_of/solve_tsync 结构。
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import runpy

BASE = runpy.run_path("环15锁定概率复合_两分支核对.py")
PC = BASE["PC"]; EC = BASE["EC"]; TC = BASE["TC"]
p_pair = BASE["p_pair"]

A_WP = 3.802960                     # 工作点 a = Φ^-1(1-y/2)
SIG2_WP = np.pi ** 2 / (2.0 * A_WP ** 2)   # σ_θ² = (π/(√2 a))²
SIG2_BKT = 0.89294                  # β_KT 上界（σ_θ² ≤ β_KT）

def corr(sig2, s):
    return sig2 / (2.0 * np.pi ** 2 * s ** 2)

def t_sync(sig2, s, m):
    c = corr(sig2, s)
    ece = EC / (1.0 + c)
    y = lambda t: 0.0 if t <= 0 else 2.0 * np.pi * np.exp(-ece / t)
    f = lambda t: p_pair(t) * (1.0 - y(t)) ** m - PC
    return brentq(f, TC, 1.5, xtol=1e-12)

rows = []
for s in (0.5, 1.0, 2.0, 4.0):
    c_wp = corr(SIG2_WP, s); c_b = corr(SIG2_BKT, s)
    ece = EC / (1.0 + c_wp)
    y_tc = 2.0 * np.pi * np.exp(-ece / TC)
    y0 = 2.0 * np.pi * np.exp(-EC / TC)
    rows.append(dict(s=s, alpha=-4 * np.pi * s, c_at_wp=c_wp, c_at_bkt=c_b,
                     y_Tc=y_tc, y_Tc_ratio=y_tc / y0,
                     T_sync_m1=t_sync(SIG2_WP, s, 1), T_sync_m2=t_sync(SIG2_WP, s, 2),
                     T_sync_m1_bkt=t_sync(SIG2_BKT, s, 1)))

T1_0 = BASE["out"]["T_sync_m1"]; T2_0 = BASE["out"]["T_sync_m2"]
out = dict(sigma2_wp=SIG2_WP, sigma2_bkt=SIG2_BKT, EC=EC, a_wp=A_WP,
           y_Tc_linear=2.0 * np.pi * np.exp(-EC / TC),
           T_sync_m1_linear=T1_0, T_sync_m2_linear=T2_0, rows=rows)

with open("环15锁定概率_非线性修正.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
ax = axes[0]
ss = np.linspace(0.5, 4.0, 200)
ax.plot(ss, [corr(SIG2_WP, x) for x in ss], label="σ_θ²@wp")
ax.plot(ss, [corr(SIG2_BKT, x) for x in ss], "--", label="σ_θ²≤β_KT")
ax.set(xlabel="|s| (θ=αλ, α=-4πs)", ylabel="相对方差修正 c", title="(a) O(σ²) 修正随 s 缩小")
ax.legend(fontsize=8); ax.set_yscale("log")
ax = axes[1]
ax.plot([r["s"] for r in rows], [r["T_sync_m1"] for r in rows], "o-", label="T_sync m=1")
ax.plot([r["s"] for r in rows], [r["T_sync_m2"] for r in rows], "s--", label="T_sync m=2")
ax.axhline(T1_0, color="C0", ls=":", alpha=0.6); ax.axhline(T2_0, color="C1", ls=":", alpha=0.6)
ax.set(xlabel="|s|", ylabel="T_sync", title="(b) 非线性修正后的同步温度（虚线=线性基线）")
ax.legend(fontsize=8)
fig.tight_layout(); fig.savefig("环15锁定概率_非线性修正.png", dpi=130)

for r in rows:
    print("s=%.1f  c_wp=%.4f  c_bkt=%.4f  y_Tc/y0=%.2f  T1=%.6f (%.6f)  T2=%.6f (%.6f)"
          % (r["s"], r["c_at_wp"], r["c_at_bkt"], r["y_Tc_ratio"],
             r["T_sync_m1"], T1_0, r["T_sync_m2"], T2_0))
print("sigma2_wp=%.6f  sigma2_bkt=%.4f" % (SIG2_WP, SIG2_BKT))
print("图片: 环15锁定概率_非线性修正.png")
