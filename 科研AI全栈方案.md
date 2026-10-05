# CQMFormal 科研 AI 全栈方案

> 面向「耦合常数量子力学（CQM）」项目的 Agent / MCP / 工具 / 计算 / Lean 形式化一体化科研方案。
>
> **文档定位**：本方案是**工具与工作流的技术底座**，不修改、不引申、不评价任何 CQM 物理结论；所有涉及理论的表述均以 `README.md` 与 `01–09` 各文档的权威定义处为准（见 `.workbuddy/审校/00_修订基准与准则.md`）。
>
> **验收对齐**：直接服务 `提示词.md` 的最终验收标准 —— *“第一性使用构建的形式化理论和已有理论严格推出元素 FG（电子分布以及结合能等等的实验确定的数据、性质或公式方程）”*。

---

## 0. 三条红线（贯穿全流程，不可妥协）

| 红线 | 含义 | 技术保障 |
|:---|:---|:---|
| **不欺骗** | 不得用 `axiom` / `定义式证明` / 占位 `def` 冒充已证结论 | Lean 审计脚本 + CI 门禁（§4.4） |
| **不绕过** | 不得跳过未闭合缺口（C、G2–G8、G9–G22、N1–N4、H3.1–H3.3 等） | 缺口台账单一源 + 状态列强制保留（§3.1） |
| **不虚构** | 不得引入 CQM 未涉及的观点、术语、数值、文献 | 术语表 + 审校基准文本 + 变更日志可 `grep` 复核（§3.1） |

---

## 1. 项目现状诊断

### 1.1 资产盘点

| 资产 | 位置 | 规模/状态 |
|:---|:---|:---|
| 理论文档库 | `01 核心理论` … `09 精细引力（FG）`、`文献/` | 9 大主题、数十篇 Markdown + 4 篇 PDF 文献 |
| Lean 4 形式化 | `06 Lean形式化/` | 11 个库、**748 定理 + 30 公理**；Lean `v4.34.0`；依赖 `mathlib` + **`physlib`**（已在 `lakefile.toml` 中） |
| 超导材料设计器 | `08 超导/超导材料设计器/godot_project/` | Godot 4.6 + GDScript + Godot MCP（`godot-ai`），回归 105 + 冒烟 52 全通过 |
| AI 协作治理 | `.workbuddy/`、`提示词.md`、`.codeartsdoer/` | 审校基准、变更日志、会话记忆、OpenCode 插件 |
| 版本控制 | `.git/` | 已接 `origin/main`（历史记录含推送代理配置） |

### 1.2 Lean 编译与缺口现状（据 `06 Lean形式化/README.md`）

| 库 | 编译 | 主要问题 |
|:---|:---:|:---|
| CausalSet / CouplingSpace / CartanAlgebra / Decoherence / PhysicalConstants / PrimeGeometry / Methodology / GN | ✅ 通过 | GN 零 `sorry`、零新增 `axiom` |
| SpectralGeometry | ❌ 部分 | `RiemannXi.lean`（`HasDerivAt.mul` 单子不匹配、类型不匹配）；`GLnTrivialSpectralQuantum.lean` 坏导入 `Mathlib.Analysis.SpecialFunctions.Exp.Deriv`（4.34.0 已移除） |
| Superconductivity | ❌ 部分 | `FormalizationRigor.lean` 坏导入 `Mathlib.Topology.Definitions.Filter`；`ElementCartan`、`BridgeTheorems`、`DeepConstruction`、`DeepResearch` |
| FGChain | ❌ 多数 | `QuantumOscillation.lean:107` 正性未证出；`FiberBundle`/`CurvatureOperator`/`SyncOperator`/`Hierarchy` 等 10/12 不通过 |

**失败三分类**：① Mathlib 版本漂移（坏导入）② Mathlib API 变更 ③ 证明本身未通过。三类均先于最近一次审计存在。

### 1.3 关键风险清单

