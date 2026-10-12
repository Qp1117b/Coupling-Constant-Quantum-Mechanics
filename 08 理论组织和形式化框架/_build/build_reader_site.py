# -*- coding: utf-8 -*-
"""
维度7（核心） · 展示可视化 · 离线阅读站（Material for MkDocs 版，v1.8.0）

替代旧的自研单页阅读站（`build_reader.py`，其全文搜索仅为字符串 indexOf）。
采用专业文档栈 **Material for MkDocs**：

  · 搜索 = lunr.js + 官方 `zh` 支持 + **jieba 中文分词**（构建期）
    —— 另生成 **CQM 用户词典**（概念名/同义词/符号名/缺口编号）实现术语级检索
  · **offline 插件**：官方保证「分发 site 目录即用、搜索在离线环境工作」→ file:// 双击可用
  · **privacy 插件**：构建期把外部字体等资源下载本地，成品无 CDN（离线红线）
  · `use_directory_urls: false`：file:// 下直出平铺 .html（目录式 URL 在 file:// 只会显示列表）
  · 数学 = pymdownx.arithmatex + 随包 `tex-svg.js`（复用旧阅读站资产，MathJax 本地化）

语料口径与 `build_reader.py` 完全一致（根 README + 01–07 + 一体化研究/附录，全部**只读**）：
  · staging 复制到 `_build/mkdocs_src/docs/`（在 _build 内 → 不计产品文件、不进 md 扫描）
  · 跨文档 .md 链接改写为 staged 文件名；被引用的图片/附件复制到 `docs/_src/`
  · 01–07 理论文本永不修改

产出：
  _build/mkdocs.yml、_build/mkdocs_src/…（中间物）
  10_展示可视化/阅读站/            （mkdocs build 输出，整站）
运行：python build_reader_site.py
"""
import glob
import io
import json
import os
import re
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT08 = os.path.dirname(HERE)
ROOT = os.path.dirname(ROOT08)
SITE = os.path.join(ROOT08, "10_展示可视化", "阅读站")
STAGE = os.path.join(HERE, "mkdocs_src")
DOCS = os.path.join(STAGE, "docs")
CONF = os.path.join(HERE, "mkdocs.yml")
REF_YAML = os.path.join(ROOT08, "00_外部引用", "引用清单.yaml")
TEX_SVG = os.path.join(ROOT08, "10_展示可视化", "阅读站", "assets", "tex-svg.js")

INCLUDE_DIRS = [
    "01 核心理论", "02 量子引力", "03 引力与退相干", "04 前沿研究",
    "05 方法论与批判", "06 超导", "07 精细引力（FG）",
                 "08 理论组织和形式化框架/附录",
]
DOC_RE = re.compile(
    r"-\s*\{id:\s*(D\d+),\s*path:\s*([^,]+),\s*title:\s*([^,]+),\s*layer:\s*(\d+),\s*type:\s*([^}]+)\}")
LAYER_NAME = {0: "权威基准", 1: "理论主干", 2: "专题深化", 3: "涌现与应用", 4: "形式化与方案"}
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")


