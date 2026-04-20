---
name: "04-00-experiment-design"
description: "基于 01-story.md 和 03-00-structure.md 设计实验。用于定义实验方案。"
allowed-tools: Read, Write, mcp__codex__codex
---

# 04-00-experiment-design

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 `01-story.md` + `03-00-structure.md` 设计实验方案。

## 输入

- `01-story.md`
- `03-00-structure.md`
- `03-01-related-work.md`（如已生成，用于确认 baseline / metric 范围）
- `03-02-theory-analysis.md`（如已生成，用于提取理论 prediction、适用边界与 failure case）

## 输出

`04-00-experiments.md` （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 提取 claim 与理论预测

从 story 中提取需要实验支撑的核心论点：
- 主要 claim（我们声称什么）
- 次要 claim（我们验证什么）

如果存在 `03-02-theory-analysis.md`，进一步提取：
- 需要被实验直接验证或削弱的 prediction
- theory 成立 / 不成立的 regime
- 必须覆盖的 comparison、control 与 failure case

如果 claim 表述含糊、证据边界不清、theory prediction 与 story 存在多种实验解读，先向用户确认，不要自行假设。

### Step 2: 设计实验

为每个 claim 设计实验，优先选择支撑 claim 所必需的最小实验集。

如需确认 baseline、指标或实验比较范围，可参考 `03-01-related-work.md`；如需确认理论应如何落到实验对照，可参考 `03-02-theory-analysis.md`；但不要因此默认扩展实验范围。

**可选实验类型**:
- 主实验：验证核心 claim
- 对比实验：与 baseline 比较
- 消融实验：验证各组件贡献
- 鲁棒性实验：不同设置下的稳定性

不要默认把所有实验类型都加上；只保留对当前 story 和 structure 直接必要的实验。

**每类实验包含**:
```markdown
## 实验 N: [名称]

目的: 支撑哪个 claim
对应理论预测: [对应 `03-02` 中的 prediction / 若无则写明 purely empirical]

设置:
- 数据集: [名称]
- Baseline: [对比方法]
- 指标: [评估指标]

预期结果: [描述预期结果]
最小验证标准: [跑通后应观察到的文件、表格或核心指标]
若结果不符合预期，意味着: [削弱了哪个理论判断或经验判断]
```

### Step 3: 用户确认

展示实验方案，等待用户确认或修改。

明确标出：哪些实验是必需的，哪些是可选的，哪些因资源或信息限制暂不纳入。

### Step 4: Codex Review

调用 `mcp__codex__codex` 检查实验设计是否以最小必要实验集支撑 story 中的 claim：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下实验设计是否同时支撑 story 中的 claim，并覆盖 theory analysis 中需要验证的 prediction：

    Story claim: {claim 内容}
    Theory Analysis: {03-02-theory-analysis.md}
    实验设计: {experiments 内容}

    检查要点：
    1. 是否所有关键 claim 都有对应实验？
    2. theory → experiment 的覆盖是否完整？
    3. 评估指标是否合理？
    4. 是否把 purely empirical 现象误写成理论验证？
```
