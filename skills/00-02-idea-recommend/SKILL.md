---
name: "00-02-idea-recommend"
description: "基于 idea 池与评估结果推荐主选 idea、备选方案，并给出进入 story 的 framing。"
allowed-tools: Read, Write, mcp__codex__codex
---

# 00-02-idea-recommend

- REVIEWER_MODEL = `claude-opus-4-7` — Model used via Codex MCP.

基于 `00-00-idea-pool.md` 与 `00-01-idea-evaluation.md`，生成 `00-02-idea-recommendation.md`。

## 输入

- `00-00-idea-pool.md`
- `00-01-idea-evaluation.md`

## 输出

- `00-02-idea-recommendation.md` -- （主要语言要用中文，名词等专业用语可以保留英文）
- `00-02-idea-open-questions.md` -- （仅在存在关键歧义时生成）

## 工作流

### Step 1: 整理候选结论

读取 idea pool 与 evaluation，归纳：
- 哪个 idea 最适合作为主选
- 哪些 idea 适合作为备选
- 哪些 idea 虽然新，但当前不值得做

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查推荐计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 idea recommendation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    Evaluation: {00-01-idea-evaluation.md 内容摘要}
    执行计划: 综合评分结果选出主选与备选，给出 story framing

    检查：要点见 codex-review-template.md
```

### Step 3: 形成推荐结论

参考 `skills/shared/idea-recommendation-template.md` 输出：
- 主选 idea
- 备选 idea（1-2 个）
- 不推荐项及原因
- 推荐理由摘要
- 建议的 story framing：是什么 / 为什么 / 怎么做

要求：
- 不是简单选最高分，而是综合 novelty、可做性、实验成本、venue fit、叙事完整度
- 若主选 idea 仍有关键不确定性，必须明确写入 open questions
- framing 必须足够具体，能够直接喂给 `/01-paper-init`

### Step 4: 生成待确认问题（如需要）

如果存在关键歧义，生成 `00-02-idea-open-questions.md`，列出：
- 待确认选择
- 不同选择的影响
- 对后续 story / venue / experiments 的影响

### Step 5: Post-review

调用 `mcp__codex__codex` 检查推荐是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下 idea recommendation 是否合理：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}
    Recommendation: {00-02-idea-recommendation.md}

    检查：要点见 codex-review-template.md
```

### Step 6: 输出确认

输出：
- `00-02-idea-recommendation.md` 已生成
- 若存在关键歧义，提示先确认 `00-02-idea-open-questions.md`
- 否则提示下一步：`/01-paper-init`
