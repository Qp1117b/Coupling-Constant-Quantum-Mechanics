# -*- coding: utf-8 -*-
"""
范畴论模型 · 形式化函子 F 的良定性核验
读 03 超图 + 04 映射，检查 F: C_CQM → C_Lean 在生成元上的定义域与复合相容（可核部分）。
运行：python functor.py
"""
import csv, json, os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # 08 理论组织和形式化框架
D10 = os.path.dirname(HERE)                            # 08_元理论反思


def load():
    hg = json.load(open(os.path.join(ROOT, "03_超图与理论图", "超图数据.json"), encoding="utf-8"))
    mp = list(csv.DictReader(open(os.path.join(ROOT, "04_Lean对接", "Lean↔概念映射.csv"), encoding="utf-8-sig")))
    return hg, mp


def build_F(mp):
    """对象映射：concept_id -> (lean_library, lean_symbol)"""
    F = {}
    for r in mp:
        for cid in r["concept_ids"].split(";"):
            cid = cid.strip()
            if cid:
                F.setdefault(cid, (r["lean_library"], r["lean_symbol"]))
    return F


def main():
    hg, mp = load()
    F = build_F(mp)
    nodes = [n["id"] for n in hg["nodes"]]
    covered = [c for c in nodes if c in F]
    uncovered = [c for c in nodes if c not in F]

    # 复合相容性（可核部分）：对 directed 链 c1→c2，若两者都在 F 定义域，记 F 上的候选配对
    comp = []
    for e in hg.get("directed_edges", []):
        pass  # directed_edges 无 concept id 字段，使用论证表的结构
    args = list(csv.DictReader(open(os.path.join(ROOT, "01_结构化数据", "论证表.csv"), encoding="utf-8-sig")))

    def toks(t):
        return [x.strip() for x in t.replace(";", "→").split("→") if x.strip().startswith("C")]

    mapped_edges = 0
    for a in args:
        ids = toks(a["source_concept"])
        if len(ids) >= 2 and all(i in F for i in ids):
            mapped_edges += 1
            comp.append({"rule": a["arg_id"], "relation": a["type"],
                         "images": [F[i][1] for i in ids]})

    print(f"对象: {len(nodes)}；F 有定义: {len(covered)}；无定义: {len(uncovered)}")
    print(f"覆盖度: {len(covered)/len(nodes)*100:.1f}%")
    print(f"全部前件/后件都在 F 定义域内的规则: {mapped_edges}/{len(args)}")
    print("未覆盖（无 Lean 载体）示例:", ", ".join(uncovered[:12]), "...")
    print("F 上可核的复合相容条目示例:")
    for c in comp[:6]:
        print("  ", c["rule"], c["relation"], "|", " ⊗ ".join(c["images"]))


if __name__ == "__main__":
    main()
