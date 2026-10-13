(function () {
  var CATS = ["概念", "缺口", "论证", "符号", "命题", "文档", "链条步"];
  function boot() {
    var app = document.getElementById("terms-app");
    if (!app || app.__done) return;
    var G = window.CQM_GLOSSARY;
    if (!G) return;
    app.__done = 1;
    var terms = G.terms || {}, index = G.index || [];
    var style = document.createElement("style");
    style.textContent = ''
      + '.terms-app{font-size:14px}'
      + '.terms-chips{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}'
      + '.terms-chips button{padding:5px 13px;border:1px solid var(--vp-c-divider);border-radius:16px;'
      +   'background:var(--vp-c-bg);color:var(--vp-c-text-1);cursor:pointer;font:inherit}'
      + '.terms-chips button[data-on="1"]{background:var(--vp-c-brand-soft);border-color:var(--vp-c-brand-1);color:var(--vp-c-brand-1)}'
      + '.terms-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}'
      + '.terms-card{border:1px solid var(--vp-c-divider);border-radius:8px;padding:10px 12px;cursor:pointer;'
      +   'background:var(--vp-c-bg);transition:border-color .15s}'
      + '.terms-card:hover{border-color:var(--vp-c-brand-1)}'
      + '.terms-card__n{font-weight:600;margin-bottom:3px;display:flex;gap:6px;align-items:baseline}'
      + '.terms-card__ty{font-size:11px;color:var(--vp-c-text-3);font-weight:400}'
      + '.terms-card__s{font-size:12.5px;color:var(--vp-c-text-2);line-height:1.5;}'
      + '.terms-toolbar{display:flex;gap:8px;align-items:center;margin:10px 0}'
      + '.terms-toolbar input{flex:0 0 260px;padding:6px 11px;border:1px solid var(--vp-c-divider);'
      +   'border-radius:6px;background:var(--vp-c-bg);color:var(--vp-c-text-1);font:inherit}';
    document.head.appendChild(style);

    var keyOf = function (ty, tt) {
      if (ty === "缺口") return tt.replace(/^缺口\s*/, "");
      if (ty === "论证") return tt.replace(/^论证\s*/, "");
      if (ty === "符号") return tt.split("\u3000")[0];
      return tt;
    };

    /* sb 摘要：先按可见字符截断（绝不切在 $…$ 内部——切断会让 MathJax 失配、
       把 $\bar{\delta}_v$ 之类的反斜杠字面露出），再做 HTML 转义；
       $…$ 公式转义后原样保留，由下面的 typesetGrid 排版。 */
    function esc(s) {
      return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
      });
    }
    function clip(s, n) {
      s = String(s == null ? "" : s);
      if (s.length <= n) return s;
      var re = /\$\$[\s\S]*?\$\$|\$[^$\n]*?\$/g, m, cut = n;
      while ((m = re.exec(s))) {
        if (m.index < cut && cut < m.index + m[0].length) { cut = m.index; break; }
      }
      return s.slice(0, cut).replace(/\s+$/, "") + "…";
    }
    var _tsTimer = null;
    function typesetGrid(grid) {
      if (_tsTimer) clearTimeout(_tsTimer);
      _tsTimer = setTimeout(function () {
        if (window.MathJax && window.MathJax.typesetPromise) {
          try { window.MathJax.typesetPromise([grid]); } catch (e) {}
        }
      }, 120);
    }

    function cardHtml(item) {
      var key = keyOf(item.ty, item.tt);
      var hasCard = !!terms[key];
      return '<div class="terms-card"' + (hasCard ? ' data-cqm="' + esc(key) + '"' : "") + '>' +
        '<div class="terms-card__n"><span>' + esc(item.tt) + '</span><span class="terms-card__ty">' + esc(item.ty) + '</span></div>' +
        '<div class="terms-card__s">' + esc(clip(item.sb, 110)) + '</div></div>';
    }

    function paint(filterCat, filterQ) {
      var grid = app.querySelector(".terms-grid");
      var items = index.filter(function (it) {
        if (filterCat && it.ty !== filterCat) return false;
        if (filterQ) {
          var q = filterQ.toLowerCase();
          if ((it.tt + " " + (it.sb || "") + " " + (it.dc || "")).toLowerCase().indexOf(q) < 0) return false;
        }
        return true;
      });
      grid.innerHTML = items.map(cardHtml).join("") ||
        '<div style="opacity:.7">无匹配条目</div>';
      app.querySelector("#terms-count").textContent = items.length + " 条";
      typesetGrid(grid);
    }

    app.innerHTML =
      '<p style="margin-top:.2em">全部 <strong>' + index.length + '</strong> 条术语与实体的集中浏览：' +
      '悬停或点击卡片查看完整解释（公式与出处同悬浮卡）；用上方分类与搜索框缩小范围。</p>' +
      '<div class="terms-toolbar"><input id="terms-q" placeholder="按名称或内容筛选…"></div>' +
      '<div class="terms-chips" id="terms-chips"></div>' +
      '<div id="terms-count" style="opacity:.7;margin-bottom:8px"></div>' +
      '<div class="terms-grid"></div>';

    var chips = app.querySelector("#terms-chips");
    var all = document.createElement("button");
    all.textContent = "全部"; all.setAttribute("data-on", "1");
    all.addEventListener("click", function () {
      Array.prototype.forEach.call(chips.children, function (b) { b.setAttribute("data-on", "0"); });
      all.setAttribute("data-on", "1");
      paint("", app.querySelector("#terms-q").value);
    });
    chips.appendChild(all);
    CATS.forEach(function (cat) {
      var n = index.filter(function (it) { return it.ty === cat; }).length;
      if (!n) return;
      var b = document.createElement("button");
      b.textContent = cat + " " + n;
      b.addEventListener("click", function () {
        Array.prototype.forEach.call(chips.children, function (x) { x.setAttribute("data-on", "0"); });
        b.setAttribute("data-on", "1");
        paint(cat, app.querySelector("#terms-q").value);
      });
      chips.appendChild(b);
    });
    var inp = app.querySelector("#terms-q");
    inp.addEventListener("input", function () {
      var cat = "";
      Array.prototype.forEach.call(chips.children, function (b) {
        if (b.getAttribute("data-on") === "1" && b.textContent !== "全部") {
          cat = b.textContent.split(" ")[0];
        }
      });
      paint(cat, inp.value);
    });
    paint("", "");
  }
  new MutationObserver(function () { boot(); })
    .observe(document.documentElement, { childList: true, subtree: true });
  boot();
})();
