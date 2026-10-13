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
