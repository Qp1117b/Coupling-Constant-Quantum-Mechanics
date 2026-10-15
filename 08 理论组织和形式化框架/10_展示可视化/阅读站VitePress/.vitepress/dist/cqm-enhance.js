(function () {
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
    if (el) { e.preventDefault(); if (cur === el) hidePop(); else showPop(el); }
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
