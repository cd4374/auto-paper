---
name: "06-paper-review"
description: "系统审查论文草稿，检查叙事一致性、逻辑完整性、语言质量、格式规范。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 06-paper-review

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

系统审查论文草稿，输出结构化修改意见。

## 输入

- `01-story.md` — 叙事逻辑
- `03-structure.md` — 文章结构
- `02-journal-requirements.md` — 期刊要求
- `05-template/` — 论文 LaTeX 草稿

## 输出

- `06-paper-review/report.md` — 审查报告
- `06-paper-review/revision-log.md` — 修改日志

## 审查维度

| 维度 | 检查要点 |
|------|----------|
| 叙事一致性 | 论文是否覆盖 story 的核心主张？章节是否服务于故事线？ |
| 逻辑连贯性 | 引言→动机→方法→实验→结论的论证链是否完整？ |
| 语言质量 | 语法、专业术语、学术写作规范、避免口语化 |
| 格式规范 | 期刊格式（页数限制、引用格式、图表位置） |
| 图表质量 | 说明性、分辨率、引用位置、与正文呼应 |
| 技术正确性 | 公式推导、算法描述、实验设置是否准确 |

## 工作流

### Step 1: 自检清单

逐项检查，输出 `06-paper-review/self-check.md`：

```bash
# 检查项
- [ ] Abstract 是否覆盖 what/why/how/evidence/result 五要素
- [ ] Introduction 的 gap → approach → contributions 逻辑链是否清晰
- [ ] Related Work 是否覆盖相关工作且分类合理
- [ ] Method 的符号定义是否一致、无歧义
- [ ] 实验是否验证了所有假设
- [ ] 结论是否回应了引言的动机
- [ ] 所有 \ref 指向有效 \label
- [ ] 所有 \cite 在 references.bib 中有对应条目
- [ ] 无 TODO/FIXME 残留
```

### Step 2: Codex 深度审查

调用 Codex 逐章节审查：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请审查论文草稿的 {章节名} 部分。

    Story 要求: {该章在 story 中的定位}
    Structure 要求: {该章在 structure 中的叙事内容}
    期刊要求: {02-journal-requirements.md 中的相关要求}

    请检查：
    1. 是否完整覆盖 story 和 structure 的要求？
    2. 论证逻辑是否严密？是否有漏洞？
    3. 语言是否清晰、符合学术规范？
    4. 与其他章节的衔接是否顺畅？
    5. 是否有技术错误或表述歧义？

    输出格式：
    ## 评分 (1-10)
    ## 主要问题
    ## 具体修改建议
```

### Step 3: 生成报告

汇总所有问题到 `06-paper-review/report.md`：

```markdown
# 论文审查报告

## 审查概览
- 审查时间：
- 目标期刊：
- 整体评分：

## 问题汇总

### 严重问题（必须修改）
1. ...

### 一般问题（建议修改）
1. ...

### 优化建议（可选）
1. ...

## 章节评分
| 章节 | 评分 | 主要问题 |
|------|------|----------|
| Abstract | /10 | ... |
| Introduction | /10 | ... |
| ...

## 图表评估
- 图1: ...
- 表1: ...

## 格式检查
- 页数：X/Y
- 引用格式：✓/✗
- 图表位置：✓/✗
```

### Step 4: 修订论文

根据 report.md 修订 05-template/ 中的内容，更新 `06-paper-review/revision-log.md`。

### Step 5: 终检

确认所有严重问题已解决，方可进入 07-paper-compile。
