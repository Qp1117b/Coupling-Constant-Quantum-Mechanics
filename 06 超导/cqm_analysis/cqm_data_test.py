"""CQM 几何命题 vs 226 种超导材料数据库 —— 数据驱动检验。

检验对象（全部来自核心文档的真实声称，不自造靶子）：
  P-N     §11.9: 中子数 N 大 -> 缺陷源多 -> 角亏涨落 Delta delta_v 大 -> Tc 潜力高(非单调)
  P-delta  §4/§9: 角亏 delta_v / 涨落越丰富 -> 配对通道越强 -> Tc 高
  P-H      §7: 金属氢(Z=1,N=0)无角亏涨落 -> 不超导

方法克制：只做 Spearman 相关与分组中位数，不做多参数拟合/最小二乘。
混淆变量(类别、结构族、发现年份、常压/高压)一律单独报告，不混进主结论。

化学式解析：支持 Xn 计数、括号 (AB)n、点号水合物、掺杂 x/y 占位符。
掺杂位(含 x,y,delta 或 1-x 形式)按主元素计，不解析占位比例。
"""
import csv
import json
import math
import re
import collections
import statistics

ELEM = json.load(open("element_fg_table.json", encoding="utf-8"))
BY_SYM = {e["symbol"]: e for e in ELEM}


def parse_formula(f):
    """返回 {sym: count}；忽略掺杂变量 x/y/delta，忽略结晶水。"""
    f = f.strip()
    f = re.sub(r"\s+", "", f)
    # 去掉常见后缀/相标记
    f = re.split(r"[-–]\s*[A-Z]", f)[0]  # e.g. Ba-122 -> Ba (激进，稍后特殊处理)
    # 去点号水合物/插层
    f = f.split("·")[0].split(".")[0]
    # 展开括号 (...)n
    def expand(s):
        pat = re.compile(r"\(([^()]*)\)(\d*\.?\d*)")
        while pat.search(s):
            s = pat.sub(lambda m: m.group(1) * (int(m.group(2)) if m.group(2) else 1), s)
        return s
    f = expand(f)
    # 令牌：元素符号 + 可选数字(整数或小数)；跳过含 x/y 的掺杂项
    toks = re.findall(r"([A-Z][a-z]?)(\d*\.?\d*)", f)
    out = collections.defaultdict(float)
    for sym, num in toks:
        if sym not in BY_SYM:
            continue
        if num == "":
            out[sym] += 1.0
        else:
            try:
                out[sym] += float(num)
            except ValueError:
                out[sym] += 1.0
    return dict(out)


