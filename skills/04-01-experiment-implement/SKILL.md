---
name: "04-01-experiment-implement"
description: "基于实验设计生成 Jupyter Notebook 实现，所有操作代码（数据、训练、评估、可视化）集中在 notebook 中。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-01-experiment-implement

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

根据 `04-00-experiments.md` 生成实验代码。**一个实验目标对应一个 Jupyter Notebook（`.ipynb`）**，禁止将多个实验目标挤入同一个 notebook。

Notebook 命名规则：`experiment_NN_xxx.ipynb`，其中 `NN` 对应 `04-00-experiments.md` 中的实验编号。

## Cell 语言规范（强制）

- **Markdown cell**：使用中文撰写，包含实验说明、步骤描述、结果讨论等叙述性内容
- **Code cell**：使用英文编写，包含所有 Python 代码、注释、变量名等

典型的 notebook 结构及与上游文件的对应关系：
```
引用上游                   Notebook 内容
─────────────────────────────────────────────────────
                         [code cell - 英文] # Verify conda env scf-paper
04-00-experiments.md     [md cell - 中文]   ## 实验 1：XXX 对比实验
01-story.md              [md cell - 中文]   验证 claim：XXX 在 YYY 条件下优于 baseline
04-00-experiments.md     [md cell - 中文]   ### 1. 数据生成
                         [code cell - 英文] # Generate synthetic data
                         [md cell - 中文]   ### 2. 数据装载与预处理
                         [code cell - 英文] # Load, normalize, split
                         [md cell - 中文]   ### 3. 模型训练
                         [code cell - 英文] # Define model, training loop
                         [md cell - 中文]   ### 4. 评估
                         [code cell - 英文] # Evaluate, compute metrics
03-00-structure.md       [md cell - 中文]   ### 5. 可视化
(figure plan)            [md cell - 中文]   此图用于论文第 X 节，展示...
                         [code cell - 英文] # Plot (save PDF + display inline)
01-story.md              [md cell - 中文]   ### 6. 结果讨论
(claim check)            [md cell - 中文]   上述结果支持/不支持 claim X，因为...
```

每个 md cell 在引用上游文件时，应明确标注来源（如 "对应 04-00 实验 1 的设置 A"、"支撑 01-story 中的 claim 2"）。

## 数据规范（强制）

**绘图数据必须从外部文件读取，禁止在 notebook 中硬编码数据**：

```python
# ✅ 正确：从文件读取
import json
with open('outputs/results.json') as f:
    data = json.load(f)

# ❌ 错误：硬编码
values = [82.3, 85.1, 86.7, 89.2]
```

- 实验的中间结果保存为 JSON/CSV 到 `outputs/`，绘图 cell 从 `outputs/` 读取
- 确保 notebook 从头重跑时数据会被重新生成，图也会随之更新

## 绘图规范（强制）

**每个绘图 cell 必须同时保存 PDF 并内联显示图片**：

```python
# Plot and save
fig, ax = plt.subplots()
ax.plot(x, y)
save_fig_and_show(fig, 'fig_name')  # 保存 PDF + 在 cell 中显示
```

- 使用 `shared/paper_plot_style.py` 中的 `save_fig_and_show()` 函数
- 图片格式仅限 PDF（矢量）
- 图片输出到 `figures/` 目录

## 输入

- `04-00-experiments.md`
- `03-00-structure.md`

## 输出

`04-01-experiment-code/` 目录。Notebook 是唯一可执行载体，**一个实验目标一个 notebook**。

```bash
04-01-experiment-code/
├── README.md                 # 环境配置、notebook 与实验编号对应表
├── requirements.txt          # 依赖版本
├── experiment_01_xxx.ipynb   # 对应 04-00 实验 1
├── experiment_02_xxx.ipynb   # 对应 04-00 实验 2
├── configs/                  # 实验配置（YAML/JSON）
├── data/                     # 数据文件（可选，仅当数据较大不便内嵌时）
├── figures/                  # 生成的 PDF 图表
└── outputs/                  # 临时输出（.gitignore）
```

