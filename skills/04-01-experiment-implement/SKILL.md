---
name: "04-01-experiment-implement"
description: "基于实验设计生成实验代码。数据生成/训练/评估逻辑放在独立 .py 脚本，Jupyter Notebook 负责调用脚本并绘图。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 04-01-experiment-implement

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

根据 `04-00-experiments.md` 生成实验代码。**一个 `Fig.x` / `Table.x` 对应一个独立文件**，禁止将多个图表资产的生成逻辑挤入同一个文件。

**图表资产分为两类**：
1. **数据图/表**（类型为 `[数据图]` 或 `[数据表]`）：对应一个 Jupyter Notebook（`.ipynb`），**不包含内嵌的数据生成/训练代码**，而是调用独立 `.py` 脚本生成数据，再基于输出数据绘图/制表
2. **示意图**（类型为 `[示意图]`）：不需要运行代码实验，对应一个 Markdown 文件（`.md`），包含生成该图的**详细 prompt**（用于调用 LLM / GPT Image 2 等模型绘制）

两类资产使用不同格式：数据图/表用 `.ipynb`，示意图用 `.md`。

**数据生成脚本规范（强制）**：
- 每个数据类 `Fig.x` / `Table.x` 对应一个独立的 `.py` 数据生成脚本，放在 `scripts/` 目录下
- 脚本命名：`fig_NN_xxx_data.py` 或 `tab_NN_xxx_data.py`，与对应 notebook 一一对应
- 脚本职责：完成该图/表所需的全部数据生成、训练、评估、指标计算，将中间结果保存到 `outputs/`
- 脚本必须是**可直接运行的 Python 文件**（`python scripts/fig_NN_xxx_data.py`），不依赖 notebook 上下文
- notebook 中通过 `subprocess.run([sys.executable, 'scripts/fig_NN_xxx_data.py'])` 调用脚本生成数据，再读取 `outputs/` 中的结果进行绘图

**文件命名规则**：
- 数据图/表：`fig_NN_xxx.ipynb` 或 `tab_NN_xxx.ipynb`
- 示意图：`fig_NN_xxx.md`（直接用 markdown，不需要 `.ipynb`）

其中 `NN` 对应 `03-00-structure.md` 中的图表资产编号（如 `fig_01_problem_setup.ipynb` / `fig_01_problem_setup.md` 对应 Fig.1）。若同一实验生成多个图/表，必须拆分为多个文件。

## 文档语言规范（强制）

- **叙述性内容**（markdown / notebook 中的 md cell）：使用中文撰写，包含实验说明、步骤描述、结果讨论等
- **代码**（notebook 中的 code cell / `.py` 脚本）：使用英文编写，包含所有 Python 代码、注释、变量名等

**数据图/表 notebook 典型结构**：
```
引用上游                   Notebook 内容
─────────────────────────────────────────────────────
                         [code cell - 英文] # Verify conda env scf-paper
04-00-experiments.md     [md cell - 中文]   ## 实验 1：XXX 对比实验
01-story.md              [md cell - 中文]   验证 claim：XXX 在 YYY 条件下优于 baseline
04-00-experiments.md     [md cell - 中文]   ### 1. 数据生成
                         [md cell - 中文]   运行数据生成脚本：
                         [code cell - 英文] import subprocess, sys
                         [code cell - 英文] subprocess.run([sys.executable, 'scripts/fig_NN_xxx_data.py'], check=True)
                         [md cell - 中文]   ### 2. 数据装载
                         [code cell - 英文] # Load generated data from outputs/
                         [md cell - 中文]   ### 3. 可视化
03-00-structure.md       [md cell - 中文]   此图对应 `03-00-structure.md` 中的 Fig.x，用于论文第 X 节，展示...
(figure plan)            [code cell - 英文] # Plot (save PDF + display inline)
01-story.md              [md cell - 中文]   ### 4. 结果讨论
(claim check)            [md cell - 中文]   上述结果支持/不支持 claim X，因为...
```

