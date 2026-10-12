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
    "05 方法论与批判", "06 超导", "07 精细引力（FG）", "一体化研究/附录",
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
extra_javascript:
  - assets/backlinks.js             # 构建期生成：被引用数据
  - assets/backlink-inject.js       # 页尾注入「被引用」区块
  - assets/math-config.js
  - assets/tex-svg.js
nav:
{nav}
"""
    with io.open(CONF, "w", encoding="utf-8", newline="\n") as f:
        f.write(yml)


def build_nav(staged_map):
    lines = ["  - 首页: index.md"]
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
    n_docs = len(staged_map)
    # 旧站资产在 stage 前需先备份 tex-svg（TEX_SVG 指向旧站目录，stage 不清站点目录）
    site_dir = SITE.replace(os.sep, "/")
    write_config(build_nav(staged_map), site_dir)
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
    print(f"[OK] 阅读站：{len(files)} 个文件 / index.html {os.path.getsize(idx) if os.path.exists(idx) else 0:,} B")
    if r.returncode != 0:
        print(out[-2500:])
        sys.exit(1)


if __name__ == "__main__":
    main()
