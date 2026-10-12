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

1. **形式化覆盖 50%**（41/82 概念）——未覆盖概念不得视为已形式化。
2. **缺口状态未改动**：C、G2–G8、G9–G22、N1–N4、H3.1–H3.3 保持权威源状态。
3. **贝叶斯 CPT 为占位**（待标定），其输出不构成理论结论。
4. **$G_N$、$\\alpha$ 类数值**一律带"构造后验数字校验，待独立复现"。
5. **前向派生不可达 1 概念**（C074）如实登记。
6. **抽取候选不入表**：术语候选 / cooccur 关系候选 / LLM 定型候选一律只进候选池；`verified` 仅人工复核可置真（无复核文件时硬断言全为 False）。
""")


if __name__ == "__main__":
    main()
