# CQMFormal — Lean 源码目录（08 已清空库）

**状态更新（2026-11-27）**：本目录原有的唯一库 `SuperconductivityChain`（`Basic`／`Gaps`／`Stage1`–`Stage9`，12 模块 / 124 声明 / 60 定理，2026-11-21 `lake build` 2902 jobs 通过）**已移除**，连同 `lakefile.toml` 的 `lean_lib` 声明。删除理由：该库从未被研究侧 import——`10 探索/超导第一性研究/05_Lean验证` 的 46 个模块只 `import Ring15Spec`，两套形式化互不接线。

保留内容：`lakefile.toml`（仅 `require mathlib`）、`lean-toolchain`（`v4.29.1`）、`lake-manifest.json`、本 README、`.github/`。`_build/build_lean.py` 仍可运行，但抽取结果为空集。

## 当前形式化在哪

`10 探索/超导第一性研究/05_Lean验证/`：

- `Ring15Spec.lean` — Spec v46（840 行），只 import Mathlib 基线，不含任何证明模块
- 46 个证明模块（`Ring15Lock*`），统一 `import Ring15Spec`
- `a_gate.ps1` — 一键闸：编译 46 模块 → `#print axioms` 109 条白名单 → `#check` 91 条类型 ≡ Spec → token 卫生
- 实测口径：46/46 编译、109/109 axioms、91/91 type、FAIL 0

## 历史

移除前的 12 模块源码与映射在 git 历史 `fe37c3b`（`08 理论组织和形式化框架/04_Lean对接/Lean源码/SuperconductivityChain*`），需要可从中取回。

## 相关文档

- 研究侧口径：`10 探索/超导第一性研究/PROGRESS.md`、`DISCARD.md`、`00_当前有效口径表.md`
- 缺口台账：`08 理论组织和形式化框架/附录/缺口台账.md`
- 本层说明：`04_Lean对接/README.md`
