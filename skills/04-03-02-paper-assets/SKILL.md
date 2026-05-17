---
name: "04-03-02-paper-assets"
description: "整理论文可用图表资产、生成 LaTeX 嵌入片段，并完成关键图图片审查。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__kimi-code__kimi_read_media, mcp__MiniMax__understand_image, Shell
---

# 04-03-02-paper-assets

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex CLI.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于已完成审计结果，从 notebook 产出的图表中整理最小必要论文图表资产并做图片审查。

## 输入
- `04-03-experiment-analysis.md`（来自 04-03-01 的审计结论）
- `04-01-experiment-code/figures/`（数据图为 PDF，示意图为 SVG）
- `04-02-experiment-results/`
- `03-00-structure.md`

## 输出
- `04-03-paper-assets/`
- `04-03-paper-assets/latex_includes.tex`
- 更新 `04-03-experiment-analysis.md` 的 `## Figure Review`

## 工作流

### Step 1: 选择最小必要资产并分类

先读取 `03-00-structure.md` 中的 `图表资产` 清单，获取全文计划的 `Fig.x` / `Table.x` 及其叙事功能说明。再读取 `04-01-experiment-code/README.md` 中的文件与图表资产对应表。然后从 `04-01-experiment-code/figures/` 中筛选图表资产（数据图为 PDF，示意图为 SVG），按生成方式分类：

| 类别 | 来源 | 处理方式 |
|------|------|----------|
| 数据图 | `fig_NN_xxx.ipynb` 代码生成 | 直接复制 PDF 到 `04-03-paper-assets/figures/` |
| 数据表 | `tab_NN_xxx.ipynb` 代码生成 | 直接复制/生成 LaTeX 表格代码 |
| 示意图 | `fig_NN_xxx.md` prompt 文档 | 读取 `.md` 中的 prompt，标记 `[PROMPT]`，提醒用户调用 LLM 生成 SVG；生成后将 SVG 复制到 assets |
| 手动图 | 人工绘制（draw.io / Figma / TikZ 等） | 标记 `[MANUAL]`，提醒用户补充 |

命名需可回溯到 notebook 中的实验或 claim，且与 `03-00-structure.md` 中的 `Fig.x` / `Table.x` 编号一一对应。由于 `04-01` 实行"一个图表资产一个 notebook"，每张图/表应能精确对应到 `fig_NN_xxx.ipynb` 或 `tab_NN_xxx.ipynb`。

**分类处理逻辑**：
- **数据图/数据表**：检查 `04-01-experiment-code/figures/` 中是否存在对应 PDF，存在则复制到 `04-03-paper-assets/figures/`
- **示意图**：打开对应 `fig_NN_xxx.md`，提取 prompt，在 `latex_includes.tex` 中标记 `% Fig.x [PROMPT]` 并备注"需调用 LLM 生成 SVG，保存为 figures/fig_NN_xxx.svg"；不阻塞流水线，但在 Figure Review 中记录待生成状态
- **LaTeX 嵌入说明**：SVG 需配合 `\usepackage{svg}` 与 `\includesvg{}` 使用（编译时需 `--shell-escape` 及 Inkscape），或在编译前手动将 SVG 转为 PDF
- **手动图**：标记 `[MANUAL]`，提醒用户补充

若 structure 中声明的某 `Fig.x` / `Table.x` 在实验结果中缺失且非 `[PROMPT]`/`[MANUAL]`，标记为 `[PENDING]`，在 `latex_includes.tex` 中预留注释占位，并在 Figure Review 中说明。

### Step 2: 生成/整理 LaTeX 片段
写入 `04-03-paper-assets/latex_includes.tex`，要求：
- 宽度 `0.48\textwidth`（单栏）或 `0.95\textwidth`（双栏）
- caption 简洁完整，与 `03-00-structure.md` 中对应 `Fig.x` / `Table.x` 的叙事功能说明保持一致
- label 使用 `fig:NN_description` 或 `tab:NN_description`（编号前缀 + 描述性命名，如 `fig:1_problem_setup`、`tab:1_summary`），确保与 `03-00-structure.md` 中的 `Fig.NN` / `Table.NN` 一一对应；在每个环境上方用注释标注 structure 编号，如 `% Fig.1` / `% Table.1`

标准 LaTeX 嵌入格式：
```latex
% Fig.1
\begin{figure}[t]
    \centering
    % 数据图: \includegraphics[width=0.48\textwidth]{figures/fig_name.pdf}
    % 示意图(SVG): \includesvg[width=0.48\textwidth]{figures/fig_name.svg} (需 \usepackage{svg})
    \includegraphics[width=0.48\textwidth]{figures/fig_name.pdf}
    \caption{...}
    \label{fig:fig_name}
\end{figure}
```

