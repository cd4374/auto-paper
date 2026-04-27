---
name: "04-02-experiment-run"
description: "运行实验代码并收集结果。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-02-experiment-run

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

运行实验并收集结果到 `04-02-experiment-results.md`。

## 输入

- `04-01-experiment-code/` （已实现的代码）
- `04-00-experiments.md`

## 输出

- `04-02-experiment-results.md` （实验结果汇总）
- `04-02-experiment-results/` （原始输出、日志、图表）

## 工作流

### Step 1: Pre-review

调用 `mcp__codex__codex` 检查实验运行计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下实验运行计划是否合理：

    实验设计: {04-00-experiments.md 实验列表}
    实现代码: {04-01-experiment-code/README.md 运行说明}
    执行计划: 逐个运行实验，收集结果到 04-02-experiment-results/

    检查：要点见 codex-review-template.md
```

### Step 2: 环境准备

根据 `04-01-experiment-code/README.md` 配置环境：
- 安装依赖
- 准备数据（如需要）
- 验证代码可运行

如果运行前提不清楚、数据来源缺失或资源条件不足，先向用户确认，不要自行假设。

### Step 3: 执行实验

根据 `04-00-experiments.md` 中的实验列表逐个运行，优先使用 `04-01` 中定义的最小运行命令：

- 参考 `04-01-experiment-code/README.md` 的运行命令
- 保存输出到 `04-02-experiment-results/`
- 记录运行日志

询问用户：
- 是否需要并行运行
- 是否有资源限制
- 是否需要中断/续跑支持

不要自行扩大实验范围，不额外添加未在 `04-00-experiments.md` 中定义的实验、扫描或参数搜索。

### Step 4: 收集结果

从输出文件中提取关键数据：
- 数值结果（表格格式）
- 图表文件（复制到 results 目录）
- 关键日志片段

只整理与当前实验目标直接相关的结果；不要顺手改写、清洗或重组无关产物。

**绘图规范（强制）**：
生成图表时必须满足以下要求，否则重绘：

**推荐使用共享样式脚本** `skills/shared/paper_plot_style.py`：
```python
import sys
sys.path.append('skills/shared')
from paper_plot_style import *
```

**绘图规范**：
1. **多子图编号**：每个子图左上角必须有 (a)、(b)、(c)... 编号
2. **字体**：serif 字体（Times New Roman），base size = 10pt
3. **可读性**：无重叠、遮挡，坐标轴标签清晰
4. **分辨率**：≥ 300 DPI（PDF 矢量格式优先）
5. **色条**：必须标注数值范围与单位
6. **尺寸**：单栏图 3.5–6 inches，双栏/通栏图 7–12 inches

### Step 5: 生成结果文档

创建 `04-02-experiment-results.md`：
- 按 `04-00-experiments.md` 的实验结构组织
- 表格/图表展示结果
- 与预期结果对比标注
- 明确标注哪些结果已验证、哪些失败、哪些因条件不足未完成

### Step 6: Post-review（迭代循环，最多 10 轮）

先检查每个实验是否完成了预期运行命令并产生了约定输出，再调用 `mcp__codex__codex` 对比结果与实验设计中的预期：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下实验结果是否达到预期：

    实验设计预期: {预期结果}
    实际结果: {实际结果}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议调整实验运行 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...