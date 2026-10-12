import DefaultTheme from 'vitepress/theme'

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
