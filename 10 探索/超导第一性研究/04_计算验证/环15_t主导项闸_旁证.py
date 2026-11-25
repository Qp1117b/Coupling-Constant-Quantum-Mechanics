# 环15_t主导项闸_旁证.py（第 195 轮）
# 目的：核对 G-186c 的条件式判据在整段工作域上是否成立——
#   判据：Δt>0 ⟺ S := (ln(1-y2)-ln(1-y1))*ln p1 + ln(1-y1)*(ln p1-ln p2) > 0
#   等价的可检查量：ρ := |p 项| / (y 项) < 1（ρ 与 m 无关）。
# 定位：只作 B 闸判定的数值旁证与反馈层显影，不回写第一性输入，不参与建模。
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import chi2
from scipy.optimize import brentq

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

PC = 0.592746
NU = 9.0
TC = 0.3
XC = 4.5
UPS0 = 2.0 * 3.207211 / np.pi ** 2


def w(x, n=40001):
    if x <= 0.0:
        return 1.0
    u = np.linspace(0.0, 1.0, n)
    return float(2.0 * np.trapezoid(u * np.tanh(u / (2.0 * x)), u))


WC = w(TC)
p_pair = lambda T: 1.0 - chi2.cdf(XC * WC / w(T), NU)
y_of = lambda T: 2.0 * np.pi * np.exp(-np.pi ** 2 * (UPS0 * w(T)) / (2.0 * T))
t_of = lambda T, m: 1.0 + m * np.log(1.0 - y_of(T)) / np.log(p_pair(T))

K_BREAK = 2.0 * np.log(2.0 * np.pi) / np.pi ** 2
T_BREAK = float(brentq(lambda T: UPS0 * w(T) / T - K_BREAK, TC, 2.0, xtol=1e-14))
T_END = T_BREAK - 1e-3          # y→1 处 1-y≤0，须留边

Ts = np.linspace(TC, T_END, 401)
yT = np.array([y_of(float(T)) for T in Ts])
pT = np.array([p_pair(float(T)) for T in Ts])

L = np.log(1.0 - yT)
lq = np.log(pT)
d1 = np.diff(L) * lq[:-1]                  # y 通道项（>0）
d2 = L[:-1] * (lq[:-1] - lq[1:])           # p 通道项（<0）
rho = np.abs(d2) / d1                      # 主导项余量指标（与 m 无关）

out = {
    "T_c": TC,
    "T_break": T_BREAK,
    "T_end_used": T_END,
    "m_note": "ρ 与 m 无关（Δt = m·S/N，S 不含 m）；故判据对 m=1,2 同结论",
    "y_criterion_true_all": bool(np.all(rho < 1.0)),
    "rho_min": float(np.min(rho)),
    "rho_mean": float(np.mean(rho)),
    "rho_max": float(np.max(rho)),
    "rho_at_Tc": float(rho[0]),
    "T_at_rho_max": float(Ts[1:][int(np.argmax(rho))]),
    "t_Tc_m1": t_of(TC, 1.0),
    "t_end_m1": t_of(T_END, 1.0),
    "t_Tc_m2": t_of(TC, 2.0),
    "t_end_m2": t_of(T_END, 2.0),
    "t_strict_increasing_m1": bool(np.all(np.diff([t_of(float(T), 1.0) for T in Ts]) > 0)),
    "t_strict_increasing_m2": bool(np.all(np.diff([t_of(float(T), 2.0) for T in Ts]) > 0)),
    "note": ("判据 Δt>0 ⟺ S>0 在工作域 [T_c,T_break) 全程成立，余量 ρ≤max<1；"
             "但这是逐点数值核对，不是链内证明——证明只覆盖'判据本身'（TargetPropTChanCriterion）"
             "与'判据成立即 t 增'（TargetPropTChanDominate）。"),
}

fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.2))
ax[0].plot(Ts[1:], rho, "C3-", lw=1.8)
ax[0].axhline(1.0, color="k", ls=":", lw=1, label="失效线 ρ=1")
ax[0].set_xlabel("T"); ax[0].set_ylabel("ρ = |p 项| / y 项")
ax[0].set_title("(a) 主导项余量：全域 $\\rho<1$")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)
ax[1].plot(Ts, [t_of(float(T), 1.0) for T in Ts], "C0-", lw=2, label="m=1")
ax[1].plot(Ts, [t_of(float(T), 2.0) for T in Ts], "C2--", lw=1.6, label="m=2")
ax[1].set_xlabel("T"); ax[1].set_ylabel(r"$t$")
ax[1].set_title("(b) 两通道复合后的 $t(T)$")
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)
fig.suptitle("环 15：G-186c 的主导项闸（第 195 轮旁证）")
fig.tight_layout()
fig.savefig("环15_t主导项闸_旁证.png", dpi=160)

with open("环15_t主导项闸_旁证.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
