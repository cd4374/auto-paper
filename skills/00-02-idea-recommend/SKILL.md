---
name: "00-02-idea-recommend"
description: "基于 idea 池与评估结果推荐主选 idea、备选方案，并给出进入 story 的 framing。"
allowed-tools: Read, Write, mcp__codex__codex
---

# 00-02-idea-recommend

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于 `00-00-idea-pool.md` 与 `00-01-idea-evaluation.md`，生成 `00-02-idea-recommendation.md`。

## 输入

- `00-00-idea-pool.md`
- `00-01-idea-evaluation.md`

## 输出

- `00-02-idea-recommendation.md` -- （主要语言要用中文，名词等专业用语可以保留英文）
- `00-02-idea-open-questions.md` -- （仅在存在关键歧义且影响主线决策时生成）

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
  model: gpt-5.5
  prompt: |
    请检查以下 idea recommendation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    Evaluation: {00-01-idea-evaluation.md 内容摘要}
    执行计划: 综合评分结果选出主选与备选，给出 story framing

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 3: 形成推荐结论

按以下格式输出推荐结论：

```
# Idea Recommendation

## 主选方案
- Idea:
- 推荐理由:
- 理论-模拟闭环说明:
- 主要风险:

## 备选方案
### 备选 1
- Idea:
- 保留理由:
- 风险:

## 不推荐项
### Ixx
- 不推荐原因:

## Suggested Story Framing

### 核心问题
[我们想理解/探索什么问题]

### 探索路径
[我们从哪个角度切入？预期会发现什么]
- 探索1:
- 探索2:

### 关键发现（预期）
[我们预期会发现什么]
- 发现1:
- 发现2:

### 深层理解（预期）
[我们如何解释这些发现]
- 机制/原理:
- 理论框架:

### 贡献
[这个理解的价值]
- 理论贡献:
- 实践贡献:

## Next Step
- 建议进入 `/01-paper-init`
```

要求：
- 不是简单选最高分，而是综合 novelty、可做性、实验成本、venue fit、叙事完整度
- 对计算/理论/数值模拟导向用户，默认优先选择“理论机制明确 + 数值模拟可验证”的主选方案
- 若主选 idea 仍有关键不确定性，必须明确写入 open questions
- framing 必须足够具体，能够直接喂给 `/01-paper-init`

### Step 4: 记录关键歧义与系统默认决策（如需要）

如果存在关键歧义，优先由系统按当前目标与约束做默认决策，并在 `00-02-idea-open-questions.md` 记录：
- 歧义点与系统默认选择
- 该选择的影响
- 对后续 story / venue / experiments 的影响

### Step 5: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查推荐是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea recommendation 是否合理：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}
    Recommendation: {00-02-idea-recommendation.md}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 recommendation → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...

### Step 6: 输出确认

输出：
- `00-02-idea-recommendation.md` 已生成
- 若存在关键歧义，输出 `00-02-idea-open-questions.md` 并说明已采用的系统默认决策
- 提示下一步：`/01-paper-init`
