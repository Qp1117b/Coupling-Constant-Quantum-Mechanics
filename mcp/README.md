# CQM 只读知识 MCP server

> 把 `08 理论组织和形式化框架/01_结构化数据/*.csv` 及其派生结构化产物暴露为 MCP tools / resources，
> 使 agent 与 AI IDE 会话可直接**检索、导航、追溯**理论结构，而不是只读原始 Markdown 文本。

## 定位

- **只读**：不写入、不修改任何源数据；返回值是源文件内容的原样投影，不做推断、补全或改写。
- **单一事实源**：数据一律来自 `08 理论组织和形式化框架/01_结构化数据/*.csv`（唯一源）及其派生 JSON；
  本 server 不新增事实、不成为第二事实源。
- **缺口原样**：缺口状态按源数据原样返回，禁止升级为"已证/已闭合"。

## 启动

```bash
uv run --no-project --with "mcp>=2,<3" python mcp/cqm_knowledge_server.py
```

已在根 `mcp.json` 注册为 `cqm-knowledge`（stdio）。自检（不启动传输层）：

```bash
uv run --no-project --with "mcp>=2,<3" python mcp/cqm_knowledge_server.py --selftest
```

## Tools

| 工具 | 作用 |
|:---|:---|
| `project_overview` | 概念/命题/论证/超图/缺口/文档/Lean 映射计数与本体统计 |
| `search_concepts` | 按关键词检索概念（名称/定义/同义词），可按类型过滤 |
| `get_concept` | 概念全记录 + 入/出边 + 超边 + 相关论证 + Lean 映射 |
| `search_propositions` | 检索命题/缺口（按类型、状态过滤） |
| `get_proposition` | 命题全记录 + `depends_on` 解析 |
| `list_gaps` | 列出全部缺口（命题表 `type=缺口`），状态原样 |
| `neighbors` | 概念在超图/依赖图中的邻接（出/入/双向，可按关系类型过滤） |
| `find_path` | 图上 BFS 最短路（沿边方向），报告不可达情形 |
| `list_arguments` | 列出论证（超边），可按概念、关系类型过滤 |
| `lean_mapping` | Lean 形式化映射，可按概念或库过滤 |
| `resolve_document` | 文档 ID → 路径/标题/层级；或按关键词检索文档 |

## Resources

| URI | 内容 |
|:---|:---|
| `cqm://glossary` | 术语表原文 |
| `cqm://gaps` | 缺口台账原文 |
| `cqm://gap-closure` | 缺口依赖闭包原文 |
| `cqm://concepts` / `cqm://propositions` / `cqm://arguments` | 三张源表（JSON） |
| `cqm://hypergraph` | 超图数据（节点/超边/有向边） |
| `cqm://documents` | 文档引用清单（D001–D052） |
| `cqm://ontology-stats` | 本体统计 |
| `cqm://term-symbol-consistency` | 术语符号一致清单原文 |

## 依赖

- `uv`（`uv run --with mcp` 按需拉取 `mcp>=2,<3`，无需预装）。
- 运行环境需能解析 `mcp.server.mcpserver.MCPServer`（mcp 2.x API）。