1. **公理依赖集中**：30 个 `axiom`/待证（H3.1、H3.2、C、黎曼、Mathieu、素数冻结、Tate 自对偶、G_N 变分原理…）—— 是严谨性的最大敞口。
2. **形式化与理论的映射一致性**：文档 ↔ Lean 的定义/术语/数值需一一对应，否则“证明”与“理论”脱节。
3. **可复现性**：`mathlib`/`physlib` 为本地 `path` 依赖，未锁定远端 `rev`；换机易漂移。
4. **非主流理论的可核查性**：README 已如实标注“构造后验数字校验，待独立复现”；方案须放大这种**如实标注 + 可复现**，而非削弱。

---

## 2. 总体架构（七层）

```
┌──────────────────────────────────────────────────────────────────────┐
│ L7 Agent 编排层   物理/数学科研 Agent + 审校 Agent + 形式化 Agent        │
├──────────────────────────────────────────────────────────────────────┤
│ L6 形式化验证层   Lean 4.34.0 · mathlib · physlib · aesop · LeanCopilot │
├──────────────────────────────────────────────────────────────────────┤
│ L5 数学/符号层    SymPy · Jacobian · Mathematica/Wolfram · 数值核查      │
├──────────────────────────────────────────────────────────────────────┤
│ L4 物理计算层     DFT(VASP/QE) · MD(LAMMPS) · 超导材料设计器 · 实验数据  │
├──────────────────────────────────────────────────────────────────────┤
│ L3 文献知识层     arXiv · Paper-Search · NASA ADS · Zotero              │
├──────────────────────────────────────────────────────────────────────┤
│ L2 文档治理层     权威基准 · 术语表 · 缺口台账 · 变更日志（.workbuddy）  │
├──────────────────────────────────────────────────────────────────────┤
│ L1 基础设施层     Git · Lake · CI(lean-action) · 版本锁定 · 复现脚本     │
└──────────────────────────────────────────────────────────────────────┘
        数据流：文献 → 文档治理 → 形式化 → 计算 → 实验比对 → 回写缺口台账
```

---

## 3. 逐层方案

### 3.1 L2 文档治理与审校层（强化现有 `.workbuddy` 流程）

现有 `.workbuddy/审校/00_修订基准与准则.md` 已是一份高质量“裁判文本”。本层在其上加**自动化**：

| 机制 | 落地物 | 说明 |
|:---|:---|:---|
| 单一权威源 | 维持 `00_修订基准与准则.md` + `README.md` 数值表 | 冲突裁定顺序不变 |
| 术语表 | `附录/术语表.md`（从 §2.1–2.4 生成） | 供自动化比对，不新增写法 |
| 缺口台账 | `附录/缺口台账.md` | 汇总 C/G2–G22/N1–N4/G13/G20… 与 Lean 状态，**与 Lean 审计脚本联动** |
| 变更日志 | 维持既有管道格式 | 每条可 `grep` 复核 |
| 一致性检查脚本 | `scripts/doc_audit.sh` | 检查：术语变体残留、`$…$` 成对、缺口标注未被“解决”化、失效相对链接、`⇒` 误用 |

**禁用词自动扫描**（对齐基准 §4.1）：
`已删除|已澄清|已修正|已解决|此前错误|旧版|已废弃|不再|现已统一|早期形式|本版`

### 3.2 L3 文献与知识层（MCP）

| 工具 | 星标 | 用途 |
|:---|:---:|:---|
| **blazickjp/arxiv-mcp-server** | 3190 | arXiv 分节读 LaTeX 原文、BibTeX、主题监控（对接 `文献/` 与各文档参考文献） |
| **openags/paper-search-mcp** | 2742 | 多源论文检索（arXiv/PubMed/OpenAlex 等） |
| **wp-a/nature-academic-search** | 291 | 中文友好，跨 CrossRef/PubMed/arXiv/OpenAlex/EuropePMC |
| **takashiishida/arxiv-latex-mcp** | 146 | arXiv LaTeX 源码精读（数学严谨性核对） |
| **io.github.54yyyu/zotero-mcp** | — | 若用 Zotero 管理 `文献/` |
| **prtc/nasa-ads-mcp** | 8 | 若涉及宇宙学/天体物理方向的文献检索 |

