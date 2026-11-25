# 环15 w 严格性沿链传递的数值旁证（第 193 轮）
# 只作旁证：核对 K(T) 严格减、y(T) 严格增、t(T)（p 固定）严格增，
# 与 192/185 的登记值对齐。不参与建模，不反充输入。

import json
import math

import numpy as np

TC = 0.3
UPS0 = 0.649917      # = 2*E_c/pi^2，乙类（仅下界 0.442819 已证）
UPC = 3.207211
PC = 0.592746
Y_CRIT = 0.025007
P_PAIR_TC = 0.875539   # 登记值：T_c 处 p_pair（m=1 口径），仅作固定 p 的数值示例


def w_of_T(T):
    u = np.linspace(0.0, 1.0, 400001)
    return float(np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u))


def K_of_T(T):
    return UPS0 * w_of_T(T) / T


def y_of_K(K):
    return 2.0 * math.pi * math.exp(-(math.pi ** 2) * K / 2.0)


def t_of_y(p, y, m=1):
    return 1.0 + m * math.log(1.0 - y) / math.log(p)


Ts = np.round(np.arange(0.30, 0.3861, 0.0005), 6)
K = np.array([K_of_T(float(T)) for T in Ts])
Y = np.array([y_of_K(float(k)) for k in K])
Tt = np.array([t_of_y(P_PAIR_TC, float(y)) for y in Y])

dK = np.diff(K)
dY = np.diff(Y)
dT = np.diff(Tt)

# y 越过 y_crit 的温度（网格内线性插值）
cross = None
for i in range(len(Y) - 1):
    if Y[i] < Y_CRIT <= Y[i + 1]:
        cross = float(Ts[i] + (Y_CRIT - Y[i]) * (Ts[i + 1] - Ts[i]) / (Y[i + 1] - Y[i]))
        break

out = {
    "Tc": TC,
    "Upsilon0": UPS0,
    "w_Tc": w_of_T(TC),
    "K_Tc": float(K[0]),
    "y_Tc": float(Y[0]),
    "t_Tc_p_fixed": float(Tt[0]),
    "grid": [float(Ts[0]), float(Ts[-1]), len(Ts)],
    "K_strict_decreasing_on_grid": bool(np.all(dK < 0)),
    "K_max_step_up": float(dK.max()),
    "y_strict_increasing_on_grid": bool(np.all(dY > 0)),
    "y_min_step_down": float(dY.min()),
    "t_strict_increasing_on_grid_p_fixed": bool(np.all(dT > 0)),
    "t_min_step_down": float(dT.min()),
    "y_cross_y_crit_T": cross,
    "K_end": float(K[-1]),
    "y_end": float(Y[-1]),
    "t_end_p_fixed": float(Tt[-1]),
    "note": "只作旁证：K/y/t 三环方向与 192/185 登记一致；不含 p_pair(T) 通道（G-186p）",
}

with open("环15_w严格性沿链传递_旁证.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

print(json.dumps(out, ensure_ascii=False, indent=2))
