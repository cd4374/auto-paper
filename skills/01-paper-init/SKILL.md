---
name: "01-paper-init"
description: "从研究想法生成 story.md。用于开始新论文项目时定义叙事逻辑。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 01-paper-init

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

从研究想法生成 `01-story.md`。

## 输入

用户描述的研究想法

## 输出

`01-story.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 澄清研究想法

追问以下问题：
- 研究的核心问题是什么？
- 为什么要解决这个问题？（动机/应用价值）
- 初步的方法思路是什么？
- 预期的贡献是什么？

### Step 2: 生成 story.md

基于 `../shared/story-template.md` 模板生成 `01-story.md`：

```markdown
# 是什么
[研究的问题是什么？]

# 为什么
[为什么要研究这个问题？动机/价值/应用场景]

# 怎么做
[解决问题的思路是什么？核心方法概述]
```

### Step 3: Codex Review

调用 `mcp__codex__codex` 检查叙事逻辑：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下 story 的叙事逻辑：

    {story 内容}

    检查要点：
    1. 三问（是什么/为什么/怎么做）是否都回答清楚？
    2. 逻辑链条是否自洽？
    3. 是否有明显的逻辑漏洞？
```

### Step 4: 输出确认

输出：
- `01-story.md` 已生成
- 总结核心论点
- 提示下一步：`/02-paper-journal`
