# -*- coding: utf-8 -*-
"""R45：七纯数的生成元结构（指数矩阵与封闭性）。"""
import csv
import math
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import numpy as np

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(OUT, "..", "..", ".."))
GAMMA = 0.5772156649015329
ZETA3 = 1.2020569031595943


def main():
    ledger = open(os.path.join(ROOT, "10 探索", "超导第一性研究", "00_当前有效口径表.md"),
                  encoding="utf-8").read()
    checks = {
        "R6": "2.77069" in ledger,
        "SJ": "2.659919" in ledger or "4\\pi e^\\gamma" in ledger,
        "五纯数": "五纯数一致性网络" in ledger,
    }
    assert all(checks.values()), "P1: %s" % checks

    R1 = 2 * math.pi / math.exp(GAMMA)
    R2 = 12 / (7 * ZETA3)
    R3 = 2 * math.sqrt(math.pi)
    R4 = 3 / (4 * math.exp(2 * GAMMA))
    kap = 2 * math.sqrt(2) * math.exp(GAMMA) / math.sqrt(7 * ZETA3)
    R6 = math.pi ** 2 / (2 * math.exp(GAMMA))
    SJ = 4 * math.pi * math.exp(GAMMA) / (7 * ZETA3)

    # 指数矩阵（pi, e^gamma, zeta3）
    M = np.array([
        [1, -1, 0],
        [0, 0, -1],
        [0.5, 0, 0],
        [0, -2, 0],
        [0, 1, -0.5],
        [2, -1, 0],
        [1, 1, -1],
    ], dtype=float)
    rank = np.linalg.matrix_rank(M)
    assert rank == 3, "P3: 秩 %d" % rank

    # 由 R1,R2,R3 生成其余四个
    derived = {
        "R4 = 3 R1^2 / R3^4": abs(R4 - 3 * R1 ** 2 / R3 ** 4),
        "kappa = R3^2 sqrt(R2)/(R1 sqrt(6))": abs(kap - R3 ** 2 * math.sqrt(R2) / (R1 * math.sqrt(6))),
        "R6 = R1 R3^2 / 16": abs(R6 - R1 * R3 ** 2 / 16),
        "SJ = R2 R3^4/(24 R1)": abs(SJ - R2 * R3 ** 4 / (24 * R1)),
    }
    for k, v in derived.items():
        assert v < 1e-12, "P4: %s 残差 %.3e" % (k, v)

    print("R45 七纯数结构核对：")
    print("  P1 登记 %s" % checks)
    print("  指数矩阵秩 = %d（生成元 pi, e^gamma, zeta3）" % rank)
    for k, v in derived.items():
        print("    %-38s 残差 %.3e" % (k, v))
    print("  P5 Lean 关键组合恒等式")

    out = os.path.join(OUT, "R45_七纯数生成元结构_摘要.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as fo:
        wr = csv.writer(fo)
        wr.writerow(["纯数", "pi 指数", "e^gamma 指数", "zeta3 指数"])
        names = ["R1", "R2", "R3", "R4", "kappa", "R6", "SJ"]
        wr.writerows([names[i]] + list(M[i]) for i in range(7))
        wr.writerow([])
        for k, v in derived.items():
            wr.writerow([k, "残差", "%.3e" % v])
    print("CSV:", out)


if __name__ == "__main__":
    main()
