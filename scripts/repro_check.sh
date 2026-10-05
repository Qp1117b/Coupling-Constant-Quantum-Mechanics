#!/usr/bin/env bash
# 复现性检查 —— 对齐 科研AI全栈方案.md §8.3
# 检测：lean-toolchain 固定、依赖 rev 锁定、CI 配置、变更日志 grep 可复核
# 退出码：0=全部满足  1=存在缺失  2=环境错误
set -uo pipefail

YEL='\033[1;33m'; GRN='\033[0;32m'; CYN='\033[0;36m'; RST='\033[0m'
flag=0

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LEAN_DIR="$ROOT/06 Lean形式化"
cd "$ROOT" || exit 2

echo -e "${CYN}========== 复现性清单检查 ==========${RST}"
echo -e "时间：$(date '+%Y-%m-%d %H:%M:%S')\n"

# 1) lean-toolchain 固定
echo -e "${CYN}[1] lean-toolchain 版本${RST}"
if [ -f "$LEAN_DIR/lean-toolchain" ]; then
  ver=$(cat "$LEAN_DIR/lean-toolchain")
  if echo "$ver" | grep -q 'v4.34.0'; then
    echo -e "${GRN}  ✓ 固定 v4.34.0${RST}"
  else
    echo -e "${YEL}  ✗ 版本非 v4.34.0：$ver${RST}"; flag=1
  fi
else
  echo -e "${YEL}  ✗ 缺少 lean-toolchain${RST}"; flag=1
fi

# 2) 依赖 rev 锁定
echo -e "\n${CYN}[2] mathlib/physlib 依赖锁定${RST}"
if [ -f "$LEAN_DIR/lakefile.toml" ]; then
  if grep -q 'rev\s*=' "$LEAN_DIR/lakefile.toml"; then
    echo -e "${GRN}  ✓ 已锁定远端 rev${RST}"
  else
    echo -e "${YEL}  ✗ path 依赖未锁定 rev（见方案 §3.7）${RST}"; flag=1
  fi
else
  echo -e "${YEL}  ✗ 缺少 lakefile.toml${RST}"; flag=1
fi

# 3) lake-manifest.json 存在
echo -e "\n${CYN}[3] lake-manifest.json${RST}"
if [ -f "$LEAN_DIR/lake-manifest.json" ]; then
  echo -e "${GRN}  ✓ 存在${RST}"
else
  echo -e "${YEL}  ✗ 缺少（建议 lake build 生成）${RST}"; flag=1
fi

# 4) 审计脚本存在
echo -e "\n${CYN}[4] 审计脚本${RST}"
for s in lean_audit.sh doc_audit.sh; do
  if [ -f "$ROOT/scripts/$s" ]; then
    echo -e "${GRN}  ✓ scripts/$s${RST}"
  else
    echo -e "${YEL}  ✗ 缺少 scripts/$s${RST}"; flag=1
  fi
done

# 5) CI 配置
echo -e "\n${CYN}[5] CI 门禁配置${RST}"
for w in lean.yml doc-audit.yml; do
  if [ -f "$ROOT/.github/workflows/$w" ]; then
    echo -e "${GRN}  ✓ .github/workflows/$w${RST}"
  else
    echo -e "${YEL}  ✗ 缺少 $w${RST}"; flag=1
  fi
done

# 6) 附录台账
echo -e "\n${CYN}[6] 附录台账${RST}"
for a in 术语表.md 缺口台账.md; do
  if [ -f "$ROOT/附录/$a" ]; then
    echo -e "${GRN}  ✓ 附录/$a${RST}"
  else
    echo -e "${YEL}  ✗ 缺少 附录/$a${RST}"; flag=1
  fi
done

echo -e "\n${CYN}====================================${RST}"
if [ $flag -eq 0 ]; then
  echo -e "${GRN}复现性清单全部满足。${RST}"
else
  echo -e "${YEL}存在缺失项，见上方标记。${RST}"
fi
exit $flag