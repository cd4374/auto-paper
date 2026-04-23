---
name: "03-00-paper-structure"
description: "基于 01-story.md 和 02-journal-requirements.md 生成 03-00-structure.md。用于定义论文章节结构。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 03-00-paper-structure

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于 `01-story.md` + 期刊要求生成 `03-00-structure.md`。

## 输入

- `01-story.md`
- `02-journal-requirements.md`

## 输出

`03-00-structure.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 读取输入

读取 story 和 requirements。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查章节设计计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下章节设计计划是否合理：

    Story: {01-story.md 内容摘要}
    Journal Requirements: {02-journal-requirements.md 格式限制}
    执行计划: 根据叙事逻辑设计章节，每章填写叙事内容+需求

    检查：要点见 codex-review-template.md
```

### Step 3: 设计章节

根据 story 的叙事逻辑设计章节。

默认可采用以下五章结构，但可根据 story 与 venue 要求调整：

```
1. Introduction - 引出问题
2. Related Work - 相关工作
3. Method - 方法
4. Experiments - 实验
5. Conclusion - 结论
```

### Step 4: 填写章节内容

参考 `skills/shared/structure-template.md` 模板，每章填写：
- **叙事内容**: 本章要讲什么故事
- **需求**: 字数范围、图表数量、公式数量

章节与小节规划时遵循“密度优先”原则：
- 不要为了把要点列整齐而拆出过多小节
- 预计只有 1–2 个短段落的内容，默认并入父节，不单独设小节
- 只有当某部分承载独立论证单元、并且内容足以自成展开时，才单独设小节

```markdown
# Chapter 1: Introduction
叙事内容: [本章要讲什么故事]

需求:
  - 字数: 500-800
  - 图表: 1张问题示意图

# Chapter 2: Related Work
...
```

### Step 5: 结合期刊要求

根据 `02-journal-requirements.md` 调整：
- 字数上限
- 章节命名
- 图表限制

### Step 6: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查 structure 是否支撑 story：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 structure 是否支撑 story：

    Story: {story 内容}
    Structure: {structure 内容}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 structure → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...