> 用途：为 `04 前沿研究`、`05 方法论与批判` 的文献引用提供**可溯源核对**（Voros、LeClair、Sierra、Tate、Berry–Keating 等）。

### 3.3 L5 数学 / 符号计算层

| 工具 | 星标 | 用途 |
|:---|:---:|:---|
| **sdiehl/sympy-mcp** | 85 | 符号推导、数值复核（相变量子 ☯、Mathieu、A₄ 本征值、κ 等） |
| **morluto/jacobian** | 197 | 面向 agent 的数学工具集 |
| **AbhiRawat4841/mathematica-mcp** | 51 | Wolfram Mathematica（闭式化简、级数） |
| **siqiliu-tsinghua/mma-mcp** | 32 | 本地 Wolfram Engine 封装 |
| WolframAlpha MCP | 86/75/55 | 快速核对（`akalaric/mcp-wolframalpha` 等） |

> **与 Lean 的分工**：符号层负责“**发现/复核数值**”，Lean 层负责“**证明**”。数值复核结果写入文档时，须带“构造后验数字校验，待独立复现”限定语（基准 §2.2）。

### 3.4 L4 物理计算与实验数据层（对齐元素 FG 验收）

| 方向 | 工具 | 星标 | 用途 |
|:---|:---|:---:|:---|
| DFT | **JiaxuanLiu-Arsko/VASPilot** | 116 | CrewAI+MCP 自动 VASP 计算，验证元素/晶胞结合能 |
| DFT 编排 | **The66user/dft-autopilot-mcp** | 3 | QE / VASP / Gaussian 编排（HPC） |
| MD | **Chenghao-Wu/MCP_LAMMPS** | 14 | LAMMPS 分子动力学（声子/晶格相关） |
| 材料计算 | **Nour-elhaq/scimcp** | 1 | LAMMPS / DFT / ML 分析 |
| 可视化 | **wjgoarxiv/pymol-mcp / ovito-mcp** | 1 / 4 | 分子可视化 / 轨迹分析 |
| 物理 Agent | **psi-oss/get-physics-done** | 968 | agentic 物理学家（推导辅助） |
| 物理核验 | **io.github.Ranshiv/noether-physics** | — | 方程量纲核验 + arXiv 复核 |
| 已有资产 | **超导材料设计器（Godot MCP）** | — | 已有，对接 DFT 做 T_c 预估校验 |

**实验数据基准源**（验收比对，非工具）：NIST/CODATA 常数、元素电子构型与结合能、超导 T_c 实验库（如 SuperCon / NIMS）。*（具体数据源以项目实际采用者为准，本方案不代拟。）*

### 3.5 L6 Lean 形式化层（专项，见 §4）

### 3.6 L7 Agent 编排层

| Agent | 星标 | 定位 |
|:---|:---:|:---|
| **get-physics-done** | 968 | 物理推导 Agent |
| **MCP-Agent**（lastmile-ai） | — | 可组合多 Agent 编排框架 |
| **oOo0oOo/lean-lsp-mcp** | 521 | 形式化 Agent 的 Lean 工具入口 |
| **lean-dojo/LeanDojo** | 841 | Lean 程序化交互/数据提取（做形式化 Agent 的底座） |
| 审校 Agent | 自建（对齐 `.workbuddy` 流程） | 文档一致性、缺口标注、变更日志 |
| 形式化 Agent | 自建 + LeanCopilot | 修复坏导入、补证缺口、审计欺骗 |
| 文献 Agent | 自建 + arxiv-mcp | 引用核对、术语溯源 |

**Agent 协作流程**（对齐 §5 闭环）：

```
文献 Agent ──引用核对──→ 审校 Agent ──一致性检查──→ 形式化 Agent
      │                        │                        │
      ▼                        ▼                        ▼
  arxiv/paper-search       doc_audit.sh          lean-lsp-mcp / LeanCopilot
      │                        │                        │
      └─────── 缺口台账 ←──────┴─────── lake build ─────┘
```

