---
name: "05-03-paper-gate"
description: "最终检查与门控判定"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 05-03-paper-gate

最终检查与门控判定。

## 接口契约

```
Preconditions: 05-template/sections/*.tex 存在，且章节由 03-00-structure.md 驱动生成
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

## Step 0: 前置检查

验证以下前置条件满足：
- [ ] `05-template/sections/*.tex` 存在
- [ ] `02-journal-requirements.md` 存在
- [ ] `03-00-structure.md` 存在
- [ ] `05-template/` 目录存在

若不满足，阻塞并提示补齐。

## Step 1: 自动化检查

**结构优先检查（唯一模式）**：只支持 `sections/*.tex` 多文件模式，并以 `03-00-structure.md` 为章节对齐基准。

- 所有 `\ref{}` 有对应 `\label{}`
- 所有 `\cite{}` 在 references.bib 中存在
- 所有 `\includegraphics` 文件存在
- 无 TODO/FIXME/XXX 残留
- sections/*.tex 与 `03-00-structure.md` 章节一一对齐
- main.tex 引入所有 sections/*.tex

失败则阻塞。

## Step 2: 最终检查

按 `skills/shared/quality-checklist.md` 的"2. 论文自检清单"和"4. LaTeX 完整性检查"执行。

额外检查：
- 每章覆盖 `03-00-structure.md` 对应叙事
- 实验表述与 `04-03-experiment-analysis.md` 一致（如存在）
- 实验叙事可追溯到上游材料（cite experiment-analysis 具体结论）
- `04-03` 中标注"不可直写"的内容不得进入正文

## Step 3: 叙事覆盖度验证

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

## Step 4: Venue 约束检查

按 `02-journal-requirements.md` 检查：匿名要求、引用风格、checklist 包含。

## Step 5: 门控判定

收集失败项，生成 `05-template/check-failures.md`：
- 有阻塞项 → 必须修复
- 仅非阻塞项 → 用户确认后继续

## Step 6: 编译输出

若门控通过（无阻塞项），直接编译 PDF。

### 6.1 检查编译工具

```bash
which pdflatex || { echo "ERROR: pdflatex not found. Install MacTeX: brew install --cask mactex" && exit 1 }
which bibtex || { echo "ERROR: bibtex not found" && exit 1 }
which latexmk && LATEXMK=true || LATEXMK=false
```

若工具缺失，阻塞并提示安装方法。

### 6.2 编译

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

### 6.3 验证与清理

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