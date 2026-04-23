---
name: "05-03-paper-gate"
description: "最终检查与门控判定"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 05-03-paper-gate

最终检查与门控判定。

## 接口契约

```
Preconditions: 05-template/sections/*.tex 存在（multi-file）或 entry_tex 存在（single-file）
Inputs(required):
  - 02-journal-requirements.md（venue 约束）
  - 03-00-structure.md
  - 05-template/
Inputs(optional):
  - 03-01-related-work.md、03-02-theory-analysis.md、04-03-experiment-analysis.md（清单检查）
Outputs: 05-template/check-failures.md（如有失败项）
Failure(阻塞): 修复后重跑
Failure(非阻塞): 用户确认后继续
```

## Step 7: 最终检查清单（9项）

- 每章覆盖 `03-00-structure.md` 对应叙事
- Related Work 基于 `03-01-related-work.md`（如存在）
- Method/Theory/Experiments 与 `03-02-theory-analysis.md` 一致（如存在）
- 实验表述与 `04-03-experiment-analysis.md` 一致（如存在）
- 实验叙事可追溯到上游材料（cite experiment-analysis 具体结论）
- `04-03` 中标注"不可直写"的内容不得进入正文
- `references.bib` 与 `03-01-references.bib` 来源一致
- heuristic 不写成 theorem-level certainty
- assumptions/limitations 充分暴露
- 无 TODO/FIXME 残留

## Step 7.1: 自动化检查

**模式判定**：按 venue 配置判断 multi-file 或 single-file。

**Multi-file 检查**：
- 所有 `\ref{}` 有对应 `\label{}`
- 所有 `\cite{}` 在 references.bib 中存在
- 所有 `\includegraphics` 文件存在
- 无 TODO/FIXME/XXX 残留
- sections/*.tex 与 structure.md 章节对齐
- main.tex 引入所有 sections/*.tex

**Single-file 检查**（仅 entry_tex）：
- 引用/图表/TODO 同上
- 章节覆盖由 Codex 审查（无 sections/*.tex 对齐）

失败则阻塞。

## Step 7.2: 叙事覆盖度验证

**判定表**（每章）：

| 指标 | 完整覆盖阈值 | 阻塞阈值 |
|------|-------------|---------|
| 字数 | ≥ structure 要求的 80% | < 50% |
| 图表数 | ≥ structure 要求 | < 1（若要求≥1）|
| 公式数 | ≥ structure 要求的 70% | < 1（若要求≥1）|

提取每章指标，按表判定：
- 完整覆盖 → 通过
- 部分缺失（低于完整但高于阻塞）→ 非阻塞
- 严重缺失（低于阻塞阈值）→ 阻塞

调用 Codex 审查，将证据写入 `check-failures.md`。

## Step 7.3: Venue 约束检查

按 `02-journal-requirements.md` 检查：匿名要求、引用风格、checklist 包含。

## Step 7.4: 门控判定

收集失败项，生成 `05-template/check-failures.md`：
- 有阻塞项 → 必须修复
- 仅非阻塞项 → 用户确认后继续

## Step 8: 编译输出

若门控通过（无阻塞项），直接编译 PDF。

### 8.1 检查编译工具

```bash
which pdflatex || { echo "ERROR: pdflatex not found. Install MacTeX: brew install --cask mactex" && exit 1 }
which bibtex || { echo "ERROR: bibtex not found" && exit 1 }
which latexmk && LATEXMK=true || LATEXMK=false
```

若工具缺失，阻塞并提示安装方法。

### 8.2 编译

进入 `05-template/` 目录，优先使用 `latexmk`：

```bash
cd 05-template
if $LATEXMK; then
  latexmk -pdf -interaction=nonstopmode main.tex
else
  # Fallback: 手写编译链（最多 3 次直到引用稳定）
  for i in 1 2 3; do
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    bibtex main > /dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    if ! grep -q "Warning.*Rerun" main.log 2>/dev/null; then
      break
    fi
  done
fi
```

### 8.3 验证与清理

检查 `main.pdf` 是否生成，并记录编译日志中的关键错误：

```bash
# 检查未定义引用、缺失 citation、overfull hbox
if [ -f main.pdf ]; then
  echo "✓ PDF 生成成功"
  grep -i "undefined reference\|missing citation\|overfull.*hbox" main.log | head -20
else
  echo "✗ 编译失败，请检查 main.log"
  exit 1
fi
```

编译产物（`main.pdf`）保留在 `05-template/` 中，不额外创建输出目录。

## 输出

- 门控通过 + 编译成功：`05-template/main.pdf` 已生成。提示下一步：`/06-paper-review`
- 门控失败：`05-template/check-failures.md`（阻塞，修复后重跑）
- 编译失败：返回 `05-template/main.log` 关键错误（阻塞，修复后重跑）