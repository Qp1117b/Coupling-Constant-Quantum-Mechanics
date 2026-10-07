(function () {
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
      var key = t.replace(/^\.\//, "").replace(/^\//, "");
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
    var m = /^#\/doc\/(.+)$/.exec(location.hash || "");
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
      var snip = h.d.text.substr(start, 90).replace(/\s+/g, " ");
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
