#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建 VitePress 版 CQM 研究站（与 Material 阅读站并行）。

复用 build_reader_site.py 已经 staged 到 _build/mkdocs_src/docs 的 markdown，
转成 VitePress 的 docs/ + .vitepress/config.mts，产出真正由 VitePress v1.6.4
生成的静态站（验收点：<meta name="generator" content="VitePress v1.6.4">，
观感为顶部导航 + 左侧分组侧栏 + 右侧大纲 + 品牌靛蓝 #3451b2 + 首页 hero/特性卡）。
"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT08 = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MK_SRC = os.path.join(ROOT08, "_build", "mkdocs_src", "docs")
VP_ROOT = os.path.join(ROOT08, "10_展示可视化", "阅读站VitePress")
VP_DOCS = os.path.join(VP_ROOT, "docs")
VP_PUBLIC = os.path.join(VP_DOCS, "public")
VP_CFG_DIR = os.path.join(VP_ROOT, ".vitepress")

NODE_DIR = r"C:/Users/13649/.workbuddy/binaries/node/versions/22.22.2-6"
NODE = os.path.join(NODE_DIR, "node.exe")
VITEPRESS_BIN = os.path.join(VP_ROOT, "node_modules", "vitepress", "bin", "vitepress.js")

for d in (VP_DOCS, VP_PUBLIC, VP_CFG_DIR):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- 1. 复制 markdown
assert os.path.isdir(MK_SRC), "staged 源不存在：%s（请先运行 build_reader_site.py）" % MK_SRC
md_files = sorted(f for f in os.listdir(MK_SRC) if f.endswith(".md"))
assert md_files, "staged 源里没有 md 文件"

# ---------------------------------------------------------------- 数学保护（构建期占位符）
# 为什么不能只靠 markdown-it 规则：VitePress 把 markdown-it 打包进自身 bundle，
# 拿到的插件实例行为不可控，实测公式里的 \\（LaTeX 换行）会被转义规则吃成
# <span>\</span>、_ 会被强调规则吃成 <em>，标签一旦插进公式，MathJax 就再也
# 匹配不到这对 $ 定界符，公式只能以 LaTeX 原文裸露。
# 因此改在 markdown 解析「之前」把公式整段换成纯 ASCII 占位符，构建完成后
# 再在产物（HTML / JS）里还原：HTML 里做 HTML 转义，JS 字符串里做 JSON 转义。
MATH_RE = re.compile(
    r'(?<!\\)\$\$[\s\S]+?(?<!\\)\$\$'          # 块级 $$...$$（可跨行）
    r'|(?<!\\)\$(?!\$)(?:[^$\n]|\\\$)+?(?<!\\)\$(?!\$)'   # 行内 $...$（不跨行）
)
MATH_STORE = {}
HEADING_RE = re.compile(r'^\s{0,3}#{1,6}[ \t]')     # 标题行原样保留（锚点 id 不被占位符污染）


def protect_math(text):
    """逐段保护公式；标题行跳过（标题里的公式量少，交给 markdown-it 侧规则兜底）。"""
    lines = text.split("\n")
    out, buf = [], []

    def flush():
        if not buf:
            return
        seg = "\n".join(buf)
        buf.clear()

        def repl(m):
            key = "CQMMATHPLCHOLDER%dEND" % len(MATH_STORE)
            MATH_STORE[key] = m.group(0)
            return key

        out.append(MATH_RE.sub(repl, seg))

    for ln in lines:
        if HEADING_RE.match(ln):
            flush()
            out.append(ln)
        else:
            buf.append(ln)
    flush()
    return "\n".join(out)


MATH_MISSED = set()


def restore_math(text, js=False):
    """把产物里的占位符还原成公式原文。"""
    def repl(m):
        f = MATH_STORE.get(m.group(0))
        if f is None:
            MATH_MISSED.add(m.group(0))
            return m.group(0)
        return json.dumps(f, ensure_ascii=False)[1:-1] if js else html.escape(f, quote=False)

    return re.sub(r'CQMMATHPLCHOLDER\d+END', repl, text)


