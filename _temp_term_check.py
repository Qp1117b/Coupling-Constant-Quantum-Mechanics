#!/usr/bin/env python3
"""Check terminology consistency across all .md files."""
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

files = find_md_files(root, skip_dirs)

# Check terminology pairs
term_pairs = [
    ('曲率算子', '曲率算符'),
    ('再生产算子', '再生产算符'),
    ('同步算子', '同步算符'),
    ('Hecke算子', 'Hecke算符'),
    ('赫克算子', '赫克算符'),
    ('群算子', '群算符'),
    ('谱算子', '谱算符'),
    ('曲率算子', '曲率算符'),
    ('作用量算子', '作用量算符'),
    ('紧化算子', '紧化算符'),
    ('波利亚算子', '波利亚算符'),
    ('投影算子', '投影算符'),
]

print("=== 术语一致性检查（算子 vs 算符）===\n")
for term1, term2 in term_pairs:
    count1 = 0
    count2 = 0
    files1 = []
    files2 = []
    for fp in files:
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        c1 = content.count(term1)
        c2 = content.count(term2)
        if c1 > 0:
            count1 += c1
            files1.append(os.path.basename(fp))
        if c2 > 0:
            count2 += c2
            files2.append(os.path.basename(fp))
    if count1 > 0 and count2 > 0:
        print(f'⚠️ {term1}/{term2}: {count1} vs {count2}')
        print(f'  {term1} in: {", ".join(files1[:5])}')
        print(f'  {term2} in: {", ".join(files2[:5])}')
    elif count1 > 0:
        print(f'✅ {term1}: {count1} (统一)')
    elif count2 > 0:
        print(f'✅ {term2}: {count2} (统一)')

# Check other consistency issues
print("\n=== 其他一致性检查 ===\n")

# Check for "光速" (should be "时空同步特征速度" except in comparison notes)
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        if '光速' in line and '时空同步特征速度' not in line and '对照' not in line and '比较' not in line:
            # Check if it's in a context where "光速" is appropriate (e.g., E=mc²)
            if 'mc^2' not in line and 'E=mc' not in line and '光速不变' not in line:
                print(f'⚠️ {os.path.basename(fp)}:L{i}: 光速 → {line.strip()[:80]}')

# Check for "谱量子" as constant name (not filename)
print("\n=== 谱量子检查（排除文件名引用）===\n")
for fp in files:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove filename references
    cleaned = content.replace('CQM_核心_朗兰兹分层共振与谱量子.md', '').replace('朗兰兹分层共振与谱量子', '')
    if '谱量子' in cleaned:
        print(f'⚠️ {os.path.basename(fp)}: 谱量子作为常量名残留')
        for i, line in enumerate(content.splitlines(), 1):
            cleaned_line = line.replace('CQM_核心_朗兰兹分层共振与谱量子.md', '').replace('朗兰兹分层共振与谱量子', '')
            if '谱量子' in cleaned_line:
                print(f'  L{i}: {line.strip()[:100]}')

print("\nDone!")