## 工作流

### Step 1: 分析实验设计

从 `04-00-experiments.md` 提取**实验编号列表**（如实验 1、实验 2...），每个编号对应一个 notebook。然后逐实验分析：
- 实验类型（AI/ML、数值模拟、物理理论等）
- 实验目的与验证目标
- 对应的 `01-story.md` claim
- 需要的资源与依赖
- 输入数据与输出格式
- 在 `03-00-structure.md` 中对应的 figure plan

如果实验描述存在歧义、缺失前提或实现路径不唯一，先向用户确认，不要自行假设。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查代码实现计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下代码实现计划是否合理：

    实验设计: {04-00-experiments.md 内容摘要}
    执行计划: 根据实验类型生成最小必要代码，包含核心逻辑+参数入口+输出格式

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 3: 设计代码结构

根据实验类型设计代码结构，但优先复用现有项目结构；只有缺失时才创建最小必要目录与文件。

询问用户：
- 语言偏好（Python、MATLAB、C++等）
- 是否有现有代码框架可复用
- 计算资源需求（本地、集群、云）

不要为一次性实验添加通用框架、额外抽象层或未被要求的可配置性。

### Step 4: 实现代码

根据 `04-00-experiments.md` 的实验编号，**逐实验生成对应的 notebook**。一个实验目标 → 一个 `.ipynb` 文件，禁止将多个实验合并到一个 notebook 中。

**Notebook 是唯一的可执行载体**，所有操作代码——数据生成、数据装载、预处理、模型定义、训练循环、评估、可视化——全部内嵌在 notebook 中。

Notebook 必须遵循 **Cell 语言规范**（见顶部）：
- Markdown cell → 中文
- Code cell → 英文

每个 notebook 按完整生命周期组织，并在 md cell 中标注对应的上游文件来源：

| 步骤 | Cell 类型 | 内容 | 上游来源 |
|------|-----------|------|----------|
| 1. 实验目标 | md（中文） | 对应哪个实验、验证哪个 claim | `04-00-experiments.md` |
| 2. story 上下文 | md（中文） | 该实验在论文叙事中的角色 | `01-story.md` |
| 3. 数据生成/装载 | code（英文） | 合成数据或加载外部数据集 | `04-00` 实验设置 |
| 4. 预处理 | code（英文） | 归一化、划分 train/val/test | `04-00` 实验设置 |
| 5. 模型/算法定义 | code（英文） | 模型结构或算法逻辑 | `04-00` 实验设置 |
| 6. 训练/运行 | code（英文） | 训练循环或主计算 | `04-00` 实验设置 |
| 7. 评估 | code（英文） | 在测试集上计算指标 | `04-00` 评估指标 |
| 8. 可视化 | code（英文） | `save_fig_and_show()` 生成 PDF 图表 | `03-00-structure.md` figure plan |
| 9. 结果讨论 | md（中文） | 结果是否支撑 claim，讨论边界条件 | `01-story.md` claims |

**不额外创建独立脚本**。即使某个操作用到通用逻辑（如自定义 loss、数据生成器），也应在 notebook 的 code cell 中定义，而非放在外部 `.py` 文件中 import。唯一允许的外部依赖是 `skills/shared/paper_plot_style.py`。

若已有 notebook，优先做局部增量修改；不要顺手重构、迁移目录或清理无关代码。

每个实验实现前应明确：
- 对应 `04-00-experiments.md` 中哪个实验编号
- 对应 `01-story.md` 中哪个 claim
- notebook 文件名（`experiment_NN_xxx.ipynb`）
- 成功后应产生哪些输出（PDF 图表路径、指标值等）

**绘图代码规范（强制）**：若实验需要生成图表，必须在 notebook code cell 中使用以下模式：

