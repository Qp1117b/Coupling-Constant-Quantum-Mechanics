# 环15_t两通道反号_旁证.py（第 194 轮）
# 目的：核对 Lean 已证的两件事在实际工作点上的形态——(i) t 对 p 严格增（p 通道压低 t）；
#       (ii) 复合增量 = y 通道项(>0) + p 通道项(<0) 的反号分解；看哪一项主导。
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

M = 1.0
# 同步点：p_pair*(1-y)^m = p_c
T_SYNC = float(brentq(lambda T: p_pair(T) * (1.0 - y_of(T)) ** M - PC, TC, T_BREAK - 1e-6, xtol=1e-14))

out = {
    "T_c": TC,
    "T_sync_m1": T_SYNC,
    "T_break": T_BREAK,
    "m": M,
    "y_Tc": y_of(TC),
    "p_Tc": p_pair(TC),
    "t_Tc": t_of(TC, M),
    "y_sync": y_of(T_SYNC),
    "p_sync": p_pair(T_SYNC),
    "t_sync": t_of(T_SYNC, M),
}

Ts = np.linspace(TC, T_SYNC, 201)
yT = np.array([y_of(float(T)) for T in Ts])
pT = np.array([p_pair(float(T)) for T in Ts])
tT = np.array([t_of(float(T), M) for T in Ts])

# 单调方向核对
out["y_strict_increasing_on_grid"] = bool(np.all(np.diff(yT) > 0))
out["p_strict_decreasing_on_grid"] = bool(np.all(np.diff(pT) < 0))
out["t_strict_increasing_on_grid"] = bool(np.all(np.diff(tT) > 0))

# 反号分解：Δ = m[(L2-L1)ln p1 + L1 (ln p1 - ln p2)] / (ln p1 ln p2)
L = np.log(1.0 - yT)
lq = np.log(pT)
d1 = np.diff(L) * lq[:-1]                      # y 通道项（>0）
d2 = L[:-1] * (lq[:-1] - lq[1:])               # p 通道项（<0）
den = lq[:-1] * lq[1:]
dT = M * (d1 + d2) / den
out["y_channel_positive_all"] = bool(np.all(d1 > 0))
out["p_channel_negative_all"] = bool(np.all(d2 < 0))
out["delta_t_positive_all"] = bool(np.all(dT > 0))
out["min_abs_ratio_p_over_y"] = float(np.min(np.abs(d2) / d1))
out["mean_abs_ratio_p_over_y"] = float(np.mean(np.abs(d2) / d1))
out["max_abs_ratio_p_over_y"] = float(np.max(np.abs(d2) / d1))
out["t_total_increase"] = float(tT[-1] - tT[0])
out["note"] = ("t 的上升全部来自 y 通道；p 通道全程反号抵消一部分，"
               "故不能由两条单调性直接复合出 t 随 T 严格增，须主导项比较（G-186c）。")

# ---- 图 ----
fig, ax = plt.subplots(1, 3, figsize=(15.5, 4.4))
ax[0].plot(Ts, tT, "C0-", lw=2, label=r"$t(T)$  m=1")
ax[0].axhline(1.0, color="k", ls=":", lw=1)
ax[0].set_xlabel("T"); ax[0].set_ylabel(r"$t$")
ax[0].set_title("(a) 复合后 $t$ 仍严格增")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.3)

ax[1].semilogy(Ts[1:], np.abs(d1), "C2-", lw=1.8, label=r"y 通道项 $>0$")
ax[1].semilogy(Ts[1:], np.abs(d2), "C3-", lw=1.8, label=r"p 通道项 $<0$（取绝对值）")
ax[1].set_xlabel("T"); ax[1].set_ylabel("项的量级")
ax[1].set_title("(b) 两通道反号、量级对比")
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.3)

ax[2].plot(Ts[1:], dT, "C0-", lw=1.8)
ax[2].axhline(0.0, color="C3", ls=":", lw=1)
ax[2].set_xlabel("T"); ax[2].set_ylabel(r"$\Delta t$（相邻格点）")
ax[2].set_title("(c) 复合增量全程为正")
ax[2].grid(alpha=0.3)

fig.suptitle("环 15：$t$ 的两条通道方向相反（第 194 轮旁证）")
fig.tight_layout()
fig.savefig("环15_t两通道反号_旁证.png", dpi=160)

with open("环15_t两通道反号_旁证.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(json.dumps(out, ensure_ascii=False, indent=2))
