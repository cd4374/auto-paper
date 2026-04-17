---
name: "07-paper-compile"
description: "编译 LaTeX 生成 PDF。用于验证论文可编译并生成最终 PDF。"
allowed-tools: Bash, Read
---

# 07-paper-compile

编译 LaTeX 项目生成 PDF。

## 输入

`05-template/` 中的 LaTeX 项目

## 输出

`07-output/paper.pdf`

## 工作流

### Step 1: 检查文件

```bash
# 确认必要文件存在
ls 05-template/main.tex
ls 05-template/references.bib
```

### Step 2: 创建输出目录

```bash
mkdir -p 07-output
```

### Step 3: 编译

```bash
cd 05-template
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

### Step 4: 处理错误

检查 `main.log` 中的错误：
- Undefined references → 添加 `\label`
- Missing citations → 添加 bib 条目
- Overfull hbox → 调整排版

### Step 5: 复制输出

```bash
cp 05-template/main.pdf 07-output/paper.pdf
```

### Step 6: 验证

```bash
# 检查 PDF 非空
pdfinfo 07-output/paper.pdf | grep Pages
```

### 错误修复

常见错误及修复：
| 错误 | 修复 |
|------|------|
| Undefined reference | 添加 `\label{}` |
| Missing bib entry | 添加到 references.bib |
| Overfull hbox | 调整文本/使用 `\small` |
| Font not found | 安装缺失宏包 |
