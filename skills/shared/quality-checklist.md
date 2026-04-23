# 统一质量检查清单

本文档汇总 auto-paper 项目各阶段的质量检查项，确保标准统一。

---

## 1. 图表质量检查清单（12 项）

用于 04-03-experiment-analysis 的图片审查。

### 可读性
- [ ] 字体大小合适，printed size 可读（≥ 8pt）
- [ ] 颜色在灰度模式下可区分（打印友好）
- [ ] 曲线、热图、坐标轴、legend、colorbar、annotation 清晰可读
- [ ] 文字与图形元素无重叠、遮挡
- [ ] 坐标轴标签有单位（如适用）
- [ ] 坐标轴标签是 publication 级别（如 `Cross-Entropy Loss` 而非 `loss`）

### 多子图
- [ ] 每个子图左上角有 (a)、(b)、(c)... 编号
- [ ] 编号清晰可见、位置一致
- [ ] 正文中可引用 "(如图 (a) 所示)"

### 布局
- [ ] Legend 不遮挡数据（放在外侧或右下角）
- [ ] 无箭头/连接线交叉
- [ ] 间距平衡（不太挤也不太稀疏）
- [ ] 图表宽度符合期刊要求（单栏 0.48\textwidth，双栏 0.95\textwidth）

### 样式
- [ ] Serif 字体（Times New Roman）匹配正文
- [ ] 无 matplotlib 默认 title（title 只在 LaTeX caption 中）
- [ ] 无装饰元素（背景色、3D 效果、chart junk）
- [ ] 色彩协调（非彩虹色，3-5 种主色）

### 格式
- [ ] PDF 输出为矢量格式（非光栅化）
- [ ] 分辨率 ≥ 300 DPI（如用 PNG）
- [ ] colorbar 有完整标注（数值范围、单位）

---

## 2. 论文自检清单

用于 06-paper-review 的自检。

```bash
# 检查项
- [ ] Abstract 是否覆盖 what/why/how/evidence/result 五要素
- [ ] Introduction 的 gap → approach → contributions 逻辑链是否清晰
- [ ] Related Work 是否覆盖相关工作且分类合理
- [ ] Method 的符号定义是否一致、无歧义
- [ ] 理论表述是否与 `03-02-theory-analysis.md` 一致，未把 heuristic 写成已证结论
- [ ] 实验是否验证了所有关键理论预测或明确说明未覆盖部分
- [ ] 结论是否回应了引言的动机
- [ ] 所有 \ref 指向有效 \label
- [ ] 所有 \cite 在 references.bib 中有对应条目
- [ ] 关键 figures 已用图片理解 MCP 做可读性与表达审查
- [ ] 无 TODO/FIXME 残留
- [ ] 没有大量只有 1–2 个短段落却单独成节的小节
```

---

## 3. 实验可复现性检查清单

用于 04-01-experiment-implement 的 Step 5.5。

每个实验必须满足：
- [ ] 随机种子已固定（如 `torch.manual_seed(42)`、`np.random.seed(42)`）
- [ ] 有 `requirements.txt` 或 `environment.yml` 记录依赖版本
- [ ] README 中的运行命令可从零复现结果（包含所有必要参数）
- [ ] 代码覆盖了 `04-00-experiments.md` 中该实验的所有设置项（数据集、baseline、指标）

---

## 4. LaTeX 完整性检查

用于 05-paper-write 的 Step 7.1。

```bash
cd 05-template

# 检查未定义的 \ref
echo "=== Undefined refs ==="
for ref in $(grep -oE '\\ref\{[^}]+\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*\\ref{\([^}]*\)}.*/\1/' | sort -u); do
  grep -r "\\label{$ref}" . > /dev/null 2>&1 || echo "UNDEFINED REF: $ref"
done

# 检查缺失的 bib 条目
echo "=== Missing bib entries ==="
for key in $(grep -oE '\\cite[p]?\{[^}]+\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*{\([^}]*\)}.*/\1/' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u); do
  grep -E "^\@.*\{${key}[,@]" references.bib > /dev/null 2>&1 || echo "MISSING BIB: $key"
done

# 检查缺失的图表文件
echo "=== Missing figures ==="
for fig in $(grep -oE '\\includegraphics[^;]*\{([^}]+)\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*{\([^}]*\)}.*/\1/' | sort -u); do
  if [[ "$fig" = figures/* ]]; then
    [ -f "$fig" ] || echo "MISSING FIGURE: $fig"
  elif [[ "$fig" = /* ]]; then
    echo "OUTSIDE PATH: $fig (must use relative path)"
  else
    [ -f "figures/$fig" ] || echo "MISSING FIGURE: figures/$fig"
  fi
done

# 检查 TODO/FIXME 残留
echo "=== TODO/FIXME ==="
grep -n -i "TODO\|FIXME\|XXX" sections/*.tex main.tex 2>/dev/null && echo "TODO/FIXME found!"
```

---

## 5. Review 触发点清单

| Skill | Pre-review 触发点 | Post-review 触发点 |
|-------|-------------------|-------------------|
| 00-00-idea-brainstorm | 生成 idea 前 | 生成 00-00-idea-pool.md 后 |
| 00-01-idea-evaluate | 评估前 | 生成 00-01-idea-evaluation.md 后 |
| 00-02-idea-recommend | 推荐前 | 生成 00-02-idea-recommendation.md 后 |
| 01-paper-init | 生成 story 前 | 生成 01-story.md 后 |
| 02-paper-journal | 推荐前 | 生成 requirements 后 |
| 03-00-paper-structure | 设计章节前 | 生成 03-00-structure.md 后 |
| 03-01-paper-bibliography | 检索前 | 生成 references.bib 后 |
| 03-02-paper-theory-analysis | 分析前 | 生成 03-02-theory-analysis.md 后 |
| 04-00-experiment-design | 设计实验前 | 生成 04-00-experiments.md 后 |
| 04-01-experiment-implement | 实现前 | 实现完成后 |
| 04-02-experiment-run | 运行前 | 收集结果后 |
| 04-03-experiment-analysis | 分析前 | 生成 analysis.md + 图表后 |
| 05-paper-write | 每章撰写前/后 | 同上 |
| 06-paper-review | 审查前 | 生成 report.md 后 |
| 06-01-review-assess | 评估前 | 生成 action-plan 后 |
| 06-02-review-apply | 修改前 | 修改完成后 |
