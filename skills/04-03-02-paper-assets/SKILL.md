---
name: "04-03-02-paper-assets"
description: "整理论文可用图表资产、生成 LaTeX 嵌入片段，并完成关键图图片审查。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__kimi-code__kimi_read_media, mcp__MiniMax__understand_image, mcp__codex__codex
---

# 04-03-02-paper-assets

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于已完成审计结果，生成最小必要论文图表资产并做图片审查。

## 输入
- `04-03-experiment-analysis.md`（来自 04-03-01 的审计结论）
- `04-02-experiment-results/`
- `03-00-structure.md`

## 输出
- `04-03-paper-assets/`
- `04-03-paper-assets/latex_includes.tex`
- 更新 `04-03-experiment-analysis.md` 的 `## Figure Review`

## 工作流

### Step 1: 选择最小必要资产
只保留可直接支撑当前 story/structure 的图表，命名需可回溯到实验或 claim。

### Step 2: 生成/整理 LaTeX 片段
写入 `04-03-paper-assets/latex_includes.tex`，要求：
- 宽度 `0.48\textwidth`（单栏）或 `0.95\textwidth`（双栏）
- caption 简洁完整
- label 使用 `fig:fig_name`

### Step 3: 图片审查（优先 Kimi）
对关键 figures 逐个审查：
- 字体、坐标轴、legend、annotation、colorbar 可读性
- panel 布局与子图编号
- 图-citation-正文一致性与科学表达清晰度

降级规则：
- 先 `mcp__kimi-code__kimi_read_media`
- 不可用时再 `mcp__MiniMax__understand_image`
- 必须记录降级原因

### Step 4: 写入 Figure Review
把结论写回 `04-03-experiment-analysis.md`：
- 哪些图可直接用于论文
- 哪些需小改
- 哪些需重绘

### Step 5: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查图表资产与审查结论是否可回溯、是否服务主线；有问题则迭代。

## 约束
- 不做无关重绘、不新增无关图表。
- 不把仅内部判断的图直接标为可写入论文。