def load_materials():
    rows = []
    with open("superconductors_deduplicated.csv", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            tc_raw = r["临界温度 Tc (K)"].strip()
            m = re.search(r"[\d.]+", tc_raw)
            if not m:
                continue
            tc = float(m.group())
            if tc <= 0 or tc > 300:
                continue
            rows.append({
                "cat": r["类别"], "formula": r["材料(化学式)"], "tc": tc,
                "structure": r["晶体结构"], "kind": r["类型(I/II)"],
                "mech": r["超导机制"], "cond": r["条件"], "year": r["发现年份"],
            })
    return rows


def material_features(formula):
    c = parse_formula(formula)
    if not c or sum(c.values()) <= 0:
        return None
    tot = sum(c.values())
    feats = {}
    # 原子分数加权的元素几何量
    for key, field in [
        ("Z", "Z"), ("N", "neutrons"), ("mass", "mass"),
        ("delta", "mean_delta_v"), ("deform", "deform"),
    ]:
        vals = [(c[s] / tot) * BY_SYM[s][field] for s in c]
        feats[key] = sum(vals)
    # A1 型(O 等零角亏)原子分数
    feats["frac_A1"] = sum(c[s] / tot for s in c if BY_SYM[s]["cartan_type"] == "A1")
    # 最大单元素角亏(丰富度的一个代理)
    feats["delta_max_elem"] = max(BY_SYM[s]["mean_delta_v"] for s in c)
    feats["n_elem"] = len(c)
    feats["comp"] = c
    return feats


def spearman(xs, ys):
    n = len(xs)
    if n < 3:
        return float("nan"), n
    def rank(a):
        order = sorted(range(len(a)), key=lambda i: a[i])
        r = [0.0] * len(a)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.mean(rx), statistics.mean(ry)
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    den = math.sqrt(sum((v - mx) ** 2 for v in rx) * sum((v - my) ** 2 for v in ry))
    return (num / den if den else float("nan")), n


def main():
    rows = load_materials()
    print("=== 数据库规模 ===", len(rows))
    print("机制分布:", dict(collections.Counter(r["mech"] for r in rows)))
    print("条件分布(常压/高压):", dict(collections.Counter("高压" if "高压" in r["cond"] else "常压" for r in rows)))
    print()

    data = []
    for r in rows:
        f = material_features(r["formula"])
        if f:
            data.append((r, f))
        else:
            pass
    print("=== 成功解析 ===", len(data), "/", len(rows))
    fail = [r["formula"] for r in rows if material_features(r["formula"]) is None]
    if fail:
        print("解析失败样例:", fail[:15])
    print()

    print("=== 全样本 Spearman(Tc, 几何量) ===")
    for key in ["N", "Z", "mass", "delta", "deform", "frac_A1", "delta_max_elem", "n_elem"]:
        xs = [f[key] for _, f in data]
        ys = [r["tc"] for r, _ in data]
        rho, n = spearman(xs, ys)
        print("  rho(Tc, %-14s) = %+.3f   (n=%d)" % (key, rho, n))
    print()

    # 按机制分层（关键：CQM 命题主要针对非常规/高温，常规 BCS 应次导）
    print("=== 按机制分层 Spearman(Tc, N) 与 (Tc, delta) ===")
    for mech in sorted(set(r["mech"] for r, _ in data)):
        sub = [(r, f) for r, f in data if r["mech"] == mech]
        if len(sub) < 5:
            continue
        rN, _ = spearman([f["N"] for _, f in sub], [r["tc"] for r, _ in sub])
        rD, _ = spearman([f["delta"] for _, f in sub], [r["tc"] for r, _ in sub])
        med = statistics.median(r["tc"] for r, _ in sub)
        print("  %-8s n=%3d  rho(Tc,N)=%+.3f  rho(Tc,delta)=%+.3f  Tc中位=%.1fK"
              % (mech, len(sub), rN, rD, med))
    print()

    # 高压混淆：只取常压
    print("=== 只取常压样本 Spearman(Tc, N/delta) ===")
    amb = [(r, f) for r, f in data if "高压" not in r["cond"]]
    for key in ["N", "delta"]:
        rho, n = spearman([f[key] for _, f in amb], [r["tc"] for r, _ in amb])
        print("  rho(Tc, %-6s) = %+.3f  (n=%d)" % (key, rho, n))
    print()

    # 分组：按平均中子数四分位看 Tc 中位数（检验非单调命题）
    print("=== 按 N 四分位的 Tc 中位数（检验§11.9非单调叙事）===")
    ss = sorted(data, key=lambda rf: rf[1]["N"])
    q = len(ss) // 4
    for k in range(4):
        grp = ss[k * q:(k + 1) * q] if k < 3 else ss[3 * q:]
        tcs = [r["tc"] for r, _ in grp]
        ns = [f["N"] for _, f in grp]
        print("  Q%d: N∈[%.1f,%.1f]  Tc中位=%6.1fK  n=%d"
              % (k + 1, min(ns), max(ns), statistics.median(tcs), len(grp)))
    print()

    # P-H: 金属氢 / 富氢
    print("=== P-H 检验：含 H 材料 ===")
    hmat = [(r, f) for r, f in data if "H" in f["comp"]]
    for r, f in hmat[:20]:
        print("  %-18s Tc=%5.1fK  H原子分数=%.2f  mech=%s  cond=%s"
              % (r["formula"][:18], r["tc"], f["comp"].get("H", 0) / sum(f["comp"].values()),
                 r["mech"], r["cond"]))
    print("  含H材料数=%d, Tc中位=%.1fK (全样本中位=%.1fK)"
          % (len(hmat),
             statistics.median([r["tc"] for r, _ in hmat]) if hmat else 0,
             statistics.median([r["tc"] for r, _ in data])))


if __name__ == "__main__":
    main()
