window.MathJax = {
  tex: {
    inlineMath: [['$','$'],['\\(','\\)']],
    displayMath: [['$$','$$'],['\\[','\\]']],
    processEscapes: true,
    macros: { xRightarrow: ['\\overset{#1}{\\Longrightarrow}', 1] }
  },
  svg: { fontCache: 'global' },
  options: { skipHtmlTags: ['script','noscript','style','textarea','pre','code'] }
};
