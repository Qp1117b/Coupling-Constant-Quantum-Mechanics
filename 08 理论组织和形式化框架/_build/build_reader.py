# -*- coding: utf-8 -*-
"""
维度7（核心） · 展示可视化 · 离线阅读站

把理论文本（README + 01–07 各主题文档 + 一体化研究/附录）打包为**自包含、离线可用、无 CDN 依赖**
的单页阅读站：侧栏目录树 + 全文搜索 + 文档内跳转 + 反链（构建期解析文档间引用得到）+ 公式渲染。

与 `build_site.py` 的分工：`build_site.py` 的产物由 `01_结构化数据/*.csv` 派生（源 CSV 闭环）；
本脚本的产物由 01–07 理论文本派生，**不进入源 CSV 闭环**，也不修改任何理论文本（只读取）。

产出：
  10_展示可视化/阅读站/index.html          （含内嵌语料，file:// 可直接打开）
  10_展示可视化/阅读站/app.js              （渲染/搜索/路由）
  10_展示可视化/阅读站/assets/marked.min.js（Markdown 渲染，随包）
  10_展示可视化/阅读站/assets/tex-svg.js   （MathJax TeX→SVG，随包）
运行：python build_reader.py
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT08 = os.path.dirname(HERE)
ROOT = os.path.dirname(ROOT08)
SITE = os.path.join(ROOT08, "10_展示可视化", "阅读站")
ASSETS = os.path.join(SITE, "assets")
REF_YAML = os.path.join(ROOT08, "00_外部引用", "引用清单.yaml")

INCLUDE_DIRS = [
    "01 核心理论",
    "02 量子引力",
    "03 引力与退相干",
    "04 前沿研究",
    "05 方法论与批判",
    "06 超导",
    "07 精细引力（FG）",
    "一体化研究/附录",
]
_DOC_RE = re.compile(
    r"-\s*\{id:\s*(D\d+),\s*path:\s*([^,]+),\s*title:\s*([^,]+),\s*layer:\s*(\d+),\s*type:\s*([^}]+)\}"
)


def read(p, enc="utf-8"):
    with open(p, "r", encoding=enc) as f:
        return f.read()


def doc_registry():
    reg = {}
    if os.path.isfile(REF_YAML):
        for m in _DOC_RE.finditer(read(REF_YAML)):
            reg[m.group(2).strip().replace("\\", "/")] = {
                "doc_id": m.group(1),
                "title": m.group(3).strip(),
                "layer": int(m.group(4)),
                "type": m.group(5).strip(),
            }
    return reg


def first_heading(text, fallback):
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return fallback


def collect():
    paths = []
    if os.path.isfile(os.path.join(ROOT, "README.md")):
        paths.append("README.md")
    for d in INCLUDE_DIRS:
        base = os.path.join(ROOT, d)
        for p in sorted(glob.glob(os.path.join(base, "**", "*.md"), recursive=True)):
            paths.append(os.path.relpath(p, ROOT).replace("\\", "/"))
    return paths


def rewrite_links(text, doc_dir, doc_index):
    """把 md 链接/图片改写为站内路由或相对站点的路径。"""

    def repl(m):
        target = m.group(1).strip()
        if not target or target.startswith(("http://", "https://", "mailto:", "file:", "#")):
            return m.group(0)
        anchor = ""
        if "#" in target:
            target, anchor = target.split("#", 1)
            anchor = "#" + anchor
        for c in (target, os.path.normpath(target)):
            abs_p = os.path.normpath(os.path.join(ROOT, doc_dir, c))
            if os.path.exists(abs_p):
                rel = os.path.relpath(abs_p, ROOT).replace("\\", "/")
                if rel in doc_index:
                    return "](#/doc/%s%s)" % (doc_index[rel], anchor)
                to_site = os.path.relpath(abs_p, SITE).replace("\\", "/")
                return "](%s%s)" % (to_site, anchor)
        return m.group(0)

    return re.sub(r"\]\(([^)]+)\)", repl, text)


def backlink_targets(text, doc_dir, doc_index):
    """构建期扫描：本文件对其它文档的引用（markdown 链接 + 反引号路径）。"""
    out = set()
    for m in re.finditer(r"\]\(([^)]+)\)", text):
        t = m.group(1).split("#")[0].strip()
        if not t or t.startswith(("http", "mailto:", "file:")):
            continue
        abs_p = os.path.normpath(os.path.join(ROOT, doc_dir, t))
        rel = os.path.relpath(abs_p, ROOT).replace("\\", "/")
        if rel in doc_index:
            out.add(doc_index[rel])
    for m in re.finditer(r"`([^`\n]+\.md)`", text):
        t = m.group(1).strip()
        for cand in (t, os.path.normpath(t)):
            rel = os.path.relpath(os.path.join(ROOT, cand), ROOT).replace("\\", "/")
            if rel in doc_index:
                out.add(doc_index[rel])
    return out


def group_of(path):
    if "/" in path:
        return path.split("/")[0]
    return "总览"


def build():
    reg = doc_registry()
    paths = collect()

    doc_index = {}
    for p in paths:
        info = reg.get(p)
        doc_index[p] = info["doc_id"] if info else ("F" + str(len(doc_index) + 1).zfill(3))

    docs = []
    out_links = {}
    for p in paths:
        abs_p = os.path.join(ROOT, p)
        text = read(abs_p)
        info = reg.get(p, {})
        title = info.get("title") or first_heading(text, os.path.basename(p)[:-3])
        doc_dir = os.path.dirname(p)
        rewritten = rewrite_links(text, doc_dir, doc_index)
        out_links[doc_index[p]] = backlink_targets(text, doc_dir, doc_index)
        docs.append(
            {
                "id": doc_index[p],
                "doc_id": info.get("doc_id", ""),
                "title": title,
                "path": p,
                "group": group_of(p),
                "layer": info.get("layer", ""),
                "type": info.get("type", ""),
                "text": rewritten,
            }
        )

    back = {d["id"]: [] for d in docs}
    for src, tgts in out_links.items():
        for t in tgts:
            if t != src:
                back.setdefault(t, []).append(src)
    for d in docs:
        d["backlinks"] = sorted(back.get(d["id"], []))
        d["outlinks"] = sorted(out_links.get(d["id"], []))

    groups = []
    for d in docs:
        if d["group"] not in groups:
            groups.append(d["group"])
    groups.sort(key=lambda g: (g == "总览", g))

    payload = {
        "generated_from": "README.md + 01–07 各主题文档 + 一体化研究/附录（只读）",
        "count": len(docs),
        "groups": groups,
        "docs": docs,
    }
    return payload


INDEX_HTML = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CQM 理论阅读站</title>
<link rel="stylesheet" href="app.css">
<script>
  window.MathJax = {
    tex: {inlineMath: [['$', '$'], ['\\\\(', '\\\\)']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]},
    options: {skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']},
    svg: {fontCache: 'global'},
    startup: {typeset: false}
  };
</script>
<script src="assets/marked.min.js"></script>
<script id="cqm-docs" type="application/json">__DOCS_JSON__</script>
</head>
<body>
<div id="layout">
  <aside id="sidebar">
    <div class="brand">
      <span class="brand-title">CQM 理论阅读站</span>
      <span class="brand-sub" id="doc-count"></span>
    </div>
    <div class="search-wrap">
      <input id="search" type="search" placeholder="全文搜索（概念 / 术语 / 公式片段）…" autocomplete="off">
      <div id="search-results" hidden></div>
    </div>
    <nav id="tree"></nav>
  </aside>
  <main id="main">
    <article id="doc"></article>
    <section id="backlinks"></section>
  </main>
</div>
<script src="assets/tex-svg.js" id="MathJax-script" async></script>
<script src="app.js"></script>
</body>
</html>
"""

