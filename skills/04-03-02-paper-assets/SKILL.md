---
name: "04-03-02-paper-assets"
description: "整理论文可用图表资产、生成 LaTeX 嵌入片段，并完成关键图图片审查。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__kimi-code__kimi_read_media, mcp__MiniMax__understand_image, mcp__codex__codex
---

# 04-03-02-paper-assets

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于已完成审计结果，从 notebook 产出的图表中整理最小必要论文图表资产并做图片审查。

## 输入
- `04-03-experiment-analysis.md`（来自 04-03-01 的审计结论）
- `04-01-experiment-code/figures/`（notebook 生成的 PDF 图表）
- `04-02-experiment-results/`
- `03-00-structure.md`

## 输出
- `04-03-paper-assets/`
- `04-03-paper-assets/latex_includes.tex`
- 更新 `04-03-experiment-analysis.md` 的 `## Figure Review`

## 工作流

### Step 1: 选择最小必要资产并分类

从 `04-01-experiment-code/figures/` 中筛选 PDF 图表，按生成方式分类：

| 类别 | 来源 | 处理方式 |
|------|------|----------|
| 数据图 | notebook 自动生成 | 直接复制到 `04-03-paper-assets/` |
| 架构/流程/示意图 | 手动创建（draw.io / Figma / TikZ） | 标记 `[MANUAL]`，提醒用户补充 |
| AI 插图 | `paper-illustration` 等外部工具 | 标记 `[MANUAL]`，检查格式兼容性 |

命名需可回溯到 notebook 中的实验或 claim。只复制可直接支撑当前 story/structure 的图表。手动类图表不阻塞流水线，但在 `latex_includes.tex` 和 Figure Review 中明确标注为待补充。

### Step 2: 生成/整理 LaTeX 片段
写入 `04-03-paper-assets/latex_includes.tex`，要求：
- 宽度 `0.48\textwidth`（单栏）或 `0.95\textwidth`（双栏）
- caption 简洁完整
- label 使用 `fig:fig_name`

标准 LaTeX 嵌入格式：
```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.48\textwidth]{figures/fig_name.pdf}
    \caption{...}
    \label{fig:fig_name}
\end{figure}
```

尺寸参考：
| 宽度 | LaTeX 命令 | 适用场景 |
|------|-----------|----------|
| 单栏 | `width=0.48\textwidth` | 论文正文中的独立图 |
| 双栏 | `width=0.95\textwidth` | 占满整页的图 |
| 半栏 | `width=0.23\textwidth` | 并排多图 |

### Step 3: 图片审查（优先 Kimi）

按以下清单逐项检查：

**可读性**：
- [ ] 字体大小合适，printed size 可读（≥ 8pt）
- [ ] 颜色在灰度模式下可区分（打印友好）
- [ ] 曲线、热图、坐标轴、legend、colorbar、annotation 清晰可读
- [ ] 文字与图形元素无重叠、遮挡
- [ ] 坐标轴标签有单位（如适用）
- [ ] 坐标轴标签是 publication 级别（如 `Cross-Entropy Loss` 而非 `loss`）
- [ ] 信息密度合适：读者应在 5 秒内理解图表主旨

**多子图**：
- [ ] 每个子图左上角有 (a)、(b)、(c)... 编号
- [ ] 编号清晰可见、位置一致
- [ ] 正文中可引用 "(如图 (a) 所示)"

**布局**：
- [ ] Legend 不遮挡数据（放在外侧或右下角）
- [ ] 无箭头/连接线交叉
- [ ] 间距平衡（不太挤也不太稀疏）
- [ ] 图表宽度符合期刊要求（单栏 0.48\textwidth，双栏 0.95\textwidth）

**样式**：
- [ ] Serif 字体（Times New Roman）匹配正文
- [ ] 无 matplotlib 默认 title（title 只在 LaTeX caption 中）
- [ ] 无装饰元素（背景色、3D 效果、chart junk）
- [ ] 色彩协调（非彩虹色，3-5 种主色）

**格式**：
- [ ] PDF 输出为矢量格式（非光栅化）
- [ ] 图表文件后缀统一为 .pdf
- [ ] colorbar 有完整标注（数值范围、单位）

降级规则：
- 先 `mcp__kimi-code__kimi_read_media`
- 不可用时再 `mcp__MiniMax__understand_image`
- 必须记录降级原因

### Step 3.5: 语义审查（Codex MCP）

视觉审查通过后，对每张图做语义审查——图类型是否适合展示该数据：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请审查以下论文图表（语义层面）：

    图表列表及描述：
    [逐图列出：文件名、图类型、展示的数据、对应的 story claim]

    对每张图检查：
    1. 图类型是否适合展示该数据？（如：比较方法应用 bar chart 而非 line plot）
    2. 是否有更有效的可视化选择？
    3. 该图是否清晰支撑了其对应的 story claim？
    4. 图中信息密度是否合适（不过密、不过空）？
```

### Step 4: 写入 Figure Review
把结论写回 `04-03-experiment-analysis.md`：
- 哪些图可直接用于论文
- 哪些需小改
- 哪些需重绘

### Step 5: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查图表资产与审查结论是否可回溯、是否服务主线；有问题则迭代。

## 约束
- 不做无关重绘、不新增无关图表。
- 不把仅内部判断的图直接标为可写入论文。