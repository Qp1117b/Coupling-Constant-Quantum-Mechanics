# -*- coding: utf-8 -*-
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
