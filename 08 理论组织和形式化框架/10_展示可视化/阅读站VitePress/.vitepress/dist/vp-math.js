window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']],
    processEscapes: true,
    // 语料里 21 处 \xRightarrow 是「重组实现」用的双线箭头；它不是 MathJax 内置宏
    // （bundle 里只有 \xrightarrow）。本包 tex-svg.js 带 noundefined 扩展，未定义宏
    // 不报错而是把宏名以红字**字面**排出来（实测页面显示红色的 \xRightarrow），
    // 故在此补定义：等价于带标签的双线箭头，与 \xrightarrow 的观感一致。
    macros: {
      xRightarrow: ["\\overset{#1}{\\Longrightarrow}", 1]
    }
  },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code'] }
};

/* ---------------------------------------------------------------- 载入引擎
   tex-svg.js 是本包 2.1MB 的完整 SVG 引擎，配置必须**先于**它执行，故注入逻辑
   写在同一个文件里（配置赋值在前，注入在后），不再另挂 <script> 标签。

   取源按地址分两路：
     · localhost / 127.0.0.1 / 内网段 —— 取随站文件，离线站与局域网阅读不受影响；
     · 其他（公网部署）—— 依次尝试国内 CDN，全部失败再回落随站文件。
   为什么要分路：2.1MB 从境外源站直取，实测 30–70s 才到位，这段时间里正文与
   标题的公式一律以 LaTeX 原文露出；国内 CDN 同一文件 1s 内下完。回落的仍是
   随站文件，所以断网、CDN 被拦时功能不缺，只是慢。
   两份字节不同但同为 MathJax 3.2.2：随站版把 CDN 地址本地化了（供离线用），
   与渲染无关的分支，排版结果一致。 */
(function () {
  var LOCAL = "/tex-svg.js?v=3.2.2";
  var CDNS = ["https://lib.baomitu.com/mathjax/3.2.2/es5/tex-svg.js",
              "https://cdn.bootcdn.net/ajax/libs/mathjax/3.2.2/es5/tex-svg.js"];
  var h = location.hostname || "";
  var localOnly = !h || h === "localhost" || h === "127.0.0.1" || h === "::1" ||
      /^(10\.|192\.168\.|172\.(1[6-9]|2\d|3[01])\.)/.test(h);

  function load(src, onFail) {
    var s = document.createElement("script");
    s.src = src;
    s.async = true;
    if (onFail) { s.onerror = onFail; }
    document.head.appendChild(s);
  }
  if (localOnly) { load(LOCAL, null); return; }
  (function tryCdn(i) {
    if (i >= CDNS.length) { load(LOCAL, null); return; }
    load(CDNS[i], function () { tryCdn(i + 1); });
  })(0);
})();
