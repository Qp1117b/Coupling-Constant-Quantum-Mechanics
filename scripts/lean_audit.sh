#!/usr/bin/env bash
# Lean 严谨性审计 —— 对齐 提示词.md 第 7 条与 科研AI全栈方案.md §4.3
# 检测：sorry/admit、axiom、native_decide/unsafe、可疑占位、结论统计
# 退出码：0=无候选  1=存在候选（须人工复核）  2=环境错误
set -uo pipefail

RED='\033[0;31m'; YEL='\033[1;33m'; GRN='\033[0;32m'; CYN='\033[0;36m'; RST='\033[0m'
flag=0

LEAN_DIR="$(cd "$(dirname "$0")/.." && pwd)/06 Lean形式化"
if [ ! -d "$LEAN_DIR" ]; then
  echo -e "${RED}错误：未找到 Lean 目录 $LEAN_DIR${RST}"
  exit 2
fi

cd "$LEAN_DIR" || exit 2

echo -e "${CYN}========== Lean 严谨性审计 ==========${RST}"
echo -e "目录：$LEAN_DIR"
echo -e "时间：$(date '+%Y-%m-%d %H:%M:%S')\n"

# 1) sorry / admit
echo -e "${CYN}== 1) sorry / admit ==${RST}"
if out=$(grep -rn --include='*.lean' -E '\b(sorry|admit)\b' . | grep -v '.lake/'); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 2) 新增/遗留 axiom
echo -e "\n${CYN}== 2) 新增/遗留 axiom ==${RST}"
if out=$(grep -rn --include='*.lean' -E '^\s*axiom\s' . | grep -v '.lake/'); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 3) native_decide / unsafe / implemented_by
echo -e "\n${CYN}== 3) native_decide / unsafe / 逃逸 ==${RST}"
if out=$(grep -rn --include='*.lean' -E 'native_decide|@\[implemented_by|unsafe\b' . | grep -v '.lake/'); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 4) 可疑占位
echo -e "\n${CYN}== 4) 可疑占位（:= True / := 0 / rfl 冒充定理）==${RST}"
if out=$(grep -rn --include='*.lean' -E ':\s*Prop\s*:=\s*True|:=\s*0\b' . | grep -v '.lake/'); then
  echo -e "${YEL}$out${RST}"; flag=1
else echo -e "${GRN}  无${RST}"; fi

# 5) 结论统计
echo -e "\n${CYN}== 5) 定理/引理统计 ==${RST}"
grep -rc --include='*.lean' -E '^\s*(theorem|lemma)\s' . 2>/dev/null \
  | grep -v ':0$' | grep -v '.lake/' || echo "  无"

# 6) axiom 计数
echo -e "\n${CYN}== 6) axiom 计数 ==${RST}"
ax_count=$(grep -rn --include='*.lean' -E '^\s*axiom\s' . 2>/dev/null | grep -vc '.lake/')
thm_count=$(grep -rn --include='*.lean' -E '^\s*(theorem|lemma)\s' . 2>/dev/null | grep -vc '.lake/')
echo "  axiom = $ax_count   theorem+lemma = $thm_count"

echo -e "\n${CYN}====================================${RST}"
if [ $flag -eq 0 ]; then
  echo -e "${GRN}审计通过：未发现可疑候选。${RST}"
else
  echo -e "${YEL}发现候选：以上标记须人工结合 提示词.md 语义裁定是否构成欺骗/绕过。${RST}"
fi
exit $flag