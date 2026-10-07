# leanblueprint 源文件说明

本目录的 `index.html` 为交互式蓝图（由 `_build/build_lean.py` 生成，离线自包含）。

若改用 leanblueprint 官方工具链，目录应含：

```text
10_输出可视化展示/蓝图/
├── content.tex      # 蓝图正文，节点用 \lean{{...}} / \uses{{...}} 标注
├── web.tex          # \documentclass{{report}} + \usepackage{{blueprint}} ...
├── plastex.cfg
└── blueprint/src/   # \lean{{...}} 指向的 Lean 源码（软链或拷贝 08 理论组织和形式化框架/04_Lean对接/Lean源码/）
```

生成：`leanblueprint web`（需 `pip install leanblueprint` + `plasTeX`）。

> 与 `04_Lean对接/蓝图/蓝图.md` 的分工：后者是 Lean↔概念↔缺口的对照源，本目录是其面向读者的 HTML 呈现。
