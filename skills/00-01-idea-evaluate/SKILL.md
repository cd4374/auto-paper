---
name: "00-01-idea-evaluate"
description: "对候选 idea 池做结构化评估，并对 top-k 想法做 novelty 与 paperability 风险审查。"
allowed-tools: Read, Write, WebSearch, WebFetch, mcp__codex__codex
---

# 00-01-idea-evaluate

- REVIEWER_MODEL = `claude-opus-4-7` — Model used via Codex MCP.

对 `00-00-idea-pool.md` 做结构化评分，并生成 `00-01-idea-evaluation.md`。

## 输入

- `00-00-idea-pool.md`
- 可选：用户补充偏好（偏快出结果、偏理论、偏顶会、偏低算力）

## 输出

`00-01-idea-evaluation.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 读取与拆分 idea

读取 `00-00-idea-pool.md`，为每个 idea 提炼：
- 核心 problem
- 关键 claim
- 最小方法差异
- 最小实验包

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查评估计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 idea evaluation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    执行计划: 对全部候选做轻量评分，选出 top-k 做深度 novelty 审查

    检查：要点见 codex-review-template.md
```

### Step 3: 轻量评分全体候选

参考 `skills/shared/idea-evaluation-template.md`，先对全部候选做结构化评分。

默认评分维度：
- novelty
- feasibility
- experiment cost
- theory potential
- paperability
- venue fit
- resource fit

要求：
- 不要只看“听起来新”，要看是否能形成可验证 claim
- `experiment cost` 分数越高表示越昂贵，需在结论中解释
- 对明显不成立或不适合当前约束的 idea，应直接标记 `reject`

### Step 4: 深度审查 top-k

选出最值得推进的 top-k（默认 3 个）idea，做更深入评估：
- 提炼每个 idea 最需要成立的 2-4 个 claim
- 使用 `WebSearch` / `WebFetch` 检查最近相关工作
- 记录 closest prior work、true delta、reviewer attack points

要求：
- novelty 深查只覆盖 top-k，避免流程过重
- 若在轻量评分阶段已能明确淘汰多数候选，可把 deep review 收缩到 1-3 个 idea
- 若发现“其实不新”，也要保留其 paperability / feasibility 价值判断
- 如果 novelty 不高但 framing 或 finding 仍有机会，要明确写出

### Step 5: Post-review

调用 `mcp__codex__codex` 检查评估是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 idea evaluation 是否合理：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}

    检查：要点见 codex-review-template.md
```

### Step 6: 输出确认

输出：
- `00-01-idea-evaluation.md` 已生成
- 总结主推与淘汰理由
- 提示下一步：`/00-02-idea-recommend`
