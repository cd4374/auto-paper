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
- 研究问题（是什么）
- 动机与价值（为什么）
- 方法思路（怎么做）

必须区分”直接证据支持”与”合理推断”。

### Step 3: 生成 `01-story.md`

按以下格式生成，中文为主、术语可保留英文。证据不足处必须显式标注"待确认/缺失"：

```
# 是什么
[研究的问题是什么？一句话定义研究问题，明确边界与范围]

# 为什么
[为什么要研究这个问题？动机/价值/应用场景。说明不做的代价或当前gap的严重性]

# 怎么做
[解决问题的思路是什么？核心方法概述，关键洞察是什么，与已有方法的核心差异]
```

### Step 4: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查 story 是否严格基于证据；有问题则迭代。

## 约束
- 不把无证据推断写成既成事实。
- 证据不足处必须显式标注“待确认/缺失”。