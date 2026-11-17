"""
同结构不同 Tc 分析 —— 证伪"静态结构决定 Tc"(可复核产物)
================================================================
结论来源: 10 探索/CQM_探索_第一性计算II_同结构不同Tc证伪结构决定论.md

方法: 用 3DSC 的 material_id_2 (Materials Project 结构 ID) 分组 —— 同一 ID = 同一底层晶体结构;
      统计组内不同化学掺杂条目的 Tc 分布。这是干净的自然实验: 结构固定, 只变化学掺杂。

若"结构决定 Tc"成立, 同结构必给出同 Tc; 数据明确否定(中位 2.12 倍)。

用法: python same_structure_analysis.py
数据: data_raw/3DSC_MP.csv (3DSC, Nature Sci Data 2023, doi:10.1038/s41597-023-02721-y, CC BY 4.0)
"""
import csv, sys, statistics, collections
sys.stdout.reconfigure(encoding="utf-8")

CSV = "06 超导/cqm_analysis/data_raw/3DSC_MP.csv"

def load_rows():
    with open(CSV, encoding="utf-8") as fh:
        lines = fh.readlines()
    hi = [i for i, l in enumerate(lines) if l.startswith("formula_sc,")][0]
    hdr = lines[hi].rstrip().split(",")
    return list(csv.DictReader([l for l in lines[hi+1:] if l.strip()], fieldnames=hdr))

def analyze(min_n=3):
    rows = load_rows()
    groups = collections.defaultdict(list)
    for r in rows:
        mid = r.get("material_id_2", "").strip()
        tc = r.get("tc", "").strip()
        if not mid or not tc:
            continue
        try:
            tcv = float(tc)
        except ValueError:
            continue
        if tcv <= 0:
            continue
        groups[mid].append((r["formula_sc"], tcv, r.get("sc_class", "")))

    multi = {k: v for k, v in groups.items() if len(v) >= min_n}
    spreads = []
    for mid, v in multi.items():
        tcs = [x[1] for x in v]
        spreads.append((max(tcs) - min(tcs), max(tcs) / max(min(tcs), 0.1),
                        len(v), mid, min(tcs), max(tcs)))
    spreads.sort(reverse=True)

    print(f"total materials with structure id: {sum(len(v) for v in groups.values())}")
    print(f"structure ids with >={min_n} superconducting entries: {len(multi)}")
    print("\n=== top 15 same-structure / different-Tc groups ===")
    for d, ratio, n, mid, tmin, tmax in spreads[:15]:
        print(f"  {mid:14s} n={n:2d}  Tc=[{tmin:6.1f},{tmax:6.1f}]  spread={d:6.1f}K  ratio={ratio:5.1f}x")

    ratios = [x[1] for x in spreads]
    print(f"\nmedian Tc ratio within same structure = {statistics.median(ratios):.2f}x")
    print(f"fraction with ratio>=2: {sum(1 for x in ratios if x >= 2) / len(ratios):.2%}")
    print(f"fraction with ratio>=3: {sum(1 for x in ratios if x >= 3) / len(ratios):.2%}")

    if spreads:
        mid = spreads[0][3]
        print(f"\n=== detail of {mid} ===")
        for form, tc, cls in multi[mid]:
            print(f"  {form:28s} Tc={tc:6.1f}  class={cls}")
    return spreads

if __name__ == "__main__":
    analyze()
