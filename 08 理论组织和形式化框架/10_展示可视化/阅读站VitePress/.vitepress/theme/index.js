import DefaultTheme from 'vitepress/theme'

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
