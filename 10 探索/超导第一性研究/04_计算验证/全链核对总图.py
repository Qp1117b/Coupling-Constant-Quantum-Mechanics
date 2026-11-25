# -*- coding: utf-8 -*-
"""
R12: 十二轮候选研究诚实总账总图——有效/作废/开放的分布与轮次时间线。
只汇总状态，不拟合。仅用 matplotlib。
运行：python "10 探索/超导第一性研究/04_计算验证/全链核对总图.py"
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))
ROUNDS = list(range(1, 13))
STATUS = ["有效", "作废", "作废", "有效", "有效", "有效",
          "有效", "有效", "作废", "有效", "有效", "有效"]
LABELS = ["R1 λ几何", "R2 Cooper对数", "R3 全链拉通", "R4 模和no-go",
          "R5 DOS形状", "R6 数据对照", "R7 热核no-go", "R8 不可能性",
          "FE09 旧(作废)", "R10 核修正", "R11 证伪判别", "R12 总账"]

COLORS = {"有效": "tab:green", "作废": "tab:red", "开放": "tab:gray"}


def main():
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) 有效/作废计数
    ax = axes[0, 0]
    eff = STATUS.count("有效")
    ret = STATUS.count("作废")
    ax.bar(["有效成果", "作废/回改"], [eff, ret],
           color=[COLORS["有效"], COLORS["作废"]])
    for i, v in enumerate([eff, ret]):
        ax.text(i, v + 0.2, str(v), ha="center", fontsize=11)
    ax.set_ylabel("轮数")
    ax.set_title("(a) 12 轮：有效 9、作废 3")
    ax.grid(alpha=0.3, axis="y")

    # (b) 轮次状态时间线
    ax = axes[0, 1]
    ys = [1 if s == "有效" else 0 for s in STATUS]
    ax.bar(ROUNDS, ys, color=[COLORS[s] for s in STATUS])
    ax.set_xticks(ROUNDS)
    ax.set_xlabel("轮次")
    ax.set_ylabel("有效=1 / 作废=0")
    ax.set_title("(b) 各轮状态（R2/R3/FE09旧 作废）")
    ax.grid(alpha=0.3, axis="y")

    # (c) 链能给的 vs 不能给的
    ax = axes[1, 0]
    labels = ["零点结构", "形状同形", "对数", "费米热核", "隙方程", "绝对能标"]
    vals = [1, 1, 0, 0, 0, 0]
    cols = [COLORS["有效"] if v else COLORS["作废"] for v in vals]
    ax.barh(labels, vals, color=cols)
    ax.set_xlabel("链内可提供？")
    ax.set_title("(c) R8 定理：后四项均外生")
    ax.grid(alpha=0.3, axis="x")

    # (d) 候选理论状态
    ax = axes[1, 1]
    labels = ["FE09 阈值超导", "精密数据支持度", "闭环需求"]
    vals = [1, 0.2, 1]  # 示意：候选存在、数据支持弱、需授权/实验
    ax.bar(labels, vals, color=["tab:purple", "tab:orange", "tab:gray"])
    ax.set_ylabel("程度（示意）")
    ax.set_title("(d) FE09：候选在、证据不足、需判别实验")
    ax.grid(alpha=0.3, axis="y")

    fig.suptitle("R12: 十二轮候选研究诚实总账（有效 9 / 作废 3）", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    png = os.path.join(HERE, "全链核对总图.png")
    fig.savefig(png, dpi=140)
    plt.close(fig)
    print(f"图像: {png}")


if __name__ == "__main__":
    main()
