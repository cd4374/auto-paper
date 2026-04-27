---
name: "project-import-01-survey-story"
description: "项目普查并恢复 01-story.md，严格区分直接证据与合理推断。"
allowed-tools: Bash, Read, Glob, Grep, Write, mcp__codex__codex
---

# project-import-01-survey-story

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

从既有项目恢复 narrative 基线与 story。

## 输入
- 现有项目目录，可能包含代码、结果、草稿、README、配置。

## 输出
- `01-story.md`
- 项目证据摘要（可写入 story 附录或内部记录）：high/medium/missing

## 工作流

### Step 1: 项目普查与证据分级
扫描并归类：
- narrative sources（abstract/introduction/conclusion/README）
- method sources（代码结构、配置命名）
- experiment sources（脚本、配置、入口）
- result sources（日志、表格、图表）

对每类证据标记 `high confidence` / `medium confidence` / `missing`。

### Step 2: 恢复 story 主线
提炼：
- 核心问题
- 探索路径
- 关键发现
- 深层理解

必须区分“直接证据支持”与“合理推断”。

### Step 3: 生成 `01-story.md`
参考 `skills/shared/story-template.md` 生成，中文为主、术语可保留英文。

### Step 4: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查 story 是否严格基于证据；有问题则迭代。

## 约束
- 不把无证据推断写成既成事实。
- 证据不足处必须显式标注“待确认/缺失”。