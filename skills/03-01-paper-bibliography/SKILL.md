---
name: "03-01-paper-bibliography"
description: "基于 01-story.md、03-00-structure.md 和 venue 要求检索文献并生成参考文献初稿。"
allowed-tools: Bash, Read, Write, WebSearch, WebFetch, mcp__codex__codex
---

# 03-01-paper-bibliography

- REVIEWER_MODEL = `claude-opus-4-7` — Model used via Codex MCP.

基于 `01-story.md`、`02-journal-requirements.md` 与 `03-00-structure.md` 做定向文献检索，生成 Related Work 笔记与参考文献初稿。

## 输入

- `01-story.md`
- `02-journal-requirements.md`
- `03-00-structure.md`

## 输出

- `03-01-related-work.md` （主要语言要用中文，名词等专业用语可以保留英文）
- `03-01-references.bib`
- `03-01-open-questions.md`（仅在检索范围或候选引用存在歧义时生成）

## 工作流

### Step 1: 读取检索策略

读取 `skills/shared/source-policy.md` 了解：
- 数据库检索优先级（DBLP → CrossRef → 网络搜索）
- 来源标识规则（正式出版物 vs arXiv preprint）
- 时间窗口策略

如论文领域属于通信/硬件，额外读取 `skills/shared/venue-tiering.md` 确定相关 venue 分层。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查文献检索计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下文献检索计划是否合理：

    Story: {01-story.md 内容摘要}
    Structure: {03-00-structure.md 中 Related Work/Experiments 的引用需求}
    执行计划: 检索最小必要文献池，生成 related work 笔记与 BibTeX

    检查：要点见 codex-review-template.md
```

### Step 3: 提取检索意图

从输入中提取：
- 问题域与核心任务
- 方法关键词与同类方法簇
- 需要比较的 baseline 类型
- `03-00-structure.md` 中 Related Work / Experiments 对引用的直接需求
- 目标 venue 与风格约束

如果当前 story 对任务边界、方法类别或 baseline 范围定义不清，先向用户确认，不要自行扩大检索范围。

### Step 4: 检索最小必要文献池

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

### Step 5: 整理 related work 笔记

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
- 区分”必须进入正文的引用”和”只作背景补充的引用”
- 明确每篇文献与当前 story、structure、baseline 的关系
- 不要把相关性弱、仅名称相近的工作混入主线

### Step 6: 生成 BibTeX

**工具分工**：WebSearch/WebFetch 用于文献发现和元数据获取，Bash/curl 用于获取可验证的 BibTeX。

对每篇需要引用的论文，按以下顺序获取 BibTeX：

**① DBLP（首选）**：适用于 ML/AI、物理、数学等正式发表论文

```bash
# 1. 搜索（返回 JSON）
curl -s "https://dblp.org/search/publ/api?q=TITLE+AUTHOR&format=json&h=3"
# 2. 从 JSON 的 "info > url" 字段提取 DBLP key（如 "conf/iclr/Devlin20"）
# 3. 获取 BibTeX
curl -s "https://dblp.org/rec/{key}.bib"
```

若 DBLP API 返回为空或超时，**必须记录**，继续下一步。

**② CrossRef（第二 fallback）**：适用于有 DOI 的论文
```bash
curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"
```

**③ Semantic Scholar API（第三 fallback）**：
```bash
curl -s "https://api.semanticscholar.org/graph/v1/paper/search?query=TITLE&fields=title,authors,year,venue,externalIds" | python3 -c "
import json, sys
data = json.load(sys.stdin)
for p in data.get('data', []):
    if 'ArXiv' in p.get('externalIds', {}):
        print(f'arXiv: {p[\"externalIds\"][\"ArXiv\"]}')
    if 'DOI' in p.get('externalIds', {}):
        print(f'DOI: {p[\"externalIds\"][\"DOI\"]}')
"
```

**④ [VERIFY] 标记（最后手段）**：所有 API 均失败时：
- 在条目前加 `% [VERIFY]` 注释
- 记录到 `03-01-open-questions.md`
- **禁止编造任何字段**（尤其是 author、year、pages、venue）

**额外规则**：
- **arXiv preprint 必须标注正式发表 venue**（如论文已有正式版本，引用正式版本而非 arXiv）
- arXiv 条目标注格式：`@misc{key, author={...}, title={...}, year={...}, eprint={arXiv ID}, archivePrefix={arXiv}, primaryClass={cs.XX}, note={[preprint]}}`
- 只收录实际会被引用的最小必要文献集
- key 格式：`{firstauthor}{year}{keyword}`（如 `vaswani2017attention`）

### Step 7: Post-review

调用 `mcp__codex__codex` 检查文献池与 story/structure 是否一致：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下文献检索结果是否与论文 story 和 structure 对齐：

    Story: {01-story.md}
    Structure: {03-00-structure.md}
    Related Work Notes: {03-01-related-work.md}
    Bibliography: {03-01-references.bib}

    检查：要点见 codex-review-template.md
```

### Step 8: 输出下一步提示

输出：
- `03-01-related-work.md` 已生成
- `03-01-references.bib` 已生成
- 若存在歧义，提示先处理 `03-01-open-questions.md`
- 提示下一步：`/03-02-paper-theory-analysis`
