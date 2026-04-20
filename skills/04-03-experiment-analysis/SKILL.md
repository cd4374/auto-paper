---
name: "04-03-experiment-analysis"
description: "复核实验实现与结果，分析结论边界并生成论文可用图表资产。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__codex__codex, mcp__MiniMax__understand_image
---

# 04-03-experiment-analysis

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

复核实验实现与结果，生成面向论文写作的分析结论和图表资产。

## 输入

- `04-00-experiments.md`
- `04-01-experiment-code/`
- `04-02-experiment-results.md`
- `04-02-experiment-results/`
- `03-00-structure.md`
- `03-02-theory-analysis.md`（如已生成，用于 theory vs experiment 对照）

## 输出

- `04-03-experiment-analysis.md` （主要语言要用中文，名词等专业用语可以保留英文）
- `04-03-paper-assets/` （论文可直接引用的图、表、整理后的中间文件）

## 工作流

### Step 1: 复核实现与实验设计是否一致

对照 `04-00-experiments.md` 与 `04-01-experiment-code/`，逐项检查：
- 是否覆盖了每个必需实验
- 实现是否对应正确的数据、baseline、指标与输出
- 最小运行命令是否与实际结果来源一致
- 是否存在实现偏移、遗漏模块或与实验设计不一致的默认设置

如果实现路径不清楚、结果来源无法回溯，先向用户确认，不要自行假设。

### Step 2: 复核结果是否完整且可信

对照 `04-02-experiment-results.md` 与 `04-02-experiment-results/`，检查：
- 是否所有必需实验都已完成
- 是否产生了 `04-00` 中约定的关键输出
- 是否存在明显异常值、缺失项、日志报错或结果与描述不一致
- baseline 比较是否公平，指标解释是否成立

不要把“结果不理想”误判为“实验失败”；重点检查结果是否足以支撑或反驳 claim。

### Step 3: 分析结果与 claim / theory prediction 的对应关系

围绕 `04-00-experiments.md` 中的 claim，提炼：
- 哪些 claim 已被结果直接支撑
- 哪些 claim 仅被部分支撑
- 哪些 claim 当前证据不足或被结果削弱
- 哪些现象值得在论文中解释，哪些只是噪声不应过度解读

如果存在 `03-02-theory-analysis.md`，还要对照其中的 prediction：
- 哪些 theory prediction 已被结果支撑
- 哪些 prediction 仅被部分支撑
- 哪些 prediction 被结果削弱或尚未测试
- theory–experiment mismatch 更可能来自理论边界、实现偏移还是证据不足

只分析当前 story 和 structure 直接需要的结论；不要默认扩展新故事线或补做未批准实验。

### Step 4: 生成论文可用图表资产

将可直接进入论文的图表与表格统一整理到 `04-03-paper-assets/`：
- 主结果表
- ablation/robustness 表（如当前实验需要）
- 论文可直接引用的 figures
- 图表对应的简短说明或数据来源记录

要求：
- 图表命名清晰，能回溯到实验名称或 claim
- 只保留论文写作需要的最小必要资产
- 若需要重绘，优先复用现有结果文件，不重跑无关实验

### Step 5: 图表可读性与表达 review

对准备进入论文的关键 figures，使用 `mcp__MiniMax__understand_image` 做图片理解审查，至少检查：
- panel 布局是否清楚
- 曲线、热图、坐标轴、legend、colorbar、annotation 是否可读
- 图是否真正表达了当前 claim 对应的现象
- 是否存在可能引发 reviewer 困惑的展示问题、歧义或视觉误导

可参考如下提示词：

```
mcp__MiniMax__understand_image(
  image_source: "{figure path}",
  prompt: "Analyze this scientific figure for an academic paper. Describe the panel layout, whether the visualization clearly communicates the intended finding, whether labels, legends, annotations, and color scales are readable, and identify any weaknesses in presentation, scientific clarity, or potential reviewer confusion."
)
```

将图片审查结论写入 `04-03-experiment-analysis.md`，并明确：
- 哪些图可以直接进入论文
- 哪些图需要重绘、裁剪、放大字体或补充 caption 信息
- 哪些图虽然结果有效，但当前呈现方式不适合直接投稿

### Step 6: 生成分析文档

创建 `04-03-experiment-analysis.md`，建议结构：

```markdown
# Experiment Analysis

## Summary
- 已支撑的核心 claim:
- 部分支撑的 claim:
- 当前未支撑的 claim:
- 是否建议补实验:

## Experiment-by-Experiment Review

### 实验 1: ...
- 实现复核:
- 结果复核:
- 主要发现:
- 对 claim 的支撑程度:
- 对理论预测的支撑程度:
- 可写入论文的图表/表格:
- 图片审查结论:
- 风险与限制:

## Theory vs Experiment
- Prediction P1: 支撑 / 部分支撑 / 削弱 / 未测试
- Prediction P2: ...

## Figure Review
- 图1: 图片审查结论 / 是否建议重绘 / 是否可直接用于论文
- 图2: ...

## Writing Notes
- 正文应强调:
- 正文应避免过度解读:
- 需要回到 `04-00` 或 `04-01` 修正的问题:
```

明确标注：哪些结论可以进入 `05-paper-write`，哪些只能作为内部判断，不能直接写进论文。

### Step 7: Codex Review

先检查分析文档、图表资产、图片审查结论与原始结果是否可回溯，再调用 `mcp__codex__codex` 检查分析是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下实验分析是否合理：

    实验设计: {04-00-experiments.md}
    Theory Analysis: {03-02-theory-analysis.md}
    实现概览: {04-01-experiment-code 概览}
    原始结果: {04-02-experiment-results.md + 关键产物}
    分析文档: {04-03-experiment-analysis.md}

    检查要点：
    1. 是否错误地把未验证的现象或理论写成结论？
    2. 是否漏掉了对关键异常、限制或 theory–experiment mismatch 的说明？
    3. claim / theory prediction 与证据的对应关系是否清楚？
    4. 图表资产是否足以支持论文写作？
    5. 是否充分吸收了图片理解 review 暴露的可读性与表达问题？
```
