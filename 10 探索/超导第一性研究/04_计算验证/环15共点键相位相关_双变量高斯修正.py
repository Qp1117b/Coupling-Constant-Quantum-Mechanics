# -*- coding: utf-8 -*-
"""
环 15 / 审-6 第五段（第 176 轮）：共点两键的相位差相关 -> 锁定/失锁概率的修正因子
题目来源：第 173 轮暴露的"条件'给定键已存在'的链内来源"缺口。

第一性依据（链内、无新假设）：
  顶点相位独立、等方差 v（链内登记 σ_θ² = k_B T / Υ0，第 161 轮）
  X := θ_i - θ_j, Y := θ_j - θ_k
  Var X = Var Y = 2v, Cov(X,Y) = -Var(θ_j) = -v  =>  ρ = -1/2   （与 v 无关）
于是"两键同时锁定/同时失锁"的概率不等于边际乘积，修正因子可算：

  C_lock(a)   = P(|X|<θ_c, |Y|<θ_c) / P(|X|<θ_c)^2
  C_unlock(a) = P(|X|>θ_c, |Y|>θ_c) / P(|X|>θ_c)^2 ,  a := θ_c / sqrt(2v)

只做函数图像与符号读数，不拟合任何数据。
运行：python "环15共点键相位相关_双变量高斯修正.py"
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.integrate import quad

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
RHO = -0.5
S = float(np.sqrt(1.0 - RHO ** 2))


def _inner(x, a, sign):
    """给定 X=x 时，P(sign*Y < a) 的标准化自变量。"""
    return (sign * a - RHO * x) / S


def box(a):
    """P(|X|<a, |Y|<a)：对 X 做一维积分，避免二维 cdf 的抵消误差。"""
    f = lambda x: norm.pdf(x) * (norm.cdf(_inner(x, a, 1)) - norm.cdf(_inner(x, a, -1)))
    return float(quad(f, -a, a, limit=200)[0])


def both_out(a):
    """P(|X|>a, |Y|>a)：同号角 + 异号角（交换对称）。"""
    f1 = lambda x: norm.pdf(x) * norm.cdf(_inner(x, a, -1))   # Y < -a
    f2 = lambda x: norm.pdf(x) * (1.0 - norm.cdf(_inner(x, a, 1)))  # Y > a
    return float(2.0 * quad(f1, a, np.inf, limit=200)[0]
                 + 2.0 * quad(f2, a, np.inf, limit=200)[0])


A = np.linspace(0.2, 4.0, 200)
CL, CU = [], []
for a in A:
    p_in = 2.0 * norm.cdf(a) - 1.0          # P(|X|<a)
    p_out = 1.0 - p_in                       # P(|X|>a)
    CL.append(box(a) / p_in ** 2)
    CU.append(both_out(a) / p_out ** 2)
CL = np.array(CL)
CU = np.array(CU)

sel = [0.5, 1.0, 1.5, 2.0, 3.0]
rows = [{"a": a, "C_lock": float(box(a) / (2 * norm.cdf(a) - 1) ** 2),
         "C_unlock": float(both_out(a) / (1 - (2 * norm.cdf(a) - 1)) ** 2)} for a in sel]

# 工作点：y(Tc)=1.43e-4 为单键失锁概率 => P(|X|>a)=y => a=Phi^{-1}(1-y/2)
Y_WP = 1.4298e-4
A_WP = float(norm.isf(Y_WP / 2.0))
P_IN_WP = 1.0 - Y_WP
C_LOCK_WP = float(box(A_WP) / P_IN_WP ** 2)

fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
ax[0].plot(A, CL, "-", color="#1f77b4", lw=2, label=r"$C_{\rm lock}(a)$")
ax[0].axhline(1.0, color="k", ls=":", lw=1.2, label="独立基线 = 1")
ax[0].set(xlabel=r"$a=\theta_c/\sqrt{2v}$", ylabel=r"$C_{\rm lock}$",
          title=r"(a) 同时『锁定』：同类型聚集（$C\geq 1$，工作域偏离极小）")
ax[0].legend(fontsize=8); ax[0].grid(alpha=0.25)

ax[1].plot(A, CU, "-", color="#d62728", lw=2, label=r"$C_{\rm unlock}(a)$")
ax[1].axhline(1.0, color="k", ls=":", lw=1.2, label="独立基线 = 1")
ax[1].set(xlabel=r"$a=\theta_c/\sqrt{2v}$", ylabel=r"$C_{\rm unlock}$",
          title=r"(b) 同时『失锁』：$C_{\rm unlock}>1$（正聚集）")
ax[1].legend(fontsize=8); ax[1].grid(alpha=0.25)

fig.suptitle(r"$\rho=-1/2$：同类型事件（都锁/都失锁）被抬高，混合态被压低", fontsize=11)
fig.tight_layout()
out_png = os.path.join(HERE, "环15共点键相位相关_双变量高斯修正.png")
fig.savefig(out_png, dpi=150)
plt.close(fig)

data = {
    "round": 176,
    "rho": RHO,
    "note": "算术核与概率修正；theta_c 未从第 161 轮取，故只给函数与符号，不给单点物理数值",
    "C_lock_range": [float(CL.min()), float(CL.max())],
    "C_unlock_range": [float(CU.min()), float(CU.max())],
    "C_lock_all_below_one": bool(np.all(CL < 1.0)),
    "C_unlock_all_above_one": bool(np.all(CU > 1.0)),
    "workpoint": {"y": Y_WP, "a": A_WP, "C_lock_at_workpoint": C_LOCK_WP,
                  "p_lock_bias_rel": C_LOCK_WP - 1.0},
    "table": rows,
    "verdict": ("rho=-1/2 => |X|,|Y| 正关联：都锁与都失锁均被抬高、混合态被压低。"
                "但工作点 y=1.43e-4 => a≈3.80 => C_lock-1≈1e-6 量级，故 (1-y)^m 的独立假设"
                "在链内工作域内数值影响可忽略；独立性仍是未经链内证明的假设，未闭合。"),
}
with open(os.path.join(HERE, "环15共点键相位相关_双变量高斯修正.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print(json.dumps(data, ensure_ascii=False, indent=2))
print("图片:", out_png)