def read(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def registry():
    reg = {}
    for m in DOC_RE.finditer(read(REF_YAML)):
        reg[m.group(2).strip().replace("\\", "/")] = {
            "id": m.group(1), "title": m.group(3).strip(),
            "layer": int(m.group(4)), "type": m.group(5).strip()}
    return reg


def collect():
    paths = []
    rp = os.path.join(ROOT, "README.md")
    if os.path.isfile(rp):
        paths.append("README.md")
    for d in INCLUDE_DIRS:
        for p in sorted(glob.glob(os.path.join(ROOT, d, "**", "*.md"), recursive=True)):
            paths.append(os.path.relpath(p, ROOT).replace("\\", "/"))
    return paths


def safe_name(staged):
    base = os.path.basename(staged)
    if base.endswith(".md"):
        base = base[:-3]
    return re.sub(r"[^\w\-]+", "_", base).strip("_") + ".md"


def build_user_dict():
    """jieba 用户词典：概念名/同义词/符号名与符号/缺口编号（术语级检索）。"""
    import csv as _csv
    terms = {}
    def add(t, w=100, pos="nz"):
        t = (t or "").strip()
        if len(t) >= 2:
            terms.setdefault(t, (w, pos))
    cpath = os.path.join(ROOT08, "01_结构化数据", "概念表.csv")
    with io.open(cpath, encoding="utf-8-sig", newline="") as f:
        for r in _csv.DictReader(f):
            add(r["name"], 200)
            for s in (r.get("synonyms") or "").split(","):
                add(s, 150)
    spath = os.path.join(ROOT08, "09_桥接与翻译", "符号对照表.csv")
    if os.path.isfile(spath):
        with io.open(spath, encoding="utf-8-sig", newline="") as f:
            for r in _csv.DictReader(f):
                add(r.get("name"), 150)
                add(r.get("symbol"), 80)
    for n in list(range(1, 23)):
        add(f"G{n}", 60); add(f"N{n}", 60)
    add("缺口"); add("相变量子"); add("量纲发生学"); add("同步算符")
    out = os.path.join(HERE, "cqm_user_dict.txt")
    with io.open(out, "w", encoding="utf-8", newline="\n") as f:
        for t, (w, pos) in sorted(terms.items()):
            f.write(f"{t} {w} {pos}\n")
    return out, len(terms)


def stage_docs(reg):
    if os.path.exists(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(os.path.join(DOCS, "_src"), exist_ok=True)
    corpus = collect()
    staged_map, unreg = {}, 0
    plan = []
    for rel in corpus:
        src = os.path.join(ROOT, rel)
        meta = reg.get(rel)
        if meta:
            sid, title, layer = meta["id"], meta["title"], meta["layer"]
        else:
            unreg += 1
            sid, title, layer = f"F{unreg:02d}", os.path.basename(rel)[:-3], 9
        name = safe_name(f"{sid}_{title}")
        plan.append((rel, src, sid, name, title, layer))
        staged_map[rel] = (sid, name, title, layer)
    # index.md ← 根 README（站首页）
    root_src = os.path.join(ROOT, "README.md")
    index_content = read(root_src) if os.path.isfile(root_src) else "# CQM 理论\n"
    # 链接改写（先全量映射表，再逐篇改写）
    def resolve(target, src_dir):
        t = target.split("#", 1)[0].split("?", 1)[0]
        if not t or t.startswith(("http://", "https://", "mailto:", "tel:")):
            return None, target
        p = os.path.normpath(os.path.join(src_dir, t.replace("/", os.sep)))
        if os.path.isfile(p):
            return os.path.relpath(p, ROOT).replace("\\", "/"), target
        return None, target

    def rewrite(text, src_path, cur_out):
        """改写链接；href 相对**当前文件的输出位置**计算（支持 docs 根与 docs/_src 深层）。"""
        src_dir = os.path.dirname(src_path)
        cur_dir = os.path.dirname(cur_out) or "."
        def href_for(out_path):
            return os.path.relpath(out_path, cur_dir).replace("\\", "/").replace(" ", "%20")
        def repl(m):
            bang, label, target = m.group(1), m.group(2), m.group(3).strip()
            # 剥离可选的 "标题" 尾注（允许目标含空格，如 "01 核心理论/xxx.md"）
            tm = re.search(r'\s+"[^"]*"$', target)
            if tm:
                target = target[:tm.start()]
            anchor = ""
            if "#" in target:
                target, anc = target.split("#", 1)
                anchor = "#" + anc
            target = target.replace("%20", " ").strip()
            if target.startswith(("http://", "https://", "mailto:", "tel:")):
                return m.group(0)
            # 目录链接（如 "08 理论组织和形式化框架/04_Lean对接/Lean源码/"）站内无对应页 → 降级为纯文本
            if target.rstrip().endswith(("/", "\\")):
                return label
            rel, _ = resolve(target, src_dir)
            if rel is None:
                return m.group(0)
            if os.path.isdir(os.path.join(ROOT, rel)):
                return label
            if rel in staged_map:
                return f"{bang}[{label}]({href_for(staged_map[rel][1])}{anchor})"
            # 非语料文件：复制进 docs/_src（md 内容按其输出位置同步改写）并改写引用
            src_abs = os.path.join(ROOT, rel)
            dst_rel = "_src/" + rel.replace("\\", "/")
            dst_abs = os.path.join(DOCS, dst_rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(dst_abs), exist_ok=True)
            if not os.path.exists(dst_abs):
                if src_abs.lower().endswith(".md"):
                    with io.open(dst_abs, "w", encoding="utf-8", newline="\n") as f:
                        f.write(rewrite(read(src_abs), src_abs, dst_rel))
                else:
                    shutil.copyfile(src_abs, dst_abs)
            return f"{bang}[{label}]({href_for(dst_rel)}{anchor})"
        return LINK_RE.sub(repl, text)

    for rel, src, sid, name, title, layer in plan:
        text = rewrite(read(src), src, name)
        with io.open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    index_content = rewrite(index_content, root_src, "index.md")
    with io.open(os.path.join(DOCS, "index.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(index_content)
    # assets：MathJax 本地化
    adir = os.path.join(DOCS, "assets")
    os.makedirs(adir, exist_ok=True)
    os.makedirs(os.path.join(adir, "stylesheets"), exist_ok=True)
    if os.path.isfile(TEX_SVG):
        shutil.copyfile(TEX_SVG, os.path.join(adir, "tex-svg.js"))
    with io.open(os.path.join(adir, "math-config.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(
            "window.MathJax = {\n"
            "  tex: { inlineMath: [['\\\\(','\\\\)']], displayMath: [['\\\\[','\\\\]']], processEscapes: true },\n"
            "  svg: { fontCache: 'global' },\n"
            "  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }\n"
            "};\n")
    return staged_map, unreg


def write_support_assets(staged_map):
    """生成反链数据/注入脚本/品牌样式（阅读站"好用/好看"三件套）。"""
    # ---- 反链：扫描 staged 文档中的站内链接，倒排 ----
    name2info = {name: (sid, title) for rel, (sid, name, title, layer) in staged_map.items()}
    back = {}
    link_re = re.compile(r"\]\((?:\./)?(D\d+_[^)]+?\.md|F\d+_[^)]+?\.md)\)")
    for fn in os.listdir(DOCS):
        if not fn.endswith(".md"):
            continue
        txt = io.open(os.path.join(DOCS, fn), encoding="utf-8").read()
        src = name2info.get(fn, ("", fn[:-3]))
        for m in link_re.finditer(txt):
            tgt = m.group(1)
            if tgt == fn:
                continue
            lst = back.setdefault(tgt[:-3] + ".html", [])
            if (src[1], src[0]) not in [(x["title"], x["sid"]) for x in lst]:
                lst.append({"title": src[1], "sid": src[0], "file": fn[:-3] + ".html"})
    adir = os.path.join(DOCS, "assets")
    os.makedirs(adir, exist_ok=True)
    with io.open(os.path.join(adir, "backlinks.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.__CQM_BACKLINKS=" + json.dumps(back, ensure_ascii=False) + ";\n")
    # ---- 注入脚本：页尾「被引用」区块 ----
    with io.open(os.path.join(adir, "backlink-inject.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(r"""(function () {
  function curFile() {
    try { return decodeURIComponent(location.pathname.split("/").pop()); }
    catch (e) { return location.pathname.split("/").pop(); }
  }
  function go() {
    var data = window.__CQM_BACKLINKS, file = curFile();
    if (!data || !data[file]) return;
    var art = document.querySelector("article");
    if (!art) { setTimeout(go, 200); return; }
    if (art.querySelector(".cqm-backlinks")) return;
    var box = document.createElement("section");
    box.className = "cqm-backlinks md-typeset";
    var h = document.createElement("h2");
    h.textContent = "被引用（" + data[file].length + "）";
    box.appendChild(h);
    var ul = document.createElement("ul");
    data[file].forEach(function (it) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "./" + it.file;
      a.textContent = it.title + (it.sid ? " [" + it.sid + "]" : "");
      li.appendChild(a);
      ul.appendChild(li);
    });
    box.appendChild(ul);
    art.appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go);
  else go();
})();
""")
    # ---- 品牌样式：项目深蓝渐变 + CJK 排版 + 反链卡片 ----
    with io.open(os.path.join(adir, "stylesheets", "extra.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write("""/* CQM 阅读站定制（构建期生成）：品牌色 + CJK 排版 + 反链卡片 */
:root {
  --cqm-blue: #2f6fb5;
  --cqm-deep: #22456b;
  --cqm-cyan: #38bdf8;
  --cqm-violet: #a78bfa;
}
/* 头部品牌渐变（覆盖 primary 纯色） */
.md-header {
  background: linear-gradient(120deg, var(--cqm-deep), var(--cqm-blue) 70%, #3578c4);
  box-shadow: 0 2px 14px rgba(34, 69, 107, .35);
}
.md-header__button.md-logo { opacity: .95; }
.md-typeset h1 { letter-spacing: .01em; }
.md-typeset h2 { border-bottom: 1px solid rgba(47, 111, 181, .18); padding-bottom: .2em; }
.md-typeset h2::before,
.md-typeset h3::before {
  content: ""; display: inline-block; width: 3px; height: .95em;
  margin-right: .5em; vertical-align: -.12em; border-radius: 2px;
  background: linear-gradient(180deg, var(--cqm-blue), var(--cqm-violet));
}
/* CJK 排版：行宽/行高/段距 */
.md-typeset { font-size: 15.5px; line-height: 1.95; letter-spacing: .01em; }
.md-typeset p { margin: .85em 0; text-align: justify; }
.md-typeset table { font-size: .82em; }
.md-typeset table th { background: rgba(47, 111, 181, .08); }
.md-typeset table tr:hover td { background: rgba(47, 111, 181, .05); }
.md-typeset code {
  font-family: Consolas, "Cascadia Mono", "Microsoft YaHei", monospace;
  font-size: .86em; background: rgba(47, 111, 181, .08); color: #1c3d5e;
  border-radius: 4px; padding: .1em .35em;
}
[data-md-color-scheme="slate"] .md-typeset code { color: #bcd6f0; background: rgba(120, 170, 230, .13); }
.md-typeset pre { border-radius: 10px; }
.md-typeset blockquote {
  border-left: 3px solid var(--cqm-cyan);
  background: rgba(56, 197, 248, .06); border-radius: 0 8px 8px 0; padding: .5em .9em;
}
.md-typeset blockquote p { text-align: left; }  /* 含行内公式时 justify 会拉开字距 */
.md-typeset .admonition, .md-typeset details { border-radius: 10px; }
/* 目录栏强调 */
.md-nav__title { font-weight: 600; }
.md-sidebar--primary .md-nav__item--active > .md-nav__link { font-weight: 600; }
/* 反链卡片 */
.cqm-backlinks {
  margin-top: 2.2em; padding: 1em 1.3em; border-radius: 12px;
  border: 1px solid rgba(47, 111, 181, .25);
  background: linear-gradient(135deg, rgba(47, 111, 181, .07), rgba(167, 139, 250, .06));
}
.cqm-backlinks h2 { font-size: 1.05em; margin: 0 0 .5em; border: 0 !important; }
.cqm-backlinks h2::before { display: none; }
.cqm-backlinks ul { margin: 0; padding-left: 1.2em; }
.cqm-backlinks li { margin: .25em 0; }
/* 公式容器不被裁切 */
mjx-container { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
mjx-container[display="true"] { margin: .9em 0; }
/* 滚动条（WebKit/Blink） */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-thumb { background: rgba(47, 111, 181, .45); border-radius: 6px; }
::-webkit-scrollbar-track { background: transparent; }
""")


# ==================== 阅读站增强：术语悬浮 · 缺口徽章 · 高级搜索 · 展开链 ====================
# 数据全部来自既有产物（概念表 / 概念别名表 / 缺口编号对照 / 命题表 / 符号对照表 / 证据映射），
# 卡片里的定义与引文一律**逐字**取自这些表，不在本脚本里改写任何表述。

D00 = os.path.join(ROOT08, "00_外部引用")
D01 = os.path.join(ROOT08, "01_结构化数据")
D09 = os.path.join(ROOT08, "09_桥接与翻译")
CHAIN_PAGE = "L000_展开链.md"
LECT_DIR = os.path.join(ROOT08, "10_展示可视化", "讲稿")
# 可视化整合：把原本分散的四个自包含 HTML 收进阅读站（assets/viz/ 下，iframe 内嵌）。
# 每项 = (源相对 10_展示可视化 的路径, 落地文件名, 需一并复制的伴随文件, 栏目标题, 一句话说明)
VIZ_SOURCES = [
    ("源_可视化/超图交互.html", "viz_超图交互.html", ("cytoscape.min.js", "cytoscape.min.js"),
     "可推演超图", "Cytoscape.js 多层超图：6 种布局、邻域聚焦、有向路径、派生级联回放、命题/缺口层开关"),
    ("源_可视化/研究驾驶舱/index.html", "viz_研究驾驶舱.html", ("data.json", "驾驶舱数据.json"),
     "研究驾驶舱", "9 面板 + 内联 SVG 图表 + 全局检索 + 证据面板（215 条断言）+ 质量看板"),
    ("源_可视化/检索台/index.html", "viz_检索台.html", None,
     "检索台", "图谱检索（分面/别名/证据/上下游）+ 全文 BM25 + 证据复核 + 质量看板 + SPARQL 能力问答"),
    ("../04_Lean对接/蓝图/index.html", "viz_蓝图.html", None,
     "形式化蓝图", "Lean ↔ 概念 ↔ 缺口交互蓝图（映射覆盖环、声明构成、axiom 待证清单）"),
]
VIZ_LINK_FIX = [
    ('href="../交互式可视化/超图交互.html"', 'href="V001_可推演超图.html"'),
    ('href="../检索台/index.html"', 'href="V003_检索台.html"'),
    ('href="../蓝图/index.html"', 'href="V004_形式化蓝图.html"'),
    ('href="../阅读站/index.html"', 'href="index.html"'),
]
# 讲稿的深度分层（构建期配置，运行期由 cqm-enhance.js 按二级标题打标）：
# 1 导读 / 2 概念 / 3 链条 / 4 技术；键为二级标题前缀，未命中的章节取默认 3。
LECT_DEPTH_DEFAULT = 3
LECT_DEPTH_MAP = {
    "卷首": 1,
    "第一章": 1,
    "第二章": 2,
    "第三章": 3,
    "第四章": 3,
    "第五章": 3,
    "第六章": 3,
    "第七章": 3,
    "附录 A": 4,
    "附录 B": 4,
    "附录 C": 2,
}
LECT_DEPTH_LEVELS = {"1": "导读", "2": "概念", "3": "链条", "4": "技术"}
# 命中这些词的块**不随深度隐藏**（断点与限定语必须在任何深度可见）。
# 只认「缺口状态」与「限定语」两类，不用泛词（"缺口""不得"满篇都是，会把滑杆废掉）。
LECT_DEPTH_FORCE = ["未闭合", "待证明", "axiom", "构造后验", "待独立复现", "有待确定"]
LECT_DEPTH_FORCE_RE = r"缺口\s*[CGN]|[CG]\d{1,2}\b|N[1-4]\b|H3\.\d"
ARROW_RE = re.compile(r"[→⇒]")
CHAIN_MIN_ARROWS, CHAIN_MAX_SPAN = 3, 240
CHAIN_SOURCES = ["README.md", "01 核心理论", "02 量子引力", "03 引力与退相干",
                 "04 前沿研究", "05 方法论与批判", "06 超导", "07 精细引力（FG）"]
STATE_WORDS = ["已证", "未闭合", "待证明", "假设", "构造", "axiom", "猜想", "占位", "闭合"]
GAP_RE = re.compile(r"\bG(\d{1,2})\b|缺口\s*([CN])\b|\bC\d{3}\b|\bN[1-4]\b")


def _csv(path):
    import csv as _c
    if not os.path.isfile(path):
        return []
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        return list(_c.DictReader(f))


def _esc(s):
    return (str(s or "").replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def _mathify(s):
    """卡片里的 $...$ / $$...$$ 转成 MathJax 认识的分隔符（页面正文由 arithmatex 处理，
    但卡片是运行期动态插入的，MathJax 不再扫描，故在构建期转换）。"""
    s = re.sub(r"\$\$(.+?)\$\$", r"\\[\1\\]", str(s or ""))
    s = re.sub(r"\$(.+?)\$", r"\\(\1\\)", s)
    return s


def collect_chain_steps(layer_of):
    """只读扫描 01–07 + README 的箭头链条句（逐字），按 文档层级 + 行号 排序。"""
    out = []
    for rel_top in CHAIN_SOURCES:
        p = os.path.join(ROOT, rel_top)
        files = [p] if os.path.isfile(p) else [
            os.path.join(dp, fn) for dp, _, fns in os.walk(p) for fn in fns if fn.endswith(".md")]
        for fp in files:
            rel = os.path.relpath(fp, ROOT).replace("\\", "/")
            text = io.open(fp, encoding="utf-8", errors="replace").read()
            base = 0
            for ln, line in enumerate(text.splitlines(), 1):
                pos = [m.start() for m in ARROW_RE.finditer(line)]
                if len(pos) >= CHAIN_MIN_ARROWS:
                    lo, hi = pos[0], pos[-1]
                    st = 0
                    for ch in ("，", "。", "|", "：", "；"):
                        st = max(st, line.rfind(ch, 0, max(lo - 20, 0)) + 1)
                    en = len(line)
                    for ch in ("。", "；", "|"):
                        k = line.find(ch, hi + 1)
                        if k > 0:
                            en = min(en, k + 1)
                    span = line[st:en].strip()
                    if len(span) > CHAIN_MAX_SPAN:
                        span = span[:CHAIN_MAX_SPAN].rstrip() + "…"
                    out.append({
                        "doc": rel, "line": ln, "start": base + st, "end": base + st + len(span),
                        "text": span, "layer": layer_of.get(rel, 9),
                        "states": [w for w in STATE_WORDS if w in span],
                        "gaps": list(dict.fromkeys(m.group(0).strip() for m in GAP_RE.finditer(line))),
                    })
                base += len(line) + 1
    seen, uniq = set(), []
    for h in out:
        key = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "", h["text"])
        if len(key) < 12 or key in seen:
            continue
        seen.add(key)
        uniq.append(h)
    uniq.sort(key=lambda h: (h["layer"], h["doc"], h["line"]))
    return uniq


def build_glossary(staged_map, steps):
    """把既有表拼成前端数据：术语卡 / 缺口卡 / 检索索引。"""
    sid2file = {sid: name[:-3] + ".html" for (sid, name, _t, _l) in staged_map.values()}
    ev = {}
    for r in _csv(os.path.join(D00, "证据映射.csv")):
        sid = (r.get("struct_id") or "").strip()
        if sid and sid not in ev and (r.get("quote_clean") or r.get("quote")):
            ev[sid] = r
    alias = {}
    for r in _csv(os.path.join(D01, "概念别名表.csv")):
        alias.setdefault((r.get("concept_id") or "").strip(), []).append((r.get("alias") or "").strip())
    near = {}
    for r in _csv(os.path.join(ROOT08, "05_机器学习数据准备", "嵌入就绪", "语义近邻.csv")):
        near[(r.get("concept_id") or "").strip()] = (r.get("neighbors") or "").strip()
    concepts = _csv(os.path.join(D01, "概念表.csv"))
    gaps = _csv(os.path.join(D01, "缺口编号对照.csv"))
    props = _csv(os.path.join(D01, "命题表.csv"))
    syms = _csv(os.path.join(D09, "符号对照表.csv"))

    terms, index, term_keys, id2name = {}, [], [], {}
    for r in concepts:
        id2name[(r.get("concept_id") or "").strip()] = (r.get("name") or "").strip()
    for r in concepts:
        cid = (r.get("concept_id") or "").strip()
        name = (r.get("name") or "").strip()
        if not name:
            continue
        f = sid2file.get((r.get("source_doc") or "").strip(), "")
        url = "./" + f if f else ""
        al = [a for a in alias.get(cid, []) if a and a != name]
        h = ['<div class="cqm-pop__head"><span class="cqm-pop__name">%s</span>' % _esc(name)]
        if r.get("type"):
            h.append('<span class="cqm-pop__tag">%s</span>' % _esc(r["type"]))
        h.append('<span class="cqm-pop__id">%s</span></div>' % _esc(cid))
        if r.get("definition"):
            h.append('<div class="cqm-pop__def">%s</div>' % _esc(_mathify(r["definition"])))
        e = ev.get(cid)
        if e:
            h.append('<blockquote class="cqm-pop__quote">%s</blockquote>'
                     % _esc(_mathify(e.get("quote_clean") or e.get("quote"))))
            h.append('<div class="cqm-pop__src">原文引文 · %s %s · 字符 %s–%s · 置信 %s</div>' % (
                _esc(e.get("evidence_doc")), _esc(e.get("loc_raw")),
                _esc(e.get("char_start")), _esc(e.get("char_end")), _esc(e.get("confidence"))))
        if al:
            h.append('<div class="cqm-pop__alias">别名：%s</div>' % _esc("、".join(al)))
        nb = []
        for tok in near.get(cid, "").split(";"):
            if ":" not in tok:
                continue
            nid, sc = tok.split(":", 1)
            nb.append("%s（%s）" % (id2name.get(nid.strip(), nid.strip()), sc.strip()))
            if len(nb) >= 5:
                break
        if nb:
            h.append('<div class="cqm-pop__alias">语义近邻（TF-IDF 相似度，'
                     '非理论关系，仅作定位线索）：%s</div>' % _esc("、".join(nb)))
        if url:
            h.append('<div class="cqm-pop__act"><a href="%s">在权威文档中打开</a>'
                     '<span class="cqm-pop__hint">权威源仍是原文与 README，此处只作索引</span></div>' % url)
        terms[name] = "".join(h)
        for a in al:
            if len(a) >= 2:
                terms.setdefault(a, "".join(h))
        term_keys.append(name)
        index.append({"ty": "概念", "tt": name, "sb": (r.get("definition") or ""),
                      "u": url, "dc": (r.get("source_doc") or ""),
                      "hs": " ".join([name, cid, r.get("definition") or "", r.get("type") or "", " ".join(al)]).lower()})

    for r in gaps:
        code = (r.get("gap_code") or "").strip()
        pid = (r.get("prop_id") or "").strip()
        if not code:
            continue
        st = (r.get("status_closure") or r.get("status_prop") or "").strip()
        h = ['<div class="cqm-pop__head"><span class="cqm-pop__name">缺口 %s</span>' % _esc(code)]
        if st:
            h.append('<span class="cqm-pop__tag cqm-pop__tag--%s">%s</span>'
                     % ("open" if st in ("未闭合", "占位") else "wip", _esc(st)))
        h.append('<span class="cqm-pop__id">%s</span></div>' % _esc(pid))
        if r.get("desc_closure"):
            h.append('<div class="cqm-pop__def">%s</div>' % _esc(_mathify(r["desc_closure"])))
        if r.get("lean"):
            h.append('<div class="cqm-pop__rows">Lean：%s</div>' % _esc(_mathify(r["lean"])))
        if r.get("section"):
            h.append('<div class="cqm-pop__src">%s</div>' % _esc(r["section"]))
        h.append('<div class="cqm-pop__act"><a href="./D004_缺口台账.html">在缺口台账中打开</a>'
                 '<span class="cqm-pop__hint">缺口状态原样呈现，不因呈现而升格</span></div>')
        terms[code] = "".join(h)
        if code not in term_keys:
            term_keys.append(code)
        index.append({"ty": "缺口", "tt": "缺口 %s" % code, "sb": (r.get("desc_closure") or ""),
                      "u": "", "dc": pid, "hs": " ".join([code, pid, r.get("desc_closure") or "", st]).lower()})

    for r in props:
        pid = (r.get("prop_id") or "").strip()
        if not pid or (r.get("type") or "").strip() == "缺口":
            continue
        index.append({"ty": "命题", "tt": "%s %s" % (pid, (r.get("type") or "").strip()),
                      "sb": (r.get("statement") or ""), "u": "",
                      "dc": (r.get("source_doc") or ""),
                      "hs": " ".join([pid, r.get("statement") or "", r.get("status") or ""]).lower()})

    for r in syms:
        s = (r.get("symbol") or "").strip()
        if not s:
            continue
        # 符号卡：21 个符号此前只进检索索引，现在补成悬浮卡（含 LaTeX 与出处链接）
        src_raw = (r.get("source") or "").strip()
        h = ['<div class="cqm-pop__head"><span class="cqm-pop__name">%s</span>' % _esc(s),
             '<span class="cqm-pop__tag">符号</span>',
             '<span class="cqm-pop__id">%s</span></div>' % _esc(r.get("name") or "")]
        if r.get("latex"):
            h.append('<div class="cqm-pop__def">%s</div>' % _esc(_mathify(r["latex"])))
        if r.get("kind"):
            h.append('<div class="cqm-pop__rows">类别：%s</div>' % _esc(r["kind"]))
        if r.get("value_or_note"):
            h.append('<div class="cqm-pop__rows">%s</div>' % _esc(_mathify(r["value_or_note"])))
        if src_raw:
            h.append('<div class="cqm-pop__src">出处：%s</div>' % _esc(src_raw))
            first_doc = src_raw.split("§")[0].split("；")[0].strip()
            f = sid2file.get(first_doc, "")
            if f:
                h.append('<div class="cqm-pop__act"><a href="./%s">在权威文档中打开</a></div>' % f)
        terms[s] = "".join(h)
        # 双字符以上的符号才做正文标注（c/α 这类单字符会满页命中）
        if len(s) >= 2 and s not in term_keys:
            term_keys.append(s)
        index.append({"ty": "符号", "tt": s + "　" + (r.get("name") or ""),
                      "sb": "；".join(x for x in [r.get("value_or_note"), r.get("kind")] if x),
                      "u": "", "dc": src_raw,
                      "hs": " ".join([s, r.get("name") or "", r.get("latex") or "",
                                      r.get("value_or_note") or ""]).lower()})

    # 论证卡：70 条重组实现/推导论证，含前件⇒后件与依据文档链接
    args = _csv(os.path.join(D01, "论证表.csv"))
    for r in args:
        aid = (r.get("arg_id") or "").strip()
        if not aid:
            continue
        docs = [x.strip() for x in (r.get("source_doc") or "").split(";") if x.strip()]
        h = ['<div class="cqm-pop__head"><span class="cqm-pop__name">论证 %s</span>' % _esc(aid),
             '<span class="cqm-pop__tag">论证</span>',
             '<span class="cqm-pop__id">%s</span></div>' % _esc(r.get("type") or "")]
        prem = (r.get("premises") or "").strip()
        conc = (r.get("conclusion") or "").strip()
        h.append('<div class="cqm-pop__def">%s ⇒ %s</div>'
                 % (_esc(_mathify(prem)), _esc(_mathify(conc))))
        links = []
        for d in docs:
            f = sid2file.get(d, "")
            links.append('<a href="./%s">%s</a>' % (f, _esc(d)) if f else _esc(d))
        if links:
            h.append('<div class="cqm-pop__src">依据文档：%s</div>' % "、".join(links))
        if r.get("source_concept"):
            h.append('<div class="cqm-pop__rows">概念链：%s</div>' % _esc(r["source_concept"]))
        terms[aid] = "".join(h)
        term_keys.append(aid)
        index.append({"ty": "论证", "tt": "论证 %s" % aid,
                      "sb": "%s ⇒ %s" % (prem, conc), "u": "",
                      "dc": ";".join(docs),
                      "hs": " ".join([aid, prem, conc, r.get("type") or ""]).lower()})

    for i, h in enumerate(steps, 1):
        index.append({"ty": "链条步", "tt": "S%03d" % i, "sb": h["text"], "u": "./" + CHAIN_PAGE[:-3] + ".html",
                      "dc": "%s:%d" % (h["doc"].split("/")[-1], h["line"]),
                      "hs": (h["text"] + " " + " ".join(h["states"])).lower()})

    for sid, name, title, _l in staged_map.values():
        index.append({"ty": "文档", "tt": "%s %s" % (sid, title), "sb": "", "u": "./" + name[:-3] + ".html",
                      "dc": sid, "hs": (sid + " " + title).lower()})

    return {
        "terms": terms,
        "termKeys": sorted(set(term_keys)),
        "index": index,
        "chain": [{"n": i, "doc": h["doc"], "line": h["line"], "cs": h["start"], "ce": h["end"],
                   "text": h["text"], "states": h["states"], "gaps": h["gaps"]}
                  for i, h in enumerate(steps, 1)],
    }


def write_chain_page(steps, staged_map, gap_rows):
    f = os.path.join(DOCS, CHAIN_PAGE)
    sid2file = {sid: name[:-3] + ".md" for (sid, name, _t, _l) in staged_map.values()}
    title_of = {sid: t for (sid, _n, t, _l) in staged_map.values()}
    with io.open(f, "w", encoding="utf-8", newline="\n") as fh:
        w = fh.write
        w("# 展开链（拉通阅读）\n\n")
        w("> 本页由 `_build/build_reader_site.py` 从原文**只读**生成：每一条都是原文**逐字片段**，\n")
        w("> 顺序按「文档层级 → 文档 → 行号」机械排列，**不推断因果、不改写、不补边**。\n")
        w("> 本页是**呈现层索引**，不是权威源；权威源仍是各文档原文与 `README.md`。\n\n")
        w("## 一步一读（%d 条）\n\n" % len(steps))
        for i, h in enumerate(steps, 1):
            gn = "、".join(h["gaps"]) or "—"
            stt = "、".join(h["states"]) or "—"
            w("### S%03d · %s 第 %d 行\n\n" % (i, h["doc"], h["line"]))
            # 逐字片段里可能自带 markdown 链接语法（源文档的表行），
            # 转义方括号使其按字面显示，避免站点把源目录相对路径当链接解析。
            lit = h["text"].replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")
            w("> %s\n\n" % lit.replace(">", "\\>"))
            w("- 出处：`%s` 字符 %d–%d ｜ 涉及缺口：%s ｜ 状态词：%s\n\n" % (
                h["doc"], h["cs"], h["ce"], gn, stt))
        w("## 断点清单（缺口，逐字取自 `缺口编号对照.csv`）\n\n")
        w("| 编号 | 闭合状态 | 描述 | Lean | 所属分组 |\n|:--|:--|:--|:--|:--|\n")
        for r in gap_rows:
            if not (r.get("gap_code") or "").strip():
                continue
            w("| %s | %s | %s | %s | %s |\n" % (
                r.get("gap_code", ""), r.get("status_closure") or r.get("status_prop", ""),
                (r.get("desc_closure") or "").replace("|", "\\|"), r.get("lean", ""),
                r.get("section", "")))
        w("\n## 口径说明\n\n")
        w("- 箭头（`→` / `⇒`）是**原文写法**，其含义（推导／分化／对应）由各文档自行界定，本页不统一。\n")
        w("- 判据只认箭头：用文字推进的叙述会漏，并列对比可能被收入。\n")
        w("- 「涉及缺口」由同句匹配得到，只提示该句谈到某缺口，**不代表逻辑位置**。\n")
        w("- 跨缺口的阅读必须以缺口自身状态为前提，缺口状态见上表，未闭合项不得读作已成立。\n")
    return f


def stage_lectures():
    """把 一体化研究/展开链讲稿/ 的撰述稿 staged 进站（L001 起编号，L000 留给展开链页）。

    讲稿是**撰述**（作者叙述），不属于理论语料，故不进引用清单、不计入语料统计；
    仅作为阅读站的呈现页出现，正文逐字原样复制、不做改写。
    """
    out = []
    if not os.path.isdir(LECT_DIR):
        return out
    for i, src in enumerate(sorted(glob.glob(os.path.join(LECT_DIR, "*.md"))), 1):
        stem = safe_name(os.path.basename(src)[:-3])   # safe_name 已带回 .md 后缀
        name = f"L{i:03d}_{stem}"
        with io.open(os.path.join(DOCS, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(read(src))
        out.append({"file": name, "title": os.path.basename(src)[:-3], "id": f"L{i:03d}"})
    return out


def stage_viz():
    """把四个分散的自包含可视化收进阅读站：HTML 落 assets/viz/，各自生成一个 iframe 包装页。"""
    vdir = os.path.join(DOCS, "assets", "viz")
    os.makedirs(vdir, exist_ok=True)
    out = []
    for rel, name, extra, title, desc in VIZ_SOURCES:
        src = os.path.join(ROOT08, "10_展示可视化", rel)
        if not os.path.isfile(src):
            continue
        txt = read(src)
        for a, b in VIZ_LINK_FIX:
            txt = txt.replace(a, b)
        if extra:
            txt = txt.replace(extra[0], extra[1])
            esrc = os.path.join(os.path.dirname(src), extra[0])
            if os.path.isfile(esrc):
                shutil.copyfile(esrc, os.path.join(vdir, extra[1]))
        with io.open(os.path.join(vdir, name), "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        out.append({"src": name, "title": title, "desc": desc})
    return out


def write_viz_pages(viz):
    """可视化栏目：总览页 + 每个可视化一个 iframe 包装页。"""
    if not viz:
        return []
    pages = []
    overview = os.path.join(DOCS, "V000_可视化总览.md")
    with io.open(overview, "w", encoding="utf-8", newline="\n") as f:
        f.write("# 可视化总览\n\n")
        f.write("> 本栏目把原先分散在各目录的自包含可视化收进同一站点，入口唯一：\n")
        f.write("> 左侧「可视化」→ 本页 → 四个子页。原文件仍留在 `10_展示可视化/` 各目录（作为源），\n")
        f.write("> 本页由 `_build/build_reader_site.py` 构建期复制与包装，**不改动源文件**。\n\n")
        f.write("| 页 | 看什么 | 数据来源 | 形态 |\n|:--|:--|:--|:--|\n")
        for i, v in enumerate(viz, 1):
            f.write("| [%s](V%03d_%s.md) | %s | 见子页内标注 | 自包含 HTML，iframe 内嵌 |\n"
                    % (v["title"], i, v["title"], v["desc"]))
        f.write("\n**共用的口径**：所有可视化只呈现既有产物（源 CSV、`超图数据.json`、`知识图谱.json`、"
                "`证据映射.json`、`declarations.json` 等），不新增理论内容、不改数值、不改缺口状态。\n\n")
        f.write("**另外两处**：`03_超图与理论图/超图可视化.html` 与「可推演超图」是同一构件的同步副本"
                "（03 维度内另存一份，便于就近引用）；阅读站自身的「展开链」与「讲稿」页不属于本栏目，"
                "它们是文本层而非图谱层。\n")
    pages.append({"file": "V000_可视化总览.md", "title": "可视化总览"})
    for i, v in enumerate(viz, 1):
        p = "V%03d_%s.md" % (i, v["title"])
        with io.open(os.path.join(DOCS, p), "w", encoding="utf-8", newline="\n") as f:
            f.write("# %s\n\n" % v["title"])
            f.write("%s\n\n" % v["desc"])
            f.write('<iframe class="cqm-frame" src="assets/viz/%s" title="%s"></iframe>\n\n'
                    % (v["src"], v["title"]))
            f.write('<p class="cqm-frame__fb">若内嵌框未显示（个别浏览器对本地文件的内嵌有限制），'
                    '<a href="assets/viz/%s" target="_blank" rel="noopener">点此在新标签页直接打开</a>。</p>\n'
                    % v["src"])
        pages.append({"file": p, "title": v["title"]})
    return pages


def write_enhance_assets(staged_map, lectures=(), viz=()):
    gg = build_glossary(staged_map, collect_chain_steps({rel: v[3] for rel, v in staged_map.items()}))
    for lec in lectures:
        body = read(os.path.join(DOCS, lec["file"])) if os.path.isfile(os.path.join(DOCS, lec["file"])) else ""
        head, quote = "", ""
        for ln in body.splitlines():
            if not head and ln.startswith("# "):
                head = ln[2:].strip()
            if not quote and ln.startswith("> ") and len(ln) > 40 and "稿子性质" not in ln:
                quote = ln[2:].strip()
            if head and quote:
                break
        gg["index"].append({"ty": "讲稿", "tt": head or lec["title"], "sb": quote,
                            "u": "./" + lec["file"][:-3] + ".html", "dc": lec["id"],
                            "hs": (head + " " + quote + " " + lec["title"] + " 展开链 讲稿 撰述").lower()})
    adir = os.path.join(DOCS, "assets")
    os.makedirs(os.path.join(adir, "stylesheets"), exist_ok=True)
    with io.open(os.path.join(adir, "cqm-glossary.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.CQM_GLOSSARY=" + json.dumps(gg, ensure_ascii=False) + ";\n")
    depth_cfg = {"map": LECT_DEPTH_MAP, "levels": LECT_DEPTH_LEVELS, "default": LECT_DEPTH_DEFAULT,
                 "force": LECT_DEPTH_FORCE, "forceRe": LECT_DEPTH_FORCE_RE}
    with io.open(os.path.join(adir, "cqm-depth.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write("window.CQM_DEPTH=" + json.dumps(depth_cfg, ensure_ascii=False) + ";\n")
    with io.open(os.path.join(adir, "cqm-enhance.js"), "w", encoding="utf-8", newline="\n") as f:
        f.write(ENHANCE_JS)
    with io.open(os.path.join(adir, "stylesheets", "cqm-enhance.css"), "w", encoding="utf-8", newline="\n") as f:
        f.write(ENHANCE_CSS)
    return gg


ENHANCE_CSS = """/* CQM 阅读站增强（构建期生成）：术语悬浮卡 · 缺口徽章 · 高级搜索 */
.cqm-term {
  border-bottom: 1px dotted var(--cqm-blue, #2f6fb5);
  color: inherit; cursor: help; background: transparent;
  border-radius: 0; padding: 0; text-decoration: none;
}
.cqm-term:hover, .cqm-term:focus { background: rgba(47, 111, 181, .10); outline: none; }
.cqm-term--gap { border-bottom-color: #b4732f; }
.cqm-term--gap:hover, .cqm-term--gap:focus { background: rgba(180, 115, 47, .12); }
[data-md-color-scheme="slate"] .cqm-term:hover,
[data-md-color-scheme="slate"] .cqm-term:focus { background: rgba(120, 170, 230, .18); }
.cqm-pop {
  position: absolute; z-index: 60; width: min(460px, 92vw);
  background: var(--md-default-bg-color, #fff);
  border: 1px solid rgba(47, 111, 181, .35); border-radius: 10px;
  box-shadow: 0 10px 30px rgba(20, 40, 70, .18);
  padding: .8em .95em; font-size: .82rem; line-height: 1.8; text-align: left;
}
.cqm-pop__head { display: flex; align-items: baseline; gap: .4em; flex-wrap: wrap; margin-bottom: .35em; }
.cqm-pop__name { font-weight: 600; font-size: .95rem; }
.cqm-pop__tag {
  font-size: .68rem; padding: .05em .45em; border-radius: 999px;
  background: rgba(47, 111, 181, .12); color: var(--cqm-blue, #2f6fb5);
}
.cqm-pop__tag--open { background: rgba(200, 60, 60, .14); color: #b03434; }
.cqm-pop__tag--wip { background: rgba(180, 115, 47, .16); color: #9a641f; }
.cqm-pop__id { margin-left: auto; font-size: .68rem; opacity: .55; font-family: Consolas, monospace; }
.cqm-pop__def { margin: .2em 0 .45em; }
.cqm-pop__quote {
  margin: .3em 0; padding: .35em .6em; border-left: 3px solid var(--cqm-cyan, #38bdf8);
  background: rgba(56, 197, 248, .07); border-radius: 0 6px 6px 0;
  max-height: 9.5em; overflow: auto;
}
.cqm-pop__src, .cqm-pop__alias, .cqm-pop__rows { font-size: .7rem; opacity: .72; margin-top: .25em; }
.cqm-pop__act { margin-top: .5em; display: flex; align-items: center; gap: .6em; flex-wrap: wrap; }
.cqm-pop__act a { font-size: .74rem; }
.cqm-pop__hint { font-size: .66rem; opacity: .6; }
/* 头部按钮 */
.cqm-sbtn {
  border: 0; background: transparent; color: inherit; cursor: pointer;
  font-size: .72rem; padding: .25em .5em; border-radius: 6px;
  display: inline-flex; align-items: center; gap: .3em;
}
.cqm-sbtn:hover { background: rgba(255, 255, 255, .16); }
.cqm-kbd {
  font-family: Consolas, monospace; font-size: .64rem; padding: 0 .3em;
  border: 1px solid currentColor; border-radius: 4px; opacity: .7;
}
/* 搜索覆盖层 */
.cqm-mask { position: fixed; inset: 0; background: rgba(14, 24, 38, .45); z-index: 80; }
.cqm-search {
  position: fixed; z-index: 81; left: 50%; top: 8vh; transform: translateX(-50%);
  width: min(760px, 94vw); max-height: 80vh; display: flex; flex-direction: column;
  background: var(--md-default-bg-color, #fff); border-radius: 12px;
  border: 1px solid rgba(47, 111, 181, .3); box-shadow: 0 18px 50px rgba(10, 25, 45, .35);
  overflow: hidden; text-align: left;
}
.cqm-search__top { display: flex; gap: .5em; align-items: center; padding: .7em .9em; border-bottom: 1px solid rgba(47, 111, 181, .18); }
.cqm-search__top input { flex: 1; border: 0; outline: 0; font-size: .95rem; background: transparent; color: inherit; }
.cqm-facets { display: flex; flex-wrap: wrap; gap: .35em; padding: .5em .9em; border-bottom: 1px solid rgba(47, 111, 181, .12); }
.cqm-facet {
  font-size: .7rem; padding: .12em .55em; border-radius: 999px; cursor: pointer;
  border: 1px solid rgba(47, 111, 181, .3); background: transparent; color: inherit;
}
.cqm-facet[data-on="1"] { background: var(--cqm-blue, #2f6fb5); border-color: var(--cqm-blue, #2f6fb5); color: #fff; }
.cqm-res { overflow: auto; padding: .3em 0 .5em; }
.cqm-res__it { padding: .45em .9em; cursor: pointer; border-left: 3px solid transparent; }
.cqm-res__it[data-sel="1"] { background: rgba(47, 111, 181, .1); border-left-color: var(--cqm-blue, #2f6fb5); }
.cqm-res__tt { font-size: .82rem; font-weight: 500; }
.cqm-res__ty { font-size: .66rem; padding: .05em .4em; border-radius: 999px; background: rgba(47, 111, 181, .12); color: var(--cqm-blue, #2f6fb5); margin-right: .4em; }
.cqm-res__sb { font-size: .74rem; opacity: .78; margin-top: .12em; }
.cqm-res mark { background: rgba(255, 214, 102, .55); color: inherit; padding: 0 .05em; border-radius: 2px; }
.cqm-search__foot { display: flex; justify-content: space-between; align-items: center; padding: .45em .9em; font-size: .68rem; opacity: .75; border-top: 1px solid rgba(47, 111, 181, .12); }
/* 深度滑杆（讲稿页） */
.cqm-depthbar {
  position: sticky; top: 2.4rem; z-index: 5; display: flex; flex-wrap: wrap;
  align-items: center; gap: .4em; margin: .2em 0 1em; padding: .5em .7em;
  background: var(--md-default-bg-color, #fff); border: 1px solid rgba(47, 111, 181, .25);
  border-radius: 10px; font-size: .72rem;
}
.cqm-depthbar__lab { opacity: .7; }
.cqm-dl {
  border: 1px solid rgba(47, 111, 181, .35); background: transparent; color: inherit;
  border-radius: 999px; padding: .1em .6em; font-size: .72rem; cursor: pointer;
}
.cqm-dl[data-on="1"] { background: var(--cqm-blue, #2f6fb5); border-color: var(--cqm-blue, #2f6fb5); color: #fff; }
.cqm-depthbar__stat { margin-left: auto; opacity: .72; }
.cqm-dep-hidden { display: none !important; }
.cqm-dep-force { border-left: 3px solid rgba(200, 90, 60, .55); padding-left: .6em; }
/* 可视化内嵌框 */
.cqm-frame { width: 100%; height: calc(100vh - 230px); border: 0; border-radius: 10px; background: transparent; }
.cqm-frame__fb { font-size: .74rem; opacity: .7; }
[data-md-color-scheme="slate"] .cqm-pop,
[data-md-color-scheme="slate"] .cqm-search,
[data-md-color-scheme="slate"] .cqm-depthbar { background: #1d2430; }
"""

ENHANCE_JS = r"""(function () {
  var G = window.CQM_GLOSSARY; if (!G) return;
  var POP, cur = null, pinned = false;

  function ensurePop() {
    if (POP) return POP;
    POP = document.createElement("div");
    POP.className = "cqm-pop"; POP.style.display = "none";
    document.body.appendChild(POP);
    POP.addEventListener("mouseenter", function () { pinned = true; });
    POP.addEventListener("mouseleave", function () { pinned = false; hidePop(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") hidePop(); });
    window.addEventListener("scroll", function () { if (!pinned) hidePop(); }, true);
    return POP;
  }
  function hidePop() { if (POP) { POP.style.display = "none"; cur = null; } }
  function place(p, el) {
    var r = el.getBoundingClientRect(), sx = window.pageXOffset, sy = window.pageYOffset;
    var w = p.offsetWidth, h = p.offsetHeight;
    var vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var left = Math.max(sx + 8, Math.min(r.left + sx, sx + vw - w - 8));
    var top = r.bottom + sy + 6;
    if (r.bottom + h + 18 > vh) top = Math.max(sy + 8, r.top + sy - h - 6);
    p.style.left = left + "px"; p.style.top = top + "px";
  }
  /* MathJax 只在页面加载时扫描一次；动态插入的卡片必须重新排版，否则 $...$ 原样显示 */
  function typeset(el, cb) {
    try {
      if (window.MathJax && window.MathJax.typesetPromise) { window.MathJax.typesetPromise([el]).then(cb, cb); return; }
      if (window.MathJax && window.MathJax.startup) { window.MathJax.startup.promise.then(function () { window.MathJax.typesetPromise([el]).then(cb, cb); }); return; }
    } catch (e) {}
    cb();
  }
  function showPop(el) {
    var html = G.terms[el.getAttribute("data-cqm")];
    if (!html) return;
    var p = ensurePop();
    p.innerHTML = html; p.style.display = "block"; p.style.left = "-9999px"; p.style.top = "0";
    cur = el;
    typeset(p, function () { place(p, el); });
  }
  document.addEventListener("mouseover", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (el && el !== cur) showPop(el);
  });
  document.addEventListener("mouseout", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (el && !pinned) setTimeout(function () { if (!pinned) hidePop(); }, 180);
  });
  document.addEventListener("focusin", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]"); if (el) showPop(el);
  });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".cqm-pop a");
    if (a) return;
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (el) { e.preventDefault(); showPop(el); }
  });

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var keys = (G.termKeys || []).slice().sort(function (a, b) { return b.length - a.length; });
  function runTerms() {
    if (!keys.length) return;
    var re = new RegExp(keys.map(function (k) { return k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|"), "g");
    var used = {}, total = 0, MAX = 240, PER = 2;
    function inSkip(n) {
      var p = n.parentNode; if (!p || !p.nodeName) return true;
      var tag = p.nodeName.toLowerCase();
      // 标题、导航、按钮、表格头、代码、链接内不标注（标题里画满蓝线会让页面花掉）
      if (/^(a|code|pre|script|style|textarea|button|summary|th|caption|dt|h1|h2|h3|h4|h5|h6)$/.test(tag)) return true;
      if (p.closest && p.closest(".cqm-pop,.cqm-search,.md-nav,.md-header,.md-search,.md-sidebar,.md-footer,.md-tabs,.md-typeset h1,.md-typeset h2,.md-typeset h3,.md-typeset h4")) return true;
      return false;
    }
    function wrap(node) {
      if (inSkip(node) || !node.nodeValue || node.nodeValue.trim().length < 2) return;
      var txt = node.nodeValue, frag = null, last = 0, m; re.lastIndex = 0;
      while ((m = re.exec(txt))) {
        var k = m[0]; if (!G.terms[k]) continue;
        if ((used[k] || 0) >= PER || total >= MAX) continue;
        used[k] = (used[k] || 0) + 1; total++;
        if (!frag) frag = document.createDocumentFragment();
        if (m.index > last) frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var sp = document.createElement("span");
        sp.className = "cqm-term" + (/^(缺口\s*)?(C|G\d+|N[1-4])$/.test(k) ? " cqm-term--gap" : "");
        sp.setAttribute("data-cqm", k); sp.setAttribute("tabindex", "0");
        sp.textContent = k;
        frag.appendChild(sp); last = m.index + k.length;
      }
      if (frag) { if (last < txt.length) frag.appendChild(document.createTextNode(txt.slice(last))); node.parentNode.replaceChild(frag, node); }
    }
    var art = document.querySelector("article.md-content__inner") || document.querySelector("article");
    if (art) {
      var w = document.createTreeWalker(art, NodeFilter.SHOW_TEXT, null);
      var nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
      nodes.forEach(wrap);
    }
  }

  var IDX = G.index || [], F = { ty: "", q: "" }, SEL = 0, MASK, BOX, INP, RES;
  function tokens(q) {
    var out = [], s = q.toLowerCase().replace(/\s+/g, ""), m;
    var re = /[a-z0-9_.\-]+|[\u4e00-\u9fff]+/gi;
    while ((m = re.exec(s))) {
      var t = m[0];
      if (/^[\u4e00-\u9fff]+$/.test(t)) { out.push(t); for (var i = 0; i < t.length - 1; i++) out.push(t.slice(i, i + 2)); }
      else out.push(t);
    }
    return out;
  }
  function score(it, toks) {
    if (!toks.length) return 1;
    var hs = it.hs, hit = 0, s = 0;
    for (var i = 0; i < toks.length; i++) {
      var t = toks[i];
      if (hs.indexOf(t) >= 0) { hit++; s += 1 + t.length * 0.6; }
      else if (t.length > 2 && hs.indexOf(t.slice(0, 2)) >= 0) s += 0.25;
    }
    if (!hit) return 0;
    if (hs.indexOf(toks[0]) === 0) s += 2;
    if (it.ty === "概念") s += 1.2;
    if (it.ty === "缺口") s += 0.8;
    return s * (1 + hit / toks.length);
  }
  function hl(text, toks) {
    var t = esc(text || "");
    for (var i = 0; i < toks.length; i++) {
      var k = toks[i]; if (k.length < 2) continue;
      var safe = k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      t = t.replace(new RegExp(safe, "gi"), function (x) { return "<mark>" + x + "</mark>"; });
    }
    return t;
  }
  function run() {
    var q = INP.value, toks = tokens(q), hits = [];
    for (var i = 0; i < IDX.length; i++) {
      if (F.ty && IDX[i].ty !== F.ty) continue;
      var s = score(IDX[i], toks); if (s > 0) hits.push({ it: IDX[i], s: s });
    }
    hits.sort(function (a, b) { return b.s - a.s; });
    var top = hits.slice(0, 60);
    SEL = 0;
    RES.innerHTML = "";
    if (!top.length) {
      RES.innerHTML = '<div class="cqm-res__it"><div class="cqm-res__tt">无匹配</div>' +
        '<div class="cqm-res__sb">可放宽分类，或用页面右上角的全文检索（lunr + jieba 分词）继续。</div></div>';
      return;
    }
    top.forEach(function (h, i) {
      var d = document.createElement("div");
      d.className = "cqm-res__it"; d.setAttribute("data-i", i);
      d.innerHTML = '<div class="cqm-res__tt"><span class="cqm-res__ty">' + h.it.ty + "</span>" +
        hl(h.it.tt, toks) + '</div><div class="cqm-res__sb">' + hl(h.it.sb, toks).slice(0, 300) + "</div>";
      d.addEventListener("click", function () { open(i); });
      RES.appendChild(d);
    });
    RES.__data = top;
    sel(0);
    typeset(RES, function () {});
  }
  function sel(i) {
    var items = RES.querySelectorAll(".cqm-res__it[data-i]");
    if (!items.length) return;
    SEL = (i + items.length) % items.length;
    items.forEach(function (e, j) { e.setAttribute("data-sel", j === SEL ? "1" : "0"); });
    items[SEL].scrollIntoView({ block: "nearest" });
  }
  function open(i) {
    var top = RES.__data; if (!top || !top[i]) return;
    var u = top[i].it.u; if (u) location.href = u;
  }
  function facets() {
    var types = {}, t;
    for (var i = 0; i < IDX.length; i++) { t = IDX[i].ty; types[t] = (types[t] || 0) + 1; }
    var box = document.createElement("div"); box.className = "cqm-facets";
    var all = document.createElement("button");
    all.className = "cqm-facet"; all.textContent = "全部 " + IDX.length;
    all.setAttribute("data-on", "1"); all.addEventListener("click", function () { F.ty = ""; paint(box); run(); });
    box.appendChild(all);
    Object.keys(types).forEach(function (k) {
      var b = document.createElement("button");
      b.className = "cqm-facet"; b.setAttribute("data-ty", k); b.textContent = k + " " + types[k];
      b.addEventListener("click", function () { F.ty = (F.ty === k ? "" : k); paint(box); run(); });
      box.appendChild(b);
    });
    box.__paint = function () {
      box.querySelectorAll(".cqm-facet").forEach(function (b) {
        var k = b.getAttribute("data-ty");
        b.setAttribute("data-on", (k === null ? F.ty === "" : F.ty === k) ? "1" : "0");
      });
    };
    return box;
  }
  function paint(box) { box.__paint(); }
  function build() {
    if (BOX) return BOX;
    MASK = document.createElement("div"); MASK.className = "cqm-mask";
    MASK.addEventListener("click", close);
    BOX = document.createElement("div"); BOX.className = "cqm-search";
    var top = document.createElement("div"); top.className = "cqm-search__top";
    INP = document.createElement("input");
    INP.placeholder = "检索概念 / 缺口 / 命题 / 符号 / 链条步 / 文档（结构化实体检索）";
    INP.addEventListener("input", run);
    top.appendChild(INP);
    var fb = document.createElement("button");
    fb.className = "cqm-facet"; fb.textContent = "转到全文检索 →";
    fb.addEventListener("click", function () {
      var mi = document.querySelector(".md-search__input");
      close();
      if (mi) { mi.focus(); mi.value = INP.value; mi.dispatchEvent(new Event("input", { bubbles: true })); }
    });
    top.appendChild(fb);
    BOX.appendChild(top);
    var f = facets(); BOX.appendChild(f);
    RES = document.createElement("div"); RES.className = "cqm-res"; BOX.appendChild(RES);
    var foot = document.createElement("div"); foot.className = "cqm-search__foot";
    foot.innerHTML = "<span>↑↓ 选择 · Enter 打开 · Esc 关闭</span><span>数据来自 01_结构化数据 / 09_桥接与翻译（逐字）</span>";
    BOX.appendChild(foot);
    addEventListener("resize", function () { if (BOX && BOX.style.display !== "none") run(); });
    return BOX;
  }
  function openBox() {
    build(); MASK.style.display = "block"; BOX.style.display = "flex";
    INP.value = ""; F.ty = ""; paint(BOX.querySelector(".cqm-facets")); run(); INP.focus();
  }
  function close() { if (BOX) { BOX.style.display = "none"; MASK.style.display = "none"; } }
  function bind() {
    document.addEventListener("keydown", function (e) {
      var typing = /^(input|textarea)$/i.test((e.target.tagName || ""));
      if ((e.key === "k" || e.key === "K") && (e.ctrlKey || e.metaKey)) { e.preventDefault(); openBox(); return; }
      if (e.key === "/" && !typing) { e.preventDefault(); openBox(); return; }
      if (!BOX || BOX.style.display === "none") return;
      if (e.key === "Escape") { close(); }
      else if (e.key === "ArrowDown") { e.preventDefault(); sel(SEL + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); sel(SEL - 1); }
      else if (e.key === "Enter") { e.preventDefault(); open(SEL); }
    });
    var hdr = document.querySelector(".md-header__inner") || document.querySelector(".md-header");
    if (hdr) {
      var b = document.createElement("button");
      b.className = "cqm-sbtn"; b.type = "button";
      b.innerHTML = '高级检索 <span class="cqm-kbd">Ctrl</span><span class="cqm-kbd">K</span>';
      b.addEventListener("click", openBox);
      hdr.appendChild(b);
    }
  }
  /* ---- 深度滑杆：同一批论断的四种高度（仅讲稿页 L001 起） ---- */
  function initDepth() {
    var D = window.CQM_DEPTH; if (!D) return;
    var m = /(^|\/)(L\d{3})_/.exec(location.pathname); if (!m || m[2] === "L000") return;
    var art = document.querySelector("article.md-content__inner") || document.querySelector("article");
    if (!art) return;
    var map = D.map || {}, levels = D.levels || {}, force = D.force || [], def = D.default || 3;
    var fre = D.forceRe ? new RegExp(D.forceRe) : null;
    var heads = [], blocks = [], cur = def, i;
    for (i = 0; i < art.children.length; i++) {
      var el = art.children[i], tag = (el.tagName || "").toLowerCase();
      if (tag === "h2") {
        var t = (el.textContent || "").replace(/\s+/g, " ").trim();
        cur = def;
        for (var k in map) { if (t.indexOf(k) === 0) { cur = map[k]; break; } }
      } else if (tag !== "h3") {
        if (!/^(p|ul|ol|table|blockquote|pre|div|details|section)$/.test(tag)) continue;
      }
      var txt = el.textContent || "", isForce = false;
      for (var j = 0; j < force.length; j++) { if (txt.indexOf(force[j]) >= 0) { isForce = true; break; } }
      if (!isForce && fre && fre.test(txt)) isForce = true;
      el.__cqmDepth = cur; el.__cqmForce = isForce;
      blocks.push(el);
      if (tag === "h2" || tag === "h3") heads.push(el);
    }
    var bar = document.createElement("div");
    bar.className = "cqm-depthbar";
    bar.innerHTML = '<span class="cqm-depthbar__lab">阅读深度</span>';
    var btns = {};
    [1, 2, 3, 4].forEach(function (lv) {
      var b = document.createElement("button");
      b.className = "cqm-dl"; b.type = "button";
      b.textContent = (levels[String(lv)] || ("第" + lv + "层"));
      b.addEventListener("click", function () { setDepth(lv); });
      btns[lv] = b; bar.appendChild(b);
    });
    var stat = document.createElement("span");
    stat.className = "cqm-depthbar__stat";
    bar.appendChild(stat);
    var first = art.querySelector("h2");
    if (first && first.parentNode === art) art.insertBefore(bar, first); else art.appendChild(bar);
    function setDepth(lv) {
      localStorage.setItem("cqm-lect-depth", String(lv));
      var isHead = function (el) { return /^h[1-6]$/.test((el.tagName || "").toLowerCase()); };
      blocks.forEach(function (el) {
        if (isHead(el)) return;
        var hide = (el.__cqmDepth > lv) && !el.__cqmForce;
        el.classList.toggle("cqm-dep-hidden", hide);
        el.classList.toggle("cqm-dep-force", !!el.__cqmForce && el.__cqmDepth > lv);
      });
      heads.forEach(function (h) { h.classList.toggle("cqm-dep-hidden", h.__cqmDepth > lv); });
      heads.forEach(function (h, idx) {
        if (!h.classList.contains("cqm-dep-hidden")) return;
        var next = heads[idx + 1] || null, seen = false, start = blocks.indexOf(h) + 1;
        for (var s = start; s < blocks.length; s++) {
          if (next && blocks[s] === next) break;
          if (!blocks[s].classList.contains("cqm-dep-hidden")) { seen = true; break; }
        }
        if (seen) { h.classList.remove("cqm-dep-hidden"); h.classList.add("cqm-dep-force"); }
      });
      var shown = 0, kept = 0;
      blocks.forEach(function (el) {
        if (!el.classList.contains("cqm-dep-hidden")) shown++;
        if (el.__cqmForce && el.__cqmDepth > lv) kept++;
      });
      for (var lv2 = 1; lv2 <= 4; lv2++) if (btns[lv2]) btns[lv2].setAttribute("data-on", lv2 === lv ? "1" : "0");
      stat.textContent = "本页 " + blocks.length + " 块 · 显示 " + shown + " 块 · 隐藏 "
        + (blocks.length - shown) + " 块更深内容 · 其中断点/限定语块 " + kept + " 个不随深度隐藏";
    }
    var saved = parseInt(localStorage.getItem("cqm-lect-depth") || "", 10);
    setDepth(saved >= 1 && saved <= 4 ? saved : def);
  }

  function init() {
    document.body.appendChild(build());
    document.body.appendChild(MASK);
    BOX.style.display = "none"; MASK.style.display = "none";
    bind();
    runTerms();
    initDepth();
    probeService();
  }
  /* 本地服务探测：服务在场才亮徽标（静态/离线时 fetch 失败即静默降级） */
  function probeService() {
    try {
      fetch("api/status", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (s) {
        var hdr = document.querySelector(".md-header__inner") || document.querySelector(".md-header");
        if (!hdr || !s || !s.counts) return;
        var b = document.createElement("a");
        b.className = "cqm-sbtn"; b.href = "api"; b.title = "本地研究站服务已连接：实时 SPARQL / 结构化检索 / 证据复核写回";
        b.innerHTML = "服务已连接 · 概念 " + s.counts.concepts + " · 缺口 " + s.counts.gaps
          + " · 待复核 " + (s.review ? s.review.pending : "-");
        hdr.appendChild(b);
      })["catch"](function () {});
    } catch (e) {}
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
"""


def write_config(nav, site_dir):
    yml = f"""site_name: CQM 理论阅读站
site_description: CQM 自然语言理论文本的离线阅读层（Material for MkDocs）
docs_dir: mkdocs_src/docs
site_dir: {site_dir.replace(os.sep, '/')}
use_directory_urls: false          # file:// 直开必需（平铺 .html）
theme:
  name: material
  language: zh
  font: false                      # 不引 Google Fonts（离线）
  features:
    - navigation.top
    - navigation.sections
    - navigation.footer             # 上一页/下一页（文档连读）
    - toc.follow
    - search.highlight
    - search.suggest
    - content.code.copy
    - content.tabs.link
    - content.tooltips
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      toggle: {{ icon: material/brightness-7, name: 切换到深色模式 }}
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      toggle: {{ icon: material/brightness-4, name: 切换到浅色模式 }}
plugins:
  - search:
      lang: zh
      jieba_dict_user: cqm_user_dict.txt
  - offline
  - privacy
markdown_extensions:
  - admonition
  - attr_list
  - tables
  - toc: {{ permalink: true, toc_depth: 3 }}
  - pymdownx.arithmatex:
      generic: True                 # 关键：输出 \\(..\\) 给 MathJax v3；默认的 script[type=math/tex] 是 v2 格式，v3 不识别
  - pymdownx.highlight
  - pymdownx.superfences
  - pymdownx.details
extra_css:
  - assets/stylesheets/extra.css    # 项目品牌色 + CJK 排版定制 + 反链样式
  - assets/stylesheets/cqm-enhance.css  # 术语悬浮卡 / 缺口徽章 / 高级检索（构建期生成）
extra_javascript:
  - assets/backlinks.js             # 构建期生成：被引用数据
  - assets/backlink-inject.js       # 页尾注入「被引用」区块
  - assets/cqm-glossary.js          # 术语卡 / 缺口卡 / 检索索引（构建期生成，逐字取自既有表）
  - assets/cqm-depth.js             # 讲稿深度分层配置（1 导读 / 2 概念 / 3 链条 / 4 技术）
  - assets/cqm-enhance.js           # 术语标注 + 悬浮卡 + Ctrl/⌘+K 高级检索 + 深度滑杆
  - assets/math-config.js
  - assets/tex-svg.js
nav:
{nav}
"""
    with io.open(CONF, "w", encoding="utf-8", newline="\n") as f:
        f.write(yml)


def build_nav(staged_map, lectures=(), viz_pages=()):
    lines = ["  - 首页: index.md",
             f"  - 展开链（拉通阅读）: {CHAIN_PAGE}"]
    for lec in lectures:
        lines.append(f"  - {lec['title'].replace('_', '：')}（四层深度）: {lec['file']}")
    if viz_pages:
        lines.append("  - 可视化:")
        for p in viz_pages:
            lines.append(f"      - {p['title']}: {p['file']}")
    groups = {}
    for rel, (sid, name, title, layer) in staged_map.items():
        if rel == "README.md":
            continue
        groups.setdefault(layer, []).append((sid, name, title))
    for layer in sorted(groups):
        lines.append(f"  - {LAYER_NAME.get(layer, '其他')}:")
        for sid, name, title in sorted(groups[layer]):
            lines.append(f"      - {title} [{sid}]: {name}")
    return "\n".join(lines)


def main():
    reg = registry()
    user_dict, n_terms = build_user_dict()
    staged_map, unreg = stage_docs(reg)
    write_support_assets(staged_map)
    lectures = stage_lectures()
    viz = stage_viz()
    viz_pages = write_viz_pages(viz)
    gg = write_enhance_assets(staged_map, lectures, viz_pages)
    write_chain_page(gg["chain"], staged_map, _csv(os.path.join(D01, "缺口编号对照.csv")))
    n_docs = len(staged_map)
    # 旧站资产在 stage 前需先备份 tex-svg（TEX_SVG 指向旧站目录，stage 不清站点目录）
    site_dir = SITE.replace(os.sep, "/")
    write_config(build_nav(staged_map, lectures, viz_pages), site_dir)
    print(f"[staging] 文档 {n_docs} 篇（未登记 {unreg}）→ {DOCS}")
    print(f"[user_dict] 词条 {n_terms} → {user_dict}")
    # 清空旧站（旧单页站由 git 历史保留），保留 assets/tex-svg.js 源已被复制进 staging
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(SITE, exist_ok=True)
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    r = subprocess.run([sys.executable, "-m", "mkdocs", "build", "-f", CONF, "--clean"],
                       capture_output=True, encoding="utf-8", errors="replace", env=env)
    out = (r.stdout or "") + (r.stderr or "")
    warn = [l for l in out.splitlines() if "WARNING" in l or "ERROR" in l]
    print(f"[mkdocs] exit={r.returncode}  警告/错误 {len(warn)} 条")
    for l in warn[:12]:
        print("   ", l[:200])
    files = [p for p in glob.glob(os.path.join(SITE, "**", "*"), recursive=True) if os.path.isfile(p)]
    idx = os.path.join(SITE, "index.html")
    with io.open(os.path.join(SITE, "README.md"), "w", encoding="utf-8", newline="\n") as f:
        f.write(SITE_README)
    print(f"[OK] 阅读站：{len(files)} 个文件 / index.html {os.path.getsize(idx) if os.path.exists(idx) else 0:,} B")
    if r.returncode != 0:
        print(out[-2500:])
        sys.exit(1)


SITE_README = """# 阅读站（构建产物）

> 本目录是 `_build/build_reader_site.py` 的输出，**每次重建会整体重写**，请勿在此手工编辑。

## 打开方式

双击 `index.html` 即可（`file://` 直开）：站点为**离线自足**——`offline` 插件保证搜索可用、
`privacy` 插件把外部资源本地化，`font: false` 不引外部字体，成品零外链。

## 阅读功能

| 功能 | 入口 | 说明 |
|:--|:--|:--|
| 全文检索 | 顶栏搜索框 | Material 内置（lunr + 官方 zh + 构建期 jieba 分词 + CQM 用户词典） |
| **高级检索** | 顶栏「高级检索」按钮，或 `Ctrl/⌘ + K`、`/` | 结构化实体检索：概念 82 / 命题 / 缺口 24 / 符号 / 文档 / 展开链步；按分类筛选（facet）、结果高亮、`↑↓` 选择、`Enter` 打开；可一键「转到全文检索」 |
| **术语悬浮卡** | 正文中带蓝色虚线的术语 | 悬停/聚焦/点击弹出卡片：定义与**原文引文**（含出处文档、字符区间、置信度）逐字取自 `01_结构化数据/概念表.csv` 与 `00_外部引用/证据映射.csv` |
| **缺口徽章** | 正文中的 `C` / `G*` / `N*` 编号 | 悬停显示该缺口的**闭合状态、描述、Lean 登记与所属分组**，状态原样呈现 |
| **展开链（拉通阅读）** | 左侧导航第二项 | 由原文箭头链条句**逐字**汇总，按「文档层级 → 文档 → 行号」机械排序，附缺口断点清单 |
| **展开链讲稿（撰述）** | 左侧导航第三项起 | `一体化研究/展开链讲稿/` 的作者叙述稿：问题 → 最小内核 → 六步链条 → 量纲链 → 断点 → 数值地位；每条论断带锚点（文档＋章节＋核对状态），附录含「引文保真六关」自检。**讲稿是撰写，不是摘录**；它不进引用清单、不计入理论语料统计，正文逐字原样复制 |
| **深度滑杆** | 讲稿页顶部（粘性条） | 同一批论断的**四种高度**：导读（1）／概念（2）／链条（3）／技术（4）；按二级章节分层（映射在 `assets/cqm-depth.js`），切换即隐藏更深块并给出「本页 N 块 · 显示 M 块」计数；**断点块在任何深度都显示**（测到「断点／缺口／未闭合／待证明／构造后验」等词即固定可见，并加左侧标记）；选择记入浏览器本地 |
| 被引用（反链） | 每页页尾 | 由站内链接倒排得到 |
| **可视化（总入口）** | 左侧「可视化」栏目 | 原分散的四件自包含可视化已收进本站：**可推演超图**（Cytoscape，含随包 `cytoscape.min.js`）、**研究驾驶舱**（9 面板 + 内联 SVG）、**检索台**（图谱 + 全文 BM25 + 证据复核 + SPARQL）、**形式化蓝图**；均以 iframe 内嵌于 `assets/viz/`，源文件仍留在 `10_展示可视化/` 各目录，构建期复制并改写其相对引用，**不改源文件** |

## 口径

- 本目录是**呈现层**，不是权威源；权威源仍是各理论文档原文与 `README.md`。
- 卡片、展开链页中的文字一律**逐字**取自既有产物（概念表、缺口编号对照、命题表、符号对照表、证据映射），
  构建脚本不改写任何表述；缺口状态、限定语原样保留。
- 展开链的箭头含义由各原文自行界定，站点不做统一解释。
- 讲稿页是**撰述文字**（作者叙述），其每一条论断由讲稿附录 A 的锚点表指向出处；锚点表中标注「待逐字核对」的，
  表示定位来自索引行、尚未回到原文逐字校对，读时应按此状态对待。

## 重建

```bash
python "08 理论组织和形式化框架/_build/build_reader_site.py"
```
"""


if __name__ == "__main__":
    main()
