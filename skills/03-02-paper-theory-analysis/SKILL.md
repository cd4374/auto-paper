---
name: "03-02-paper-theory-analysis"
description: "基于 story、structure 与文献笔记提炼理论分析，并导出可直接与实验对照的预测。"
allowed-tools: Read, Write, mcp__codex__codex
---

# 03-02-paper-theory-analysis

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 `01-story.md`、`03-structure.md` 与相关文献笔记，生成论文所需的最小理论分析包，明确 assumptions、理论 claim、适用边界与可实验对照的 predictions。

## 输入
- `01-story.md`
- `03-structure.md`
- `03-01-related-work.md`（如已生成）
- `02-journal-requirements.md`（仅在 theory section 的风格或篇幅明显受 venue 影响时参考）

## 输出
- `03-02-theory-analysis.md` （主要语言要用中文，名词等专业用语可以保留英文）
- `03-02-open-questions.md`（仅在关键 assumptions、推导链条或可验证 prediction 存在歧义时生成）

## 工作流

### Step 1: 提取需要理论支撑的 claim
从 `01-story.md` 与 `03-structure.md` 中提取：
- 需要理论支撑的核心 claim
- 只应由实验支撑、不要误写成理论结论的 claim
- method / theory / experiments 章节真正需要解释的机制问题

如果理论目标、论证边界或 claim 强度不清，先向用户确认，不要自行拔高为更强结论。

### Step 2: 建立 assumptions 与分析范围
围绕当前论文主线整理最小必要分析框架：
- 记号、对象、变量与前提
- 关键 assumptions
- 适用 regime / 边界条件
- 明确哪些情况不在当前理论覆盖范围内

不要把分析扩展为脱离当前 story 的泛化综述或纯数学笔记。

### Step 3: 生成理论 claim 与 reasoning sketch
为每个核心理论结论写明：
- `Statement`
- `Type`：theorem / proposition / derivation / heuristic / conjecture
- `Why it matters`
- `Dependency on assumptions`

同时给出最小必要的 reasoning sketch，明确哪些部分是 rigorous argument，哪些只是 heuristic intuition，哪些步骤仍需补强或用户确认。

### Step 4: 导出可与实验对照的 predictions
把理论结论转成后续实验可直接验证或削弱的预测：
- 如果理论成立，实验应观察到什么现象
- 最合适的 metric / observable
- 最合适的 baseline / comparison
- 哪些结果会削弱该理论
- 哪些 regime 应成立，哪些 regime 不应成立

只保留当前论文主线必需的 prediction 集，不默认扩展更多故事线。

### Step 5: 生成 `03-02-theory-analysis.md`
建议结构：

```markdown
# Theory Analysis

## 1. Goal and Scope
- 理论要回答的核心问题
- 需要理论支撑的 story claim
- 当前明确不覆盖的内容

## 2. Assumptions and Setup
- 记号 / 对象 / 前提
- 关键 assumptions
- 适用边界与 regime

## 3. Main Theoretical Claims
### Claim T1
- Statement:
- Type:
- Why it matters:
- Dependency on assumptions:

## 4. Derivation or Reasoning Sketch
- 推导链条
- rigorous / heuristic 的边界
- 仍待补强处

## 5. Experiment-Contrast Predictions
### Prediction P1
- 如果理论成立，实验应观察到:
- 最适合的 metric / observable:
- 最适合的 baseline / comparison:
- 会削弱理论的结果模式:

## 6. Implications for Experiment Design
- 必做实验
- 必要 control / ablation
- 应覆盖的 regime
- 理论不应成立的情况

## 7. Writing Notes
- 可直接写入论文的表述
- 必须加限定词的表述
- 不应写成已证结论的内容

## 8. Open Risks and Limits
- 假设敏感性
- theory–experiment mismatch 风险
- 当前理论证据的边界
```

### Step 6: 处理歧义
如果以下问题会直接影响后续实验设计或论文表述，生成 `03-02-open-questions.md`，不要自行编造：
- 关键 assumption 是否成立
- 某个 claim 应归为严格结论还是 heuristic
- prediction 与可观测量之间是否存在多种合理映射
- theory section 的范围是否需要收缩或拆分

### Step 7: Codex Review
调用 `mcp__codex__codex` 检查理论分析是否足以服务实验设计与论文写作：

```text
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下理论分析是否合理，并且是否足以支持后续实验设计与论文写作：

    Story: {01-story.md}
    Structure: {03-structure.md}
    Related Work: {03-01-related-work.md}
    Theory Analysis: {03-02-theory-analysis.md}

    检查要点：
    1. 是否把 heuristic 误写成了已证明结论？
    2. assumptions 与 claim 的依赖关系是否清楚？
    3. 是否导出了可被实验直接验证或削弱的 prediction？
    4. 是否明确了 theory 的适用边界与不能过度表述的部分？
    5. 文档是否足以供 `04-00`、`04-03` 与 `05` 直接使用？
```

### Step 8: 输出下一步提示
输出：
- `03-02-theory-analysis.md` 已生成
- 若存在歧义，提示先处理 `03-02-open-questions.md`
- 提示下一步：`/04-00-experiment-design`
