---
name: "06-02-review-apply"
description: "依据 review action plan 修改项目内容，并记录修改落实情况。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 06-02-review-apply

根据 `06-01-review-action-plan.md` 执行已经确认的修改，并记录落实情况。

## 输入

- `06-01-review-action-plan.md`
- 当前项目文件：
  - `01-story.md`
  - `03-structure.md`
  - `04-00-experiments.md`
  - `04-02-experiment-results.md`
  - `05-template/`
- `06-01-review-open-questions.md`（如存在，且已由用户确认）

## 输出

- 更新后的项目文件
- `06-02-review-resolution.md` — 每条 review 意见的最终落实记录（主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 读取 action plan

读取 `06-01-review-action-plan.md`，只处理：
- `accept`
- `partial`

默认不处理：
- `reject`
- `defer`
- `confirm`（除非用户已明确确认）

### Step 2: 按源头优先顺序修改

修改顺序：
1. `01-story.md`
2. `03-structure.md`
3. `04-00-experiments.md`
4. `04-02-experiment-results.md`
5. `05-template/`

要求：
- 先改源头文件，再改 LaTeX
- 不要只在 `05-template/` 里头痛医头
- 如果 review 影响核心主张，必须先改 `01-story.md`
- 如果 review 影响章节组织，必须先改 `03-structure.md`
- 如果 review 指向实验不足，应先更新 `04-*` 再决定是否修改正文

### Step 3: 记录落实情况

生成 `06-02-review-resolution.md`：

```markdown
# Review Resolution Log

## Applied
- R1: 已修改，位置 ...

## Partially Applied
- R2: 仅修改了 ...

## Rejected
- R3: 未修改，原因 ...

## Pending
- R4: 待确认 ...
```

要求：
- 每条意见都要能在 resolution 中找到归宿
- 说明改动落到了哪些文件
- 若只部分落实，要说明为什么没有全部采用

### Step 4: Codex 审查

调用 `mcp__codex__codex` 检查修改是否与 action plan 一致：

```
mcp__codex__codex:
  prompt: |
    请检查以下修改是否严格遵循 review action plan：

    Action Plan: {06-01-review-action-plan.md}
    Updated Story/Structure/Experiments/Results: {updated files}
    Updated LaTeX: {05-template changes}
    Resolution Log: {06-02-review-resolution.md}

    检查要点：
    1. 是否漏改了应修改的 accept 项？
    2. 是否错误修改了 reject/defer 项？
    3. 是否存在只改 LaTeX、未改源头文件的问题？
    4. resolution log 是否与实际改动一致？
```

### Step 5: 输出下一步建议

最后总结：
- 哪些意见已落实
- 哪些意见仅部分落实
- 哪些问题仍待用户确认
- 建议下一步执行：
  - `/06-paper-review` 进行再审查
  - `/07-paper-compile` 重新编译论文
