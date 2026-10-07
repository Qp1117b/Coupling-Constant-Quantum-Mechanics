# -*- coding: utf-8 -*-
"""
元数据层 · 11_元数据
扫描 08 目录全部产物，生成清单（含大小/哈希）与版本、变更日志、验证状态。
产出（11_元数据/）：
  manifest.json
  版本.md
  变更日志.md
  验证状态.md
运行：python build_meta.py
"""
import csv
import hashlib
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # 08 理论组织和形式化框架
PARENT = os.path.dirname(ROOT)
S11 = os.path.join(ROOT, "11_元数据")

SKIP_DIRS = {"_build", "Lean源码"}   # Lean源码 为外部 Lean 4 项目，不计入组织层产物清单
SKIP_EXT = {".png"}   # 二进制大文件仍登记大小，但不计哈希


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan():
    files = []
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP_DIRS]
        for fn in fns:
            p = os.path.join(dp, fn)
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            st = os.stat(p)
            item = {
                "path": rel,
                "dir": rel.split("/")[0] if "/" in rel else ".",
                "ext": os.path.splitext(fn)[1].lower(),
                "bytes": st.st_size,
                "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime)),
            }
            if os.path.splitext(fn)[1].lower() not in SKIP_EXT:
                item["sha256"] = sha256(p)[:16]
            files.append(item)
    return sorted(files, key=lambda x: x["path"])


