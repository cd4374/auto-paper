---
name: "project-import"
description: "解析现有研究项目并转化为 auto-paper 标准格式（主入口，编排 project-import-01/02/03 子阶段）。"
allowed-tools: Bash, Read, Glob, Grep, Write, mcp__kimi-code__kimi_web_search, mcp__kimi-code__kimi_fetch_url, mcp__MiniMax__web_search, WebSearch, WebFetch, mcp__codex__codex
forbidden-actions:
  - 不要重构已有的实验代码
  - 不要补做 structure 之外的实验
  - 不要凭空生成不存在的实验结果
  - 不要修改用户提供的原始文件
  - 不要把 medium confidence 的推断标记为 high confidence
---

# project-import

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

导入主入口：分三段恢复 story、venue/structure 与理论/实验材料。

## 输入
- 一个现有项目目录（代码、实验结果、论文草稿、笔记）

## 输出（尽可能生成）
- `01-story.md`
- `02-journal-recommendation.md`
- `02-journal-requirements.md`
- `03-00-structure.md`
- `03-02-theory-analysis.md`（证据充足时）
- `04-00-experiments.md`
- `04-02-experiment-results.md`（证据充足时）

信息不足时必须明确标注“待确认/缺失”，禁止编造。

## 子阶段编排

**执行约束（强制）**：必须按 `Stage A → Stage B → Stage C` 串行执行，禁止跳步或只执行部分子阶段。若某阶段证据不足，应在该阶段显式标注“待确认/缺失”，再进入下一阶段。

### Stage A: `/project-import-01-survey-story`

目标：项目普查 + 证据分级 + `01-story.md` 恢复。

产出：
- 证据摘要（high/medium/missing）
- `01-story.md`

### Stage B: `/project-import-02-venue-structure`

目标：识别/推荐 venue，并恢复 `03-00` 结构。

产出：
- `02-journal-recommendation.md`
- `02-journal-requirements.md`
- `03-00-structure.md`

### Stage C: `/project-import-03-experiment-recovery`

目标：条件性恢复 `03-02` 与 04 阶段材料并做一致性检查。

产出（按证据）：
- `03-02-theory-analysis.md`
- `04-00-experiments.md`
- `04-02-experiment-results.md`

## 统一约束

- 证据优先，不做无依据推断。
- 只做映射与恢复，不重写原项目代码。
- 只恢复当前主线所需最小材料。

## 最终输出与下游提示

最后总结：
- 已生成文件清单
- high/medium/missing 项
- 仍需用户确认项

下游依赖检查：
- 缺 `03-01-related-work.md`/`03-01-references.bib` → 建议先 `/03-01-paper-bibliography`
- 缺 `04-03-paper-assets/`/`04-03-experiment-analysis.md` → 建议先 `/04-03-experiment-analysis`

不要默认直接跳到 `/05-02-paper-write`，除非 `03-01` 与 `04-03` 已完整。