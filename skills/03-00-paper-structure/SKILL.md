---
name: "03-00-paper-structure"
description: "基于 01-story.md 和 02-journal-requirements.md 生成 03-00-structure.md。用于定义论文章节结构。"
allowed-tools: Bash, Read, Write, Glob, mcp__codex__codex
---

# 03-00-paper-structure

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于 `01-story.md` + 期刊要求生成 `03-00-structure.md`。

## 输入

- `01-story.md`
- `02-journal-requirements.md`
- `skills/shared/templates/venue-requirements.json`

## 输出

`03-00-structure.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 叙事框架

本章结构将 story 的三部分映射为论文的"探索 → 发现 → 理解"叙事弧：
- **是什么** → 对应 Introduction 的问题定义与背景
- **为什么** → 对应 Introduction 的动机与 Related Work 的定位
- **怎么做** → 对应 Method 的方法设计，并驱动 Experiments 的验证逻辑

## 工作流

### Step 1: 读取输入

读取 story 和 requirements。

### Step 2: 读取 venue 配置

从 `02-journal-requirements.md` 读取 `venue_key`，解析规则：
1. 优先读取 front matter：`venue_key: <key>`
2. 若无 front matter，则读取正文字段：`- venue_key: <key>`

若两者都缺失 → 阻塞，提示先重新生成 `02-journal-requirements.md`。

根据 `venue_key` 从 `venue-requirements.json` 读取 `section_structure`。
venue-requirements.json 位于 `skills/shared/templates/venue-requirements.json`。

### Step 3: Pre-review

调用 `mcp__codex__codex` 检查章节设计计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下章节设计计划是否合理：

    Story: {01-story.md 内容摘要，重点关注研究问题/动机/方法思路}
    Journal Requirements: {02-journal-requirements.md 格式限制}
    Venue Section Structure: {venue-requirements.json 中的 section_structure}
    执行计划: 根据叙事逻辑设计章节，遵循探索→发现→理解框架

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 4: 设计章节

根据 story 的叙事逻辑设计章节，遵循"发现递进"结构。

**基于 venue 配置生成章节**：
- 读取 venue-requirements.json 中对应 venue 的 section_structure
- 每节的 narrative_points 是必须覆盖的要点
- 根据 story 内容填充各节的发现/内容

**章节叙事重心**（参考 venue 配置）：

| 章节 | 叙事重心 | 核心问题 |
|------|---------|---------|
| Introduction | 探索动机 → 预期 vs 现实 | "这个领域有什么值得探索的？" |
| Related Work / (融入) | 已有理解的局限 | "别人的理解缺什么？" |
| Method | 探索策略 | "我们怎么系统地探索？" |
| Experiments / Results | 发现1 → 发现2 → ... | "我们发现了什么意料之外的事？" |
| Conclusion / Conclusions / Discussion | 理解的意义 | "我们理解了什么新东西？" |

章节与小节规划时遵循"密度优先"原则：
- 不要为了把要点列整齐而拆出过多小节
- 预计只有 1–2 个短段落的内容，默认并入父节，不单独设小节
- 只有当某部分承载独立论证单元、并且内容足以自成展开时，才单独设小节

### Step 5: 填写章节内容

参考 venue-requirements.json 中对应 venue 的 section_structure，每章填写：
- **叙事内容**: 本章要讲什么故事（探索动机、发现序列、理解深化）
- **需求**: 字数范围、图表数量、公式数量（来自 venue 配置）

```markdown
# Chapter 1: Introduction
叙事内容: 探索动机 → 预期 vs 现实

需求:
  - 字数: 500-800
  - 图表: 1张问题示意图
```

### Step 6: 结合期刊要求

根据 `02-journal-requirements.md` 调整：
- 字数上限
- 章节命名（参考 venue 配置中的 name）
- 图表限制

### Step 7: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查 structure 是否支撑 story：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 structure 是否支撑 story：

    Story: {story 内容，重点关注 是什么/为什么/怎么做 是否在章节中得到充分展开}
    Structure: {structure 内容}

    检查要点：
    1. 章节顺序是否服务于"探索→发现→理解"的递进逻辑？
    2. 每章叙事是否充分展开了 story 中定义的问题、动机与方法？
    3. 发现是否有层次感（从初步到深层）？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 structure → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...