**示意图 markdown 文件典型结构**（`fig_NN_xxx.md`）：
```
## Fig.x: [图名称]
类型: [示意图]
用途: 用于论文第 X 节，展示...
叙事功能: 该图要支撑 claim X，帮助读者理解...

### 视觉要求
- 尺寸: 单栏/双栏
- 风格: 学术简洁 / 拟物 / 扁平
- 配色: 与论文一致（避免彩虹色）
- 字体: Times New Roman 或无衬线
- 必须包含的元素: A、B、C...
- 布局: 从上到下 / 从左到右...

### 生成 Prompt
```
[详细的英文或中文 prompt，可直接复制到 LLM 图像生成工具中使用]
```

### 生成参数建议
- 推荐工具: GPT Image 2 / DALL-E 3 / Midjourney / Stable Diffusion
- 参数: aspect ratio、style reference 等

### 输出要求
- 输出格式: PNG/SVG/PDF（优先矢量或可无损放大）
- 保存路径: `figures/fig_name.pdf`
- 生成后检查: 字体可读、元素完整、与描述一致
```

每个叙述性段落在引用上游文件时，应明确标注来源（如 "对应 04-00 实验 1 的设置 A"、"支撑 01-story 中的 claim 2"）。

## 数据规范（强制）

**数据生成与绘图分离**：
- 数据生成逻辑必须放在独立的 `.py` 脚本（`scripts/fig_NN_xxx_data.py`）中，禁止在 notebook 的 code cell 内嵌长段训练/计算逻辑
- notebook 只负责调用脚本、读取 `outputs/` 中的结果、绘图/制表

**绘图数据必须从 `outputs/` 读取，禁止在 notebook 中硬编码数据**：

```python
# ✅ 正确：运行脚本 + 从文件读取
import subprocess, sys
subprocess.run([sys.executable, 'scripts/fig_01_xxx_data.py'], check=True)

import json
with open('outputs/results.json') as f:
    data = json.load(f)

# ❌ 错误：硬编码
values = [82.3, 85.1, 86.7, 89.2]
```

- 脚本生成的中间结果保存为 JSON/CSV 到 `outputs/`，绘图 cell 从 `outputs/` 读取
- 确保 notebook 从头重跑时先调用脚本重新生成数据，图也会随之更新

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

`04-01-experiment-code/` 目录。数据图/表用 notebook（可执行），示意图用 markdown（无需执行）。

```bash
04-01-experiment-code/
├── README.md                 # 环境配置、notebook / 脚本 / 图表资产对应表
├── requirements.txt          # 依赖版本
├── fig_01_xxx.ipynb          # [数据图] 对应 03-00 Fig.1（调用脚本 + 绘图）
├── fig_02_xxx.md             # [示意图] 对应 03-00 Fig.2（prompt 文档，无需执行）
├── tab_01_xxx.ipynb          # [数据表] 对应 03-00 Table.1
├── scripts/                  # 数据生成脚本（仅数据图/表需要，一个对应一个 .py）
│   ├── fig_01_xxx_data.py    # 生成 Fig.1 所需数据
│   └── tab_01_xxx_data.py
├── configs/                  # 实验配置（YAML/JSON）
├── data/                     # 数据文件（可选，仅当数据较大不便内嵌时）
├── figures/                  # 生成的 PDF 图表（与 Fig.x 一一对应）
└── outputs/                  # 脚本输出（JSON/CSV）（.gitignore）
```

## 工作流

### Step 1: 分析实验设计

从 `04-00-experiments.md` 提取**实验编号列表**，并从 `03-00-structure.md` 提取**图表资产列表**（`Fig.x` / `Table.x`）。每个图表资产对应一个文件（数据类用 `.ipynb`，示意类用 `.md`）。然后逐资产分析：
- 实验类型（AI/ML、数值模拟、物理理论等）
- 实验目的与验证目标
- 对应的 `01-story.md` claim
- 需要的资源与依赖
- 输入数据与输出格式
- 在 `03-00-structure.md` 中对应的 `Fig.x` / `Table.x` 编号与叙事功能

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

根据 `04-00-experiments.md` 的实验编号与 `03-00-structure.md` 的图表资产，**逐资产生成对应的文件**。一个 `Fig.x` / `Table.x` → 一个 `.ipynb`（数据类）或 `.md`（示意类），禁止将多个图表资产合并到一个文件中。

**Notebook 是可视化和分析的载体，数据生成逻辑必须拆分到独立 `.py` 脚本**。每个 `Fig.x` / `Table.x` 的完整实验链路为：

