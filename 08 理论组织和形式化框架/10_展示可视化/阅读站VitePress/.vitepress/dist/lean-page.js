(function () {
  var escMap = { '&': '&amp;', '<': '&lt;', '>': '&gt;' };
  function e(s) { return String(s == null ? '' : s).replace(/[&<>]/g, function (c) { return escMap[c]; }); }

  var CSS = ''
    + '.lean-app{font-size:14px;line-height:1.7}'
    + '.lean-app code,.lean-app pre{font-family:var(--vp-font-family-mono,monospace)}'
    + '.lean-tabs{display:flex;gap:8px;margin:14px 0;flex-wrap:wrap}'
    + '.lean-tabs button{padding:6px 14px;border:1px solid var(--vp-c-divider);border-radius:8px;'
    +   'background:var(--vp-c-bg);color:var(--vp-c-text-1);cursor:pointer;font:inherit}'
    + '.lean-tabs button[data-on="1"]{background:var(--vp-c-brand-soft);border-color:var(--vp-c-brand-1);color:var(--vp-c-brand-1)}'
    + '.lean-split{display:flex;gap:18px;align-items:flex-start;flex-wrap:wrap}'
    + '.lean-mods{width:270px;flex:0 0 auto;max-height:66vh;overflow:auto;border:1px solid var(--vp-c-divider);border-radius:8px;padding:8px}'
    + '.lean-mods ul{list-style:none;margin:0;padding:0}'
    + '.lean-mods li{padding:4px 8px;border-radius:6px;cursor:pointer;display:flex;justify-content:space-between}'
    + '.lean-mods li:hover{background:var(--vp-c-bg-soft)}'
    + '.lean-mods li[data-on="1"]{background:var(--vp-c-brand-soft);color:var(--vp-c-brand-1)}'
    + '.lean-mods .lean-n{opacity:.7;font-variant-numeric:tabular-nums}'
    + '.lean-decls{flex:1 1 480px;min-width:380px;max-height:66vh;overflow:auto}'
    + '.lean-app table{width:100%;border-collapse:collapse;font-size:13px}'
    + '.lean-app th,.lean-app td{border-bottom:1px solid var(--vp-c-divider);padding:6px 9px;text-align:left;vertical-align:top}'
    + '.lean-app th{position:sticky;top:0;background:var(--vp-c-bg-alt);z-index:1}'
    + '.lean-k{display:inline-block;padding:0 7px;border-radius:9px;font-size:11.5px;margin-right:4px;'
    +   'background:var(--vp-c-bg-soft);border:1px solid var(--vp-c-divider)}'
    + '.lean-k.axiom{background:#fdf3e0;border-color:#e8c98a;color:#8a5a00}'
    + '.lean-k.theorem{background:#e3f3ea;border-color:#bfe0cc;color:#1c7a3d}'
    + '.lean-src{max-height:60vh;overflow:auto;background:var(--vp-c-bg-alt);border:1px solid var(--vp-c-divider);'
    +   'border-radius:8px;padding:12px;font-size:12.5px;line-height:1.55}'
    + '.lean-src .ln{display:inline-block;width:3.2em;color:var(--vp-c-text-3);user-select:none}'
    + '.lean-src .cur{background:var(--vp-c-brand-soft);display:inline-block;width:100%}'
    + '.lean-toolbar{display:flex;gap:8px;align-items:center;margin:8px 0;flex-wrap:wrap}'
    + '.lean-toolbar input,.lean-toolbar select{padding:5px 9px;border:1px solid var(--vp-c-divider);'
    +   'border-radius:6px;background:var(--vp-c-bg);color:var(--vp-c-text-1);font:inherit}'
    + '.lean-run{padding:7px 18px;border-radius:8px;border:1px solid var(--vp-c-brand-1);'
    +   'background:var(--vp-c-brand-1);color:#fff;cursor:pointer;font:inherit}'
    + '.lean-run:disabled{opacity:.5;cursor:default}'
    + '.lean-log{max-height:46vh;overflow:auto;background:#0b1020;color:#c8d6f5;padding:12px;'
    +   'border-radius:8px;font-size:12.5px;white-space:pre-wrap}'
    + '.lean-status{font-weight:600}';

  var S = { mods: [], decls: [], mapping: [], mod: '', kind: '' };

  function api(p) {
    return fetch(p).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    });
  }

  function kindBadge(k) { return '<span class="lean-k ' + e(k) + '">' + e(k) + '</span>'; }

  function render(app) {
    app.innerHTML =
      '<div class="lean-tabs">' +
      '<button data-tab="mods" data-on="1">模块与声明</button>' +
      '<button data-tab="map">概念 ↔ Lean</button></div>' +
      '<div class="lean-body"></div>';
    var body = app.querySelector('.lean-body');
    function show(tab) {
      Array.prototype.forEach.call(app.querySelectorAll('.lean-tabs button'), function (b) {
        b.setAttribute('data-on', b.getAttribute('data-tab') === tab ? '1' : '0');
      });
      if (tab === 'mods') renderMods(body);
      if (tab === 'map') renderMap(body);
    }
    Array.prototype.forEach.call(app.querySelectorAll('.lean-tabs button'), function (b) {
      b.addEventListener('click', function () { show(b.getAttribute('data-tab')); });
    });
    show('mods');
  }

  /* ---------- Tab 1：模块与声明 + 源码 ---------- */
  function renderMods(body) {
    body.innerHTML =
      '<div class="lean-toolbar">' +
      '<select id="lean-kind"><option value="">全部种类</option></select>' +
      '<input id="lean-q" placeholder="搜索声明名…" style="min-width:200px">' +
      '<span id="lean-count" style="opacity:.7"></span></div>' +
      '<div class="lean-split"><div class="lean-mods"><ul id="lean-modlist"></ul></div>' +
      '<div class="lean-decls"><table><thead><tr><th>种类</th><th>名称</th><th>位置</th></tr></thead>' +
      '<tbody id="lean-declrows"></tbody></table></div></div>' +
      '<div id="lean-srcbox" style="margin-top:14px"></div>';

    var kinds = [];
    S.decls.forEach(function (d) { if (kinds.indexOf(d.kind) < 0) kinds.push(d.kind); });
    kinds.sort();
    var ksel = body.querySelector('#lean-kind');
    kinds.forEach(function (k) {
      var o = document.createElement('option'); o.value = k; o.textContent = k; ksel.appendChild(o);
    });
    ksel.value = S.kind;

    var modlist = body.querySelector('#lean-modlist');
    modlist.innerHTML = S.mods.map(function (m) {
      return '<li data-m="' + e(m.module) + '"' + (m.module === S.mod ? ' data-on="1"' : '') + '>' +
        '<span>' + e(m.module) + '</span><span class="lean-n">' + e(m.total_decl) + '</span></li>';
    }).join('');
    modlist.addEventListener('click', function (ev) {
      var li = ev.target.closest('li[data-m]'); if (!li) return;
      S.mod = li.getAttribute('data-m');
      Array.prototype.forEach.call(modlist.children, function (x) {
        x.setAttribute('data-on', x === li ? '1' : '0');
      });
      paintRows(body);
    });

    body.querySelector('#lean-kind').addEventListener('change', function () {
      S.kind = this.value; paintRows(body);
    });
    body.querySelector('#lean-q').addEventListener('input', function () { paintRows(body); });

    modlist.addEventListener('dblclick', function (ev) {
      var li = ev.target.closest('li[data-m]'); if (!li) return;
      var m = li.getAttribute('data-m');
      var row = S.mods.filter(function (x) { return x.module === m; })[0];
      if (row && row.file) openSource(body, row.file, 0);
    });
    paintRows(body);

    function paintRows(body2) {
      var q = (body2.querySelector('#lean-q') || {}).value || '';
      var rows = S.decls.filter(function (d) {
        if (S.mod && d.module !== S.mod) return false;
        if (S.kind && d.kind !== S.kind) return false;
        if (q && d.name.toLowerCase().indexOf(q.toLowerCase()) < 0) return false;
        return true;
      });
      body2.querySelector('#lean-count').textContent = rows.length + ' 条声明';
      body2.querySelector('#lean-declrows').innerHTML = rows.slice(0, 600).map(function (d) {
        return '<tr><td>' + kindBadge(d.kind) + '</td><td><code>' + e(d.name) + '</code></td>' +
          '<td><a href="javascript:void 0" data-f="' + e(d.file) + '" data-l="' + e(d.line) + '">' +
          e(d.module) + ':' + e(d.line) + '</a></td></tr>';
      }).join('');
    }
    body.addEventListener('click', function (ev) {
      var a = ev.target.closest('a[data-f]'); if (!a) return;
      openSource(body, a.getAttribute('data-f'), parseInt(a.getAttribute('data-l'), 10) || 0);
    });
  }

  function openSource(body, file, line) {
    var box = body.querySelector('#lean-srcbox') || body;
    box.innerHTML = '<div class="lean-toolbar"><strong>' + e(file) + '</strong>' +
      '<span style="opacity:.7">（来自 /api/lean/source，只读）</span></div>' +
      '<pre class="lean-src" id="lean-src">加载中…</pre>';
    var pre = box.querySelector('#lean-src');
    fetch('/api/lean/source?file=' + encodeURIComponent(file))
      .then(function (r) { return r.text(); })
      .then(function (src) {
        var lines = src.split('\n');
        var html = lines.map(function (l, i) {
          return '<span class="ln' + (line && (i + 1) === line ? ' cur' : '') + '">' + (i + 1) + '</span>' +
            (line && (i + 1) === line ? '<span class="cur">' + e(l) + '</span>' : e(l));
        }).join('\n');
        pre.innerHTML = html;
        if (line) {
          var cur = pre.querySelector('.cur');
          if (cur) cur.scrollIntoView({ block: 'center' });
        }
      })
      .catch(function (err) { pre.textContent = '加载失败：' + err; });
  }

  /* ---------- Tab 2：概念 ↔ Lean ---------- */
  function renderMap(body) {
    var axioms = S.decls.filter(function (d) { return d.kind === 'axiom'; });
    body.innerHTML =
      '<h4 style="margin:.4em 0">人工整理的概念/命题/缺口 ↔ Lean 符号映射（' + S.mapping.length + ' 条）</h4>' +
      '<div style="max-height:40vh;overflow:auto"><table><thead><tr>' +
      '<th>Lean 库</th><th>Lean 符号</th><th>概念</th><th>命题</th><th>缺口</th><th>说明</th></tr></thead><tbody>' +
      S.mapping.map(function (m) {
        return '<tr><td><code>' + e(m.lean_library) + '</code></td><td><code>' + e(m.lean_symbol) + '</code></td>' +
          '<td>' + e(m.concept_ids) + '</td><td>' + e(m.prop_ids) + '</td><td>' + e(m.gap_ids) + '</td>' +
          '<td>' + e(m.remark) + '</td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<h4 style="margin:1.2em 0 .4em">axiom 待证清单（' + axioms.length + ' 条 · 物理假设的 Lean 承载，形式化覆盖 40/81 概念之外的诚实边界）</h4>' +
      '<div style="max-height:32vh;overflow:auto"><table><thead><tr><th>种类</th><th>名称</th><th>模块</th><th>行</th></tr></thead><tbody>' +
      axioms.map(function (d) {
        return '<tr><td>' + kindBadge(d.kind) + '</td><td><code>' + e(d.name) + '</code></td>' +
          '<td>' + e(d.module) + '</td><td>' + e(d.line) + '</td></tr>';
      }).join('') + '</tbody></table></div>' +
      '<p style="opacity:.75;font-size:13px">呈现边界：缺口状态与「axiom 待证」原样登记，不因呈现而升格；' +
      '映射由人工整理，机器不推断新的对应关系。</p>';
  }

  function boot() {
    var app = document.getElementById('lean-app');
    if (!app || app.__done) return;
    app.__done = 1;
    var style = document.createElement('style');
    style.textContent = CSS;
    document.head.appendChild(style);
    app.textContent = '正在加载 Lean 对接数据…';
    Promise.all([api('/api/lean/modules'), api('/api/lean/decls'), api('/api/lean/mapping')])
      .then(function (rs) {
        S.mods = rs[0]; S.decls = rs[1]; S.mapping = rs[2];
        render(app);
      })
      .catch(function (err) {
        app.textContent = 'Lean 数据加载失败：' + err +
          '（研究站服务需在运行：http://127.0.0.1:8080）';
      });
  }
  new MutationObserver(function () { boot(); })
    .observe(document.documentElement, { childList: true, subtree: true });
  boot();
})();