| 流程节点 | 输入 | 输出 | 工具 |
|:---|:---|:---|:---|
| 文献 Agent | 文档引用列表 | 引用核对报告（Voros/LeClair/Sierra/Tate/Berry–Keating 等） | arxiv-mcp + paper-search |
| 审校 Agent | 全库 .md | 术语/排版/缺口标注一致性报告 | `doc_audit.sh` + 术语表 |
| 形式化 Agent | Lean 源码 + 缺口台账 | 编译报告 + 欺骗审计 + 修复建议 | `lean_audit.sh` + lean-lsp-mcp + LeanCopilot |
| 物理 Agent | 理论公式 | 数值复核（带"构造后验数字校验"限定语） | sympy + wolfram |

### 3.7 L1 基础设施与 CI

- **工具链固定**：`lean-toolchain = leanprover/lean4:v4.34.0` 保持不变；升级须单独 PR + 全量 `lake build` 验证。
- **依赖锁定**：将 `mathlib`/`physlib` 的 `path` 依赖补充远端 `rev`（或提交 `lake-manifest.json` 的 git 版本），保证换机可复现。
- **CI**：GitHub Actions 使用官方 `leanprover/lean-action`（`lake build` + 审计脚本）。参考 `.github/workflows/lean.yml`（§6.3）。
- **构建缓存**：`~/.cache/mathlib` 预热，避免每次全量重编（对本机慢盘尤其重要，见 §8）。

---

## 4. Lean 形式化专项方案（严谨性核心）

### 4.1 修复优先级（按依赖与阻塞面排序）

| 优先级 | 目标 | 具体动作 |
|:---:|:---|:---|
| **P0** | 恢复可编译基线 | 修复坏导入：`GLnTrivialSpectralQuantum.lean`、`FormalizationRigor.lean`（重定位到 4.34.0 现行路径）；修 `RiemannXi.lean` 的 `HasDerivAt.mul` 与类型不匹配 |
| **P1** | SpectralGeometry 全绿 | `RiemannXi.lean` 修复（承 `A2.2` 与 GN 定理 1.1 的 Hadamard 侧）；`Mathieu.lean` 对齐现行 API |
| **P2** | FGChain 收敛 | 先解 `QuantumOscillation.lean:107` 正性证明（这是 FK 链源头）；再逐模块修复 FiberBundle→CurvatureOperator→SyncOperator→Hierarchy |
| **P3** | Superconductivity 收敛 | `ElementCartan`、`BridgeTheorems`、`DeepConstruction`、`DeepResearch` |
| **P4** | 缺口公理收敛 | 逐个把 `axiom` 升级为 `theorem`（已有先例：`bcsConstant_gt_one` 从 axiom 升级为 theorem） |

### 4.2 版本漂移治理

- 建立 `06 Lean形式化/维护记录.md`：记录每次 Mathlib/physlib 升级导致的 API 变更与修复。
- 用 `lake exe cache get` 拉取 mathlib 预编译缓存，降低全量编译成本。
- **禁止**在未全量 `lake build` 验证的情况下升级依赖。

### 4.3 严谨性审计（检测“欺骗/绕过/虚构/定义式/占位”）

审计脚本 `scripts/lean_audit.sh`，逐条对齐 `提示词.md` 的要求：

```bash
#!/usr/bin/env bash
# Lean 严谨性审计 —— 对齐 提示词.md 第 7 条
set -uo pipefail
cd "$(dirname "$0")/../06\ Lean形式化" 2>/dev/null || cd "$(dirname "$0")/../06 Lean形式化"
echo "== 1) sorry / admit =="
grep -rn --include=*.lean -E '\b(sorry|admit)\b' . | grep -v '.lake/' || echo "  无"
echo "== 2) 新增/遗留 axiom =="
grep -rn --include=*.lean -E '^\s*axiom\s' . | grep -v '.lake/' || echo "  无"
echo "== 3) native_decide / 逃逸 =="
grep -rn --include=*.lean -E 'native_decide|@\[implemented_by|unsafe\b' . | grep -v '.lake/' || echo "  无"
echo "== 4) 可疑占位（= True / 恒等 def / rfl 冒充定理） =="
grep -rn --include=*.lean -E ':\s*Prop\s*:=\s*True|= 0\b' . | grep -v '.lake/' || echo "  无"
echo "== 5) 结论统计 =="
grep -rc --include=*.lean -E '^\s*(theorem|lemma)\s' . 2>/dev/null | grep -v ':0$' | grep -v '.lake/' || true
```

