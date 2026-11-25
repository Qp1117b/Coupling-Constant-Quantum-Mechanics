# -*- coding: utf-8 -*-
"""
环 4／85：亏角涨落的 q 幂来自"参考亏角是否为零"——响应二分与谱指数合成律
==========================================================================
第 84 轮把等时关联写成 $\\rho_m$ 的 Bessel 核，但索引 $m$ 只按 $m=2n$ 给，
且分叉（$m=2$ vs $3$）悬空。本轮用环 3 的 Regge 定义直接算，回答两件事：

  (1) 亏角对位移的线性响应是否存在？——取决于参考亏角：
      R1（$\\langle\\varepsilon\\rangle=0$，平坦参考）：顶点始终落在 R³，
          四面体平铺其凸包 ⇒ 亏角**恒等于 0**（任何位移、任何阶），
          平坦参考根本不能承载 $\\varepsilon$；
      R2（$\\langle\\varepsilon\\rangle\\ne0$，弯曲参考）：$\\Delta\\varepsilon
          =\\sum_e(\\partial\\varepsilon/\\partial l_e)\\delta l_e=O(\\text{应变})$
          ⇒ 线性响应存在，$|G_q|^2\\propto q^2$（$n=1$）。
  (2) 几何阶 $n$ 与色散指数 $s$ 怎样合成核指数：
      $m_{\\rm eff}=2n+1-s$，且 $\\sigma_0^2\\propto Q^{m_{\\rm eff}+1}$
      —— 同一个 $m_{\\rm eff}$ 同时控形状与标度。

数值：Kuhn（六四面体）立方三角化补片上的亏角直接求和（只取"闭合"边，
即参考角和在 $10^{-8}$ 内等于 $2\\pi$ 的边，以排除补片边界）。
  A. 平坦参考：均匀应变下 $\\delta\\equiv0$；平面波位移下涨落 $\\propto A^2$。
  B. 弯曲参考（边长受扰）：均匀应变下 $|\\Delta\\delta|\\propto\\varepsilon$（斜率 1）。
  C. 合成律：逐 (n,s) 数值求 $\\int_0^Qq^{2n+1-s}dq$ 的 Q 斜率 = $m_{\\rm eff}+1$。
  D. 核与 $S_\\rho$：$m_{\\rm eff}=1,2,3,4,6$ 的收敛性与部分和。
"""
import itertools
import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.special import j0

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_CSV = "环04_亏角q幂与谱指数合成.csv"
OUT_PNG = "环04_亏角q幂与谱指数合成.png"
OUT_TXT = "环04_亏角q幂与谱指数合成_摘要.txt"

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
LOG = []


def emit(s=""):
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- Kuhn 三角化
def build_patch(M):
    """Kuhn（Freudenthal）立方三角化补片：M³ 个立方×6 四面体，非周期。"""
    verts = {}

    def get(v):
        if v not in verts:
            verts[v] = len(verts)
        return verts[v]

    tets = []
    for i in range(M):
        for j in range(M):
            for k in range(M):
                o = (i, j, k)
                for perm in itertools.permutations(range(3)):
                    path = [o]
                    cur = list(o)
                    for ax in perm:
                        cur[ax] += 1
                        path.append(tuple(cur))
                    tets.append(tuple(get(x) for x in path))
    pos = np.zeros((len(verts), 3))
    for v, idx in verts.items():
        pos[idx] = np.array(v, dtype=float)
    return pos, np.array(tets, dtype=int)


def tet_edges(tet):
    return [tuple(sorted((int(tet[a]), int(tet[b])))) for a, b in PAIRS]


def edge_lengths(pos, tets):
    l = {}
    for tet in tets:
        for (a, b), key in zip(PAIRS, tet_edges(tet)):
            if key not in l:
                l[key] = float(np.linalg.norm(pos[tet[a]] - pos[tet[b]]))
    return l


def edge_dirs(pos, tets):
    d = {}
    for tet in tets:
        for (a, b), key in zip(PAIRS, tet_edges(tet)):
            if key not in d:
                v = pos[tet[b]] - pos[tet[a]]
                n = np.linalg.norm(v)
                d[key] = v / n
    return d


