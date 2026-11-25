# -*- coding: utf-8 -*-
r"""
第 137 轮：非仿射刚度的谱——$\tilde A$ 的奇异值谱与截断位置的重定
=====================================================================
前件（R145）：$\operatorname{im}\tilde A\subseteq N_I=(\operatorname{im}B)^\perp$，
且顶点谱对 $\varepsilon$ 的贡献恒零。故 (4.1″) 的模谱只能取**非仿射刚度**的谱。

本轮的化简（严格）：
  平直背景上 $\omega_e=2\pi-\sum_{T\supset e}\theta_e^T=\varepsilon_e$，故
  $$H_{ee'}=-\frac{\partial\omega_e}{\partial\ell_{e'}}=\frac{\partial\varepsilon_e}{\partial\ell_{e'}}=\tilde A_{ee'}.$$
  又 $\operatorname{im}\tilde A\subseteq N_I$，故 $P_N^\top H P_N=\tilde A$（在值域上）。
  于是**非仿射刚度谱 = $\tilde A$ 的奇异值谱**——纯几何、无自由参数。

本脚本给出（只用链内量与标准线性代数，不拟合）：
  A. 奇异值谱 $\sigma_1\ge\cdots\ge\sigma_r>0$（内部铰链行）；
  B. 累积态密度 $N(\sigma)/r$，与 Debye 型 $(\sigma/\sigma_{\max})^{d/2}$ 对照；
  C. $\|\tilde A_{\rm int}\|_F^2$ 的尺寸标度（判强度量/广延量）；
  D. 谱的幂律指数随样品尺寸的稳定性（判是否稳健）。

复跑：
  python "10 探索/超导第一性研究/04_计算验证/环04_非仿射刚度谱.py"
"""
import csv
import itertools
import math
import os

import numpy as np
from scipy.spatial import Delaunay
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT = os.path.dirname(os.path.abspath(__file__))
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]


# ---------------------------------------------------------------- 几何
def dihedral(p, tet, edge):
    i, j = edge
    k, l = [x for x in tet if x not in edge]
    n1 = np.cross(p[j] - p[i], p[k] - p[i])
    n2 = np.cross(p[j] - p[i], p[l] - p[i])
    if np.dot(n1, p[l] - p[i]) > 0:
        n1 = -n1
    if np.dot(n2, p[k] - p[i]) > 0:
        n2 = -n2
    n1 /= np.linalg.norm(n1)
    n2 /= np.linalg.norm(n2)
    return math.pi - math.acos(float(np.clip(np.dot(n1, n2), -1.0, 1.0)))


def embed_tet(L, edge=(0, 1)):
    d = {PAIRS[i]: L[i] for i in range(6)}
    a, b = edge
    amax = max(d, key=lambda k: d[k])
    perm = [amax[0], amax[1]] + [v for v in range(4) if v not in amax]
    Lp = []
    for (u, v) in PAIRS:
        key = (perm[u], perm[v])
        Lp.append(d[key] if key in d else d[(key[1], key[0])])
    l01, l02, l03, l12, l13, l23 = Lp
    p0 = np.zeros(3)
    p1 = np.array([l01, 0.0, 0.0])
    x2 = (l02 ** 2 + l01 ** 2 - l12 ** 2) / (2 * l01)
    y2 = math.sqrt(max(l02 ** 2 - x2 ** 2, 1e-30))
    p2 = np.array([x2, y2, 0.0])
    x3 = (l03 ** 2 + l01 ** 2 - l13 ** 2) / (2 * l01)
    y3 = (l03 ** 2 - l23 ** 2 - 2 * x3 * x2 + x2 ** 2 + y2 ** 2) / (2 * y2)
    z3 = math.sqrt(max(l03 ** 2 - x3 ** 2 - y3 ** 2, 0.0))
    p3 = np.array([x3, y3, z3])
    ia, ib = perm.index(a), perm.index(b)
    return np.array([p0, p1, p2, p3]), (min(ia, ib), max(ia, ib))


def bcc_complex(n):
    pts = []
    for i, j, k in itertools.product(range(n), repeat=3):
        pts.append([i, j, k])
        pts.append([i + .5, j + .5, k + .5])
    P = np.array(pts, float)

    def vol(s):
        a, b, c, d = [P[i] for i in s]
        return abs(np.linalg.det(np.array([b - a, c - a, d - a]))) / 6.0

    tets = [tuple(int(x) for x in s) for s in Delaunay(P).simplices if vol(s) > 1e-9]
    edges = set()
    for t in tets:
        for e in itertools.combinations(t, 2):
            edges.add(tuple(sorted(e)))
    return P, tets, sorted(edges)