> **输出必须人工复核**：脚本只标记候选，最终“是否构成欺骗”须结合 `提示词.md` 语义判定。

### 4.4 缺口台账 ↔ Lean 状态联动

- `附录/缺口台账.md` 每行标注：缺口编号、文档权威处、Lean 对应符号/模块、状态（`axiom` / `数值验证` / `已证明` / `待证明`）。
- CI 校验：台账中标记“已证明”的项，`lean_audit.sh` 不得在对应模块报出 `axiom`。

### 4.5 physlib 集成（物理形式化）

`lakefile.toml` 已引入 `physlib`（对应 `leanprover-community/physlib`，769★，物理结果 Lean 形式化）。建议：

- 用 `physlib` 的物理定义（量子力学、相对论、场论）为 CQM 相关构造提供**已形式化的基础层**，减少自建公理。
- 新增 Lean 模块时优先复用 `mathlib4` / `physlib` 的既有定义，避免“定义式证明”。

### 4.6 Lean 专用工具链

| 工具 | 星标 | 用途 |
|:---|:---:|:---|
| **oOo0oOo/lean-lsp-mcp** | 521 | 把 Lean LSP 工具暴露给 AI（诊断、`#check`、`#print`、goal 状态） |
| **lean-dojo/LeanCopilot** | 1328 | LLM 证明补全（`suggest`/`search` 策略） |
| **lean-dojo/LeanDojo** | 841 | Lean 程序化交互（构建形式化 Agent 底座） |
| **lean-dojo/ReProver** | 338 | 检索增强证明 |
| **deepseek-ai/DeepSeek-Prover-V2** | 1308 | 开源定理证明模型（补证候选） |
| **Goedel-LM/Goedel-Prover** | 239 | 自动化证明 |
| **leanprover-community/aesop** | 407 | 白盒自动化（已是 mathlib 依赖） |

---

## 5. 计算–形式化–实验 闭环（对齐元素 FG 验收）

```
① 理论文档（权威定义处）
      │  术语/公式/缺口标注
      ▼
② Lean 形式化（mathlib + physlib，审计通过）
      │  抽查一致性：文档定义 ↔ Lean 定义
      ▼
③ 数值复核（SymPy / Mathematica）
      │  与文档数值表比对（带“构造后验数字校验”限定语）
      ▼
④ 物理计算（VASP/VASPilot、LAMMPS、超导设计器）
      │  结合能 / 电子分布 / T_c 预估
      ▼
⑤ 实验数据比对（NIST/CODATA、元素实验数据、超导 T_c 库）
      │  偏差记录 + 缺口台账更新
      ▼
⑥ 回写：缺口收敛 / 新缺口登记（禁止“已解决”化）
```

**验收锚点**：第 ⑤ 步须能**第一性**地用②的形式化结果 + 已有理论，推出①中元素 FG（电子分布、结合能）的实验值/公式。任一环节缺口须如实登记，不得跳过。

---

## 6. 落地配置

### 6.1 MCP 配置（`mcp.json`，通用 `mcpServers` 形态）

