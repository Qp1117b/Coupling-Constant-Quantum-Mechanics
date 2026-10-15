import { defineConfig } from 'vitepress'

// 中文检索分词：minisearch 默认把连续的 CJK 当一个词，中文查询几乎命中不了。
// 这里按「单字 + 二元」切分中文、按词切分拉丁；索引与查询共用同一 tokenize。
const cqmTokenize = (text) => {
  const out = []
  const re = /[\u4e00-\u9fff]+|[A-Za-z0-9_\-]+/g
  let m
  while ((m = re.exec(text))) {
    const s = m[0]
    if (/^[\u4e00-\u9fff]+$/.test(s)) {
      for (let i = 0; i < s.length; i++) {
        out.push(s[i])
        if (i + 1 < s.length) out.push(s.slice(i, i + 2))
      }
    } else {
      out.push(s.toLowerCase())
    }
  }
  return out
}

export default defineConfig({
  lang: 'zh-CN',
  title: 'CQM 研究站',
  description: '耦合常数量子力学（CQM）组织层研究站：结构化数据 · 知识图谱 · 证据层 · 形式化验证',
  srcDir: 'docs',
  outDir: '.vitepress/dist',
  // 死链不再放行：站内 404 已清零（见 fix_src_links），让构建自己当验证器——
  // 一旦再引入失效链接，构建会直接失败并点名文件与目标。
  ignoreDeadLinks: false,
  // 数学保护：VitePress 默认没有数学插件，markdown-it 会先按普通文本解析，
  // 于是公式里的 _ / * 被当成强调语法，例如 $$\mathbb{R}_{>0}$$ 被解析成
  // "\mathbb{R}<em>{>0}</em>"——标签一旦插入，MathJax 就无法再匹配这对
  // 定界符，该公式只能以 LaTeX 原文裸露在页面上。
  // 这里在 emphasis 规则之前插入一条规则，把 $...$ / $$...$$ 整段取出、
  // 原样输出（只做 HTML 转义，不改内容），再由页面上的 MathJax 排版。
  // attrs.disable：VitePress 默认启用 markdown-it-attrs，会把块/单元格末尾的
  // {...} 当属性块吞掉（实测 D019 表格「重数 {1,4,5}」整段消失、<td> 里
  // 多出畸形属性 1,4,5=""）。CQM 语料零有意属性用法（{.class}/{: ...} 扫描
  // 为 0），直接关闭，保文本原样。
  markdown: {
    attrs: { disable: true },
    config(md) {
      const DOLLAR = 0x24, BACKSLASH = 0x5c
      const isDollar = (c) => c === DOLLAR
      const isEscaped = (src, i) => i > 0 && src.charCodeAt(i - 1) === BACKSLASH
      const escHtml = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')

      // 注意：不要替换 markdown-it 的 text 规则。它的终止字符表本来就有 '$'
      // （连同星号、下划线、波浪号等 22 个），曾误以为缺 '$' 而自行重写，
      // 结果漏抄星号等下划线等，导致加粗与斜体语法全被 text 规则整段吞掉
      // （实测 6 113 处加粗字面未解析）。此处只用下面的 cqm_math 规则，
      // 它的注册位置在 emphasis 之前，足以整段接管 $…$。
      md.inline.ruler.before('emphasis', 'cqm_math', function (state, silent) {
        const src = state.src, start = state.pos, max = state.posMax
        if (!isDollar(src.charCodeAt(start)) || isEscaped(src, start)) return false
        const block = (start + 1 < max) && isDollar(src.charCodeAt(start + 1))
        const openLen = block ? 2 : 1
        let pos = start + openLen, close = -1
        while (pos < max) {
          const c = src.charCodeAt(pos)
          if (c === BACKSLASH) { pos += 2; continue }
          if (isDollar(c)) {
            if (block) {
              if (pos + 1 < max && isDollar(src.charCodeAt(pos + 1))) { close = pos; break }
            } else if (!isEscaped(src, pos)) { close = pos; break }
          }
          pos++
        }
        if (close < 0 || close === start + openLen) return false
        if (!silent) {
          const token = state.push('cqm_math', 'math', 0)
          token.content = src.slice(start, close + openLen)
        }
        state.pos = close + openLen
        return true
      })

      md.renderer.rules.cqm_math = (tokens, idx) => escHtml(tokens[idx].content)
    }
  },
  head: [
    // 这些资源文件名不带内容哈希，必须挂版本串：否则重建后浏览器仍用旧脚本，
    // 现象是「明明修好了、页面上却还是老样子」。
    ['link', { rel: 'stylesheet', href: '/vp-brand.css?v=20261015095557' }],
    ['link', { rel: 'stylesheet', href: '/vp-read.css?v=20261015095557' }],
    ['link', { rel: 'stylesheet', href: '/stylesheets/cqm-enhance.css?v=20261015095557' }],
    ['script', { src: '/cqm-glossary.js?v=20261015095557', defer: true }],
    ['script', { src: '/cqm-depth.js?v=20261015095557', defer: true }],
    ['script', { src: '/cqm-enhance-vp.js?v=20261015095557', defer: true }],
    ['script', { src: '/vp-math.js?v=20261015095557', defer: true }],
    ['script', { src: '/tex-svg.js?v=20261015095557', defer: true }],
    ['script', { src: '/lean-page.js?v=20261015095557', defer: true }],
    ['script', { src: '/terms-app.js?v=20261015095557', defer: true }]
  ],
  themeConfig: {
    nav: [
  {
    "text": "首页",
    "link": "/"
  },
  {
    "text": "展开链",
    "link": "/L000_展开链"
  },
  {
    "text": "讲稿",
    "link": "/L001_第一分册_从问题到链条"
  },
  {
    "text": "可视化",
    "link": "/V000_可视化总览"
  },
  {
    "text": "Lean 对接",
    "link": "/LEAN_Lean对接"
  },
  {
    "text": "术语表",
    "link": "/TERMS_术语表"
  },
  {
    "text": "检索台",
    "link": "/V003_检索台"
  }
],
    sidebar: [
  {
    "text": "展开链",
    "items": [
      {
        "text": "展开链（拉通阅读）",
        "link": "/L000_展开链"
      }
    ]
  },
  {
    "text": "讲稿",
    "items": [
      {
        "text": "展开链讲稿 · 第一分册：从问题到链条",
        "link": "/L001_第一分册_从问题到链条"
      },
      {
        "text": "展开链讲稿 · 第二分册：统一体怎么自组装，α 从哪里来",
        "link": "/L002_第二分册_统一体自组装与α"
      },
      {
        "text": "展开链讲稿 · 第三分册：谱方程与黎曼零点（Sierra-CQM 耦谱定理）",
        "link": "/L003_第三分册_谱方程与黎曼零点"
      },
      {
        "text": "展开链讲稿 · 第四分册：超导涌现链（跃迁耦级谱与自由能竞争）",
        "link": "/L004_第四分册_超导涌现链"
      },
      {
        "text": "展开链讲稿 · 第五分册：与标准理论的关系与涨落伴丛",
        "link": "/L005_第五分册_与标准理论的关系与涨落伴丛"
      },
      {
        "text": "展开链讲稿 · 第六分册：量纲发生学专章（K 家族与自守形式猜想）",
        "link": "/L006_第六分册_量纲发生学专章"
      }
    ]
  },
  {
    "text": "核心理论",
    "items": [
      {
        "text": "耦合常数量子力学（CQM）——集成理论",
        "link": "/D005_集成理论_总纲"
      },
      {
        "text": "CQM 核心：两种引力存在论前提与中子缺陷矩阵",
        "link": "/D006_引力存在论前提"
      },
      {
        "text": "因果网络同步理论：从黎曼结构到物理涌现",
        "link": "/D007_因果网络同步理论"
      },
      {
        "text": "朗兰兹分层共振与相变量子：CQM 的统一发生学",
        "link": "/D008_朗兰兹分层共振与相变量子"
      },
      {
        "text": "CQM 核心：量纲与群论（量纲发生学）",
        "link": "/D009_量纲与群论"
      },
      {
        "text": "唯物主义群论：Sym ⊃ Diff ⊃ GL(n,𝔽) 三层结构、群约束性分类与不变性",
        "link": "/D010_唯物主义群论"
      },
      {
        "text": "CQM核心：声子理论——振荡、曲率与同步的量子媒介",
        "link": "/D011_声子理论"
      },
      {
        "text": "CQM核心：共形场论与OPE——同步 ⊗ 耦合 → 群的数学基础",
        "link": "/D012_共形场论与OPE"
      }
    ]
  },
  {
    "text": "量子引力讨论",
    "items": [
      {
        "text": "CQM 量子引力讨论：两个候选与 FG",
        "link": "/D013_量子引力讨论"
      }
    ]
  },
  {
    "text": "引力与退相干",
    "items": [
      {
        "text": "CQM 牛顿引力常数 G_N 的可能公式",
        "link": "/D014_GN可能公式"
      },
      {
        "text": "引力因果限制场与退相干理论",
        "link": "/D015_引力因果场_退相干"
      },
      {
        "text": "CQM 退相干：跨层级深耦合与唯一性难题",
        "link": "/D016_跨层级深耦合与唯一性难题"
      }
    ]
  },
  {
    "text": "前沿研究",
    "items": [
      {
        "text": "CQM 下的黎曼猜想证明思路",
        "link": "/D017_黎曼猜想证明思路"
      },
      {
        "text": "CQM 待推 1（边界条件）深度分析 —— 五重联系整合版",
        "link": "/D018_待推1边界条件"
      },
      {
        "text": "G_N 第一性推导：公理化证明稿",
        "link": "/D019_GN第一性推导公理化"
      },
      {
        "text": "CQM 质量研究思路汇总",
        "link": "/D020_质量研究思路汇总"
      },
      {
        "text": "Wyler 常数的 A_4 群论分解与 CQM 框架嵌入",
        "link": "/D021_Wyler常数"
      },
      {
        "text": "贝里曲率与 Regge 曲率的关联：文献调研与研究论文",
        "link": "/D022_贝里曲率与Regge曲率"
      },
      {
        "text": "规范对称性重组下的超导、相变路径积分与 SU(5) 五重态内禀时间结构（前沿研究）",
        "link": "/D023_规范重组超导与SU5五重态"
      },
      {
        "text": "相变弧线上的自守形式同步：局部共形对称性与全局模对称性",
        "link": "/D024_相变弧线与自守形式同步"
      },
      {
        "text": "量子快置乱普适速率极限与 CQM 对称群谱系的交叉研究",
        "link": "/D025_量子快置乱普适速率极限"
      }
    ]
  },
  {
    "text": "方法论与批判",
    "items": [
      {
        "text": "对 Hilbert–Pólya 猜想的批判",
        "link": "/D026_HilbertPolya批判"
      },
      {
        "text": "资本主义、旧物理学与层级还原论：一个意识形态-科学同构系统的批判与超越",
        "link": "/D027_资本主义-旧物理-层级还原论批判"
      }
    ]
  },
  {
    "text": "超导",
    "items": [
      {
        "text": "CQM 超导核心理论",
        "link": "/D030_超导核心理论"
      },
      {
        "text": "CQM 超导：专题与应用扩展",
        "link": "/D031_专题与扩展"
      },
      {
        "text": "FG 层级同步算符体系：从元素 FG 到分子 FG 的第一性超导预测框架",
        "link": "/D032_FG层级同步算符体系"
      },
      {
        "text": "CQM超导统一方法论：四层FG纤维丛与相对第一性计算链",
        "link": "/D033_统一方法论"
      },
      {
        "text": "CQM 3D专业引力超导实验软件",
        "link": "/D034_材料设计器总览"
      },
      {
        "text": "01 系统架构设计",
        "link": "/D035_系统架构设计"
      },
      {
        "text": "02 元素及同位素数据库",
        "link": "/D036_元素同位素数据库"
      },
      {
        "text": "03 超导性质自动计算与判定算法",
        "link": "/D037_超导判定算法"
      },
      {
        "text": "04 应用场景与对比",
        "link": "/D038_应用场景与对比分析"
      },
      {
        "text": "05 元素嘉当矩阵参数化设计",
        "link": "/D039_元素嘉当矩阵参数化设计"
      },
      {
        "text": "06 文献调研与专业化路线",
        "link": "/D040_文献调研与专业化路线"
      },
      {
        "text": "07 目标超导搜索策略",
        "link": "/D041_目标超导搜索策略"
      }
    ]
  },
  {
    "text": "精细引力（FG）",
    "items": [
      {
        "text": "FG核心理论",
        "link": "/D028_FG核心理论"
      },
      {
        "text": "FG纤维丛理论",
        "link": "/D029_FG纤维丛理论"
      }
    ]
  },
  {
    "text": "可视化",
    "items": [
      {
        "text": "可视化总览",
        "link": "/V000_可视化总览"
      },
      {
        "text": "可推演超图",
        "link": "/V001_可推演超图"
      },
      {
        "text": "研究驾驶舱",
        "link": "/V002_研究驾驶舱"
      },
      {
        "text": "检索台",
        "link": "/V003_检索台"
      },
      {
        "text": "形式化蓝图",
        "link": "/V004_形式化蓝图"
      }
    ]
  },
  {
    "text": "Lean 对接",
    "items": [
      {
        "text": "Lean 对接 · 统一视图",
        "link": "/LEAN_Lean对接"
      }
    ]
  },
  {
    "text": "术语表",
    "items": [
      {
        "text": "术语总览（227 条）",
        "link": "/TERMS_术语表"
      }
    ]
  },
  {
    "text": "其它",
    "items": [
      {
        "text": "CQM 超导材料设计器 - AI代理规则",
        "link": "/F01_AGENTS"
      },
      {
        "text": "Godot AI",
        "link": "/F02_README"
      }
    ]
  }
],
    // 内置全文搜索（VitePress 官方 local provider）：构建期生成索引，离线可用；
    // Ctrl/⌘+K 唤起，导航栏出现搜索按钮。索引走 fetch，需经 HTTP 访问。
    search: {
      provider: 'local',
      options: {
        detailedView: true,
        translations: {
          button: { buttonText: '搜索', buttonAriaLabel: '搜索文档' },
          modal: {
            displayDetails: '显示详细列表',
            resetButtonTitle: '清除查询条件',
            backButtonTitle: '返回',
            noResultsText: '未找到相关结果',
            footer: {
              selectText: '选择',
              selectKeyAriaLabel: '回车',
              navigateText: '切换',
              navigateUpKeyAriaLabel: '上箭头',
              navigateDownKeyAriaLabel: '下箭头',
              closeText: '关闭',
              closeKeyAriaLabel: 'Esc'
            }
          }
        },
        miniSearch: {
          options: { tokenize: cqmTokenize },
          searchOptions: { fuzzy: 0.2, prefix: true, boost: { title: 4, text: 2 } }
        }
      }
    },
    outline: [2, 3],
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: false
  },
})
