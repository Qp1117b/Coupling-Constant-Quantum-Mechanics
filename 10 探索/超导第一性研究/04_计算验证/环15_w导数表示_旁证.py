# -*- coding: utf-8 -*-
"""
环15 第 196 轮数值旁证：w'(T) 的链内表示（G-190c）
  w(T)          = ∫_0^1 2u tanh(u/(2T)) du
  wGapDeriv(T)  = -(1/T^2) ∫_0^1 u^2 sech^2(u/(2T)) du
核对：中心差分（h=1e-6）对 wGapDeriv 的相对偏差；导数为负；w/|w'| 的形状。
此脚本只做数值一致性核对，不反充第一性输入。
"""
import json
import numpy as np

T_c = 0.3
T_break = 0.7304390

def w(T, n=20001):
    u = np.linspace(0.0, 1.0, n)
    f = 2.0 * u * np.tanh(u / (2.0 * T))
    return np.trapezoid(f, u)

def w_deriv_integral(T, n=20001):
    u = np.linspace(0.0, 1.0, n)
    g = u ** 2 / np.cosh(u / (2.0 * T)) ** 2
    return -(1.0 / T ** 2) * np.trapezoid(g, u)

Ts = np.linspace(T_c, T_break, 61)
h = 1e-5
fd = np.array([(w(T + h) - w(T - h)) / (2 * h) for T in Ts])
an = np.array([w_deriv_integral(T) for T in Ts])
rel = np.abs(fd - an) / np.abs(an)
wv = np.array([w(T) for T in Ts])
ratio = wv / np.abs(an)

out = {
    "T_c": T_c,
    "T_break": T_break,
    "n_points": int(Ts.size),
    "rel_err_max": float(rel.max()),
    "rel_err_mean": float(rel.mean()),
    "deriv_negative_all": bool((an < 0).all()),
    "w_pos_all": bool((wv > 0).all()),
    "w_monotone_decreasing_all": bool((np.diff(wv) < 0).all()),
    "wPrime_abs_min": float(np.abs(an).min()),
    "wPrime_abs_max": float(np.abs(an).max()),
    "wPrime_abs_at_Tc": float(np.abs(an[0])),
    "wPrime_abs_at_Tbreak": float(np.abs(an[-1])),
    "ratio_w_over_absWprime_min": float(ratio.min()),
    "ratio_w_over_absWprime_max": float(ratio.max()),
    "ratio_at_Tc": float(ratio[0]),
    "ratio_at_Tbreak": float(ratio[-1]),
}
print(json.dumps(out, ensure_ascii=False, indent=2))
with open("环15_w导数表示_旁证.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = ["Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    ax = axes[0]
    ax.plot(Ts, np.abs(an), "b-", lw=2, label=r"$|w'(T)|$ (integral formula)")
    ax.plot(Ts, np.abs(fd), "r--", lw=1.5, label=r"$|w'(T)|$ (central difference)")
    ax.set_xlabel("T")
    ax.set_ylabel(r"$|w'|$")
    ax.set_title(r"(a) $w'$ integral vs finite difference")
    ax.legend(fontsize=9)
    ax2 = axes[1]
    ax2.semilogy(Ts, rel, "k-", lw=2)
    ax2.set_xlabel("T")
    ax2.set_ylabel("relative error")
    ax2.set_title("(b) relative error of finite difference")
    ax3 = axes[2]
    ax3.plot(Ts, ratio, "g-", lw=2)
    ax3.set_xlabel("T")
    ax3.set_ylabel(r"$w/|w'|$")
    ax3.set_title(r"(c) shape factor $w/|w'|$")
    fig.tight_layout()
    fig.savefig("环15_w导数表示_旁证.png", dpi=150)
    print("png written")
except Exception as e:  # pragma: no cover
    print("plot skipped:", e)