```json
{
  "mcpServers": {
    "arxiv":        { "command": "uvx", "args": ["arxiv-mcp-server"] },
    "paper-search": { "command": "uvx", "args": ["paper-search-mcp"] },
    "sympy":        { "command": "uvx", "args": ["mcp-sympy"] },
    "lean":         { "command": "uvx", "args": ["lean-lsp-mcp", "--lean-project-path", "D:/WorkSpace/物理/CQMFormal/06 Lean形式化"] },
    "nasa-ads":     { "command": "uvx", "args": ["nasa-ads-mcp"],
                      "env": { "ADS_API_TOKEN": "<token>" } },
    "zotero":       { "command": "uvx", "args": ["zotero-mcp"],
                      "env": { "ZOTERO_API_KEY": "<token>", "ZOTERO_LIBRARY_ID": "<id>" } },
    "wolfram":      { "command": "uvx", "args": ["mcp-wolframalpha"],
                      "env": { "WOLFRAM_API_KEY": "<token>" } }
  }
}
```

> **已安装验证**（无需密钥）：`arxiv-mcp-server` v0.8.0 ✅、`paper-search-mcp` v0.1.4 ✅、`mcp-sympy` v0.1.0 ✅、`lean-lsp-mcp` v0.31.0 ✅（已配 `--lean-project-path`）。
> **需填密钥**：`nasa-ads`（ADS_API_TOKEN）、`zotero`（ZOTERO_API_KEY）、`wolfram`（WOLFRAM_API_KEY）。
> `jacobian` 在 PyPI 无包且 GitHub 构建失败（pplpy 依赖），已从配置移除；DFT/MD 类需本地软件与许可证，按需增补。

### 6.1a 多平台 MCP 配置指引

本方案 MCP 配置以 `mcp.json`（通用形态）为单一源，各平台按下表引用：

| 平台 | 配置文件 | 位置 | 说明 |
|:---|:---|:---|:---|
| **CodeArts** | `.mcp.json` | 项目根目录 | CodeArts 原生读取项目级 `.mcp.json`，已创建，内容与 `mcp.json` 一致 |
| **TRAE** | `mcp.json` | 项目根目录 | TRAE AI IDE 读取项目 `mcp.json`；或在 TRAE 设置面板手动添加各 server |
| **Codex（OpenAI 桌面）** | `~/.codex/config.json` | 用户目录 | 将 `mcpServers` 内容合并入 Codex 配置 |
| **ChatBox** | 设置面板 | GUI | 在 ChatBox 设置 → MCP 中逐条添加 server（command + args + env） |
| **workbuddy** | `.workbuddy/mcp.json` | workbuddy 目录 | 审校流程引用；可软链或复制 `mcp.json` |
| **zcode / 其他** | `mcp.json` | 项目根目录 | 通用 `mcpServers` 形态，支持 MCP 协议的工具均可引用 |

**token 填入**：各 `env` 中的 `<token>` / `<id>` 占位符须替换为实际 API 密钥后生效。未填 token 的 server（如 `arxiv`、`sympy`、`jacobian`、`lean`）无需认证即可使用。

**按需启用**：
- 文献核对：`arxiv` + `paper-search` + `nasa-ads`（+ `zotero` 若用 Zotero 管理 `文献/`）
- 数值复核：`sympy` + `jacobian` + `wolfram`
- 形式化：`lean`（Lean LSP 诊断、`#check`、goal 状态）
- DFT/MD：需本地 VASP/QE/LAMMPS + 许可证，按需增补（见 §3.4）

### 6.2 目录约定（增量，不改动现有结构）

```
CQMFormal/
├── 附录/                     # 新增：术语表.md、缺口台账.md
├── scripts/                  # 新增：doc_audit.sh、lean_audit.sh、repro_check.sh
├── .github/workflows/        # 新增：lean.yml、doc-audit.yml
├── .workbuddy/               # 既有：审校基准、变更日志、记忆
├── 06 Lean形式化/            # 既有：Lean 库
└── …                         # 既有文档目录（01–09）
```

### 6.3 CI 门禁（`.github/workflows/lean.yml` 参考）

```yaml
name: lean
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: leanprover/lean-action@v1
        with:
          build-args: --wfail
      - name: 严谨性审计
        run: bash scripts/lean_audit.sh
      - name: 文档一致性审计
        run: bash scripts/doc_audit.sh
```

> 目标：**绿色即“可编译 + 无可疑绕过”**；`--wfail` 使警告即失败，杜绝“带警告交付”。

