---
name: "03-paper-structure"
description: "基于 story.md 和 journal-requirements.md 生成 structure.md。用于定义论文章节结构。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 03-paper-structure

基于 story + 期刊要求生成 `03-structure.md`。

## 输入

- `01-story.md`
- `02-journal-requirements.md`

## 输出

`03-structure.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 读取输入

读取 story 和 requirements。

### Step 2: 设计章节

根据 story 的叙事逻辑设计章节：

```
1. Introduction - 引出问题
2. Related Work - 相关工作
3. Method - 方法
4. Experiments - 实验
5. Conclusion - 结论
```

### Step 3: 填写章节内容

参考 `../shared/structure-template.md` 模板，每章填写：
- **叙事内容**: 本章要讲什么故事
- **需求**: 字数范围、图表数量、公式数量

```markdown
# Chapter 1: Introduction
叙事内容: [本章要讲什么故事]

需求:
  - 字数: 500-800
  - 图表: 1张问题示意图

# Chapter 2: Related Work
...
```

### Step 4: 结合期刊要求

根据 `02-journal-requirements.md` 调整：
- 字数上限
- 章节命名
- 图表限制

### Step 5: Codex Review

调用 `mcp__codex__codex` 检查 structure 是否支撑 story：

```
mcp__codex__codex:
  prompt: |
    请检查以下 structure 是否支撑 story：

    Story: {story 内容}
    Structure: {structure 内容}

    检查要点：
    1. 章节是否覆盖 story 的完整叙事？
    2. 各章叙事是否连贯？
    3. 需求（字数/图表）是否合理？
```
