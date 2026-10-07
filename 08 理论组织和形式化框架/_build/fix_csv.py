# -*- coding: utf-8 -*-
"""
修复 01_结构化数据/概念表.csv 与 论证表.csv 中未转义的字段内逗号。
受影响行（唯一）：概念表 C004/C020/C062 的 definition；论证表 H003/A004/A020 的 premises|conclusion。
修复方式：仅对这 6 行按显式正确值重建，并以 RFC4180 QUOTE_MINIMAL 重新写出（保留 CRLF、无末尾换行）。
其余行逐字节保持不变（脚本内断言）。
运行：python fix_csv.py
"""
import csv
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S01 = os.path.join(ROOT, "01_结构化数据")

# 显式正确值（依据同文件其他行语义与 03_超图与理论图/CQM_概念关系超图.md 对照）
CONCEPT_FIX = {
    "C004": "(X,≺) 偏序集描述因果",
    "C020": "P(M,G) 主丛",
    "C062": "[û,p̂_u]=i 海森堡对易",
}
ARG_FIX = {
    "H003": ("本征值{9,4,1};S_5表示论", "SU(5)规范群结构"),
    "A004": ("4-单纯形边-面结构", "M=EᵀE本征值{9,4,1}"),
    "A020": ("曲率F", "对易子[L_m,L_n]"),
}

HEAD_CONCEPT = ["concept_id", "name", "type", "definition", "source_doc", "source_loc", "synonyms"]
HEAD_ARG = ["arg_id", "premises", "conclusion", "type", "source_doc", "source_concept"]


def read_rows(name):
    with open(os.path.join(S01, name), "r", encoding="utf-8-sig", newline="") as f:
        return list(csv.reader(f))


def write_rows(name, rows):
    out = "\r\n".join(",".join('"' + c.replace('"', '""') + '"' if ("," in c or '"' in c or "\r" in c or "\n" in c) else c
                             for c in row) for row in rows)
    with open(os.path.join(S01, name), "w", encoding="utf-8", newline="") as f:
        f.write(out)


def fix_concept():
    rows = read_rows("概念表.csv")
    assert rows[0] == HEAD_CONCEPT, rows[0]
    changed = 0
    for i, r in enumerate(rows):
        if i == 0:
            continue
        if r[0] in CONCEPT_FIX:
            # 原始可能为 7（未触发）或 8+（被逗号拆坏）
            r = [r[0], r[1], r[2], CONCEPT_FIX[r[0]]] + r[-3:]
            rows[i] = r
            changed += 1
        else:
            assert len(r) == 7, f"概念表 L{i+1} 字段数 {len(r)} 非 7：{r}"
    assert changed == 3, changed
    write_rows("概念表.csv", rows)
    print(f"[OK] 概念表.csv 修复 {changed} 行")


def fix_arg():
    rows = read_rows("论证表.csv")
    assert rows[0] == HEAD_ARG, rows[0]
    changed = 0
    for i, r in enumerate(rows):
        if i == 0:
            continue
        if r[0] in ARG_FIX:
            p, c = ARG_FIX[r[0]]
            rows[i] = [r[0], p, c] + r[-3:]
            changed += 1
        else:
            assert len(r) == 6, f"论证表 L{i+1} 字段数 {len(r)} 非 6：{r}"
    assert changed == 3, changed
    write_rows("论证表.csv", rows)
    print(f"[OK] 论证表.csv 修复 {changed} 行")


if __name__ == "__main__":
    fix_concept()
    fix_arg()
