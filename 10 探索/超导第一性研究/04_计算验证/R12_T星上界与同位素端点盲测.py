# -*- coding: utf-8 -*-
"""预注册判定 R12：T* 上界与同位素端点盲测（第 160 轮）

严格按 07_数据与现象/预注册判定_R12.md 的判据跑数；无拟合、无反解、不挑子集。
运行：python "R12_T星上界与同位素端点盲测.py"（本目录）
输出：R12_T星上界与同位素端点盲测.png / .json
"""
import csv
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BASE = Path("..") / "07_数据与现象"
ELEM = BASE / "实验数据_元素.csv"
IND = BASE / "数据" / "独立参数集_第一性Eliashberg.csv"

PREF = 1.13 * np.exp(-1.0 / 6.0)     # 0.95653


def tstar(lam, wlog):
    return PREF * wlog * np.exp(-(1.0 + lam) / lam)


def read_csv(path):
    rows = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or not line.strip():
                continue
            rows.append(line.rstrip("\n").split(","))
    return rows[0], rows[1:]


checks = {}

# ---- P1 同位素端点（A 类） ----
hdr, data = read_csv(ELEM)
alpha_col = hdr.index("alpha_measured")
alphas = []
for r in data:
    v = r[alpha_col].strip()
    if v:
        alphas.append((r[0], float(v)))
violations = [(e, a) for e, a in alphas if a < 0 or a > 0.5]
checks["P1_alphas"] = {e: a for e, a in alphas}
checks["P1_violations"] = violations
checks["P1_pass"] = len(violations) == 0

# ---- P2 T* >= Tc（B 类） ----
hdr2, data2 = read_csv(IND)
rows = []
for r in data2:
    try:
        lam = float(r[1])
        wlog_raw = r[3].split("(")[0].strip()
        wlog = float(wlog_raw)
        tc_raw = r[6].strip().replace("~", "")
        tc = float(tc_raw)
    except (ValueError, IndexError):
        continue
    ts = tstar(lam, wlog)
    rows.append((r[0], lam, wlog, tc, ts, ts / tc))
checks["P2_rows"] = [
    {"system": s, "lambda": l, "omega_log_K": w, "Tc_exp_K": tc,
     "Tstar_K": ts, "ratio": ratio}
    for s, l, w, tc, ts, ratio in rows
]
checks["P2_pass"] = all(ts >= tc for _, _, _, tc, ts, _ in rows)

# ---- P3 比值随 lambda 单调减 ----
by_lam = sorted(rows, key=lambda x: x[1])
ratios = [x[5] for x in by_lam]
checks["P3_sorted"] = [(x[0], x[1], x[5]) for x in by_lam]
checks["P3_monotone_decrease"] = bool(all(ratios[i] > ratios[i + 1] for i in range(len(ratios) - 1)))
checks["P3_spearman"] = -1.0 if checks["P3_monotone_decrease"] else None
checks["P3_pass"] = checks["P3_monotone_decrease"]

# ---- P4 端点登记（不判） ----
checks["P4_endpoint_count"] = sum(1 for _, a in alphas if abs(a - 0.5) < 1e-9)
checks["P4_MgB2_alpha_external"] = 0.3

# ---------------- 图像 ----------------
fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

ax = axes[0]
names = [e for e, _ in alphas]
vals = [a for _, a in alphas]
ax.bar(names, vals, color=["tab:red" if (a < 0 or a > 0.5) else "tab:blue" for a in vals])
ax.axhline(0.5, color="k", ls="--", label="链内上界 0.5")
ax.set(ylabel="alpha", title="(P1) 同位素端点")
ax.legend(fontsize=8)

ax = axes[1]
labels = [x[0] for x in rows]
tcv = [x[3] for x in rows]
tsv = [x[4] for x in rows]
xpos = np.arange(len(labels))
ax.bar(xpos - 0.2, tcv, 0.4, label="Tc_exp")
ax.bar(xpos + 0.2, tsv, 0.4, label="T*_chain")
ax.set_xticks(xpos)
ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
ax.set(ylabel="K", title="(P2) T* >= Tc")
ax.legend(fontsize=8)

ax = axes[2]
ax.plot([x[1] for x in by_lam], ratios, "o-")
ax.set(xlabel="lambda", ylabel="T*/Tc", title="(P3) 余量随耦合收窄")

fig.tight_layout()
fig.savefig("R12_T星上界与同位素端点盲测.png", dpi=150)
with open("R12_T星上界与同位素端点盲测.json", "w", encoding="utf-8") as fh:
    json.dump(checks, fh, ensure_ascii=False, indent=2)
print(json.dumps(checks, ensure_ascii=False, indent=2))
