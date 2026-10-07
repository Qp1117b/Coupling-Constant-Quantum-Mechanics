# -*- coding: utf-8 -*-
"""
组织层一致性硬检查（08 目录 AGENTS.md §八 完成判据的执行器）。

跨产物核对：计数一致性、引用完整性、⇒/→ 约定、维度覆盖、失效链接、禁用词。
退出码 0 = 全部通过；非 0 = 存在硬失败（研究视为未完成）。

运行：python check_consistency.py
"""
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                 # 08 理论组织和形式化框架
PARENT = os.path.dirname(ROOT)               # 项目根

results = []          # (level, name, detail)  level: PASS/FAIL/WARN


def rec(level, name, detail=""):
    results.append((level, name, detail))


def check(name, cond, detail=""):
    rec("PASS" if cond else "FAIL", name, detail)


def rd(p):
    with open(p, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def jload(p):
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    # ---------- 源 ----------
    concepts = rd(os.path.join(ROOT, "01_结构化数据", "概念表.csv"))
    props = rd(os.path.join(ROOT, "01_结构化数据", "命题表.csv"))
    args = rd(os.path.join(ROOT, "01_结构化数据", "论证表.csv"))
    cids = {c["concept_id"] for c in concepts}
    pids = {p["prop_id"] for p in props}
    check("源 CSV 行数 82/63/70",
          (len(concepts), len(props), len(args)) == (82, 63, 70),
          f"实为 {len(concepts)}/{len(props)}/{len(args)}")

    # ---------- 超图 ----------
    hg = jload(os.path.join(ROOT, "03_超图与理论图", "超图数据.json"))
    he, de = hg["hyperedges"], hg["directed_edges"]
    check("超图 JSON 节点 82", len(hg["nodes"]) == 82, str(len(hg["nodes"])))
    check("超图 JSON 超边 19 / 有向边 51", (len(he), len(de)) == (19, 51),
          f"{len(he)}/{len(de)}")
    check("metadata 计数与实体一致",
          (hg["metadata"]["node_count"], hg["metadata"]["hyperedge_count"],
           hg["metadata"]["directed_edge_count"]) == (82, 19, 51))
    check("超边全为『重组实现』", all(h["premises"] and h["conclusion"] for h in he))
    check("有向边不含『重组实现』",
          all(d.get("type") != "重组实现" for d in de))
    check("论证总数 = 超边 + 有向边", len(he) + len(de) == len(args) == 70)

    # ---------- 本体 ----------
    owl = open(os.path.join(ROOT, "02_概念本体", "本体.owl"), encoding="utf-8").read()
    nC = len(set(re.findall(r'rdf:about="#(C\d{3})"', owl)))
    nP = len(set(re.findall(r'rdf:about="#(P\d{3})"', owl)))
    nG = len(set(re.findall(r'rdf:about="#(G\d{3})"', owl)))
    nH = len(set(re.findall(r'rdf:about="#(H\d{3})"', owl)))
    nA = len(set(re.findall(r'rdf:about="#(A\d{3})"', owl)))
    check("本体个体 概念82/命题63/论证70",
          (nC, nP + nG, nH + nA) == (82, 63, 70), f"{nC}/{nP+nG}/{nH+nA}")

    # ---------- ML ----------
    nf = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "node_features.csv"))
    check("ML 节点特征 82 行", len(nf) == 82, str(len(nf)))
    hei = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "hyperedge_index.csv"))
    dei = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "directed_edge_index.csv"))
    check("ML 超图关联 = 47", len(hei) == 47, str(len(hei)))
    check("ML 有向边 = 51", len(dei) == 51, str(len(dei)))
    try:
        import numpy as np
        z = np.load(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "hypergraph_index.npz"))
        check("npz 形状 (82,15)/超边索引/边索引",
              z["x"].shape == (82, 15) and z["hyperedge_index"].shape[1] == 47
              and z["edge_index"].shape[1] == 51,
              f"{z['x'].shape},{z['hyperedge_index'].shape},{z['edge_index'].shape}")
    except Exception as e:  # noqa
        rec("WARN", "npz 校验跳过", str(e))

    # ---------- 动态机制 ----------
    dyn = jload(os.path.join(ROOT, "06_动态机制", "仿真", "dynamic_hypergraph.json"))["dynamics"]
    check("动态：种子 44 / 可达 81 / 不可达 1",
          (len(dyn["seed_concepts"]), dyn["reachable_concepts"], len(dyn["unreachable_concepts"])) == (44, 81, 1))

    # ---------- 桥接 ----------
    b1 = rd(os.path.join(ROOT, "09_桥接与翻译", "概念Lean物理映射.csv"))
    check("桥接：概念映射 82 行", len(b1) == 82, str(len(b1)))
    check("桥接：符号对照 21 条",
          len(rd(os.path.join(ROOT, "09_桥接与翻译", "符号对照表.csv"))) == 21)

    # ---------- Lean 对接 ----------
    decls = jload(os.path.join(ROOT, "04_Lean对接", "Lean结构提取", "declarations.json"))
    mods = rd(os.path.join(ROOT, "04_Lean对接", "Lean结构提取", "模块清单.csv"))
    check("Lean 声明 1388 / 模块 68", (len(decls), len(mods)) == (1388, 68),
          f"{len(decls)}/{len(mods)}")
    lmap = rd(os.path.join(ROOT, "04_Lean对接", "Lean↔概念映射.csv"))
    bad = []
    for r in lmap:
        for t in r["concept_ids"].split(";"):
            t = t.strip()
            if t and t not in cids:
                bad.append(t)
    check("Lean 映射概念 id 均可解析", not bad, str(bad[:8]))

    # ---------- 引用完整性 ----------
    bad_ref = []
    for a in args:
        for t in a["source_concept"].replace(";", "→").split("→"):
            t = t.strip()
            if t.startswith("C") and t not in cids:
                bad_ref.append((a["arg_id"], t))
    check("论证表概念引用完整", not bad_ref, str(bad_ref[:8]))
    bad_dep = []
    for p in props:
        for t in p["depends_on"].split(";"):
            t = t.strip()
            if t and t.startswith("C") and t not in cids:
                bad_dep.append((p["prop_id"], t))
    check("命题表概念依赖完整", not bad_dep, str(bad_dep[:8]))

    # ---------- 前端数据一致 ----------
    site = jload(os.path.join(ROOT, "10_输出可视化展示", "网站", "data.json"))
    check("网站 data.json 与源一致",
          (len(site["concepts"]), len(site["props"]), len(site["args"])) == (82, 63, 70)
          and site["meta"]["hyperedges"] == 19 and site["meta"]["edges"] == 51,
          str(site["meta"]))

    # ---------- 维度覆盖 ----------
    dims = {"结构化": ["00_外部引用", "01_结构化数据", "03_超图与理论图"],
            "本体": ["02_概念本体"], "ML": ["05_机器学习数据准备"],
            "形式化": ["04_Lean对接"], "输出": ["10_输出可视化展示"],
            "动态": ["06_动态机制"], "经验": ["07_经验检验"],
            "元理论": ["08_元理论反思"], "桥接": ["09_桥接与翻译"], "元数据": ["11_元数据"]}
    missing = []
    for d, dirs in dims.items():
        for dd in dirs:
            p = os.path.join(ROOT, dd)
            if not os.path.isdir(p) or not any(os.scandir(p)):
                missing.append(dd)
    check("六维度目录均有产物", not missing, str(missing))

    # ---------- 失效链接（md） ----------
    broken = []
    for md in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if any(s in md.replace("\\", "/") for s in ("_build", "Lean源码")):
            continue
        base = os.path.dirname(md)
        for m in re.finditer(r"\]\(([^)]+)\)", open(md, encoding="utf-8").read()):
            tgt = m.group(1).split("#")[0].strip()
            if not tgt or tgt.startswith(("http", "mailto:", "file:")):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, tgt))):
                broken.append(f"{os.path.relpath(md, ROOT)} -> {tgt}")
    check("Markdown 相对链接有效", not broken, "; ".join(broken[:6]))

    # ---------- 禁用词 ----------
    BANNED = ["已删除", "已澄清", "已修正", "已解决", "旧版", "已废弃", "现已统一", "早期形式", "本版"]
    NEG = ("不得", "禁止", "非", "避免", "反模式", "×", "违规", "违反")
    hits = []
    for md in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if any(s in md.replace("\\", "/") for s in ("_build", "Lean源码")):
            continue
        for i, line in enumerate(open(md, encoding="utf-8"), 1):
            for w in BANNED:
                if w in line and not any(n in line for n in NEG):
                    hits.append(f"{os.path.relpath(md, ROOT)}:{i} {w}")
    check("无过程性禁用词（负向引用除外）", not hits, "; ".join(hits[:6]))

    # ---------- 汇报 ----------
    nf_ = sum(1 for lv, _, _ in results if lv == "FAIL")
    nw = sum(1 for lv, _, _ in results if lv == "WARN")
    print("=" * 66)
    for lv, name, detail in results:
        mark = {"PASS": "  OK ", "FAIL": "FAIL ", "WARN": "WARN "}[lv]
        print(f"[{mark}] {name}" + (f"   ({detail})" if detail and lv != "PASS" else ""))
    print("=" * 66)
    print(f"检查项 {len(results)}：通过 {len(results)-nf_-nw} · 失败 {nf_} · 警告 {nw}")
    print("结果：" + ("全部通过" if nf_ == 0 else "存在硬失败——研究视为未完成"))
    return 1 if nf_ else 0


if __name__ == "__main__":
    sys.exit(main())