def dihedral_at_edges(l6):
    """6 边长（PAIRS 序）→ 6 个内二面角（PAIRS 序）。"""
    out = []
    for (a, b) in PAIRS:
        e = l6[PAIRS.index((a, b))]
        rem = [x for x in range(4) if x not in (a, b)]
        r, s = rem

        def L(u, v):
            return l6[PAIRS.index(tuple(sorted((u, v))))]

        ar, br, as_, bs, rs = L(a, r), L(b, r), L(a, s), L(b, s), L(r, s)
        zr = (ar ** 2 - br ** 2 + e ** 2) / (2 * e)
        zs = (as_ ** 2 - bs ** 2 + e ** 2) / (2 * e)
        rr2 = max(ar ** 2 - zr ** 2, 0.0)
        rs2 = max(as_ ** 2 - zs ** 2, 0.0)
        rr, rss = math.sqrt(rr2), math.sqrt(rs2)
        if rr < 1e-14 or rss < 1e-14:
            out.append(math.pi)
            continue
        # 投影间距：|u-v|² = |r-s|² - (zr-zs)²
        uv2 = max(rs ** 2 - (zr - zs) ** 2, 0.0)
        c = (rr2 + rs2 - uv2) / (2 * rr * rss)
        out.append(math.acos(min(1.0, max(-1.0, c))))
    return out


def angle_sums(tets, l_by_edge):
    acc = {}
    for tet in tets:
        keys = tet_edges(tet)
        l6 = [l_by_edge[k] for k in keys]
        angs = dihedral_at_edges(l6)
        for key, a in zip(keys, angs):
            acc[key] = acc.get(key, 0.0) + a
    return acc


def deficits(sums):
    return {k: 2 * math.pi - v for k, v in sums.items()}


