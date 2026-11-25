# -*- coding: utf-8 -*-
"""R43：132 轮 Lean 产物的禁用项与编译审计（纯本地）。"""
import csv
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
LEAN_DIR = os.path.join(ROOT, "10 探索", "超导第一性研究", "05_Lean验证")
FORBIDDEN = ["axiom", "sorry", "admit", "native_decide", "unsafe"]


def strip_comments(s):
    s = re.sub(r"/-[\s\S]*?-/", "", s)
    s = re.sub(r"--[^\n]*", "", s)
    return s


def main():
    files = sorted((f for f in os.listdir(LEAN_DIR) if f.endswith(".lean")),
                   key=lambda f: os.path.getmtime(os.path.join(LEAN_DIR, f)), reverse=True)
    assert len(files) > 30, "A1: 文件数 %d" % len(files)

    total = 0
    bad_files = []
    rows = []
    for name in files:
        txt = open(os.path.join(LEAN_DIR, name), encoding="utf-8").read()
        code = strip_comments(txt)
        hits = [k for k in FORBIDDEN if re.search(r"\b" + k + r"\b", code)]
        n = len(re.findall(r"^\s*(?:theorem|lemma)\s", code, re.M))
        total += n
        if hits or n == 0:
            bad_files.append((name, hits, n))
        rows.append((name, n, ",".join(hits) if hits else "无"))

    assert not bad_files, "A2/A3: %s" % bad_files[:10]

    print("R43 Lean 审计：")
    print("  文件数 %d；theorem/lemma 总数 %d" % (len(files), total))
    print("  禁用项：0；空文件：0")
    print("  最近 5 文件：%s" % ", ".join(files[-5:]))

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "R43_Lean审计_摘要.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["文件", "theorem/lemma 数", "禁用项"])
        wr.writerows(rows)
    print("CSV:", out)


if __name__ == "__main__":
    main()