```python
import sys
sys.path.append('skills/shared')
from paper_plot_style import *

# 创建图表
fig, ax = plt.subplots()
# ... 绘图代码 ...

# 添加子图编号
add_subfigure_label(ax, 'a')  # 添加 (a) 标签

# 保存 PDF + 在 notebook cell 中显示图片
save_fig_and_show(fig, 'fig_name')
```

`save_fig_and_show(fig, name)` 行为：
1. 保存 `figures/{name}.pdf`（矢量 PDF）
2. 在 notebook cell 输出区内联显示图片

**图表类型决策树**：

| 数据模式 | 推荐类型 | 宽度 |
|----------|----------|------|
| X=时间/steps, Y=指标 | Line plot（折线图） | 0.48\textwidth |
| X=方法/类别, Y=数值 | Bar chart（柱状图） | 0.48\textwidth |
| X=连续, Y=连续 | Scatter plot（散点图） | 0.48\textwidth |
| 矩阵/网格值 | Heatmap（热图） | 0.48\textwidth |
| 分布比较 | Box/violin plot | 0.48\textwidth |
| 多数据集/多方法 | Multi-panel（多子图） | 0.95\textwidth |

**绘图规范**：

1. **多子图编号**：使用 `add_subfigure_label(ax, 'a')` 添加 (a)、(b)、(c)... 编号
2. **字体**：serif 字体（Times New Roman），base size = 10pt
3. **分辨率**：300 DPI（用于导出一致性）
4. **布局**：使用 `fig.tight_layout()` 避免重叠
5. **色条**：必须标注数值范围与单位
6. **导出 + 内联显示**：使用 `save_fig_and_show(fig, name)` 同时保存 PDF 并在 cell 中显示图片
7. **格式**：仅 PDF（矢量），输出到 `figures/` 目录

### Step 5: 生成运行说明

在 `04-01-experiment-code/README.md` 中记录：
- **Python 环境**：conda env `scf-paper`（强制），若不存在则停止
- 环境配置命令：`conda activate scf-paper && pip install -r requirements.txt`
- 最小运行命令：`jupyter nbconvert --to notebook --execute experiment_NN_xxx.ipynb`

每个 notebook 的第一个 code cell 必须包含环境检查：
```python
# Verify conda environment
import sys, subprocess
result = subprocess.run(['conda', 'env', 'list'], capture_output=True, text=True)
if 'scf-paper' not in result.stdout:
    raise RuntimeError(
        'conda env scf-paper not found. '
        'Create it: conda create -n scf-paper python=3.10'
    )
print(f'Python: {sys.version} | conda env: scf-paper')
```
- 必要参数说明
- 预期输出文件或指标

### Step 5.5: 可复现性检查（强制）

**不满足的项目必须在进入 04-02 前修复**：

每个实验必须满足：
- [ ] `04-00-experiments.md` 中的每个实验目标都有对应的 notebook，无遗漏无合并
- [ ] 每个 notebook 的 md cell 标注了上游来源（`04-00` 实验编号、`01-story` claim、`03-00` figure plan）
- [ ] conda env `scf-paper` 已确认存在，notebook 第一个 cell 包含环境检查
- [ ] 有 `requirements.txt` 记录依赖版本
- [ ] 随机种子已固定（如 `torch.manual_seed(42)`、`np.random.seed(42)`）
- [ ] README 中记录了 notebook 与实验编号的对应表及执行顺序
- [ ] notebook 从头到尾可顺序执行复现结果（`Cell → Run All`）

若不满足，**阻塞并修复**，不得跳过进入 04-02。

### Step 6: Post-review（迭代循环，最多 10 轮）

先用最小运行命令验证入口、参数和输出路径是否成立，再调用 `mcp__codex__codex` 检查代码是否支撑实验设计中的目标：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下代码实现是否支撑实验设计中的目标：

    实验设计: {experiments 内容}
    代码结构: {code 结构描述}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改代码 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...