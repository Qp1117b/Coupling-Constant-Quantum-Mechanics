#!/usr/bin/env python3
"""Fix trailing whitespace in all .md files."""
import os

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
total_fixed = 0

for fp in sorted(files):
    with open(fp, 'r', encoding='utf-8', newline='') as f:
        lines = f.readlines()

    fixed_lines = []
    file_changed = False
    for line in lines:
        # Strip trailing whitespace but preserve newline
        rstripped = line.rstrip()
        if rstripped + '\n' != line and line.strip() != '':
            # Has trailing whitespace and is not a blank line
            fixed_lines.append(rstripped + '\n')
            file_changed = True
        elif rstripped != line.rstrip('\n'):
            # Blank line with spaces
            fixed_lines.append('\n')
            file_changed = True
        else:
            fixed_lines.append(line)

    if file_changed:
        with open(fp, 'w', encoding='utf-8', newline='') as f:
            f.writelines(fixed_lines)
        count = sum(1 for o, n in zip(lines, fixed_lines) if o != n)
        total_fixed += count
        print(f'Fixed: {os.path.basename(fp)} ({count} lines)')

print(f'\nTotal: {total_fixed} lines fixed in {len(files)} files')