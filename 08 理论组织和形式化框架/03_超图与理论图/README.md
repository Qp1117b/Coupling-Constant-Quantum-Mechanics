# 03 · 超图与理论图

> 维度 1（结构化）。概念实体与关系的有向超图，及其可视化。

| 文件 | 内容 |
|:---|:---|
| `超图数据.json` | 82 节点 / 19 超边 `⇒` / 51 有向边 `→`（由标准 CSV 解析重建） |
| `CQM_概念关系超图.md` | 概念集合、发生学主干、超边清单、关系摘要、Graphviz 建模建议 |
| `CQM_概念关系超图.dot` | Graphviz 源（6 cluster，哑节点展开超边） |
| `CQM_概念关系超图.svg` / `.png` | 静态渲染 |
| ~~`超图可视化.html`~~ | 已并入 VitePress 站「可视化 → 可推演超图」（`10_展示可视化/阅读站VitePress/.vitepress/dist/V001_可推演超图.html`）；本目录不再保留副本 |
| `理论依赖图.md` | 文档级依赖 DAG（分层总览、逐篇卡片、关键依赖矩阵） |

构建：`_build/build_base.py`（数据）、`_build/build_site.py`（交互可视化，并复制 `assets/cytoscape.min.js`）。
