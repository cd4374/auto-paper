---
name: "04-02-experiment-run"
description: "运行实验代码并收集结果。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-02-experiment-run

运行实验并收集结果到 `04-02-experiment-results.md`。

## 输入

- `04-01-experiment-code/` （已实现的代码）
- `04-00-experiments.md`

## 输出

- `04-02-experiment-results.md` （实验结果汇总）
- `04-02-experiment-results/` （原始输出、日志、图表）

## 工作流

### Step 1: 环境准备

根据 `04-01-experiment-code/README.md` 配置环境：
- 安装依赖
- 准备数据（如需要）
- 验证代码可运行

### Step 2: 执行实验

根据 `04-00-experiments.md` 中的实验列表逐个运行：

- 参考 `04-01-experiment-code/README.md` 的运行命令
- 保存输出到 `04-02-experiment-results/`
- 记录运行日志

询问用户：
- 是否需要并行运行
- 是否有资源限制
- 是否需要中断/续跑支持

### Step 3: 收集结果

从输出文件中提取关键数据：
- 数值结果（表格格式）
- 图表文件（复制到 results 目录）
- 关键日志片段

### Step 4: 生成结果文档

创建 `04-02-experiment-results.md`：
- 按 `04-00-experiments.md` 的实验结构组织
- 表格/图表展示结果
- 与预期结果对比标注

### Step 5: Codex Review

调用 `mcp__codex__codex` 对比结果与实验设计中的预期：

```
mcp__codex__codex:
  prompt: |
    请检查以下实验结果是否达到预期：

    实验设计预期: {预期结果}
    实际结果: {实际结果}

    检查要点：
    1. 核心指标是否达标？
    2. 是否有意外发现？
    3. 是否需要补充实验？
```