---
name: "02-paper-journal"
description: "基于 01-story.md 推荐期刊并生成格式要求。用于选择目标发表venue。"
allowed-tools: Read, Write, WebSearch, WebFetch, mcp__codex__codex
---

# 02-paper-journal

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 `01-story.md` 推荐期刊并生成格式要求。

## 输入

`01-story.md`

## 输出

- `02-journal-recommendation.md` — 推荐 1-2 个期刊及理由（主要语言要用中文，名词等专业用语可以保留英文）
- `02-journal-requirements.md` — 选中期刊的格式要求（主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 分析 story

读取 `01-story.md`，提取：
- 研究领域/主题
- 贡献类型（理论/实验/应用）
- 预期贡献度

### Step 2: 推荐期刊

支持的期刊：
- **ML会议**: neurips (9页), icml (8页), iclr (9页), aaai (7页)
- **物理/复杂系统**: pre (10页), prl (3750词/约4-6页), prx (15页), chaos (10页), njp (无限制), jstat (无限制), jmp (无限制), cn (无限制)
- **数值计算**: jcp (无限制), cpc (无限制)
- **综合/跨学科**: nature (约8页), science (约10页)

根据 story 主题匹配推荐 1-2 个候选期刊。

每条推荐包含：
- 期刊/会议名称
- 匹配理由
- 格式要求摘要

### Step 3: 用户选择

展示推荐，等待用户选择目标期刊。

### Step 4: 生成 requirements

从 `venue-requirements.json` 读取选中期刊的详细要求，生成 `02-journal-requirements.md`：

```markdown
# 期刊要求

## 基本信息
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
- 格式: [pdf/png/eps/tiff]
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

从 `../shared/templates/venue-requirements.json` 中提取对应期刊的完整配置。

### Step 5: Codex Review

调用 `mcp__codex__codex` 检查推荐是否匹配 story 的贡献度：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下期刊推荐是否匹配 story 的贡献度：

    Story: {story 内容}
    推荐: {recommendation 内容}

    检查要点：
    1. 期刊级别是否匹配贡献度？
    2. 格式要求是否可满足？
```
