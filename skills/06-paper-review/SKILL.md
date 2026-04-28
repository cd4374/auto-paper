---
name: "06-paper-review"
description: "系统审查论文草稿，检查叙事一致性、逻辑完整性、语言质量、格式规范。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex, mcp__kimi-code__kimi_read_media, mcp__MiniMax__understand_image
---

# 06-paper-review

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

系统审查论文草稿，输出结构化修改意见。

## 输入

- `01-story.md` — 叙事逻辑
- `03-00-structure.md` — 文章结构
- `03-02-theory-analysis.md` — 理论分析与表述边界（如已生成）
- `02-journal-requirements.md` — 期刊要求
- `05-template/` — 论文 LaTeX 草稿

## 输出

- `06-paper-review/report.md` — 审查报告
- `06-paper-review/revision-log.md` — 修改日志（仅在本阶段同时修订论文时生成/更新）

## 审查维度

| 维度 | 检查要点 |
|------|----------|
| 叙事一致性 | 论文是否覆盖 story 的核心主张？章节是否服务于故事线？ |
| 逻辑连贯性 | 引言→动机→方法→实验→结论的论证链是否完整？ |
| 语言质量 | 语法、专业术语、学术写作规范、避免口语化 |
| 格式规范 | 期刊格式（页数限制、引用格式、图表位置） |
| 图表质量 | 说明性、分辨率、引用位置、与正文呼应；必要时回溯 `04-03` 图表资产是否充分 |
| 技术正确性 | 公式推导、算法描述、实验设置是否准确；实验分析问题优先回溯 `04-03` |
| 理论一致性 | 理论 claim 是否与 `03-02` 一致，assumptions 是否充分暴露，theory 与 experiment 是否真正形成对照 |
| 分节密度 | 是否存在过碎的小节、只有很短内容却单独成节的情况 |

## 工作流

### Step 1: Pre-review

调用 `mcp__codex__codex` 检查审查准备是否充分：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下论文审查准备是否充分：

    Story: {01-story.md 内容摘要}
    Structure: {03-00-structure.md 章节规划}
    Theory Analysis: {03-02-theory-analysis.md 理论边界}
    Journal Requirements: {02-journal-requirements.md 格式限制}
    LaTeX: {05-template 文件列表}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 2: 自检清单

逐项检查，结果作为内部中间内容最终合并到 Step 5 的报告中：

- [ ] Abstract 是否覆盖 what/why/how/evidence/result 五要素
- [ ] Introduction 的 gap → approach → contributions 逻辑链是否清晰
- [ ] Related Work 是否覆盖相关工作且分类合理
- [ ] Method 的符号定义是否一致、无歧义
- [ ] 理论表述是否与 `03-02-theory-analysis.md` 一致，未把 heuristic 写成已证结论
- [ ] 实验是否验证了所有关键理论预测或明确说明未覆盖部分
- [ ] 结论是否回应了引言的动机
- [ ] 所有 \ref 指向有效 \label
- [ ] 所有 \cite 在 references.bib 中有对应条目
- [ ] 关键 figures 已用图片理解 MCP 做可读性与表达审查
- [ ] 无 TODO/FIXME 残留
- [ ] 没有大量只有 1–2 个短段落却单独成节的小节

### Step 3: 图片理解审查

对论文中的关键 figures 按优先级逐个检查：先用 `mcp__kimi-code__kimi_read_media`，仅当前一工具不可用时降级到 `mcp__MiniMax__understand_image`；重点看：
- panel 布局是否清楚
- 坐标轴、legend、annotation、colorbar、字体是否可读
- 图与 caption、正文引用是否一致
- 图是否准确表达想要支撑的现象，是否存在 reviewer 容易误解的地方

可参考如下优先级调用：

```
mcp__kimi-code__kimi_read_media(
  path: "{figure path}",
  prompt: "Analyze this scientific figure for an academic paper. Describe the panel layout, whether the visualization clearly communicates the intended finding, whether labels, legends, annotations, and color scales are readable, and identify any weaknesses in presentation, scientific clarity, or potential reviewer confusion."
)
# fallback only when unavailable:
mcp__MiniMax__understand_image(
  image_source: "{figure path}",
  prompt: "Analyze this scientific figure for an academic paper. Describe the panel layout, whether the visualization clearly communicates the intended finding, whether labels, legends, annotations, and color scales are readable, and identify any weaknesses in presentation, scientific clarity, or potential reviewer confusion."
)
```

将结论**直接写入 `report.md` 的"图表评估"章节**，格式如下：

```markdown
## 图表评估
| Figure | 检查项通过率 | 结论 | 建议 |
|--------|-------------|------|------|
| fig1.pdf | 10/12 | 可直接使用 | - |
| fig2.pdf | 8/12 | 需小幅修改 | 重绘 legend 位置 |
```

**不要生成独立文件**，所有图片审查结论汇总到 report.md。

### Step 4: Post-review（迭代循环，最多 10 轮）

调用 Codex 逐章节审查：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请审查论文草稿的 {章节名} 部分。

    Story 要求: {该章在 story 中的定位}
    Structure 要求: {该章在 structure 中的叙事内容}
    Theory Analysis: {03-02-theory-analysis.md}
    期刊要求: {02-journal-requirements.md 中的相关要求}

    请检查：是否覆盖 story/structure？逻辑是否严密？语言是否规范？

    若有问题，明确指出并给出修改建议。

    输出格式：
    ## 评分 (1-10)
    ## 主要问题
    ## 具体修改建议
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 report → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...

### Step 5: 生成报告

将 Step 2 自检清单结果（内部中间内容）与 Step 3 图片审查结果汇总到 `06-paper-review/report.md`：

> **说明**: Step 2 的自检清单结果作为内部审查章节合并到 report.md，不作为独立文件输出。

只记录与 story、structure、experiments、results、analysis、venue 要求直接相关的问题；不要顺手扩展为全面重写建议。

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

### Step 6: 修订论文

默认先输出审查结果，不直接改稿；只有在用户明确要求本阶段同时修订时，才根据 report.md 修改 `05-template/` 并更新 `06-paper-review/revision-log.md`。

### Step 7: 终检

确认所有严重问题已解决，方可结束审查流程。
