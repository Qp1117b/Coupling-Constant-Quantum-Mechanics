#!/usr/bin/env bash
# 文档一致性审计 —— 对齐 科研AI全栈方案.md §3.1 与 00_修订基准与准则.md §4
# 检测：禁用词、术语变体残留、$...$ 成对、失效链接、⇒ 误用、缺口"解决"化
# 退出码：0=无问题  1=存在问题（须人工复核）  2=环境错误
set -uo pipefail

RED='\033[0;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; CYN='\033[0;36m'; RST='\033[0m'
flag=0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || exit 2

echo -e "${CYN}========== 文档一致性审计 ==========${RST}"
echo -e "目录：$ROOT"
echo -e "时间：$(date '+%Y-%m-%d %H:%M:%S')\n"

# 扫描范围：理论文档（01-09、归档、README），排除配置/元文件
MD_FILES=$(find . -name '*.md' \
  -not -path './.lake/*' -not -path './.git/*' \
  -not -path './归档/归档\ CNT/*' -not -path './.workbuddy/*' \
  -not -path './.codeartsdoer/*' -not -path './.arts/*' \
  -not -path './06\ Lean形式化/.lake/*' \
  -not -name 'AGENTS.md' -not -name '科研AI全栈方案.md' \
  -not -name '提示词.md' -not -name 'mcp.json' 2>/dev/null)

# 1) 禁用词（修订过程性叙述）
echo -e "${CYN}== 1) 禁用词扫描（§4.1）==${RST}"
BANNED='已删除|已澄清|已修正|已解决|此前错误|旧版|已废弃|现已统一|早期形式|本版'
if out=$(echo "$MD_FILES" | xargs grep -rnE "$BANNED" 2>/dev/null); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 2) 术语变体残留
echo -e "\n${CYN}== 2) 术语变体残留（§2.4）==${RST}"
VARIANTS='普量子|谱量子|构造合法|同步辩证法|谱冻结|时空度规涨落|普适相变量子|随意组合|时空前沿同步速度|晶格量子振荡|前组织网络|引力因果场[^限]'
if out=$(echo "$MD_FILES" | xargs grep -rnE "$VARIANTS" 2>/dev/null); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 3) $...$ 成对检查
echo -e "\n${CYN}== 3) \$...\$ 定界符成对检查 ==${RST}"
for f in $MD_FILES; do
  n=$(grep -o '\$' "$f" 2>/dev/null | wc -l)
  if [ $((n % 2)) -ne 0 ]; then
    echo -e "${YEL}  $f : 奇数个 \$ ($n)${RST}"; flag=1
  fi
done
[ $flag -eq 0 ] && echo -e "${GRN}  全部成对${RST}" || true

# 4) 失效相对链接
echo -e "\n${CYN}== 4) 失效相对链接 ==${RST}"
link_flag=0
for f in $MD_FILES; do
  dir=$(dirname "$f")
  while IFS= read -r link; do
    target="$dir/$link"
    if [ ! -e "$target" ]; then
      echo -e "${YEL}  $f -> $link (不存在)${RST}"; link_flag=1; flag=1
    fi
  done < <(grep -oP '\]\(\K[^)]+\.md(?=\))' "$f" 2>/dev/null)
done
[ $link_flag -eq 0 ] && echo -e "${GRN}  无失效链接${RST}" || true

# 5) ⇒ 误用（应为 →）
echo -e "\n${CYN}== 5) ⇒ 误用检查（§2.5：⇒ 仅表重组实现）==${RST}"
if out=$(echo "$MD_FILES" | xargs grep -rn '⇒' 2>/dev/null | grep -vE '重组实现|重组|⇒.*SU|⇒.*GL|⇒.*\);'); then
  echo -e "${YEL}  以下 ⇒ 使用须人工确认是否为重组实现：${RST}\n$out"; flag=1
else echo -e "${GRN}  无可疑 ⇒${RST}"; fi

# 6) 缺口"解决"化检查
echo -e "\n${CYN}== 6) 缺口标注完整性（§4.2）==${RST}"
if out=$(echo "$MD_FILES" | xargs grep -rnE '缺口.*(已解决|已闭合|已证明)' 2>/dev/null); then
  echo -e "${RED}  疑似缺口"解决"化：${RST}\n$out"; flag=1
else echo -e "${GRN}  无${RST}"; fi

echo -e "\n${CYN}====================================${RST}"
if [ $flag -eq 0 ]; then
  echo -e "${GRN}审计通过：文档一致性无问题。${RST}"
else
  echo -e "${YEL}发现问题：以上标记须人工复核。${RST}"
fi
exit $flag