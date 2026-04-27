---
name: "02-paper-journal"
description: "基于 01-story.md 推荐期刊并生成格式要求。用于选择目标发表venue。"
allowed-tools: Read, Write, Glob, mcp__kimi-code__kimi_web_search, mcp__kimi-code__kimi_fetch_url, mcp__MiniMax__web_search, WebSearch, WebFetch, mcp__codex__codex
---

# 02-paper-journal

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于 `01-story.md` 推荐期刊并生成格式要求。

## 输入

- `01-story.md`
- `skills/shared/templates/venue-requirements.json`（支持的期刊列表）

## 输出

- `02-journal-recommendation.md` — 推荐 1-2 个期刊及理由（主要语言要用中文，名词等专业用语可以保留英文）
- `02-journal-requirements.md` — 选中期刊的格式要求（主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 分析 story

读取 `01-story.md`，提取：
- 研究领域/主题
- 贡献类型（理论/实验/应用）
- 预期贡献度

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查期刊推荐计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下期刊推荐计划是否合理：

    Story: {01-story.md 内容摘要}
    执行计划: 根据 story 主题匹配 1-2 个候选期刊

    检查：要点见 codex-review-template.md
```

### Step 3: 读取支持的期刊列表

读取 `skills/shared/templates/venue-requirements.json`，获取所有支持的期刊及其基本信息。

### Step 4: 推荐期刊

先按优先级做外部检索（仅当前一工具不可用时才降级）：`mcp__kimi-code__kimi_web_search` → `mcp__MiniMax__web_search` → `WebSearch`；需要抓取期刊官网或 CFP 细节时按优先级使用：`mcp__kimi-code__kimi_fetch_url` → `WebFetch`。

根据 story 主题匹配推荐 1-2 个候选期刊。

每条推荐包含：
- 期刊/会议名称
- 匹配理由
- 格式要求摘要

### Step 5: 用户选择

展示推荐，等待用户选择目标期刊。

### Step 6: 生成 requirements

从 `venue-requirements.json` 读取选中期刊的详细要求，生成 `02-journal-requirements.md`：

```markdown
---
venue_key: [如 neurips / nature / prl]
---

# 期刊要求

## 基本信息
- venue_key: [如 neurips / nature / prl]
- 名称: [期刊名]
- 类型: [conference/journal]
- 年份: [年份]

## 格式要求
- 摘要字数: 最多 [N] 字
- 页数限制: [N] 页
- 页数计算: [包含/不包含哪些部分]
- 字数限制: [N] 字（如有）

## 引用格式
- 风格: [numeric/author-year]
- LaTeX 包: [natbib/cite]
- 命令: [\\citep{}/\\cite{}]
- BibTeX 样式: [.bst 文件名]

## 图表要求
- 最少图表: [N] 张
- 格式: [pdf]
- 标题位置: [top/bottom/separate]

## 提交要求
- 匿名: [true/false]
- 作者信息: [说明]
- 伦理声明: [required/optional]
- 可复现性清单: [true/false]
- 补充材料: [allowed/not allowed]

## 实验要求
- 消融实验: [required/not required]
- 说明: [描述]
```

从 `skills/shared/templates/venue-requirements.json` 中提取对应期刊的完整配置。

`02-journal-requirements.md` 必须写入 `venue_key`（front matter + 基本信息字段），供 `/03-00-paper-structure` 与 `/05-01-paper-template` 统一解析。

### Step 7: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查两件事：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下两项：
    1. 期刊推荐是否匹配 story 的贡献度？
    2. requirements 文件格式是否完整？（必须包含：基本信息/格式要求/引用格式/图表要求/提交要求/实验要求）

    Story: {story 内容}
    推荐: {02-journal-recommendation.md}
    Requirements: {02-journal-requirements.md}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 recommendation/requirements → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...
