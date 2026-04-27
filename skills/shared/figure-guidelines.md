# 图表绘制指南

本文档定义 auto-paper 项目的图表生成与质量标准。

---

## 1. 快速参考

### 推荐工具
```python
import sys
sys.path.append('skills/shared')
from paper_plot_style import *
```

### 常量
| 常量 | 默认值 | 说明 |
|------|--------|------|
| DPI | 300 | 输出分辨率 |
| FORMAT | pdf | 统一导出格式（仅 PDF） |
| FONT_SIZE | 10 | 基础字号 |
| COLOR_PALETTE | tab10 | 颜色方案 |

---

## 2. 图表类型选择

| 数据模式 | 推荐类型 | 宽度 |
|----------|----------|------|
| X=时间/steps, Y=指标 | Line plot | 0.48\textwidth |
| X=方法/类别, Y=数值 | Bar chart | 0.48\textwidth |
| X=连续, Y=连续 | Scatter plot | 0.48\textwidth |
| 矩阵/网格值 | Heatmap | 0.48\textwidth |
| 分布比较 | Box/violin plot | 0.48\textwidth |
| 多数据集/多方法 | Multi-panel | 0.95\textwidth |
| 理论对比表 | LaTeX table | full width |

---

## 3. 绘图规范

### 字体
- Serif 字体：Times New Roman
- 基础字号：10pt
- 坐标轴标签：≥ 10pt
- Tick 标签：≥ 8pt

### 尺寸
- 单栏图：3.5–6 inches 宽
- 双栏/通栏图：7–12 inches 宽
- 高度比例：通常 0.6–0.8 × 宽度

### 分辨率
- PDF：矢量格式，无限清晰（统一导出格式）

### 多子图编号
```python
add_subfigure_label(ax, 'a')  # 添加 (a) 标签
```

### 布局
- 使用 `fig.tight_layout()` 避免重叠
- Legend 放在数据外侧或右下角
- 坐标轴标签有单位

---

## 4. 示例代码

### 基本折线图
```python
from paper_plot_style import *

fig, ax = plt.subplots(figsize=(5, 3))
ax.plot(steps, values, label='Method', color=COLORS[0])
ax.set_xlabel('Training Steps')
ax.set_ylabel('Loss')
ax.legend(frameon=False)
save_fig(fig, 'fig_training_curve')
```

### 多子图
```python
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

add_subfigure_label(ax1, 'a')
add_subfigure_label(ax2, 'b')

ax1.plot(...)
ax2.plot(...)

fig.tight_layout()
save_fig(fig, 'fig_comparison')
```

### 柱状图
```python
fig, ax = plt.subplots(figsize=(5, 3))
methods = ['A', 'B', 'Ours']
values = [82.3, 85.1, 89.2]
bars = ax.bar(methods, values, color=[COLORS[i] for i in range(len(methods))])

for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
            f'{val:.1f}', ha='center', va='bottom', fontsize=FONT_SIZE-1)

ax.set_ylabel('Accuracy (%)')
save_fig(fig, 'fig_bar_comparison')
```

---

## 5. LaTeX 嵌入

### 标准格式
```latex
\begin{figure}[t]
    \centering
    \includegraphics[width=0.48\textwidth]{figures/fig_name.pdf}
    \caption{Training curves comparing factorized and baseline methods.}
    \label{fig:training_curves}
\end{figure}
```

### 尺寸参考
| 宽度 | LaTeX 命令 | 适用场景 |
|------|-----------|----------|
| 单栏 | `width=0.48\textwidth` | 论文正文中的独立图 |
| 双栏 | `width=0.95\textwidth` | 占满整页的图 |
| 半栏 | `width=0.23\textwidth` | 并排多图 |

### 引用方式
```latex
如图~\ref{fig:training_curves} 所示
如图~\subref{fig:sub_a} 所示
```

---

## 6. 常见问题

### 字体太小
- 检查 axes.labelsize 和 xtick.labelsize
- 建议 base font size ≥ 10pt

### 图例遮挡数据
- 使用 `loc='best'` 或手动指定位置
- 或使用 `frameon=False` 去掉边框

### PDF 字体嵌入问题
- 使用 `bbox_inches='tight'`
- 或设置 `savefig.pad_inches = 0.05`

### 多子图间距不均
- 使用 `fig.subplots_adjust(wspace=0.3, hspace=0.3)`
- 或使用 `GridSpec` 做精确控制

---

## 7. 质量检查

生成图表后，按优先级做图片审查：先使用 Kimi MCP（`mcp__kimi-code__kimi_read_media`），仅当前一工具不可用时降级到 MiniMax MCP（`mcp__MiniMax__understand_image`）：

```
mcp__kimi-code__kimi_read_media(
  path: "path/to/figure.pdf",
  prompt: "Analyze this scientific figure for an academic paper. Check: (1) Is the font readable? (2) Are subplot labels (a), (b)... visible? (3) Are axis labels and legends clear? (4) Any overlap or occlusion?"
)
# fallback only when unavailable:
mcp__MiniMax__understand_image(
  image_source: "path/to/figure.pdf",
  prompt: "Analyze this scientific figure for an academic paper. Check: (1) Is the font readable? (2) Are subplot labels (a), (b)... visible? (3) Are axis labels and legends clear? (4) Any overlap or occlusion?"
)
```

检查清单（12 项）详见 `quality-checklist.md`。
