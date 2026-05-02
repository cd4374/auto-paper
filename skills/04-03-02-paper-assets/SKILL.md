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

### Step 1: 选择最小必要资产

从 `04-01-experiment-code/figures/` 中筛选可直接支撑当前 story/structure 的 PDF 图表，复制到 `04-03-paper-assets/`。命名需可回溯到 notebook 中的实验或 claim。

注意：所有图表均通过 notebook 中的 `save_fig_and_show()` 生成，已为 PDF 矢量格式，无需格式转换。

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