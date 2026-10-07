# CQM skills（按需加载技能）

> 遵循 Agent Skills 开放标准（`SKILL.md`）：技能只在任务匹配时加载，避免 `AGENTS.md` 每轮对话全量注入。
> 本目录即 TRAE 项目级技能目录（`.trae/skills/`），技能在会话中按 `description` 自动匹配加载。

## 技能清单

| 技能 | 何时加载 |
|:---|:---|
| `cqm-doc-review` | 修改 `01–07` 活动文档、`归档/` 文档、`README.md` 或 `一体化研究/附录/` |
| `cqm-symbol-typesetting` | 写入或修改含公式、表格、符号的文本 |
| `cqm-lean-audit` | 改动 `08 理论组织和形式化框架/04_Lean对接/Lean源码/` 下文件，或提交前复核禁止项 |
| `cqm-consistency-check` | 概念/命题/论证有增改，或改动 `08 理论组织和形式化框架/` 任一产物 |

## 加载方式

各技能为 `<技能名>/SKILL.md`，含 YAML frontmatter（`name`、`description`）与正文。

- TRAE：置于项目 `.trae/skills/`，由客户端按 `description` 自动发现并按需加载。
- 其他 Agent Skills 客户端：把本目录（或其符号链接）指向其技能目录（如 `.claude/skills/`、`.agents/skills/`）。
- 不支持自动发现的客户端：按根 `AGENTS.md` 的技能索引，手动读取对应 `SKILL.md`。

## 边界

技能内容只是根 `AGENTS.md` 既有规则的**按需分片**，不含新规则、新观点、新数值。三条红线与目录约定始终保留在根 `AGENTS.md` 中，不随技能加载。