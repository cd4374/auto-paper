---
name: "07-paper-compile"
description: "编译 LaTeX 生成 PDF。用于验证论文可编译并生成最终 PDF。"
allowed-tools: Bash, Read, mcp__codex__codex
---

# 07-paper-compile

- REVIEWER_MODEL = `claude-opus-4-7` — Model used via Codex MCP.

编译 LaTeX 项目生成 PDF。

## 输入

- `05-template/` 中的 LaTeX 项目
- `02-journal-requirements.md`（用于确定模板入口与编译约束，如可用）

## 输出

`07-output/paper.pdf`

## 工作流

### Step 1: Pre-review

调用 `mcp__codex__codex` 检查编译准备是否充分：

```
mcp__codex__codex:
  model: claude-opus-4-7
  prompt: |
    请检查以下编译准备是否充分：

    LaTeX 目录: {05-template 文件列表}
    期刊要求: {02-journal-requirements.md 格式要求}

    检查：要点见 codex-review-template.md
```

### Step 2: 确定编译入口并检查文件

1. 若 `02-journal-requirements.md` 包含 venue 信息，读取 `venue-requirements.json` 中的 `entry_tex`（如 `neurips/main.tex`）
2. 从 `entry_tex` 提取文件名（不含子目录），作为编译入口：
   - `entry_tex = "neurips/main.tex"` → 入口为 `main.tex`
   - `entry_tex = "aps/main.tex"` → 入口为 `main.tex`
3. 若无法确定，默认入口为 `main.tex`
4. 确认入口文件与必要文件存在：

```bash
ls 05-template
```

### Step 3: 创建输出目录

```bash
mkdir -p 07-output
```

### Step 4: 编译

根据入口文件名（如 `main.tex`）执行编译，stem 为 `main`：

```bash
cd 05-template
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

若模板文档指定了其他编译方式（如 `latexmk`），优先按模板说明执行。

### Step 5: 记录编译问题

检查对应日志文件中的错误并记录：
- Undefined references
- Missing citations
- Overfull hbox
- Missing package / template-specific errors

默认记录并返回问题，不在本阶段自动扩展为正文修订或依赖安装。

### Step 6: 复制输出

```bash
cp 05-template/{stem}.pdf 07-output/paper.pdf
```

### Step 7: 验证与 Post-review

先验证 PDF 非空，再调用 `mcp__codex__codex` 检查编译结果是否满足期刊要求：

```bash
pdfinfo 07-output/paper.pdf | grep Pages
```

```
mcp__codex__codex:
  model: claude-opus-4-7
  prompt: |
    请检查以下编译结果是否满足期刊要求：

    期刊要求: {02-journal-requirements.md 页数/格式要求}
    PDF 信息: {pdfinfo 输出}
    编译日志: {关键错误摘要}

    检查：要点见 codex-review-template.md
```

### 常见编译问题

常见问题：
| 问题 | 处理方式 |
|------|----------|
| Undefined reference | 记录缺失引用并返回对应位置 |
| Missing bib entry | 记录缺失条目并返回对应位置 |
| Overfull hbox | 记录排版问题并返回对应位置 |
| Missing package / font | 记录缺失依赖或模板问题 |