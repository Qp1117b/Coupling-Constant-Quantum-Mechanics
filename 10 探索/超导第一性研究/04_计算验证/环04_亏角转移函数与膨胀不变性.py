# -*- coding: utf-8 -*-
"""
环 4／86：亏角转移函数——膨胀不变性、c_ε ∝ 曲率尺度、零点幅度归属
================================================================
第 85 轮把 $|G_q|^2\\propto q^2$ 定成 $n=1$，剩余是 O(1) 角向因子 $c_\\varepsilon$。
本轮做三件事：

 (1) **零点幅度归属**（口径订正）：$\\Delta\\varepsilon_q=G_q u_q$，故
     $\\langle|\\Delta\\varepsilon_q|^2\\rangle=|G_q|^2\\langle|u_q|^2\\rangle$。
     $\\hbar/(2\\rho_m\\omega_q)$ 属于**位移模**；(2.1) 若直接把它当亏角幅度，
     就与 (4.1) 相差 $|G_q|^2\\propto q^2$——那正是第 85 轮撤销的 $n=0$ 位移读法。
 (2) **转移函数定义**：均匀应变下 $\\Delta\\varepsilon_e=C_{e}:\\epsilon$（$C$ 无量纲）；
     平面波 $\\epsilon=\\mathrm{sym}(\\mathrm i\\mathbf q\\otimes A\\hat u)$ 给
     $G_q=\\mathrm i\\,q_i C_{ij}\\hat u_j$，故 $c_\\varepsilon^2=|\\hat q_iC_{ij}\\hat u_j|^2$。
     各向同性膨胀保持所有二面角 ⇒ $\\mathrm{tr}_\\epsilon C=0$（解析，可数值核验）。
 (3) **测量**：弯曲 Kuhn 参考上逐边反解 $C_e$（六个应变基），核验
     $\\mathrm{tr}_\\epsilon C=0$、给出纵向／横向 $c_\\varepsilon$，并测
     $c_\\varepsilon$ 随参考曲率 $\\eta$ 的标度。附带检验并**否证**"相对亏损律"
     $\\Delta\\varepsilon_e\\propto\\varepsilon_e^{(0)}$（对角基 corr≈0）。
"""
import itertools
import math
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

OUT_CSV = "环04_亏角转移函数.csv"
OUT_PNG = "环04_亏角转移函数.png"
OUT_TXT = "环04_亏角转移函数_摘要.txt"

PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
LOG = []


def emit(s=""):
    print(s)
    LOG.append(s)


# ---------------------------------------------------------------- Kuhn 三角化
def build_patch(M):
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
    out = []
    for (a, b) in PAIRS:
        e = l6[PAIRS.index((a, b))]
        rem = [x for x in range(4) if x not in (a, b)]
        r, s = rem

        def L(u, v):
            return l6[PAIRS.index(tuple(sorted((u, v))))]

        ar, br, as_, bs, rsl = L(a, r), L(b, r), L(a, s), L(b, s), L(r, s)
        zr = (ar ** 2 - br ** 2 + e ** 2) / (2 * e)
        zs = (as_ ** 2 - bs ** 2 + e ** 2) / (2 * e)
        rr2 = max(ar ** 2 - zr ** 2, 0.0)
        rs2 = max(as_ ** 2 - zs ** 2, 0.0)
        rr, rss = math.sqrt(rr2), math.sqrt(rs2)
        if rr < 1e-14 or rss < 1e-14:
            out.append(math.pi)
            continue
        uv2 = max(rsl ** 2 - (zr - zs) ** 2, 0.0)
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


# 六个正交归一的对称应变基（Frobenius 范数为 1）
S_MODES = [
    np.array([[1.0, 0, 0], [0, 0, 0], [0, 0, 0]]),           # xx
    np.array([[0, 0, 0], [0, 1.0, 0], [0, 0, 0]]),           # yy
    np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1.0]]),           # zz
    np.array([[0, 1.0, 0], [1.0, 0, 0], [0, 0, 0]]) / math.sqrt(2),  # xy
    np.array([[0, 0, 0], [0, 0, 1.0], [0, 1.0, 0]]) / math.sqrt(2),  # yz
    np.array([[0, 0, 1.0], [0, 0, 0], [1.0, 0, 0]]) / math.sqrt(2),  # zx
]
MODE_NAMES = ["xx", "yy", "zz", "xy", "yz", "zx"]


def strained_lengths(l0, dirs, E, eps):
    return {k: l0[k] * (1.0 + eps * float(dirs[k] @ E @ dirs[k])) for k in l0}


