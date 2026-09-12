#!/usr/bin/env python3
"""Comprehensive scan of all .md files for formatting and formula anomalies."""
import os
import re

root = r'D:\WorkSpace\物理\CQMFormal'
skip_dirs = {'.git', '.lake', '.arts', '.codeartsdoer', '归档', '归档 CNT', '__pycache__', '.vscode', 'node_modules', 'godot_project'}

def find_md_files(root, skip_dirs):
    result = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if fn.endswith('.md'):
                result.append(os.path.join(dirpath, fn))
    return result

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()

    issues = []
    fname = os.path.basename(filepath)

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # 1. \xRightarrow{} / \xrightarrow{} empty param
        if r'\xRightarrow{}' in line:
            issues.append((i, r'\xRightarrow{} 空参数', stripped[:100]))
        if r'\xrightarrow{}' in line:
            issues.append((i, r'\xrightarrow{} 空参数', stripped[:100]))

        # 2. \xleftrightarrow old convention
        if r'\xleftrightarrow' in line:
            issues.append((i, r'\xleftrightarrow 旧约定', stripped[:100]))

        # 3. 约束 remaining
        if '约束' in line:
            issues.append((i, '约束 残留', stripped[:100]))

        # 4. Table row not closed
        if stripped.startswith('|') and not stripped.endswith('|') and not stripped.startswith('|--') and not stripped.startswith('|:'):
            # Check if it looks like a table row (has multiple |)
            if stripped.count('|') >= 2:
                issues.append((i, '表格行未闭合|', stripped[:100]))

        # 5. $ unpaired (inline math)
        single_d = line.count('$') - 2 * line.count('$$')
        if single_d % 2 != 0:
            issues.append((i, '$不配对', stripped[:100]))

        # 6. 谱量子 as constant name (not in filename reference)
        if '谱量子' in line:
            # Check if it's NOT just a filename reference
            if '谱量子' in line.replace('CQM_核心_朗兰兹分层共振与谱量子.md', '').replace('朗兰兹分层共振与谱量子', ''):
                issues.append((i, '谱量子(非文件名引用)', stripped[:100]))

        # 7. 时空同步速度 without 特征
        if '时空同步速度' in line and '时空同步特征速度' not in line:
            issues.append((i, '时空同步速度缺特征', stripped[:100]))

        # 8. Double full-width periods (。。)
        if '。。' in line:
            issues.append((i, '双句号', stripped[:100]))
        if '，，' in line:
            issues.append((i, '双逗号', stripped[:100]))

        # 9. Mixed full/half-width punctuation (common issues)
        # Full-width comma followed by half-width space (inconsistent)
        # Skip - too many false positives in mixed CN/EN text

        # 10. \text{} with empty content
        if r'\text{}' in line:
            issues.append((i, r'\text{} 空内容', stripped[:100]))

        # 11. Unbalanced braces in LaTeX (simple check)
        # Count { and } in the line
        brace_count = line.count('{') - line.count('}')
        # Skip - can span multiple lines

        # 12. Broken inline code (single ` without pair)
        backtick_count = line.count('`')
        if backtick_count % 2 != 0:
            issues.append((i, '`不配对', stripped[:100]))

        # 13. Heading with trailing space
        m = re.match(r'^(#+)\s+(.*?)\s*$', line.rstrip())
        if m and line.rstrip() != line.rstrip().rstrip():
            # Heading has trailing whitespace
            pass  # Skip - rstrip already handles this

        # 14. List marker inconsistency (- vs *)
        # Skip - context dependent

        # 15. § vs § (different section symbols)
        if '§' in line and '§' in line:
            pass  # Both are valid

        # 16. \to in recombination context (should be \Rightarrow)
        # Skip - context dependent, already checked

        # 17. Multiple consecutive spaces in Chinese text
        # Check for 3+ consecutive spaces (not in code block)
        if '   ' in line and not stripped.startswith('```') and not stripped.startswith('|'):
            # Could be indentation or alignment, skip
            pass

        # 18. Full-width space (　) - invisible but problematic
        if '　' in line:
            issues.append((i, '全角空格', stripped[:100]))

        # 19. Zero-width space or other invisible characters
        for j, ch in enumerate(line):
            if ord(ch) in [0x200B, 0x200C, 0x200D, 0xFEFF, 0x00A0]:
                issues.append((i, f'不可见字符 U+{ord(ch):04X}', stripped[:100]))
                break

        # 20. \boxed without closing
        if r'\boxed' in line and line.count(r'\boxed') != line.count('}') :
            pass  # Too complex to check on single line

        # 21. LaTeX \frac without proper structure
        # Skip - too complex for line-by-line check

        # 22. Inconsistent dash (—— vs -- vs ─)
        if '--' in line and '——' not in line and not stripped.startswith('|') and not stripped.startswith('```'):
            # Check if it's in a math context or URL
            if '$' not in line and 'http' not in line and '.md' not in line:
                # Could be a half-width dash that should be full-width
                pass  # Skip - too many false positives

        # 23. Broken markdown link [text](url) - check for unclosed
        if '[' in line and '](' in line and ')' not in line.split('](')[1]:
            issues.append((i, '链接可能未闭合', stripped[:100]))

        # 24. \ldots vs \cdots vs ... inconsistency
        # Skip - context dependent

        # 25. Trailing whitespace (non-empty lines)
        if line.rstrip() != line.rstrip('\n').rstrip() and stripped != '':
            issues.append((i, '行尾空格', stripped[:100]))

    # Global checks
    content = ''.join(lines)

    # $$ pairing
    dd_count = content.count('$$')
    if dd_count % 2 != 0:
        issues.append((0, f'$$不配对: 共{dd_count}个', ''))

    # Heading level jumps
    prev_level = 0
    for i, line in enumerate(lines, 1):
        m = re.match(r'^(#+)\s', line)
        if m:
            level = len(m.group(1))
            if prev_level > 0 and level > prev_level + 1:
                issues.append((i, f'标题层级跳跃: {prev_level}→{level}', line.rstrip()[:80]))
            prev_level = level

    # Consecutive blank lines (>2)
    blank_count = 0
    for i, line in enumerate(lines, 1):
        if line.strip() == '':
            blank_count += 1
            if blank_count > 2:
                issues.append((i, f'连续空行{blank_count}行', ''))
        else:
            blank_count = 0

    return fname, issues

files = find_md_files(root, skip_dirs)
print(f'Found {len(files)} .md files\n')

total_issues = 0
issue_files = 0
for fp in sorted(files):
    fname, issues = check_file(fp)
    if issues:
        total_issues += len(issues)
        issue_files += 1
        print(f'=== {fname} ({len(issues)} issues) ===')
        for lineno, desc, content in issues:
            if content:
                print(f'  L{lineno}: {desc}')
                print(f'    {content[:120]}')
            else:
                print(f'  L{lineno}: {desc}')
        print()

print(f'Total: {total_issues} issues in {issue_files} files (out of {len(files)} scanned)')