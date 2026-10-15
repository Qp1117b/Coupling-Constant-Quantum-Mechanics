# -*- coding: utf-8 -*-
"""
元数据层 · 11_元数据
扫描 08 目录全部产物，生成清单（含大小/哈希）与版本、变更日志、验证状态。
产出（11_元数据/）：
  manifest.json
  版本.md
  变更日志.md
  验证状态.md
运行：python build_meta.py
"""
import csv
import hashlib
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 08 理论组织和形式化框架
PARENT = os.path.dirname(ROOT)
S11 = os.path.join(ROOT, "11_元数据")

SKIP_DIRS = {"_build", "Lean源码", "node_modules"}   # Lean源码 为外部 Lean 4 项目；node_modules 为第三方依赖
# 路径段级排除（相对 ROOT）：VitePress 工程内的构建中间物
SKIP_SEGS = ("阅读站VitePress/docs", "阅读站VitePress/.vitepress/cache")
SKIP_EXT = {".png"}   # 二进制大文件仍登记大小，但不计哈希


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan():
    files = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        rel_dir = os.path.relpath(dp, ROOT).replace("\\", "/")
        if any(rel_dir.startswith(s) for s in SKIP_SEGS):
            dns[:] = []
            continue
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            st = os.stat(p)
            item = {
                "path": rel,
                "dir": rel.split("/")[0] if "/" in rel else ".",
                "ext": os.path.splitext(fn)[1].lower(),
                "bytes": st.st_size,
                "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
            }
            if os.path.splitext(fn)[1].lower() not in SKIP_EXT:
                item["sha256"] = sha256(p)[:16]
            files.append(item)
    return sorted(files, key=lambda x: x["path"])


