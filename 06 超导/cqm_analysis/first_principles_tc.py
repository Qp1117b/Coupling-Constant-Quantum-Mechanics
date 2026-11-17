"""
CQM 第一性 Tc 标度律 —— 端到端计算（可复核产物）
====================================================

沿骨架 (06 超导/CQM_超导核心理论.md) §11.14 + §18.2 的第一性计算链：

  材料结构 -> 亏角涨落 Delta eps_0 -> (自由能闭式) -> Tc

推导（全程不引入材料拟合参数，外生能标在代数中抵消）：

  (1) 双尺度亏角涨落 (骨架 line 1602/1606/1612):
      Delta eps_0^2 = C^2/(omega_D) * (1-f) * (3*hbar/4) * F_struct
      F_struct = (1/L^2)(2z/M_cell) + (1/l^2) sum_intra(1/m_i + 1/m_j)
      C (边长->亏角转换), f (关联因子), z (配位) 为普适量, 与材料无关。

  (2) 自由能 Tc 闭式 (骨架 line 1636):
      Tc^2 = 8 Delta eps_0^2 K_eff theta_D / (9 ln2),  K_eff 曲率刚度(普适)

  (3) omega_D = k_B theta_D / hbar 代入 (1) 再入 (2):
      Tc^2 ~ [F_struct/theta_D] * theta_D = F_struct   (theta_D 消去)
  =>  Tc 正比于 sqrt(F_struct)   —— 零材料拟合参数的纯第一性标度律。

这与 CQM 定位一致 (命题 Z2): CQM 是无量纲普适类理论, 给相对标度, 不给绝对 Tc;
绝对比例常数 (含 W-3 待推的 C, K_eff) 不是材料拟合参数, 只作整体归一化。

数据: 3DSC (Nature Sci Data 2023, doi:10.1038/s41597-023-02721-y, CC BY 4.0)
      superconductors_3D/data/final/MP/3DSC_MP.csv  (5773 条, 含 Tc/晶格常数/体积/化学式)
元素质量: element_fg_table.json (CQM 元素 FG 表, 118 元素)

输出: 每材料 F_struct 与 Tc_pred ∝ sqrt(F_struct); 与实验 Tc 的秩相关;
      系统偏差分析 (对应骨架 line 1575 的 W-3 "裸涨落增强缺口")。
"""
import csv, json, math, re, collections, statistics, sys
sys.stdout.reconfigure(encoding="utf-8")

HERE = "06 超导/cqm_analysis"
CSV = f"{HERE}/data_raw/3DSC_MP.csv"
ELEM = f"{HERE}/element_fg_table.json"

ELEM_TAB = json.load(open(ELEM, encoding="utf-8"))
MASS = {e["symbol"]: e["mass"] for e in ELEM_TAB}

# 配位数 z 按晶系近似 (仅进入普适比例, 不影响相对标度的大结构)
Z_COORD = {"cubic": 8, "tetragonal": 8, "orthorhombic": 6, "hexagonal": 8,
           "trigonal": 6, "monoclinic": 6, "triclinic": 6}

def parse_formula(f):
    """返回 {sym: count}; 忽略掺杂占位小数精确到符号计数。"""
    f = re.sub(r"\s+", "", f.strip())
    f = f.split("(")[0] if f.startswith("(") else f
    toks = re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", f)
    out = collections.defaultdict(float)
    for sym, num in toks:
        if sym not in MASS:
            continue
        out[sym] += float(num) if num else 1.0
    return dict(out)

def load():
    with open(CSV, encoding="utf-8") as fh:
        lines = fh.readlines()
    hi = [i for i, l in enumerate(lines) if l.startswith("formula_sc,")][0]
    hdr = lines[hi].rstrip("\n").split(",")
    data = [l for l in lines[hi+1:] if l.strip()]
    out = []
    for r in csv.DictReader(data, fieldnames=hdr):
        try:
            tc = float(r["tc"])
            a, b, c = float(r["lata_2"]), float(r["latb_2"]), float(r["latc_2"])
            V = float(r["cell_volume_2"])
            ns = int(float(r["nsites_2"]))
            comp = parse_formula(r["formula_sc"])
        except (ValueError, KeyError):
            continue
        if tc <= 0 or V <= 0 or ns <= 0 or not comp:
            continue
        out.append(dict(formula=r["formula_sc"], tc=tc, a=a, b=b, c=c,
                        V=V, ns=ns, sys=r.get("crystal_system_2", ""),
                        comp=comp, cls=r.get("sc_class", "")))
    return out

def f_struct(r):
    """第一性结构-质量指纹 (忠实骨架 line 1606/1612):
       Delta delta_inter^2 ~ (1/L^2)(2z/M_cell)   L=晶胞间距 ~ V^(1/3)
       Delta delta_intra^2 ~ (1/l^2) sum(1/m_i)   l=晶胞内原子间距 ~ (V/ns)^(1/3)
       普适因子 C^2(1-f)(3hbar/4)/omega_D 已剥离 (不影响相对标度)。
    """
    L = r["V"] ** (1.0/3.0)                    # 晶胞尺度 (Angstrom)
    l = (r["V"] / r["ns"]) ** (1.0/3.0)        # 晶胞内原子间距 (Angstrom)
    comp = r["comp"]
    M_cell = sum(MASS[s]*n for s, n in comp.items())       # 晶胞总质量 (amu)
    S_inv = sum(n/MASS[s] for s, n in comp.items())        # sum(1/m_i)
    z = Z_COORD.get(r["sys"], 6)
    inter = (2.0*z/M_cell) / L**2
    intra = S_inv / l**2                                    # 注意: intra 用 l (键内尺度)
    return inter + intra, inter, intra

