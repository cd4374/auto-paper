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
- `02-journal-requirements.md`
- `../shared/templates/` 中的选中期刊模板

## 输出

填写好的 LaTeX 文件到 `05-template/`

## 工作流

### Step 1: 准备模板

1. 创建 `05-template/` 目录
2. 根据 `02-journal-requirements.md` 确定的模板，从 `../shared/templates/` 复制对应期刊的模板
3. 创建章节文件

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
2. 读取 experiments 中相关结果
3. 撰写完整 LaTeX（不是占位符）
4. 调用 `mcp__codex__codex` review 检查

### Step 4: 撰写要点

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
```

### Step 6: 最终检查

- 所有 `\ref` 有对应 `\label`
- 所有 `\cite` 有对应 bib 条目
- 无 TODO/FIXME 残留