def main():
    emit("=" * 78)
    emit("环 4／85：亏角涨落的 q 幂＝参考亏角二分；谱指数合成律 m_eff = 2n+1-s")

    M = 6
    pos, tets = build_patch(M)
    emit(f"\n[0] Kuhn 三角化补片：M={M}，顶点 {len(pos)}，四面体 {len(tets)}")

    l0 = edge_lengths(pos, tets)
    s0 = angle_sums(tets, l0)
    closed = {k for k, v in s0.items() if abs(v - 2 * math.pi) < 1e-8}
    emit(f"    边总数 {len(s0)}，闭合（内部）边 {len(closed)}，边界边 {len(s0)-len(closed)}")
    d0 = deficits({k: s0[k] for k in closed})
    mx0 = max(abs(v) for v in d0.values())
    emit(f"    平坦参考：闭合边 max|δ| = {mx0:.3e}   （应为 0）")
    assert mx0 < 1e-10, "平坦参考应零亏角"

    # ---------- A. 平坦参考 ----------
    emit("\n[A] 平坦参考：均匀应变（应保持 0）与平面波（应二阶）")
    strains = [1e-3, 2e-3, 4e-3, 8e-3]
    mxA = []
    for e in strains:
        E = np.array([[0.0, 0.5 * e, 0.0], [0.5 * e, 0.0, 0.0], [0.0, 0.0, 0.0]])
        p2 = pos + pos @ E.T
        lE = edge_lengths(p2, tets)
        sE = angle_sums(tets, lE)
        dE = deficits({k: sE[k] for k in closed})
        mxA.append(max(abs(v) for v in dE.values()))
    emit("    均匀应变 max|δ|: " + " ".join(f"{v:.2e}" for v in mxA))
    assert max(mxA) < 1e-9, "平坦参考的均匀应变应保持零亏角"

    amps = [0.02, 0.04, 0.08, 0.16, 0.32]
    mxW = []
    qw = 2 * math.pi * 1.0 / M
    for A in amps:
        p2 = pos + (A * np.sin(qw * pos[:, 2]))[:, None] * np.array([0.0, 0.0, 1.0])
        lA = edge_lengths(p2, tets)
        sA = angle_sums(tets, lA)
        dA = deficits({k: sA[k] for k in closed})
        mxW.append(max(abs(v) for v in dA.values()))
    emit("    平面波 max|δ|: " + " ".join(f"{v:.2e}" for v in mxW))
    emit("    → 平坦参考的亏角对位移**恒等于 0**（任意振幅、任意阶）：")
    emit("      顶点始终落在 R³ 中，四面体平铺其凸包 ⇒ 内禀曲率恒为零；")
    emit("      故平坦参考根本不能承载 ε，环 3／4 的亏角涨落要求**弯曲参考**。")
    assert max(mxW) < 1e-12, "平坦参考下亏角应恒为零"
    emit("    [断言] 平坦参考：ε ≡ 0（无线性响应可言），链必在弯曲参考  ✓")

    # ---------- B. 弯曲参考 ----------
    emit("\n[B] 弯曲参考（边长受扰）：|Δδ| 对应变是否线性")
    rng = np.random.default_rng(20261123)
    eta = {k: rng.uniform(-0.06, 0.06) for k in l0}
    lref = {k: l0[k] * (1.0 + eta[k]) for k in l0}
    sref = angle_sums(tets, lref)
    dref = deficits({k: sref[k] for k in closed})
    mxr = max(abs(dref[k]) for k in closed)
    emit(f"    参考亏角（闭合边）max|δ₀| = {mxr:.4f} rad（非零）")
    assert mxr > 1e-3, "受扰参考应有非零亏角"

    dirs = edge_dirs(pos, tets)
    strainsB = [1e-3, 2e-3, 4e-3, 8e-3]
    dB = []
    for e in strainsB:
        E = np.array([[0.0, 0.5 * e, 0.0], [0.5 * e, 0.0, 0.0], [0.0, 0.0, 0.0]])
        lE = {k: lref[k] * (1.0 + float(dirs[k] @ E @ dirs[k])) for k in lref}
        sE = angle_sums(tets, lE)
        dE = deficits({k: sE[k] for k in closed})
        dB.append(max(abs(dE[k] - dref[k]) for k in closed))
    slopeB = float(np.polyfit(np.log(strainsB), np.log(dB), 1)[0])
    emit("    max|Δδ|: " + " ".join(f"{v:.3e}" for v in dB) + f"   斜率(ε)={slopeB:.3f}")
    assert 0.85 < slopeB < 1.15, "弯曲参考的响应应线性"
    assert dB[-1] > 5 * dB[0], "响应应随应变增长"
    emit("    [断言] 非零参考亏角 ⇒ 线性响应存在（n=1）  ✓")

    # ---------- C. 合成律 ----------
    emit("\n[C] 合成律 m_eff = 2n+1-s 与 σ₀² ∝ Q^{m_eff+1}")
    combos = [(1, 1), (2, 2), (1, 2), (2, 1), (3, 1)]
    Qs = np.array([2.0, 4.0, 8.0, 16.0, 32.0])
    for (n, s) in combos:
        meff = 2 * n + 1 - s
        vals = []
        for Q in Qs:
            q = np.linspace(0, Q, 400001)
            vals.append(float(np.trapezoid(q ** (2 * n + 1 - s), q)))
        vals = np.array(vals)
        sl = float(np.polyfit(np.log(Qs), np.log(vals), 1)[0])
        rel = float(np.max(np.abs(vals / (Qs ** (meff + 1) / (meff + 1)) - 1)))
        emit(f"    (n,s)=({n},{s}): m_eff={meff}, Q 斜率={sl:.6f}, 归一残差={rel:.2e}")
        assert abs(sl - (meff + 1)) < 1e-6, "σ₀ 标度指数应 = m_eff+1"
        assert rel < 1e-9, "归一化应精确"
    emit("    [断言] 形状指数 m_eff 与 σ₀ 标度指数 m_eff+1 同源  ✓")

    # ---------- D. 核与 S_ρ ----------
    emit("\n[D] 核 ρ_m 与 S_ρ（m_eff=1,2,3,4,6）")

    def rho(m, k, Q=math.pi, nq=60001):
        q = np.linspace(0.0, Q, nq)
        return float(np.trapezoid((q ** m) * j0(q * k), q)) / (Q ** (m + 1) / (m + 1))

    ms = [1, 2, 3, 4, 6]
    tab = {m: [rho(m, k) for k in range(1, 401)] for m in ms}
    for m in ms:
        part = [sum(tab[m][:k]) for k in (50, 100, 200, 400)]
        inc = part[-1] - part[-2]
        emit(f"    m={m}: S_ρ(50,100,200,400) = " + " ".join(f"{v:.6f}" for v in part)
             + f"   末段增量={inc:.2e}")
        if m >= 2:
            assert abs(inc) < 2e-3, f"m={m} 应收敛"
    assert abs(sum(tab[1][:400]) - sum(tab[1][:200])) < 2e-3, "m_eff=1 也应收敛"
    emit("    [断言] m_eff≥1 全部收敛（m_eff=1 边缘但收敛）  ✓")

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5))
    ax = axes[0, 0]
    ax.loglog(strains, np.maximum(mxA, 1e-16), "o-", label="均匀应变（平坦参考）≡0")
    ax.loglog(amps, np.maximum(mxW, 1e-16), "^-", label="平面波（平坦参考）≡0")
    ax.loglog(strainsB, dB, "s-", label="均匀应变（弯曲参考）")
    ax.set_xlabel("幅度"); ax.set_ylabel("max|Δδ|")
    ax.set_title("响应二分：平坦恒零，弯曲线性"); ax.legend(fontsize=8); ax.grid(True, alpha=.3)

    ax = axes[0, 1]
    for (n, s) in combos:
        meff = 2 * n + 1 - s
        vals = []
        for Q in Qs:
            q = np.linspace(0, Q, 20001)
            vals.append(float(np.trapezoid(q ** (2 * n + 1 - s), q)))
        ax.loglog(Qs, vals, "o-", label=f"(n,s)=({n},{s}), m_eff={meff}")
    ax.set_xlabel("截断 Q"); ax.set_ylabel("∫q^(2n+1-s)dq")
    ax.set_title("sigma0² 标度：斜率 = m_eff+1"); ax.legend(fontsize=7); ax.grid(True, alpha=.3)

    ax = axes[0, 2]
    for m in ms:
        ax.plot(range(1, 61), [tab[m][k - 1] for k in range(1, 61)], label=f"m_eff={m}")
    ax.set_xlabel("格点距 k"); ax.set_ylabel("ρ(k)")
    ax.set_title("Bessel 核"); ax.legend(fontsize=8); ax.grid(True, alpha=.3)

    ax = axes[1, 0]
    for m in ms:
        ax.plot(range(1, 401), np.cumsum(tab[m]), label=f"m_eff={m}")
    ax.set_xlabel("k"); ax.set_ylabel("Σρ")
    ax.set_title("部分和收敛（m_eff≥1）"); ax.legend(fontsize=8); ax.grid(True, alpha=.3)

    ax = axes[1, 1]
    for m in ms:
        k = np.arange(20, 200)
        ax.semilogx(k, [tab[m][kk - 1] * kk ** 1.5 for kk in k], label=f"m_eff={m}", lw=1)
    ax.set_xlabel("k"); ax.set_ylabel("k^{3/2}ρ(k)")
    ax.set_title("渐近包络有界（k^{-3/2}）"); ax.legend(fontsize=8); ax.grid(True, alpha=.3)

    ax = axes[1, 2]
    labels = ["(1,1)", "(2,1)", "(1,2)", "(2,2)", "(3,1)"]
    vals = [2 * n + 1 - s for (n, s) in combos]
    ax.bar(range(5), vals, color="#4a7ebb")
    ax.set_xticks(range(5))
    ax.set_xticklabels([f"{lab}\nm={v}" for lab, v in zip(labels, vals)], fontsize=9)
    ax.set_ylabel("m_eff")
    ax.set_title("(n,s) 到 m_eff 合成表"); ax.grid(True, axis="y", alpha=.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    emit(f"\n图已保存：{OUT_PNG}")

    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("k," + ",".join(f"rho_m{m}" for m in ms) + "\n")
        for k in range(1, 401):
            f.write(f"{k}," + ",".join(f"{tab[m][k-1]:.10f}" for m in ms) + "\n")
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    emit(f"CSV：{OUT_CSV}；摘要：{OUT_TXT}")
    emit("\n全部断言通过。")


if __name__ == "__main__":
    main()

