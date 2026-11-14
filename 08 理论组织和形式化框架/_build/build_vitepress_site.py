#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""构建 VitePress 版 CQM 研究站（唯一站点）。

复用 build_reader_site.py 已经 staged 到 _build/mkdocs_src/docs 的 markdown，
转成 VitePress 的 docs/ + .vitepress/config.mts，产出真正由 VitePress v1.6.4
生成的静态站（验收点：<meta name="generator" content="VitePress v1.6.4">，
观感为顶部导航 + 左侧分组侧栏 + 右侧大纲 + 品牌靛蓝 #3451b2 + 首页 hero/特性卡）。
"""
import csv
import html
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import time

ROOT08 = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MK_SRC = os.path.join(ROOT08, "_build", "mkdocs_src", "docs")
VP_ROOT = os.path.join(ROOT08, "10_展示可视化", "阅读站VitePress")
VP_DOCS = os.path.join(VP_ROOT, "docs")
VP_PUBLIC = os.path.join(VP_DOCS, "public")
VP_CFG_DIR = os.path.join(VP_ROOT, ".vitepress")

NODE_DIR = r"C:/Users/13649/.workbuddy/binaries/node/versions/22.22.2-6"
NODE = os.path.join(NODE_DIR, "node.exe")
VITEPRESS_BIN = os.path.join(VP_ROOT, "node_modules", "vitepress", "bin", "vitepress.js")

for d in (VP_DOCS, VP_PUBLIC, VP_CFG_DIR):
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------- 1. 复制 markdown
assert os.path.isdir(MK_SRC), "staged 源不存在：%s（请先运行 build_reader_site.py）" % MK_SRC
md_files = sorted(f for f in os.listdir(MK_SRC) if f.endswith(".md"))
assert md_files, "staged 源里没有 md 文件"
# 清掉上一轮遗留、本轮 staging 已剔除的页面（如 06 超导/godot_project 的工程文档），
# 否则它们既不在 sidebar/nav，又会触发可达性断言失败。
for _f in sorted(os.listdir(VP_DOCS)):
    if _f.endswith(".md") and _f not in md_files:
        os.remove(os.path.join(VP_DOCS, _f))

# ------------------------------------------------- 1a. 文献总览页（先生成到 staging，随正文一起过公式保护管线）
# 为什么必须进 MK_SRC：直写 VP_DOCS 会绕过 protect_math → fix_cjk_bold，
# markdown-it 会把公式里的 _ / * 当强调语法吃掉，MathJax 再也匹配不到定界符
# ——文献页首版正是这样出现下标与符号裸露的。
_REF_HEAD = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
_REF_START = re.compile(r"参考文献|文献锚定|参考资料|^参考$|^文献$")
_REF_ITEM = re.compile(r"^\s*(?:\d+[.)]|[-*+])\s+")
_REF_TOKEN = re.compile(
    r"arXiv[:\s]|DOI[:\s]|doi\.org|Phys\.\s*Rev\.|Phys\.Rev\.|Nature|Science|JHEP|"
    r"Commun\.\s*Math\.\s*Phys|Annals of Mathematics|Invent\.\s*Math|SIAM|Proc\.\s*R\.\s*Soc\.")
_REF_ID = re.compile(r"arXiv[:\s]*[\w\-./]+|10\.\d{4,9}/[^\s)）\]`，。；]+")


def _ref_linkify(s):
    """给文献条目里的 arXiv/DOI 标识加可点击外链（已有 markdown 链接则不动）。"""
    if "](http" in s:
        return s

    def _ar(m):
        aid = m.group(1)
        return "[arXiv:%s](https://arxiv.org/abs/%s)" % (aid, aid)

    def _doi(m):
        d = m.group(1).rstrip(".,;")
        return "[DOI:%s](https://doi.org/%s)" % (d, d)

    s = re.sub(r"arXiv:\s*([A-Za-z\-]+/\d{7}|\d{4}\.\d{4,5})", _ar, s)
    s = re.sub(r"DOI:\s*(10\.\d{4,9}/[^\s)）\]`，。；]+)", _doi, s)
    return s


def _plain_symbols(s):
    """把文献条目里的数学字母/下标换成常见字符，避免站点字体缺字（SL₂(ℝ) → SL2(R)）。"""
    table = {"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4",
             "₊": "+", "ℝ": "R", "ℂ": "C", "ℚ": "Q", "ℤ": "Z", "ℕ": "N"}
    for a, b in table.items():
        s = s.replace(a, b)
    return s


def _ref_items(buf):
    """参考文献段落 → 条目列表（表格行按「·」拼接，列表项去序号；不改写文字）。"""
    out, prev = [], None
    for raw in buf:
        s = raw.strip()
        if not s or s.startswith("---") or s.startswith("***"):
            continue
        if s.startswith("|"):
            cells = [c.strip() for c in s.strip("|").split("|")]
            if cells and all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
                continue
            cells = [c for c in cells if c]
            if not cells:
                continue
            s = " · ".join(cells)
        if s.startswith(">"):
            s = s.lstrip("> ").strip()
        m = _REF_ITEM.match(s)
        if m:
            out.append(_REF_ITEM.sub("", s, count=1).strip())
            prev = len(out) - 1
            continue
        if _REF_TOKEN.search(s):
            if prev is not None and out[prev].endswith(("，", "、", "（", "(")):
                out[prev] += " " + s
            else:
                out.append(s)
                prev = len(out) - 1
        elif prev is not None and (raw.startswith(("  ", "\t")) or len(out[prev]) < 120):
            out[prev] += " " + s
    seen, res = set(), []
    for x in out:
        if not x or x in seen:
            continue
        # 文献 = 体系外引用：排除内部文档指针、自引（Zenodo CNT）与“参见本库”类条目
        if ".md" in x or "核心文献参见" in x:
            continue
        if "ruster" in x.lower() or "10.5281/zenodo.20804380" in x:
            continue
        if re.match(r"^\s*(见|参见|相关文档|出处)", x):
            continue
        if ".lean" in x or "Lean源码" in x:
            continue
        # 必须带外部文献特征（arXiv/DOI/期刊/出版社/年份），否则视为内部条目
        if not re.search(r"arXiv|DOI|doi\.org|Phys\.|Nature|Science|JHEP|Commun\.|Annals|"
                         r"Invent\.|SIAM|Proc\.|Press|University|GTM|LNM|Cambridge|Springer|"
                         r"Academic|World Scientific|\((?:19|20)\d{2}[a-z]?\)", x):
            continue
        seen.add(x)
        res.append(_ref_linkify(_plain_symbols(x)))
    return res


def _extract_refs(txt):
    """返回 (条目列表, 章节标题列表)。"""
    lines = txt.splitlines()
    items, heads, i = [], [], 0
    while i < len(lines):
        m = _REF_HEAD.match(lines[i])
        if m and _REF_START.search(m.group(2).strip()):
            lvl = len(m.group(1))
            heads.append(m.group(2).strip())
            j = i + 1
            buf = []
            while j < len(lines):
                m2 = _REF_HEAD.match(lines[j])
                if m2 and len(m2.group(1)) <= lvl:
                    break
                buf.append(lines[j])
                j += 1
            items.extend(_ref_items(buf))
            i = j
        else:
            i += 1
    return items, heads


def _title_clean(s):
    """标题纯文本化：简单数学（G_N、A_4）保留内容，含 LaTeX 命令的式子整体丢弃。"""
    def _repl(m):
        body = m.group(1)
        return "" if "\\" in body else body
    s = re.sub(r"\$([^$]*)\$", _repl, s)
    s = re.sub(r"[：:]\s+", "：", s)
    return re.sub(r"\s{2,}", " ", s).strip(" ：")


def _brief_clean(t, limit=140):
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\*\*|`|^>\s*", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    m = re.search(r"^(.{20,}?[。！？])", t)
    if m:
        t = m.group(1)
    return t[:limit] + ("…" if len(t) > limit else "")


def _bad_brief(t):
    """简介质量闸：LaTeX 残片、公式堆、指代开头、中文过少、非完整句一律不采用。"""
    if "\\text{" in t or "\\begin{" in t or "CQMMATH" in t:
        return True
    if t.lstrip().startswith(("&", "\\", "和", "与", "但", "而", "即", "则",
                              "因此", "两者", "该", "此", "隐含条件", "其中",
                              "这里", "说明", "注：", "设")):
        return True
    if len(re.findall(r"[\u4e00-\u9fff]", t)) < 20:
        return True
    if len(re.findall(r"\$[^$]*\$", t)) > 2:
        return True
    if t.rstrip().endswith(("：", ":", "，", ",")):
        return True
    return not t.rstrip().endswith(("。", "！", "？", "…"))


def _doc_brief(txt, limit=140):
    """取文档简介：优先「定位 / 状态说明 / 摘要」引用块，否则首段正文。

    跳过标题、代码围栏、表格、列表与 $$…$$ 公式块（避免从公式中段截断，
    首版 D020 的简介曾截到 ``\\text{质量不是…``）。
    """
    lines = txt.splitlines()
    h1 = next((k for k, ln in enumerate(lines) if ln.strip().startswith("# ")), -1)
    if h1 >= 0:
        # 只认文档开头（h1 后 40 行内）的「摘要 / 状态说明」块；「定位注」常是
        # 正文深处的技术附注，不作简介。
        for i in range(h1 + 1, min(len(lines), h1 + 41)):
            s = lines[i].strip()
            if s.startswith(">") and ("摘要" in s or "状态说明" in s):
                buf, j = [], i
                while j < len(lines) and lines[j].strip().startswith(">"):
                    buf.append(lines[j].strip().lstrip(">").strip())
                    j += 1
                t = _brief_clean(" ".join(buf), limit)
                if len(t) >= 20 and not _bad_brief(t):
                    return t

    started, paras, cur, in_math, in_fence = False, [], [], False, False
    for ln in lines:
        s = ln.strip()
        if not started:
            if s.startswith("# "):
                started = True
            continue
        if s.startswith("```"):
            in_fence = not in_fence
            if cur:
                paras.append(cur)
                cur = []
            continue
        if in_fence:
            continue
        if s.startswith("$$"):
            in_math = not in_math
            if cur:
                paras.append(cur)
                cur = []
            continue
        if in_math:
            continue
        if not s or s.startswith(("#", "|", ">", "-", "*", "---")):
            if cur:
                paras.append(cur)
                cur = []
            continue
        if s.startswith("**作者**") or len(s) < 8:
            continue
        cur.append(s)
    if cur:
        paras.append(cur)
    for p in paras[:5]:
        t = _brief_clean(" ".join(p), limit * 3)
        if len(t) < 30 or t.rstrip().endswith(("：", ":", "，", ",")):
            continue          # 定义引子 / 公式残片，继续找下一段
        if _bad_brief(t):
            continue
        return _brief_clean(t, limit)
    return ""


def _ref_slug(h):
    return re.sub(r"\s+", "-", re.sub(r"[`*$]", "", h).strip())


def _sub_html(s):
    """表格纯文本标题里的简单下标（G_N、A_4）→ <sub>，避免下划线看着像乱码。"""
    return re.sub(r"([A-Za-z])_([A-Za-z0-9]+)", r"\1<sub>\2</sub>", s)


ref_sections, ref_ids, ref_counts = [], set(), {}
REF_SUM_PATH = os.path.join(ROOT08, "00_外部引用", "文献摘要.json")
REF_SUM = {}
if os.path.isfile(REF_SUM_PATH):
    try:
        with open(REF_SUM_PATH, "r", encoding="utf-8") as _fh:
            REF_SUM = json.load(_fh).get("items", {})
    except Exception as _e:
        print("[vp][warn] 文献摘要缓存不可读：%s" % _e)


def _norm_ref_key(s):
    s = re.sub(r"arXiv:\s*", "arXiv:", s.strip())
    s = re.sub(r"DOI:\s*", "DOI:", s)
    s = s.rstrip(".,;")
    if re.match(r"^10\.\d{4,9}/", s):
        s = "DOI:" + s
    return s
for _f in list(md_files):
    if _f == "index.md" or _f.startswith(("L", "V", "LEAN", "TERMS", "REFS")):
        continue
    _src = os.path.join(MK_SRC, _f)
    if not os.path.isfile(_src):
        continue
    with open(_src, "r", encoding="utf-8") as _fh:
        _txt = _fh.read()
    _refs, _heads = _extract_refs(_txt)
    if not _refs:
        continue
    _base = _f[:-3]
    _title = _base
    for _line in _txt.splitlines():
        _mm = re.match(r"^#\s+(.+?)\s*$", _line)
        if _mm:
            _title = _title_clean(_mm.group(1))
            break
    ref_sections.append((_base, _title, _refs, _doc_brief(_txt),
                         _ref_slug(_heads[0]) if _heads else ""))
    for _r in _refs:
        for _m in _REF_ID.finditer(_r):
            _k = _norm_ref_key(_m.group(0))
            ref_ids.add(_k)
            ref_counts[_k] = ref_counts.get(_k, 0) + 1

REF_TOTAL = sum(len(x[2]) for x in ref_sections)

# ---- 文献摘要：按被引用次数排序的 arXiv/DOI 论文卡片（题录+中文概括+原链接）
_sum_items = []
for _key, _v in REF_SUM.items():
    _n = ref_counts.get(_key, 0)
    if _n > 0 and (_v.get("summary_zh") or "").strip():
        _sum_items.append((_n, _key, _v))
_sum_items.sort(key=lambda t: (-t[0], -(t[2].get("year") or 0), t[1]))

# ---- 其他外部文献：无摘要，去重后只列题录与外链（不含任何站内跳转）
_other, _seen_ref = [], set()
for _base, _title, _refs, _brief, _anchor in ref_sections:
    for _r in _refs:
        _ids = [_norm_ref_key(m.group(0)) for m in _REF_ID.finditer(_r)]
        if any(i in REF_SUM for i in _ids):
            continue
        _k = re.sub(r"\s+", " ", _r).strip()
        if _k in _seen_ref:
            continue
        _seen_ref.add(_k)
        _other.append(_r)
_other.sort(key=lambda s: s.lower())

REF_MD = ["---", "title: 文献总览", "---", "", "# 文献总览", "",
          "本页只收录**体系外文献**（arXiv / DOI / 期刊论文 / 专著），不含本体系文档、Lean 源码与自引，"
          "也不提供站内文档跳转。共整理 **%d 篇带摘要的论文** 与 **%d 条其他外部文献**。"
          % (len(_sum_items), len(_other)), "",
          "使用说明：点击每条下方的 arXiv / DOI 链接可打开原始文献页面；"
          "概括据原文摘要转写，只作阅读定位，不替代原文。", ""]
if _sum_items:
    REF_MD += ["## 文献摘要（%d 篇）" % len(_sum_items), "",
               "按被引用次数排序；题录与概括据 arXiv / Crossref 公开元数据与原文摘要转写。", ""]
    for _n, _key, _v in _sum_items:
        _auth = _v.get("authors") or []
        _authors = "、".join(_auth[:3]) + (" 等" if len(_auth) > 3 else "")
        REF_MD.append(
            "<details open><summary><strong>%s</strong> · %s（%s）· 被 %d 条引用</summary>"
            "<p>概括：%s</p><p><a href=\"%s\" target=\"_blank\" rel=\"noreferrer\">%s</a></p></details>"
            % (html.escape(_v.get("title", ""), quote=False),
               html.escape(_authors, quote=False), _v.get("year", ""), _n,
               html.escape(_v.get("summary_zh", ""), quote=False),
               _v.get("url", ""), html.escape(_key, quote=False)))
        REF_MD.append("")
if _other:
    REF_MD += ["## 其他外部文献（%d 条，无摘要）" % len(_other), "",
               "以下条目未取得公开摘要，仅列题录与原始链接。", ""]
    REF_MD += ["- %s" % _r for _r in _other]
    REF_MD.append("")

with open(os.path.join(MK_SRC, "REFS_文献总览.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(REF_MD))
md_files = sorted(md_files + ["REFS_文献总览.md"])
print("[vp] 已写文献总览页（摘要 %d 篇 / 其他 %d 条 / 原引用 %d 条）"
      % (len(_sum_items), len(_other), REF_TOTAL))

# ---------------------------------------------------------------- 数学保护（构建期占位符）
# 为什么不能只靠 markdown-it 规则：VitePress 把 markdown-it 打包进自身 bundle，
# 拿到的插件实例行为不可控，实测公式里的 \\（LaTeX 换行）会被转义规则吃成
# <span>\</span>、_ 会被强调规则吃成 <em>，标签一旦插进公式，MathJax 就再也
# 匹配不到这对 $ 定界符，公式只能以 LaTeX 原文裸露。
# 因此改在 markdown 解析「之前」把公式整段换成纯 ASCII 占位符，构建完成后
# 再在产物（HTML / JS）里还原：HTML 里做 HTML 转义，JS 字符串里做 JSON 转义。
MATH_RE = re.compile(
    r'(?<!\\)\$\$[\s\S]+?(?<!\\)\$\$'          # 块级 $$...$$（可跨行）
    r'|(?<!\\)\$(?!\$)(?:[^$\n]|\\\$)+?(?<!\\)\$(?!\$)'   # 行内 $...$（不跨行）
)
MATH_STORE = {}
HEADING_RE = re.compile(r'^\s{0,3}#{1,6}[ \t]')     # 标题行原样保留（锚点 id 不被占位符污染）

# ---- MathJax 文本模式的转义兼容（只在数学区间内做） ----
# MathJax 的 \text{} 是**逐字文本模式**，不展开宏、也不认 \_ 与 \S：
# 实测 \text{unit\_cell} 渲染成 unit\_cell（反斜杠露出）、\text{（\S8）} 渲染成
# （\S8）、\text{GL(5)\to SU(5)} 渲染成 GL(5)\to SU(5)。这三种都是合法 LaTeX 写法
# （真 LaTeX 的文本模式里 \_ 是下划线、\S 是 §；\to 严格说属数学模式，但语料里
# 混写进了 \text{}），只是 MathJax 不支持。修法放在**显示层**：仅在数学区间的
# \text{} 类组体内把转义还原成其本义字符，语料/原稿一字不动。范围限定在组体内，
# 绝不碰数学模式（数学模式里 _ 是下标算子、\to 正常展开，改不得）。
TEXTMODE_GROUP_RE = re.compile(
    r'(\\(?:text|mbox|textrm|textit|textbf|textsf|texttt|operatorname)\{)'
    r'((?:[^{}]|\{[^{}]*\})*)(\})')
# 组体内需要还原的写法 → 本义字符（用正则加边界，避免 \top → →p、\Sigma → §igma）
TEXTMODE_MAP = [(r"\\_", "_"), (r"\\S(?![A-Za-z])", "§"),
                (r"\\rightarrow(?![A-Za-z])", "→"), (r"\\to(?![A-Za-z])", "→")]


def repair_text_mode(tex):
    """还原 \\text{} 类组体内的文本模式转义（\\_ → _、\\S → §、\\to → →）。"""
    fixed = [0]

    def repl(m):
        body = m.group(2)
        new = body
        for pat, v in TEXTMODE_MAP:
            new = re.sub(pat, v, new)
        if new != body:
            fixed[0] += 1
            return m.group(1) + new + m.group(3)
        return m.group(0)

    out = TEXTMODE_GROUP_RE.sub(repl, tex)
    return out, fixed[0]


def protect_math(text):
    """逐段保护公式；标题行跳过（标题里的公式量少，交给 markdown-it 侧规则兜底）。"""
    lines = text.split("\n")
    out, buf = [], []

    def flush():
        if not buf:
            return
        seg = "\n".join(buf)
        buf.clear()

        def repl(m):
            key = "CQMMATHPLCHOLDER%dEND" % len(MATH_STORE)
            body, nfix = repair_text_mode(m.group(0))
            if nfix:
                TEXT_MODE_FIXED[0] += nfix
            MATH_STORE[key] = body
            return key

        out.append(MATH_RE.sub(repl, seg))

    for ln in lines:
        if HEADING_RE.match(ln):
            flush()
            out.append(ln)
        else:
            buf.append(ln)
    flush()
    return "\n".join(out)


MATH_MISSED = set()
TEXT_MODE_FIXED = [0]      # 文本模式转义还原计数（构建日志用）


def restore_math(text, js=False):
    """把产物里的占位符还原成公式原文（.html 与真实 .json 文件用）。"""
    def repl(m):
        f = MATH_STORE.get(m.group(0))
        if f is None:
            MATH_MISSED.add(m.group(0))
            return m.group(0)
        return json.dumps(f, ensure_ascii=False)[1:-1] if js else html.escape(f, quote=False)

    return re.sub(r'CQMMATHPLCHOLDER\d+END', repl, text)


def _js_escape_plain(f):
    """单/双引号普通 JS 字符串的转义：反斜杠、引号、回车换行。"""
    return (f.replace("\\", "\\\\").replace("'", "\\'")
             .replace('"', '\\"').replace("\r", "\\r").replace("\n", "\\n"))


def restore_math_js(text):
    """页面 chunk 的占位符还原（上下文感知）。

    VitePress 页面 chunk 把内容放在**单引号** JS 字符串里（Vue 编译产物），
    pageData 则是 JSON.parse('…')。json.dumps 只转义双引号不转义单引号——
    LaTeX 素数记号 ζ'(s)、c'_n、|G'⟩ 里的撇号会提前终止单引号字符串，
    chunk 整体 SyntaxError → 路由动态 import 失败 → 页面 200 但内容 404。
    （2026-10-13：D003/D005/D010/D014/D017/D020/D028/D029/D030/D032/L001 共 11 页。）
    故逐字符扫描字符串上下文：
      - 普通字符串：转义 \\ ' " 与换行；
      - JSON.parse('…') 上下文：先 JSON 转义再对结果做 JS 层转义（双层）。
    """
    out = []
    i, n = 0, len(text)
    in_str = None
    json_ctx = False
    while i < n:
        c = text[i]
        if in_str:
            if c == "\\":
                out.append(text[i:i + 2]); i += 2; continue
            if c == in_str:
                in_str = None; out.append(c); i += 1; continue
            if text.startswith("CQMMATHPLCHOLDER", i):
                m = re.match(r"CQMMATHPLCHOLDER\d+END", text[i:])
                if m:
                    key = m.group(0)
                    f = MATH_STORE.get(key)
                    if f is None:
                        MATH_MISSED.add(key); out.append(key)
                    elif json_ctx:
                        t = json.dumps(f, ensure_ascii=False)[1:-1]
                        t = t.replace("\\", "\\\\").replace("'", "\\'")
                        out.append(t)
                    else:
                        out.append(_js_escape_plain(f))
                    i += len(key); continue
            out.append(c); i += 1; continue
        if c in ("'", '"'):
            in_str = c
            json_ctx = text[max(0, i - 11):i] == "JSON.parse("
            out.append(c); i += 1; continue
        out.append(c); i += 1; continue
    return "".join(out)


# ---------------------------------------------------------------- 站内 404 修复
# mkdocs_src 里的行内链接形如 [理论组织和形式化框架总览](./_src/08 .../README.html)——
# 那是 Material 站把所有源文档编译进 _src/ 后的地址。VitePress 不处理 '_' 前缀目录，
# 站内没有 _src/，于是这些链接全部 404。
# 站内本就有这些源文档的渲染版（F01/F02/…），故指过来；没有对应页面的（归档、
# LICENSE、元数据等）降级为纯文本，不留死链。
SRC_LINK_MAP = {
    "_src/08 理论组织和形式化框架/README": "/F02_README",
    "_src/08 理论组织和形式化框架/AGENTS": "/F01_AGENTS",
}
SRC_LINK_RE = re.compile(r'\[([^\]\n]+)\]\((\.?/?_src/[^)\s]+?)(\.html)?(#[^)]*)?\)')


def fix_src_links(txt):
    def repl(m):
        text, base, _ext, _anchor = m.group(1), m.group(2), m.group(3), m.group(4)
        key = base.lstrip("./")
        for prefix, target in SRC_LINK_MAP.items():
            if key.startswith(prefix):
                return "[%s](%s)" % (text, target)
        return text          # 无对应站内页面 → 去掉链接，保留文字

    return SRC_LINK_RE.sub(repl, txt)


# ---------------------------------------------------------------- 中文强调修复
# CommonMark 的强调 flanking 判定在中文标点处会误判：**“存在论相变”** 里，
# 左 ** 的右侧是“（标点）、左侧是汉字，被判为「不是左 flanking」而不能开强调；
# **可观察子群（observable subgroup）**问题 里，右 ** 的左侧是）（标点）、
# 右侧是汉字，同样不能闭。于是这些成对的 ** 被原样保留（实测 18 处）。
# Material 时代的 Python-Markdown 规则宽松，故此前不显。
# 处理：逐行把成对的 **…** 提前落成 <strong>…</strong>；跳过代码围栏，行内代码
# 先取走再放回，避免误伤。
FENCE_RE = re.compile(r'^\s*(?:```|~~~)')
INLINE_CODE_RE = re.compile(r'`[^`\n]*`')
BOLD_RE = re.compile(r'\*\*(?=\S)([^*\n]{1,300}?)(?<=\S)\*\*')
# 裸文本下标：U(1)_B、U(1)_{B-L}、G_N、K_L、A_4 这类没有写进 $…$ 的下标记号，
# 只要同段出现两个就会被 markdown-it 当斜体开闭配对，实测把
# 「U(1)_B、U(1)_B-L、U(1)_Y」渲染成「U(1)<em>B、U(1)</em>B-L、U(1)_Y」。
# 给这类下划线加反斜杠转义，输出仍是字面下划线，视觉不变。
BARE_SUB_RE = re.compile(r'(?<=[A-Za-z0-9)\]}])_(?=[A-Za-z0-9({])')
# URL 保护跨度：转义裸下标前先把 URL 整段取走。关键动因——markdown-it 的
# linkify 规则先于 emphasis 运行，裸 URL 会被整段吞成链接令牌，其中的 _ 若被
# 转义成 \_，反斜杠会泄漏进 href（实测 percent-encode 成 %5C，点击即 404）
# 与链接显示文本（字面 \_）。实证：D022 文献链接
# http://var.scholarpedia.org/article/Riemann_zeros_and_quantum_chaos 两处俱伤。
# 行内链接目标（[label](url)）里的 _ 不转义也安全：destination 解析器原样
# 收取，链接文本是 label 不受影响（D023 两例实证无恙）。故意不含 ) 排除：
# 维基式 URL 带平衡括号，宁多保护几个字符（还原是恒等，零风险）不可漏保护。
URL_SPAN_RE = re.compile(r'https?://[^\s<>\[\]"\'`]+')
# 行内代码包公式解包（展示层适配，源文档不动）：上游符号表惯用 `$☯$` 写法
# 防 markdown/MathJax 干扰，但 MathJax 的 skipHtmlTags 含 code，公式以原文露出
# （☯ 再被 emoji 字体彩色化）。反引号内只要出现完整的 $…$ / $$…$$ 段
# （含一段反引号包多个公式的形态，如 `$\mathrm{GL}(5)$ ⇒ $\mathrm{SU}(5)$`），
# 就去掉反引号，公式交还 MathJax。
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
CODE_MATH_HAS_RE = re.compile(r"\$\$[^$\n]+\$\$|\$[^$\n]+?\$")


def _unpack_code_math(m):
    inner = m.group(1)
    if CODE_MATH_HAS_RE.search(inner):
        return inner
    return m.group(0)


def fix_cjk_bold(txt):
    lines = txt.split("\n")
    out, in_fence = [], False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            out.append(ln)
            continue
        if in_fence:
            out.append(ln)
            continue
        codes = []
        urls = []

        def stash(m):
            codes.append(m.group(0))
            return "\x01C%d\x01" % (len(codes) - 1)

        def stash_url(m):
            urls.append(m.group(0))
            return "\x01U%d\x01" % (len(urls) - 1)

        ln2 = INLINE_CODE_RE.sub(stash, ln)
        ln2 = URL_SPAN_RE.sub(stash_url, ln2)   # URL 先于 BARE_SUB_RE 取走（见 URL_SPAN_RE 注释）
        ln2 = BOLD_RE.sub(lambda m: "<strong>%s</strong>" % m.group(1), ln2)
        # 标题行不转义裸下标：protect_math 原样保留标题（锚点 id 不被占位符污染），
        # 若此处把标题公式的 _ 转义成 \_（$G_N$ → $G\_N$），MathJax 渲染虽同形，
        # 但搜索索引（从 md 提取标题文本）与 aria-label 会带上反斜杠原文，
        # 用户即在搜索结果里看到「G\_N」——故标题行整体跳过 BARE_SUB_RE。
        if not HEADING_RE.match(ln):
            ln2 = BARE_SUB_RE.sub(lambda m: "\\_", ln2)     # 裸下标：转义 _ 而非配成斜体
        for i, c in enumerate(codes):
            ln2 = ln2.replace("\x01C%d\x01" % i, c)
        for i, u in enumerate(urls):
            ln2 = ln2.replace("\x01U%d\x01" % i, u)
        out.append(ln2)
    return "\n".join(out)


_MATHBB_MAP = {"R": "ℝ", "C": "ℂ", "Z": "ℤ", "Q": "ℚ", "N": "ℕ", "F": "𝔽",
               "P": "ℙ", "E": "𝔼", "H": "ℍ"}
_LATEX_SYM_MAP = {
    "supset": "⊃", "supseteq": "⊇", "subset": "⊂", "subseteq": "⊆",
    "in": "∈", "notin": "∉", "times": "×", "cdot": "·", "cdots": "⋯",
    "ldots": "…", "dots": "…", "to": "→", "rightarrow": "→", "Rightarrow": "⇒",
    "leftarrow": "←", "leftrightarrow": "↔", "Leftrightarrow": "⇔", "iff": "⇔",
    "cup": "∪", "cap": "∩", "le": "≤", "leq": "≤", "ge": "≥", "geq": "≥",
    "ne": "≠", "neq": "≠", "infty": "∞", "approx": "≈", "equiv": "≡",
    "sim": "∼", "propto": "∝", "pm": "±", "mp": "∓", "circ": "∘", "prime": "′",
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "Delta": "Δ",
    "epsilon": "ε", "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ",
    "Theta": "Θ", "iota": "ι", "kappa": "κ", "lambda": "λ", "Lambda": "Λ",
    "mu": "μ", "nu": "ν", "xi": "ξ", "Xi": "Ξ", "pi": "π", "Pi": "Π",
    "rho": "ρ", "sigma": "σ", "Sigma": "Σ", "tau": "τ", "upsilon": "υ",
    "phi": "φ", "Phi": "Φ", "varphi": "φ", "chi": "χ", "psi": "ψ", "Psi": "Ψ",
    "omega": "ω", "Omega": "Ω", "Gamma": "Γ", "nabla": "∇", "partial": "∂",
    "forall": "∀", "exists": "∃", "neg": "¬", "land": "∧", "lor": "∨",
    "langle": "⟨", "rangle": "⟩", "perp": "⊥", "oplus": "⊕", "otimes": "⊗",
}


def _latex_to_text(t):
    """把标题里的 LaTeX 摘成可读纯文本（仅对含 $ 的标题启用）。

    顺序敏感：先屏蔽 \\mathrm 等包装宏再做符号映射，否则解包后
    \\supset 与相邻字母粘连成 \\supsetDiff 被当成一个宏名（实测踩过）。"""
    t = re.sub(r"\\mathbb\{(\w)\}",
               lambda m: _MATHBB_MAP.get(m.group(1), m.group(1)), t)
    for w in ("mathrm", "mathcal", "mathfrak", "mathbf", "text", "operatorname"):
        t = t.replace("\\" + w, "\x01" + w)
    t = re.sub(r"\\([A-Za-z]+)",
               lambda m: _LATEX_SYM_MAP.get(m.group(1), m.group(1)), t)
    t = re.sub(r"\x01(?:[A-Za-z]+)\{([^{}]*)\}", r"\1", t)
    t = t.replace("{", "").replace("}", "").replace("\x01", "")
    # 二元符号两侧补空格，读起来不粘连
    t = re.sub(r"\s*([⊃⊇⊂⊆∈→⇒↔⇔×∪∩≤≥≠≈≡∼⊕⊗])\s*", r" \1 ", t)
    return t


def plain_title(t):
    """侧边栏/导航/浏览器标题是纯文本：不走 markdown-it（反斜杠转义不会被消化回 _）、
    不排 MathJax（$…$ 原样露出）。剥掉定界符并消化 BARE_SUB_RE 留下的转义；
    含 $ 的标题再做 LaTeX→Unicode 摘译，否则侧边栏出现
    「$G\\_N$ 第一性推导」「\\mathrm{Sym}\\supset…」这类字面残骸。"""
    had_math = "$" in t
    t = t.replace("\\_", "_")
    t = t.replace("$", "")
    if had_math:
        t = _latex_to_text(t)
    return re.sub(r"\s{2,}", " ", t).strip()


def unify_h1(txt):
    """展示层适配：每页仅保留首个 h1，后续 h1 降为 h2（仅 staging，源文档不动）。

    动因：D019 源稿用 h1 标四大部分（数学事实层/框架内定理/启发式构造/推导链
    总览），连同页标题共 5 个 h1——一页双标题违 HTML 文档大纲语义（根节点唯一），
    侧边大纲也把「第一部分」与页标题并列成两级根。站点层统一为单 h1：页标题留
    任 h1，四个部分标题降为 h2。源稿的四部分并列关系在大纲里完整保留，只是不再
    与页标题争位；标题文字与锚点 id 不变（id 由文字生成，与层级无关），页内锚点
    链接不受影响。降级只动 # 前缀，围栏内的 # 注释（如 F01 的 shell 片段）不误伤。
    """
    out, seen, n, in_fence = [], False, 0, False
    for ln in txt.split("\n"):
        s = ln.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            out.append(ln)
            continue
        if not in_fence:
            m = re.match(r"^(#{1,6})(\s.*)$", ln)
            if m and len(m.group(1)) == 1:
                if seen:
                    ln = "##" + m.group(2)
                    n += 1
                else:
                    seen = True
        out.append(ln)
    return "\n".join(out), n


def wrap_vpre(txt):
    """把正文整体放进 <div v-pre>，避免正文里的 {{ }} 被 Vue 当成插值编译。

    VitePress 会把 markdown 编译成 Vue SFC；物理文档里出现 {{ / }} 或 \\u 序列时
    会被 @vue/compiler-core 解析报错（曾试过把 {{ }} 转 HTML 实体，但源文本里
    还有 \\{\\{ 之类的写法，实体替换覆盖不全，仍会报 "Interpolation end sign
    was not found"）。整页 v-pre 是唯一能彻底关闭插值编译的办法。

    代价：所有 h2/h3/p 会变成 .vp-doc 的孙节点而非直接子块。因此增强脚本里的
    contentRoot() 会逐层下潜到真正承载标题的容器，深度滑杆才能正常按块工作。
    若文件带 YAML frontmatter，则保留 frontmatter，只包裹正文。
    """
    lines = txt.split("\n")
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is not None:
            fm = "\n".join(lines[:end + 1])
            body = "\n".join(lines[end + 1:])
            return fm + "\n\n<div v-pre>\n\n" + body + "\n\n</div>\n"
    return "<div v-pre>\n\n" + txt + "\n\n</div>\n"


wrapped = 0
demoted_total = 0
for f in md_files:
    with open(os.path.join(MK_SRC, f), "r", encoding="utf-8") as fh:
        txt = fh.read()
    # VitePress 的静态资源根是 public/，viz 从 assets/viz/ 迁到 /viz/
    txt = txt.replace("assets/viz/", "/viz/")
    txt = fix_src_links(txt)         # 消除指向 _src/ 的失效链接
    # 展示层适配（仅 staging，源文档不动）：code 包公式解包 + emoji 字符单色化
    txt = CODE_SPAN_RE.sub(_unpack_code_math, txt)
    txt = txt.replace("✅", "✓").replace("❌", "✗")
    if f != "index.md":
        txt, demoted = unify_h1(txt)   # 多 h1 页统一为单 h1（D019 四部分降 h2）
        demoted_total += demoted
        txt = protect_math(txt)      # 公式先换成占位符，躲开 markdown-it
        txt = fix_cjk_bold(txt)      # 中文标点旁的 **…** 落成 <strong>…</strong>
        # <title> 修复：h1 里带公式时，VitePress 从渲染后的 DOM 提取标题，
        # 数学部分（MathJax SVG/辅助 MML）不产生正常文本节点 → 浏览器标题栏
        # 要么丢掉 G_N 要么变成「G N」（NBSP）。凡 h1 含 $ 且无 frontmatter 的，
        # 注入纯文本 title。必须在 fix_cjk_bold 之后：否则注入的 G_N 会被
        # BARE_SUB_RE 再转义成 G\_N，而 YAML 双引号里 \_ 是 NBSP 转义。
        if not txt.startswith("---"):
            m_h1 = re.search(r"^#\s+(.+?)\s*$", txt, re.M)
            if m_h1 and "$" in m_h1.group(1):
                clean = plain_title(m_h1.group(1))
                if clean:
                    txt = "---\ntitle: %s\n---\n\n" % json.dumps(clean, ensure_ascii=False) + txt
        txt = wrap_vpre(txt)
        wrapped += 1
    with open(os.path.join(VP_DOCS, f), "w", encoding="utf-8") as fh:
        fh.write(txt)
print("[vp] 已复制 %d 个 markdown 页面（其中 %d 页套 v-pre，%d 个后续 h1 降为 h2）"
      % (len(md_files), wrapped, demoted_total))

# ---------------------------------------------------------------- 1b. 构建期统计（全部实测）
# 红线（不虚构 / 可复现）：首页特性卡、Lean 页、术语总览页与侧栏里出现的每一个计数，
# 都必须在构建期从源文件实测读出——脚本正文不得再写死数字。口径与 _build/check_consistency.py
# 完全一致（同源、同算法），避免两处漂移：
#   01_结构化数据/{概念表,命题表,论证表,缺口编号对照}.csv
#   09_桥接与翻译/符号对照表.csv · 00_外部引用/证据映射.csv
#   03_超图与理论图/知识图谱.json · 04_Lean对接/{Lean结构提取/*,Lean↔概念映射.csv}
S00 = os.path.join(ROOT08, "00_外部引用")
S01 = os.path.join(ROOT08, "01_结构化数据")
S03 = os.path.join(ROOT08, "03_超图与理论图")
S04 = os.path.join(ROOT08, "04_Lean对接")
S09 = os.path.join(ROOT08, "09_桥接与翻译")


def _csv_rows(path):
    """读源 CSV（utf-8-sig）：BOM 与引号内换行交给 csv 模块，不按物理行数偷懒。"""
    if not os.path.isfile(path):
        sys.exit("[vp][FATAL] 统计源缺失：%s（数字必须实测，不接受写死或默认值）" % path)
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def _json_read(path):
    if not os.path.isfile(path):
        sys.exit("[vp][FATAL] 统计源缺失：%s（数字必须实测，不接受写死或默认值）" % path)
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _thousands(n):
    """1388 → '1 388'：沿用站内既有的「千位用空格」排版。"""
    return "{:,}".format(n).replace(",", " ")


_concepts = _csv_rows(os.path.join(S01, "概念表.csv"))
_concept_ids = {(r.get("concept_id") or "").strip() for r in _concepts}
_lean_map = _csv_rows(os.path.join(S04, "Lean↔概念映射.csv"))
_lean_decls = _json_read(os.path.join(S04, "Lean结构提取", "declarations.json"))
_kg_json = _json_read(os.path.join(S03, "知识图谱.json"))
_covered = set()
for _row in _lean_map:
    for _cid in (_row.get("concept_ids") or "").split(";"):
        _cid = _cid.strip()
        if _cid in _concept_ids:
            _covered.add(_cid)

STATS = {
    "concept": len(_concepts),
    "prop": len(_csv_rows(os.path.join(S01, "命题表.csv"))),
    "arg": len(_csv_rows(os.path.join(S01, "论证表.csv"))),
    "gap": len([r for r in _csv_rows(os.path.join(S01, "缺口编号对照.csv"))
                if (r.get("gap_code") or "").strip()]),
    "symbol": len(_csv_rows(os.path.join(S09, "符号对照表.csv"))),
    "evidence": len(_csv_rows(os.path.join(S00, "证据映射.csv"))),
    "kg_node": len(_kg_json["nodes"]),
    "kg_edge": len(_kg_json["edges"]),
    "lean_module": len(_csv_rows(os.path.join(S04, "Lean结构提取", "模块清单.csv"))),
    "lean_decl": len(_lean_decls),
    "lean_axiom": len([d for d in _lean_decls if (d.get("kind") or "") == "axiom"]),
    "lean_map": len(_lean_map),
    "lean_cover": len(_covered),
}
STATS["lean_decl_txt"] = _thousands(STATS["lean_decl"])


def _glossary_stats():
    """术语总览的真实条数/分类：读 build_reader_site.py stage 出的 window.CQM_GLOSSARY
    （index = 检索索引，terms = 悬浮卡，index 每项的 ty = 分类）。

    取数顺序（前者是后者的复制源，避免读到上一轮留下的陈旧副本）：
      1) _build/mkdocs_src/docs/assets/cqm-glossary.js —— 阅读站 stage 产物（唯一源）
      2) docs/public/cqm-glossary.js                   —— 本脚本第 2 步复制出的副本
      3) .vitepress/dist/cqm-glossary.js               —— 上一次构建的产物
    三个都不存在时给出可执行报错（点名 build_reader_site.py），不抛裸栈。"""
    cands = [os.path.join(MK_SRC, "assets", "cqm-glossary.js"),
             os.path.join(VP_PUBLIC, "cqm-glossary.js"),
             os.path.join(VP_CFG_DIR, "dist", "cqm-glossary.js")]
    for path in cands:
        if not os.path.isfile(path):
            continue
        with open(path, "r", encoding="utf-8") as fh:
            txt = fh.read()
        key = "window.CQM_GLOSSARY="
        pos = txt.find(key)
        if pos < 0:
            sys.exit("[vp][FATAL] %s 里找不到 `window.CQM_GLOSSARY=`，无法实测术语条数" % path)
        payload = txt[pos + len(key):].strip()
        if payload.endswith(";"):
            payload = payload[:-1]
        try:
            gl = json.loads(payload)
        except ValueError as exc:
            sys.exit("[vp][FATAL] %s 不是合法 JSON：%s" % (path, exc))
        items = gl.get("index") or []
        seen, first = {}, []
        for it in items:
            ty = (it or {}).get("ty") or ""
            if not ty:
                continue
            if ty not in seen:
                seen[ty] = 0
                first.append(ty)
            seen[ty] += 1
        # 既有分类固定展示顺序，其余类别（日后新增的）按首次出现顺序追加——不会再漏类别
        pref = ["概念", "缺口", "论证", "符号", "命题", "文档", "链条步", "讲稿"]
        cats = [c for c in pref if c in seen] + [c for c in first if c not in pref]
        return path, items, len(gl.get("terms") or {}), [(c, seen[c]) for c in cats]
    sys.exit("[vp][FATAL] 未找到术语总览数据 cqm-glossary.js（候选：%s、%s、%s）——"
             "请先在 _build/ 下运行 build_reader_site.py 生成悬浮卡与检索索引。"
             % tuple(cands))


_glossary_path, _glossary_index, _glossary_terms, _glossary_cats = _glossary_stats()
STATS["glossary_index"] = len(_glossary_index)
STATS["glossary_terms"] = _glossary_terms
STATS["glossary_cats"] = " · ".join("%s %d" % (c, n) for c, n in _glossary_cats)

print("[vp] 构建期实测：概念 %(concept)d · 命题 %(prop)d · 论证 %(arg)d · 缺口 %(gap)d · "
      "符号 %(symbol)d · 证据 %(evidence)d · 图谱 %(kg_node)d 实体/%(kg_edge)d 边 · "
      "Lean %(lean_module)d 模块/%(lean_decl)s 声明（axiom %(lean_axiom)d）· 映射 %(lean_map)d 条 · "
      "覆盖 %(lean_cover)d/%(concept)d 概念 · 术语索引 %(glossary_index)d 条/悬浮卡 %(glossary_terms)d 张"
      % STATS)
print("[vp] 术语数据源：%s；分类：%s" % (_glossary_path, STATS["glossary_cats"]))

# ---------------------------------------------------------------- 2. 静态资源 -> public/
mk_assets = os.path.join(MK_SRC, "assets")
if os.path.isdir(mk_assets):
    for name in os.listdir(mk_assets):
        s = os.path.join(mk_assets, name)
        d = os.path.join(VP_PUBLIC, name)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
    print("[vp] 已复制静态资源（含 viz/）到 public/")
else:
    print("[vp] 警告：未找到 %s，viz iframe 可能失效" % mk_assets)

# viz 内 HTML 的相对资源引用改写（只改 public/ 下的副本，源文件不动）：
#   源 HTML 写 assets/cytoscape.min.js，但 public/viz/ 下依赖是平铺的
#   （cytoscape.min.js / 驾驶舱数据.json），不改写会 404 → 超图页空白。
VIZ_FIX = (
    ('src="assets/cytoscape.min.js"', 'src="cytoscape.min.js"'),
    ("src='assets/cytoscape.min.js'", "src='cytoscape.min.js'"),
    ('href="assets/cytoscape.min.js"', 'href="cytoscape.min.js"'),
    ('src="data.json"', 'src="驾驶舱数据.json"'),
    ('"data.json"', '"驾驶舱数据.json"'),
    # ✅/❌ 彩色 emoji 字形与全站单色口径不符，统一替换单色 ✓/✗
    ("✅", "✓"),
    ("❌", "✗"),
)
# viz 页面（检索台 / 驾驶舱 / 超图 / 蓝图）是自包含 HTML，本身不带 MathJax，
# 而它们的正文（尤其检索台的实体/证据卡）里有大量 $…$ 公式——是 JS 运行时生成的，
# 构建期静态扫描看不到，打开页面就是一片 LaTeX 原文。
# 这里给它们注入本地 MathJax 与一个「DOM 变化后自动重排」的钩子
# （检索台的结果是点击/输入后动态渲染的，只在 DOMContentLoaded 排一次不够）。
VIZ_MATH = r"""<style>
/* 与 vp-read.css 第 8/9 条同源（viz 页面不加载 vp-read.css 故单独内联）：
   ① 剔除 emoji 字体并补 Segoe UI Symbol——公式内 MathJax SVG 未知字符
     （☯、中文、中文标点）与正文裸符号一律单色、与站点字体栈一致；
   ② @font-face 把 ☯/卦符定向到本机单色符号字体。 */
