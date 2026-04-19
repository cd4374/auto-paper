---
name: "05-paper-write"
description: "基于 structure.md 和实验结果撰写 LaTeX 论文。用于生成可编译的论文草稿。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 05-paper-write

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 structure + experiments 撰写 LaTeX。

## 输入

- `01-story.md`
- `03-structure.md`
- `04-00-experiments.md`
- `04-02-experiment-results.md`
- `04-03-experiment-analysis.md`
- `04-03-paper-assets/`
- `02-journal-requirements.md`
- `skills/shared/templates/` 中的选中期刊模板

## 输出

填写好的 LaTeX 文件到 `05-template/`

## 工作流

### Step 1: 准备模板

1. 优先复用现有 `05-template/`；只有缺失时才创建最小必要文件
2. 根据 `02-journal-requirements.md` 确定的模板，从 `skills/shared/templates/` 复制对应期刊的模板
3. 按 `03-structure.md` 创建必要的章节文件

如果模板选择、章节边界或输入材料不清楚，先向用户确认，不要自行假设。

### Step 2: 生成结构

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

### Step 3: 逐章撰写

按 `03-structure.md` 的章节顺序撰写：

**每章流程**:
1. 读取 structure 中该章的叙事内容
2. 优先读取 `04-03-experiment-analysis.md` 中已确认的分析结论与 `04-03-paper-assets/` 中的图表资产；必要时回溯 `04-02` 原始结果
3. 撰写完整 LaTeX（不是占位符）
4. 先检查该章是否覆盖既定叙事与结果证据
5. 调用 `mcp__codex__codex` review 检查

只写 `03-structure.md` 明确要求的内容；不要自行补充未要求的小节、扩展讨论或额外故事线。

写作时遵循“少而实”的分节原则：
- 不要为了覆盖每个点而机械新增 `subsection`/`subsubsection`
- 若某小节只有 1–2 个短段落，默认并入父节；只有 `03-structure.md` 明确要求或该小节承担独立论证功能时才保留
- 只有当该小节承担清晰且相对独立的论证功能时，才保留其标题

### Step 4: 撰写要点

以下为默认写作要点；若 `03-structure.md` 或 venue 要求更窄，以其为准。

**Abstract**: 5 部分（what/why hard/how/evidence/result），150-250 字
**Introduction**: hook + gap + approach + contributions + roadmap
**Related Work**: 按类别组织，不少于 1 页
**Method**: 符号定义 + 公式 + 算法
**Experiments**: setup → main results → ablation → analysis
**Conclusion**: 总结 + 局限性 + 未来方向

### Step 5: Codex Review

每章完成后调用 `mcp__codex__codex` 进行 review：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下章节内容：

    Structure 要求: {该章叙事内容}
    实际内容: {章节 LaTeX 内容}

    检查要点：
    1. 是否覆盖 structure 中的叙事？
    2. 语言是否清晰简洁？
    3. 是否符合期刊风格？
    4. 是否存在只有极少内容却单独成节的小节？
```

### Step 6: 最终检查

- 每章内容已覆盖 `03-structure.md` 中对应叙事
- 所有实验描述都能回溯到 `04-00` / `04-02` / `04-03`
- 所有 `\ref` 有对应 `\label`
- 所有 `\cite` 有对应 bib 条目
- 无 TODO/FIXME 残留