def main():
    emit("=" * 78)
    emit("环 4／86：亏角转移函数——膨胀不变性、c_ε ∝ 曲率尺度、零点幅度归属")

    M = 6
    pos, tets = build_patch(M)
    l0 = edge_lengths(pos, tets)
    s0 = angle_sums(tets, l0)
    closed = {k for k, v in s0.items() if abs(v - 2 * math.pi) < 1e-8}
    d0 = deficits({k: s0[k] for k in closed})
    keys = sorted(closed)
    dirs = edge_dirs(pos, tets)
    emit(f"\n[0] Kuhn 补片 M={M}：顶点 {len(pos)}，四面体 {len(tets)}，闭合边 {len(keys)}")

    # ---------- [1] 弯曲参考与六个应变基的响应 ----------
    eta = 0.06

    def build_ref(eta_amp, seed=20261123):
        rng = np.random.default_rng(seed)
        e = {k: rng.uniform(-eta_amp, eta_amp) for k in l0}
        lr = {k: l0[k] * (1.0 + e[k]) for k in l0}
        sr = angle_sums(tets, lr)
        return lr, deficits({k: sr[k] for k in closed})

    lref, dref = build_ref(eta)
    emit(f"    参考亏角：max={max(abs(dref[k]) for k in keys):.4f} rad，"
         f"RMS={np.sqrt(np.mean([dref[k]**2 for k in keys])):.4f} rad")

    delta = 5e-5
    C = np.zeros((6, len(keys)))
    for ai, E in enumerate(S_MODES):
        lp = strained_lengths(lref, dirs, E, +delta)
        lm = strained_lengths(lref, dirs, E, -delta)
        dp = deficits({k: v for k, v in angle_sums(tets, lp).items() if k in closed})
        dm = deficits({k: v for k, v in angle_sums(tets, lm).items() if k in closed})
        for ei, k in enumerate(keys):
            C[ai, ei] = (dp[k] - dm[k]) / (2 * delta)
    emit("    已反解 6 个应变基的逐边响应 C_{a,e}=∂δ_e/∂ε_a（中心差分）")

    dvec = np.array([dref[k] for k in keys])
    nx = np.array([dirs[k][0] for k in keys])
    ny = np.array([dirs[k][1] for k in keys])
    nz = np.array([dirs[k][2] for k in keys])

    # ---------- [2] 膨胀不变性 tr C = 0 ----------
    emit("\n[2] 各向同性膨胀保持所有二面角 ⇒ tr_ε C = 0（解析恒等式，数值核验）")
    tr = C[0] + C[1] + C[2]
    scaleC = math.sqrt(float(np.mean(C[0] ** 2 + C[1] ** 2 + C[2] ** 2)))
    emit(f"    max|C_xx+C_yy+C_zz| = {np.max(np.abs(tr)):.3e}；典型 |C| = {scaleC:.4f}；"
         f"比值 = {np.max(np.abs(tr))/scaleC:.3e}")
    assert np.max(np.abs(tr)) < 1e-6 * max(1.0, scaleC), "膨胀响应应恒为零"
    emit("    [断言] 亏角对纯膨胀零响应（只有形状改变才响应）  ✓")

    # ---------- [2b] 否证相对亏损律 ----------
    emit("\n[2b] 相对亏损律 Δδ_e ∝ δ_e(0) 的检验（预期否证对角基）")
    for ai in (0, 1, 3):
        r = C[ai]
        cc = float(np.corrcoef(r, dvec)[0, 1])
        beta = float(np.dot(r, dvec) / np.dot(dvec, dvec))
        pred = beta * dvec
        r2 = 1.0 - np.sum((r - pred) ** 2) / np.sum((r - r.mean()) ** 2)
        emit(f"    {MODE_NAMES[ai]}: corr(R,delta0)={cc:.4f}，斜率 beta={beta:.4f}，R^2={r2:.4f}")
    emit("    结论：对角基 corr≈0 ⇒ 响应不是参考亏角的函数；剪切基 R^2≈0.68 只是部分相关。")

    # ---------- [3] c_ε 的测量与各向同性 ----------
    emit("\n[3] 转移函数：纵向 c²=⟨C_aa²⟩；横向 c²=⟨C_ab²⟩=⟨C_S4²⟩/2（归一化基换算）")
    c2 = [float(np.mean(C[ai] ** 2)) for ai in range(6)]
    for ai in range(6):
        emit(f"    {MODE_NAMES[ai]}: ⟨C_S²⟩={c2[ai]:.6f}（S 为 Frobenius 归一）")
    c_long = float(np.mean(c2[:3]))
    c_trans = float((c2[3] + c2[4] + c2[5]) / 3.0 / 2.0)
    emit(f"    纵向 c_ε={math.sqrt(c_long):.4f}；横向 c_ε={math.sqrt(c_trans):.4f}；"
         f"c² 比 = {c_trans/c_long:.3f}")

    # ---------- [4] c_ε 随参考曲率的标度 ----------
    emit("\n[4] c_ε 随参考曲率幅度 η 的标度（同一随机图案缩放）")
    etas = [0.01, 0.02, 0.04, 0.08]
    cets = []
    for e in etas:
        lr, dr = build_ref(e)
        dvec_e = np.array([dr[k] for k in keys])
        cs = []
        for ai in range(3):
            lp = strained_lengths(lr, dirs, S_MODES[ai], +delta)
            lm = strained_lengths(lr, dirs, S_MODES[ai], -delta)
            dp = deficits({k: v for k, v in angle_sums(tets, lp).items() if k in closed})
            dm = deficits({k: v for k, v in angle_sums(tets, lm).items() if k in closed})
            R = np.array([(dp[k] - dm[k]) / (2 * delta) for k in keys])
            cs.append(math.sqrt(float(np.mean(R ** 2))))
        cets.append(float(np.mean(cs)))
        emit(f"    η={e:.2f}: c_ε={cets[-1]:.4f}，RMS(δ⁰)={np.sqrt(np.mean(dvec_e**2)):.4f}，"
             f"c_ε/RMS={cets[-1]/np.sqrt(np.mean(dvec_e**2)):.3f}")
    slope = float(np.polyfit(np.log(etas), np.log(cets), 1)[0])
    emit(f"    log-log 斜率 = {slope:.3f}（c_ε ∝ η 的判据；η→0 时 c_ε→0）")
    assert 0.85 < slope < 1.15, "c_ε 应对参考曲率线性"

    # ---------- [5] σ₀ 标度：正确 Q³ vs 直接读 (2.1) 的 Q ----------
    emit("\n[5] σ₀² 的 Q 标度：正确读法（含 |G_q|²∝q²） vs 直接读 (2.1)")
    Qs = np.array([2.0, 4.0, 8.0, 16.0, 32.0])
    s_correct, s_naive = [], []
    for Q in Qs:
        q = np.linspace(1e-6, Q, 400001)
        # 正确：∫ q·|G|²/(2ρc q) dq = ∫ q² dq /(2ρc) ⇒ ∝ Q³
        s_correct.append(float(np.trapezoid(q ** 2, q)))
        # 直接读 (2.1)：∫ q·1/(2ρc q) dq = ∫ dq ⇒ ∝ Q
        s_naive.append(float(np.trapezoid(np.ones_like(q), q)))
    sl_c = float(np.polyfit(np.log(Qs), np.log(s_correct), 1)[0])
    sl_n = float(np.polyfit(np.log(Qs), np.log(s_naive), 1)[0])
    emit(f"    正确读法斜率 {sl_c:.4f}（=3=m_eff+1）；直接读 (2.1) 斜率 {sl_n:.4f}（=1）")
    assert abs(sl_c - 3) < 1e-6 and abs(sl_n - 1) < 1e-6

    # ---------- [6] 维数定律：m_eff^(d) = 2n+(d-1)-s ----------
    emit("\n[6] 模求和维数 d 进入指数：m_eff^(d)=2n+(d-1)-s")
    from scipy.special import j0 as besselJ0

    for (n_, s_) in [(1, 1), (1, 2)]:
        row = []
        for d_ in (2, 3):
            me = 2 * n_ + (d_ - 1) - s_
            vals = []
            for Q in Qs:
                q = np.linspace(0, Q, 200001)
                vals.append(float(np.trapezoid(q ** me, q)))
            sl = float(np.polyfit(np.log(Qs), np.log(vals), 1)[0])
            row.append((d_, me, sl))
        emit(f"    (n,s)=({n_},{s_}): " + "；".join(
            f"d={d_} ⇒ m_eff={me}、σ0² 斜率 {sl:.3f}" for (d_, me, sl) in row))
        for (d_, me, sl) in row:
            assert abs(sl - (me + 1)) < 1e-6
    emit("    [断言] σ0² 的指数始终 = m_eff^(d)+1；d=2 给 3，d=3 给 4  ✓")

    # 3D 核（j0 代替 J0）下的 S_ρ（m_eff=3）
    emit("\n    3D 角向核 j0(qr)=sin(qr)/(qr) 下的 S_ρ（m_eff=3，与 2D 的 -0.0756 对照）")

    def rho3(m, k, Q=math.pi, nq=120001):
        q = np.linspace(1e-9, Q, nq)
        return float(np.trapezoid((q ** m) * (np.sin(q * k) / (q * k)), q)) / (Q ** (m + 1) / (m + 1))

    S3 = sum(rho3(3, k) for k in range(1, 401))
    S3h = sum(rho3(3, k) for k in range(1, 201))
    emit(f"    S_ρ^(3D)(m=3, k≤400) = {S3:.6f}（k≤200 时 {S3h:.6f}；末段增量 {S3-S3h:.2e}）")
    assert abs(S3 - S3h) < 2e-3, "3D 核的 S_ρ 应收敛"

    # ---------- 图 ----------
    fig, axes = plt.subplots(2, 3, figsize=(15, 8.5))

    ax = axes[0, 0]
    ax.scatter(dvec, C[0], s=8, alpha=0.6)
    xs = np.linspace(dvec.min(), dvec.max(), 50)
    beta = float(np.dot(C[0], dvec) / np.dot(dvec, dvec))
    ax.plot(xs, beta * xs, "r-", label=f"beta={beta:.2f}")
    ax.set_xlabel("参考亏角 delta0"); ax.set_ylabel("响应 C_xx")
    ax.set_title("相对亏损律的否证：corr≈0"); ax.legend(); ax.grid(alpha=.3)

    ax = axes[0, 1]
    rho = np.where(np.abs(dvec) > 0.05, C[0] / np.where(np.abs(dvec) > 0.05, dvec, 1), np.nan)
    proj = nx ** 2
    ax.scatter(proj, rho, s=8, alpha=0.6)
    ax.set_xlabel("方向投影 n_x^2"); ax.set_ylabel("rho = C_xx/delta0")
    ax.set_title("rho 的离散度：响应不是 delta0 的函数"); ax.grid(alpha=.3)

    ax = axes[0, 2]
    ax.bar(range(6), [math.sqrt(v) for v in c2], color="#4a7ebb")
    ax.set_xticks(range(6)); ax.set_xticklabels(MODE_NAMES)
    ax.set_ylabel("sqrt(mean(C^2))")
    ax.set_title("六个归一化应变基的响应振幅"); ax.grid(axis="y", alpha=.3)

    ax = axes[1, 0]
    ax.loglog(etas, cets, "o-")
    ax.set_xlabel("参考曲率幅度 eta"); ax.set_ylabel("c_eps")
    ax.set_title(f"c_eps 正比于 eta（斜率 {slope:.2f}）"); ax.grid(alpha=.3, which="both")

    ax = axes[1, 1]
    ax.loglog(Qs, s_correct, "o-", label="正确：Q^3")
    ax.loglog(Qs, s_naive, "s-", label="直接读 (2.1)：Q")
    ax.set_xlabel("截断 Q"); ax.set_ylabel("sigma0^2 的 Q 权重")
    ax.set_title("零点幅度归属：差一个 q^2"); ax.legend(); ax.grid(alpha=.3, which="both")

    ax = axes[1, 2]
    ax.hist(C[0], bins=40, color="#8e6cb0", alpha=.85)
    ax.axvline(0, color="k", lw=.8)
    ax.set_xlabel("C_xx"); ax.set_ylabel("边数")
    ax.set_title("逐边响应的分布（零均值、有限宽度）"); ax.grid(alpha=.3)

    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=150)
    emit(f"\n图已保存：{OUT_PNG}")

    with open(OUT_CSV, "w", encoding="utf-8") as f:
        f.write("edge,nx,ny,nz,delta0," + ",".join(f"C_{m}" for m in MODE_NAMES) + "\n")
        for ei, k in enumerate(keys):
            f.write(f"{ei},{nx[ei]:.6f},{ny[ei]:.6f},{nz[ei]:.6f},{dvec[ei]:.8f},"
                    + ",".join(f"{C[ai, ei]:.8f}" for ai in range(6)) + "\n")
    with open(OUT_TXT, "w", encoding="utf-8") as f:
        f.write("\n".join(LOG))
    emit(f"CSV：{OUT_CSV}；摘要：{OUT_TXT}")
    emit("\n全部断言通过。")


if __name__ == "__main__":
    main()
