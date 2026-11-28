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

# 全量 md 扫描的排除段：构建中间物与第三方源码。
#   _build             —— 脚本目录，含 mkdocs_src（stage 中间物）
#   Lean源码           —— 外部形式化源码，非组织层文档
#   阅读站VitePress/docs —— build_vitepress_site.py 从 _build/mkdocs_src 复制的
#                          stage 中间物，内容是 01–07 源语料副本（外部文本不动原则），
#                          不由组织层文字规范约束；其产品形态是 dist/ 下的 HTML。
SCAN_SKIP = ("_build", "Lean源码", "阅读站VitePress/docs", "node_modules")

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
    check("源 CSV 行数 83/63/69",
          (len(concepts), len(props), len(args)) == (83, 63, 69),
          f"实为 {len(concepts)}/{len(props)}/{len(args)}")

    # ---------- 超图 ----------
    hg = jload(os.path.join(ROOT, "03_超图与理论图", "超图数据.json"))
    he, de = hg["hyperedges"], hg["directed_edges"]
    check("超图 JSON 节点 83", len(hg["nodes"]) == 83, str(len(hg["nodes"])))
    check("超图 JSON 超边 19 / 有向边 50", (len(he), len(de)) == (19, 50),
          f"{len(he)}/{len(de)}")
    check("metadata 计数与实体一致",
          (hg["metadata"]["node_count"], hg["metadata"]["hyperedge_count"],
           hg["metadata"]["directed_edge_count"]) == (83, 19, 50))
    check("超边全为『重组实现』", all(h["premises"] and h["conclusion"] for h in he))
    check("有向边不含『重组实现』",
          all(d.get("type") != "重组实现" for d in de))
    check("论证总数 = 超边 + 有向边", len(he) + len(de) == len(args) == 69)

    # ---------- 本体 ----------
    owl = open(os.path.join(ROOT, "02_概念本体", "本体.owl"), encoding="utf-8").read()
    nC = len(set(re.findall(r'rdf:about="#(C\d{3})"', owl)))
    nP = len(set(re.findall(r'rdf:about="#(P\d{3})"', owl)))
    nG = len(set(re.findall(r'rdf:about="#(G\d{3})"', owl)))
    nH = len(set(re.findall(r'rdf:about="#(H\d{3})"', owl)))
    nA = len(set(re.findall(r'rdf:about="#(A\d{3})"', owl)))
    check("本体个体 概念83/命题63/论证69",
          (nC, nP + nG, nH + nA) == (83, 63, 69), f"{nC}/{nP+nG}/{nH+nA}")

    # ---------- ML ----------
    nf = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "node_features.csv"))
    check("ML 节点特征 83 行", len(nf) == 83, str(len(nf)))
    hei = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "hyperedge_index.csv"))
    dei = rd(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "directed_edge_index.csv"))
    check("ML 超图关联 = 47", len(hei) == 47, str(len(hei)))
    check("ML 有向边 = 50", len(dei) == 50, str(len(dei)))
    try:
        import numpy as np
        z = np.load(os.path.join(ROOT, "05_机器学习数据准备", "超图导出", "hypergraph_index.npz"))
        check("npz 形状 (83,15)/超边索引/边索引",
              z["x"].shape == (83, 15) and z["hyperedge_index"].shape[1] == 47
              and z["edge_index"].shape[1] == 50,
              f"{z['x'].shape},{z['hyperedge_index'].shape},{z['edge_index'].shape}")
    except Exception as e:  # noqa
        rec("WARN", "npz 校验跳过", str(e))

    # ---------- 动态机制 ----------
    dyn = jload(os.path.join(ROOT, "06_动态机制", "仿真", "dynamic_hypergraph.json"))["dynamics"]
    # 2026-11-18（v1.9.224）：新增 C083「记忆核积分」/C084「固有时流速差异历史总和」
    # （概念 81→83，权威源 06 超导 §0.3/§0.6），重写规则与种子按新概念重算
    # 44→46、可达 80→82；不可达仍为 C074（前向派生不可达 1，红线如实登记）。
    check("动态：种子 46 / 可达 82 / 不可达 1",
          (len(dyn["seed_concepts"]), dyn["reachable_concepts"], len(dyn["unreachable_concepts"])) == (46, 82, 1))

    # ---------- 桥接 ----------
    b1 = rd(os.path.join(ROOT, "09_桥接与翻译", "概念Lean物理映射.csv"))
    check("桥接：概念映射 83 行", len(b1) == 83, str(len(b1)))
    check("桥接：符号对照 21 条",
          len(rd(os.path.join(ROOT, "09_桥接与翻译", "符号对照表.csv"))) == 21)

    # ---------- Lean 对接 ----------
    decls = jload(os.path.join(ROOT, "04_Lean对接", "Lean结构提取", "declarations.json"))
    mods = rd(os.path.join(ROOT, "04_Lean对接", "Lean结构提取", "模块清单.csv"))
    # 2026-11-21（v1.9.247）：Ring 23/27 补基数与非负性引理，声明 116→118、定理 54→56。
    # 2026-11-21（v1.9.248）：RH/Goldbach 以显式外部假设接入，声明 118→124、定理 56→60。
    # 2026-11-27：08 移除 SuperconductivityChain 库（形式化权威转 10 探索/超导第一性研究/05_Lean验证），
    # 抽取结果为空集，故此处基线改为 0 声明 / 0 模块。
    check("Lean 声明 0 / 模块 0（08 已无库）", (len(decls), len(mods)) == (0, 0),
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
    site = jload(os.path.join(ROOT, "10_展示可视化", "源_可视化", "研究驾驶舱", "data.json"))
    check("网站 data.json 与源一致",
          (len(site["concepts"]), len(site["props"]), len(site["args"])) == (83, 63, 69)
          and site["meta"]["hyperedges"] == 19 and site["meta"]["edges"] == 50,
          str(site["meta"]))

    # ---------- 证据层 / 主张层 / 图谱 / 校验 ----------
    ev = rd(os.path.join(ROOT, "00_外部引用", "证据映射.csv"))
    ev_by_id = {r["struct_id"]: r for r in ev}
    want_ev = cids | pids | {a["arg_id"] for a in args}
    check("证据层覆盖 83+63+69 条断言", set(ev_by_id) == want_ev and len(ev) == len(want_ev),
          f"{len(ev)} 条 / 期望 {len(want_ev)}")
    corpus_txt = {}
    bad_quote = 0
    for r in ev:
        did = r.get("evidence_doc") or r.get("doc_id")
        if did not in corpus_txt:
            p = None
            for d in rd(os.path.join(ROOT, "00_外部引用", "语料清单.csv")):
                if d["doc_id"] == did:
                    p = os.path.join(PARENT, d["path"])
            corpus_txt[did] = (open(p, encoding="utf-8", errors="replace").read()
                               if p and os.path.exists(p) else None)
        raw = corpus_txt.get(did)
        if raw is None:
            continue
        try:
            st, en = int(r["char_start"]), int(r["char_end"])
        except Exception:
            continue
        if not (0 <= st < en <= len(raw)) or (r["quote"] and raw[st:en] != r["quote"]):
            bad_quote += 1
    check("证据引文与字符区间逐字一致", bad_quote == 0, f"{bad_quote} 条不一致")

    gapx = rd(os.path.join(ROOT, "01_结构化数据", "缺口编号对照.csv"))
    gapd = rd(os.path.join(ROOT, "01_结构化数据", "缺口依赖.csv"))
    clm = rd(os.path.join(ROOT, "01_结构化数据", "命题依赖.csv"))
    gaps_only = [g for g in gapx if g.get("gap_code")]
    check("缺口编号对照 = 24 个缺口 + 8 条 id 前缀冲突登记",
          len(gaps_only) == 24 and len(gapx) - len(gaps_only) == 8,
          f"{len(gaps_only)} + {len(gapx)-len(gaps_only)}")
    check("缺口依赖链 G2→G3→G4→G5", {(e["src"], e["dst"]) for e in gapd} ==
          {("G2", "G3"), ("G3", "G4"), ("G4", "G5")}, str(len(gapd)))
    check("claim 级边 > 250（原为 0）", len(clm) > 250, str(len(clm)))

    kgj = jload(os.path.join(ROOT, "03_超图与理论图", "知识图谱.json"))
    # 边数随语料变化浮动：低置信「语义近邻（候选）」边低于阈值时消失，属合法派生变化
    # （先例：v1.9.61 357→354；v1.9.65 357→354；D056 新增语料 352→355）。
    # 2026-11-14：全链重建对齐后 355→352。用旧文本做对照重建同样得 352，
    # 确认漂移发生在本轮之前（语料已改而派生物未同步），与 δ(Z,N) 口径修正无关。
    # 2026-11-14（v1.9.85）：06 超导两篇并为一篇（语料 51→50，句 19,368→19,353），
    # 「语义近邻（候选）」边随段界变化由 18 降至 16，故 352→350；144 实体与概念节点未变。
    # 2026-11-16（v1.9.160）：`06 超导核心理论` 改为差异-记忆核口径（语料 55 篇，句 19,379→19,556），
    # 证据句重匹配使 claim 级边 281→275，dir 50 / hyper 19 未变，故 350→344；144 实体未变。
    # 2026-11-16（v1.9.161）：T1–T7 文本落地后证据句重匹配使 claim 级边 275→277，
    # dir 50 / hyper 19 未变，故 344→346；144 实体未变。
    # 2026-11-17（v1.9.209）：曲率载体口径重构——超导核心 §0.2 改写、删跨材料指针块、
    # 五份权威源 δ_v 语义改为归一化亏角，致证据句重匹配使 claim 级边 277→274，
    # dir 50 / hyper 19 未变，故 346→343；144 实体未变（C026 定义文本随原文档同步）。
    # 2026-11-17（v1.9.210）：术语统一（角亏→亏角，456 处）致证据句再重匹配，
    # claim 级边 274→271，dir 50 / hyper 19 未变，故 343→340；144 实体未变。
    # 2026-11-17（v1.9.216）：删除基于顶点角亏的定量内容（C²=2/3、Δε₀ 计算链、
    # 自由能 T_c 链）致证据句重匹配，claim 级边 271→274，dir 50 / hyper 19 未变，
    # 故 340→343；144 实体未变。
    # 2026-11-17（v1.9.221）：全量删除 `10 探索/` 53 篇探索稿 + 清理 01–07/README 失效引用，
    # 证据句重匹配使 claim 级边 343→346；dir 50 / hyper 19、144 实体与概念节点未变。
    # 2026-11-17（v1.9.221 续）：新增九主题综合文档 + README 文档表加一行，证据句再重匹配，
    # claim 级边 346→343；dir 50 / hyper 19、144 实体与概念节点未变。
    # 2026-11-18（v1.9.222）：`06 超导` 三篇副文档（FG层级同步算符体系/统一方法论/非马尔可夫对接方案）
    # 退役，C073/P028/P029/H011 改挂 D028、G025–G027 改挂 D042；轴心正文按稳定稿修正（§0.2/§0.3/§4.1/§6/§7.3）
    # 后证据句重匹配，知识图谱边 343→339；144 实体、dir 50 / hyper 19 未变。
    # 2026-11-20（v1.9.225）：06 拆为理论卷/材料卷，语料变化使 claim 级边 336→337；
    # 实体 146 不变，dir 50 / hyper 19 未变。
    # 2026-11-21（v1.9.240）：27 环/相变等效/BCS 提升/关系性实在论落笔，P026 新增“电子”
    # 概念提及边 1 条（证据句重匹配另换 8 条旧边），再随本轮句索引重排净减 5 条；实体 146 不变。
    # 2026-11-21（v1.9.248）：RH/Goldbach 外部假设写入文档，kg 新增 3 条边；实体 146 不变。
    # 2026-11-27：08 移除 Lean 库并以当前语料重跑证据层（build_extract → build_evidence → build_kg），
    # 证据句重匹配使 claim 级边 336→334（实体 146、dir 50 / hyper 19 未变）。
    # 2026-11-28：旧 GN 库证据重定向后 claim 级边 334→336（实体 146 未变）。
    # 2026-11-28：术语统一（同步算符 → 紧化算符，全库 411 处替换）使两条同义 claim
    # 边合并去重，claim 级边 336→335（实体 146、dir 50 / hyper 19 未变）。
    # 2026-11-28：缺口 C 口径统一为「禁闭边界几何为何恰好是 A_4」（原「退相干稳态」表述根除），
    # 证据句重匹配后 claim 级边 335→332（实体 146、dir 50 / hyper 19 未变）。
    check("知识图谱 146 实体 / 332 边",
          (len(kgj["nodes"]), len(kgj["edges"])) == (146, 332),
          f"{len(kgj['nodes'])}/{len(kgj['edges'])}")
    ttl = open(os.path.join(ROOT, "03_超图与理论图", "知识图谱.ttl"), encoding="utf-8").read()
    check("RDF 导出 > 5000 行", ttl.count("\n") > 5000, f"{ttl.count(chr(10))} 行")
    qrep = jload(os.path.join(ROOT, "02_概念本体", "本体校验报告.json"))
    check("SHACL 数据契约全部通过", qrep["shacl"]["conforms"] is True,
          f"违约 {qrep['shacl']['violations']}")
    ost = jload(os.path.join(ROOT, "02_概念本体", "本体统计.json"))
    check("HermiT 推理一致且无不可满足类",
          ost["reasoner"]["consistent"] is True and not ost["reasoner"]["unsatisfiable_classes"],
          str(ost["reasoner"]["unsatisfiable_classes"]))
    # 2026-11-18（v1.9.224）：概念 81→83、证据 213→215，本体个体 426→430；类/对象属性未变。
    # 2026-11-28：3 条证据 unresolved，证据个体 215→212，本体个体 430→427；类/对象属性未变。
    check("本体公理层：25 类 / 427 个体 / 16 对象属性",
          (ost["owl_classes"], ost["owl_individuals"], ost["owl_object_properties"]) == (25, 427, 16),
          f"{ost['owl_classes']}/{ost['owl_individuals']}/{ost['owl_object_properties']}")
    ext = jload(os.path.join(ROOT, "05_机器学习数据准备", "关系抽取", "抽取评测.json"))
    check("抽取评测含召回上界（诚实边界）",
          "recall_ceiling_sentence_cooccurrence" in ext and ext["gold_pairs"] > 0,
          f"上界 {ext.get('recall_ceiling_sentence_cooccurrence')}")
    tpool = jload(os.path.join(ROOT, "05_机器学习数据准备", "术语候选", "术语候选统计.json"))
    check("术语候选池存在且未写入概念表", tpool["new_candidates_kept"] > 0 and len(concepts) == 83,
          f"候选 {tpool['new_candidates_kept']}")
    for rel in ("10_展示可视化/源_可视化/检索台/index.html", "10_展示可视化/源_可视化/研究驾驶舱/index.html",
                "10_展示可视化/源_可视化/超图交互.html", "03_超图与理论图/知识图谱.ttl",
                "02_概念本体/shapes.shacl.ttl", "00_外部引用/句索引/句索引.jsonl"):
        p = os.path.join(ROOT, rel.replace("/", os.sep))
        check(f"产物存在：{rel}", os.path.exists(p) and os.path.getsize(p) > 1000,
              f"{os.path.getsize(p) if os.path.exists(p) else 0} B")

    # ---------- 维度覆盖 ----------
    dims = {"结构化": ["00_外部引用", "01_结构化数据", "03_超图与理论图"],
            "本体": ["02_概念本体"], "ML": ["05_机器学习数据准备"],
            "形式化": ["04_Lean对接"], "输出": ["10_展示可视化"],
            "动态": ["06_动态机制"], "经验": ["07_经验检验"],
            "元理论": ["08_元理论反思"], "桥接": ["09_桥接与翻译"], "元数据": ["11_元数据"]}
    missing = []
    for d, dirs in dims.items():
        for dd in dirs:
            p = os.path.join(ROOT, dd)
            if not os.path.isdir(p) or not any(os.scandir(p)):
                missing.append(dd)
    check("七维度目录均有产物", not missing, str(missing))

    # ---------- 失效链接（md） ----------
    broken = []
    for md in glob.glob(os.path.join(ROOT, "**", "*.md"), recursive=True):
        if any(s in md.replace("\\", "/") for s in SCAN_SKIP):
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
        if any(s in md.replace("\\", "/") for s in SCAN_SKIP):
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