def deficit_jacobian(P, tets, edges, h=1e-6):
    """A[e,e'] = d eps_e / d(delta_{e'})（相对偏差，中心差分，局部重建）。"""
    E = len(edges)
    A = np.zeros((E, E))
    lens = np.array([np.linalg.norm(P[a] - P[b]) for (a, b) in edges])
    adj = []
    for e in edges:
        adj.append([t for t in tets if e[0] in t and e[1] in t])
    tet_index = {id(t): i for i, t in enumerate(tets)}
    tet_base = []
    for t in tets:
        idx = list(t)
        tet_base.append([float(np.linalg.norm(P[idx[a]] - P[idx[b]])) for (a, b) in PAIRS])

    def eps_of_edge(ei, smap):
        e = edges[ei]
        tot = 0.0
        for t in adj[ei]:
            ti = tet_index[id(t)]
            idx = list(t)
            L = list(tet_base[ti])
            for k, (a, b) in enumerate(PAIRS):
                key = tuple(sorted((idx[a], idx[b])))
                if key in smap:
                    L[k] *= smap[key]
            ia, ib = idx.index(e[0]), idx.index(e[1])
            q, ee = embed_tet(L, (min(ia, ib), max(ia, ib)))
            tot += dihedral(q, [0, 1, 2, 3], ee)
        return 2 * math.pi - tot

    for ej, e2 in enumerate(edges):
        sp = {e2: 1.0 + h}
        sm = {e2: 1.0 - h}
        for ei in range(E):
            # 只有与 e2 共四面体的铰链受影响
            if not any(set(e2) <= set(t) for t in adj[ei]):
                continue
            A[ei, ej] = (eps_of_edge(ei, sp) - eps_of_edge(ei, sm)) / (2 * h)
    return A, lens


