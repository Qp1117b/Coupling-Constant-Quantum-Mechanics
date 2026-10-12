(function () {
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
  /* 卡片文字来自结构化数据（CSV 原文），里面会带行内代码标记（如 Lean 的模块名）
     与 \(…\) 公式。公式交给 MathJax，反引号在这里落成 <code>。 */
  var ESC = { "&": "&amp;", "<": "&lt;", ">": "&gt;" };
  function cardHtml(html) {
    return String(html).replace(/`([^`\n]+)`/g, function (m, s) {
      return "<code>" + s.replace(/[&<>]/g, function (c) { return ESC[c]; }) + "</code>";
    });
  }
  function showPop(el) {
    var html = G.terms[el.getAttribute("data-cqm")];
    if (!html) return;
    var p = ensurePop();
    p.innerHTML = cardHtml(html); p.style.display = "block"; p.style.left = "-9999px"; p.style.top = "0";
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
    var used = {}, total = 0, MAX = 320, PER = 2;
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
  /* ---------- 搜索跳转后的关键词高亮 ----------
     点击搜索结果前把查询词存 sessionStorage，目标页加载后对正文文本节点
     打 <mark class="cqm-hl">（跳过代码/公式/已有标注），一次性使用。 */
  function applySearchHighlight() {
    var q = "";
    try { q = sessionStorage.getItem("cqm-hl") || ""; } catch (e) {}
    if (!q) return;
    try { sessionStorage.removeItem("cqm-hl"); } catch (e) {}
    var doc = contentRoot(); if (!doc) return;
    var words = q.split(/\s+/).filter(function (w) { return w.length >= 2; });
    if (!words.length) return;
    var re = new RegExp("(" + words.map(function (w) {
      return w.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    }).join("|") + ")", "gi");
    var walker = document.createTreeWalker(doc, NodeFilter.SHOW_TEXT, null);
    var nodes = [], n;
    while ((n = walker.nextNode())) {
      if (!n.nodeValue || !n.nodeValue.trim()) continue;
      var p = n.parentNode, tag = p.nodeName.toLowerCase();
      if (/^(code|pre|script|style|textarea|mark)$/.test(tag)) continue;
      if (p.closest && p.closest("mjx-container,.cqm-pop")) continue;
      nodes.push(n);
    }
    var count = 0;
    nodes.forEach(function (node) {
      if (count >= 200) return;
      var txt = node.nodeValue;
      re.lastIndex = 0;
      if (!re.test(txt)) { re.lastIndex = 0; return; }
      re.lastIndex = 0;
      var frag = document.createDocumentFragment(), last = 0, m;
      while ((m = re.exec(txt)) && count < 200) {
        if (m.index > last) frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var mk = document.createElement("mark");
        mk.className = "cqm-hl"; mk.textContent = m[0];
        frag.appendChild(mk);
        last = m.index + m[0].length; count++;
        re.lastIndex = 0;
      }
      if (last < txt.length) frag.appendChild(document.createTextNode(txt.slice(last)));
      if (node.parentNode) node.parentNode.replaceChild(frag, node);
    });
    if (count) {
      var first = doc.querySelector("mark.cqm-hl");
      if (first) { try { first.scrollIntoView({ block: "center" }); } catch (e) {} }
    }
  }
  document.addEventListener("click", function (e) {
    var hit = e.target.closest && e.target.closest(".VPLocalSearchBox a");
    if (!hit) return;
    var inp = document.querySelector(".VPLocalSearchBox input");
    if (inp && inp.value.trim()) {
      try { sessionStorage.setItem("cqm-hl", inp.value.trim()); } catch (err) {}
    }
    // 点到当前页自身时 SPA 不会触发路由回调，这里主动补一次高亮
    setTimeout(function () { if (window.CQM && window.CQM.highlight) window.CQM.highlight(); }, 900);
  }, true);

  /* ---------- 长文档仪表：页顶阅读进度 + 回到顶部 ---------- */
  function mountReadAids() {
    if (document.querySelector(".cqm-progress")) return;
    var bar = document.createElement("div");
    bar.className = "cqm-progress";
    var top = document.createElement("button");
    top.className = "cqm-top"; top.type = "button";
    top.setAttribute("aria-label", "回到顶部"); top.title = "回到顶部";
    top.textContent = "↑";
    top.addEventListener("click", function () {
      try { window.scrollTo({ top: 0, behavior: "smooth" }); } catch (e) { window.scrollTo(0, 0); }
    });
    document.body.appendChild(bar); document.body.appendChild(top);
    var onScroll = function () {
      var doc = document.documentElement;
      var h = doc.scrollHeight - window.innerHeight;
      var y = window.scrollY || doc.scrollTop || 0;
      bar.style.width = (h > 0 ? Math.min(100, (y / h) * 100) : 0) + "%";
      top.setAttribute("data-on", y > 320 ? "1" : "0");
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    onScroll();
  }

  /* ---------- 搜索结果里的公式排版 ----------
     VitePress 内置搜索的摘要是从 md 提取的纯文本，公式以 $…$ / $$…$$ 原文出现；
     结果项是真实 DOM，交给 MathJax 重排即可。结果每次输入都会重渲染，
     故对结果容器挂 MutationObserver + 节流。 */
  var searchObs = null;
  function hookSearchTypeset() {
    var box = document.querySelector(".VPLocalSearchBox");
    if (!box || searchObs) return;
    searchObs = new MutationObserver(function () {
      if (hookSearchTypeset._t) return;
      hookSearchTypeset._t = setTimeout(function () {
        hookSearchTypeset._t = null;
        if (window.MathJax && window.MathJax.typesetPromise) {
          try { window.MathJax.typesetPromise([box]); } catch (e) {}
        }
      }, 350);
    });
    searchObs.observe(box, { childList: true, subtree: true });
  }

  function initOnce() {
    if (bound) return; bound = true;
    build();
    document.body.appendChild(BOX); document.body.appendChild(MASK);
    BOX.style.display = "none"; MASK.style.display = "none";
    bindKeys();
    mountReadAids();
    document.addEventListener("click", function (e) {
      if (e.target.closest && e.target.closest(".DocSearch-Button")) {
        setTimeout(hookSearchTypeset, 500);
        setTimeout(hookSearchTypeset, 1300);
      }
    });
  }
  /* 外部链接新窗口打开，避免研究中途离开本站 */
  function fixExternalLinks() {
    var root = contentRoot(); if (!root) return;
    var as = root.querySelectorAll('a[href^="http"]');
    for (var i = 0; i < as.length; i++) {
      var a = as[i];
      if (a.host && a.host !== location.host && !a.getAttribute("target")) {
        a.setAttribute("target", "_blank");
        a.setAttribute("rel", "noopener noreferrer");
      }
    }
  }

  function initPage() {
    runTerms();
    initDepth();
    applySearchHighlight();
    fixExternalLinks();
    // 导航栏由 Vue 异步渲染：首次初始化时 .VPNavBarMenu 往往还不存在，
    // 若只挂一次就会整轮丢失（服务徽标因 fetch 延迟刚好躲过，曾掩盖此问题）。
    // 这里每次页面初始化都确保挂上，内部有幂等检查；再补一轮定时重试兜底。
    mountNav();
    probeService();
    // 导航栏由 Vue 异步渲染，重页面（公式上千个）会明显更晚。
    // 固定次数重试会在这类页面上耗光而漏挂，故改为观察 DOM 直到挂上。
    if (!document.querySelector(".cqm-advbtn") && !initPage._obs) {
      initPage._obs = new MutationObserver(function () {
        mountNav();
        if (document.querySelector(".cqm-advbtn")) {
          initPage._obs.disconnect(); initPage._obs = null;
        }
      });
      initPage._obs.observe(document.body, { childList: true, subtree: true });
      setTimeout(function () {
        if (initPage._obs) { initPage._obs.disconnect(); initPage._obs = null; }
      }, 45000);
    }
  }
  window.CQM = { init: function () { initOnce(); initPage(); },
                 highlight: function () { applySearchHighlight(); } };
  function boot() { window.CQM.init(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
