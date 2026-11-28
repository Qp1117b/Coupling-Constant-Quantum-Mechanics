# CQM — Lean 源码目录（工具链基线）

**当前状态（2026-11-27）**：本目录当前工作树不含 `SuperconductivityChain` 库（`Basic`／`Gaps`／`Stage1`–`Stage9`，12 模块 / 124 声明 / 60 定理，2026-11-21 `lake build` 2902 jobs 通过），`lakefile.toml` 也不再声明 `lean_lib`。原因：该库从未被研究侧 import——`10 探索/超导第一性研究/05_Lean验证` 的证明模块只 `import Ring15Spec`，两套形式化互不接线。

保留内容：`lakefile.toml`（仅 `require mathlib`）、`lean-toolchain`（`v4.29.1`）、`lake-manifest.json`、本 README、`.github/`。`_build/build_lean.py` 仍可运行，但抽取结果为空集。

## 当前形式化在哪

`10 探索/超导第一性研究/05_Lean验证/`：

- `Ring15Spec.lean` — Spec v52，只 import Mathlib 基线，不含任何证明模块
- 52 个在闸证明模块（`Ring15Lock*` 等），统一 `import Ring15Spec`
- `a_gate.ps1` — 一键闸：编译 52 模块 → `#print axioms` 白名单 → `#check` 类型 ≡ Spec → token 卫生
- 实测口径（第 235 轮）：52/52 编译、124/124 axioms、101/101 type、FAIL 0

## 历史

本目录旧库 12 模块源码与映射在 git 历史 `53af525`（`08 理论组织和形式化框架/04_Lean对接/Lean源码/SuperconductivityChain*`），需要可从中取回。旧库内 GN 库 107 定理（零 `sorry`、零新增 `axiom`）的审计记录随库退役，原始证据文档不可读；记录见变更日志 v1.9.46（GN 101 → 107）。

## 相关文档

- 研究侧口径：`10 探索/超导第一性研究/PROGRESS.md`、`DISCARD.md`、`00_当前有效口径表.md`
- 缺口台账：`08 理论组织和形式化框架/附录/缺口台账.md`
- 本层说明：`04_Lean对接/README.md`
