import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

U = np.linspace(0.0, 1.0, 4001)


def wfun(T):
    s = 1.0 / (2.0 * T)
    return 2.0 * np.trapezoid(U * np.tanh(U * s), U)


def wabsd(T):
    s = 1.0 / (2.0 * T)
    return np.trapezoid(U ** 2 * (1.0 / np.cosh(U * s) ** 2), U) / T ** 2


def deriv_old(T):
    s = 1.0 / (2.0 * T)
    h = np.tanh(s)
    w = wfun(T)
    sc2 = 1.0 / np.cosh(s) ** 2
    return (wabsd(T) * h - w * sc2 / (2.0 * T ** 2)) / h ** 2


def deriv_new(T):
    s = 1.0 / (2.0 * T)
    h = np.tanh(s)
    w = wfun(T)
    sc2 = 1.0 / np.cosh(s) ** 2
    return 2.0 * (h - w) / (T * h) - w * sc2 / (2.0 * T ** 2 * h ** 2)


def delta(T):
    return 1.0 - wfun(T) / np.tanh(1.0 / (2.0 * T))


Tg = np.linspace(0.05, 5.0, 3001)
dn = np.array([deriv_new(t) for t in Tg])
do = np.array([deriv_old(t) for t in Tg])
dv = np.array([(delta(t + 1e-6) - delta(t - 1e-6)) / 2e-6 for t in Tg])

rel = np.abs(dn - do) / np.maximum(np.abs(do), 1e-30)
relfd = np.abs(dn - dv) / np.maximum(np.abs(dv), 1e-30)

ub = 2.0 / (3.0 * Tg)
margin = np.minimum(ub - dn, 2.0 * np.array([delta(t) for t in Tg]) / Tg - dn)

print("=== 第215轮：δ′ 新闭式与上界的数值旁证（反馈层，非定理） ===")
print("T 范围：0.05 .. 5.0（3001 点）")
print("闭式(新) vs 闭式(旧,含|w'|) 最大相对差 = %.3e" % rel.max())
print("闭式(新) vs 中心差分 最大相对差 = %.3e" % relfd.max())
print("δ′ 最大 = %.6f 于 T = %.4f" % (dn.max(), Tg[dn.argmax()]))
print("δ′ 最小 = %.6f 于 T = %.4f" % (dn.min(), Tg[dn.argmin()]))
print("δ′/(2/(3T)) 最大 = %.6f 于 T = %.4f" % ((dn / ub).max(), Tg[(dn / ub).argmax()]))
print("差值上界 2/(3T)-δ′ 最小 = %.6f 于 T = %.4f" % ((ub - dn).min(), Tg[(ub - dn).argmin()]))
print("2δ/T - δ′ 最小 = %.6f 于 T = %.4f" % (margin.min(), Tg[margin.argmin()]))
print("δ′<0 的点数 = %d ; δ′<2/(3T) 不成立的点数 = %d" % ((dn <= 0).sum(), (dn >= ub).sum()))
for t in [0.1, 0.2, 0.5, 1.0, 2.0, 5.0]:
    print("T=%.2f : δ=%.6f, δ′新=%.6f, δ′差分=%.6f, 2δ/T=%.6f, 2/(3T)=%.6f"
          % (t, delta(t), deriv_new(t), (delta(t + 1e-6) - delta(t - 1e-6)) / 2e-6,
             2 * delta(t) / t, 2.0 / (3.0 * t)))

fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))

ax[0].plot(Tg, dn, label="δ′(新闭式)")
ax[0].plot(Tg, dv, "k--", lw=0.8, label="δ′(中心差分)")
ax[0].plot(Tg, 2 * np.array([delta(t) for t in Tg]) / Tg, "g:", label="2δ/T")
ax[0].set_xlabel("T")
ax[0].set_title("(a) δ′ 与 2δ/T 上界")
ax[0].legend()
ax[0].grid(alpha=0.3)

ax[1].semilogy(Tg, rel, label="新闭式 vs 旧闭式")
ax[1].semilogy(Tg, relfd, label="新闭式 vs 差分")
ax[1].set_xlabel("T")
ax[1].set_ylabel("相对差")
ax[1].set_title("(b) 闭式一致性（对数轴）")
ax[1].legend()
ax[1].grid(alpha=0.3)

ax[2].plot(Tg, dn / ub, label="δ′ / (2/(3T))")
ax[2].axhline(1.0, color="r", ls="--", lw=0.9)
ax[2].set_xlabel("T")
ax[2].set_ylim(0.0, 1.05)
ax[2].set_title("(c) 上界 2/(3T) 的余量")
ax[2].legend()
ax[2].grid(alpha=0.3)

fig.tight_layout()
fig.savefig("环15_δ上界_数值旁证.png", dpi=150)
print("图已写出：环15_δ上界_数值旁证.png")
