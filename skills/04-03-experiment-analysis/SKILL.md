---
name: "04-03-experiment-analysis"
description: "复核实验实现与结果，分析结论边界并生成论文可用图表资产。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__codex__codex, mcp__MiniMax__understand_image
---

# 04-03-experiment-analysis

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 3 — Post-review 迭代轮数上限。

复核实验实现与结果，生成面向论文写作的分析结论和图表资产。

## 输入

- `01-story.md`（必须读取，用于 claim 覆盖度核查）
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

### Step 1: Pre-review

调用 `mcp__codex__codex` 检查实验分析计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下实验分析计划是否合理：

    实验设计: {04-00-experiments.md 实验列表}
    实现代码: {04-01-experiment-code 概览}
    原始结果: {04-02-experiment-results.md 结果摘要}
    执行计划: 复核实现与结果一致性，分析 claim 支撑程度，生成图表资产

    检查：要点见 codex-review-template.md
```

### Step 2: 复核实现与实验设计是否一致

对照 `04-00-experiments.md` 与 `04-01-experiment-code/`，逐项检查：
- 是否覆盖了每个必需实验
- 实现是否对应正确的数据、baseline、指标与输出
- 最小运行命令是否与实际结果来源一致
- 是否存在实现偏移、遗漏模块或与实验设计不一致的默认设置

如果实现路径不清楚、结果来源无法回溯，先向用户确认，不要自行假设。

### Step 3: 复核结果是否完整且可信

对照 `04-02-experiment-results.md` 与 `04-02-experiment-results/`，检查：
- 是否所有必需实验都已完成
- 是否产生了 `04-00` 中约定的关键输出
- 是否存在明显异常值、缺失项、日志报错或结果与描述不一致
- baseline 比较是否公平，指标解释是否成立

不要把“结果不理想”误判为“实验失败”；重点检查结果是否足以支撑或反驳 claim。

### Step 4: 分析结果与 claim / theory prediction 的对应关系

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

### Step 5: 生成图表资产

整理图表到 `04-03-paper-assets/`，要求：
- 图表命名清晰，能回溯到实验名称或 claim
- 只保留论文写作需要的最小必要资产
- 若需要重绘，优先复用现有结果文件，不重跑无关实验

### Step 6: 图片审查

用 `mcp__MiniMax__understand_image` 审查关键 figures，检查：
- panel 布局是否清楚
- 曲线、热图、坐标轴、legend、colorbar、annotation 是否可读
- 图是否真正表达了当前 claim 对应的现象
- 是否存在可能引发 reviewer 困惑的展示问题、歧义或视觉误导

结论写入 `04-03-experiment-analysis.md`，明确哪些图可直接进入论文、哪些需要重绘。

### Step 7: 叙事→实验覆盖度检查

**这是 P0 强制门控，不得跳过。**

读取 `01-story.md`，对照实验结果，检查：

```
## Story Claim Coverage（必须填写）
| Story Claim（来自01-story.md）| 支撑实验 | 支撑程度 | 论文处理方式 |
|---|---|---|---|
| Claim C1: ... | 实验N | 支撑/部分支撑/不支持/无实验 | 直接引用/加限定词/移至future work |
```

**判定标准**：
- **支撑**：核心指标超过 baseline，统计显著
- **部分支撑**：趋势正确但不显著，或只在部分 regime 成立
- **不支持**：核心指标低于或等于 baseline
- **无实验**：该 claim 没有任何对应实验

**系统不支持处理**（≥2 个核心 claim 为"不支持"或"无实验"）：
1. 必须生成 `04-03-story-gap.md`，列出所有覆盖缺口
2. **阻塞进入 05-paper-write**
3. 向用户说明，由用户选择：
   - (a) 修改 story/claim（回退到 `/01-paper-init` 或 `/03-02-paper-theory-analysis`）
   - (b) 补充/修改实验（回退到 `/04-00-experiment-design`）
   - (c) 放弃该项目

### Step 8: 生成分析文档

创建 `04-03-experiment-analysis.md`，结构如下：

```markdown
# Experiment Analysis

## Summary
- 已支撑的核心 claim:
- 部分支撑的 claim:
- 当前未支撑的 claim:
- 是否建议补实验:

## Story Claim Coverage（必填）
| Story Claim | 支撑实验 | 支撑程度 | 论文处理方式 |
|---|---|---|---|
| ... | ... | ... | ... |

**⚠️ 覆盖缺口声明**（若有未支撑的 claim）：
- 已在正文中加限定词的 claim:
- 移至 future work 的 claim:
- [若无缺口] 所有核心 claim 均有实验支撑

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

## Figure Review
- 图1: 审查结论 / 是否建议重绘 / 是否可直接用于论文

## Writing Notes
- 正文应强调:
- 正文应避免过度解读:
```

明确标注：哪些结论可进入 `05-paper-write`，哪些仅作内部判断。

### Step 9: Post-review（迭代循环，最多 3 轮）

先检查分析文档、图表资产、图片审查结论与原始结果是否可回溯，再调用 `mcp__codex__codex` 检查分析是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下实验分析是否合理：

    实验设计: {04-00-experiments.md}
    Theory Analysis: {03-02-theory-analysis.md}
    实现概览: {04-01-experiment-code 概览}
    原始结果: {04-02-experiment-results.md + 关键产物}
    分析文档: {04-03-experiment-analysis.md}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 experiment-analysis → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束
