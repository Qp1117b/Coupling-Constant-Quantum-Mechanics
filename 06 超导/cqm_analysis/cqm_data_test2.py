"""第二层检验：拆解混淆变量 + 检验真正可用的一阶信号。

关键混淆：高压(氢化物) vs 常压；元素数(化合物复杂度) vs 中子数。
方法仍是 Spearman 与分层，不做多参数拟合。
"""
import statistics
from cqm_data_test import (load_materials, material_features, spearman)

rows = load_materials()
data = [(r, material_features(r["formula"])) for r in rows]
data = [(r, f) for r, f in data if f]


def hi_pressure(r):
    return "高压" in r["cond"]


print("=== 1) 高压 vs 常压 完全分层 ===")
for label, sel in [("常压", lambda r: not hi_pressure(r)),
                   ("高压", lambda r: hi_pressure(r))]:
    sub = [(r, f) for r, f in data if sel(r)]
    print(" -- %s n=%d, Tc中位=%.1fK" % (label, len(sub), statistics.median(r["tc"] for r, _ in sub)))
    for key in ["N", "Z", "delta", "deform", "n_elem", "frac_A1"]:
        rho, _ = spearman([f[key] for _, f in sub], [r["tc"] for r, _ in sub])
        print("      rho(Tc,%-10s)=%+.3f" % (key, rho))
    print()

print("=== 2) 氢化物单独剔除后，常压常规材料的 N 效应 ===")
sub = [(r, f) for r, f in data if not hi_pressure(r) and "常规" in r["mech"] and "H" not in f["comp"]]
rho, n = spearman([f["N"] for _, f in sub], [r["tc"] for r, _ in sub])
print("   n=%d  rho(Tc,N)=%+.3f  Tc range [%.1f,%.1f]"
      % (n, rho, min(r["tc"] for r, _ in sub), max(r["tc"] for r, _ in sub)))

print()
print("=== 3) 元素数 n_elem 是不是真信号？按类别分层 ===")
for cat in sorted(set(r["cat"] for r, _ in data)):
    sub = [(r, f) for r, f in data if r["cat"] == cat]
    if len(sub) < 6:
        continue
    rho, _ = spearman([f["n_elem"] for _, f in sub], [r["tc"] for r, _ in sub])
    med = statistics.median(r["tc"] for r, _ in sub)
    print("  %-26s n=%3d rho(Tc,n_elem)=%+.3f Tc中位=%6.1fK" % (cat[:26], len(sub), rho, med))

print()
print("=== 4) 中子数N与原子序数Z高度共线 -> 检查 N/Z ===")
rho, _ = spearman([f["N"] for _, f in data], [f["Z"] for _, f in data])
print("   rho(N,Z)=%+.3f  (近1说明N/Z难分离，§11.9的'N效应'可能是Z/周期表效应)" % rho)

print()
print("=== 5) 关键反例检验：轻元素 vs 重元素的高Tc ===")
# 常规超导中的高Tc(>15K)与低Tc(<5K)的N中位数
for lab, cond in [("常规 Tc>15K", lambda r: "常规" in r["mech"] and r["tc"] > 15),
                  ("常规 Tc<5K", lambda r: "常规" in r["mech"] and r["tc"] < 5)]:
    sub = [(r, f) for r, f in data if cond(r) and not hi_pressure(r)]
    if sub:
        print("  %-14s n=%3d  N中位=%.1f  delta中位=%.4f  n_elem中位=%.1f"
              % (lab, len(sub), statistics.median(f["N"] for _, f in sub),
                 statistics.median(f["delta"] for _, f in sub),
                 statistics.median(f["n_elem"] for _, f in sub)))

print()
print("=== 6) 发现年份 -> Tc (CQM 无此命题，作为数据质量/选择偏差检查) ===")
sub = [(r, f) for r, f in data if r["year"].isdigit()]
rho, _ = spearman([int(r["year"]) for r, _ in sub], [r["tc"] for r, _ in sub])
print("   rho(Tc,year)=%+.3f  (n=%d)" % (rho, len(sub)))
