---
name: "07-paper-compile"
description: "编译 LaTeX 生成 PDF。用于验证论文可编译并生成最终 PDF。"
allowed-tools: Bash, Read
---

# 07-paper-compile

编译 LaTeX 项目生成 PDF。

## 输入

- `05-template/` 中的 LaTeX 项目
- `02-journal-requirements.md`（用于确定模板入口与编译约束，如可用）

## 输出

`07-output/paper.pdf`

## 工作流

### Step 1: 确定编译入口并检查文件

优先根据模板实际入口文件编译；若 `02-journal-requirements.md` 或模板目录中能确定入口文件，则以其为准，`main.tex` 仅作为默认约定。

```bash
# 确认入口文件与必要文件存在
ls 05-template
```

### Step 2: 创建输出目录

```bash
mkdir -p 07-output
```

### Step 3: 编译

根据模板入口文件执行编译；若模板已有明确编译方式，则优先沿用模板方式。

```bash
cd 05-template
pdflatex -interaction=nonstopmode <entry>.tex
bibtex <entry>
pdflatex -interaction=nonstopmode <entry>.tex
pdflatex -interaction=nonstopmode <entry>.tex
```

### Step 4: 记录编译问题

检查对应日志文件中的错误并记录：
- Undefined references
- Missing citations
- Overfull hbox
- Missing package / template-specific errors

默认记录并返回问题，不在本阶段自动扩展为正文修订或依赖安装。

### Step 5: 复制输出

```bash
cp 05-template/<entry>.pdf 07-output/paper.pdf
```

### Step 6: 验证

```bash
# 检查 PDF 非空
pdfinfo 07-output/paper.pdf | grep Pages
```

### 常见编译问题

常见问题：
| 问题 | 处理方式 |
|------|------|
| Undefined reference | 记录缺失引用并返回对应位置 |
| Missing bib entry | 记录缺失条目并返回对应位置 |
| Overfull hbox | 记录排版问题并返回对应位置 |
| Missing package / font | 记录缺失依赖或模板问题 |