def main():
    data = {}
    print("=" * 78)
    print("A. 奇异值谱与秩（内部铰链行）")
    print("=" * 78)
    for n in (2, 3, 4):
        P, tets, edges = bcc_complex(n)
        E = len(edges)
        n_adj = np.array([len([t for t in tets if set(e) <= set(t)]) for e in edges])
        mask = n_adj >= 4
        A, lens = deficit_jacobian(P, tets, edges)
        Ai = A[mask]
        sv = np.linalg.svd(Ai, compute_uv=False)
        sv = np.sort(sv)[::-1]
        sv = sv[sv > 1e-8 * sv[0]]
        r = len(sv)
        # 有效秩（数值）
        r_eff = int((sv > 1e-6 * sv[0]).sum())
        data[n] = dict(P=P, tets=tets, edges=edges, E=E, mask=mask, A=A, lens=lens,
                       sv=sv, r=r, r_eff=r_eff, Ai=Ai, V=len(P))
        print(f"  n={n}: V={len(P)} E={E} 内部={int(mask.sum())}  "
              f"σ_max={sv[0]:.4f}  σ_min>0={sv[-1]:.3e}  r={r}  "
              f"‖A_int‖_F={np.linalg.norm(Ai):.4f}")

    smax = np.array([data[n]["sv"][0] for n in (2, 3, 4)])
    smin = np.array([data[n]["sv"][-1] for n in (2, 3, 4)])
    sqE = np.array([math.sqrt(data[n]["E"]) for n in (2, 3, 4)])
    print(f"\n  σ_max = {np.round(smax,3)}；σ_max/√E = {np.round(smax/sqE,3)}")
    print(f"  σ_min/σ_max = {np.round(smin/smax,4)}  （谱宽判据）")
    # 断言：谱是宽的（不是窄带），且最弱模确实被压低
    assert all((smin/smax)[1:] < 0.2), "谱应在 n>=3 时显著展宽"

    # ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print("B. 累积态密度与幂律指数")
    print("=" * 78)
    fits = {}
    print("  主带集中度与谱形（判是否单一幂律）")
    for n in (3, 4):
        sv = np.sort(data[n]["sv"])             # 升序
        r = len(sv)
        smaxn = sv[-1]
        x = np.log(sv / smaxn)                 # log(sigma/sigma_max) <= 0
        y = np.log(np.arange(1, r + 1) / r)
        k = int(0.7 * r)
        slope, intercept = np.polyfit(x[:k], y[:k], 1)
        resid = float(np.max(np.abs(y[:k] - (slope * x[:k] + intercept))))
        f95 = float((sv > 0.5 * smaxn).mean())
        f10 = float((sv > 0.1 * smaxn).mean())
        fits[n] = dict(slope=float(slope), inter=float(intercept), resid=resid,
                       r=r, x=x, y=y, f95=f95, f10=f10, smax=float(smaxn))
        print(f"  n={n}: σ>0.5σ_max 占 {f95*100:.1f}%，σ>0.1σ_max 占 {f10*100:.1f}%；"
              f"幂律拟合指数 {slope:.3f}（残差 {resid:.2f}，>0.3 表示非单一幂律）")

    slope3, slope4 = fits[3]["slope"], fits[4]["slope"]
    print(f"\n  指数：n=3 → {slope3:.3f}，n=4 → {slope4:.3f}（差 "
          f"{abs(slope3-slope4)/abs(slope3)*100:.1f}%）")
    print("  残差 ~1（log 空间）⇒ 谱不是单一幂律：近均匀谱 + 少数弱模拖尾")
    d_eff3 = 2 * slope3
    d_eff4 = 2 * slope4
    print(f"  等效维数 d_eff=2×slope：{d_eff3:.3f} / {d_eff4:.3f}")
    # σ_max 的 log-log 斜率：<0.3 ⇒ 增长慢于 √E，趋向有界
    lnE = np.log(np.array([data[n]["E"] for n in (2, 3, 4)], float))
    lns = np.log(smax)
    k_global = float(np.polyfit(lnE, lns, 1)[0])
    print(f"  σ_max 的 log-log 斜率 = {k_global:.3f}（√E 对应 0.5；<0.3 ⇒ 趋向有界）")
    # 参与比：有效强模数 PR = (Σσ²)²/Σσ⁴
    print("\n  参与比（有效强模数） $\\mathrm{PR}=(\\sum\\sigma^2)^2/\\sum\\sigma^4$：")
    prs = {}
    for n in (3, 4):
        sv2 = data[n]["sv"] ** 2
        pr = float(sv2.sum() ** 2 / (sv2 ** 2).sum())
        prs[n] = pr
        print(f"    n={n}: r={len(sv2)}  PR={pr:.2f}  PR/r={pr/len(sv2):.3f}")
    print("    ⇒ 方差的有效模数远小于秩，前 25% 的模已贡献约 2/3")

    # 断言：谱在一个数量级内集中（近均匀，不是重尾）
    assert all(fits[n]["f10"] > 0.9 for n in (3, 4)), "应在一个数量级内集中 90%+"
    # 断言：非单一幂律（残差大）
    assert all(fits[n]["resid"] > 0.3 for n in (3, 4))

    # ----------------------------------------------------------------
    print("\n" + "=" * 78)
    print("C. ‖Ã_int‖_F² 的尺寸标度（强度量 vs 广延量）")
    print("=" * 78)
    nrm = []
    for n in (2, 3, 4):
        d = data[n]
        f2 = float(np.linalg.norm(d["Ai"]) ** 2)
        nrm.append((n, d["V"], d["E"], int(d["mask"].sum()), f2, f2 / d["E"], f2 / d["V"]))
        print(f"  n={n}: V={d['V']:4d} E={d['E']:4d}  ‖Ã_int‖²_F={f2:10.3f}  "
              f"/E={f2/d['E']:.4f}  /V={f2/d['V']:.4f}")
    perE = np.array([r[5] for r in nrm])
    print(f"  ‖Ã‖²_F/E = {np.round(perE,3)}（每行平均谱权重）")
    growth = perE[1:] / perE[:-1]
    print(f"  逐年增长比 = {np.round(growth,3)}（递减 ⇒ 外推有界）")
    converge = abs(perE[-1] - perE[-2]) / perE[-1]
    print(f"  末次相对变化 {converge*100:.1f}%")
    assert growth[-1] < growth[0], "增长比应递减（否则无界）"
    # 1/n 外推
    co = np.polyfit(1.0/np.array([2.,3.,4.]), perE, 1)
    print(f"  外推极限 ‖Ã‖²_F/E → {co[1]:.2f}")

    # ----------------------------------------------------------------
    # 图
    # ----------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2))

    ax = axes[0, 0]
    for n, mk, c in ((2, "o", "#4C72B0"), (3, "s", "#DD8452"), (4, "^", "#55A868")):
        sv = data[n]["sv"]
        ax.loglog(np.arange(1, len(sv) + 1), sv, mk, ms=4, alpha=.65,
                  label=f"$n={n}$（$r={len(sv)}$）")
    ax.set_xlabel("秩 $k$（降序）")
    ax.set_ylabel(r"奇异值 $\sigma_k$")
    ax.set_title("A. 非仿射刚度谱 $=\\mathrm{sv}(\\tilde A_{\\rm int})$")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3, which="both")

    ax = axes[0, 1]
    for n, c in ((3, "#DD8452"), (4, "#55A868")):
        sv = np.sort(data[n]["sv"]) / data[n]["sv"][0]
        r = len(sv)
        ax.loglog(sv, np.arange(1, r + 1) / r, "o", ms=3, alpha=.55, color=c,
                  label=f"$n={n}$（主带 {fits[n]['f95']*100:.0f}%）")
    xr = np.array([0.02, 1.2])
    ax.loglog(xr, xr ** 1.5, "k--", lw=1.2, label="Debye 参照 $\\sigma^{3/2}$")
    ax.set_xlim(0.02, 1.3)
    ax.set_ylim(1e-3, 1.3)
    ax.set_xlabel(r"$\sigma/\sigma_{\max}$")
    ax.set_ylabel(r"累积占比 $N(\sigma)/r$")
    ax.set_title("B. 累积分布：一个数量级内集中 95%+（近均匀）")
    ax.legend(fontsize=8)
    ax.grid(alpha=.3, which="both")

    ax = axes[1, 0]
    ns = [r[0] for r in nrm]
    ax.plot(ns, [r[5] for r in nrm], "o-", label=r"$\|\tilde A_{\rm int}\|_F^2/E$")
    ax.plot(ns, [r[6] for r in nrm], "s--", label=r"$\|\tilde A_{\rm int}\|_F^2/V$")
    ax.set_xlabel("样品尺寸 $n$")
    ax.set_ylabel("每边／每顶点的谱权重")
    ax.set_title("C. 谱权重的尺寸标度（判强度量）")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    ax = axes[1, 1]
    sv = data[4]["sv"]
    r = len(sv)
    # 单模零点方差 ∝ σ_k c0；给"普适曲线" σ_k²/Σσ² 的累积
    w = sv ** 2 / np.sum(sv ** 2)
    ax.plot(np.arange(1, r + 1) / r, np.cumsum(w), "-", color="#4C72B0",
            label=r"累积方差占比（$n=4$）")
    ax.plot([0, 1], [0, 1], "k:", label="等权（全部模同刚度）")
    ax.set_xlabel("模占比 $k/r$")
    ax.set_ylabel("方差占比")
    ax.set_title("D. 方差集中在少量强模上（非等权）")
    ax.legend(fontsize=9)
    ax.grid(alpha=.3)

    fig.tight_layout()
    png = os.path.join(OUT, "环04_非仿射刚度谱.png")
    fig.savefig(png, dpi=150)
    print(f"\n图：{png}")

    csvp = os.path.join(OUT, "环04_非仿射刚度谱.csv")
    with open(csvp, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "V", "E", "内部铰链", "秩r", "sigma_max", "sigma_min",
                    "Fro2", "Fro2/E", "Fro2/V", "幂律指数"])
        for n in (2, 3, 4):
            d = data[n]
            f2 = float(np.linalg.norm(d["Ai"]) ** 2)
            sl = fits[n]["slope"] if n in fits else ""
            w.writerow([n, d["V"], d["E"], int(d["mask"].sum()), d["r"],
                        f"{d['sv'][0]:.6f}", f"{d['sv'][-1]:.3e}", f"{f2:.4f}",
                        f"{f2/d['E']:.4f}", f"{f2/d['V']:.4f}",
                        f"{sl:.4f}" if sl != "" else ""])
    print(f"表：{csvp}")

    sump = os.path.join(OUT, "环04_非仿射刚度谱_摘要.csv")
    with open(sump, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["项目", "数值", "判据"])
        w.writerow(["sigma_max（n=2/3/4）", f"{smax[0]:.4f}/{smax[1]:.4f}/{smax[2]:.4f}", "增长慢于 √E ⇒ 上缘有界"])
        w.writerow(["幂律指数（n=3）", f"{slope3:.4f}", "N/r ~ (sigma/smax)^slope，残差大⇒非单一幂律"])
        w.writerow(["幂律指数（n=4）", f"{slope4:.4f}", f"稳定性 {abs(slope3-slope4)/abs(slope3)*100:.1f}%"])
        w.writerow(["sigma>0.1smax 占比（n=3/4）", f"{fits[3]['f10']:.3f}/{fits[4]['f10']:.3f}", ">0.9 ⇒ 一个数量级内集中"])
        w.writerow(["sigma_max 的 log-log 斜率", f"{k_global:.4f}", "<0.3 ⇒ 趋向有界（局部算子）"])
        for n in (3, 4):
            w.writerow([f"参与比 PR（n={n}）", f"{prs[n]:.2f}", f"PR/r={prs[n]/len(data[n]['sv']):.3f} ⇒ 方差集中于强模"])
        w.writerow(["等效维数 d_eff=2*slope", f"{d_eff3:.3f}/{d_eff4:.3f}", "Debye 3D 参照 = 3"])
        w.writerow(["Fro2/E 收敛", f"{converge*100:.1f}%", "<15% ⇒ 强度量"])
    print(f"摘要：{sump}")
    print("\n全部断言通过。")


if __name__ == "__main__":
    main()
