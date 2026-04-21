---
name: "05-paper-write"
description: "基于 03-00-structure.md、文献笔记与实验结果撰写 LaTeX 论文。用于生成可编译的论文草稿。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 05-paper-write

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 `03-00-structure.md`、文献笔记与实验结果撰写 LaTeX。

## 输入

- `01-story.md`
- `03-00-structure.md`
- `03-01-related-work.md`
- `03-01-references.bib`
- `03-02-theory-analysis.md`
- `04-00-experiments.md`
- `04-02-experiment-results.md`
- `04-03-experiment-analysis.md`
- `04-03-paper-assets/`
- `02-journal-requirements.md`
- `skills/shared/templates/` 中的选中期刊模板

## 输出

填写好的 LaTeX 文件到 `05-template/`

## 工作流

### Step 0: 进入条件检查

**必须满足以下条件方可开始撰写**：
1. `04-03-experiment-analysis.md` 已存在且包含 `## Story Claim Coverage` 章节
2. 所有核心 story claim 均有实验支撑，或已在 `04-03-story-gap.md` 中记录并获用户确认继续

若不满足，**阻塞并返回 04-03 补齐**，不得跳过。

### Step 1: 准备模板

1. 优先复用现有 `05-template/`；只有缺失时才创建最小必要文件
2. 根据 `02-journal-requirements.md` 确定的模板，从 `skills/shared/templates/` 复制对应期刊的模板
3. 按 `03-00-structure.md` 创建必要的章节文件

如果模板选择、章节边界或输入材料不清楚，先向用户确认，不要自行假设。

### Step 2: 生成结构

按 `03-00-structure.md` 的章节规划创建目录。以下为常见示例：

```bash
05-template/
├── main.tex
├── sections/
│   ├── 1_introduction.tex
│   ├── 2_related_work.tex
│   ├── 3_method.tex
│   ├── 4_experiments.tex
│   └── 5_conclusion.tex
├── figures/
├── references.bib
└── template.sty
```

**产物自包含要求**（P0.2）：

1. 将 `03-01-references.bib` 复制/生成到 `05-template/references.bib`
2. 更新 LaTeX 中的 `\bibliography{}` 命令指向 `references`
3. 将 `04-03-paper-assets/` 中的所有图表复制到 `05-template/figures/`
4. 更新 LaTeX 中的 `\includegraphics` 路径为相对路径（相对于 `05-template/`）

实际章节命名与数量以 `03-00-structure.md` 为准。

### Step 3: Pre-review

调用 `mcp__codex__codex` 检查撰写准备是否充分：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下论文撰写准备是否充分：

    Story: {01-story.md 内容摘要}
    Structure: {03-00-structure.md 章节规划}
    Related Work: {03-01-related-work.md 必引文献}
    Theory Analysis: {03-02-theory-analysis.md 可写入结论}
    Experiment Analysis: {04-03-experiment-analysis.md 可直接用于论文的图表}
    Journal Requirements: {02-journal-requirements.md 格式限制}

    检查：要点见 codex-review-template.md
```

### Step 4: 逐章撰写

按 `03-00-structure.md` 的章节顺序撰写：

**每章流程**:
1. 读取 structure 中该章的叙事内容
2. 若当前章节涉及 Related Work，优先读取 `03-01-related-work.md`；若涉及引用条目，优先使用 `03-01-references.bib`
3. 若当前章节涉及 Method / Theory / Experiments / Discussion，优先读取 `03-02-theory-analysis.md` 中已确认的 claim、assumptions、prediction 与 writing notes
4. **只使用 `04-03-experiment-analysis.md` 中明确标注"可直接用于论文"的图表资产**；标注为"不能直接写进论文"的结论不得进入正文
5. 撰写完整 LaTeX（不是占位符）
6. 先检查该章是否覆盖既定叙事与结果证据
7. 调用 `mcp__codex__codex` review 检查

只写 `03-00-structure.md` 明确要求的内容；不要自行补充未要求的小节、扩展讨论或额外故事线。

写作时遵循“少而实”的分节原则：
- 不要为了覆盖每个点而机械新增 `subsection`/`subsubsection`
- 若某小节只有 1–2 个短段落，默认并入父节；只有 `03-00-structure.md` 明确要求或该小节承担独立论证功能时才保留
- 只有当该小节承担清晰且相对独立的论证功能时，才保留其标题

### Step 5: 撰写要点

以下为默认写作要点；若 `03-00-structure.md` 或 venue 要求更窄，以其为准。

**Abstract**: 5 部分（what/why hard/how/evidence/result），150-250 字
**Introduction**: hook + gap + approach + contributions + roadmap
**Related Work**: 按类别组织，不少于 1 页
**Method**: 符号定义 + 公式 + 算法
**Experiments**: setup → main results → ablation → analysis
**Conclusion**: 总结 + 局限性 + 未来方向

### Step 6: 每章 Post-review

每章完成后调用 `mcp__codex__codex` 进行 review：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下章节内容：

    Structure 要求: {该章叙事内容}
    Theory Analysis: {03-02-theory-analysis.md}
    实际内容: {章节 LaTeX 内容}

    检查：要点见 codex-review-template.md
```

### Step 7: 最终检查

- 每章内容已覆盖 `03-00-structure.md` 中对应叙事
- Related Work 章节优先基于 `03-01-related-work.md`
- Method / Theory / Experiments / Discussion 中的理论表述与 `03-02-theory-analysis.md` 一致
- 实验表述与 `04-03-experiment-analysis.md` 一致，未写入标注为"不能直接写进论文"的内容
- heuristic 不被误写成 theorem-level certainty
- assumptions / limitations 在正文中得到充分暴露
- `05-template/references.bib` 以 `03-01-references.bib` 为基础生成或填充
- 所有实验描述都能回溯到 `03-02` / `04-00` / `04-02` / `04-03`
- 无 TODO/FIXME 残留

### Step 7.1: 自动化 LaTeX 完整性检查

**必须执行，不得跳过**：

```bash
cd 05-template

# 检查未定义的 \ref
echo "=== Undefined refs ==="
for ref in $(grep -oE '\\\\ref\{[^}]+\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*\\ref{\([^}]*\)}.*/\1/' | sort -u); do
  grep -r "\\\\label{$ref}" . > /dev/null 2>&1 || echo "UNDEFINED REF: $ref"
done

# 检查缺失的 bib 条目
echo "=== Missing bib entries ==="
for key in $(grep -oE '\\cite[p]?\{[^}]+\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*{\([^}]*\)}.*/\1/' | tr ',' '\n' | sed 's/^ *//;s/ *$//' | sort -u); do
  grep -E "^\@.*\{${key}[,@]" references.bib > /dev/null 2>&1 || echo "MISSING BIB: $key"
done

# 检查缺失的图表文件
echo "=== Missing figures ==="
for fig in $(grep -oE '\\\\includegraphics[^;]*\{([^}]+)\}' sections/*.tex main.tex 2>/dev/null | sed 's/.*{\([^}]*\)}.*/\1/' | sort -u); do
  # 处理相对路径（相对于 05-template/）
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

若任何检查有输出，**必须修复后才能进入 06-paper-review**，不得绕过。
