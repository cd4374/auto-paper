---
name: "project-import-02-venue-structure"
description: "识别或推荐 venue，生成 02-journal-* 与 03-00-structure.md。"
allowed-tools: Read, Write, Glob, Grep, mcp__kimi-code__kimi_web_search, mcp__kimi-code__kimi_fetch_url, mcp__MiniMax__web_search, WebSearch, WebFetch, mcp__codex__codex
---

# project-import-02-venue-structure

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

从现有线索恢复 venue 与结构层。

## 输入
- `01-story.md`
- 项目中的模板线索（class/sty/bst、草稿会议信息）
- `skills/shared/templates/venue-requirements.json`

## 输出
- `02-journal-recommendation.md`
- `02-journal-requirements.md`
- `03-00-structure.md`

## 工作流

### Step 1: 识别或推荐 venue
优先识别已有 venue（模板 marker / 草稿痕迹）。
识别失败时按优先级检索推荐 1-2 个候选：
`mcp__kimi-code__kimi_web_search` → `mcp__MiniMax__web_search` → `WebSearch`。
必要时抓取官网细节：`mcp__kimi-code__kimi_fetch_url` → `WebFetch`。

### Step 2: 生成 02-journal 文件
结合 `venue-requirements.json` 输出 recommendation + requirements。

### Step 3: 生成 `03-00-structure.md`
规则：
- 有成熟草稿结构则优先保留
- 否则按 venue `section_structure` 生成
- 每章叙事必须映射回 story

### Step 4: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查：
- venue 推荐与 story 匹配性
- structure 对 story 支撑度

## 约束
- 不因“看起来更像顶会”而偏离现有证据。
- 不把不确定 venue 信息写成确定事实。