表格示例：
```latex
% Table.1
\begin{table}[t]
    \centering
    \caption{...}
    \label{tab:tab_name}
    \begin{tabular}{...}
        ...
    \end{tabular}
\end{table}
```

尺寸参考：
| 宽度 | LaTeX 命令 | 适用场景 |
|------|-----------|----------|
| 单栏 | `width=0.48\textwidth` | 论文正文中的独立图 |
| 双栏 | `width=0.95\textwidth` | 占满整页的图 |
| 半栏 | `width=0.23\textwidth` | 并排多图 |

### Step 3: 图片审查（优先 Kimi）

**仅对数据图执行以下清单审查**。示意图和手动图在生成/补充后再审查。

按以下清单逐项检查：

**可读性**：
- [ ] 字体大小合适，printed size 可读（≥ 8pt）
- [ ] 颜色在灰度模式下可区分（打印友好）
- [ ] 曲线、热图、坐标轴、legend、colorbar、annotation 清晰可读
- [ ] 文字与图形元素无重叠、遮挡
- [ ] 坐标轴标签有单位（如适用）
- [ ] 坐标轴标签是 publication 级别（如 `Cross-Entropy Loss` 而非 `loss`）
- [ ] 信息密度合适：读者应在 5 秒内理解图表主旨

**多子图（Panel Architecture）**：
- [ ] 每个子图左上角有 (a)、(b)、(c)... 编号，9–10 pt 加粗
- [ ] 编号清晰可见、位置一致
- [ ] 正文中可引用 "(如图 (a) 所示)"
- [ ] 每个 panel 只承载一层核心信息，无过度叠加
- [ ] 同列 panel x 轴对齐，同行 panel y 轴范围统一或已注明差异
- [ ] panel 之间留白 ≥ 0.3 inch
- [ ] 共享 legend 统一放在图右侧或底部，未在每个 panel 内重复

**布局**：
- [ ] Legend 不遮挡数据（放在外侧或右下角）
- [ ] 无箭头/连接线交叉
- [ ] 间距平衡（不太挤也不太稀疏）
- [ ] 图表宽度符合期刊要求（单栏 0.48\textwidth，双栏 0.95\textwidth）

**样式（Typography & Colour）**：
- [ ] Serif 字体（Times New Roman）匹配正文
- [ ] 字号层级合规：轴标签 8–10 pt，刻度 7–8 pt，图例 7–8 pt，注释 7–9 pt
- [ ] 线宽合规：主线 1.0–1.5 pt，辅助线 0.5–0.8 pt，边框 0.8 pt
- [ ] 无 matplotlib 默认 title（title 只在 LaTeX caption 中）
- [ ] 无装饰元素（背景色、3D 效果、阴影、chart junk）
- [ ] 色彩板合规：使用固定语义色板（主色 `#2878B5`、对比 `#9AC9DB`、强调 `#C82423`、辅助 `#D3D3D3`、第三组 `#F8AC8C`）
- [ ] 单图主色 ≤ 3 种（灰色不计入），未使用随机生成颜色
- [ ] 连续数据使用单色渐变（如 `Blues` / `Greys` / `viridis`），未使用 `jet` / `rainbow` / `turbo`
- [ ] 色盲友好：无纯红-绿对比；双色对比使用蓝-橙或蓝-红

**格式**：
- [ ] PDF 输出为矢量格式（非光栅化）
- [ ] 图表文件后缀统一为 .pdf
- [ ] colorbar 有完整标注（数值范围、单位）

降级规则：
- 先 `mcp__kimi-code__kimi_read_media`
- 不可用时再 `mcp__MiniMax__understand_image`
- 必须记录降级原因

### Step 3.5: 语义审查（Codex CLI）

视觉审查通过后，对每张图做语义审查——图类型是否适合展示该数据：

```bash
codex exec -c model="gpt-5.5" << 'EOF'
请审查以下论文图表（语义层面）：

图表列表及描述：
[逐图列出：structure 编号（Fig.x/Table.x）、文件名、图类型、展示的数据、对应的 story claim]

对每张图检查：
1. 图类型是否适合展示该数据？（如：比较方法应用 bar chart 而非 line plot）
2. 是否有更有效的可视化选择？
3. 该图是否清晰支撑了其对应的 story claim？
4. 图中信息密度是否合适（不过密、不过空）？
EOF
```

### Step 4: 写入 Figure Review
把结论写回 `04-03-experiment-analysis.md`：
- 哪些图可直接用于论文
- 哪些需小改
- 哪些需重绘

### Step 5: Post-review（最多 10 轮）
调用 `codex exec` 检查图表资产与审查结论是否可回溯、是否服务主线；有问题则迭代。

## 约束
- 不做无关重绘、不新增无关图表。
- 不把仅内部判断的图直接标为可写入论文。