---

## 7. 分阶段路线图

| 阶段 | 目标 | 产出 |
|:---:|:---|:---|
| **S0**（1–2 天） | 基线可复现 | `lean_audit.sh`/`doc_audit.sh` 落地；依赖 `rev` 锁定；CI 跑通（允许当前红色，先可视化） |
| **S1**（1 周） | P0 全绿 | 修复 3 处坏导入 + `RiemannXi` 基础错误；`lake build` 剩余失败数下降 |
| **S2**（2–3 周） | 形式化收敛 | SpectralGeometry 全绿 → FGChain 源头正性 → Superconductivity 模块 |
| **S3**（持续） | 缺口收敛 | 逐个 axiom→theorem；缺口台账状态实时更新 |
| **S4**（并行） | 计算–实验闭环 | DFT/MD 接入，元素 FG 数据比对，超导 T_c 校验 |

---

## 8. 质量与性能保障

### 8.1 高口碑工具选型原则

全部优先 **社区官方 / 高星** 来源：`leanprover-community`（lean4 9394★、mathlib4 4222★、physlib 769★、aesop 407★）、`lean-dojo`（LeanCopilot 1328★、LeanDojo 841★）、`psi-oss`（get-physics-done 968★）、`blazickjp`（arxiv 3190★）。

### 8.2 性能注意（结合本机环境）

- 本机 WSL 的 **VHDX 位于慢速 D 盘，冷启动约 28 s**；`mathlib` 首次全量编译与本方案的 CI 本地复现会明显偏慢。
- **建议**：`lake exe cache get` 预取缓存；重型编译放原生 Linux/HPC 或远程 CI；本地仅做增量 `lake build <库>`。

### 8.3 复现性清单

- [ ] `lean-toolchain` 固定 `v4.34.0`
- [ ] `mathlib`/`physlib` 锁定远端 `rev`
- [ ] CI 全绿（build + 两份审计）
- [ ] 变更日志每条可 `grep`
- [ ] 缺口台账与 Lean 状态一致

---

## 9. 风险与边界声明

1. 本方案是**工具/工作流方案**，不对 CQM 物理结论做任何判定或背书；理论状态以各文档与 `README.md` 的如实标注为准。
2. MCP / Agent 工具为第三方开源项目，星标为检索时快照，接入前须自行评估安全与许可证。
3. Lean 审计脚本仅**标记候选**，“是否构成欺骗/绕过”须人工结合 `提示词.md` 语义裁定。
4. 实验数据源需项目按学科规范自行确定，本方案不代拟具体数据集。
5. 任何“缺口”在闭合前，均须按基准 §4.2 保留标注，**禁止**改写为“已解决”。

---

## 附录 A：命令速查

```bash
# 编译（在 06 Lean形式化/ 下）
lake build                      # 全量
lake build GN                   # 单库
lake exe cache get              # 预取 mathlib 缓存

# 审计（在项目根目录）
bash scripts/lean_audit.sh
bash scripts/doc_audit.sh

# 本文档引用的核心来源
#   Lean 4        : https://github.com/leanprover/lean4
#   mathlib4      : https://github.com/leanprover-community/mathlib4
#   physlib       : https://github.com/leanprover-community/physlib   (原 PhysLean，官网 physlib.io)
#   lean-lsp-mcp  : https://github.com/oOo0oOo/lean-lsp-mcp
#   LeanCopilot   : https://github.com/lean-dojo/LeanCopilot
#   arxiv-mcp     : https://github.com/blazickjp/arxiv-mcp-server
```

## 附录 B：与现有规范的关系

- **不新增**任何 CQM 理论观点、术语、数值、编号、文献（对齐 `提示词.md` 与基准 §五）。
- 本方案仅规定**工具、流程、审计与复现**；理论内容的任何修订仍须依据 `00_修订基准与准则.md`。
- 本文件为新增技术文档，不影响既有文档体例与 `README.md` 导航。

---

*生成时间：2026-10-05 · 适用版本：`CQMFormal v0.7.0`（Lean 4.34.0）*