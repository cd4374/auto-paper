---
name: "01-paper-init"
description: "从研究想法生成 01-story.md。用于开始新论文项目时定义叙事逻辑。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 01-paper-init

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 3 — Post-review 迭代轮数上限。

从研究想法生成 `01-story.md`。

## 输入

- 用户描述的研究想法
- 可选：`00-02-idea-recommendation.md`（若已完成 idea funnel，则优先读取其中的主选 idea 与 story framing）

## 输出

`01-story.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 澄清研究想法

如果存在 `00-02-idea-recommendation.md`，优先读取其中的：
- 主选 idea
- 推荐理由
- 建议的 story framing（是什么 / 为什么 / 怎么做）

在此基础上补足仍不清楚的部分；如果没有 `00-02-idea-recommendation.md`，则直接追问以下问题：
- 研究的核心问题是什么？
- 为什么要解决这个问题？（动机/应用价值）
- 初步的方法思路是什么？
- 预期的贡献是什么？

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查 story 生成计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 story 生成计划是否合理：

    输入来源: {00-02-idea-recommendation.md 或用户描述}
    执行计划: 基于 story-template.md 生成是什么/为什么/怎么做三问

    检查：要点见 codex-review-template.md
```

### Step 3: 生成 story.md

基于 `skills/shared/story-template.md` 模板生成 `01-story.md`：

```markdown
# 是什么
[研究的问题是什么？]

# 为什么
[为什么要研究这个问题？动机/价值/应用场景]

# 怎么做
[解决问题的思路是什么？核心方法概述]
```

### Step 4: Post-review（迭代循环，最多 3 轮）

调用 `mcp__codex__codex` 检查叙事逻辑：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 story 的叙事逻辑：

    {story 内容}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 story → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

### Step 5: 输出确认

输出：
- `01-story.md` 已生成
- 总结核心论点
- 若当前还没有经过 `00` 阶段，可提示可选前置步骤：`/00-00-idea-brainstorm` → `/00-01-idea-evaluate` → `/00-02-idea-recommend`
- 提示下一步：`/02-paper-journal`