# ---------------------------------------------------------------- 站内 404 修复
# mkdocs_src 里的行内链接形如 [理论组织和形式化框架总览](./_src/08 .../README.html)——
# 那是 Material 站把所有源文档编译进 _src/ 后的地址。VitePress 不处理 '_' 前缀目录，
# 站内没有 _src/，于是这些链接全部 404。
# 站内本就有这些源文档的渲染版（F01/F02/…），故指过来；没有对应页面的（归档、
# LICENSE、元数据等）降级为纯文本，不留死链。
SRC_LINK_MAP = {
    "_src/08 理论组织和形式化框架/README": "/F02_README",
    "_src/08 理论组织和形式化框架/AGENTS": "/F01_AGENTS",
}
SRC_LINK_RE = re.compile(r'\[([^\]\n]+)\]\((\.?/?_src/[^)\s]+?)(\.html)?(#[^)]*)?\)')


def fix_src_links(txt):
    def repl(m):
        text, base, _ext, _anchor = m.group(1), m.group(2), m.group(3), m.group(4)
        key = base.lstrip("./")
        for prefix, target in SRC_LINK_MAP.items():
            if key.startswith(prefix):
                return "[%s](%s)" % (text, target)
        return text          # 无对应站内页面 → 去掉链接，保留文字

    return SRC_LINK_RE.sub(repl, txt)


# ---------------------------------------------------------------- 中文强调修复
# CommonMark 的强调 flanking 判定在中文标点处会误判：**“存在论相变”** 里，
# 左 ** 的右侧是“（标点）、左侧是汉字，被判为「不是左 flanking」而不能开强调；
# **可观察子群（observable subgroup）**问题 里，右 ** 的左侧是）（标点）、
# 右侧是汉字，同样不能闭。于是这些成对的 ** 被原样保留（实测 18 处）。
# Material 时代的 Python-Markdown 规则宽松，故此前不显。
# 处理：逐行把成对的 **…** 提前落成 <strong>…</strong>；跳过代码围栏，行内代码
# 先取走再放回，避免误伤。
FENCE_RE = re.compile(r'^\s*(?:```|~~~)')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')
BOLD_RE = re.compile(r'\*\*(?=\S)([^*\n]{1,300}?)(?<=\S)\*\*')
# 裸文本下标：U(1)_B、U(1)_{B-L}、G_N、K_L、A_4 这类没有写进 $…$ 的下标记号，
# 只要同段出现两个就会被 markdown-it 当斜体开闭配对，实测把
# 「U(1)_B、U(1)_B-L、U(1)_Y」渲染成「U(1)<em>B、U(1)</em>B-L、U(1)_Y」。
# 给这类下划线加反斜杠转义，输出仍是字面下划线，视觉不变。
BARE_SUB_RE = re.compile(r'(?<=[A-Za-z0-9)\]}])_(?=[A-Za-z0-9({])')


def fix_cjk_bold(txt):
    lines = txt.split("\n")
    out, in_fence = [], False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        codes = []

        def stash(m):
            codes.append(m.group(0))
            return "\x01C%d\x01" % (len(codes) - 1)

        ln2 = INLINE_CODE_RE.sub(stash, ln)
        ln2 = BOLD_RE.sub(lambda m: "<strong>%s</strong>" % m.group(1), ln2)
        ln2 = BARE_SUB_RE.sub(lambda m: "\\_", ln2)     # 裸下标：转义 _ 而非配成斜体
        for i, c in enumerate(codes):
            ln2 = ln2.replace("\x01C%d\x01" % i, c)
        out.append(ln2)
    return "\n".join(out)


def wrap_vpre(txt):
    """把正文整体放进 <div v-pre>，避免正文里的 {{ }} 被 Vue 当成插值编译。

    VitePress 会把 markdown 编译成 Vue SFC；物理文档里出现 {{ / }} 或 \\u 序列时
    会被 @vue/compiler-core 解析报错（曾试过把 {{ }} 转 HTML 实体，但源文本里
    还有 \\{\\{ 之类的写法，实体替换覆盖不全，仍会报 "Interpolation end sign
    was not found"）。整页 v-pre 是唯一能彻底关闭插值编译的办法。

    代价：所有 h2/h3/p 会变成 .vp-doc 的孙节点而非直接子块。因此增强脚本里的
    contentRoot() 会逐层下潜到真正承载标题的容器，深度滑杆才能正常按块工作。
    若文件带 YAML frontmatter，则保留 frontmatter，只包裹正文。
    """
    lines = txt.split("\n")
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            fm = "\n".join(lines[:end + 1])
            body = "\n".join(lines[end + 1:])
            return fm + "\n\n<div v-pre>\n\n" + body + "\n\n</div>\n"
    return "<div v-pre>\n\n" + txt + "\n\n</div>\n"


