---
name: "04-paper-experiment"
description: "基于 story.md 和 structure.md 设计实验。用于定义实验方案。"
---

# 04-paper-experiment

基于 story + structure 设计实验方案。

## 输入

- `01-story.md`
- `03-structure.md`

## 输出

`04-experiments.md`

## 工作流

### Step 1: 提取 claim

从 story 中提取需要实验支撑的核心论点：
- 主要 claim（我们声称什么）
- 次要 claim（我们验证什么）

### Step 2: 设计实验

为每个 claim 设计实验：

**实验类型**:
- 主实验：验证核心 claim
- 对比实验：与 baseline 比较
- 消融实验：验证各组件贡献
- 鲁棒性实验：不同设置下的稳定性

**每类实验包含**:
```markdown
## 实验 N: [名称]

目的: 支撑哪个 claim

设置:
- 数据集: [名称]
- Baseline: [对比方法]
- 指标: [评估指标]

预期结果: [描述预期结果]
```

### Step 3: 用户确认

展示实验方案，等待用户确认或修改。

### Step 4: 执行实验

用户确认后执行实验，收集结果。

### Step 5: Codex Review

```markdown
请检查以下实验设计是否支撑 story 中的 claim：

Story claim: {claim 内容}

实验设计: {experiments 内容}

检查要点：
1. 是否所有 claim 都有对应实验？
2. 评估指标是否合理？
3. 是否包含 ablation？
```