def spearman(xs, ys):
    n = len(xs)
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        rr = [0.0]*n; i = 0
        while i < n:
            j = i
            while j+1 < n and a[order[j+1]] == a[order[i]]:
                j += 1
            avg = (i+j)/2 + 1
            for k in range(i, j+1):
                rr[order[k]] = avg
            i = j+1
        return rr
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((rx[i]-mx)*(ry[i]-my) for i in range(n))
    den = math.sqrt(sum((v-mx)**2 for v in rx)*sum((v-my)**2 for v in ry))
    return num/den if den else float("nan")

def main():
    rows = load()
    print(f"=== 3DSC 可计算样本: {len(rows)} / 5773 ===")
    for r in rows:
        F, inter, intra = f_struct(r)
        r["F"] = F; r["inter"] = inter; r["intra"] = intra
        r["Tc_pred_shape"] = math.sqrt(F)   # ∝ Tc (零拟合参数)

    print("\n=== 第一性标度律 Tc ∝ sqrt(F_struct) 的检验 ===")
    rho_all = spearman([r["Tc_pred_shape"] for r in rows], [r["tc"] for r in rows])
    print(f"  Spearman(sqrt(F_struct), Tc_exp) 全样本 = {rho_all:+.3f}  (n={len(rows)})")

    # 按类别分层 (对照实验类别标签, 不作为拟合输入)
    by = collections.defaultdict(list)
    for r in rows:
        by[r["cls"]].append(r)
    print("\n=== 按 sc_class 分层 (第一性标度律在各类内的秩相关) ===")
    for cls, sub in sorted(by.items(), key=lambda kv: -len(kv[1])):
        if len(sub) < 15:
            continue
        rho = spearman([r["Tc_pred_shape"] for r in sub], [r["tc"] for r in sub])
        print(f"  {cls:18s} n={len(sub):4d}  rho={rho:+.3f}")

    # 标志性材料对照 (验证物理图像: 轻原子 -> 大 F -> 高 Tc 潜力)
    print("\n=== 标志性材料的第一性指纹 (验证 CQM '氢轻->涨落大' 图像) ===")
    keys = ["H3S", "YH9", "LaH10", "MgB2", "Nb3Ge", "Al", "Nb", "Pb", "YBa2Cu3O7", "FeSe"]
    shown = 0
    for key in keys:
        for r in rows:
            if r["formula"].replace(".", "").lower() == key.lower().replace(".", "").lower():
                print(f"  {r['formula']:20s} Tc={r['tc']:6.1f}K  F={r['F']:8.4f}  sqrtF={r['Tc_pred_shape']:6.3f}  inter={r['inter']:.4f} intra={r['intra']:.4f}")
                shown += 1
                break
    if shown == 0:
        # 退而求其次: 显示 F 最大/最小的材料
        srt = sorted(rows, key=lambda r: -r["F"])
        print("  (精确式未命中, 显示 F 最高 5 例)")
        for r in srt[:5]:
            print(f"  {r['formula']:20s} Tc={r['tc']:6.1f}K  F={r['F']:8.4f}  sqrtF={r['Tc_pred_shape']:6.3f}")

    # 两阶段分支检验 (骨架 §0.5/§18.1):
    #   配对限制支 T*=min -> Tc 由配对幅度控制 -> 应与 sqrt(F_struct) 正相关;
    #   相位限制支 T_theta=min (赝能隙材料) -> Tc 由相位刚度控制 -> 与配对幅度弱/无关。
    # 分支标注用实验类别事实 (外部标注, 不进入计算):
    PAIR_LIMITED = {"Other", "Carbon", "Chevrel", "Heavy_fermionChevrel"}
    PHASE_LIMITED = {"Cuprate", "Ferrite", "Oxide"}   # 层状/强关联, 常见赝能隙
    print("\n=== 两阶段分支检验 (Tc 由哪一阶段主导) ===")
    for label, classes in [("配对限制候选", PAIR_LIMITED), ("相位限制候选", PHASE_LIMITED)]:
        sub = [r for r in rows if r["cls"] in classes]
        if len(sub) < 10:
            continue
        rho = spearman([r["Tc_pred_shape"] for r in sub], [r["tc"] for r in sub])
        print(f"  {label:12s} n={len(sub):4d}  rho(sqrt(F),Tc)={rho:+.3f}")

    # W-3 增强缺口: Tc_exp / sqrt(F) 的分布 (应非常数 -> 印证 W-3 待推)
    ratios = [r["tc"]/r["Tc_pred_shape"] for r in rows if r["Tc_pred_shape"] > 0]
    print(f"\n=== W-3 增强缺口诊断: Tc_exp / sqrt(F_struct) ===")
    print(f"  中位数={statistics.median(ratios):.2f}  几何标准差因子={math.exp(statistics.pstdev([math.log(x) for x in ratios])):.2f}")
    print("  (若 W-3 已闭合, 该比值应为材料无关常数; 离散度反映待推的增强环节)")

if __name__ == "__main__":
    main()
