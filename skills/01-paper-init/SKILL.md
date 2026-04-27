---
name: "01-paper-init"
description: "从研究想法生成 01-story.md。用于开始新论文项目时定义叙事逻辑。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 01-paper-init

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

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
- 建议的 story framing（探索路径/关键发现/深层理解）

在此基础上补足仍不清楚的部分；如果没有 `00-02-idea-recommendation.md`，则直接追问以下问题：
- 我们想理解/探索什么问题？
- 我们打算从哪个角度切入？
- 我们预期会发现什么？
- 我们如何解释这些发现？

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查 story 生成计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 story 生成计划是否合理：

    输入来源: {00-02-idea-recommendation.md 或用户描述}
    执行计划: 基于 story-template.md 生成探索→发现→理解框架

    检查：要点见 codex-review-template.md
```

### Step 3: 生成 story.md

基于 `skills/shared/story-template.md` 模板生成 `01-story.md`，确保覆盖：
- 核心问题（我们想理解什么）
- 探索路径（我们怎么切入）
- 关键发现（我们预期发现什么）
- 深层理解（我们如何解释）
- 贡献（新理解的价值）

### Step 4: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查叙事逻辑：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 story 的叙事逻辑：

    {story 内容}

    检查要点：
    1. 探索路径是否清晰？我们如何切入问题？
    2. 预期发现是否具体？是否有意外发现的潜力？
    3. 深层理解是否回应了探索动机？
    4. 贡献是否体现了"理解了什么"而非仅仅是"解决了什么"？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 story → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...

### Step 5: 输出确认

输出：
- `01-story.md` 已生成
- 总结核心论点
- 若当前还没有经过 `00` 阶段，可提示可选前置步骤：`/00-00-idea-brainstorm` → `/00-01-idea-evaluate` → `/00-02-idea-recommend`
- 提示下一步：`/02-paper-journal`
