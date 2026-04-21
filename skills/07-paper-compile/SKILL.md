---
name: "07-paper-compile"
description: "编译 LaTeX 生成 PDF。用于验证论文可编译并生成最终 PDF。"
allowed-tools: Bash, Read, mcp__codex__codex
---

# 07-paper-compile

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

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
  model: gpt-5.4
  prompt: |
    请检查以下编译准备是否充分：

    LaTeX 目录: {05-template 文件列表}
    期刊要求: {02-journal-requirements.md 格式要求}

    检查：要点见 codex-review-template.md
```

### Step 2: 确定编译入口并检查工具

1. 若 `02-journal-requirements.md` 包含 venue 信息，读取 `venue-requirements.json` 中的 `entry_tex`
2. 从 `entry_tex` 提取文件名作为编译入口
3. 检查工具可用性：
```bash
which pdflatex || { echo "ERROR: pdflatex not found. Install MacTeX: brew install --cask mactex" && exit 1 }
which bibtex || { echo "ERROR: bibtex not found" && exit 1 }
which latexmk && LATEXMK=true || LATEXMK=false
which pdfinfo && PDFINFO=true || PDFINFO=false
```

若 pdflatex 不存在，**阻塞并报错**，不尝试修复。

### Step 3: 创建输出目录

```bash
mkdir -p 07-output
```

### Step 4: 编译

**优先使用 latexmk**（自动处理引用和引用循环直到稳定）：

```bash
cd 05-template
if $LATEXMK; then
  latexmk -pdf -interaction=nonstopmode main.tex
else
  # Fallback: 手写编译链（最多 3 次直到稳定）
  for i in 1 2 3; do
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    bibtex main > /dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    pdflatex -interaction=nonstopmode main.tex > /dev/null 2>&1
    # 检查是否还有未解决的引用
    if ! grep -q "Warning.*Rerun" main.log; then
      break
    fi
  done
fi
```

### Step 5: 记录编译问题

检查 `main.log` 中的错误并记录：
- Undefined references
- Missing citations
- Overfull hbox
- Missing package / template-specific errors

若存在上述错误，**不得跳过**，返回缺失位置供用户修复。

### Step 6: 复制输出

```bash
cp 05-template/main.pdf 07-output/paper.pdf
```

### Step 7: 验证与 Post-review

```bash
[ -s 07-output/paper.pdf ] || { echo "ERROR: PDF is empty or missing" && exit 1 }
if $PDFINFO; then
  PAGES=$(pdfinfo 07-output/paper.pdf | grep Pages | awk '{print $2}')
  echo "PDF pages: $PAGES"
  # 页数超限检查（由 Codex 检查，与 venue-requirements.json 对照）
fi
```

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下编译结果是否满足期刊要求：

    期刊要求页数限制: {02-journal-requirements.md 中的 page_limit}
    实际页数: {pdfinfo 输出}
    编译日志: {关键错误摘要}

    检查：要点见 codex-review-template.md
```

### 常见编译问题

| 问题 | 处理方式 |
|------|----------|
| Undefined reference | 记录缺失引用位置，返回修复 |
| Missing bib entry | 记录缺失条目，返回 03-01 补文献 |
| Overfull hbox | 记录位置，返回正文调整 |
| Missing package | 记录包名，建议用户安装 tlmgr |

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
  model: gpt-5.4
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