wrapped = 0
for f in md_files:
    with open(os.path.join(MK_SRC, f), "r", encoding="utf-8") as fh:
        txt = fh.read()
    # VitePress 的静态资源根是 public/，viz 从 assets/viz/ 迁到 /viz/
    txt = txt.replace("assets/viz/", "/viz/")
    txt = fix_src_links(txt)         # 消除指向 _src/ 的失效链接
    if f != "index.md":
        txt = protect_math(txt)      # 公式先换成占位符，躲开 markdown-it
        txt = fix_cjk_bold(txt)      # 中文标点旁的 **…** 落成 <strong>…</strong>
        txt = wrap_vpre(txt)
        wrapped += 1
    with open(os.path.join(VP_DOCS, f), "w", encoding="utf-8") as fh:
        fh.write(txt)
print("[vp] 已复制 %d 个 markdown 页面（其中 %d 页套 v-pre）" % (len(md_files), wrapped))

# ---------------------------------------------------------------- 2. 静态资源 -> public/
mk_assets = os.path.join(MK_SRC, "assets")
if os.path.isdir(mk_assets):
    for name in os.listdir(mk_assets):
        s = os.path.join(mk_assets, name)
        d = os.path.join(VP_PUBLIC, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print("[vp] 已复制静态资源（含 viz/）到 public/")
else:
    print("[vp] 警告：未找到 %s，viz iframe 可能失效" % mk_assets)

# viz 内 HTML 的相对资源引用改写（只改 public/ 下的副本，源文件不动）：
#   源 HTML 写 assets/cytoscape.min.js，但 public/viz/ 下依赖是平铺的
#   （cytoscape.min.js / 驾驶舱数据.json），不改写会 404 → 超图页空白。
VIZ_FIX = (
    ('src="assets/cytoscape.min.js"', 'src="cytoscape.min.js"'),
    ("src='assets/cytoscape.min.js'", "src='cytoscape.min.js'"),
    ('href="assets/cytoscape.min.js"', 'href="cytoscape.min.js"'),
    ('src="data.json"', 'src="驾驶舱数据.json"'),
    ('"data.json"', '"驾驶舱数据.json"'),
)
viz_dir = os.path.join(VP_PUBLIC, "viz")
viz_fixed = 0
if os.path.isdir(viz_dir):
    for name in os.listdir(viz_dir):
        if not name.lower().endswith(".html"):
            continue
        p = os.path.join(viz_dir, name)
        with open(p, "r", encoding="utf-8") as fh:
            txt = fh.read()
        before = txt
        for a, b in VIZ_FIX:
            txt = txt.replace(a, b)
        if txt != before:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(txt)
            viz_fixed += 1
print("[vp] viz 资源引用改写：%d 个 HTML 被修正" % viz_fixed)

# ---------------------------------------------------------------- 3. 品牌色覆盖
BRAND_CSS = """/* CQM 研究站：对齐参考站 VitePress 观感，品牌色靛蓝 #3451b2 */
:root {
  --vp-c-brand: #3451b2;
  --vp-c-brand-light: #4662c4;
  --vp-c-brand-lighter: #5573d6;
  --vp-c-brand-dark: #2c4395;
  --vp-c-brand-darker: #22347a;
  --vp-c-brand-1: #3451b2;
  --vp-c-brand-2: #4662c4;
  --vp-c-brand-3: #5573d6;
  --vp-c-brand-soft: rgba(52, 81, 178, 0.14);
}
.dark {
  --vp-c-brand-1: #5c74d8;
  --vp-c-brand-2: #6d84e2;
  --vp-c-brand-3: #7e94ec;
  --vp-c-brand-soft: rgba(92, 116, 216, 0.16);
}
"""
with open(os.path.join(VP_PUBLIC, "vp-brand.css"), "w", encoding="utf-8") as fh:
    fh.write(BRAND_CSS)

# ------------------------------------------------- 3b. 本地 MathJax（$ / $$，离线）
# 正文公式是 $...$；这里不依赖 markdown-it-mathjax3（它会拉 CDN），
# 改用随站复制到 public/ 的本地 tex-svg.js，配置以 $ 为分隔符。
MATH_JS = """window.MathJax = {
  tex: { inlineMath: [['$', '$']], displayMath: [['$$', '$$']], processEscapes: true },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
};
"""
with open(os.path.join(VP_PUBLIC, "vp-math.js"), "w", encoding="utf-8") as fh:
    fh.write(MATH_JS)

# ------------------------------------------------- 3c. VitePress 版交互增强
# 与 Material 版（cqm-enhance.js）同源，但适配 VitePress：
#   正文容器 .vp-doc（原 article.md-content__inner）
#   导航容器 .VPNavBar（原 .md-header__inner）
#   快捷键 Ctrl+Shift+K（避开 VitePress 自带搜索的 Ctrl+K）
#   拆成 initOnce（全局单例：弹卡/检索框/快捷键/导航按钮/探测徽标）
#   与 initPage（每页：术语标注 + 深度滑杆），由 theme/index.js 在路由切换后重跑。
VP_ENHANCE_JS = r'''(function () {
  var G = window.CQM_GLOSSARY; if (!G) return;
  var POP, cur = null, pinned = false;
  var BOX, MASK, INP, RES, SEL = 0, F = { ty: "", q: "" };
  var bound = false;

  /* ---------- 悬浮卡（全局单例） ---------- */
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

  /* ---------- 正文容器定位 ---------- */
  /* 构建期为避开 Vue 插值，整页被 <div v-pre> 包住：h2/h3/p 成了 .vp-doc 的孙节点。
     initDepth() 必须遍历「直接子块」才能按块切深度，故逐层下潜到真正承载标题的容器。 */
  function contentRoot() {
    var el = document.querySelector(".vp-doc");
    if (!el) return null;
    var guard = 0;
    while (guard++ < 5) {
      if (el.children.length !== 1) break;
      var c = el.children[0];
      if ((c.tagName || "").toLowerCase() !== "div") break;
      if (!c.querySelector("h1,h2,h3")) break;
      el = c;
    }
    return el;
  }

  /* ---------- 术语标注（每页执行；先还原再重标，避免重复嵌套） ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var keys = (G.termKeys || []).slice().sort(function (a, b) { return b.length - a.length; });
  function inSkip(n) {
    var p = n.parentNode; if (!p || !p.nodeName) return true;
    var tag = p.nodeName.toLowerCase();
    // 标题、代码、以及 MathJax 排版产物（mtext/mi/mo… 里带着公式原文，
    // 一旦被术语标注替换成 span，公式就被切碎，MathJax 再也匹配不到）
    if (/^(a|code|pre|script|style|textarea|button|summary|th|caption|dt|h1|h2|h3|h4|h5|h6|mjx-container|mjx-assistive-mml|math|svg|mrow|mtext|mi|mo|mn|ms|mtd|mtr|mtable)$/.test(tag)) return true;
    if (p.closest && p.closest(".cqm-pop,.cqm-search,.VPNavBar,.VPSidebar,.VPDocAsideOutline,.VPNav,.VPLocalSearchBox,mjx-container")) return true;
    return false;
  }
  // 公式区间：术语标注必须避开 $...$ / $$...$$ 内部，否则 \text{中文} 里的
  // 中文术语会被包成 span，把公式文本切碎，MathJax 就无法再匹配定界符。
  var MATH_RE = /\$\$[\s\S]*?\$\$|\$[^$\n]*?\$/g;
  function mathRanges(txt) {
    var rs = [], m; MATH_RE.lastIndex = 0;
    while ((m = MATH_RE.exec(txt))) rs.push([m.index, m.index + m[0].length]);
    return rs;
  }
  function inMath(pos, rs) {
    for (var i = 0; i < rs.length; i++) if (pos >= rs[i][0] && pos < rs[i][1]) return true;
    return false;
  }
  function unwrap(root) {
    if (!root) return;
    var spans = root.querySelectorAll("span.cqm-term");
    for (var i = 0; i < spans.length; i++) {
      var s = spans[i];
      s.parentNode.replaceChild(document.createTextNode(s.textContent), s);
    }
  }
  function runTerms() {
    if (!keys.length) return;
    var art = contentRoot();
    if (!art) return;
    unwrap(art);
    var re = new RegExp(keys.map(function (k) { return k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }).join("|"), "g");
    var used = {}, total = 0, MAX = 240, PER = 2;
    function wrap(node) {
      if (inSkip(node) || !node.nodeValue || node.nodeValue.trim().length < 2) return;
      var txt = node.nodeValue, frag = null, last = 0, m; re.lastIndex = 0;
      var rs = mathRanges(txt);
      while ((m = re.exec(txt))) {
        var k = m[0]; if (!G.terms[k]) continue;
        if (rs.length && inMath(m.index, rs)) continue;   // 不进入公式内部
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
    var w = document.createTreeWalker(art, NodeFilter.SHOW_TEXT, null);
    var nodes = []; while (w.nextNode()) nodes.push(w.currentNode);
    nodes.forEach(wrap);
  }

  /* ---------- 高级检索（全局单例） ---------- */
  var IDX = G.index || [];
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
    SEL = 0; RES.innerHTML = "";
    if (!top.length) {
      RES.innerHTML = '<div class="cqm-res__it"><div class="cqm-res__tt">无匹配</div>' +
        '<div class="cqm-res__sb">可放宽分类；VitePress 自带全文检索用 Ctrl+K，本框为结构化实体检索（Ctrl+Shift+K 调出）。</div></div>';
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
  function bindKeys() {
    document.addEventListener("keydown", function (e) {
      if ((e.key === "K" || e.key === "k") && (e.ctrlKey || e.metaKey) && e.shiftKey) { e.preventDefault(); openBox(); return; }
      if (!BOX || BOX.style.display === "none") return;
      if (e.key === "Escape") close();
      else if (e.key === "ArrowDown") { e.preventDefault(); sel(SEL + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); sel(SEL - 1); }
      else if (e.key === "Enter") { e.preventDefault(); open(SEL); }
    });
  }

  /* ---------- 导航按钮 + 服务探测（全局单例；挂在 VitePress 顶栏） ---------- */
  function navHost() {
    return document.querySelector(".VPNavBar .VPNavBarMenu") || document.querySelector(".VPNavBar");
  }
  function mountNav() {
    var hdr = navHost(); if (!hdr) return;
    // 注意：判定「是否已挂载」必须用本按钮专属的 class。服务徽标也带 .cqm-sbtn，
    // 而它由 fetch 异步插入，先到时会顶掉这个判定，导致高级检索按钮永远不出现。
    if (hdr.querySelector(".cqm-advbtn")) return;
    var b = document.createElement("button");
    b.className = "cqm-sbtn cqm-advbtn"; b.type = "button";
    b.innerHTML = '高级检索 <span class="cqm-kbd">Ctrl</span><span class="cqm-kbd">Shift</span><span class="cqm-kbd">K</span>';
    b.addEventListener("click", openBox);
    hdr.appendChild(b);
  }
  function probeService() {
    try {
      fetch("api/status", { cache: "no-store" }).then(function (r) { return r.json(); }).then(function (s) {
        var hdr = navHost(); if (!hdr || !s || !s.counts) return;
        if (hdr.querySelector(".cqm-badge")) return;
        var a = document.createElement("a");
        a.className = "cqm-sbtn cqm-badge"; a.href = "api";
        a.title = "本地研究站服务已连接：实时 SPARQL / 结构化检索 / 证据复核写回";
        a.innerHTML = "服务已连接 · 概念 " + s.counts.concepts + " · 缺口 " + s.counts.gaps
          + " · 待复核 " + (s.review ? s.review.pending : "-");
        hdr.appendChild(a);
      })["catch"](function () {});
    } catch (e) {}
  }

  /* ---------- 深度滑杆（每页执行） ---------- */
  function initDepth() {
    var D = window.CQM_DEPTH; if (!D) return;
    var m = /(^|\/)(L\d{3})_/.exec(location.pathname);
    if (!m || m[2] === "L000") return;
    var art = contentRoot(); if (!art) return;
    var old = art.querySelector(".cqm-depthbar"); if (old && old.parentNode) old.parentNode.removeChild(old);
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

  /* ---------- 初始化：一次性 + 每页 ---------- */
  function initOnce() {
    if (bound) return; bound = true;
    build();
    document.body.appendChild(BOX); document.body.appendChild(MASK);
    BOX.style.display = "none"; MASK.style.display = "none";
    bindKeys();
  }
  function initPage() {
    runTerms();
    initDepth();
    // 导航栏由 Vue 异步渲染：首次初始化时 .VPNavBarMenu 往往还不存在，
    // 若只挂一次就会整轮丢失（服务徽标因 fetch 延迟刚好躲过，曾掩盖此问题）。
    // 这里每次页面初始化都确保挂上，内部有幂等检查；再补一轮定时重试兜底。
    mountNav();
    probeService();
    if (!document.querySelector(".cqm-advbtn")) {
      var n = 0;
      var t = setInterval(function () {
        mountNav();
        if (document.querySelector(".cqm-advbtn") || ++n > 20) clearInterval(t);
      }, 200);
    }
  }
  window.CQM = { init: function () { initOnce(); initPage(); } };
  function boot() { window.CQM.init(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
'''

with open(os.path.join(VP_PUBLIC, "cqm-enhance-vp.js"), "w", encoding="utf-8") as fh:
    fh.write(VP_ENHANCE_JS)
print("[vp] 已写 VitePress 版增强脚本 public/cqm-enhance-vp.js")

# ------------------------------------------------- 3d. 自定义主题（接路由 hook）
# VitePress 是 SPA：路由切换后必须重跑 initPage（术语标注 + 深度滑杆）并重排公式。
THEME_JS = r'''import DefaultTheme from 'vitepress/theme'

/* 公式排版：VitePress 是 SPA，MathJax 只在文档加载时自动排版一次，
   之后「客户端路由切换」与「Vue 异步渲染的侧栏/大纲」都不会再排。
   这里在每次路由切换后主动 typeset，并对尚未就绪的 MathJax 做轮询重试。*/
function cqmTypeset(tries) {
  if (tries == null) tries = 10
  const MJ = window.MathJax
  if (!MJ || typeof MJ.typesetPromise !== 'function') {
    if (tries > 0) setTimeout(() => cqmTypeset(tries - 1), 200)
    return
  }
  const go = () => { try { MJ.typesetPromise() } catch (e) {} }
  if (MJ.startup && MJ.startup.promise) MJ.startup.promise.then(go, go)
  else go()
}

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    if (typeof window === 'undefined') return
    const run = () => {
      // 等两帧，确保新页面的 .vp-doc 已挂载
      requestAnimationFrame(() => requestAnimationFrame(() => {
        try { window.CQM && window.CQM.init && window.CQM.init() } catch (e) {}
        cqmTypeset()
        // 侧栏与右侧大纲由 Vue 稍后渲染，再补排两次
        setTimeout(() => cqmTypeset(0), 150)
        setTimeout(() => cqmTypeset(0), 500)
      }))
    }
    run()
    router.onAfterRouteChanged = run
  }
}
'''

theme_dir = os.path.join(VP_CFG_DIR, "theme")
os.makedirs(theme_dir, exist_ok=True)
with open(os.path.join(theme_dir, "index.js"), "w", encoding="utf-8") as fh:
    fh.write(THEME_JS)
print("[vp] 已写自定义主题 .vitepress/theme/index.js（路由切换后重跑增强）")

# ---------------------------------------------------------------- 4. 首页（VitePress home 布局）
HOME_MD = """---
layout: home

hero:
  name: "CQM"
  text: "耦合常数量子力学研究站"
  tagline: 组织层 · 证据层 · 主张层 · 知识图谱 · 形式化验证
  actions:
    - theme: brand
      text: 理论展开链
      link: /L000_展开链
    - theme: alt
      text: 讲稿（第一分册）
      link: /L001_第一分册_从问题到链条

features:
  - title: 结构化数据（唯一源）
    details: 概念 82 · 命题 63 · 论证 70 · 缺口 24
  - title: 知识图谱与 SPARQL
    details: 145 实体 / 359 边；在线只读 SPARQL（Jena 内存模型）
  - title: 证据层
    details: 215 条断言，逐字引文 + 字符区间可回溯
  - title: 形式化验证
    details: Lean 覆盖 41/82 概念；SHACL / HermiT 一致性通过
---
"""
with open(os.path.join(VP_DOCS, "index.md"), "w", encoding="utf-8") as fh:
    fh.write(HOME_MD)


# ---------------------------------------------------------------- 5. 导航/侧栏（按文件名分组）
def md_title(path, fallback):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^#\s+(.+?)\s*$", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return fallback


overview, lect, viz, other = [], [], [], []
for f in md_files:
    if f == "index.md":
        continue
    base = os.path.splitext(f)[0]
    item = {"text": md_title(os.path.join(VP_DOCS, f), base), "link": "/" + base}
    if f.startswith("L000"):
        overview.append(item)
    elif f.startswith("L"):
        lect.append(item)
    elif f.startswith("V"):
        viz.append(item)
    else:
        other.append(item)

sidebar = []
if overview:
    sidebar.append({"text": "展开链", "items": overview})
if lect:
    sidebar.append({"text": "讲稿", "items": lect})
if viz:
    sidebar.append({"text": "可视化", "items": viz})
if other:
    sidebar.append({"text": "结构化与参考", "items": other})

nav = [{"text": "首页", "link": "/"}]
if overview:
    nav.append({"text": "展开链", "link": overview[0]["link"]})
if lect:
    nav.append({"text": "讲稿", "link": lect[0]["link"]})
if viz:
    nav.append({"text": "可视化", "link": viz[0]["link"]})
nav.append({"text": "检索台", "link": "/V003_检索台"})

CONFIG_MTS = """import { defineConfig } from 'vitepress'

// 中文检索分词：minisearch 默认把连续的 CJK 当一个词，中文查询几乎命中不了。
// 这里按「单字 + 二元」切分中文、按词切分拉丁；索引与查询共用同一 tokenize。
const cqmTokenize = (text) => {
  const out = []
  const re = /[\\u4e00-\\u9fff]+|[A-Za-z0-9_\\-]+/g
  let m
  while ((m = re.exec(text))) {
    const s = m[0]
    if (/^[\\u4e00-\\u9fff]+$/.test(s)) {
      for (let i = 0; i < s.length; i++) {
        out.push(s[i])
        if (i + 1 < s.length) out.push(s.slice(i, i + 2))
      }
    } else {
      out.push(s.toLowerCase())
    }
  }
  return out
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'CQM 研究站',
  description: '耦合常数量子力学（CQM）组织层研究站：结构化数据 · 知识图谱 · 证据层 · 形式化验证',
  srcDir: 'docs',
  outDir: '.vitepress/dist',
  // 死链不再放行：站内 404 已清零（见 fix_src_links），让构建自己当验证器——
  // 一旦再引入失效链接，构建会直接失败并点名文件与目标。
  ignoreDeadLinks: false,
  // 数学保护：VitePress 默认没有数学插件，markdown-it 会先按普通文本解析，
  // 于是公式里的 _ / * 被当成强调语法，例如 $$\\mathbb{R}_{>0}$$ 被解析成
  // "\\mathbb{R}<em>{>0}</em>"——标签一旦插入，MathJax 就无法再匹配这对
  // 定界符，该公式只能以 LaTeX 原文裸露在页面上。
  // 这里在 emphasis 规则之前插入一条规则，把 $...$ / $$...$$ 整段取出、
  // 原样输出（只做 HTML 转义，不改内容），再由页面上的 MathJax 排版。
  markdown: {
    config(md) {
      const DOLLAR = 0x24, BACKSLASH = 0x5c
      const isDollar = (c) => c === DOLLAR
      const isEscaped = (src, i) => i > 0 && src.charCodeAt(i - 1) === BACKSLASH
      const escHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

      // 注意：不要替换 markdown-it 的 text 规则。它的终止字符表本来就有 '$'
      // （连同星号、下划线、波浪号等 22 个），曾误以为缺 '$' 而自行重写，
      // 结果漏抄星号等下划线等，导致加粗与斜体语法全被 text 规则整段吞掉
      // （实测 6 113 处加粗字面未解析）。此处只用下面的 cqm_math 规则，
      // 它的注册位置在 emphasis 之前，足以整段接管 $…$。
      md.inline.ruler.before('emphasis', 'cqm_math', function (state, silent) {
        const src = state.src, start = state.pos, max = state.posMax
        if (!isDollar(src.charCodeAt(start)) || isEscaped(src, start)) return false
        const block = (start + 1 < max) && isDollar(src.charCodeAt(start + 1))
        const openLen = block ? 2 : 1
        let pos = start + openLen, close = -1
        while (pos < max) {
          const c = src.charCodeAt(pos)
          if (c === BACKSLASH) { pos += 2; continue }
          if (isDollar(c)) {
            if (block) {
              if (pos + 1 < max && isDollar(src.charCodeAt(pos + 1))) { close = pos; break }
            } else if (!isEscaped(src, pos)) { close = pos; break }
          }
          pos++
        }
        if (close < 0 || close === start + openLen) return false
        if (!silent) {
          const token = state.push('cqm_math', 'math', 0)
          token.content = src.slice(start, close + openLen)
        }
        state.pos = close + openLen
        return true
      })

      md.renderer.rules.cqm_math = (tokens, idx) => escHtml(tokens[idx].content)
    }
  },
  head: [
    ['link', { rel: 'stylesheet', href: '/vp-brand.css' }],
    ['link', { rel: 'stylesheet', href: '/stylesheets/cqm-enhance.css' }],
    ['script', { src: '/cqm-glossary.js' }],
    ['script', { src: '/cqm-depth.js' }],
    ['script', { src: '/cqm-enhance-vp.js' }],
    ['script', { src: '/vp-math.js' }],
    ['script', { src: '/tex-svg.js', async: true }]
  ],
  themeConfig: {
    nav: %s,
    sidebar: %s,
    // 内置全文搜索（VitePress 官方 local provider）：构建期生成索引，离线可用；
    // Ctrl/⌘+K 唤起，导航栏出现搜索按钮。索引走 fetch，需经 HTTP 访问。
    search: {
      provider: 'local',
      options: {
        detailedView: true,
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索文档' },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清除查询条件',
            backButtonTitle: '返回',
            noResultsText: '未找到相关结果',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '回车',
              navigateText: '切换',
              navigateUpKeyAriaLabel: '上箭头',
              navigateDownKeyAriaLabel: '下箭头',
              closeText: '关闭',
              closeKeyAriaLabel: 'Esc'
            }
          }
        },
        miniSearch: {
          options: { tokenize: cqmTokenize },
          searchOptions: { fuzzy: 0.2, prefix: true, boost: { title: 4, text: 2 } }
        }
      }
    },
    outline: [2, 3],
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: false
  },
})
""" % (json.dumps(nav, ensure_ascii=False, indent=2),
       json.dumps(sidebar, ensure_ascii=False, indent=2))

with open(os.path.join(VP_CFG_DIR, "config.mts"), "w", encoding="utf-8") as fh:
    fh.write(CONFIG_MTS)
print("[vp] 已生成 .vitepress/config.mts（nav=%d 项，sidebar=%d 组）" % (len(nav), len(sidebar)))

# ---------------------------------------------------------------- 6. vitepress build
if not os.path.isfile(VITEPRESS_BIN):
    sys.exit("[vp] 未找到 vitepress：%s —— 请先在阅读站VitePress 目录 npm install" % VITEPRESS_BIN)

print("[vp] 开始 vitepress build ...")
subprocess.run([NODE, VITEPRESS_BIN, "build"], cwd=VP_ROOT, check=True)

dist = os.path.join(VP_CFG_DIR, "dist")
print("[vp] 构建完成，产物：%s" % dist)

# ---------------------------------------------------------------- 7. 还原数学占位符
# 产物里两类上下文要分别转义：
#   .html —— 文本节点，做 HTML 转义（& < >）
#   .js   —— Vue 渲染函数里的字符串字面量，做 JSON 转义（\ " 换行）
restored = 0
if MATH_STORE:
    for dp, dns, fns in os.walk(dist):
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".html", ".js", ".json"):
                continue   # .json 里是结构化数据（本地检索索引），按 JSON 转义还原
            p = os.path.join(dp, fn)
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    txt = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            if "CQMMATHPLCHOLDER" not in txt:
                continue
            new = restore_math(txt, js=(ext in (".js", ".json")))
            if new != txt:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new)
                restored += 1
print("[vp] 数学保护：%d 处公式入占位 → %d 个产物文件已还原" % (len(MATH_STORE), restored))

index_html = os.path.join(dist, "index.html")
if os.path.isfile(index_html):
    with open(index_html, "r", encoding="utf-8") as fh:
        head = fh.read(4000)
    m = re.search(r'name="generator"\s+content="([^"]+)"', head)
    print("[vp] generator = %s" % (m.group(1) if m else "未找到（异常）"))