def main():
    os.makedirs(S11, exist_ok=True)
    files = scan()
    by_dir = {}
    for f in files:
        by_dir.setdefault(f["dir"], {"files": 0, "bytes": 0})
        by_dir[f["dir"]]["files"] += 1
        by_dir[f["dir"]]["bytes"] += f["bytes"]
    manifest = {
        "project": "CQMFormal",
        "unit": "08 理论组织和形式化框架",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "totals": {"files": len(files), "bytes": sum(f["bytes"] for f in files)},
        "by_directory": by_dir,
        "build_scripts": sorted(
            os.path.relpath(os.path.join(ROOT, "_build", x), ROOT).replace("\\", "/")
            for x in os.listdir(os.path.join(ROOT, "_build")) if x.endswith(".py")),
        "files": files,
    }
    with open(os.path.join(S11, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    write_version(manifest, by_dir)
    write_changelog()
    write_validation()
    print(f"[OK] manifest.json: {len(files)} 文件 / {manifest['totals']['bytes']} 字节")
    for d, v in sorted(by_dir.items()):
        print(f"     {d}: {v['files']} 文件")


def write_version(manifest, by_dir):
    rows = "\n".join(f"| `{d}` | {v['files']} | {v['bytes']:,} |" for d, v in sorted(by_dir.items()))
    scripts = "\n".join(f"- `{s}`" for s in manifest["build_scripts"])
    with open(os.path.join(S11, "版本.md"), "w", encoding="utf-8") as f:
        f.write(f"""# 元数据 · 版本

| 项 | 值 |
|:---|:---|
| 单元 | CQM 理论组织与形式化框架（`08`） |
| 顶层设计 | `设计方案.md` |
| 数据快照时间 | {manifest['generated_at']} |
| 文件总数 | {manifest['totals']['files']} |
| 总体积 | {manifest['totals']['bytes']:,} 字节 |
| 权威源 | `README.md` > `附录/术语表.md` > `附录/缺口台账.md`（`一体化研究/` 已于 v1.9.1 撤销，两份附录移入本目录） |
| Lean 版本 | `leanprover/lean4:v4.29.1`（固定，见 `08 理论组织和形式化框架/04_Lean对接/Lean源码/lean-toolchain`） |

## 一、各目录文件分布

| 目录 | 文件数 | 字节 |
|:---|:---:|:---:|
{rows}

## 二、构建脚本（可复现）

{scripts}

> 脚本位于 `08 理论组织和形式化框架/_build/`，从 `01_结构化数据/*.csv` 与外部 Lean 源码可重复生成全部产物（`build_reader.py` 另读 `README.md` 与 `01`–`07` 理论文本）；`_build/` 不计入产品文件统计。
""")


def write_changelog():
    with open(os.path.join(S11, "变更日志.md"), "w", encoding="utf-8") as f:
        f.write("""# 元数据 · 变更日志

> 记录 `08 理论组织和形式化框架/` 的建设事件。仅记结构性变更，不记临时工具与中间产物。

## v1.9.35 — 研究站控制台错误清零（续）：probeService 端口检查 · head 脚本 defer · typesetGrid 空闲调度 · 悬浮卡点击 toggle

- **变更动机**：v1.9.33 修复后用户反馈控制台仍有 `/api/status` 404（×3）、`Hydration completed but contains mismatches`、`'setTimeout' handler took 1007ms` 违规；悬浮卡点击交互要求"已弹出→隐藏，未弹出→弹出"。
- **修复一：probeService 改为端口 8080 检查**：v1.9.33 的 `hostname !== "localhost"` 检查在 VitePress preview（`localhost:4173`）上仍通过（hostname 确实是 localhost），导致 `fetch("/api/status")` 仍发出并 404。改为 `if (location.port !== "8080") return;`，只在研究站后端服务端口（8080）探测。
- **修复二：head 脚本加 defer 消除 Hydration mismatch**：`cqm-glossary.js`、`cqm-depth.js`、`cqm-enhance-vp.js` 原先在 `<head>` 中不带 `defer` 加载，同步执行时机早于 Vue hydration，干扰 SSR DOM 匹配。改为均加 `defer: true`，脚本在 HTML 解析后、DOMContentLoaded 前按序执行，不阻塞渲染。
- **修复三：typesetGrid 用 requestIdleCallback**：术语总览页 227 张卡的 MathJax 排版经 `setTimeout(fn, 120)` 触发，浏览器报告 `'setTimeout' handler took 1007ms` 违规。改为优先 `requestIdleCallback(run, { timeout: 200 })`，将排版推迟到浏览器空闲时段，不阻塞主线程响应。
- **修复四：悬浮卡点击改为简单 toggle**：`cqm-enhance-vp.js` 的 click handler 原先在 `!pinned` 状态下点击当前词只固定不隐藏，不符合"已弹出→隐藏，未弹出→弹出"的预期。改为：`cur === el && POP.style.display !== "none"` 时一律 `hidePop()`，否则 `showPop(el)`。
- **修复五：去掉 `_` → `&#95;` 转义消除双重转义**：v1.9.34 的 `_frag_plain` 和 `_frag_cell_html` 将 `_` 转义为 `&#95;`，但 VitePress markdown-it 将 `&#95;` 再次转义为 `&amp;#95;`，页面上显示字面 `&#95;` 而非 `_`。去掉两处转义：反引号和 `<table>` 内 `_` 不会被解析为斜体，且 `BARE_SUB_RE` 要求 `_` 前后均为 `[A-Za-z0-9({]`，表格中 `_` 后面通常是中文不匹配。
- **未修复（VitePress 内部）**：`util-*.js` `TypeError: e.indexOf is not a function` 来自 VitePress `content.js` 内部渲染管线；`'wheel' input event delayed 3168ms` 来自 VitePress `content.js` 内部滚动处理——均非项目代码，无法直接修复。
- **验证**：重跑 `build_vitepress_site.py`；产物中 `probeService` 端口检查在位（`location.port !== "8080"`）、三脚本 `defer` 在位、`requestIdleCallback` 在位、toggle 逻辑在位；三道核查通过。

## v1.9.34 — 展开链页面排版/渲染异常修复：反斜杠转义改 HTML 实体

- **变更动机**：用户反馈展开链页面（131 条链步）存在多种排版和文本渲染异常，如 `│ └──` 树形符号、`\\>` 字面反斜杠露出、`**` 未闭合加粗标记字面露出、`## ` 标题在引用块中被解析、`T\\_c` 转义下划线字面露出等。
- **根因**：`build_reader_site.py` 的 `_frag_plain` 函数用反斜杠转义处理引用块内的 Markdown 元字符，但 VitePress markdown-it 在引用块内对反斜杠转义的处理不稳定，实测页面上露出字面反斜杠。
- **修复**：`_frag_plain` 函数改用 HTML 实体代替反斜杠转义：`>` 行首 → `&gt;`、`[` `]` → `&#91;` `&#93;`、`_` → `&#95;`（先还原源文档 `\\_` 转义）、行首 `#` → `&#35;`、`|` 不转义、`<>` 不转义、未闭合的 `**`（奇数个）→ 去掉全部 `**`。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；三道核查通过。

## v1.9.33 — 研究站控制台错误清零：/api/status 404 · Hydration mismatch · scroll passive

- **变更动机**：用户反馈浏览器控制台存在三类错误/警告：`/api/status` 404（×3）、`Hydration completed but contains mismatches`、`'scroll' handler took 228ms` + Forced reflow。
- **修复一：probeService 只在 localhost 探测**：改为开头加 `if (h !== "localhost" && h !== "127.0.0.1" && h !== "[::1]") return;`，只在本地开发服务探测。
- **修复二：去掉 DOMContentLoaded boot 消除 Hydration mismatch**：`cqm-enhance-vp.js` 原先在 `DOMContentLoaded` 时调 `boot()` → `CQM.init()`，该时机早于 Vue hydration。改为不自动 boot，初始化由 `theme/index.js` 的 `enhanceApp` 经双 `requestAnimationFrame` 在 hydration 之后调用。
- **修复三：scroll handler 加 passive**：悬浮卡全局 scroll 监听改为 `{ capture: true, passive: true }`。
- **验证**：重跑 `build_vitepress_site.py`；三道核查通过。

## v1.9.32 — 公式中 | 保留原样（去掉 escape_pipe_in_math）

- **变更动机**：用户反馈"13.9 对称性叠加"公式渲染异常，`\\vert` 与后续字母粘连产生未知命令。
- **根因**：`escape_pipe_in_math` 把公式中 `|` 替换为 `\\vert` 但未加空格，导致 `\\vertG` 被 MathJax 解析为未知命令。
- **修复**：去掉 `escape_pipe_in_math` 调用，公式中 `|` 保留原样。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；三道核查通过。

## v1.9.31 — ☯ 别名/引文渲染修复 + 裸 Unicode 符号映射扩展

- **变更动机**：用户反馈 ☯ 概念的别名、引文区域渲染异常。
- **修复一**：`_SB_UNICODE_INMATH` 新增数学区间内 ☯→`\\mathcal{C}` 映射；`_sb_unicode_to_latex` 在数学区间内也替换 ☯。
- **修复二**：`_SB_UNICODE_MATH` 全面扩展到希腊字母全表 + 关系符 + 管头 + ☯。
- **修复三**：别名区域加 `_sb_unicode_to_latex` 防御性转换。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；三道核查通过。

## v1.9.27 — 术语表多类异常修复（G/S/P/缺口/符号/链条步/☯/A₄）

- **变更动机**：用户反馈术语表中 G/S/P/缺口/符号/链条步/☯/A₄ 等多类术语存在渲染异常。
- **修复**：缺口 `desc_closure` → 裸 Unicode 修复、符号 `value_or_note` 裸 Unicode 修复、论证 `sb` 中 `⇒` 修复、链条步 `##` 标记修复、☯/A₄ 别名用 `latex` 字段。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；三道核查通过。

## v1.9.25 — 补全量纲符号定义包裹 + 悬浮卡点击 toggle 交互

- **变更动机**：用户反馈术语表中"量纲转换常数族""4-单纯形"等仍有渲染异常，要求全面检查修复；悬浮卡交互应"悬停弹出、移出消失、点击也消失"。
- **修复一：补全 8 个量纲概念定义**：v1.9.23 遗漏 C032–C039（`T`/`L`/`M`/`Q`/`Θ`/`N`/`J` 量纲符号和 `K_L K_M K_Q K_Θ K_N K_J` 转换常数族），未用 `$...$` 包裹。逐条补裹为 `$T$ 第一量纲`、`$K_L\, K_M\, K_Q\, K_\Theta\, K_N\, K_J$` 等。
- **修复二：悬浮卡点击 toggle**：`cqm-glossary.js` 与 `cqm-enhance-vp.js` 的 click handler 原先只 `showPop`（始终弹出），改为 `if (cur === el) hidePop(); else showPop(el)`——已显示则点击隐藏，未显示则点击弹出。
- **验证**：Puppeteer 实测 9 个代表术语全部 `mjx=1`（量纲转换常数族、4-单纯形、时间/长度/质量/温度量纲、角亏、主导群、禁闭边界）；交互测试：悬停弹出✅ 点击隐藏✅ 再点击弹出✅ 移出消失✅；三道核查通过。

## v1.9.24 — 修复悬浮卡引文嵌套定界符 \(...\) 包裹 \[...\]

- **变更动机**：用户反馈"禁闭边界"悬浮卡弹出渲染、排版、内容异常。
- **根因**：`_mathify` 步骤 3 在检查是否已含定界符时，只检查 `\(`/`\)`（行内），**未检查 `\[`/`\]`（显示）**。当步骤 1 将 `$$...$$` 转为 `\[...\]` 后，步骤 3 再次整体包裹 `\(...\)`，产生嵌套 `\(\[...\]\)`。MathJax 遇到内联定界符包裹显示定界符时解析错乱，公式以原文露出。
- **修复**：`_mathify` 步骤 3 条件增加 `"\\[" not in s and "\\]" not in s`，防止对已含 `\[...\]` 的字符串再次包裹。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；全量检查 225 个术语，嵌套定界符 0 个；三道核查通过。

## v1.9.23 — 概念表定义字段数学符号用 $...$ 包裹

- **变更动机**：术语表页面与悬浮卡中，含数学符号的定义（如 `$\delta_v$ Regge剖分顶点角亏`、`$G_{\text{主导}}=\arg\min F_n$`）以纯文本显示，下标、公式未渲染。
- **根因**：源 CSV `概念表.csv` 的 `definition` 字段混用中文与 Unicode 数学符号（`δ_v`、`v_τ=√(1−βδ_v)`、`G_主导=argmin F_n` 等），但数学部分未用 `$...$` 标记。`_mathify` 函数只处理含 `$...$` 或 LaTeX 宏的字符串，裸 Unicode 符号不触发包裹，MathJax 不渲染。
- **修复**：逐条将 52 个概念的 `definition` 字段中数学部分用 `$...$` 包裹，Unicode 符号转 LaTeX 命令（`δ`→`\delta`、`√`→`\sqrt`、`β`→`\beta`、`𝔠`→`\mathfrak{c}`、`☯`→`\mathcal{C}` 等），下标 `_v`→`_v`（LaTeX 下标语法）。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；Puppeteer 实测 8 个代表术语卡片全部 `hasMjx=1`（角亏、固有时流速、主导群、声子、再生产、曲率、和乐、资格条件），公式正确渲染为 MathJax SVG；三道核查通过。

## v1.9.22 — 修复术语表页面公式渲染时序问题

- **变更动机**：术语表页面（`TERMS_术语表.html`）公式以 `$...$` 原文露出，需等待 8 秒后才渲染。
- **根因**：`tex-svg.js`（MathJax bundle，2.1 MB）用 `async` 加载，需 3–5 秒初始化；`terms-app.js`（`defer`）在 MathJax 就绪前执行 `typesetGrid()`，此时 `window.MathJax.typesetPromise` 不存在，公式以原文露出。Puppeteer 实测：3 秒时 `mjxCount=0, rawDollarCount=87`；8 秒时重试逻辑最终生效但延迟过长。
- **修复一**：`typesetGrid` 函数增加 MathJax 就绪重试逻辑——若 `typesetPromise` 不存在，检查 `startup.promise`，否则每 300 ms 重试。
- **修复二（关键）**：VitePress 主配置 `head` 脚本顺序调整——`tex-svg.js` 从 `async` 改为 `defer`，`vp-math.js` 从 regular 改为 `defer`，两者移至 `lean-page.js` 和 `terms-app.js` 之前。`defer` 脚本按文档顺序执行，确保 MathJax bundle 在 `terms-app.js` 运行前完成加载与初始化。viz 页面同步修正。
- **验证**：重跑 `build_vitepress_site.py`；Puppeteer 实测 3 秒时 `mjxCount=188, rawDollarCount=0`——公式全部正确渲染，不再有原文露出；三道核查通过。

## v1.9.21 — 修复悬浮卡公式嵌套定界符与 CSS 暗色模式适配

- **变更动机**：用户反馈悬浮卡（术语弹出解释）排版和公式渲染异常。
- **根因一：嵌套 `\\(...\\)` 定界符**：`_mathify` 函数步骤 3 在引文含 LaTeX 宏但无 `$` 时，将整段文字包裹在 `\\(...\\)` 中——即使文中已含 `\\(...\\)` 定界符（来自步骤 2 的 `$...$` 转换），导致嵌套。MathJax 遇到嵌套定界符解析错乱，公式以原文露出、中文被卷入 math 模式。实测 20 个术语受影响（相变量子、RH、跃迁耦级谱等）。
- **修复一**：`_mathify` 步骤 3 增加 `\\(` / `\\)` 存在性检查——若字符串已含定界符则不再整体包裹。
- **根因二：裸 LaTeX 命令未包裹**：13 个定义含 `\\mathfrak`、`\\gamma` 等宏但无定界符，`_BARE_FORMULA_RE` 白名单未覆盖，导致裸露不渲染。
- **修复二**：`_BARE_FORMULA_RE` 扩展宏白名单：新增 `\\mathfrak`、`\\hat`、`\\partial`、`\\det`、`\\epsilon`、`\\gamma`、`\\delta`、`\\beta`、`\\rho`、`\\mu`、`\\xi`、`\\ln`、`\\nabla`、`\\alpha`、`\\bar`、`\\sqrt`。
- **根因三：CSS 暗色模式不适配**：`.cqm-pop` 等用 MkDocs 变量 `var(--md-default-bg-color, #fff)` 和 `[data-md-color-scheme="slate"]` 选择器，VitePress 中不存在，暗色模式白底白字不可读。
- **修复三**：`var(--md-default-bg-color, #fff)` → `var(--vp-c-bg, #fff)`（3 处）；`[data-md-color-scheme="slate"]` → `.dark`（3 处）。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py`；嵌套定界符 0 个；三道核查通过。

## v1.9.20 — 移除 MkDocs 阅读站，VitePress 研究站成为唯一站点

- **变更动机**：用户裁定 MkDocs 阅读站已无存在必要，VitePress 研究站（`阅读站VitePress/`）为唯一站点。
- **变更内容**：
  - `build_reader_site.py` 主函数移除 MkDocs 构建步骤（`shutil.rmtree(SITE)` + `mkdocs build`），仅保留 staging 环节（为 VitePress 供料）；删除废弃 `SITE_README` 变量。
  - 删除 `10_展示可视化/阅读站/` 目录（MkDocs 构建产物）。
  - `build_vitepress_site.py` 头部注释更新：「与 Material 阅读站并行」→「唯一站点」。
  - `build_site.py` 七维度表「阅读站」→「研究站」。
  - `08/AGENTS.md` §六依赖列表移除 `mkdocs-material`（阅读站）。
  - `_build/README.md` 依赖列表移除 `mkdocs-material`（阅读站，pip 安装）。
- **保留**：`build_reader_site.py` 的 staging 功能（悬浮卡/检索/术语/讲稿数据生成）仍为 VitePress 研究站供料，`mkdocs_src/docs/` 目录结构保留。
- **验证**：重跑 `build_reader_site.py` → `build_vitepress_site.py` → `build_meta.py`；三道核查通过。

## v1.9.19 — 修复 MkDocs 阅读站 MathJax bundle 缺失与表格公式断裂

- **变更动机**：MkDocs 阅读站公式无法渲染——`assets/tex-svg.js`（MathJax v3 bundle，2.1 MB）缺失，导致 `\(...\)` 定界符以纯文本显示。
- **根因一**：`build_reader_site.py` 中 `TEX_SVG` 源路径指向阅读站**自身**目录（`阅读站/assets/tex-svg.js`），而主流程 `shutil.rmtree(SITE)` 清空旧站时将其删除；后续运行 `os.path.isfile(TEX_SVG)` 返回 False，跳过复制，MathJax bundle 永久缺失。
- **修复一**：`TEX_SVG` 源路径改为 VitePress 研究站 `阅读站VitePress/.vitepress/dist/tex-svg.js`（同源 MathJax bundle，不受 `rmtree` 影响）；源缺失时输出 `[WARN]` 告警。
- **修复二**：`math-config.js` 补充 `xRightarrow` 宏定义（`\\overset{#1}{\\Longrightarrow}`，语料 22 处使用），与 VitePress `vp-math.js` 配置一致；`inlineMath` 增补 `$...$` 定界符。
- **根因二**：Markdown 表格扩展在 `arithmatex` 之前运行，表格中公式内的 `|`（如 `\\big|_{s=1}`）被解释为列分隔符，导致公式断裂、MathJax 无法渲染（D008/D012/D005/D014 等页面 rawLatex 择留）。
- **修复三**：staging 阶段添加 `escape_pipe_in_math` 函数，把 `$...$` / `$$...$$` 公式中未转义的 `|` 替换为 `\\vert`（LaTeX 等价，不改变渲染结果），避免表格列分隔符冲突。
- **验证**：重跑 `build_reader_site.py`；Puppeteer 检查 MkDocs 站 D008/D005/D012/D014——mjx-container 286/823/408/384 个，裸露定界符 0，rawLatex 0；VitePress 研究站 40 页全检——39 页 OK（D016 无公式属正常）。
- 验收：`check_consistency` **41/41**；`check_provenance` **10/10**；`consistency_probe` 问题项 **0**。

## v1.9.18 — 修正 SU(5) 涌现组装链起点表述

- **变更动机**：`01 核心理论/CQM_核心_集成理论.md` §7.1 组装链起点写作「禁闭内部离散自由度（因果集事件）」——因果集是描述物质自组织因果结构的理论，不应限定为「禁闭内部」的自由度；且禁闭内部非起点（先有前质子-前中子，后才有禁闭）。去掉「禁闭内部」限定，因果集描述物质自组织环节，不加限制。
- **修正**：「禁闭内部离散自由度（因果集事件）」→「离散自由度（因果集事件）」。
- **同步**：讲稿 `第二分册_统一体自组装与α.md` 同步修正；重跑 build_evidence → build_claims → build_ontology → build_kg → build_site → build_search → build_reader_site → build_vitepress_site → build_meta，证据映射 / 句索引 / 知识图谱.ttl 中旧引文全部更新。
- 验收：`check_consistency` **41/41**；`check_provenance` **10/10**；`consistency_probe` 问题项 **0**。

## v1.9.17 — 删除「质数前网络」概念（C010）与全链同步

- **变更动机**：根 `AGENTS.md` §四「以原（第一）文档为准」——原始文档中「质数前网络」系描述物质自组织关系的数学结构，非独立本体概念；组织层概念表 C010 将其登记为独立概念与理论口径不符，予以剔除。
- **源数据变更**：概念表删 C010 行；论证表删 A043 行（A043 的 source_concept 引用 C010）；术语表删「质数前网络」条目。
- **第一文档同步**：`README.md`、`01 核心理论/` 三篇、`06 超导/` 两篇、`归档/CQM_框架路线与理论纪要.md` 中所有「质数前网络」「前网络」$\\mathbb{P}_{\\infty}$ 表述删除或改写（仅删术语词，保留句义，最小改动）。
- **Lean 对接**：`build_lean.py` MAPPING 删 PrimeGeometry 行；`Superconductivity.lean` 注释删「质数前网络→」；映射口径 41/82 → 40/81（49.4%）。
- **计数变更**：概念 82→81 · 论证 70→69 · 有向边 51→50 · 本体个体 430→426 · 知识图谱 145/359→144/358 · 证据 215→213 · ML 张量 (82,15)→(81,15) · 桥接映射 82→81 · 可达 81/82→80/81（不可达仍为 C074）。
- **全链重跑**：fix_csv → build_base → build_evidence → build_claims → build_ontology → build_kg → build_lean → build_ml → build_extract → build_dynamics → build_causal → build_bridge → build_site → build_search → build_reader_site → build_vitepress_site → build_meta，16 个脚本全部成功。
- **脚本断言更新**：`build_base.py`、`build_ontology.py`、`build_lean.py`、`build_site.py`、`build_reader_site.py`、`build_vitepress_site.py`、`build_search.py`、`build_extract.py`、`check_consistency.py`、`check_provenance.py` 中所有硬编码计数同步更新。
- **手工文档回填**：讲解文档 `03_超图总览与关系类型.md`、`CQM_概念关系超图.md` 统计数字同步回填。
- 验收：`check_consistency` **41/41**；`check_provenance` **10/10**；`consistency_probe` 问题项 **0**。
- 同步：`_build/` 全部构建脚本与核查脚本、`01_结构化数据/` 源 CSV、`附录/术语表.md`、讲解文档、超图说明、本日志。

## v1.9.16 — 侧栏文档主题分类（按源目录七组）· 服务彻底重启

- **侧栏文档分类**：「结构化与参考」此前把 41 篇文档平铺、无主题分类。现按 **staged 源的顶层目录**分为七组（核心理论 / 量子引力讨论 / 引力与退相干 / 前沿研究 / 方法论与批判 / 超导 / 精细引力（FG）），与仓库目录结构一一对应；sid→源目录映射**复用 `build_reader_site.registry()`**（sid 分配逻辑的唯一权威，避免两处实现漂移）。映射失败时整体回退「其它」组并在构建日志告警。
- 实测：侧栏七个主题组 + 展开链/讲稿/可视化/Lean 对接/术语表全部在线；站内链接失效 0。
- **服务彻底重启**：终止旧 java 进程并重新启动（研究站与 `/api/lean/*` 恢复正常）。
- 运维注：`nohup`/分离方式启动的服务在 Agent 会话结束后会被回收——期间运行链路探测会得到「全站失效」的假阳性；探测前先确认服务存活。
- 验收：端到端 `verify_station` **29/29**；站内链接 **123** 条失效 **0**；`consistency_probe` 问题项 **0**；`generator = VitePress v1.6.4`。
- 同步：`_build/build_vitepress_site.py`（主题分组）、本日志。

## v1.9.15 — 服务徽标 404 根因修复（VitePress router 拦截相对链接）

- **复现**（CDP 点击徽标）：点击后 URL 变为 **`/api/status.html`** → 404 页；失败请求另见 **`/api/api/status`**。
- **根因**：徽标 `href="api/status"` 是站内相对链接，被 **VitePress router 拦截做 SPA 导航**——无扩展名被补 `.html`、相对路径按 SPA 路由二次解析，结果落到不存在的地址。改为绝对路径也无法绕过（router 拦截一切站内 `<a>`）。
- **修法**：徽标加 `target="_blank"` + `rel="noopener"`（新窗口打开状态 JSON，绕过 router）。
- **实测**：点击后当前页不变（无 404）；`target=_blank` 生效。
- **说明**：用户清单中其余 11 个页面（D005/L001/D003/D010/D014/D017/D020/D028/D029/D030/D032）服务端逐个实测**全部 200**，`G_N` 渲染复核正常（D014 截图）——请硬刷新后仍异常的页面提供具体入口。
- 验收：端到端 `verify_station` **29/29**；站内链接 **126** 条失效 **0**；`check_consistency` **41/41**；`check_provenance` **10/10**。
- 同步：`_build/build_vitepress_site.py`（徽标 target）、本日志。

## v1.9.14 — 搜索跳转高亮严重缺陷修复（整页文本被查询词重复覆盖）

- **现象**（用户报「点击一个 item 后搜索内容大量复制到跳转文本处」）：搜索点击跳转后，目标页**整页文本变成查询词的几百次重复**（满屏黄块）。
- **根因**：`applySearchHighlight` 的匹配循环内**重置了正则的 `lastIndex`**——`/gi` 正则的 `exec` 依赖 `lastIndex` 推进，重置后永远停在第一个匹配：同一位置被反复替换为 mark，直至触发 200 上限，原文全部丢失。
- **修法**：删除循环内的 `re.lastIndex = 0`（保留循环前的预检重置）。
- **实测**：搜索「退相干」→ 点击结果 → 目标页 **26 处**与文本匹配数一致的高亮、正文逐字正常、无重复（截图复核）。
- 验收：端到端 `verify_station` **29/29**；站内链接 **126** 条失效 **0**（全站链接普查持续覆盖，讲稿三页/徽标/卡片链接均实测 200，用户报的 404 未复现，请提供具体入口）；`check_consistency` **41/41**；`check_provenance` **10/10**。
- 同步：`_build/build_vitepress_site.py`（高亮循环修复）、本日志、`验证状态.md`。

## v1.9.13 — 概念 C008「退相干」定义修正（口径统一：因果截断只是其中一种表现）

- **用户裁定口径 A（全项目统一）**：「退相干是物质自组织的表现，其中因果截断只是其中一种表现」。
- **修正**：`01_结构化数据/概念表.csv` C008 definition 由「质子集体引力因果限制的因果截断」（把退相干等同于因果截断）改为「退相干是物质自组织的表现，其中因果截断（质子集体引力因果限制）只是其中一种表现」——保留质子集体引力因果限制作为限定，因果截断降为表现之一。悬浮卡/检索/总览页随构建自动更新，实测卡面已呈现新口径。
- **排查范围**：01–07 源文档中「退相干＝因果截断」的定义性表述——除 D015 外零命中；卡片链接 23 条全 200；讲稿三页与全部导航链接实测 200（用户报的讲稿 404 未复现，请求提供具体入口；服务徽标 404 已于 v1.9.9 修复为 /api/status）。
- **待用户逐句裁定（不擅改理论核心句）**：D015 行 47「将退相干重新定义为**关系性因果截断**，而非本体性态缩减」——与口径 A 存在张力（因果截断从定义降为表现之一）；行 580/590 为「表观截断」的术语用法说明，张力较小。
- **验证**：组织层全链 14 个构建脚本重跑；`consistency_probe` 概念 82/82、缺口 24/24、论证 70/70、符号 21/21、问题项 0；`check_consistency` **41/41**；`check_provenance` **10/10**；端到端 **29/29**。
- 同步：`01_结构化数据/概念表.csv`（C008）、本日志、`验证状态.md`。

## v1.9.12 — 派生内容一致性核查（全绿）：悬浮卡 vs 源 CSV 逐字、数字口径、术语统一

**1. 新增长期核查工具 `.workbuddy/tools/consistency_probe.py`**
- 核对三件事：① 悬浮卡文字 vs 源 CSV **逐字**（概念/缺口/论证/符号四类全量）；② 渲染产物里的关键数字口径（82/63/70/24/131/215/1 388/68/41/82…）；③ 术语统一（渲染产物中的旧变体）。
- 比对方法：卡 HTML 先剥 math 包装（`反斜杠括号` → 内容）再剥标签，源字段去空白与 `$` 后做包含判断。

**2. 核查发现并修复的一处真不一致**
- **G_N 键覆盖**：`G_N` 既是概念（牛顿引力常数）又是符号（同实体），构建时符号卡**覆盖**了概念卡，概念 definition 的原文形态（无逗号）被符号卡（有逗号）顶掉。修法：符号卡遇同键**并入**既有卡（LaTeX/取值以分区追加，不覆盖）。
- 修复后：概念卡 **82/82**、缺口卡 **24/24**、论证卡 **70/70**、符号卡 **21/21** 全部逐字命中，**问题项 0**。

**3. 合法引用登记（不算旧变体）**
- `基础自守量纲`：D003 术语表「唯一名；曾用名「基础量纲」「基础自守量纲」已废止」——历史引用。
- `量子引力层`：D006「CQM 不设独立的量子引力层」——否定式声明。
- 两处均为源文档原文的有意保留，`consistency_probe` 已把它们从变体表移出并注明依据。

**4. 验收**：端到端 `verify_station` **29/29**；站内链接 **126** 条失效 **0**；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 **32 → 64 → 102 → 107**；`generator = VitePress v1.6.4`。
- 同步：`_build/build_reader_site.py`（符号卡并入）、`.workbuddy/tools/consistency_probe.py`（长期核查工具，不入库）、本日志、`验证状态.md`。

## v1.9.11 — 高级检索渲染修复 · 术语总览页（411 条）· 正文字号调节

**1. 高级检索结果渲染修复（用户报「高级检索渲染和排版异常」）**
- 实测（CDP 多查询）：「量纲」查询的结果里有 **20 处 `**` 字面**、「G_N」查询有 **6 处 `$` 字面**——结果摘要（`sb`，来自概念定义/命题陈述/论证前件⇒后件）是**纯文本**，加粗与公式从不渲染。
- 修法：新增 `sbRender()`——**公式先摘成占位符**（防止关键词 mark 把 `$…$` 内部切开，MathJax 就匹配不到），再做关键词高亮，然后加粗 `**…**` → `<strong>`、行内代码 `` `…` `` → `<code>`，最后还原公式交给 typeset。
- 实测：「量纲」查询 → `**` 残留 **20 → 0**、`<strong>` 10 处、`mjx` 20 个。

**2. 术语总览页（新增「术语表」导航组）**
- 悬浮卡此前只能「遇到术语才看到」；新增 `TERMS_术语表.html`：**411 条**索引集中为卡片网格（概念/缺口/论证/符号/命题/文档/链条步 七类 chips + 内容筛选框），悬停或点击即弹出与正文一致的完整悬浮卡（复用全局 `data-cqm` 机制），数据直接取自页面已加载的 `window.CQM_GLOSSARY`，零额外请求。
- 实测：411 张卡、8 个分类按钮、479 个可悬停卡（`data-cqm`）。

**3. 正文字号调节（阅读体感）**
- 导航栏新增「A / A+ / A++」按钮：三档循环（1 / 1.12 / 1.25），CSS 变量 `--cqm-font-scale` 驱动 `.vp-doc` 字号，`localStorage` 记忆。

**4. 验收**：端到端 `verify_station` **29/29**；站内链接 **126** 条失效 **0**；渲染普查 **11/13** 类 OK；深度滑杆 **32 → 64 → 102 → 107**；`check_consistency` **41/41**；`check_provenance` **10/10**。
- 同步：`_build/build_vitepress_site.py`（`sbRender`、TERMS 页与脚本、字号调节、分组与导航）、本日志、`验证状态.md`。

## v1.9.10 — 按裁定移除站内编译 · 表格横向滚动修复

**1. 移除站内编译（用户裁定「编译功能不要」）**
- 前端：LEAN_Lean对接 页删去「编译」页签与描述，只保留**模块与声明**、**概念 ↔ Lean** 两个页签。
- 服务端：`LeanController` 删去 `POST/GET build` 端点与编译状态字段；`StationProperties.Lean` 删去 `lake-exe` 与 `build-enabled`（保留源码目录供源码查看）。
- 编译能力不受影响：本机 elan 工具链（Lean 4.29.1）可手工执行 `lake build`；此前触发的构建已在 `.lake/` 留有增量缓存。
- 实测：`POST /api/lean/build` → 404；LEAN 页仅剩两个页签。

**2. 表格把整页撑出横向滚动（回归修复）**
- 根因：上轮为解决竖排引入的 `width: max-content` **缺了 `max-width` 与 `overflow` 约束**——宽表（实测 D001 一张 8 750 px、D009 一张 1 914 px，视口 1 461 px）直接把 `document.scrollWidth` 撑到 9 145 px，整页左右晃。
- 修法：采用 **GitHub 的成熟模式**——`display: block; width: max-content; max-width: 100%; overflow-x: auto`：窄表按内容自然展开，宽表**在表格内部横向滚动**，页面不再横向滚动。
- 实测（CDP）：D009 / D001 / LEAN 三页 `pageHScroll = false`（D001 的 `scrollWidth` 从 9 145 回到 1 461）；截图复核表格内容横排、链接可点、无竖排回归。

**3. 验收**：端到端 `verify_station` **29/29**；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 **32 → 64 → 102 → 107**；站内链接失效 **0**。
- 同步：`_build/build_vitepress_site.py`（表格 CSS、LEAN 页/脚本）、`09 研究站服务`（`LeanController.java`、`StationProperties.java`、`application.yml`）、本日志、`验证状态.md`。

## v1.9.9 — 服务徽标链接修复 · 高级检索面板实测

- **服务徽标 404**：徽标 `href="api"`（相对路径 → `/api`），而 `/api` 本身没有映射，点击即落 404。改指真实存在的 `/api/status`（状态 JSON）。另经 CDP 复测，`/api` 现由错误页控制器接管。
- **高级检索面板实测（结论：正常）**：CDP 打开面板并输入查询——面板定位（fixed，视口内）、分面（全部 411/概念 82/缺口 24/命题 39/符号 21/论证 70/链条步 131/文档 42）、结果项 30 条、公式 18 个 `mjx-container`、无横向溢出，截图复核通过。用户报告的「渲染和排版异常」与旧缓存一致（缓存治理见 v1.9.6，请硬刷新一次）。
- 验收：端到端 `verify_station` **29/29**；`check_consistency` **41/41**；`check_provenance` **10/10**。
- 同步：`_build/build_vitepress_site.py`（徽标链接）、本日志。

## v1.9.8 — 术语卡扩充至 227 · 搜索跳转高亮 · 404 接入阅读站 · 箭头一致性核查

**1. 术语悬浮卡扩充（138 → 227 张）**
- **符号卡（+21）**：`09_桥接与翻译/符号对照表.csv` 的符号此前只进检索索引，现补成悬浮卡（LaTeX 形式、类别、取值说明、出处、**出处文档链接**）；单字符符号（`c`、`α`）只做卡、不做正文标注——否则会满页命中。
- **论证卡（+70）**：`01_结构化数据/论证表.csv` 的每条重组实现/推导论证现在有自己的卡：**前件 ⇒ 后件**、依据文档（可点击跳转对应页面）、概念链。正文里的 `H001`、`A004` 等论证编号从此可悬停溯源。
- **缺口卡补链接**：24 张缺口卡增加「在缺口台账中打开」（`D004_缺口台账.html`）。
- 术语标注上限 MAX 240 → 320；卡总数 **227**（去重后），termKeys **190**。
- 实测：`cqm-glossary.js` 里论证卡 70、含台账链接卡 24、符号卡样例（`☯` `A₄` `G_N`）齐全。

**2. 搜索跳转后的关键词高亮（此前没有）**
- 点击搜索结果前把查询词存入 `sessionStorage`，目标页初始化时对正文文本节点打 `<mark class="cqm-hl">`（跳过代码块/公式容器/已有标注，上限 200 处），首个高亮滚动到视口中央，深浅色各有配色。
- **坑**：点到**当前页自身**的结果时 SPA 路由不触发回调、高亮不执行——点击处理里主动补调 `window.CQM.highlight()`（已暴露）。实测全流程：搜索「群约束性」→ 点结果 → **200 处高亮**，首处即关键词。

**3. 404 接入阅读站样式**
- 此前无效路径返回 Spring Boot 默认白板错误页。新增 `ErrorPageController`：404 状态返回阅读站的 `404.html`（VitePress 产物，带站内样式与回首页路径），其余状态维持原行为。实测无效路径返回 `404 | CQM 研究站`。

**4. 箭头符号渲染一致性核查（结论：与源一致，无需修正）**
- 全站扫描异常形态（转义箭头 / HTML 实体未渲染 / ASCII `->` / 公式命令漏出）：仅 L000 展开链页 1 处字面 `\to`——该页定位为原文**逐字摘录**，属有意保留。
- 抽查 D009 / D010 / D015 的源与渲染箭头数量：差异均为 ±1 且来自导航/大纲等页面框架文本，正文箭头（`→ 100`、`⇒ 5`、`↔ 11` 等）与源一致。

**5. mcp 清理**
- 删除根目录 `mcp/`（只读知识 MCP server）、`mcp.json`（旧 server 配置）、`mcp_filesystem.log`；根 `AGENTS.md` 目录约定表同步。

**6. 验收**：端到端 `verify_station` **29/29**；站内链接 **123** 条失效 **0**（`link_audit` 同时修正了查询串被过度编码的假阳性）；渲染普查 **11/13** 类 OK（余 2 类为数学文本误报）；深度滑杆 **32 → 64 → 102 → 107**；`check_consistency` **41/41**；`check_provenance` **10/10**。
- 同步：`_build/build_reader_site.py`（符号卡/论证卡/缺口链接）、`_build/build_vitepress_site.py`（高亮、标注上限）、`09 研究站服务`（`ErrorPageController.java`）、根 `AGENTS.md`、本日志、`验证状态.md`。

## v1.9.7 — Lean 集成进研究站：统一视图 + 站内编译 · 搜索结果公式排版

**1. 搜索结果里的公式排版**
- VitePress 内置搜索的摘要是从 md 提取的**纯文本**，结果项里公式一律以 `$…$` / `$$…$$` 原文出现（实测 47 个结果项、数百个 `$`）。结果项是真实 DOM，交给 MathJax 重排即可——增强脚本对 `.VPLocalSearchBox` 挂 MutationObserver + 350ms 节流 typeset，点击搜索按钮后挂载。
- 实测：输入「量纲发生学」→ 47 个结果项生成 **312 个 `mjx-container`**，裸 `$` 残留 **1**。

**2. Lean 集成进研究站（服务端 + 前端）**
- **服务端** `LeanController`（`/api/lean/*`，全部只读除编译外）：
  - `GET modules`：68 模块清单（各类型声明计数）；`GET decls?module=&kind=`：1 388 条声明（def 419 / theorem 822 / lemma 45 / **axiom 28** / structure 53 / class 4 / inductive 7 / abbrev 10）；
  - `GET mapping`：概念/命题/缺口 ↔ Lean 符号的人工映射（25 条，来自 `Lean↔概念映射.csv`）；
  - `GET source?file=`：Lean 源码文本（路径规范化防 `..` 越界）；
  - `POST build` + `GET build`：**站内编译**——`lake build` 在 `Lean源码/` 目录运行（lake 路径与目录可配 `cqm.lean.*`），单实例串行、15 分钟超时、输出截断保存、`build-enabled` 可关。
- **前端** `LEAN_Lean对接.md` + `public/lean-page.js`（导航新增「Lean 对接」组）：
  - **模块与声明**：左侧模块列表、右侧声明表（kind 徽章、名称搜索、种类筛选），点位置即拉取源码并滚动到行；
  - **概念 ↔ Lean**：25 条人工映射 + **axiom 待证清单**（28 条物理假设的 Lean 承载，原样登记不升格）；
  - **编译**：一键触发 + 实时状态与输出日志。
- **统一口径**（呈现边界写死在页面上）：形式化覆盖 **41/82 概念**——未覆盖概念不得视为已形式化；缺口状态与「待证」限定语保持权威源口径；映射由人工整理，机器不推断新对应。
- **编译实测**：`POST /api/lean/build` 真实触发，lake 进程运行中输出 `✔ [787/2200] Built Mathlib.…`——本次是 **Mathlib 依赖的首次完整构建（2 200 步）**，需较长时间；完成后产物缓存，后续增量构建会显著加快。前端轮询、进度与日志均实测可用。
- 机制验证：`/api/lean/modules`、`decls?kind=axiom`（28 条）、`mapping`（25 条）、`source` 冒烟全通过；`LEAN_Lean对接.html` 渲染出 1 388 条声明表（600 行视口）与三个页签，零渲染残留。

**3. 验收**：端到端 `verify_station` **29/29**；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 **32 → 64 → 102 → 107**；站内链接失效 **0**。
- 同步：`09 研究站服务`（`LeanController.java`、`StationProperties.java`、`application.yml`）、`_build/build_vitepress_site.py`（LEAN 页/lean-page.js/搜索 typeset 钩子/分组与导航）、本日志、`验证状态.md`。

## v1.9.6 — 可视化页公式渲染 · 缓存治理 · 真实交互探测工具

> 用户继续报「渲染/排版异常、公式要修、蓝色弹层还有异常、** 也有异常、搜索不能点击」。本轮用 **CDP 真实交互探测**（Edge 无头 + remote-debugging-port + websockets：真的点按钮、真的输入查询、真的悬停触发卡片、真的收集控制台异常与失败请求）逐页核对，把问题定位到三处，全部修掉。

**1. 可视化页（检索台/驾驶舱等）公式全部裸露**
- 这四个页面是自包含 HTML，**本身不带 MathJax**；而它们的正文公式是 **JS 运行时生成**的（检索台的实体/证据卡、驾驶舱的公式面板），构建期静态扫描看不到——打开页面就是 111 处 LaTeX 原文（检索台实测）。
- 修法：构建期给 `public/viz/*.html` 注入本地 MathJax + 一个「DOM 变化后节流重排」的钩子（检索台的结果是点击/输入后动态渲染的，只在 DOMContentLoaded 排一次不够）。
- 实测：检索台 `rawDollar 111 → 0`、`mjx 139`；驾驶舱 `mjx 156`、残留 0；超图/蓝图无公式、无残留。

**2. 缓存治理——「明明修好了、页面上却还是老样子」**
- 研究站的增强脚本（`cqm-enhance-vp.js` / `cqm-glossary.js` / `vp-math.js` 等）**文件名不带内容哈希**，服务端此前也不发任何缓存指令 → 浏览器启发式缓存旧脚本，重建后用户看到的仍是修复前的行为（这正是用户反复报「还是异常」的主要来源之一）。
- 双重修复：服务端 `spring.web.resources.cache.cachecontrol.no-cache: true`（静态资源一律协商缓存，实测响应头 `Cache-Control: no-store`）；构建期给 head 里所有无哈希资源挂版本串 `?v=构建时间戳`。

**3. 导航栏「高级检索」按钮在重页面丢失**
- `D009` 一页就有 466 个内容块、上千个公式，Vue 渲染导航栏明显更晚；固定 20 次 × 200ms 的重试会在这类页面耗光而漏挂。改为 `MutationObserver` 观察 DOM 直到按钮挂上（挂上即断开，45s 兜底超时）。
- 实测：10 个代表页面（首页/D001/D009/D024/D029/L000/L001/L002/V000/F02）全部「搜索按钮 + 高级检索按钮」双入口在线。

**4. 新增真实交互探测工具（`.workbuddy/tools/`，临时工具不入库）**
- `browser_probe.py`：CDP 驱动 Edge 无头浏览器，逐页检查控制台异常、搜索按钮可点性与搜索结果、术语卡悬停渲染、可见文本残留；支持全站遍历与全量 138 张术语卡逐一注入真实排版。
- `page_probe.py`：通用页面交互探测（控制台/失败请求定位/输入框可交互性/渲染残留/截图）。**关键手法**：先停在 `about:blank` 接管 CDP 再导航，否则页面加载期间的异常会在 `Runtime.enable` 之前全部漏掉（曾因此误判检索台「无报错」）。

**5. 验收（全部实测）**：全站 10 个代表页零残留（`$` / `**` / 反引号）；检索台搜索输入即出结果；138 张术语卡真实排版 `badN=0`；端到端 `verify_station` **29/29**；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 **32 → 64 → 102 → 107**；`generator = VitePress v1.6.4`。
- 同步：`_build/build_vitepress_site.py`（viz MathJax 注入、资源版本串、MutationObserver 挂载）、`09 研究站服务/src/main/resources/application.yml`（缓存治理）、本日志、`验证状态.md`。

## v1.9.5 — 术语悬浮卡渲染修复 + 阅读体验增强

**1. 悬浮卡里的公式与代码（用户报「蓝色下滑弹出解释里面公式、内容没渲染」）**
- **公式**：卡片文字里的公式写作 `\\(…\\)`（Material 时代 arithmatex 转出的形式，全站 140 处；块级 `\\[…\\]` 7 处），而 MathJax 只配了 `$…$` / `$$…$$`，故卡片里的公式一律以 LaTeX 原文露出。改为**四套分隔符同时支持**（`$…$`、`$$…$$`、`\\(…\\)`、`\\[…\\]`）。对照实验：三类分隔符混排后，渲染后 DOM 里反斜杠括号残留均为 **0**，`mjx-container` 正常生成。
- **行内代码**：卡片文字里的 Lean 模块名等带反引号（如 `` `FGChain/` ``），此前按字面显示反引号。现注入时把 `` `…` `` 落成 `<code>…</code>`（并做 HTML 转义）。

**2. 阅读体验增强（联网调研后按本项目实际取舍）**
- 调研结论：社区主流是 Nolebase 的 `vitepress-plugin-enhanced-readabilities`（可调侧栏宽、聚焦模式）、`enhanced-mark`（高亮动画）、`inline-link-preview`（链接悬停预览）、`back-to-top` 等；而 **VitePress 的已知痛点是长公式会撑破版心**（MathJax 生成的 SVG 默认不换行、不加滚动条），官方主题另已内置表格横向滚动、目录高亮、代码复制。
- 本项目据此只补**缺的那几处**，全部自研、纯 CSS/原生 JS、零依赖、离线可用：
  1. **长公式横向滚动**：`mjx-container` 限宽 + `overflow-x:auto`（含行内与块级，卡片与检索结果同样限宽）。
  2. **中文长段落排版**：行高 1.9、段距 1em、列表项行高、标题前留白加大、`h2` 加分隔线、引用块用品牌色左边框。
  3. **表格**：按内容撑开（`width: max-content`）+ 最小列宽 + `word-break: keep-all`——默认 100% 宽会把中文列压成**逐字竖排**（实测），宁可整表横向滚动。
  4. **锚点定位**：`scroll-margin-top` 使标题不被顶部导航遮挡，`:target` 给一次品牌色高亮。
  5. **长文档仪表**：页顶阅读进度条 + 右下角「回到顶部」按钮（滚动 320px 后出现），打印时隐藏。
  6. **外部链接新窗口打开**（`target=_blank` + `rel=noopener`），避免研究中途离开本站。

**3. 验收**：端到端 `verify_station` **29/29**；站内链接 **120** 条失效 **0**；深度滑杆 **32 → 64 → 102 → 107**；`check_consistency` **41/41**；`check_provenance` **10/10**；`generator = VitePress v1.6.4`。新增样式文件 `public/vp-read.css`，与 `vp-brand.css` 并存，不覆盖主题默认样式。
- 同步：`_build/build_vitepress_site.py`（MathJax 分隔符、`cardHtml()`、`vp-read.css`、`mountReadAids()`、`fixExternalLinks()`）、本日志、`验证状态.md`。

## v1.9.4 — 研究站：启用内置搜索 · 站内 404 清零 · markdown 语法大面积失效修复

> 用户报「搜索没有、有些 404、各种渲染异常」。三类问题都定位到确定根因，并用**普查脚本 + 无头浏览器实测**逐项核对。

**1. markdown 语法大面积失效（加粗 6 113 处未解析）—— 自上一轮引入的回归**
- **根因**：上一轮为让 `$` 成为 markdown-it 的文本终止符，**替换了 text 规则却只抄了 11 个终止字符**，漏掉 `* _ ~ ^ = : + - @ # %`。其中 `*` 是加粗语法的起点，缺了它，`**粗体**` 被 text 规则整段吞下、emphasis 规则再无机会触发。而 markdown-it 原版终止表**本来就有 `$`**，那次替换纯属多余——替换已撤销，恢复原版行为。
- 实测：加粗字面 **6 113 → 0**；页面 `<strong>` 由 0 增至 **773** 处。
- **第二类**：中文标点旁的强调被 CommonMark 的 flanking 判定误判——`**“存在论相变”**`（左 `**` 右侧是“、左侧是汉字）、`**可观察子群（observable subgroup）**问题`（右 `**` 左侧是）、右侧是汉字）都不满足开闭条件，故整段保留字面（Material 时代的 Python-Markdown 规则宽松，此前不显）。构建期把这类成对 `**…**` 提前落成 `<strong>…</strong>`（跳过代码围栏；行内代码先取走再放回）。
- **第三类**：裸文本下标被配成斜体——`U(1)_B、U(1)_B-L、U(1)_Y` 渲染成 `U(1)<em>B、U(1)</em>B-L`。给 `_`（前为字母/数字/右括号、后为字母/数字/左括号）加反斜杠转义，输出仍是字面下划线，视觉不变。
- 注：`L000 展开链` 页里的「方括号文字 + 圆括号地址」行内链接**字面**是**有意**的（该页声明逐字摘录，构建时即转义，以免产生死链），不属缺陷。

**2. 站内 404 清零（7 条 `/_src/…html`）**
- mkdocs_src 里的行内链接形如「［理论组织和形式化框架总览］(./_src/08 …/README.html)」（原为半角方括号）——那是 Material 站把源文档编译进 `_src/` 后的地址。VitePress 不处理 `_` 前缀目录，站内没有 `_src/`，故全部 404。
- 处理：站内**已有**对应渲染页的改指过来（`README` → `/F02_README`、`AGENTS` → `/F01_AGENTS`）；没有对应页面的（归档文档、LICENSE、元数据）**降级为纯文本**，不留死链。
- 验收：`.workbuddy/tools/link_audit.py` 遍历全部 52 页的 119 条站内链接逐个请求 → **失效 0**。

**3. VitePress 内置搜索（此前完全没配）**
- 现象：导航栏没有搜索按钮、`Ctrl/⌘+K` 无反应——`config.mts` 里根本没有 `search` 配置。
- 启用官方 `provider: 'local'`：构建期生成索引（**4.7 MB**，站内自带、离线可用），导航栏出现「搜索」按钮与 `Ctrl K` 提示，`detailedView` 打开详细结果列表，界面文案中文化（按钮/无结果/页脚快捷键）。
- **中文分词**：minisearch 默认把连续 CJK 当成一个词，中文查询几乎命中不了。故自定义 `tokenize`——中文按「单字 + 二元」切分、拉丁按词，索引与查询共用；实测索引内含「退相 / 相变 / 前时空 / 自守 / qubit / GL(5)」等 token。
- 与既有的自研**结构化检索**（导航栏「高级检索 Ctrl+Shift+K」，走实体/缺口/证据索引）并存，两者互补：前者全文、后者实体。

**4. 新增两个可复用的普查工具**（`.workbuddy/tools/`，临时工具不入库）
- `link_audit.py`：遍历 dist 所有 HTML 的 `href/src`，逐个请求判定 404，按 URL 归并列出受影响页面。
- `render_audit.py`：剔除 `<code>/<pre>/<script>`、`$…$` 公式区间与全部标签后，统计加粗/斜体/行内代码/链接/删除线/高亮/上标/标题/表格/引用/列表等语法的字面残骸。

**5. 导航栏「高级检索」按钮整轮丢失（异步渲染竞态）**
- `mountNav()` 只在首次初始化跑一次，而 VitePress 的 `.VPNavBarMenu` 由 Vue **异步**渲染——首次执行时它往往还不存在，函数直接 return 且不重试。服务徽标因 `fetch` 的天然延迟躲过了这个坑，反而掩盖了问题。
- 另有第二重隐患：`mountNav()` 的「是否已挂载」判定用了 `.cqm-sbtn`，而服务徽标的 class 也含它，徽标先到时会顶掉该判定。现改用专属 class `.cqm-advbtn`。
- 修法：`mountNav()` / `probeService()` 移入 `initPage()`（每次路由切换都确保），并对首发未挂上的情形做定时重试兜底。
- 实测：导航栏三个入口并存——VitePress 搜索（`DocSearch-Button` + `Ctrl K`）、高级检索（`cqm-advbtn` + `Ctrl Shift K`）、服务徽标（`cqm-badge`）。

**6. 构筑期死链检查开启（把验证交给构建器）**
- 此前为兼容那 7 条 `_src` 链接设了 `ignoreDeadLinks: true`——它让构建不报错，却同时掩盖了所有失效链接。链接修好后改为 `false`：VitePress 现会在构建时**点名**文件与失效目标。本次构建一次通过，等价于一次全量链接验证。

**7. 验收（全部实测）**：站内链接失效 **0**（119 条逐个请求）；加粗字面 **0**；可见文本公式残留 **0**；`mjx-container` **2 629**；端到端 `verify_station` **29/29**；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 **32 → 64 → 102 → 107**；VitePress 死链检查开启后构建通过。
- 同步：`_build/build_vitepress_site.py`（撤销 text 规则替换、`fix_cjk_bold`、`fix_src_links`、search 配置与中文分词）、本日志、`验证状态.md`。

## v1.9.3 — 研究站渲染修复：公式排版 · 超图资源 · 蓝图配色 · UTF-8 响应头

> 本轮全部结论都由**实测**得出（Edge 无头截图人眼复核 + 渲染后 DOM 比对），不靠推断。

- **公式排版（三类根因，逐层剥开）**：
  1. **主题缺实现**：`build_vitepress_site.py` 生成的 `.vitepress/theme/index.js` 注释写着"重排公式"，代码里却没有 `typesetPromise()`——VitePress 只在文档加载时自动排版一次，之后客户端路由切换、Vue 异步渲染的侧栏/大纲都不再排。现由主题在**每次路由切换后**主动排版，并对尚未就绪的 MathJax 做轮询重试（另在 150 ms / 500 ms 各补一次，覆盖侧栏与大纲）。
  2. **markdown 抢先破坏公式**：VitePress 默认不带数学插件，markdown-it 先把公式当普通文本解析，`$$\\mathbb{R}_{>0}$$` 被强调规则解析成 `\\mathbb{R}<em>{>0}</em>`、`\\\\`（LaTeX 换行）被转义规则解析成 `<span>\\</span>`——**标签一插进公式，MathJax 就再也匹配不到这对定界符**，公式只能以 LaTeX 原文裸露。VitePress 把 markdown-it 打包进自身 bundle（顶层无该包），改其内部规则不可靠，故改为**构建期把公式整段换成纯 ASCII 占位符**（本轮 12,208 处），构建完成后在产物里还原：`.html` 做 HTML 转义、`.js` / `.json` 做 JSON 转义。
  3. **术语标注二次破坏**：`cqm-enhance-vp.js` 的术语标注把公式 `\\text{…中文…}` 里的中文（"时间""长度""质量"等）当术语包成 `<span class="cqm-term">`，把公式切碎。现让标注**跳过 `$…$` / `$$…$$` 区间**，并把 MathJax 产物（`mjx-container`、`mtext`、`mi`、`mo` 等）加入跳过清单。
  - 验收：`$` 内标签注入 **9 → 0**；DOM 里该公式为 `<menclose notation="box"><mtable>…<mtext>`（`\boxed`/`aligned`/中文全部正常）；文本节点残留 `$…$` 仅剩标题锚点 `aria-label` 与内嵌 JSON 数据（均不可见）。
- **可推演超图（V001）图谱空白**：页面引用 `assets/cytoscape.min.js`，而 `public/viz/` 下依赖是平铺的 `cytoscape.min.js`，请求 404 致整图不绘制（该缺陷在 Material 版时代即存在，未被端到端检查覆盖）。构建期在 `public/viz/*.html` 副本上改指同目录（源文件不动），并在日志中报出改写文件数。
- **形式化蓝图（V004）白块遮字**：`header{…color:#fff}` 之下，`<code>` 自身背景是近白色 `#fdf3e0`、文字色继承白色 → `…状态以 08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md 为权威` 整条不可见。`build_lean.py` 的样式模板为 `code` 补 `color:var(--ink)`。
- **编码（响应头 charset）**：静态资源原先只回 `text/html`、`text/javascript`，不带 charset；页面虽有自己的 `<meta charset>`，但响应头 charset 优先级更高，显式声明可避免个别浏览器与嵌入场景回落 GBK。`application.yml` 增 `server.servlet.encoding`（UTF-8 / enabled / **force**），实测 `Content-Type: text/html;charset=UTF-8`。产物侧同步扫描 178 个 HTML/JS/JSON/CSS：**U+FFFD 与不可解码文件均为 0**。
- **验收**：端到端 `verify_station` **29/29**（新增 2 项 charset 断言）；`check_consistency` **41/41**；`check_provenance` **10/10**；深度滑杆 `depth_sim_vp.py` 仍为 **32 → 64 → 102 → 107**（单调、断点块不被隐藏）；术语标注 30 处/页、公式 2,629 个 MathJax 容器并存不冲突；`generator = VitePress v1.6.4`。
- 同步：`_build/build_vitepress_site.py`（数学占位符、viz 改写、主题重排、术语标注避让）、`_build/build_lean.py`（蓝图配色）、`09 研究站服务/src/main/resources/application.yml`（编码）、`.workbuddy/tools/verify_station.py`（charset 断言）、本日志、`验证状态.md`。

## v1.9.2 — 研究站换用 VitePress（生成器切换 · 增强移植 · 单一入口收敛）

- **生成器切换**：研究站由 Material for MkDocs 换为 **VitePress v1.6.4**（用户指出该形态为众多官方资料站所采用）。新工程 `10_展示可视化/阅读站VitePress/`（`package.json` + `.vitepress/theme/index.js` + `docs/` + `.vitepress/dist/`）；新脚本 `_build/build_vitepress_site.py` 从 `_build/mkdocs_src/docs`（`build_reader_site.py` 的 stage 产物）生成 `docs/` 与 `config.mts`，随后调 `vitepress build`；`build_reader_site.py` 现仅承担 stage 环节。成品页头 `generator = VitePress v1.6.4`。
- **构建期的四处硬约束**（均为实测得出，勿回退）：
  1. **整页 `<div v-pre>`**：源文本含 `{{ }}` 会被 Vue 当插值解析并报错；实体转义方案因源里另有 `\\{\\{` 写法覆盖不全而回退，改用 `v-pre` 整页屏蔽（50 页）。
  2. **数学不引 CDN**：不启用 `markdown.math`（会拉 `markdown-it-mathjax3` 及其外链），改由 `head` 注入随包 `vp-math.js` + `tex-svg.js`，分隔符 `$…$` / `$$…$$`。
  3. **依赖安装**：npmmirror 缺 `@algolia/client-personalization@5.60.0`，须用官方源；平台 optional 包 `@esbuild/win32-x64`、`@rollup/rollup-win32-x64-msvc` 必须**同一条命令**装（分次安装会互相当作外来包移除）。
  4. **`ignoreDeadLinks: true`**：7 条链接指向 `_src/` 语料源，属既有登记现象。
- **交互增强移植**（`cqm-enhance-vp.js`，由自定义主题 `enhanceApp({router})` + `onAfterRouteChanged` 逐页重跑）：术语/缺口悬浮卡（数据 138 卡 / 检索索引 341 / termKeys 106）、四层深度滑杆（导读/概念/链条/技术）、结构化检索改为 **`Ctrl/⌘+Shift+K`**（避开 VitePress 自带的 `Ctrl+K`）、服务探测徽标改挂 `.VPNavBar`。
  - **关键坑**：`v-pre` 使 `h2/h3/p` 成为孙节点，而深度滑杆遍历直接子块 → 四层恒显示 1 块、形同失效。修法为新增 `contentRoot()` 在被 `v-pre` 包住的单一 div 中逐层下潜取真实顶层块；模拟器 `.workbuddy/tools/depth_sim_vp.py` 按同规则复算：**L001 = 32 → 64 → 102 → 107 块、L002 = 27 → 38 → 84 → 86 块**（单调），断点与限定语块在任何深度均未被隐藏，与历史基准一致。
- **离线取舍（诚实边界）**：VitePress 的本地检索依赖 `fetch` 取 JSON 分片，且默认 `base: '/'` 用绝对路径 → **`file://` 双击直开会丢资源**。研究站因此确立为「须经 HTTP 提供」：服务在场时访问 `http://127.0.0.1:8080/`；需要完全离线的场合仍用 `源_可视化/` 下的自包含 HTML。
- **服务侧**：`09 研究站服务` 的 `site-dir`、`chain-file` 改指 VitePress 的 `dist`；README 登记已知边界——`mvn spring-boot:run` 在中文含空格路径下 fork JVM 会报 `ClassNotFoundException`，一律用 `mvn -s settings.xml package -DskipTests` + `java -jar`。
- **端口冲突**：`D:\\WorkSpace\\AI\\llm` 的 `start-llm.bat`、`start-chat.bat` 原先写死 `--port 8080`（llama.cpp 自带 Web UI 会抢占研究站端口），分别改为 **8082 / 8083**，`start-cqm.bat` 保持 8081，README 增补端口分配说明（8080 = CQM 研究站）。
- **单一入口收敛**：Material 版阅读站 `10_展示可视化/阅读站/` 于 2026-10-13 经用户裁定**移除**（115 个文件随本次提交从版本记录中去掉），VitePress 站为唯一入口；`10_展示可视化/README.md`（表格行、单一入口、应用层、打开方式四处）、`03_超图与理论图/README.md`、`08/AGENTS.md`、`08/README.md`、`_build/build_site.py`（驾驶舱链接改指研究站首页）同步改指。viz 由构建脚本复制到 `docs/public/viz/`，站内路径为 `/viz/`。
- **检查脚本范围修正**：`check_consistency.py` 与 `build_meta.py` 的 md 全量扫描新增排除段 `阅读站VitePress/docs`（stage 中间物，内容为 `01`–`07` 源语料副本，受「外部文本不动」约束，不由组织层文字规范评判）与 `node_modules`（第三方依赖）；两处此前各报 1 项失败，属扫描范围问题而非产物缺陷。
- **验收**：`generator = VitePress v1.6.4`；三个增强 JS `node --check` 通过；端到端 `verify_station.py` **27/27**（静态站 4 / status 9 / 检索 2 / SPARQL 3 / 条目 4 / 复核写回 5）；`check_consistency` **41/41**；`check_provenance` **10/10**；服务侧读到 KG **5,153** 三元组、站点 56 个 HTML。
- 同步：`10_展示可视化/README.md`、`08/AGENTS.md`、`08/README.md`、`03_超图与理论图/README.md`、`09 研究站服务/README.md` 与 `application.yml`、`.gitignore`（`node_modules/` 与 `.vitepress/cache/` 不入库，`dist` 作为产品入库）、本日志、`验证状态.md`。

## v1.9.1 — 目录收敛：撤销「一体化研究」、可视化源合并、09 服务目录加空格

- **撤销 `一体化研究/`**（2026-10-13，用户裁定"这个目录没有用了"）：站点仍依赖的内容迁入正式位置——`附录/术语表.md`、`附录/缺口台账.md` → `08 理论组织和形式化框架/附录/`（引用清单 D003/D004 路径同步改指，doc_id 不变）；`展开链讲稿/` → `10_展示可视化/讲稿/`；其余（科研AI全栈方案、组织层对标与完善方案、CQM研究站架构方案、文献、研究日志、展开链骨架样例）→ `归档/一体化研究/`。核对依据：**证据层 0 条断言引用该目录的文档**（那 11 条仅语料登记），故不影响 `check_provenance` 的逐字核对；该目录已不存在。
- **可视化源合并**：`10_展示可视化/{网站,检索台,交互式可视化,蓝图}/` 四个目录收敛为 `源_可视化/`（研究驾驶舱／检索台／超图交互；蓝图唯一一份留 `04_Lean对接/蓝图/`，`build_site.py` 不再同步副本）；删除 `03_超图与理论图/超图可视化.html` 与 `03_.../assets/`（同构件副本）。`build_site.py`／`build_search.py`／`check_consistency.py`／`build_reader_site.py` 的输出与检查路径同步改指。
- **`09_研究站服务` → `09 研究站服务`**（与其他编号目录一致加空格）；`.gitignore` 同步。
- **权威计数变更（有依据，勿回退）**：句索引的 sid 为全局编号，两份文档从 `一体化研究/附录/` 移入 `08.../附录/` 后扫描次序变化，导致机器推断边 `P010—证据句提及概念→C048` 的匹配句位移而消失（知识图谱 145 实体 / **359** 边，原 360），同时证据个体由 214 补齐为 215（本体 25 类 / **430** 个体 / 16 对象属性，原 429）。**源数据未变**（概念 82 / 命题 63 / 论证 70 / 证据 215），逐字引文核对不受影响（`check_provenance` 10/10）。
- **验收**：`check_consistency` **41/41**、`check_provenance` **10/10**；阅读站重建警告 0（讲稿两分册 + 展开链 + 可视化总览均在）；`01`–`07` 理论文本未动。
- 同步：`10_展示可视化/README.md`、`02_概念本体/README.md`、`03_超图与理论图/README.md`、`报告/建设报告.md`、`00_外部引用/引用清单.yaml`、`_build/*.py`、本日志、`验证状态.md`。

## v1.9.0 — 阅读站增强：术语悬浮卡 · 缺口徽章 · 高级检索 · 展开链页

- **对标（联网调研结论）**：搜索侧主流是构建期静态索引（Pagefind：Astro Starlight 默认，中文分段好、索引小，但依赖 `fetch`/Worker，**`file://` 不可用**）、托管服务（Algolia DocSearch / Meilisearch，需服务与联网）与客户端库（lunr / MiniSearch / FlexSearch：倒排索引 + 前缀 + 模糊 + `storeFields` 生成摘要）。术语悬浮侧，Material 官方只有 `abbr` + `content.tooltips`（缩写级短提示）；"悬停链接出现整段预览卡"的主流实现是 Quartz 的 popover previews（`@floating-ui` 定位 + `flip/shift` 防溢出 + 遮罩类选择正文 + 移动端隐藏）。
- **决策**：全文检索继续用 Material 内置（lunr + 官方 zh + 构建期 jieba + CQM 用户词典，`file://` 下即可用）；**新增一层自研结构化实体检索**，不引入任何外部 JS。
- **新产物**（均由 `_build/build_reader_site.py` 构建期生成，随 `extra_javascript`/`extra_css` 挂载，全站 45 页均注入）：
  - `assets/cqm-glossary.js`（271 KB）：**138 张卡**（概念 82 + 别名、缺口 24）＋ **检索索引 339 条**（概念 82 / 命题 39 / 缺口 24 / 符号 21 / 文档 42 / 展开链步 131）；卡片文字**逐字**取自 `概念表.csv`、`缺口编号对照.csv`、`符号对照表.csv`、`证据映射.csv`；
  - `assets/cqm-enhance.js` ＋ `assets/stylesheets/cqm-enhance.css`：术语/缺口标注（每术语每页 ≤ 3 次、全页 ≤ 240 次）＋ 悬浮卡（`flip` 防溢出、`Esc` 关闭、滚动隐藏、`focus` 可及）＋ **高级检索**（`Ctrl/⌘+K`、`/` 或顶栏按钮；分类 facet、CJK 一元＋二元打分、结果 `<mark>` 高亮、`↑↓`/`Enter` 键盘导航、可一键转全文检索）；
  - `L000_展开链.md` → `L000_展开链.html`（201 KB）：**131 条**原文箭头链条句逐字汇总，按「文档层级 → 文档 → 行号」机械排序，每条附字符区间、涉及缺口、状态词；末尾为**缺口断点清单**（24 缺口，逐字取自缺口编号对照）；判据与局限在页内如实登记；
  - `阅读站/README.md`：构建期写入站点根（此前变更日志记其"重建"而实际被站点清理步骤删除，此处纠正——README 改由构建脚本写入，随站点一同重建）；
  - **展开链讲稿页**（`L001_…`）：staged `一体化研究/展开链讲稿/*.md`（**撰述**稿，非摘录、非理论语料，不进引用清单），导航紧随展开链页；讲稿含锚点表（文档＋章节＋核对状态）与「引文保真六关」自检；
  - **深度滑杆**：讲稿页顶部粘性条，四档＝导读(1)／概念(2)／链条(3)／技术(4)，按二级章节映射（`assets/cqm-depth.js`）在运行期给块打深度；**断点与限定语块不随深度隐藏**（只认缺口编号与限定语，不用泛词——早期版本用"缺口/不得"等宽词表，实测导致第 2 层往后几乎不隐藏，滑杆形同失效，已收紧）；被隐藏标题若其下仍有可见块则做救援显示；选择记入浏览器本地；
  - **可视化整合为单一入口**（2026-10-13）：原分散的四件自包含 HTML（`交互式可视化/超图交互.html`、`网站/index.html`、`检索台/index.html`、`蓝图/index.html`）收进阅读站「可视化」栏目（`V000` 总览 + `V001–V004` iframe 包装页），HTML 落 `assets/viz/`（含随包 `cytoscape.min.js` 425 KB 与 `驾驶舱数据.json` 329 KB），构建期复制并改写其相对引用与跨链，**不改源文件**；站点文件数 117 → 128，构建警告 0。
- **口径**：增强层是**呈现层**，权威源仍是各文档原文与 `README.md`；构建脚本只做拼装与定位，**不改写任何表述**，不改数值、不改缺口状态，缺口与限定语原样呈现。
- **验收**：构建 `exit=0`、警告 **0** 条；45/45 页注入增强脚本；`node --check` 三个 JS 均通过；成品零外链**资源**（脚本 `src` 外链计数 0）；术语卡含出处文档/字符区间/置信度。**深度滑杆**（`assets/cqm-depth.js` + `cqm-enhance.js` 的 `initDepth`）经离线按块模拟校验：第 1→4 层显示 **32 → 64 → 102 → 107** 块（单调递增），断点/限定语块在任何深度均未被隐藏，11/11 章节被映射覆盖（模拟器 `.workbuddy/tools/depth_sim.py`，临时工具不入库）。
- 同步：`10_展示可视化/README.md`、`_build/README.md`、`验证状态.md`（阅读站增强行）、本日志。

## v1.8.0 — 阅读站重建：Material for MkDocs + jieba 中文搜索（file:// 离线可用）

- **动机（联网调研结论）**：旧自研单页阅读站的全文搜索是 `t.indexOf(lq)`（`build_reader.py:397`）——无分词、无排序、无相关性。选型对比官方文档：[Material for MkDocs 搜索插件](https://squidfunk.github.io/mkdocs-material/plugins/search/)（lunr + **官方 zh + 构建期 jieba 分词 + 用户词典**）、[Material 离线构建](https://squidfunk.github.io/mkdocs-material/setup/building-for-offline-usage/)（`offline` 插件官方保证分发即用、搜索离线可用）、[Pagefind 多语言](https://pagefind.app/docs/multilingual/)（中文分段更强但依赖 fetch/Worker，**file:// 不可用**，需本地 HTTP 服务器）。经确认选择 **Material + offline + jieba**（保住 file:// 双击即开）。
- **新脚本** `_build/build_reader_site.py`（`build_reader.py` 保留存档）：
  - 语料口径与旧站一致（根 README + 01–07 + 一体化研究/附录，**只读**），staging 落 `_build/mkdocs_src/`（不计产品文件、不进 md 扫描）；
  - **CQM 用户词典 166 词条**（概念名/同义词/符号名与符号/缺口编号）→ 术语级检索；`相变量子` 整词入索引 **174 次**、`退相干` 619、`同步算符` 418；
  - `offline` 插件内联搜索索引（4.3 MB / 1708 段）→ **file:// 搜索可用（浏览器注入实测命中）**；`privacy` 插件本地化外部资源、`font:false` → **54 页零外链资源加载**；
  - `use_directory_urls: false` 平铺 `.html`（file:// 直开必需）；`pymdownx.arithmatex` + 随包 `tex-svg.js` 渲染公式；跨文档链接按输出位置改写（含 `_src` 深层），构建警告仅剩 1 条已登记（jsdelivr wgxpath 下载失败 → 引用已从成品移除，仅影响极旧浏览器 XPath 兼容）。
- **验收**：`check_site_reader.py` **10/10**（索引整词/零外链/平铺/浏览器端搜索实测）；`check_consistency` 41/41、`check_provenance` 10/10。
- 同步：`10_展示可视化/README.md`、`阅读站/README.md`（重建）、`_build/README.md`、`AGENTS.md`（§六 执行顺序与依赖、§九 命令速查）、`设计方案.md`（阅读站工具行 Quarto → Material 并登记决策变更）、`验证状态.md`（依赖 + 验收行）。

## v1.7.2 — 蓝图页可视化升级 · 缺口依赖链 · 复核状态回显

- **蓝图页**（`04_Lean对接/蓝图/index.html`，同步 `10_展示可视化/蓝图/`）由两张表升级为：6 项 KPI + **映射覆盖环**（映射计算恰为 **41/82 · 50.0%**，与组织层 README 权威口径的一致性由 JS **动态判定**并随数据变化自动报警）+ **声明构成 8 类分段条**（theorem 822 / def 419 / structure 53 / lemma 45 / **axiom 28** / abbrev 10 / inductive 7 / class 4）+ **axiom 待证焦点清单**（抽取 28 条 ↔ 权威 README「30 公理待证」**双口径并列登记，不擅自统一**）+ **模块声明色带 Top18** + 可筛对照表（25 条）与模块统计表（按合计降序，55 个有声明模块）。
- **驾驶舱命题面板**新增**缺口依赖链 SVG**（`G2→G3→G4→G5`，按状态着色，来源 命题表.depends_on 与 缺口依赖闭包.md §二）与**按编号系分组的状态色带**（核心 C / G2–G8 / G9–G22 / N1–N4）；**未数据化的依赖不推断、不补边**（hint 明示）。
- **复核状态回显**：驾驶舱证据表新增「复核」列、检索台证据卡新增复核标签（verdict + 复核人），与 v1.7.1 复核闭环打通。
- 验证：蓝图 jsdom **11/11**、驾驶舱/超图/检索台套件全通过；双硬检查 **10/10 + 41/41**；真实 Edge 标记渲染通过。

## v1.7.1 — 复核闭环 · 分层抽取逼近上界 · 零覆盖候选 · LLM 就绪管线

**1. 证据复核闭环（verified 置真的唯一合法路径）**
- 检索台新增**「证据复核」模式**：逐条展示断言与原文定位，判定 通过/驳回/存疑 + 复核人 + 备注；草稿存浏览器 localStorage；快捷键 1/2/3 与 ←/→；支持 CSV 导出/导入。
- 导出为 `00_外部引用/复核结果.csv` → 重跑 `build_evidence.py` 合入 `review_*` 字段；**`verified = (verdict=approved 且 reviewer 非空)`**；「通过」在复核台必须填写复核人。
- `check_provenance.py` 增至 **10 项（无复核文件）/ 13 项（有复核结果）**，含三条闭环硬校验：「复核 struct_id 必须存在于证据映射」（伪造 id 实测被拒收）、「approved 均带复核人」、「verified ⟺ approved 且有复核人」；无复核文件时断言 verified 全为 `False`。
- 管道自测：3 条合法记录 13/13 通过 → 删除自测文件重置 verified → 10/10 通过（**不留下伪造记录**）。

**2. 关系抽取改为分层候选，无向召回逼近物理上界**
- **pattern 层**（259 条）：两端间有关系线索词 → 类型可推断（P=0.069，类型命中率 0.111）；**cooccur 层**（661 条）：仅同句共现、类型标「未定」、方向按文本顺序 → 交人工/LLM 定型。
- 无向配对召回 0.474 / 物理上界 0.50 = **达上界 95%**（v1.7.0 为 28%）；有向 P/R 与分层指标同报（`precision_pattern` `recall_pattern` `recall_pair_unordered` `cooccur_only_candidates` 等新增字段）。

**3. 零覆盖语料的结构化候选**
- 21 篇零结构化条目语料逐篇跑新词发现（freq≥3 / PMI≥6 / 熵≥0.8），输出 `05/术语候选/零覆盖语料候选.csv`（**305 条**，含示例句，状态「候选待核」）——只进候选池，**不写入概念表**。

**4. LLM 关系定型（OntoGPT/SPIRES 风格 · 就绪管线）** `_build/llm_extract.py`
- schema 固定 6+1 类（不引入理论外语义）；模型须返回 `rationale_quote`，**程序要求其逐字命中候选句（span 校验），否则丢弃**——不采信无 span 的输出。
- 输出 `LLM定型候选.csv` 仅为候选；**无 `CQM_LLM_*` 环境变量时打印就绪说明并退出 0**，登记为「就绪未执行」（与 torch/dowhy 等未装依赖同一诚实口径）。

**5. 同步范围**：`00_外部引用/README.md`（复核闭环流程图）、`_build/README.md`、`AGENTS.md`（命令速查 + 复核闭环）、`10_展示可视化/README.md`、`验证状态.md`（LLM 就绪登记）、本日志。

## v1.7.0 — 证据层 · 主张图 · 公理与校验 · 抽取流水线 · 检索台

本轮针对"结构化层信息密度不足、无溯源、无主张网络"的系统性缺陷，按主流知识工程流水线补齐五层，
并全部纳入 `check_consistency.py` 硬检查（**41 项**）与 `check_provenance.py`（**9 项**）。

**1. 证据层（可审计的溯源）** `_build/build_evidence.py`
- 对 52 篇理论文本（只读）建立**语料指纹 + 1640 个章节区间 + 17,519 句句索引**（字符偏移）。
- 215 条断言（82 概念 / 63 命题 / 70 论证）逐条定位：`exact` 14 · `name`（概念名锚定）62 · `section` 13 · `doc` 125 · `unresolved` 1。
- 每行带 `char_start/char_end/quote/match_method/confidence/doc_switch`；**机器定位一律 `verified=False`**，人工复核后才可置 True。
- `_build/check_provenance.py`：引文必须**逐字等于**原文区间（实测 214/214 通过），覆盖、边界、枚举、跨文档标记全查。

**2. 主张图（Claim Graph）** `_build/build_claims.py`
- 缺口编号对照（24 缺口 ↔ 权威 C / G2–G22 / N1–N4）+ **id 前缀冲突登记**（G 前缀同时被 G001–G024 缺口与 G025–G032 其他命题占用，如实标记不擅自重编号）。
- 缺口依赖链 `G2→G3→G4→G5` 数据化（原写在 .md 表格与散文中）；命题级边从 **0 条增至 291 条**（提及概念 60 / 依据文档 96 / 证据文档 52 / 证据句提及概念 51 / 同证据句 4 / 语义近邻候选 22 / 提及缺口 2）。
- 概念别名表 35 条（同义词 / 符号 / 论证表变体）；论证词表对齐表 70 条，**暴露 10 条前件数与 ID 数不一致**、后件 19/70 文本与规范名不对齐。

**3. 本体公理层与真实推理** `_build/build_ontology.py`
- 对象属性加 `domain/range` 与 6 组逆属性；12 个概念类型声明互斥；`Hyperedge ⊑ (hasPremise min 1 Concept) ⊓ (hasConclusion min 1 Concept)`。
- **HermiT（owlready2 sync_reasoner，内存推理）一致性检查通过**，无不可满足类；个体 429（含 214 个证据个体，88% 断言带 `derivedFrom` 链路）。
- 建模修正：论证表的「依赖」是概念→概念，与命题表的 `dependsOn` 语义冲突，**由 RDFS 定义域推理暴露**（13 个概念被判成命题），已拆为 `conceptDependsOn` 独立属性。

**4. RDF 导出 · SHACL 数据契约 · SPARQL 能力问答** `_build/build_kg.py`
- `03_超图与理论图/知识图谱.ttl`：**5,567 三元组**，含 SKOS 词表（82 prefLabel + 35 altLabel + definition）、PROV-O 溯源（214 条 `prov:value/atLocation` + `wasDerivedFrom`）、Lean 映射。
- `02_概念本体/shapes.shacl.ttl` + pyshacl：概念/命题/缺口/超边/论证/证据六类形状，**全部通过（0 违约）**。
- 9 条能力问句（CQ1–CQ9）用 SPARQL 1.1 实跑并把结果存档 `03_超图与理论图/SPARQL问答.json`；CQ2 如实报出 **G031（Tate 自对偶）无证据**。

**5. 抽取流水线（可评测）** `_build/build_extract.py`
- 术语发现：n-gram 2–5 + 内部凝固度(PMI≥8) + 左右邻接熵(≥1.0) + 简化 C-value → 1,151 条候选（保留 Top 800）；**候选只进候选池，不写入概念表**。
- 关系抽取：相邻句式 `A⟨模式⟩B` → 135 条候选；以人工论证表为金标准给出 `P=0.08 R=0.14 F1=0.10`，并**量化召回上界 0.50**（金标准两端在原文同句共现的比例）→ 当前达上界 28%。
- 语义特征：概念文档 TF-IDF（语料自训练，无外部模型）1,036 个词项 + 每概念 Top-8 语义近邻。

**6. 检索台** `_build/build_search.py` → `10_展示可视化/检索台/index.html`
- 五种检索：图谱检索（分面 + 别名 + 证据 + 上下游）、**全文 BM25**（CJK 一元+二元切分、引号短语、`+/-` 必含排除、`doc:` 限定；语料 gzip+base64 内嵌，浏览器 `DecompressionStream` 本地解压）、证据检索、质量看板、能力问答。

**7. 展示层**
- 驾驶舱新增「证据」（215 条断言 → 原文定位）与「质量看板」（SHACL / HermiT / 抽取评测 / 主张图构成 / 术语候选）两个面板，共 9 面板。
- 超图新增**多层图谱**开关：命题（39）+ 缺口（24，闭合转绿）+ claim 边，与概念层、超边同图。

**8. 同步范围与验证**
- 脚本：`build_evidence · build_claims · build_ontology（改造） · build_kg · build_extract · build_site（改造） · build_search`；检查：`check_provenance`（新）· `check_consistency`（23 → 41 项）。
- 文档：`00_外部引用/README.md`、`01_结构化数据/README.md`、`_build/README.md`、`10_展示可视化/README.md`、`08/README.md`、`AGENTS.md`（闭环与命令速查）、建设报告、设计方案。
- 呈现边界不变：抽取只做定位与归一，不推断、不补全；候选池≠概念表；数值与缺口状态不由抽取改写。

## v1.6.0 — 展示可视化升级：研究驾驶舱 + 可推演超图（派生级联回放）

- `10_展示可视化/网站/index.html` 由"表格 + 搜索"升级为**暗色研究驾驶舱**：7 面板 + 8 类**内联 SVG 图表**（概念类型环图、关系类型条图、命题类型×状态堆叠条、Lean 声明构成与模块 Top16、派生级联、$G_N$ 对数弹性、概念派生深度分布），并加全局检索（`Ctrl+K`，跨概念/命题/论证跳转定位）。全部图表由页面内联脚本从数据现场绘制，不引入任何图表库或 CDN。
- `10_展示可视化/交互式可视化/超图交互.html`（同步 `03_超图与理论图/超图可视化.html`）升级为**可推演超图**：暗色辉光主题；新增**类型分簇**布局（共 6 种）；hover 邻域高亮、点击邻域聚焦、**有向路径检索**（前件 → 超边 → 后件）、图例按类型过滤、**小地图**、导出 PNG、全屏。
- 新增**派生级联回放**：以 `06_动态机制/仿真/derivation_order.csv`（49 条规则 / 4 轮 / 44 种子）驱动，逐轮点亮概念与触发规则，收束于"累计可达 81/82，不可达 C074"。`build_site.py` 构建期按轨迹复算逐轮新增（+28 / +6 / +2 / +1）并**断言与 `dynamic_hypergraph.json` 的可达数一致**；仅呈现既有数据，不新增理论内容、不改数值与缺口状态。
- 呈现边界写死：弹性图旁标注"构造后验数字校验，待独立复现"；缺口状态原样登记。
- 同步范围：`_build/build_site.py`（渲染与数据聚合）、`03_超图与理论图/README.md`、`10_展示可视化/README.md`、`10_展示可视化/报告/建设报告.md`、`08/README.md`（§四/§六/§九）、`_build/README.md`、`设计方案.md`（维度 7 工具与产出）。
- 验证：内联脚本语法检查 + jsdom DOM 冒烟（图表数、行数、检索、筛选）+ Cytoscape 桩驱动回放/路径用例 + **Edge 无头截图人眼复核**。据真实渲染据实修复两处仅在该环节暴露的问题：Cytoscape 3.34 `boundingBox().x/.y` 为 `NaN` 致小地图全空（改用 `x1/y1`）；KPI 数字 `background-clip:text` 在带 hash 的滚动合成下掉色（改辉光实色）。

## v1.5.0 — 交互式超图改用 Cytoscape.js（离线自包含）

- 交互式超图由手写 Canvas 渲染改用 **Cytoscape.js**：支持力导向 / 同心 / 环形 / 网格 / 层级 5 种布局，缩放平移、关系筛选、概念搜索与邻接面板；超边以哑节点展开（前件虚线入、后件实线出）。
- 随包离线资源 `_build/vendor/cytoscape.min.js`（v3.34.3，MIT），构建时复制到 `10_展示可视化/交互式可视化/assets/` 与 `03_超图与理论图/assets/`；页面仅引用本地 `assets/cytoscape.min.js`，不依赖 CDN。
- 同步范围：`_build/build_site.py`（渲染与库复制）、`03_超图与理论图/README.md`、`10_展示可视化/README.md`、本目录 `README.md`（图模型与工具栈）、`设计方案.md`（工具清单）。

## v1.4.0 — 离线阅读站（维度 7 阅读层）

- 新增 `_build/build_reader.py` 与 `10_展示可视化/阅读站/`：由 `README.md` + `01`–`07` 各主题文档 + `一体化研究/附录` **只读**派生的单页离线阅读站（目录树 / 全文搜索 / 站内跳转 / 反链 / MathJax 公式渲染；语料内嵌，`file://` 可直接打开）。
- 该产物不进入源 CSV 闭环：它由理论文本派生，不修改任何理论文本，也不新增理论内容。
- 随包离线资源 `阅读站/assets/marked.min.js`（MIT）、`阅读站/assets/tex-svg.js`（MathJax，Apache-2.0），站点不依赖 CDN。
- 同步登记：`10_展示可视化/README.md`、`_build/README.md`、本目录 `AGENTS.md`（§三 维度 7 产物、§九 命令速查）。

## v1.3.0 — 七维度口径恢复：展示可视化从出口层提升为核心维度 7

- 维度口径由六恢复为七：展示可视化从「出口层」提升为**第 7 维度（核心）**；七维度 = 4 核心（结构化 / ML 数据准备 / 形式化验证 / 展示可视化）+ 3 辅助（动态机制 / 经验检验 / 元理论反思）。
- 概念本体（`02`）、桥接与翻译（`09`）、元数据（`11`）明确为支撑层，不计入七维度。
- 同步范围：组织层 `AGENTS.md` / `README.md` / `设计方案.md` / `10_展示可视化/README.md` / `10_展示可视化/论文草稿/形式化组织框架.md` / `_build/build_site.py`（注释）。

## v1.2.0 — 六维度口径：人本理解降为出口层「输出可视化展示」

- 维度口径由七改六：移除「人本理解」维度；余六维为 结构化 / ML 数据准备 / 形式化验证 / 动态机制 / 经验检验 / 元理论反思。
- 原「人本理解」降为**出口层**，定名「输出可视化展示」（只呈现、不含新理论内容，面向人使用）；目录相应改名为 `10_输出可视化展示`。
- 同步范围：组织层 `README.md` / `AGENTS.md` / `设计方案.md` / 建设报告 / 论文草稿；根 `README.md` / `AGENTS.md`；`_build/build_site.py`（维度表）、`_build/check_consistency.py`（维度覆盖键 `人本`→`输出`）。

## v1.1.0 — 七维度运行规范与一致性硬检查

- 新增目录级 `AGENTS.md`：七维度责任矩阵、**研究闭环（Definition of Done）**、一致性红线、反模式、完成判据与命令速查；把"每次研究须覆盖七维度"固化为可执行条款。
- 新增 `_build/check_consistency.py`：跨产物硬检查（23 项），核对计数一致性（源 CSV ↔ 超图 JSON ↔ 本体 ↔ ML ↔ 前端 ↔ 动态 ↔ Lean）、引用完整性、`⇒`/`→` 约定、维度目录覆盖、Markdown 失效链接与禁用词；退出码非 0 即视为研究未完成。
- 根 `AGENTS.md` 目录约定表新增 `08 理论组织和形式化框架/` 行，并在"验证命令"节加入组织层一致性检查的调用。

## v1.0.0 — 七维度框架全面建成

**结构化层（既有）**
- `00_外部引用`：引用清单（52 篇）、锚点映射。
- `01_结构化数据`：概念表（82）、命题表（63）、论证表（70）、缺口依赖闭包。
- `03_超图与理论图`：超图数据、Graphviz/SVG/PNG、理论依赖图。

**本次新增**
- `02_概念本体`：本体.owl（24 类/215 个体/7 对象属性）、本体文档、概念关系图。
- `04_Lean对接`：lean代码路径.yaml、Lean 结构提取（68 模块/1388 声明）、Lean↔概念映射（25 条）、蓝图网页。
- `05_机器学习数据准备`：超图导出（PyG/DGL 就绪）、证明数据集（3 个 JSONL）、嵌入就绪。
- `06_动态机制`：重写规则（61）、理论状态模型、派生仿真（可达 81/82）。
- `07_经验检验`：$G_N$ 因果模型、缺口贝叶斯网络、实验设计（6 项）。
- `08_元理论反思`：范畴论模型、类型论基础、哲学假设。
- `09_桥接与翻译`：符号对照表、文档间等价映射、概念↔Lean↔物理映射、翻译规则。
- `10_人可读输出`：自包含 HTML 网站、交互式超图（并同步至 `03`）、蓝图网页、讲解文档（4 篇）、建设报告、论文草稿。
- `11_元数据`：本目录（清单/版本/变更日志/验证状态）。

**基座修复**
- 修复源 CSV 6 行未转义逗号（概念表 C004/C020/C062，论证表 H003/A004/A020）导致的字段错位；
- 以标准 CSV 解析重建 `03_超图与理论图/超图数据.json`；超边计数校正为 **19 超边 ⇒ / 51 有向边 →**。
""")


def write_validation():
    with open(os.path.join(S11, "验证状态.md"), "w", encoding="utf-8") as f:
        f.write("""# 元数据 · 验证状态

> 汇总 `08` 目录各产物的**验证证据**与**未验证边界**。缺口语义、数值限定语保持原样。

## 一、已核验项

| 产物 | 核验方式 | 结果 |
|:---|:---|:---|
| **组织层一致性（41 项）** | `_build/check_consistency.py`（计数/引用/约定/覆盖/链接/禁用词 + 证据层/主张层/图谱/SHACL/HermiT/抽取） | ✅ 全部通过（退出码 0） |
| **证据层完整性（10 项 / 有复核结果 13 项）** | `_build/check_provenance.py`（覆盖 215、引文逐字一致、区间边界、枚举、跨文档标记 + 复核闭环三条） | ✅ 全部通过（退出码 0） |
| **证据复核闭环自测** | 临时 3 条合法记录 → 13/13；伪造 id（ZZ99）→ 被拒收；移除自测文件复跑 → 10/10 | ✅ 通过（仓库内无 `复核结果.csv`，verified 现为 0） |
| SHACL 数据契约 | `_build/build_kg.py` + pyshacl（6 类形状） | ✅ conforms，0 违约 |
| OWL 一致性 | owlready2 + HermiT（内存推理） | ✅ 一致，无不可满足类（25 类 / 430 个体 / 16 对象属性） |
| SPARQL 能力问句 | rdflib（CQ1–CQ9 实跑） | ✅ 9/9 返回；CQ2 如实报出 1 条无证据断言 |
| 关系抽取评测（分层） | 人工论证表为金标准 | ⚠️ pattern 层 P=0.069 / 类型命中 0.111；cooccur 层无向 R=0.474 / 物理上界 0.50 = **达上界 95%**——「未定」类型不入库，交人工/LLM 定型 |
| 概念表/命题表/论证表 | 字段数断言（7/6/6）+ 概念引用完整性断言 | ✅ 82/63/70，无错位 |
| 超图数据.json | 由标准 CSV 解析重建；计数断言 | ✅ 82 节点 / 19 超边 / 51 有向边 |
| 本体.owl | owlready2 生成并回读 + HermiT 推理 | ✅ 25 类 / 430 个体 / 16 对象属性（公理层含 domain·range·逆属性·互斥·限制） |
| Lean 结构提取 | 源码扫描（68 模块） | ✅ 1388 声明；状态以 `08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md` 为权威 |
| ML 张量 | `x` 形状 (82,15)；索引与 CSV 一致 | ✅ |
| 动态仿真 | `simulate.py` 复算轨迹与 `derivation_trace.csv` 比对 | ✅ 一致 |
| 派生级联数据 | `build_site.py` 按 `derivation_order.csv` 复算逐轮新增，断言累计可达 = `dynamic_hypergraph.json` 的 81 | ✅ 一致（+28 / +6 / +2 / +1） |
| HTML 内联数据 | `const D/PAY` JSON 合法性校验 | ✅ |
| HTML 内联脚本 | 语法检查（`new Function`）+ jsdom DOM 冒烟（9 面板 / 图表 / 行数 / 检索 / 分面 / 级联 / 质量看板） | ✅ 通过 |
| 检索台 | gzip 语料 Node 侧解压校验 + jsdom 六模式冒烟（图谱/全文降级/证据/复核/质量/CQ） | ✅ 通过 |
| 超图交互逻辑 | Cytoscape 桩驱动：级联回放 4 轮 → 81/82 + C074 标注；有向路径；**多层图谱端点过滤**（claim 边不得指向不存在的节点） | ✅ 通过 |
| **研究站（VitePress v1.6.4，v1.9.2）** | 页头 `generator = VitePress v1.6.4`；构建期 50 页整页 `v-pre`、无 Vue 插值报错；增强三件套 `node --check` 通过（`cqm-glossary.js` / `cqm-enhance-vp.js` / `cqm-depth.js`）；术语卡 138 张（含出处/字符区间/置信度）、检索索引 341 条、termKeys 106、展开链步 131 条、缺口断点清单 24 项 | ✅ 通过 |
| **研究站端到端（服务在场）** | `.workbuddy/tools/verify_station.py` **29/29**：静态站 4（首页/内页/资产/内嵌 viz）+ 响应头 charset 2 + `/api/status` 9 + 检索 2 + SPARQL 3（含写操作 403）+ 条目 4 + 复核写回 5（测试后清理、仓库恢复干净） | ✅ 通过 |
| **公式排版（v1.9.3）** | Edge 无头实测：`$` 内标签注入 **0**；大块公式渲染为 `<menclose notation="box"><mtable>…<mtext>`（`\boxed` / `aligned` / `\text{中文}` 全部正确）；占位符产物残留 **0**；文本节点残留 `$…$` 仅 4 处，全在标题锚点 `aria-label` 与内嵌 JSON（不可见） | ✅ 通过 |
| **可视化页渲染（v1.9.3）** | Edge 无头逐页截图复核：V001 超图（Cytoscape 节点/边/图例/小地图）、V002 驾驶舱（9 面板）、V003 检索台（实体/证据卡）、V004 蓝图（KPI/色带/axiom 清单，`<code>` 文字可读）四页均正常；`assets/cytoscape.min.js` 404 已改指同级文件 | ✅ 通过 |
| **编码（v1.9.3）** | 响应头 `Content-Type: text/html;charset=UTF-8` / `text/javascript;charset=UTF-8`（`server.servlet.encoding.force`）；产物侧 178 个 HTML/JS/JSON/CSS 扫描：U+FFFD 0、不可解码 0 | ✅ 通过 |
| **站内链接（v1.9.4）** | `.workbuddy/tools/link_audit.py` 遍历 52 页的 **119** 条站内 `href/src` 逐个请求：**失效 0**（此前 7 条指向 `/_src/…html` 的链接全 404） | ✅ 通过 |
| **markdown 语法（v1.9.4）** | `.workbuddy/tools/render_audit.py`：加粗字面 **0**（此前 6 113）、行内代码 0、链接字面 0、删除线 0、高亮 0、标题 0、表格 0、引用 0、列表 0；页面 `<strong>` 773 处；`U(1)_B、…、U(1)_Y` 不再被配成斜体 | ✅ 通过 |
| **内置搜索（v1.9.4）** | 导航栏出现「搜索」按钮与 `Ctrl K` 提示（`DocSearch-Button`）；构建期索引 `assets/chunks/@localSearchIndexroot.*.js`（4.7 MB）；自定义中文分词，索引内含「退相 / 相变 / 前时空 / 自守 / qubit / GL(5)」token | ✅ 通过 |
| **术语悬浮卡渲染（v1.9.5）** | 对照实验页（直接注入卡片 HTML）：四套分隔符混排后渲染结果里反斜杠括号残留 **0**、`mjx-container` 正常生成；卡片里的 Lean 模块名由字面反引号落成 `<code>` | ✅ 通过 |
| **阅读体验增强（v1.9.5）** | `public/vp-read.css` 随站注入；页顶进度条 `cqm-progress`、回到顶部 `cqm-top` 均已挂载；表格改 `width: max-content` 后中文列不再逐字竖排（实测截图复核）；`mjx-container` 限宽可横向滚动；锚点 `scroll-margin-top` 84px + `:target` 高亮；外链自动 `target=_blank` | ✅ 通过 |
| **可视化页公式（v1.9.6）** | `public/viz/*.html` 注入本地 MathJax + DOM 变化节流重排；CDP 实测：检索台 `rawDollar 111 → 0`（`mjx 139`）、驾驶舱 `mjx 156` 残留 0、超图/蓝图无公式无残留 | ✅ 通过 |
| **缓存治理（v1.9.6）** | 服务端静态资源 `Cache-Control: no-store`（协商缓存）；构建期 head 无哈希资源挂 `?v=构建时间戳`；CDP 全站 10 个代表页「搜索 + 高级检索」双入口在线、零残留 | ✅ 通过 |
| **真实交互探测（v1.9.6）** | `.workbuddy/tools/browser_probe.py` / `page_probe.py`：CDP 驱动 Edge 无头，真实点击搜索（输入「退相干」→ 59 条结果）、真实悬停术语卡（138 张全量注入排版 `badN=0`）、真实收集控制台异常与失败请求 | ✅ 通过 |
| **研究站离线边界** | VitePress 本地检索依赖 `fetch` 取 JSON 分片、`base:'/'` 用绝对路径 → **`file://` 直开丢资源**；须经 HTTP 提供（服务在场 `http://127.0.0.1:8080/`）。完全离线场合改用 `源_可视化/` 自包含 HTML | ⚠️ 已知取舍，非缺陷 |
| **阅读站增强口径** | 卡片与展开链文字**逐字**取自 `概念表.csv` / `缺口编号对照.csv` / `符号对照表.csv` / `证据映射.csv`；构建脚本只拼装、不改写；缺口状态与限定语原样；术语标注限流（每术语每页 ≤3、全页 ≤240） | ✅ 一致 |
| **展开链讲稿（撰述稿）** | `10_展示可视化/讲稿/第一分册_从问题到链条.md`（308 行）：问题 → 最小内核 → 六步链条 → 量纲链 → 断点 → 数值地位；每节论断带锚点（20 条，其中 18 条逐字核对、2 条标「待逐字核对」）；断点就地标注（C／G2–G8／G9–G22／N1–N4／H3.1–H3.3 引自缺口台账）；数值分列「推导／构造后验／实验参数」并保留限定语；附录含「引文保真六关」自检。**讲稿为撰写文字，不入引用清单、不计入理论语料统计** | ✅ 已接入阅读站（`L001` 页，导航紧随展开链） |
| **深度滑杆** | 讲稿页四档分层（导读/概念/链条/技术）；离线按块模拟（`.workbuddy/tools/depth_sim_vp.py`，与增强脚本 `contentRoot()` 同规则下潜）：L001 显示 32 → 64 → 102 → 107 块、L002 显示 27 → 38 → 84 → 86 块（均单调），断点块 0 个被隐藏，章节映射覆盖 11/11；`node --check` 通过 | ✅ 通过 |
| **可视化单一入口** | 四件自包含 HTML 收进研究站「可视化」栏目（`V000–V004`，VitePress 站内路径 `/viz/`）；内嵌资源 6 个（含 `cytoscape.min.js`、`驾驶舱数据.json`）；相对引用与跨链已改写，驾驶舱跨页链接指向研究站首页，无 `../` 越界引用、无死链指向已移除目录；源文件未改动 | ✅ 通过 |
| OWL/CSV/JSON/HTML | 编码 UTF-8、路径存在 | ✅ |

## 二、未安装依赖（脚本就绪，未执行）

| 依赖 | 用途 | 目录 |
|:---|:---|:---|
| torch / PyG / DGL | 装配 `.pt` / DGL 图对象 | `05_机器学习数据准备/超图导出/build_pyg.py` |
| dowhy | 因果识别与反驳 | `07_经验检验/因果模型/dowhy_model.py` |
| pgmpy | 贝叶斯网络推断 | `07_经验检验/贝叶斯网络/infer.py` |
| leanblueprint + plasTeX | 官方蓝图网页 | `10_展示可视化/蓝图/leanblueprint_source.md` |
| Catlab (Julia) | 范畴论计算 | `08_元理论反思/范畴论模型/catlab_sketch.jl` |
| LLM API（OpenAI 兼容） | 关系定型（schema 固定 + span 校验，产出候选） | `_build/llm_extract.py`（`CQM_LLM_API_BASE/KEY/MODEL`；无密钥时打印就绪说明退出 0）。**2026-10-12 裁定：本地生成模型不采用为任何环节的生成源**（0.6B/1.7B 级模型自述"CQM 文档风格的生成/检索器，不是数学推理引擎"），该脚本保持就绪但**不接线**；相应环节改为「规则/统计提案 + 机械 span 校验 + 人工确认」三关制 |

> 以上以"就绪脚本 + 说明"给出，未执行部分**不谎报**为已完成。

## 三、诚实边界

1. **形式化覆盖 49.4%**（40/81 概念）——未覆盖概念不得视为已形式化。
2. **缺口状态未改动**：C、G2–G8、G9–G22、N1–N4、H3.1–H3.3 保持权威源状态。
3. **贝叶斯 CPT 为占位**（待标定），其输出不构成理论结论。
4. **$G_N$、$\\alpha$ 类数值**一律带"构造后验数字校验，待独立复现"。
5. **前向派生不可达 1 概念**（C074）如实登记。
6. **抽取候选不入表**：术语候选 / cooccur 关系候选 / LLM 定型候选一律只进候选池；`verified` 仅人工复核可置真（无复核文件时硬断言全为 False）。
""")


if __name__ == "__main__":
    main()
