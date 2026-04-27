---
name: "project-import-03-experiment-recovery"
description: "条件性恢复 03-02 与 04 阶段材料，并做证据边界一致性检查。"
allowed-tools: Read, Write, Glob, Grep, mcp__codex__codex
---

# project-import-03-experiment-recovery

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

恢复理论/实验层材料，但仅在证据充足时生成。

## 输入
- `01-story.md`
- `03-00-structure.md`
- 原项目中的方法说明、附录、脚本、配置、日志、图表、结果表

## 输出（按证据充足度）
- `03-02-theory-analysis.md`（条件性）
- `04-00-experiments.md`
- `04-02-experiment-results.md`（条件性）

## 工作流

### Step 1: 条件性恢复 03-02
仅当已有理论证据充足（推导/证明草稿/附录/方法说明）时生成。
若仅有局部理论直觉，必须标注“不完整/待确认”。

### Step 2: 生成 04-00 实验设计映射
从脚本/配置/草稿恢复：实验名称、claim、数据集、baseline、指标、ablation/robustness。
无法追溯者标为“推测/待确认”。

### Step 3: 条件性生成 04-02 结果文档
只有在已有清晰结果产物（CSV/JSON/图表/日志）时生成。
证据不足则不生成。

### Step 4: 一致性 Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查导入结果是否超出原项目证据；有问题则迭代修正。

## 约束
- 不默认重建 `04-01-experiment-code/`。
- 不新增不存在的实验结果。
- 不把 medium confidence 结论升级为 high confidence。