APP_CSS = """* { box-sizing: border-box; }
:root {
  --bg: #ffffff; --fg: #1c1f24; --muted: #6b7280; --line: #e5e7eb;
  --panel: #f7f8fa; --accent: #2f6fed; --mark: #fff2a8;
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #14161a; --fg: #e6e8ec; --muted: #9aa3af; --line: #2a2f37;
          --panel: #191c21; --accent: #6ea8fe; --mark: #5a4a12; }
}
html, body { margin: 0; padding: 0; background: var(--bg); color: var(--fg);
  font-family: -apple-system, "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif; }
#layout { display: flex; min-height: 100vh; }
#sidebar { width: 320px; flex: 0 0 320px; border-right: 1px solid var(--line);
  background: var(--panel); position: sticky; top: 0; height: 100vh; overflow-y: auto; padding: 14px 12px; }
.brand { display: flex; flex-direction: column; margin-bottom: 10px; }
.brand-title { font-weight: 700; font-size: 16px; }
.brand-sub { color: var(--muted); font-size: 12px; }
.search-wrap { position: relative; margin-bottom: 10px; }
#search { width: 100%; padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px;
  background: var(--bg); color: var(--fg); font-size: 13px; }
#search-results { position: absolute; z-index: 20; left: 0; right: 0; top: 40px; max-height: 60vh;
  overflow-y: auto; background: var(--bg); border: 1px solid var(--line); border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0,0,0,.18); }
#search-results .hit { padding: 8px 10px; cursor: pointer; border-bottom: 1px solid var(--line); }
#search-results .hit:hover { background: var(--panel); }
#search-results .hit .t { font-size: 13px; font-weight: 600; }
#search-results .hit .s { font-size: 12px; color: var(--muted); margin-top: 2px;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
#search-results .empty { padding: 10px; color: var(--muted); font-size: 13px; }
#tree .group { margin: 10px 0 4px; font-size: 12px; color: var(--muted); font-weight: 700;
  letter-spacing: .04em; text-transform: none; }
#tree a { display: block; padding: 4px 8px; border-radius: 6px; color: var(--fg);
  text-decoration: none; font-size: 13px; line-height: 1.5; }
#tree a:hover { background: var(--bg); }
#tree a.active { background: var(--accent); color: #fff; }
#main { flex: 1; min-width: 0; padding: 28px 40px 80px; }
#doc { max-width: 900px; line-height: 1.75; font-size: 15px; }
#doc h1 { font-size: 26px; border-bottom: 2px solid var(--line); padding-bottom: 8px; }
#doc h2 { font-size: 21px; margin-top: 32px; border-bottom: 1px solid var(--line); padding-bottom: 5px; }
#doc h3 { font-size: 17px; margin-top: 24px; }
#doc a { color: var(--accent); }
#doc table { border-collapse: collapse; display: block; overflow-x: auto; max-width: 100%; margin: 12px 0; font-size: 13.5px; }
#doc th, #doc td { border: 1px solid var(--line); padding: 5px 9px; text-align: left; vertical-align: top; }
#doc th { background: var(--panel); }
#doc code { background: var(--panel); padding: 1px 5px; border-radius: 4px; font-size: 13px; }
#doc pre { background: var(--panel); padding: 12px; border-radius: 8px; overflow-x: auto; }
#doc pre code { background: none; padding: 0; }
#doc blockquote { margin: 12px 0; padding: 4px 14px; border-left: 3px solid var(--accent); color: var(--muted); }
#doc hr { border: none; border-top: 1px solid var(--line); margin: 26px 0; }
#doc img { max-width: 100%; }
#doc mark { background: var(--mark); color: inherit; }
.doc-meta { color: var(--muted); font-size: 12.5px; margin-bottom: 18px; }
#backlinks { max-width: 900px; margin-top: 48px; border-top: 1px solid var(--line); padding-top: 16px; }
#backlinks h3 { font-size: 14px; color: var(--muted); margin: 0 0 8px; }
#backlinks a { display: inline-block; margin: 0 10px 6px 0; font-size: 13px; color: var(--accent); }
#backlinks .none { color: var(--muted); font-size: 13px; }
mjx-container { overflow-x: auto; max-width: 100%; }
@media (max-width: 860px) {
  #layout { flex-direction: column; }
  #sidebar { width: 100%; flex: none; height: auto; position: static; }
  #main { padding: 18px; }
}
"""

