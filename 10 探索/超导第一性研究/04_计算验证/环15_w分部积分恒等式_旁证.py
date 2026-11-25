# -*- coding: utf-8 -*-
"""
环15 第 197 轮数值旁证：w 的分部积分恒等式与形状项分解（G-188a）
  恒等式：w(T) = tanh(1/2T) + (T/2) w'(T)
  端点亏损： (T/2)|w'(T)| = tanh(1/2T) - w(T)
  形状项：   w/|w'| = tanh(1/2T)/|w'| - T/2
只做数值一致性核对，不反充第一性输入。
"""
import json
import numpy as np

T_c = 0.3
T_break = 0.7304390
NQ = 20001

def w(T, n=NQ):
    u = np.linspace(0.0, 1.0, n)
    return np.trapezoid(2.0 * u * np.tanh(u / (2.0 * T)), u)

def w_deriv(T, n=NQ):
    u = np.linspace(0.0, 1.0, n)
    return -(1.0 / T ** 2) * np.trapezoid(u ** 2 / np.cosh(u / (2.0 * T)) ** 2, u)

Ts = np.linspace(T_c, T_break, 61)
wv = np.array([w(T) for T in Ts])
dv = np.array([w_deriv(T) for T in Ts])
tv = np.tanh(1.0 / (2.0 * Ts))

lhs_ibp = wv
rhs_ibp = tv + 0.5 * Ts * dv
res_ibp = np.abs(lhs_ibp - rhs_ibp)
deficit = tv - wv
deficit_rhs = 0.5 * Ts * np.abs(dv)
res_def = np.abs(deficit - deficit_rhs)

shape = wv / np.abs(dv)
shape_rhs = tv / np.abs(dv) - 0.5 * Ts
res_shape = np.abs(shape - shape_rhs)

out = {
    "T_c": T_c,
    "T_break": T_break,
    "n_points": int(Ts.size),
    "ibp_resid_max": float(res_ibp.max()),
    "ibp_resid_rel_max": float((res_ibp / np.abs(lhs_ibp)).max()),
    "endpoint_deficit_resid_max": float(res_def.max()),
    "endpoint_deficit_positive_all": bool((deficit > 0).all()),
    "endpoint_deficit_min": float(deficit.min()),
    "endpoint_deficit_max": float(deficit.max()),
    "shape_split_resid_max": float(res_shape.max()),
    "shape_min": float(shape.min()),
    "shape_max": float(shape.max()),
    "shape_at_T_c": float(shape[0]),
    "shape_at_T_break": float(shape[-1]),
    "T_at_shape_min": float(Ts[int(np.argmin(shape))]),
    "w_Tc": float(wv[0]),
    "w_Tcut": float(wv[-1]),
    "tanh_half_Tc": float(tv[0]),
    "tanh_half_Tcut": float(tv[-1]),
}
print(json.dumps({k: (v if k != "endpoint_deficit_min" else out["endpoint_deficit_min"]) for k, v in out.items() if k != "endpoint_deficit_min"}, ensure_ascii=False, indent=2))
with open("环15_w分部积分恒等式_旁证.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["font.family"] = ["Microsoft YaHei", "DejaVu Sans"]
    plt.rcParams["axes.unicode_minus"] = False
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.2))
    ax = axes[0]
    ax.plot(Ts, tv, "b-", lw=2, label="tanh(1/2T)  endpoint")
    ax.plot(Ts, wv, "r--", lw=2, label="w(T)  window average")
    ax.fill_between(Ts, wv, tv, color="gray", alpha=0.25)
    ax.set_xlabel("T")
    ax.set_ylabel("value")
    ax.set_title("(a) endpoint above average: gap = (T/2)|w'|")
    ax.legend(fontsize=9)
    ax2 = axes[1]
    ax2.semilogy(Ts, res_ibp + 1e-18, "k-", lw=2, label="Ibp residual")
    ax2.semilogy(Ts, res_def + 1e-18, "g--", lw=2, label="End-deficit residual")
    ax2.semilogy(Ts, res_shape + 1e-18, "m:", lw=2, label="Shape-split residual")
    ax2.set_xlabel("T")
    ax2.set_ylabel("residual")
    ax2.set_title("(b) three identities, residual")
    ax2.legend(fontsize=9)
    ax3 = axes[2]
    ax3.plot(Ts, shape, "g-", lw=2, label="w/|w'|")
    ax3.plot(Ts, tv / np.abs(dv), "b--", lw=1.5, label="tanh(1/2T)/|w'|")
    ax3.plot(Ts, 0.5 * Ts, "k:", lw=1.5, label="T/2 offset")
    ax3.set_xlabel("T")
    ax3.set_ylabel("shape factor")
    ax3.set_title("(c) shape = endpoint/|w'| - T/2")
    ax3.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig("环15_w分部积分恒等式_旁证.png", dpi=150)
    print("png written")
except Exception as e:
    print("plot skipped:", e)
