#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建 VitePress 版 CQM 研究站（与 Material 阅读站并行）。

复用 build_reader_site.py 已经 staged 到 _build/mkdocs_src/docs 的 markdown，
转成 VitePress 的 docs/ + .vitepress/config.mts，产出真正由 VitePress v1.6.4
生成的静态站（验收点：<meta name="generator" content="VitePress v1.6.4">，
观感为顶部导航 + 左侧分组侧栏 + 右侧大纲 + 品牌靛蓝 #3451b2 + 首页 hero/特性卡）。
"""
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
    if f != "index.md":
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
    if (/^(a|code|pre|script|style|textarea|button|summary|th|caption|dt|h1|h2|h3|h4|h5|h6)$/.test(tag)) return true;
    if (p.closest && p.closest(".cqm-pop,.cqm-search,.VPNavBar,.VPSidebar,.VPDocAsideOutline,.VPNav,.VPLocalSearchBox")) return true;
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
    if (hdr.querySelector(".cqm-sbtn")) return;
    var b = document.createElement("button");
    b.className = "cqm-sbtn"; b.type = "button";
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
    mountNav();
    probeService();
  }
  function initPage() {
    runTerms();
    initDepth();
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

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    if (typeof window === 'undefined') return
    const run = () => {
      // 等两帧，确保新页面的 .vp-doc 已挂载
      requestAnimationFrame(() => requestAnimationFrame(() => {
        try { window.CQM && window.CQM.init && window.CQM.init() } catch (e) {}
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

export default defineConfig({
  lang: 'zh-CN',
  title: 'CQM 研究站',
  description: '耦合常数量子力学（CQM）组织层研究站：结构化数据 · 知识图谱 · 证据层 · 形式化验证',
  srcDir: 'docs',
  outDir: '.vitepress/dist',
  ignoreDeadLinks: true,
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
index_html = os.path.join(dist, "index.html")
if os.path.isfile(index_html):
    with open(index_html, "r", encoding="utf-8") as fh:
        head = fh.read(4000)
    m = re.search(r'name="generator"\s+content="([^"]+)"', head)
    print("[vp] generator = %s" % (m.group(1) if m else "未找到（异常）"))