APP_JS = """(function () {
  "use strict";
  var DATA = JSON.parse(document.getElementById("cqm-docs").textContent);
  var byId = {};
  var pathIndex = {};
  var baseIndex = {};
  var currentId = null;
  DATA.docs.forEach(function (d) {
    byId[d.id] = d;
    pathIndex[d.path] = d.id;
    var b = d.path.split("/").pop();
    (baseIndex[b] = baseIndex[b] || []).push(d.id);
  });
  document.getElementById("doc-count").textContent = DATA.count + " 篇 · 离线只读";

  marked.setOptions({ gfm: true, breaks: false });

  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function renderTree() {
    var nav = document.getElementById("tree");
    var html = "";
    DATA.groups.forEach(function (g) {
      html += '<div class="group">' + esc(g) + "</div>";
      DATA.docs.filter(function (d) { return d.group === g; }).forEach(function (d) {
        html += '<a href="#/doc/' + d.id + '" data-id="' + d.id + '">' + esc(d.title) + "</a>";
      });
    });
    nav.innerHTML = html;
  }

  function typeset(el, tries) {
    tries = tries || 0;
    if (window.MathJax && MathJax.typesetPromise) {
      MathJax.typesetPromise([el]).catch(function () {});
    } else if (tries < 100) {
      setTimeout(function () { typeset(el, tries + 1); }, 120);
    }
  }

  // 把文档中反引号形式的 `.md` 引用（项目主要引用约定）变为可点击站内链接
  function linkifyCodes(el) {
    el.querySelectorAll("code").forEach(function (c) {
      if (c.parentElement && c.parentElement.tagName === "PRE") return;
      var t = c.textContent.trim();
      var key = t.replace(/^\\.\\//, "").replace(/^\\//, "");
      var id = pathIndex[key];
      if (!id) {
        var bs = baseIndex[key.split("/").pop()];
        if (bs && bs.length === 1) id = bs[0];
      }
      if (!id || id === currentId) return;
      var a = document.createElement("a");
      a.href = "#/doc/" + id;
      a.title = byId[id].title;
      c.parentNode.insertBefore(a, c);
      a.appendChild(c);
    });
  }

  function openDoc(id) {
    var d = byId[id];
    if (!d) { d = DATA.docs[0]; id = d.id; }
    currentId = id;
    var art = document.getElementById("doc");
    art.innerHTML = marked.parse(d.text);
    var meta = '<div class="doc-meta">' + esc(d.path) +
      (d.doc_id ? " · " + d.doc_id : "") + (d.layer !== "" ? " · layer " + d.layer : "") + "</div>";
    art.insertAdjacentHTML("afterbegin", meta);
    linkifyCodes(art);

    var bl = document.getElementById("backlinks");
    var ids = (d.backlinks || []).filter(function (x) { return byId[x]; });
    if (ids.length) {
      bl.innerHTML = "<h3>被以下文档引用（反链）</h3>" + ids.map(function (x) {
        return '<a href="#/doc/' + x + '">' + esc(byId[x].title) + "</a>";
      }).join("");
    } else {
      bl.innerHTML = '<h3>被以下文档引用（反链）</h3><div class="none">无</div>';
    }

    document.querySelectorAll("#tree a").forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-id") === id);
    });
    window.scrollTo(0, 0);
    typeset(art);
    typeset(bl);
  }

  function route() {
    var m = /^#\\/doc\\/(.+)$/.exec(location.hash || "");
    openDoc(m ? decodeURIComponent(m[1]) : DATA.docs[0].id);
  }

  function search(q) {
    var box = document.getElementById("search-results");
    q = q.trim();
    if (!q) { box.hidden = true; box.innerHTML = ""; return; }
    var lq = q.toLowerCase();
    var hits = [];
    DATA.docs.forEach(function (d) {
      var t = d.text.toLowerCase();
      var i = t.indexOf(lq);
      if (i >= 0) hits.push({ d: d, i: i });
    });
    if (!hits.length) { box.hidden = false; box.innerHTML = '<div class="empty">无匹配</div>'; return; }
    box.innerHTML = hits.slice(0, 40).map(function (h) {
      var start = Math.max(0, h.i - 30);
      var snip = h.d.text.substr(start, 90).replace(/\\s+/g, " ");
      return '<div class="hit" data-id="' + h.d.id + '"><div class="t">' + esc(h.d.title) +
        '</div><div class="s">' + esc(snip) + "</div></div>";
    }).join("");
    box.hidden = false;
  }

  document.getElementById("search").addEventListener("input", function (e) { search(e.target.value); });
  document.getElementById("search-results").addEventListener("click", function (e) {
    var el = e.target.closest(".hit");
    if (!el) return;
    location.hash = "#/doc/" + el.getAttribute("data-id");
    document.getElementById("search-results").hidden = true;
    document.getElementById("search").value = "";
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".search-wrap")) document.getElementById("search-results").hidden = true;
  });
  window.addEventListener("hashchange", route);

  renderTree();
  route();
})();
"""


def write_outputs(payload):
    os.makedirs(ASSETS, exist_ok=True)
    docs_json = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
    html = INDEX_HTML.replace("__DOCS_JSON__", docs_json)
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(SITE, "app.js"), "w", encoding="utf-8") as f:
        f.write(APP_JS)
    with open(os.path.join(SITE, "app.css"), "w", encoding="utf-8") as f:
        f.write(APP_CSS)
    for name in ("marked.min.js", "tex-svg.js"):
        dst = os.path.join(ASSETS, name)
        if not os.path.isfile(dst):
            raise SystemExit(
                "缺少离线资源 %s；请先放入 10_展示可视化/阅读站/assets/（见 阅读站/README.md）" % name
            )


def main():
    payload = build()
    write_outputs(payload)
    total = sum(len(d["text"]) for d in payload["docs"])
    print("阅读站已生成：%s" % SITE)
    print("  文档 %d 篇，分组 %d 个，语料 %.0f KB" % (payload["count"], len(payload["groups"]), total / 1024))
    bl = sum(len(d["backlinks"]) for d in payload["docs"])
    print("  反链 %d 条" % bl)


if __name__ == "__main__":
    main()