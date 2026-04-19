---
name: "03-01-paper-bibliography"
description: "基于 story、structure 和 venue 要求检索文献并生成参考文献初稿。"
allowed-tools: Read, Write, WebSearch, WebFetch, mcp__codex__codex
---

# 03-01-paper-bibliography

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

基于 `01-story.md`、`02-journal-requirements.md` 与 `03-structure.md` 做定向文献检索，生成 Related Work 笔记与参考文献初稿。

## 输入

- `01-story.md`
- `02-journal-requirements.md`
- `03-structure.md`

## 输出

- `03-01-related-work.md` （主要语言要用中文，名词等专业用语可以保留英文）
- `03-01-references.bib`
- `03-01-open-questions.md`（仅在检索范围或候选引用存在歧义时生成）

## 工作流

### Step 1: 提取检索意图

从输入中提取：
- 问题域与核心任务
- 方法关键词与同类方法簇
- 需要比较的 baseline 类型
- `03-structure.md` 中 Related Work / Experiments 对引用的直接需求
- 目标 venue 与风格约束

如果当前 story 对任务边界、方法类别或 baseline 范围定义不清，先向用户确认，不要自行扩大检索范围。

### Step 2: 检索最小必要文献池

使用 `WebSearch` 优先检索：
- 该问题域的代表性工作
- 当前方法最直接的比较对象
- 实验中将要出现的核心 baseline
- 近年与目标 venue 高相关的代表性论文

必要时使用 `WebFetch` 读取论文页、作者页、项目页或官方页面，补充：
- 标题、作者、年份
- 方法定位
- 与当前 story 的关系
- 是否适合写入主线叙事

只保留支撑当前论文叙事和实验设计所必需的文献；不要把检索扩展为全面综述。

### Step 3: 整理 related work 笔记

生成 `03-01-related-work.md`，建议结构：

```markdown
# Related Work Notes

## 必引文献
### 主题 A
- Paper: ...
- 贡献/定位: ...
- 与本文关系: ...
- 建议在正文中如何引用: ...

## 可选文献
- ...

## 不建议进入主线的文献
- ...
```

要求：
- 区分“必须进入正文的引用”和“只作背景补充的引用”
- 明确每篇文献与当前 story、structure、baseline 的关系
- 不要把相关性弱、仅名称相近的工作混入主线

### Step 4: 生成 BibTeX 初稿

为准备进入论文正文的文献生成 `03-01-references.bib`。

要求：
- 只收录当前论文大概率会实际引用的最小必要文献集
- 条目字段尽量完整
- 若信息不足，记录到 `03-01-open-questions.md`，不要编造 BibTeX 字段

### Step 5: Codex Review

调用 `mcp__codex__codex` 检查文献池与 story/structure 是否一致：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下文献检索结果是否与论文 story 和 structure 对齐：

    Story: {01-story.md}
    Structure: {03-structure.md}
    Related Work Notes: {03-01-related-work.md}
    Bibliography: {03-01-references.bib}

    检查要点：
    1. 是否漏掉了正文或实验会直接依赖的关键 baseline？
    2. 是否纳入了与主线关系过弱的文献？
    3. Related Work 的组织是否服务于当前 story？
    4. BibTeX 初稿是否足以支撑后续写作？
```

### Step 6: 输出下一步提示

输出：
- `03-01-related-work.md` 已生成
- `03-01-references.bib` 已生成
- 若存在歧义，提示先处理 `03-01-open-questions.md`
- 提示下一步：`/03-02-paper-theory-analysis`
