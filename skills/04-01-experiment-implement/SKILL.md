---
name: "04-01-experiment-implement"
description: "基于实验设计生成可运行的代码实现。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-01-experiment-implement

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 3 — Post-review 迭代轮数上限。

根据 `04-00-experiments.md` 生成实验代码。

## 输入

- `04-00-experiments.md`
- `03-00-structure.md`

## 输出

`04-01-experiment-code/` 目录（根据实验类型动态组织）

## 工作流

### Step 1: 分析实验设计

从 `04-00-experiments.md` 分析：
- 实验类型（AI/ML、数值模拟、物理理论等）
- 实验目的与验证目标
- 需要的资源与依赖
- 输入数据与输出格式

如果实验描述存在歧义、缺失前提或实现路径不唯一，先向用户确认，不要自行假设。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查代码实现计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下代码实现计划是否合理：

    实验设计: {04-00-experiments.md 内容摘要}
    执行计划: 根据实验类型生成最小必要代码，包含核心逻辑+参数入口+输出格式

    检查：要点见 codex-review-template.md
```

### Step 3: 设计代码结构

根据实验类型设计代码结构，但优先复用现有项目结构；只有缺失时才创建最小必要目录与文件。

询问用户：
- 语言偏好（Python、MATLAB、C++等）
- 是否有现有代码框架可复用
- 计算资源需求（本地、集群、云）

不要为一次性实验添加通用框架、额外抽象层或未被要求的可配置性。

### Step 4: 实现代码

生成或补充 `04-01-experiment-code/`，仅包含支撑当前实验所必需的内容：
- 核心实验逻辑
- 最小参数入口
- 必要的数据处理（如需要）
- 与 `04-02` 对接所需的结果输出格式

若已有代码框架，优先做局部增量修改；不要顺手重构、迁移目录或清理无关代码。

每个实验实现前应明确：
- 对应哪个实验目标/claim
- 最小运行命令是什么
- 成功后应产生哪些输出文件或指标

### Step 5: 生成运行说明

在 `04-01-experiment-code/README.md` 中记录：
- 环境配置
- 最小运行命令
- 必要参数说明
- 预期输出文件或指标

### Step 5.5: 可复现性检查（强制）

**不满足的项目必须在进入 04-02 前修复**：

每个实验必须满足：
- [ ] 随机种子已固定（如 `torch.manual_seed(42)`、`np.random.seed(42)`）
- [ ] 有 `requirements.txt` 或 `environment.yml` 记录依赖版本
- [ ] README 中的运行命令可从零复现结果（包含所有必要参数）
- [ ] 代码覆盖了 `04-00-experiments.md` 中该实验的所有设置项（数据集、baseline、指标）

若不满足，**阻塞并修复**，不得跳过进入 04-02。

### Step 6: Post-review（迭代循环，最多 3 轮）

先用最小运行命令验证入口、参数和输出路径是否成立，再调用 `mcp__codex__codex` 检查代码是否支撑实验设计中的目标：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下代码实现是否支撑实验设计中的目标：

    实验设计: {experiments 内容}
    代码结构: {code 结构描述}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改代码 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束