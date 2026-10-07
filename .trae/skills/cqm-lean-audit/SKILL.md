---
name: cqm-lean-audit
description: CQM Lean 4 形式化严谨性审计。改动 08 理论组织和形式化框架/04_Lean对接/Lean源码/ 下任何文件，或提交前复核禁止项候选时加载：禁止项清单、缺口台账联动、依赖锁定与 lake build 验证。
---

# Lean 形式化规则

## 何时加载

- 改动 `08 理论组织和形式化框架/04_Lean对接/Lean源码/` 下任何文件；
- 提交前复核禁止项候选。

## 规则

1. **审计**：提交前须人工复核 `sorry`、`admit`、`native_decide`、`unsafe`、新增 `axiom` 候选。
2. **禁止**：`sorry`、`admit`、`native_decide`、`unsafe`、新增 `axiom`（除非登记缺口）。
3. **缺口台账**：`一体化研究/附录/缺口台账.md` 与 Lean 状态联动，标记"已证明"的项不得在对应模块报出 `axiom`。
4. **依赖锁定**：`lean-toolchain` 固定 `v4.29.1`；升级须单独 PR + 全量 `lake build`。

## 验证

```bash
# 在 08 理论组织和形式化框架/04_Lean对接/Lean源码/ 下
lake build
```