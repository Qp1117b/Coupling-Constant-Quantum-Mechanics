# Julia / Catlab 草稿 · 组织多范畴的生成元
# 依赖：using Catlab（Julia 包）。本文件为结构草稿，不参与 CQM 构建流程。
# 对应 ../范畴论模型.md §一：对象 = 概念，多元态射 = 重组实现 ⇒。

using Catlab
using Catlab.Theories

# ---- 对象（概念类型层） ----
# 用 AbstractCategory 的自由生成表述组织层类型骨架；具体 82 个体见 03_超图数据.json。

@present SchSig(FreeSchema) begin
    # 概念
    Concept::Ob
    # 命题
    Prop::Ob
    # 关系类型（六类）
    Rel::Ob
    # 生成态射：关系连接概念
    src::Hom(Rel, Concept)
    dst::Hom(Rel, Concept)
    # 超边：n 元态射的显式重ified 表示
    Hyperedge::Ob
    name::Hom(Hyperedge, Rel)
end

@acset_type Sig(SchSig, index=[:src, :dst])

# ---- 多元态射读法 ----
# 重组实现 ⇒ : (c1,...,cn) → c  对应多范畴的 n 元操作；
# 在 Catlab 中可用 Catlab.Theories 的多范畴/操作范畴（operad）表述：
#   op : (Concept^n) → Concept
# 普通有向边 → : Concept → Concept 为一元态射（n=1 特例）。

# ---- 形式化函子 F 的骨架（对象/生成元映射） ----
# F 的像取自 04_Lean对接/Lean↔概念映射.csv；此处仅示意映射签名。
#   F_obj  : Concept → LeanDecl
#   F_hom  : Rel(⇒) → ProofDependency
# 函子性（复合保持）的核验见 ../范畴论模型/functor.py。

println("Catlab 草稿：组织多范畴 SchSig 已定义（", nparts(Sig(), :Concept),
        " 概念；运行 build 前需 `using Catlab`）")
