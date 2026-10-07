# -*- coding: utf-8 -*-
"""
维度 05 · 动态机制
把论证表转成重写系统，做前向派生（forward chaining）仿真，记录派生轨迹与动态超图。
产出（06_动态机制/）：
  演化模型/理论状态模型.md
  演化模型/初始状态.json
  重写规则/重写规则.json
  重写规则/重写规则.md
  仿真/simulate.py
  仿真/derivation_trace.csv
  仿真/derivation_order.csv
  仿真/dynamic_hypergraph.json
  仿真/README.md
运行：python build_dynamics.py
"""
import csv
import json
import os
from collections import defaultdict, deque

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")
S03 = os.path.join(ROOT, "03_超图与理论图")
S06 = os.path.join(ROOT, "06_动态机制")


def read_csv(p):
    with open(p, "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def toks(txt):
    return [t.strip() for t in txt.replace(";", "→").split("→") if t.strip().startswith("C")]


# 参与前向派生的关系类型（等价 = 双向/同一对象，不产生新可派生节点）
DERIVE_TYPES = {"重组实现", "演化", "映射", "依赖", "层级含于"}


def main():
    for d in ["演化模型", "重写规则", "仿真"]:
        os.makedirs(os.path.join(S06, d), exist_ok=True)
    concepts = read_csv(os.path.join(S01, "概念表.csv"))
    args = read_csv(os.path.join(S01, "论证表.csv"))
    cname = {c["concept_id"]: c["name"] for c in concepts}
    ctype = {c["concept_id"]: c["type"] for c in concepts}

    rules = []
    for a in args:
        if a["type"] not in DERIVE_TYPES:
            continue
        ids = toks(a["source_concept"])
        if len(ids) < 2:
            continue
        rules.append({
            "rule_id": a["arg_id"],
            "relation": a["type"],
            "lhs": ids[:-1],
            "rhs": ids[-1],
            "premises_text": [x.strip() for x in a["premises"].split(";") if x.strip()],
            "conclusion_text": a["conclusion"],
            "source_doc": [d.strip() for d in a["source_doc"].split(";") if d.strip()],
            "is_recomposition": a["type"] == "重组实现",
        })

    # 种子：不作为任何规则后件的概念（即论证表中的"基元/接口"概念），全部纳入初值
    targets = {r["rhs"] for r in rules}
    seed_set = [c["concept_id"] for c in concepts if c["concept_id"] not in targets]

    # ---- 前向派生 ----
    available = set(seed_set)
    depth = {c: 0 for c in seed_set}
    order = []
    trace = []
    step = 0
    frontier = set(seed_set)
    while True:
        fired = []
        for r in rules:
            if r["rhs"] in available:
                continue
            if all(p in available for p in r["lhs"]):
                fired.append(r)
        if not fired:
            break
        step += 1
        for r in fired:
            nd = max((depth.get(p, 0) for p in r["lhs"]), default=0) + 1
            depth[r["rhs"]] = min(depth.get(r["rhs"], 10**9), nd)
            available.add(r["rhs"])
            order.append({"order": len(order) + 1, "step": step, "rule_id": r["rule_id"],
                          "relation": r["relation"], "rhs": r["rhs"], "rhs_name": cname[r["rhs"]],
                          "depth": nd, "lhs": ";".join(r["lhs"])})
            trace.append((r, nd, step))

    with open(os.path.join(S06, "仿真", "derivation_trace.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "rule_id", "relation", "premises", "conclusion", "conclusion_id", "depth", "source_doc"])
        for r, nd, st in trace:
            w.writerow([st, r["rule_id"], r["relation"], ";".join(r["lhs"]), r["conclusion_text"],
                        r["rhs"], nd, ";".join(r["source_doc"])])
    with open(os.path.join(S06, "仿真", "derivation_order.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["order", "step", "rule_id", "relation", "rhs", "rhs_name", "depth", "lhs"])
        w.writeheader()
        w.writerows(order)

    with open(os.path.join(S06, "重写规则", "重写规则.json"), "w", encoding="utf-8") as f:
        json.dump({"format": "CQM rewrite system / forward-chaining",
                   "derive_types": sorted(DERIVE_TYPES),
                   "note": "规则 lhs ⊆ 已有概念 ⇒ 派生出 rhs；对应论证表行，不改写理论内容。",
                   "seed_concepts": seed_set, "rules": rules}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(S06, "演化模型", "初始状态.json"), "w", encoding="utf-8") as f:
        json.dump({
            "state": {"concepts_available": seed_set,
                      "concepts_available_names": [cname[c] for c in seed_set],
                      "props_closed": [], "gaps_closed": []},
            "rationale": "种子取论证表中不作为任何规则后件的概念（基元/接口概念）。",
        }, f, ensure_ascii=False, indent=2)

    # 动态超图：标注派生深度与顺序
    hg = json.load(open(os.path.join(S03, "超图数据.json"), encoding="utf-8"))
    for n in hg["nodes"]:
        n["derive_depth"] = depth.get(n["id"])
        n["reachable_from_seed"] = n["id"] in available
    hg["dynamics"] = {
        "seed_concepts": seed_set,
        "steps": step,
        "fired_rules": len(order),
        "reachable_concepts": len(available),
        "unreachable_concepts": sorted(set(cname) - available),
        "max_depth": max(depth.values()) if depth else 0,
    }
    with open(os.path.join(S06, "仿真", "dynamic_hypergraph.json"), "w", encoding="utf-8") as f:
        json.dump(hg, f, ensure_ascii=False, indent=2)

    write_docs(seed_set, cname, rules, order, depth, available, step, ctype)

    print(f"[OK] rules={len(rules)} seeds={len(seed_set)} steps={step} fired={len(order)} reachable={len(available)}/{len(cname)}")
    print("     不可达:", sorted(set(cname) - available))


def write_docs(seed_set, cname, rules, order, depth, available, step, ctype):
    with open(os.path.join(ROOT, "06_动态机制", "重写规则", "重写规则.md"), "w", encoding="utf-8") as f:
        f.write(f"""# CQM 重写系统（动态机制 · 重写规则）

> 把 `01_结构化数据/论证表.csv` 的论证行翻译为**前向重写规则**：`lhs ⊆ 已有概念 ⇒ 派生 rhs`。
> 规则不引入理论外内容，`⇒` 与 `→` 保持权威区分；规则数 {len(rules)}。

## 一、规则格式

```json
{{ "rule_id": "H016", "relation": "重组实现",
  "lhs": ["C056","C057","C048","C047","C058"], "rhs": "C081",
  "premises_text": [...], "conclusion_text": "$G_N$", "source_doc": ["D019","D014"] }}
```

| 字段 | 含义 |
|:---|:---|
| `rule_id` | 论证表行号（H0xx 超边 / A0xx 二元边） |
| `relation` | 重写关系类型；参与派生的类型：{ "、".join(sorted(DERIVE_TYPES)) } |
| `lhs` | 前件概念 id 集合（多集，对应 `⇒` 的多因） |
| `rhs` | 后件概念 id |
| `is_recomposition` | 是否 `⇒` 重组实现 |

> **等价**关系是"同一对象两种诠释"，不产生新的可派生节点，故不参与前向派生。

## 二、规则统计

| 关系 | 条数 |
|:---|:---:|
""" + "".join(f"| {rt} | {sum(1 for r in rules if r['relation']==rt)} |\n" for rt in sorted({r['relation'] for r in rules})) + f"""
## 三、派生轨迹

- 种子概念 {len(seed_set)} 个；前向派生 {step} 轮，触发 {len(order)} 条规则；可达概念 {len(available)} 个。
- 完整轨迹见 `../仿真/derivation_trace.csv`；动态超图（含 `derive_depth`）见 `../仿真/dynamic_hypergraph.json`。
""")

    with open(os.path.join(ROOT, "06_动态机制", "演化模型", "理论状态模型.md"), "w", encoding="utf-8") as f:
        f.write(f"""# CQM 理论状态模型（动态机制 · 演化模型）

> 把 CQM 理论组织系统建模为**可演化的状态向量**，刻画"理论如何随时间被扩展、修正"。
> 状态取自现有结构化数据，不预测理论结论。

## 一、状态向量

理论在时刻 $t$ 的状态 $s_t$ 由四元组刻画：

$$s_t = \\bigl(\\mathcal K_t,\\ \\mathcal P_t,\\ \\mathcal G_t,\\ \\mathcal L_t\\bigr)$$

| 分量 | 含义 | 当前取值 | 数据源 |
|:---|:---|:---|:---|
| $\\mathcal K_t$ | 概念集 | 82 | `01_结构化数据/概念表.csv` |
| $\\mathcal P_t$ | 命题集（含定理/假设/构造/猜想） | 63 | `01_结构化数据/命题表.csv` |
| $\\mathcal G_t$ | 缺口集及其状态 | 24（含闭合/未闭合/axiom） | `01_结构化数据/缺口依赖闭包.md` |
| $\\mathcal L_t$ | Lean 形式化状态 | 68 模块 / 1388 声明 | `04_Lean对接/Lean结构提取/` |

## 二、转移算子（演化事件）

| 事件 | 记号 | 语义 | 约束 |
|:---|:---|:---|:---|
| 加概念 | $\\mathcal K_{{t+1}}=\\mathcal K_t\\cup\\{{c\\}}$ | 纳入新概念 | 须有 `source_doc` 出处 |
| 加命题 | $\\mathcal P_{{t+1}}=\\mathcal P_t\\cup\\{{p\\}}$ | 新增命题/定理 | 须标 `status` |
| 闭缺口 | $g:\\ \\text{{待证明}}\\to\\text{{闭合}}$ | 缺口闭合 | 须有 Lean 见证或严格证明 |
| 开缺口 | $g'\\notin\\mathcal G_t$ | 新登记缺口 | 保留编号 |
| 形式化 | $\\mathcal L_{{t+1}}=\\mathcal L_t\\cup\\{{\\text{{decl}}\\}}$ | 新增 Lean 声明 | 禁 `sorry`/`admit` |

转移须满足**单调扩充**：已闭合缺口不得回退为未闭合，已证定理不得降为公理。

## 三、当前初始状态

见 `初始状态.json`：种子概念 {len(seed_set)} 个（结构根），前向派生可达 {len(available)}/82 个概念。

## 四、与重写系统的接口

重写规则（`../重写规则/重写规则.json`）刻画概念的**派生可达性**；状态转移刻画命题与缺口层面的事件。二者正交：前者给出"从根概念能推出什么"，后者给出"理论被怎样修订"。
""")

    with open(os.path.join(ROOT, "06_动态机制", "仿真", "README.md"), "w", encoding="utf-8") as f:
        f.write(f"""# 动态机制 · 仿真

> 以 `../重写规则/重写规则.json` 为规则库，做前向派生（forward chaining）仿真。

## 一、运行

```bash
python simulate.py            # 复算派生轨迹并校验与已生成 CSV 一致
```

## 二、算法

1. 种子 $S_0$：论证表中不作为任何规则后件的概念（基元/接口概念）（{len(seed_set)} 个）。
2. 迭代：若规则 `lhs ⊆ available` 且 `rhs ∉ available`，则派生 `rhs`，记 `depth = max(depth(lhs)) + 1`。
3. 至不动点终止。

## 三、结果

- 派生轮数 {step}；触发规则 {len(order)} 条；可达概念 {len(available)}/82。
- 不可达概念（需理论外输入或为终端/接口概念）：见 `dynamic_hypergraph.json` → `dynamics.unreachable_concepts`。

## 四、产物

| 文件 | 内容 |
|:---|:---|
| `derivation_trace.csv` | 每步触发的规则、前件、后件、深度 |
| `derivation_order.csv` | 节点派生顺序与深度 |
| `dynamic_hypergraph.json` | 超图 + `derive_depth` 标注 |
""")

    with open(os.path.join(ROOT, "06_动态机制", "仿真", "simulate.py"), "w", encoding="utf-8") as f:
        f.write('''# -*- coding: utf-8 -*-
"""重写系统前向派生仿真：读 重写规则/重写规则.json，复算轨迹并与 derivation_trace.csv 比对。"""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
RULES = json.load(open(os.path.join(HERE, "..", "重写规则", "重写规则.json"), encoding="utf-8"))

def forward_chain(rules, seeds):
    avail, order, frontier = set(seeds), [], set(seeds); step = 0
    while True:
        fired = [r for r in rules if r["rhs"] not in avail and all(p in avail for p in r["lhs"])]
        if not fired: break
        step += 1
        for r in fired:
            avail.add(r["rhs"]); order.append((step, r["rule_id"], r["rhs"]))
    return avail, order

if __name__ == "__main__":
    avail, order = forward_chain(RULES["rules"], RULES["seed_concepts"])
    print(f"steps -> fired {len(order)} rules, reachable {len(avail)} concepts")
    csv_path = os.path.join(HERE, "derivation_trace.csv")
    if os.path.exists(csv_path):
        rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
        ok = len(rows) == len(order) and all(
            rows[i]["rule_id"] == order[i][1] for i in range(len(order)))
        print("trace consistent:", ok)
''')


if __name__ == "__main__":
    main()
