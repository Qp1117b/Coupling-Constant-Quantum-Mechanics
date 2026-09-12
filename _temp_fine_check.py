#!/usr/bin/env python3
"""Fine-grained scan for subtle formatting issues in .md files."""
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
    in_code_block = False

    for i, line in enumerate(lines, 1):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # 1. Half-width comma/period in Chinese context
        # Check for Chinese char followed by half-width comma/period
        for m in re.finditer(r'[\u4e00-\u9fff][,.]', line):
            # Check if it's in a math context
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                issues.append((i, f'中文后半角标点: {m.group()}', stripped[:100]))

        # 2. Half-width colon/semicolon in Chinese context
        for m in re.finditer(r'[\u4e00-\u9fff][:;]', line):
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                # Skip if it's a markdown link or reference
                if 'http' not in line[pos:pos+10]:
                    issues.append((i, f'中文后半角冒号/分号: {m.group()}', stripped[:100]))

        # 3. Missing space between Chinese and English/number
        # Chinese followed directly by English letter
        for m in re.finditer(r'[\u4e00-\u9fff][A-Za-z]', line):
            # Skip in math context or URLs
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                if 'http' not in line[max(0,pos-5):pos+10] and '.md' not in line[max(0,pos-5):pos+10]:
                    issues.append((i, f'中文接英文无空格: {m.group()}', stripped[:100]))

        # English letter followed directly by Chinese
        for m in re.finditer(r'[A-Za-z][\u4e00-\u9fff]', line):
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                if 'http' not in line[max(0,pos-5):pos+10] and '.md' not in line[max(0,pos-5):pos+10]:
                    issues.append((i, f'英文接中文无空格: {m.group()}', stripped[:100]))

        # 4. Missing space between Chinese and number
        for m in re.finditer(r'[\u4e00-\u9fff][0-9]', line):
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                issues.append((i, f'中文接数字无空格: {m.group()}', stripped[:100]))

        for m in re.finditer(r'[0-9][\u4e00-\u9fff]', line):
            pos = m.start()
            before = line[:pos+1]
            if '$' not in before or before.count('$') % 2 == 0:
                issues.append((i, f'数字接中文无空格: {m.group()}', stripped[:100]))

        # 5. \to vs \rightarrow inconsistency in same document
        # Skip - context dependent

        # 6. Section reference format: § vs §
        # Both are valid, skip

        # 7. Full-width parentheses in math context
        # Skip - complex check

        # 8. Trailing whitespace
        if line.rstrip('\n') != line.rstrip() and stripped != '':
            issues.append((i, '行尾空格', stripped[:100]))

        # 9. Full-width space
        if '　' in line:
            issues.append((i, '全角空格', stripped[:100]))

        # 10. Invisible characters
        for ch in line:
            if ord(ch) in [0x200B, 0x200C, 0x200D, 0xFEFF]:
                issues.append((i, f'不可见字符 U+{ord(ch):04X}', stripped[:100]))
                break

        # 11. LaTeX command issues
        # \text with nested braces
        if r'\text{' in line:
            # Check for unclosed \text{
            for m in re.finditer(r'\\text\{[^}]*$', line):
                issues.append((i, r'\text{}可能未闭合', stripped[:100]))

        # 12. Double full-width punctuation
        if '。。' in line or '，，' in line or '：：' in line:
            issues.append((i, '重复标点', stripped[:100]))

        # 13. Mixed dash styles
        if '——' in line and '─' in line:
            issues.append((i, '破折号风格混用', stripped[:100]))

        # 14. Unclosed markdown bold/italic
        bold_count = line.count('**')
        if bold_count % 2 != 0:
            issues.append((i, '**不配对', stripped[:100]))

        # 15. Unclosed inline code (single backtick, not triple)
        single_backtick = line.count('`') - 3 * (line.count('```'))
        # This is tricky - skip for now

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
        for lineno, desc, content in issues[:20]:  # Limit to first 20 per file
            print(f'  L{lineno}: {desc}')
            print(f'    {content[:120]}')
        if len(issues) > 20:
            print(f'  ... and {len(issues)-20} more')
        print()

print(f'Total: {total_issues} issues in {issue_files} files (out of {len(files)} scanned)')