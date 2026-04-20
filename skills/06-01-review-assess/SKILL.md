---
name: "06-01-review-assess"
description: "评估外部 review 意见的正确性与优先级，并生成结构化修改方案。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 06-01-review-assess

- REVIEWER_MODEL = `claude-opus-4-7` — Model used via Codex MCP.

先判断外部 review 意见是否成立，再生成结构化修改方案。

## 输入

- 外部 review 意见：评论、批注摘录、邮件、聊天记录、审稿意见列表
- 当前项目文件：
  - `01-story.md`
  - `03-00-structure.md`
  - `03-02-theory-analysis.md`
  - `04-00-experiments.md`
  - `04-01-experiment-code/`（实验代码，用于评估实现相关问题）
  - `04-02-experiment-results.md`
  - `04-03-experiment-analysis.md`
  - `05-template/`
  - `06-paper-review/report.md`（如已有）

## 输出

- `06-01-review-feedback.md` — 标准化整理后的 review 意见清单（主要语言要用中文，名词等专业用语可以保留英文）
- `06-01-review-action-plan.md` — 每条意见的处理结论与修改方案（主要语言要用中文，名词等专业用语可以保留英文）
- `06-01-review-open-questions.md` — 需要用户确认的问题（仅在存在歧义时生成）

## 工作流

### Step 1: 整理 review 意见

将原始 review 意见拆分、去重、标准化，写入 `06-01-review-feedback.md`。

每条意见至少记录：
- 编号（如 R1, R2）
- 原意见
- 来源
- 涉及位置（story / structure / experiments / results / analysis / writing）
- 初步严重性（critical / major / minor）

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查评估准备是否充分：

```
mcp__codex__codex:
  model: claude-opus-4-7
  prompt: |
    请检查以下 review 评估准备是否充分：

    Review 意见: {外部 review 摘要}
    项目文件: {01-story/03-00-structure/03-02/04/05 文件列表}

    检查：要点见 codex-review-template.md
```

### Step 3: 判断意见是否成立

对每条意见与当前项目内容对照，分类为：
- `accept` — 意见成立，应修改
- `partial` — 部分成立，应有限修改
- `reject` — 意见不成立，不应修改
- `defer` — 意见成立，但本轮暂不处理
- `confirm` — 信息不足，需要用户确认


要求：
- 不能默认 reviewer 一定正确
- 不能为了迎合 review 而破坏 story 主线
- 如果意见影响核心主张，必须回到 `01-story.md` 层判断
- 如果意见影响章节组织，必须回到 `03-00-structure.md` 层判断
- 如果意见指向理论假设、证明力度、理论表述边界或 theory–experiment mismatch，优先回到 `03-02-theory-analysis.md` 层判断
- 如果意见指向结果解释、图表质量或 claim 证据边界，优先回到 `04-03-experiment-analysis.md` 层判断

### Step 4: 生成 `06-01-review-action-plan.md`

按以下结构写入：

只保留本轮准备处理的最小必要修改集；不要把无关优化项或额外改写建议一起并入 action plan。

```markdown
# Review Action Plan

## Summary
- 总意见数:
- accept:
- partial:
- reject:
- defer:
- confirm:

## Itemized Decisions

### R1
- 原意见:
- 来源:
- 影响位置:
- 判断:
- 理由:
- 需要修改的文件:
- 修改策略:
- 风险:
```

要求：
- 每条意见都要给出理由，而不是只给结论
- 明确指出应改 `01/03-02/04/05` 哪一层
- 如果只是语言与表述问题，可限定只改 `05-template/`

### Step 5: 生成待确认问题

如果存在 `confirm` 项，生成 `06-01-review-open-questions.md`，列出：
- 不确定点
- 需要用户确认的选择
- 不同选择会影响哪些文件

### Step 6: Post-review

调用 `mcp__codex__codex` 检查 action plan：

```
mcp__codex__codex:
  model: claude-opus-4-7
  prompt: |
    请检查以下 review action plan 是否合理：

    Review 意见: {feedback}
    Story: {01-story.md}
    Structure: {03-00-structure.md}
    Theory Analysis: {03-02-theory-analysis.md}
    Experiments/Results: {04-*}
    Action Plan: {06-01-review-action-plan.md}

    检查：要点见 codex-review-template.md
```

### Step 7: 输出总结

最后总结：
- 多少条意见被 accept / partial / reject / defer / confirm
- 是否可以进入 `/06-02-review-apply`
- 若存在 `confirm` 项，应先等待用户确认