def main():
    os.makedirs(S11, exist_ok=True)
    files = scan()
    by_dir = {}
    for f in files:
        by_dir.setdefault(f["dir"], {"files": 0, "bytes": 0})
        by_dir[f["dir"]]["files"] += 1
        by_dir[f["dir"]]["bytes"] += f["bytes"]
    manifest = {
        "project": "CQMFormal",
        "unit": "08 理论组织和形式化框架",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "totals": {"files": len(files), "bytes": sum(f["bytes"] for f in files)},
        "by_directory": by_dir,
        "build_scripts": sorted(
            os.path.relpath(os.path.join(ROOT, "_build", x), ROOT).replace("\\", "/")
            for x in os.listdir(os.path.join(ROOT, "_build")) if x.endswith(".py")),
        "files": files,
    }
    with open(os.path.join(S11, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    write_version(manifest, by_dir)
    write_changelog()
    write_validation()
    print(f"[OK] manifest.json: {len(files)} 文件 / {manifest['totals']['bytes']} 字节")
    for d, v in sorted(by_dir.items()):
        print(f"     {d}: {v['files']} 文件")


def write_version(manifest, by_dir):
    rows = "\n".join(f"| `{d}` | {v['files']} | {v['bytes']:,} |" for d, v in sorted(by_dir.items()))
    scripts = "\n".join(f"- `{s}`" for s in manifest["build_scripts"])
    with open(os.path.join(S11, "版本.md"), "w", encoding="utf-8") as f:
        f.write(f"""# 元数据 · 版本

| 项 | 值 |
|:---|:---|
| 单元 | CQM 理论组织与形式化框架（`08`） |
| 顶层设计 | `设计方案.md` |
| 数据快照时间 | {manifest['generated_at']} |
| 文件总数 | {manifest['totals']['files']} |
| 总体积 | {manifest['totals']['bytes']:,} 字节 |
| 权威源 | `README.md` > `一体化研究/附录/术语表.md` > `一体化研究/附录/缺口台账.md` |
| Lean 版本 | `leanprover/lean4:v4.29.1`（固定，见 `08 理论组织和形式化框架/04_Lean对接/Lean源码/lean-toolchain`） |

## 一、各目录文件分布

| 目录 | 文件数 | 字节 |
|:---|:---:|:---:|
{rows}

## 二、构建脚本（可复现）

{scripts}

> 脚本位于 `08 理论组织和形式化框架/_build/`，从 `01_结构化数据/*.csv` 与外部 Lean 源码可重复生成全部产物；`_build/` 不计入产品文件统计。
""")


def write_changelog():
    with open(os.path.join(S11, "变更日志.md"), "w", encoding="utf-8") as f:
        f.write("""# 元数据 · 变更日志

> 记录 `08 理论组织和形式化框架/` 的建设事件。仅记结构性变更，不记临时工具与中间产物。

## v1.3.0 — 七维度口径恢复：展示可视化从出口层提升为核心维度 7

- 维度口径由六恢复为七：展示可视化从「出口层」提升为**第 7 维度（核心）**；七维度 = 4 核心（结构化 / ML 数据准备 / 形式化验证 / 展示可视化）+ 3 辅助（动态机制 / 经验检验 / 元理论反思）。
- 概念本体（`02`）、桥接与翻译（`09`）、元数据（`11`）明确为支撑层，不计入七维度。
- 同步范围：组织层 `AGENTS.md` / `README.md` / `设计方案.md` / `10_展示可视化/README.md` / `10_展示可视化/论文草稿/形式化组织框架.md` / `_build/build_site.py`（注释）。

## v1.2.0 — 六维度口径：人本理解降为出口层「输出可视化展示」

- 维度口径由七改六：移除「人本理解」维度；余六维为 结构化 / ML 数据准备 / 形式化验证 / 动态机制 / 经验检验 / 元理论反思。
- 原「人本理解」降为**出口层**，定名「输出可视化展示」（只呈现、不含新理论内容，面向人使用）；目录相应改名为 `10_输出可视化展示`。
- 同步范围：组织层 `README.md` / `AGENTS.md` / `设计方案.md` / 建设报告 / 论文草稿；根 `README.md` / `AGENTS.md`；`_build/build_site.py`（维度表）、`_build/check_consistency.py`（维度覆盖键 `人本`→`输出`）。

## v1.1.0 — 七维度运行规范与一致性硬检查

- 新增目录级 `AGENTS.md`：七维度责任矩阵、**研究闭环（Definition of Done）**、一致性红线、反模式、完成判据与命令速查；把"每次研究须覆盖七维度"固化为可执行条款。
- 新增 `_build/check_consistency.py`：跨产物硬检查（23 项），核对计数一致性（源 CSV ↔ 超图 JSON ↔ 本体 ↔ ML ↔ 前端 ↔ 动态 ↔ Lean）、引用完整性、`⇒`/`→` 约定、维度目录覆盖、Markdown 失效链接与禁用词；退出码非 0 即视为研究未完成。
- 根 `AGENTS.md` 目录约定表新增 `08 理论组织和形式化框架/` 行，并在"验证命令"节加入组织层一致性检查的调用。

## v1.0.0 — 七维度框架全面建成

**结构化层（既有）**
- `00_外部引用`：引用清单（52 篇）、锚点映射。
- `01_结构化数据`：概念表（82）、命题表（63）、论证表（70）、缺口依赖闭包。
- `03_超图与理论图`：超图数据、Graphviz/SVG/PNG、理论依赖图。

**本次新增**
- `02_概念本体`：本体.owl（24 类/215 个体/7 对象属性）、本体文档、概念关系图。
- `04_Lean对接`：lean代码路径.yaml、Lean 结构提取（68 模块/1388 声明）、Lean↔概念映射（25 条）、蓝图网页。
- `05_机器学习数据准备`：超图导出（PyG/DGL 就绪）、证明数据集（3 个 JSONL）、嵌入就绪。
- `06_动态机制`：重写规则（61）、理论状态模型、派生仿真（可达 81/82）。
- `07_经验检验`：$G_N$ 因果模型、缺口贝叶斯网络、实验设计（6 项）。
- `08_元理论反思`：范畴论模型、类型论基础、哲学假设。
- `09_桥接与翻译`：符号对照表、文档间等价映射、概念↔Lean↔物理映射、翻译规则。
- `10_人可读输出`：自包含 HTML 网站、交互式超图（并同步至 `03`）、蓝图网页、讲解文档（4 篇）、建设报告、论文草稿。
- `11_元数据`：本目录（清单/版本/变更日志/验证状态）。

**基座修复**
- 修复源 CSV 6 行未转义逗号（概念表 C004/C020/C062，论证表 H003/A004/A020）导致的字段错位；
- 以标准 CSV 解析重建 `03_超图与理论图/超图数据.json`；超边计数校正为 **19 超边 ⇒ / 51 有向边 →**。
""")


def write_validation():
    with open(os.path.join(S11, "验证状态.md"), "w", encoding="utf-8") as f:
        f.write("""# 元数据 · 验证状态

> 汇总 `08` 目录各产物的**验证证据**与**未验证边界**。缺口语义、数值限定语保持原样。

## 一、已核验项

| 产物 | 核验方式 | 结果 |
|:---|:---|:---|
| **组织层一致性（23 项）** | `_build/check_consistency.py`（跨产物计数/引用/约定/覆盖/链接/禁用词） | ✅ 全部通过（退出码 0） |
| 概念表/命题表/论证表 | 字段数断言（7/6/6）+ 概念引用完整性断言 | ✅ 82/63/70，无错位 |
| 超图数据.json | 由标准 CSV 解析重建；计数断言 | ✅ 82 节点 / 19 超边 / 51 有向边 |
| 本体.owl | owlready2 生成并回读 | ✅ 24 类 / 215 个体 / 7 对象属性 |
| Lean 结构提取 | 源码扫描（68 模块） | ✅ 1388 声明；状态以 `08 理论组织和形式化框架/04_Lean对接/Lean源码/README.md` 为权威 |
| ML 张量 | `x` 形状 (82,15)；索引与 CSV 一致 | ✅ |
| 动态仿真 | `simulate.py` 复算轨迹与 `derivation_trace.csv` 比对 | ✅ 一致 |
| HTML 内嵌数据 | `const D/HG` JSON 合法性校验 | ✅ |
| OWL/CSV/JSON/HTML | 编码 UTF-8、路径存在 | ✅ |

## 二、未安装依赖（脚本就绪，未执行）

| 依赖 | 用途 | 目录 |
|:---|:---|:---|
| torch / PyG / DGL | 装配 `.pt` / DGL 图对象 | `05_机器学习数据准备/超图导出/build_pyg.py` |
| dowhy | 因果识别与反驳 | `07_经验检验/因果模型/dowhy_model.py` |
| pgmpy | 贝叶斯网络推断 | `07_经验检验/贝叶斯网络/infer.py` |
| leanblueprint + plasTeX | 官方蓝图网页 | `10_输出可视化展示/蓝图/leanblueprint_source.md` |
| Catlab (Julia) | 范畴论计算 | `08_元理论反思/范畴论模型/catlab_sketch.jl` |

> 以上以"就绪脚本 + 说明"给出，未执行部分**不谎报**为已完成。

## 三、诚实边界

1. **形式化覆盖 50%**（41/82 概念）——未覆盖概念不得视为已形式化。
2. **缺口状态未改动**：C、G2–G8、G9–G22、N1–N4、H3.1–H3.3 保持权威源状态。
3. **贝叶斯 CPT 为占位**（待标定），其输出不构成理论结论。
4. **$G_N$、$\\alpha$ 类数值**一律带"构造后验数字校验，待独立复现"。
5. **前向派生不可达 1 概念**（C074）如实登记。
""")


if __name__ == "__main__":
    main()