@font-face {
  font-family: "CQM Symbols Mono";
  src: local("Segoe UI Symbol");
  unicode-range: U+262F, U+2630-2636;
}
body {
  font-family: "CQM Symbols Mono", "Punctuation SC", "Inter", ui-sans-serif,
    system-ui, "Segoe UI Symbol", "Noto Sans Symbols 2", sans-serif !important;
}
mjx-container svg text {
  font-family: "CQM Symbols Mono", "Punctuation SC", "Inter", ui-sans-serif,
    system-ui, "Segoe UI Symbol", "Noto Sans Symbols 2", sans-serif;
}
</style>
<script src="/vp-math.js"></script>
<script>
(function () {
  // 少数数据引文是从多行 $$…$$ 公式块里截出的单行，丢了 $ 定界符（证据映射里 7 条，
  // 如「\text{GL(5) 潜能先在}」），MathJax 不会碰 → LaTeX 原文裸露。排版前给这类
  // 纯文本节点补上行内定界符。判据保守：节点无 $、含确定属公式的宏、花括号配平。
  var BARE = /\\(?:text|boxed|xrightarrow|xRightarrow|frac|underbrace)\b/;
  function wrapBare() {
    if (!document.body) return;
    var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    var n, todo = [];
    while ((n = w.nextNode())) {
      var s = n.nodeValue || "";
      if (s.indexOf("\\") < 0 || s.indexOf("$") >= 0) continue;
      if (!BARE.test(s)) continue;
      var p = n.parentNode;
      if (!p || (p.closest && p.closest("mjx-container,code,pre,script,style,textarea"))) continue;
      todo.push(n);
    }
    for (var i = 0; i < todo.length; i++) {
      var t = todo[i], v = t.nodeValue, core = v.trim();
      if (!core) continue;
      if (core.split("{").length !== core.split("}").length) continue;  // 截断片段不动
      var at = v.indexOf(core);
      t.nodeValue = v.slice(0, at) + "$" + core + "$" + v.slice(at + core.length);
    }
  }
  function typeset() {
    if (!window.MathJax || !window.MathJax.typesetPromise) return null;
    wrapBare();
    try { return window.MathJax.typesetPromise(); } catch (e) { return null; }
  }
  function boot() { setTimeout(typeset, 300); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
  var timer = null, busy = false;
  new MutationObserver(function () {
    if (busy || timer) return;
    timer = setTimeout(function () {
      timer = null;
      if (busy) return;
      busy = true;
      var p = typeset();
      if (p && p.then) p.then(function () { busy = false; }, function () { busy = false; });
      else busy = false;
    }, 400);
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
</script>
"""

viz_dir = os.path.join(VP_PUBLIC, "viz")
viz_fixed = 0
viz_math = 0
if os.path.isdir(viz_dir):
    for name in os.listdir(viz_dir):
        if not name.lower().endswith(".html"):
            continue
        p = os.path.join(viz_dir, name)
        with open(p, "r", encoding="utf-8") as fh:
            txt = fh.read()
        before = txt
        for a, b in VIZ_FIX:
            txt = txt.replace(a, b)
        if "tex-svg.js" not in txt:
            if "</head>" in txt:
                txt = txt.replace("</head>", VIZ_MATH + "</head>", 1)
            else:
                txt = VIZ_MATH + txt
            viz_math += 1
        if txt != before:
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(txt)
            viz_fixed += 1
print("[vp] viz 资源引用改写：%d 个 HTML 被修正；注入 MathJax：%d 个页面" % (viz_fixed, viz_math))

# ---------------------------------------------------------------- 3. 品牌色覆盖
BRAND_CSS = """/* CQM 研究站：对齐参考站 VitePress 观感，品牌色靛蓝 #3451b2 */
:root {
  --vp-c-brand: #3451b2;
  --vp-c-brand-light: #4662c4;
  --vp-c-brand-lighter: #5573d6;
  --vp-c-brand-dark: #2c4395;
  --vp-c-brand-darker: #22347a;
  --vp-c-brand-1: #3451b2;
  --vp-c-brand-2: #4662c4;
  --vp-c-brand-3: #5573d6;
  --vp-c-brand-soft: rgba(52, 81, 178, 0.14);
}
.dark {
  --vp-c-brand-1: #5c74d8;
  --vp-c-brand-2: #6d84e2;
  --vp-c-brand-3: #7e94ec;
  --vp-c-brand-soft: rgba(92, 116, 216, 0.16);
}
"""
with open(os.path.join(VP_PUBLIC, "vp-brand.css"), "w", encoding="utf-8") as fh:
    fh.write(BRAND_CSS)

# ------------------------------------------------- 3c2. 阅读体验增强（纯 CSS，随站自带）
# 依据：本项目公式密集、正文含大量表格与中文长段落。VitePress 内置表格横向滚动、
# 目录高亮、代码复制，但**长公式会撑破版心**（MathJax 生成的 SVG 默认不换行、
# 不加滚动条），中文长段落的行高与段距也偏紧。这里只补这几处，不覆盖主题默认样式。
READ_CSS = """/* CQM 研究站 · 阅读体验增强 */
/* 1) 公式：长公式横向滚动，不撑破版心（含块级与行内） */
mjx-container {
  overflow-x: auto;
  overflow-y: hidden;
  max-width: 100%;
  margin: auto 2px -2px;
}
mjx-container[display="true"] {
  display: block;
  padding: 2px 0;
}
mjx-container > svg { display: inline-block; }
/* 2) 卡片与检索结果里的公式同样限宽 */
.cqm-pop mjx-container, .cqm-res mjx-container { max-width: 100%; }
/* 3) 中文长段落：行高与段距放宽，标题前留白，便于长文档阅读 */
.vp-doc { line-height: 1.9; }
.vp-doc p { margin: 1em 0; }
.vp-doc li { margin: 0.35em 0; line-height: 1.85; }
.vp-doc h2 {
  margin-top: 2.4em;
  padding-top: 0.5em;
  border-top: 1px solid var(--vp-c-divider);
}
.vp-doc h3 { margin-top: 1.8em; }
.vp-doc h4 { margin-top: 1.4em; }
.vp-doc blockquote {
  border-left: 3px solid var(--vp-c-brand-1);
  background: var(--vp-c-bg-soft);
  padding: 2px 16px;
  border-radius: 0 6px 6px 0;
}
/* 4) 表格：GitHub 模式——按内容撑开、超出容器则在表格内横向滚动。
     此前缺 max-width 与 overflow，宽表（实测 8750px）把整页撑出横向滚动。 */
.vp-doc table {
  display: block;
  width: max-content;
  max-width: 100%;
  overflow-x: auto;
}
.vp-doc table th, .vp-doc table td { min-width: 5.5em; word-break: keep-all; overflow-wrap: anywhere; }
.vp-doc table th:first-child, .vp-doc table td:first-child { white-space: nowrap; }
/* 4b) 展开链「一步一读」：源自源文档表格行的逐字片段还原成的原表行。
     内容应换行（不是横向滚动）、首列不做 nowrap（可能是整句），
     用细分隔线而非默认粗边框，避免与正文数据表混淆。 */
.vp-doc table.cqm-fragtbl { display: table; width: auto; max-width: 100%; margin: 0.4em 0 0.9em; }
.vp-doc table.cqm-fragtbl td {
  min-width: 0; padding: 3px 10px; vertical-align: top;
  border: 1px solid var(--vp-c-divider); line-height: 1.7;
}
.vp-doc table.cqm-fragtbl td:first-child { white-space: normal; color: var(--vp-c-text-2); }
/* 5) 锚点跳转：标题不被顶部导航遮挡，落点给一次高亮，便于定位 */
.vp-doc h1, .vp-doc h2, .vp-doc h3, .vp-doc h4 { scroll-margin-top: 84px; }
.vp-doc :target { background: var(--vp-c-brand-soft); border-radius: 4px; }
/* 6) 搜索跳转后的关键词高亮 */
mark.cqm-hl { background: #ffe58f; color: inherit; padding: 0 1px; border-radius: 2px; }
.dark mark.cqm-hl { background: #6b5a12; color: #fff; }
/* 6b) 正文字号三档（导航栏 A 按钮循环切换，localStorage 记忆） */
:root { --cqm-font-scale: 1; }
.vp-doc { font-size: calc(16px * var(--cqm-font-scale)); }
/* 7) 长文档仪表：页顶阅读进度 + 回到顶部 */
.cqm-progress {
  position: fixed; left: 0; top: 0; height: 3px; width: 0;
  background: var(--vp-c-brand-1); z-index: 100;
  transition: width .08s linear;
}
.cqm-top {
  position: fixed; right: 22px; bottom: 26px; width: 38px; height: 38px;
  display: flex; align-items: center; justify-content: center;
  border-radius: 50%; border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-alt); color: var(--vp-c-text-1);
  cursor: pointer; font-size: 16px; z-index: 60;
  opacity: 0; pointer-events: none; transition: opacity .2s;
}
.cqm-top[data-on="1"] { opacity: .92; pointer-events: auto; }
.cqm-top:hover { background: var(--vp-c-brand-soft); }
@media print { .cqm-progress, .cqm-top { display: none; } }
/* 8+9) 全站符号与公式未知字符字体修正：
      VitePress 默认栈把 emoji 字体排在 sans-serif 之前，后果：
      ① ☯ / ✅ / ❌ 等「默认 emoji 表现」字符被渲染成彩色 emoji；
      ② → / ⇒ 等箭头被 emoji 字体的粗黑字形接管（"箭头变普通版"）；
      ③ MathJax SVG 对认识不了的字符（☯、\text{} 内中文、中文标点）
        以 <text font-family="serif"> 通用衬线回退，观感突兀。
      处置：基础栈**剔除全部 emoji 字体**、显式补入 Segoe UI Symbol
      （本机自带，含 ☯ / 卦符 / ⚠ 等单色字形）；公式内 <text> 同样覆盖。
      @font-face + unicode-range 再加一道保险：即便前面某字体含 ☯，
      也强制这几个码点走 Segoe UI Symbol 的单色形。
      SVG presentation attribute 优先级低于任何 CSS 规则；
      已知数学字形（path 绘制）不受影响。 */
@font-face {
  font-family: "CQM Symbols Mono";
  src: local("Segoe UI Symbol");
  unicode-range: U+262F, U+2630-2636;
}
:root {
  --vp-font-family-base: "CQM Symbols Mono", "Punctuation SC", "Inter",
    ui-sans-serif, system-ui, "Segoe UI Symbol", "Noto Sans Symbols 2",
    sans-serif !important;
}
mjx-container svg text {
  font-family: "CQM Symbols Mono", "Punctuation SC", "Inter", ui-sans-serif,
    system-ui, "Segoe UI Symbol", "Noto Sans Symbols 2", sans-serif;
}
"""
with open(os.path.join(VP_PUBLIC, "vp-read.css"), "w", encoding="utf-8") as fh:
    fh.write(READ_CSS)

# ------------------------------------------------- 3b. 本地 MathJax（四套分隔符，离线）
# 不依赖 markdown-it-mathjax3（它会拉 CDN），改用随站复制到 public/ 的本地 tex-svg.js。
# 必须同时支持两套分隔符：
#   $…$ / $$…$$       —— 正文（源 md 写法）
#   \(…\) / \[…\]     —— 术语悬浮卡与证据引文（这些文字来自结构化数据，
#                        是 Material 时代 arithmatex 转出的写法，实测 140 + 7 处）
# 只配 $ 会让卡片里的公式全部以 LaTeX 原文露出。
MATH_JS = """window.MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
    processEscapes: true,
    // 语料里 21 处 \\xRightarrow 是「重组实现」用的双线箭头；它不是 MathJax 内置宏
    // （bundle 里只有 \\xrightarrow）。本包 tex-svg.js 带 noundefined 扩展，未定义宏
    // 不报错而是把宏名以红字**字面**排出来（实测页面显示红色的 \\xRightarrow），
    // 故在此补定义：等价于带标签的双线箭头，与 \\xrightarrow 的观感一致。
    macros: {
      xRightarrow: ["\\\\overset{#1}{\\\\Longrightarrow}", 1]
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
      /^(10\\.|192\\.168\\.|172\\.(1[6-9]|2\\d|3[01])\\.)/.test(h);

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
"""
with open(os.path.join(VP_PUBLIC, "vp-math.js"), "w", encoding="utf-8") as fh:
    fh.write(MATH_JS)

# ------------------------------------------------- 3c. VitePress 版交互增强
# 与 Material 版（cqm-enhance.js）同源，但适配 VitePress：
#   正文容器 .vp-doc（原 article.md-content__inner）
#   导航容器 .VPNavBar（原 .md-header__inner）
#   快捷键 Ctrl+Shift+K（避开 VitePress 自带搜索的 Ctrl+K）
#   拆成 initOnce（全局单例：弹卡/检索框/快捷键/导航按钮/探测徽标）
#   与 initPage（每页：术语标注 + 深度滑杆），由 theme/index.js 在路由切换后重跑。
VP_ENHANCE_JS = r'''(function () {
  var G = window.CQM_GLOSSARY; if (!G) return;
  var POP, cur = null, pinned = false, overPop = false;
  var BOX, MASK, INP, RES, SEL = 0, F = { ty: "", q: "" };
  var bound = false;

  /* ---------- 悬浮卡（全局单例） ----------
     交互语义（pinned = 点击固定，overPop = 鼠标在卡上）：
       · 悬停词 → 弹出；移出词（且未固定）→ 消失
       · 点击词 → 弹出并固定（移出词不消失）；再点击同一词 → 取消固定并消失
       · 已固定 → 鼠标移到别的词上不切换（"已经弹出就不变"）
       · 词内部子元素间移动不触发隐藏/重弹（relatedTarget 仍在同一元素内） */
  function ensurePop() {
    if (POP) return POP;
    POP = document.createElement("div");
    POP.className = "cqm-pop"; POP.style.display = "none";
    document.body.appendChild(POP);
    POP.addEventListener("mouseenter", function () { overPop = true; });
    POP.addEventListener("mouseleave", function () { overPop = false; if (!pinned) hidePop(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") { pinned = false; hidePop(); } });
    window.addEventListener("scroll", function () { if (!pinned) hidePop(); }, { capture: true, passive: true });
    return POP;
  }
  var hideTimer = null;   // mouseout 的延迟隐藏定时器（必须可撤销，否则旧定时器会把新弹出的卡打掉）
  var rendered = {};      // 已排版卡内容缓存：key -> 卡 DOM 副本，二次悬停零空窗
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
    // 卡文逐字取自 CSV：✅/❌ 是彩色 emoji 字形，统一替换单色 ✓/✗（与全站口径一致）
    return String(html).replace(/✅/g, "\u2713").replace(/❌/g, "\u2717").replace(/`([^`\n]+)`/g, function (m, s) {
      return "<code>" + s.replace(/[&<>]/g, function (c) { return ESC[c]; }) + "</code>";
    });
  }
  function showPop(el) {
    var key = el.getAttribute("data-cqm");
    var html = G.terms[key];
    if (!html) return;
    var p = ensurePop();
    cur = el;
    p.style.display = "block"; p.style.left = "-9999px"; p.style.top = "0";
    if (rendered[key]) {
      // 命中排版缓存：直接装填已排版的 HTML 并定位，跳过 MathJax 重排
      // （否则二次悬停会有几十~几百 ms 的不可见空窗，观感即"弹出时闪一下"）。
      // 注意缓存的是 innerHTML 字符串而非克隆 DOM——克隆整个 .cqm-pop 容器
      // 会把 fixed 定位与 -9999px 一起嵌进卡内，内容整体飞出屏幕（弹卡"消失"）。
      p.innerHTML = rendered[key];
      place(p, el);
      return;
    }
    p.innerHTML = cardHtml(html);
    typeset(p, function () {
      if (cur !== el) return;   // 排版期间目标已换词，丢弃本次结果
      if (Object.keys(rendered).length > 80) rendered = {};  // 缓存上限防膨胀
      rendered[key] = p.innerHTML;
      place(p, el);
    });
  }
  document.addEventListener("mouseover", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (!el) return;
    var from = e.relatedTarget;
    if (from && el.contains(from)) return;   // 同一元素内部移动，不当作重新进入
    // 滑到新词：先撤销前一个词 mouseout 排下的延迟隐藏，
    // 否则它会在此刻到期，把刚弹出的卡打掉（弹出的"闪一下"）
    if (hideTimer) { clearTimeout(hideTimer); hideTimer = null; }
    if (pinned) return;   // 已点击固定：鼠标移动不改变已弹出的卡（"已经弹出就不变"）
    if (el === cur) return;   // 已是当前词：不重复弹出
    showPop(el);
  });
  document.addEventListener("mouseout", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (!el) return;
    var to = e.relatedTarget;
    if (to && el.contains(to)) return;   // 仍在同一元素内部移动，不算移出词
    if (pinned) return;   // 已点击固定：移出词不隐藏
    if (hideTimer) clearTimeout(hideTimer);
    hideTimer = setTimeout(function () {
      hideTimer = null;
      if (!pinned && !overPop) hidePop();
    }, 180);
  });
  document.addEventListener("focusin", function (e) {
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (el && !pinned && el !== cur) showPop(el);   // 键盘聚焦词：弹出（固定态下不切换）
  });
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest(".cqm-pop a");
    if (a) return;
    if (e.target.closest && e.target.closest(".cqm-pop")) return;   // 点击卡片内部：不处理（可正常选中文字/点链接）
    var el = e.target.closest && e.target.closest("[data-cqm]");
    if (el) {
      e.preventDefault();
      if (cur === el && POP && POP.style.display !== "none") {
        pinned = false; hidePop();
      } else {
        pinned = true; showPop(el);
      }
      return;
    }
    // 点击词与卡片以外的区域：取消固定并隐藏
    if (pinned) { pinned = false; hidePop(); }
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
  /* 结果摘要的内联渲染：加粗、行内代码、公式。
     公式必须先摘成占位符再做关键词高亮——否则 mark 会把 $…$ 内部切开，
     MathJax 就匹配不到定界符（实测「量纲」查询下 20 处 **、6 处 $ 字面残留）。 */
  function sbRender(text, toks) {
    var t = esc(text || "");
    var math = [];
    t = t.replace(/\$\$[\s\S]*?\$\$|\$[^$\n]{1,160}\$|\\\([\s\S]*?\\\)/g, function (m) {
      math.push(m); return "\x01M" + (math.length - 1) + "\x01";
    });
    for (var i = 0; i < toks.length; i++) {
      var k = toks[i]; if (k.length < 2) continue;
      var safe = k.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      t = t.replace(new RegExp(safe, "gi"), function (x) { return "<mark>" + x + "</mark>"; });
    }
    t = t.replace(/\*\*([^*\n]{1,160})\*\*/g, "<strong>$1</strong>");
    t = t.replace(/`([^`\n]{1,160})`/g, "<code>$1</code>");
    t = t.replace(/\x01M(\d+)\x01/g, function (m, i2) { return math[+i2]; });
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
        hl(h.it.tt, toks) + '</div><div class="cqm-res__sb">' +
        sbRender(String(h.it.sb || "").slice(0, 300), toks) + "</div>";
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
    // 只在本地研究站后端服务（端口 8080）探测 /api/status；
    // VitePress preview（localhost:4173）和静态部署无后端，fetch 会 404 污染控制台。
    if (location.port !== "8080") return;
    try {
      fetch("/api/status", { cache: "no-store" }).then(function (r) { if (!r.ok) return null; return r.json(); }).then(function (s) {
        var hdr = navHost(); if (!hdr || !s || !s.counts) return;
        if (hdr.querySelector(".cqm-badge")) return;
        var a = document.createElement("a");
        // 指向真实存在的接口（/api 本身无映射，会是 404）。
        // 必须 target="_blank"：VitePress router 会拦截站内相对链接做 SPA 导航
        // （实测解析成 /api/status.html 甚至 /api/api/status → 404）；
        // 新窗口打开 JSON，绕过 router。
        a.className = "cqm-sbtn cqm-badge"; a.href = "/api/status";
        a.setAttribute("target", "_blank"); a.setAttribute("rel", "noopener");
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
      // 注意：不能在循环内重置 lastIndex——否则 exec 永远停在第一个匹配，
      // 同一位置被反复替换，整段文本变成查询词的几百次重复（已实测复现）。
      while ((m = re.exec(txt)) !== null && count < 200) {
        if (m.index > last) frag.appendChild(document.createTextNode(txt.slice(last, m.index)));
        var mk = document.createElement("mark");
        mk.className = "cqm-hl"; mk.textContent = m[0];
        frag.appendChild(mk);
        last = m.index + m[0].length; count++;
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

  /* ---------- 阅读调节：正文字号三档循环（localStorage 记忆） ---------- */
  function mountFontCtl() {
    var hdr = navHost(); if (!hdr) return;
    if (hdr.querySelector(".cqm-fontbtn")) return;
    var scales = [1, 1.12, 1.25], idx = 0;
    try { idx = parseInt(localStorage.getItem("cqm-font-idx") || "0", 10) || 0; } catch (e) {}
    if (idx < 0 || idx >= scales.length) idx = 0;
    var b = document.createElement("button");
    b.className = "cqm-sbtn cqm-fontbtn"; b.type = "button";
    b.title = "正文字号（点击循环：标准 / 大 / 特大）";
    function apply() {
      document.documentElement.style.setProperty("--cqm-font-scale", scales[idx]);
      b.textContent = "A" + (idx === 0 ? "" : idx === 1 ? "+ " : "++");
      try { localStorage.setItem("cqm-font-idx", String(idx)); } catch (e) {}
    }
    b.addEventListener("click", function () { idx = (idx + 1) % scales.length; apply(); });
    apply();
    hdr.appendChild(b);
  }

  /* ---------- 侧边栏文本下标修正 ---------- */
  /* 侧栏项文本取自标题的行内渲染，$G_N$ 的 $ 被剥掉后剩字面下划线；
     侧栏不在 MathJax 作用域（正文公式它管不了侧栏），只能在 DOM 层把
     X_Y 包装为 X<sub>Y</sub>。包装后下划线字符消失，天然幂等，
     路由切换重跑安全；返回是否有修改，供观察器判断何时断开。 */
  function fixSubScripts() {
    var root = document.querySelector('.VPSidebar');
    if (!root) return false;
    var scan = new RegExp('([A-Za-z][A-Za-z0-9]{0,10})_([A-Za-z0-9]{1,3})(?![A-Za-z0-9])');
    var walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    var nodes = [], n;
    while ((n = walker.nextNode())) {
      var p = n.parentElement;
      if (!p || p.closest('code,pre,sub,sup,script,style')) continue;
      if (scan.test(n.nodeValue)) nodes.push(n);
    }
    for (var i = 0; i < nodes.length; i++) {
      var t = nodes[i].nodeValue;
      var re = new RegExp('([A-Za-z][A-Za-z0-9]{0,10})_([A-Za-z0-9]{1,3})(?![A-Za-z0-9])', 'g');
      var frag = document.createDocumentFragment(), last = 0, m;
      while ((m = re.exec(t))) {
        if (m.index > last) frag.appendChild(document.createTextNode(t.slice(last, m.index)));
        frag.appendChild(document.createTextNode(m[1]));
        var sub = document.createElement('sub');
        sub.textContent = m[2];
        frag.appendChild(sub);
        last = m.index + m[0].length;
      }
      if (last < t.length) frag.appendChild(document.createTextNode(t.slice(last)));
      if (nodes[i].parentNode) nodes[i].parentNode.replaceChild(frag, nodes[i]);
    }
    if (nodes.length > 0) fixSubScripts._done = true;
    return nodes.length > 0;
  }

  function initPage() {
    runTerms();
    initDepth();
    applySearchHighlight();
    mountFontCtl();
    fixExternalLinks();
    // 侧栏文本下标：X_Y → X<sub>Y</sub>（幂等）。侧栏由 Vue 异步渲染，
    // 首屏 initPage 可能早于侧栏挂载，故直接修一次 + 观察兜底；
    // 修过一次即置 _done，后续路由切换不再空转观察器。
    fixSubScripts();
    if (!fixSubScripts._done && !fixSubScripts._obs) {
      fixSubScripts._obs = new MutationObserver(function () {
        if (fixSubScripts()) {
          fixSubScripts._obs.disconnect(); fixSubScripts._obs = null;
        }
      });
      fixSubScripts._obs.observe(document.body, { childList: true, subtree: true });
      setTimeout(function () {
        if (fixSubScripts._obs) { fixSubScripts._obs.disconnect(); fixSubScripts._obs = null; }
      }, 45000);
    }
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
  // 不在此处自动 boot：DOMContentLoaded 早于 Vue hydration，此时改 DOM 会触发
  // "Hydration completed but contains mismatches" 警告。
  // 初始化由 theme/index.js 的 enhanceApp 经双 rAF 在 hydration 之后调用。
})();
'''

with open(os.path.join(VP_PUBLIC, "cqm-enhance-vp.js"), "w", encoding="utf-8") as fh:
    fh.write(VP_ENHANCE_JS)
print("[vp] 已写 VitePress 版增强脚本 public/cqm-enhance-vp.js")

# ------------------------------------------------- 3c3. Lean 对接页（调 /api/lean/*）
# 页面本体是构建期生成的 LEAN_Lean对接.md（容器 + 说明）；
# 这里只放逻辑：数据来自研究站服务，SPA 路由切换后靠 MutationObserver 重新接管容器。
LEAN_PAGE_JS = r'''(function () {
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
      '<h4 style="margin:1.2em 0 .4em">axiom 待证清单（' + axioms.length + ' 条 · 物理假设的 Lean 承载，形式化覆盖 __LEAN_COVER__ 概念之外的诚实边界）</h4>' +
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
'''

# 形式化覆盖数在构建期填入（不写死）：覆盖概念数 / 概念总数，来自 Lean↔概念映射.csv 实测
LEAN_PAGE_JS = LEAN_PAGE_JS.replace(
    "__LEAN_COVER__", "%d/%d" % (STATS["lean_cover"], STATS["concept"]))

with open(os.path.join(VP_PUBLIC, "lean-page.js"), "w", encoding="utf-8") as fh:
    fh.write(LEAN_PAGE_JS)
print("[vp] 已写 Lean 对接页脚本 public/lean-page.js")

# ------------------------------------------------- 3c4. 术语总览页（悬浮卡集中浏览）
# 数据直接用页面里已加载的 window.CQM_GLOSSARY（terms + index），无需再请求。
# 点击卡片时创建临时 data-cqm 元素并派发 mouseover，复用全局悬浮卡。
TERMS_APP_JS = r'''(function () {
  /* 分类 chip：这里只固定「既有分类的展示顺序」，真实类别集合在 boot 里从 index 的
     ty 字段实测推导——新增或此前漏掉的类别（如只能靠「全部」看到的「讲稿」）
     会自动获得 chip，不会再被写死的清单落下。 */
  var CATS_ORDER = ["概念", "缺口", "论证", "符号", "命题", "文档", "链条步", "讲稿"];
  function boot() {
    var app = document.getElementById("terms-app");
    if (!app || app.__done) return;
    var G = window.CQM_GLOSSARY;
    if (!G) return;
    app.__done = 1;
    var terms = G.terms || {}, index = G.index || [];
    var _seen = {}, _first = [];
    index.forEach(function (it) {
      var ty = it && it.ty;
      if (ty && !_seen[ty]) { _seen[ty] = 1; _first.push(ty); }
    });
    var CATS = CATS_ORDER.filter(function (c) { return _seen[c]; })
      .concat(_first.filter(function (c) { return CATS_ORDER.indexOf(c) < 0; }));
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
      if (_tsTimer) { clearTimeout(_tsTimer); _tsTimer = null; }
      var run = function () {
        if (!window.MathJax) return;
        if (window.MathJax.typesetPromise) {
          try { window.MathJax.typesetPromise([grid]); } catch (e) {}
        } else if (window.MathJax.startup && window.MathJax.startup.promise) {
          window.MathJax.startup.promise.then(function () {
            if (window.MathJax.typesetPromise) {
              try { window.MathJax.typesetPromise([grid]); } catch (e) {}
            }
          });
        } else {
          _tsTimer = setTimeout(function () { typesetGrid(grid); }, 300);
        }
      };
      if (window.requestIdleCallback) { window.requestIdleCallback(run, { timeout: 200 }); }
      else { _tsTimer = setTimeout(run, 120); }
    }

    function cardHtml(item) {
      var key = item.sk || keyOf(item.ty, item.tt);
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
          if ((it.tt + " " + (it.sb || "") + " " + (it.dc || "") + " " + (it.sk || "")).toLowerCase().indexOf(q) < 0) return false;
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
'''

with open(os.path.join(VP_PUBLIC, "terms-app.js"), "w", encoding="utf-8") as fh:
    fh.write(TERMS_APP_JS)
print("[vp] 已写术语总览页脚本 public/terms-app.js")

# 术语总览页本体（张数/索引条数/分类全部构建期实测，见上面 1b 与 _glossary_stats）
TERMS_MD = """---
title: 术语表
---

<div v-pre>

# 术语总览

全部 **%(glossary_terms)d 张**悬浮卡、**%(glossary_index)d 条**索引在此集中浏览，按实际类别划分：
%(glossary_cats)s。
悬停或点击任意卡片，即可弹出与正文一致的完整解释（含公式、原文引文与出处链接）；
正文中遇到术语时也会有同样的悬浮解释。

<div id="terms-app" class="terms-app">正在加载术语数据…</div>

数据边界：卡片文字逐字取自 `01_结构化数据` 与 `09_桥接与翻译` 的结构化表，
机器不改写、不推断；语义近邻仅为 TF-IDF 定位线索，非理论关系。

</div>
"""
with open(os.path.join(VP_DOCS, "TERMS_术语表.md"), "w", encoding="utf-8") as fh:
    fh.write(TERMS_MD % STATS)
print("[vp] 已写术语总览页 docs/TERMS_术语表.md")

# ------------------------------------------------- 3d. 自定义主题（接路由 hook）
# VitePress 是 SPA：路由切换后必须重跑 initPage（术语标注 + 深度滑杆）并重排公式。
THEME_JS = r'''import DefaultTheme from 'vitepress/theme'

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
'''

theme_dir = os.path.join(VP_CFG_DIR, "theme")
os.makedirs(theme_dir, exist_ok=True)
with open(os.path.join(theme_dir, "index.js"), "w", encoding="utf-8") as fh:
    fh.write(THEME_JS)
print("[vp] 已写自定义主题 .vitepress/theme/index.js（路由切换后重跑增强）")

# ---------------------------------------------------------------- 4. 首页（VitePress home 布局）
# 四张特性卡的数字全部来自 1b 的构建期实测（%(concept)d/%(prop)d/%(arg)d/%(gap)d、
# %(kg_node)d/%(kg_edge)d、%(evidence)d、%(lean_cover)d/%(concept)d），不得写死。
HOME_MD = """---
layout: home

hero:
  name: "CQM"
  text: "耦合常数量子力学研究站"
  tagline: 组织层 · 证据层 · 主张层 · 知识图谱 · 形式化验证
  actions:
    - theme: brand
      text: 理论展开链
      link: /L000_展开链
    - theme: alt
      text: 讲稿 · 全六册
      link: /L001_第一分册_从问题到链条

features:
  - title: 结构化数据（唯一源）
    details: 概念 %(concept)d · 命题 %(prop)d · 论证 %(arg)d · 缺口 %(gap)d
  - title: 知识图谱与 SPARQL
    details: %(kg_node)d 实体 / %(kg_edge)d 边；在线只读 SPARQL（Jena 内存模型）
  - title: 证据层
    details: %(evidence)d 条断言，逐字引文 + 字符区间可回溯
  - title: 形式化验证
    details: Lean 覆盖 %(lean_cover)d/%(concept)d 概念；SHACL / HermiT 一致性通过
  - title: 文献总览
    details: 按文档汇总参考文献与文献锚定，条目逐字取自原文
---
"""
with open(os.path.join(VP_DOCS, "index.md"), "w", encoding="utf-8") as fh:
    fh.write(HOME_MD % STATS)

# ---------------------------------------------------------------- 4b. Lean 对接页
# 数据与编译走研究站服务的 /api/lean/*；脚本 lean-page.js 由 head 全局加载，
# 通过 MutationObserver 在容器出现时接管（SPA 路由切换后同样生效）。
# 正文数字（模块/声明/映射/axiom/覆盖）全部取 1b 的构建期实测值。
LEAN_MD = """---
title: Lean 对接
---

<div v-pre>

# Lean 对接：形式化与研究站的统一视图

Lean 4 形式化项目（**%(lean_module)d 个模块 / %(lean_decl_txt)s 个声明**，`leanprover/lean4:v4.29.1`）与 CQM
结构化层在这里打通：**模块与声明** 浏览源码与证明位置；**概念 ↔ Lean** 查看
人工整理的映射（%(lean_map)d 条）与 **axiom 待证清单**（%(lean_axiom)d 条，物理假设的 Lean 承载，原样登记不升格）。
<div id="lean-app" class="lean-app">正在加载 Lean 对接数据…（需要研究站服务在运行）</div>

呈现边界：形式化覆盖 **%(lean_cover)d/%(concept)d 概念**——未覆盖概念不得视为已形式化；缺口状态、
「待证」限定语保持权威源口径。

</div>
"""
with open(os.path.join(VP_DOCS, "LEAN_Lean对接.md"), "w", encoding="utf-8") as fh:
    fh.write(LEAN_MD % STATS)
print("[vp] 已写 Lean 对接页 docs/LEAN_Lean对接.md")


# ---------------------------------------------------------------- 5. 导航/侧栏（按文件名分组）
def md_title(path, fallback):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            for line in fh:
                m = re.match(r"^#\s+(.+?)\s*$", line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return fallback


overview, lect, viz, other = [], [], [], []
# 文档主题分类：按源顶层目录（01–07）分组，与仓库目录结构一一对应——
# 不再把全部文档平铺进「结构化与参考」。sid→源目录的映射复用 build_reader_site
# 的 registry（sid 分配逻辑的唯一权威，避免两处实现漂移）。
name2top = {}
try:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import build_reader_site as _brs
    for rel, meta in _brs.registry().items():
        _name = _brs.safe_name("%s_%s" % (meta["id"], meta["title"]))
        name2top[_name] = rel.split("/")[0]
except Exception as _e:
    print("[vp][warn] 文档主题分类不可用（全部回退「其它」组）：%s" % _e)
TOP_ORDER = [
    ("01 核心理论", "核心理论"),
    ("02 量子引力", "量子引力讨论"),
    ("03 引力与退相干", "引力与退相干"),
    ("04 前沿研究", "前沿研究"),
    ("05 方法论与批判", "方法论与批判"),
    ("06 超导", "超导"),
    ("07 精细引力（FG）", "精细引力（FG）"),
]
by_top = {}
for f in md_files:
    if f == "index.md":
        continue
    base = os.path.splitext(f)[0]
    item = {"text": plain_title(md_title(os.path.join(VP_DOCS, f), base)), "link": "/" + base}
    if f.startswith("L000"):
        overview.append(item)
    elif f.startswith("LEAN") or f.startswith("TERMS") or f.startswith("REFS"):
        # 专属功能页：进导航与侧栏专属组（见下方 sidebar 组装）
        by_top.setdefault("__app__", []).append(item)
    elif f.startswith("L"):
        lect.append(item)
    elif f.startswith("V"):
        viz.append(item)
    else:
        top = name2top.get(f)
        if top:
            by_top.setdefault(top, []).append(item)
        else:
            other.append(item)

sidebar = []
if overview:
    sidebar.append({"text": "展开链", "items": overview})
if lect:
    sidebar.append({"text": "讲稿", "items": lect})
for top, label in TOP_ORDER:
    items = by_top.get(top)
    if items:
        sidebar.append({"text": label, "items": items})
if by_top.get("__app__"):
    sidebar.append({"text": "功能页", "items": by_top["__app__"]})
if viz:
    sidebar.append({"text": "可视化", "items": viz})
if os.path.isfile(os.path.join(VP_DOCS, "LEAN_Lean对接.md")):
    sidebar.append({"text": "Lean 对接", "items": [
        {"text": "Lean 对接 · 统一视图", "link": "/LEAN_Lean对接"}]})
if os.path.isfile(os.path.join(VP_DOCS, "TERMS_术语表.md")):
    sidebar.append({"text": "术语表", "items": [
        {"text": "术语总览（%d 条）" % STATS["glossary_index"], "link": "/TERMS_术语表"}]})
if os.path.isfile(os.path.join(VP_DOCS, "REFS_文献总览.md")):
    sidebar.append({"text": "文献", "items": [
        {"text": "文献总览（%d 条）" % REF_TOTAL, "link": "/REFS_文献总览"}]})
if other:
    sidebar.append({"text": "其它", "items": other})

# ---- 「参考」组：TOP_ORDER 之外的源顶层目录（项目根 README.md / AGENTS.md、08 组织层自身）
# 原循环只输出 TOP_ORDER 里列出的分组，其余分组被静默丢弃——既不进 sidebar 也不进 nav，
# D001（根 README.md）与 D003/D004（08/附录/术语表、缺口台账）因此成了零入链的孤立页，
# 只能靠搜索到达。这里把剩余分组全部收进「参考」组，条目文字标出它来自哪一层。
_TOP_KEYS = {t for t, _ in TOP_ORDER}
_rest_tops = [k for k in by_top if k != "__app__" and k not in _TOP_KEYS]
_REF_ORDER = ["README.md", "AGENTS.md", "08 理论组织和形式化框架"]
_rest_tops.sort(key=lambda k: (_REF_ORDER.index(k) if k in _REF_ORDER else len(_REF_ORDER), k))
REF_SRC = {"README.md": "项目根", "AGENTS.md": "项目根",
           "08 理论组织和形式化框架": "组织层"}
ref_items = []
for _top in _rest_tops:
    _src = REF_SRC.get(_top, _top)
    for _it in by_top[_top]:
        ref_items.append({"text": "%s（%s）" % (_it["text"], _src), "link": _it["link"]})
if ref_items:
    sidebar.append({"text": "参考", "items": ref_items})

nav = [{"text": "首页", "link": "/"}]
if overview:
    nav.append({"text": "展开链", "link": overview[0]["link"]})
if lect:
    nav.append({"text": "讲稿", "link": lect[0]["link"]})
if viz:
    nav.append({"text": "可视化", "link": viz[0]["link"]})
if os.path.isfile(os.path.join(VP_DOCS, "LEAN_Lean对接.md")):
    nav.append({"text": "Lean 对接", "link": "/LEAN_Lean对接"})
if os.path.isfile(os.path.join(VP_DOCS, "TERMS_术语表.md")):
    nav.append({"text": "术语表", "link": "/TERMS_术语表"})
if os.path.isfile(os.path.join(VP_DOCS, "REFS_文献总览.md")):
    nav.append({"text": "文献", "link": "/REFS_文献总览"})
nav.append({"text": "检索台", "link": "/V003_检索台"})

# ---- 断言：docs/ 下每个 .md（除 index.md）都必须出现在 sidebar 或 nav 中 ----
# 背景：sidebar/nav 是页面的唯一入口，之前的分组丢弃让 D001/D003/D004 变成只能靠搜索
# 到达的孤立页。把「每页可达」写成构建期硬断言：一旦再出现被丢弃的分组，构建直接失败
# 并点名文件。（不查 dist/*.html：VitePress 的侧栏是客户端渲染，静态 HTML 里没有这些 <a>。）
def _collect_links(node, acc):
    if isinstance(node, dict):
        _link = node.get("link")
        if isinstance(_link, str):
            acc.add(_link)
        for _v in node.values():
            _collect_links(_v, acc)
    elif isinstance(node, list):
        for _v in node:
            _collect_links(_v, acc)


_reachable = set()
_collect_links(sidebar, _reachable)
_collect_links(nav, _reachable)
_pages = sorted(f for f in os.listdir(VP_DOCS) if f.endswith(".md") and f != "index.md")
_orphan = [f for f in _pages if "/" + os.path.splitext(f)[0] not in _reachable]
if _orphan:
    sys.exit("[vp][FATAL] 以下页面既不在 sidebar 也不在 nav，只能靠搜索到达（零入链）：%s"
             % "、".join(_orphan))
print("[vp] 可达性断言通过：docs/ 下 %d 个页面全部出现在 sidebar 或 nav" % len(_pages))

CONFIG_MTS = """import { defineConfig } from 'vitepress'

// 中文检索分词：minisearch 默认把连续的 CJK 当一个词，中文查询几乎命中不了。
// 这里按「单字 + 二元」切分中文、按词切分拉丁；索引与查询共用同一 tokenize。
const cqmTokenize = (text) => {
  const out = []
  const re = /[\\u4e00-\\u9fff]+|[A-Za-z0-9_\\-]+/g
  let m
  while ((m = re.exec(text))) {
    const s = m[0]
    if (/^[\\u4e00-\\u9fff]+$/.test(s)) {
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
  // 于是公式里的 _ / * 被当成强调语法，例如 $$\\mathbb{R}_{>0}$$ 被解析成
  // "\\mathbb{R}<em>{>0}</em>"——标签一旦插入，MathJax 就无法再匹配这对
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
    ['link', { rel: 'stylesheet', href: '/vp-brand.css?v=__VTAG__' }],
    ['link', { rel: 'stylesheet', href: '/vp-read.css?v=__VTAG__' }],
    ['link', { rel: 'stylesheet', href: '/stylesheets/cqm-enhance.css?v=__VTAG__' }],
    ['script', { src: '/cqm-glossary.js?v=__VTAG__', defer: true }],
    ['script', { src: '/cqm-depth.js?v=__VTAG__', defer: true }],
    ['script', { src: '/cqm-enhance-vp.js?v=__VTAG__', defer: true }],
    ['script', { src: '/vp-math.js?v=__VTAG__', defer: true }],
    // tex-svg.js 不在此列：引擎的注入由 vp-math.js 负责（配置必须先于引擎执行，
    // 且公网部署走国内 CDN、内网走随站文件，见 build 脚本 3b 节）。
    ['script', { src: '/lean-page.js?v=__VTAG__', defer: true }],
    ['script', { src: '/terms-app.js?v=__VTAG__', defer: true }]
  ],
  themeConfig: {
    nav: %s,
    sidebar: %s,
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
""" % (json.dumps(nav, ensure_ascii=False, indent=2),
       json.dumps(sidebar, ensure_ascii=False, indent=2))

VTAG = time.strftime("%Y%m%d%H%M%S")
CONFIG_MTS = CONFIG_MTS.replace("__VTAG__", VTAG)
with open(os.path.join(VP_CFG_DIR, "config.mts"), "w", encoding="utf-8") as fh:
    fh.write(CONFIG_MTS)
print("[vp] 已生成 .vitepress/config.mts（nav=%d 项，sidebar=%d 组）" % (len(nav), len(sidebar)))

# ---------------------------------------------------------------- 6. vitepress build
if not os.path.isfile(VITEPRESS_BIN):
    sys.exit("[vp] 未找到 vitepress：%s —— 请先在阅读站VitePress 目录 npm install" % VITEPRESS_BIN)

print("[vp] 开始 vitepress build ...")
subprocess.run([NODE, VITEPRESS_BIN, "build"], cwd=VP_ROOT, check=True)

dist = os.path.join(VP_CFG_DIR, "dist")
print("[vp] 构建完成，产物：%s" % dist)

# ---------------------------------------------------------------- 7. 还原数学占位符
# 产物里三类上下文要分别转义：
#   .html —— 文本节点，做 HTML 转义（& < >）
#   .js   —— 页面 chunk 是单引号 JS 字符串，按字符串上下文转义（\\ ' " 换行；
#            JSON.parse('…') 上下文要双层转义）——见 restore_math_js
#   .json —— 真实 JSON 文件（本地检索索引等），按 JSON 转义还原
restored = 0
if MATH_STORE:
    for dp, dns, fns in os.walk(dist):
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in (".html", ".js", ".json"):
                continue
            p = os.path.join(dp, fn)
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    txt = fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            if "CQMMATHPLCHOLDER" not in txt:
                continue
            if ext == ".js":
                new = restore_math_js(txt)
            else:
                new = restore_math(txt, js=(ext == ".json"))
            if new != txt:
                with open(p, "w", encoding="utf-8") as fh:
                    fh.write(new)
                restored += 1
print("[vp] 数学保护：%d 处公式入占位 → %d 个产物文件已还原（其中 %d 处 \\text{} 文本模式转义已还原）"
      % (len(MATH_STORE), restored, TEXT_MODE_FIXED[0]))

# ---------------------------------------------------------------- 7b. 锚点失配修复
# 手写目录链接的 href 不带连字符（#第一部分哲学与本体论），而 VitePress slugify
# 生成的 heading id 在空格/箭头处插连字符（#第一部分-哲学与本体论）→ 点击无目标，
# 页面不跳转。构建后按「规范化唯一匹配」改写失配 href：规范化只保留字母数字与
# CJK（去连字符/下划线/箭头/标点、小写），唯一命中才改，歧义或无匹配则报告不动。
# 同页 chunk JS（SPA 动态渲染的内容源）做同样字面替换。
ANCHOR_NORM_RE = re.compile(r"[^0-9A-Za-z\u4e00-\u9fff]+")
ANCHOR_LOOSE_RE = re.compile(r"[^0-9\u4e00-\u9fff]+")  # 宽松：去 ASCII 字母（公式被 slugify 清除的情形）


def _anchor_key(s):
    return ANCHOR_NORM_RE.sub("", s).lower()


def _anchor_loose(s):
    return ANCHOR_LOOSE_RE.sub("", s)


anchor_fixed_pages = 0
anchor_fixed_links = 0
anchor_unresolved = []
for f in sorted(os.listdir(dist)):
    if not f.endswith(".html") or f == "index.html":
        continue
    p = os.path.join(dist, f)
    with open(p, "r", encoding="utf-8") as fh:
        t = fh.read()
    ids = set(re.findall(r'id="([^"]+)"', t))
    if not ids:
        continue
    norm_map = {}
    loose_map = {}
    for i in ids:
        norm_map.setdefault(_anchor_key(i), []).append(i)
        loose_map.setdefault(_anchor_loose(i), []).append(i)
    fixes = {}
    for h in set(re.findall(r'href="#([^"]+)"', t)):
        if h in ids:
            continue
        cand = norm_map.get(_anchor_key(h), [])
        how = "norm"
        if len(cand) != 1:
            # 宽松匹配兜底：手写目录把公式记作 g_n/kappa 等 ASCII，
            # 而 heading 内公式经 slugify 整体消失（id 只剩编号+中文）
            cand2 = loose_map.get(_anchor_loose(h), [])
            if len(cand2) == 1 and cand2[0] != h:
                cand, how = cand2, "loose"
            else:
                anchor_unresolved.append((f, h, len(cand), len(cand2)))
                continue
        if cand[0] != h:
            fixes[h] = cand[0]
    if not fixes:
        continue
    for old, new in fixes.items():
        t = t.replace('href="#%s"' % old, 'href="#%s"' % new)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(t)
    # 同步页面对应的 chunk JS（含 .lean 变体）
    stem = f[:-5]
    for js in glob.glob(os.path.join(dist, "assets", stem + ".md.*.js")):
        with open(js, "r", encoding="utf-8") as fh:
            jt = fh.read()
        jn = jt
        for old, new in fixes.items():
            jn = jn.replace('href="#%s"' % old, 'href="#%s"' % new)
        if jn != jt:
            with open(js, "w", encoding="utf-8", newline="") as fh:
                fh.write(jn)
    anchor_fixed_pages += 1
    anchor_fixed_links += len(fixes)
print("[vp] 锚点修复：%d 个页面 %d 处失配 href 已改写；未解决 %d 处"
      % (anchor_fixed_pages, anchor_fixed_links, len(anchor_unresolved)))
for f, h, n1, n2 in anchor_unresolved[:8]:
    print("    未解决: %s #%s（严格命中 %d / 宽松命中 %d）" % (f, h, n1, n2))

# ---------------------------------------------------------------- 7c. 跨页锚点修复
# 文献总览的「查看原文」链接指向 ./Dxxx.html#参考文献，而 VitePress 会给标题 id
# 加编号前缀与标点归一（如 #13.-参考文献 → #_13-参考文献）。按「去标点归一化唯一匹配」
# 改写目标页锚点，并同步到 chunk JS（SPA 导航用同一份链接）。
_cp_fixes = {}
for _f in sorted(os.listdir(dist)):
    if not _f.endswith(".html"):
        continue
    with open(os.path.join(dist, _f), "r", encoding="utf-8") as _fh:
        _t = _fh.read()
    for _m in re.finditer(r'href="([^"#]+\.html)#([^"]+)"', _t):
        _page, _anc = _m.group(1), _m.group(2)
        _rel = _page[2:] if _page.startswith("./") else _page
        _target = os.path.normpath(os.path.join(dist, _rel.replace("/", os.sep)))
        if not os.path.isfile(_target):
            continue
        with open(_target, "r", encoding="utf-8") as _fh2:
            _ids = set(re.findall(r'id="([^"]+)"', _fh2.read()))
        if _anc in _ids:
            continue
        _norm = {}
        for _i in _ids:
            _norm.setdefault(_anchor_key(_i), []).append(_i)
        _cand = _norm.get(_anchor_key(_anc), [])
        if len(_cand) == 1:
            _cp_fixes["%s#%s" % (_page, _anc)] = "%s#%s" % (_page, _cand[0])
if _cp_fixes:
    _cp_files = 0
    for _dp, _dns, _fns in os.walk(dist):
        for _fn in _fns:
            if not _fn.endswith((".html", ".js")):
                continue
            _p = os.path.join(_dp, _fn)
            try:
                with open(_p, "r", encoding="utf-8") as _fh:
                    _txt = _fh.read()
            except (UnicodeDecodeError, OSError):
                continue
            _new = _txt
            for _old, _rep in _cp_fixes.items():
                _new = _new.replace(_old, _rep)
            if _new != _txt:
                with open(_p, "w", encoding="utf-8", newline="") as _fh:
                    _fh.write(_new)
                _cp_files += 1
    print("[vp] 跨页锚点修复：%d 处 → %d 个产物文件" % (len(_cp_fixes), _cp_files))

index_html = os.path.join(dist, "index.html")
if os.path.isfile(index_html):
    with open(index_html, "r", encoding="utf-8") as fh:
        head = fh.read(4000)
    m = re.search(r'name="generator"\s+content="([^"]+)"', head)
    print("[vp] generator = %s" % (m.group(1) if m else "未找到（异常）"))
