# -*- coding: utf-8 -*-
"""讲稿分册排序键（单一事实源）。

讲稿文件名以「第N分册」开头，中文数字必须按**数值**比大小：直接按 Unicode 码点排会得到
一(U+4E00) < 三(U+4E09) < 二(U+4E8C)，第三册会插到第二册前面，L 编号、侧栏顺序与
审计工具的页面映射全部错位。构建脚本（build_reader_site.stage_lectures）与两个审计工具
（fidelity_audit / structure_audit 的 build_page_map）必须使用同一把尺，否则审计会
静默漏页（映射名对不上 dist 文件名 → 该页不进 doc_pages，连"漏检"都不报）。

非「第N分册」模式的文件退化为码点序，并排在有编号者之后（保持既有行为）。
"""
import os
import re

CN_DIGITS = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}


def _cn_num(s):
    """中文数字串 → 整数（支持到 99：十/十一/二十）。"""
    if s == "十":
        return 10
    if "十" in s:
        a, _, b = s.partition("十")
        return (CN_DIGITS.get(a, 1) if a else 1) * 10 + (CN_DIGITS.get(b, 0) if b else 0)
    return CN_DIGITS.get(s, 0)


def lecture_sort_key(path):
    stem = os.path.basename(path)[:-3]
    m = re.match(r"^第([一二三四五六七八九十]+)分册", stem)
    if m:
        return (0, _cn_num(m.group(1)), stem)
    return (1, 0, stem)
