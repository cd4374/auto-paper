---
name: "05-01-paper-template"
description: "生成论文 LaTeX 模板和目录结构"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# 05-01-paper-template

生成 `05-template/` 目录和基础结构。

## 接口契约

```
Preconditions: 无
Inputs(required):
  - 02-journal-requirements.md
  - 03-00-structure.md
  - skills/shared/templates/venue-requirements.json（skill 相对路径）
  - skills/shared/templates/{template_dir}/（模板目录）
Inputs(optional):
  - 03-01-references.bib
  - 04-03-paper-assets/
Outputs: 05-template/（目录结构）
Failure: 用户确认后继续
```

## Step 1: 读取期刊配置

读取 `02-journal-requirements.md` 提取 `venue_key`，解析规则：
1. 优先读取 front matter：`venue_key: <key>`
2. 若无 front matter，则读取正文字段：`- venue_key: <key>`

若 `venue_key` 缺失或 `venue-requirements.json` 无对应配置 → 阻塞，提示用户补充。

从配置读取模板目录与 `section_structure`。

## Step 2: 创建目录结构

若 `05-template/` 已存在 → 增量更新，不覆盖已有用户内容。

创建 `05-template/` 并复制模板文件。

**结构链路约束（强制）**：
- 章节骨架必须以 `03-00-structure.md` 为唯一直接来源创建 `sections/*.tex`
- `03-00-structure.md` 必须是由 `/03-00-paper-structure` 基于 `venue-requirements.json` 生成的结果
- 不允许在 05 阶段绕过 `03-00` 直接按模板章节写作

文件名规则：`N_title.tex`（序号+英文小写连字符）。

若 `03-00-structure.md` 章节无法稳定解析，则阻塞并提示先回到 `/03-00-paper-structure` 重生结构；不要在 05 阶段回退为直接读取 `venue-requirements.json` 生成骨架。

若模板缺失 → 阻塞，提示用户手动下载。

## Step 3: 处理 main.tex

复制模板 `main.tex` 后，按以下算法处理：

1. **保留 preamble**：`\documentclass`、所有 `\usepackage`、会议特定命令（如 `\icmltitle`）、`\input{math_commands.tex}`/`\input{checklist.tex}` 等保留不动。
2. **清理正文示例**：删除 `\begin{document}` 到 `\bibliography{}`（或 `\end{document}`）之间的官方示例正文、说明文字、占位内容。
3. **插入章节**：在 `\begin{document}` 后、`\bibliography{}` 前，按 `03-00-structure.md` 顺序插入 `\input{sections/N_title.tex}`。
4. **更新文献**：确保 `\bibliography{references}` 和 `\bibliographystyle{...}` 指向正确文件（已复制到 `05-template/references.bib`）。

**安全规则**：
- 不删除未知命令；不确定时保留并注释说明。
- Nature 模板明确禁止 `\input`，则直接内联写入（不拆分 `sections/*.tex`）。

## Step 4: 复制资产

- `03-01-references.bib` → `05-template/references.bib`
- `04-03-paper-assets/figures/` → `05-template/figures/`
- `04-03-paper-assets/latex_includes.tex`（如存在）

## 输出

完成后提示：
```
05-template/ 已生成。下一步：/05-02-paper-write
```
