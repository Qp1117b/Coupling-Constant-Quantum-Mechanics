# 00 · 外部引用与证据层

> 维度 1/7 支撑。本目录存放**引用清单**、人工**锚点笔记**，以及 v1.7.0 起新增的**机器证据层**。
> 原则：只读取 `01`–`07` 理论文本，**不修改任何理论文本**；证据只做定位与引文摘录，不新增理论内容。

| 文件 / 目录 | 内容 | 生成方式 |
|:---|:---|:---|
| `引用清单.yaml` | 52 篇引用文档（4 权威基准 + 8 主干 + 17 专题 + 12 涌现应用 + 11 形式化），含 layer/type | 人工维护 |
| `锚点映射.csv` | 人工策展的锚点笔记（38 条，`struct_id/doc_id/location/description`） | 人工维护（保留原样） |
| `语料清单.csv` | 每篇文档的字符数、句数、章节数、SHA-256 前 16 位 | `_build/build_evidence.py` |
| `章节索引.csv` | 1,640 个章节区间（层级、编号、标题、标题行/正文起止、父节点） | 同上 |
| `句索引/句索引.jsonl` | 17,519 句，含 `doc_id/sid/start/end/kind/text`（字符偏移指向原文） | 同上 |
| `证据映射.csv` | 215 条断言 → 文档 / 章节 / 证据句 / 字符区间 / 引文 / 定位方法 / 置信度 | 同上 |
| `证据映射.json` | 同上 + Top-3 候选句（供前端证据面板与检索台消费） | 同上 |

## 定位方法分级（绝不虚构）

| 方法 | 含义 | 本库实测 |
|:---|:---|:---|
| `exact` | 断言文本（或 ≥60% 连续片段）在出处文档中**逐字出现** | 14 |
| `name` | 概念名在原文**逐字锚定**（本篇优先，缺则按引用层序全库回退，`doc_switch=True` 标记） | 62 |
| `section` | `source_loc`（§7.1 / §一 / 假设二 / 标题…）解析到章节，并在章节内按 IDF 加权回排句子 | 13 |
| `doc` | 仅能定位到文档，全篇回排最佳句 | 125 |
| `unresolved` | 既无逐字片段也无可用章节 → **如实登记，不猜** | 1 |

## 诚实边界

1. **`verified` 一律 `False`**：机器定位不是人工核验。只有**人工复核**才能置 `True`（当前 0 条）。
2. 结构化条目的**逐字重合中位数为 0 字**（≥8 字者 47/215）：说明概念定义与命题陈述多为**组织层改写**而非原文引用，
   因此"证据"是**定位**而非"引文证明"。这正是需要人工确认的原因。
3. 引文完整性由 `_build/check_provenance.py` 硬校验（`quote` 必须逐字等于原文 `[char_start, char_end)`）。

## 人工复核闭环（verified 置真的唯一合法路径）

```text
检索台/index.html · 证据复核模式   ←  逐条判定（通过/驳回/存疑）+ 复核人 + 备注（localStorage 草稿）
        │ 导出 复核结果.csv（列：struct_id, verdict, reviewer, note, reviewed_at）
        ▼
00_外部引用/复核结果.csv            ←  放入本目录
        │ python _build/build_evidence.py
        ▼
证据映射.csv/.json                  ←  合入 review_* 字段；
                                        verified = (verdict=approved 且 reviewer 非空)
        │ python _build/check_provenance.py
        ▼
硬校验（含「verified ⟺ approved 且有复核人」「approved 均带复核人」
        「复核 struct_id 必须存在于证据映射」）
```

- 「通过」在复核台**必须填写复核人**才允许提交；伪造 id 的复核记录会被硬检查拒收（管道自测实测通过）。
- 复核文件不存在时，`check_provenance.py` 断言 `verified` 全为 `False`——两条路径互斥且都硬校验。

## 重建

```bash
python _build/build_evidence.py      # 语料/章节/句索引/证据映射（读理论文本 + 合入复核结果）
python _build/check_provenance.py    # 证据层完整性硬检查（必过）
```