数据类图表的完整实验链路：
```
scripts/fig_NN_xxx_data.py  →  outputs/results.json  →  fig_NN_xxx.ipynb  →  figures/fig_NN_xxx.pdf
         (数据生成/训练/评估)        (中间结果)              (读取 + 绘图)            (最终图表)
```

示意类图表的链路（无代码执行）：
```
fig_NN_xxx.md  →  (LLM 图像生成)  →  figures/fig_NN_xxx.pdf
   (prompt 文档)                        (最终图表)
```

数据类 notebook 必须遵循 **文档语言规范**（见顶部）：
- Markdown cell → 中文
- Code cell → 英文

每个数据类 notebook 按以下结构组织，并在 md cell 中标注对应的上游文件来源：

| 步骤 | Cell 类型 | 内容 | 上游来源 |
|------|-----------|------|----------|
| 1. 实验目标 | md（中文） | 对应哪个实验、验证哪个 claim | `04-00-experiments.md` |
| 2. story 上下文 | md（中文） | 该实验在论文叙事中的角色 | `01-story.md` |
| 3. 调用数据生成脚本 | code（英文） | `subprocess.run([sys.executable, 'scripts/fig_NN_xxx_data.py'])` | `04-00` 实验设置 |
| 4. 数据装载 | code（英文） | 从 `outputs/` 读取脚本生成的 JSON/CSV | `04-00` 实验设置 |
| 5. 可视化 | code（英文） | `save_fig_and_show()` 生成对应 `Fig.x` 的 PDF 图表 | `03-00-structure.md` 图表资产 |
| 6. 结果讨论 | md（中文） | 结果是否支撑 claim，讨论边界条件 | `01-story.md` claims |

**数据生成脚本规范**：
- 脚本放在 `scripts/` 目录，命名与对应 notebook 一致（后缀 `_data.py`）
- 脚本完成该图/表所需的全部数据生成、训练、评估、指标计算，将结果保存到 `outputs/`
- 脚本必须是可直接运行的 Python 文件（不依赖 notebook 上下文）
- 通用工具函数（如自定义 loss）可在 `scripts/` 内的独立模块中定义，由多个脚本复用
- 唯一允许 notebook 直接 import 的外部依赖是 `skills/shared/paper_plot_style.py`

若已有 notebook，优先做局部增量修改；不要顺手重构、迁移目录或清理无关代码。

每个实验实现前应明确：
- 对应 `04-00-experiments.md` 中哪个实验编号
- 对应 `03-00-structure.md` 中哪个 `Fig.x` / `Table.x`
- 对应 `01-story.md` 中哪个 claim
- 图表类型（`[数据图]` / `[数据表]` / `[示意图]`）
- 文件名（数据类：`fig_NN_xxx.ipynb` / `tab_NN_xxx.ipynb`；示意类：`fig_NN_xxx.md`）
- 成功后应产生哪些输出（PDF 图表路径、指标值等）

**强制约束**：一个文件（`.ipynb` 或 `.md`）只能对应一个 `Fig.x` 或一个 `Table.x`。若实验逻辑需要生成多个图/表，必须拆分为多个文件，数据类通过共享 `outputs/` 或 `data/` 中的中间结果来实现复用。

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
- [ ] `03-00-structure.md` 中声明的每个 `Fig.x` / `Table.x` 都有且仅有一个对应文件（数据类为 `.ipynb`，示意类为 `.md`），无遗漏无合并
- [ ] 每个数据类 notebook 的 md cell / 示意类 `.md` 文件标注了上游来源（`04-00` 实验编号、`01-story` claim、`03-00` 图表资产编号）
- [ ] 数据类 notebook：conda env `scf-paper` 已确认存在，第一个 cell 包含环境检查
- [ ] 有 `requirements.txt` 记录依赖版本
- [ ] 数据类脚本：随机种子已固定（如 `torch.manual_seed(42)`、`np.random.seed(42)`）
- [ ] README 中记录了文件与实验编号的对应表及执行顺序
- [ ] 数据类 notebook 从头到尾可顺序执行复现结果（`Cell → Run All`）；示意类 `.md` 文件已包含完整的生成 prompt 和输出要求

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