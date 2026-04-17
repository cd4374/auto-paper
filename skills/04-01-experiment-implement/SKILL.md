---
name: "04-01-experiment-implement"
description: "基于实验设计生成可运行的代码实现。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-01-experiment-implement

根据 `04-00-experiments.md` 生成实验代码。

## 输入

- `04-00-experiments.md`
- `03-structure.md`

## 输出

`04-01-experiment-code/` 目录（根据实验类型动态组织）

## 工作流

### Step 1: 分析实验设计

从 `04-00-experiments.md` 分析：
- 实验类型（AI/ML、数值模拟、物理理论等）
- 实验目的与验证目标
- 需要的资源与依赖
- 输入数据与输出格式

### Step 2: 设计代码结构

根据实验类型动态设计目录结构，不预设固定模板。

询问用户：
- 语言偏好（Python、MATLAB、C++等）
- 是否有现有代码框架可复用
- 计算资源需求（本地、集群、云）

### Step 3: 实现代码

生成 `04-01-experiment-code/`，包含：
- 核心实验逻辑
- 配置/参数管理
- 数据处理（如需要）
- 结果输出格式

### Step 4: 生成运行说明

在 `04-01-experiment-code/README.md` 中记录：
- 环境配置
- 运行命令
- 参数说明

### Step 5: Codex Review

调用 `mcp__codex__codex` 检查代码是否支撑实验设计中的目标：

```
mcp__codex__codex:
  prompt: |
    请检查以下代码实现是否支撑实验设计中的目标：

    实验设计: {experiments 内容}
    代码结构: {code 结构描述}

    检查要点：
    1. 代码是否覆盖所有实验？
    2. 输出格式是否符合预期？
    3. 是否有缺失的关键模块？
```