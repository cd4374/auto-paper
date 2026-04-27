---
name: "04-03-01-experiment-audit"
description: "复核 04-01 实现与 04-02 结果是否与 04-00 设计一致，并提炼 claim/theory 对应关系。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__codex__codex
---

# 04-03-01-experiment-audit

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

复核实现与结果，形成可进入图表资产与覆盖门控的分析基础。

## 输入
- `04-00-experiments.md`
- `04-01-experiment-code/`
- `04-02-experiment-results.md`
- `04-02-experiment-results/`
- `03-02-theory-analysis.md`（如已生成）

## 输出
- 更新/生成 `04-03-experiment-analysis.md`（至少包含）：
  - `## Summary`
  - `## Experiment-by-Experiment Review`
  - `## Theory vs Experiment`

## 工作流

### Step 1: Pre-review
调用 `mcp__codex__codex` 审查审计计划，检查是否覆盖：实现一致性、结果完整性、claim/theory 对照。

### Step 2: 复核实现与设计一致性
对照 `04-00` 与 `04-01`：
- 必需实验是否覆盖
- 数据、baseline、指标、输出是否一致
- 最小运行命令与结果来源是否可回溯
- 默认设置是否造成实现偏移

### Step 3: 复核结果完整性与可信度
对照 `04-02` 文档与原始产物：
- 必需实验是否完成
- 关键输出是否齐全
- 是否存在异常值、缺失项、日志报错、描述不一致
- baseline 比较是否公平，指标解释是否成立

### Step 4: 提炼 claim/theory 对应关系
输出：
- 已直接支撑的 claim
- 部分支撑的 claim
- 当前证据不足或被削弱的 claim
- theory prediction 的支撑/部分支撑/削弱/未测试

### Step 5: 写入分析文档
把审计结果写入 `04-03-experiment-analysis.md` 的对应章节。

### Step 6: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 校验文档可回溯性与结论边界；有问题则迭代修订。

## 约束
- 只写与当前 story/structure 直接相关的审计结论。
- 不新增未批准实验，不重跑无关任务。
- 路径不清或证据缺失时先询问用户。