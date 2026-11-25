# -*- coding: utf-8 -*-
"""第 190 轮数值显影：w(T)=2∫₀¹ u tanh(u/(2T)) du 的正性、单调不增、上界 1 与 T→0 的极限。
   仅作定理行为的显影（约束/反馈层），不反充链内输入。"""
import json
import numpy as np
from scipy.integrate import quad

TC = 0.3
WBAR_TC = 0.758705  # 环 19 登记值


def w(T):
    f = lambda u: 2.0 * u * np.tanh(u / (2.0 * T))
    val, err = quad(f, 0.0, 1.0, limit=200)
    return val


Ts = np.linspace(0.02, 1.0, 300)
ws = np.array([w(t) for t in Ts])

# 单调性：逐对比较（数值上的"不增"）
mono = bool(np.all(np.diff(ws) <= 1e-14))
min_gap = float(np.min(-np.diff(ws)))  # 相邻下降量最小值（>0 表示严格减）

w_tc = w(TC)
w_max = float(ws.max())
w_min = float(ws.min())
le_one = bool(w_max <= 1.0 + 1e-12)

# T→0 的极限：w→1（用越来越小的 T 看 1-w 的衰减）
smallT = [1e-1, 1e-2, 1e-3, 1e-4]
lim = []
for t in smallT:
    val = w(t)
    lim.append({"T": t, "w": val, "one_minus_w": 1.0 - val})

# 与 19 层登记值的一致性
dev_tc = abs(w_tc - WBAR_TC)

res = {
    "w_at_Tc": w_tc,
    "w_at_Tc_registered_19": WBAR_TC,
    "dev_at_Tc": dev_tc,
    "w_max_on_grid": w_max,
    "w_min_on_grid": w_min,
    "monotone_nonincreasing_on_grid": mono,
    "min_adjacent_drop": min_gap,
    "w_le_one": le_one,
    "limit_small_T": lim,
    "strict_decrease_numerically": bool(min_gap > 0),
    "grid": {"T_from": float(Ts[0]), "T_to": float(Ts[-1]), "n": int(Ts.size)},
}

with open("环15_w结构_单调与上界.json", "w", encoding="utf-8") as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print(json.dumps(res, ensure_ascii=False, indent=2))
