# -*- coding: utf-8 -*-
"""
维度 09 · 桥接与翻译
产出（09_桥接与翻译/）：
  符号对照表.csv
  文档间等价映射.csv
  概念Lean物理映射.csv
  翻译规则.md
运行：python build_bridge.py
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S09 = os.path.join(ROOT, "09_桥接与翻译")

SYMBOLS = [
    ("☯", "相变量子", r"\ensuremath{☯}=ξ'(1)/ξ(1)", "数论不变量", "0.02309570897", "D008 §3；D005 §7.1"),
    ("A₄", "4-单纯形嘉当矩阵", r"A_4=\mathrm{Cartan}(\mathrm{SU}(5))", "群论对象", "det=5, tr=8", "D005 §7.1"),
    ("M", "边-面关联矩阵", r"M=E^{\mathsf T}E", "组合矩阵", "eig{9¹4⁴1⁵}", "D005 §7.1"),
    ("G_N", "牛顿引力常数", r"G_N", "物理常数", "构造后验数字校验，待独立复现", "D014 §5"),
    ("κ", "谱修正", r"\kappa=(31+☯)/30", "谱修正因子", "1.03410", "D031 §11"),
    ("λ_c", "Mathieu 临界", r"\lambda_c", "谱临界值", "1.316022911308", "D019 §5"),
    ("𝔠_n", "耦级（配对不变量）", r"\mathfrak c_n=1/4+\gamma_n^2", "谱不变量", "𝔠₁≈0.5211", "D008 §3"),
    ("γ_n", "黎曼零点虚部", r"\gamma_n", "数论谱", "γ₁=14.134725…", "D008 §3"),
    ("I", "Dynkin 指数比", r"I=T(24)/T(8)=5/3", "群论不变量", "1.6667", "D014 §5"),
    ("K_L", "长度量纲转换常数", r"K_L", "量纲转换", "无量纲→L", "D009 §6.3"),
    ("K_M", "质量量纲转换常数", r"K_M=G_N^{-1}", "量纲转换", "L³T⁻²→M", "D009 §6.3"),
    ("K_Q", "电荷量纲转换常数", r"K_Q", "量纲转换", "M^{1/2}L^{3/2}T⁻¹→Q", "D009 §6.3"),
    ("K_Θ", "温度量纲转换常数", r"K_\Theta", "量纲转换", "能量→Θ", "D009 §6.3"),
    ("K_N", "物质的量转换常数", r"K_N=N_A^{-1}", "量纲转换（人为定义）", "无量纲计数→N", "D009 §6.3"),
    ("K_J", "发光强度转换常数", r"K_J", "量纲转换", "→J", "D009 §6.3"),
    ("δ_v", "Regge 顶点角亏", r"\delta_v", "几何量", "——", "D006 §二.5"),
    ("⇒", "重组实现", r"\Rightarrow", "关系算子（多因一果）", "仅表重组实现", "README；术语表"),
    ("→", "演化/映射/极限", r"\to", "关系算子", "一般演化、映射、极限", "README"),
    ("R̂", "自我限制算符", r"\hat{\mathcal R}", "算符", "——", "D007 §9"),
    ("Ŝ₀", "同步/紧化算符", r"\hat{\mathcal S}_0", "算符", "——", "D008 §9"),
    ("Ĥ_HP", "Hilbert–Pólya 谱算符", r"\hat H_{\mathrm{HP}}=\hat D^2+1/4", "算符", "——", "D008 §4"),
]


def main():
    os.makedirs(S09, exist_ok=True)
    concepts = list(csv.DictReader(open(os.path.join(ROOT, "01_结构化数据", "概念表.csv"), encoding="utf-8-sig")))
    args = list(csv.DictReader(open(os.path.join(ROOT, "01_结构化数据", "论证表.csv"), encoding="utf-8-sig")))
    lean_map = list(csv.DictReader(open(os.path.join(ROOT, "04_Lean对接", "Lean↔概念映射.csv"), encoding="utf-8-sig")))

    with open(os.path.join(S09, "符号对照表.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["symbol", "name", "latex", "kind", "value_or_note", "source"])
        w.writerows(SYMBOLS)

    # 等价映射：论证表等价行 + 术语一致清单 §七跨文档差异
    eq = []
    for a in args:
        if a["type"] == "等价":
            eq.append(["论证等价", a["arg_id"], a["premises"], a["conclusion"], a["source_doc"], "论证表"])
    term_notes = [
        ["跨文档命名", "四层 FG 命名", "统一方法论:5,7（元素/分子/晶胞/超导）",
         "FG层级同步算符体系 §2（电子/元素/分子/晶胞）", "D033;D032", "术语一致清单 §七"],
        ["跨文档定义", "主丛四元组", "统一方法论:13（M_ℓ,P_ℓ,π_ℓ,G_ℓ）",
         "FG层级同步算符体系 §3.1（M_ℓ,P(M_ℓ,G_ℓ),A_ℓ,Ŝ_ℓ）", "D033;D032", "术语一致清单 §七"],
        ["跨文档符号", "温度依赖符号", "超导核心理论:483,497（Ω₀）", "超导核心理论:693（θ_D）", "D030", "术语一致清单 §七"],
        ["跨文档口径", "FG 与朗兰兹关系", "FG 纤维丛:383（称完整朗兰兹 GL(n)+GRH）",
         "项目约定：与朗兰兹纲领相关，非完整纲领", "D029", "术语一致清单 §七"],
        ["跨文档语义", "κ 语义", "专题与扩展:541（κ=(31+☯)/30）", "专题与扩展:539(κ_N)、185(条件数 κ_A)", "D031", "术语一致清单 §七"],
        ["缺口表述", "缺口 C", "README/超导§13（退相干稳态恰为 A₄）",
         "因果网络同步理论:243（退相干稳态是 {5,4} 镶嵌）", "D007", "缺口依赖闭包 §七"],
    ]
    with open(os.path.join(S09, "文档间等价映射.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["kind", "key", "side_a", "side_b", "source_doc", "remark"])
        w.writerows(eq + term_notes)

    # 概念 ↔ Lean ↔ 物理
    lean_by_concept = {}
    for r in lean_map:
        for cid in r["concept_ids"].split(";"):
            cid = cid.strip()
            if cid:
                lean_by_concept.setdefault(cid, []).append((r["lean_library"], r["lean_symbol"]))
    with open(os.path.join(S09, "概念Lean物理映射.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["concept_id", "name", "type", "lean_library", "lean_symbol", "physics_role", "source_doc"])
        for c in concepts:
            ll, ls = "", ""
            if c["concept_id"] in lean_by_concept:
                ll, ls = lean_by_concept[c["concept_id"]][0]
            role = {"量纲": "量纲/单位", "物理": "物理量/可观测量", "数论": "数论谱量",
                    "群论": "群结构", "几何": "几何量", "纤维丛": "丛结构"}.get(c["type"], "结构概念")
            w.writerow([c["concept_id"], c["name"], c["type"], ll, ls, role, c["source_doc"]])

    print("[OK] 符号对照表.csv / 文档间等价映射.csv / 概念Lean物理映射.csv")
    print(f"     符号={len(SYMBOLS)} 等价行={len(eq)}+{len(term_notes)} 概念映射={len(concepts)}")


if __name__ == "__main__":
    main()
