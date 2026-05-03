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

- `00-02-idea-recommendation.md` -- 主要语言用中文，专业术语保留英文。
- `00-02-idea-open-questions.md` -- 仅在存在关键歧义且影响主线决策时生成。

## 写作风格（重要）

推荐报告是一个**决策文件**——它要说清楚"我们选哪个、为什么、下一步怎么走"。必须果断、清晰、有说服力。具体要求：

- **结论先行**：开篇直接说主选方案是什么，不要先铺垫 500 字背景。
- **决策逻辑完整**：不是"因为评分高所以选它"，而是写出完整的决策链条——"我们选 I03 而不是 I01 是因为 X。I01 虽然 novelty 更好但 Y 在当前约束下做不了。I04 作为备选保留了 Z 的可能性。"读者应该能看到你是如何权衡的。
- **Framing 要能直接用**：Suggested Story Framing 的输出必须足够具体，可以直接喂给 `/01-paper-init`。不要写泛泛的"探索XX机制"——要说清楚具体从哪个角度切入、核心假设是什么、第一优先级验证什么。
- **对不确定性诚实**：如果主选方案有关键不确定性，不要藏着掖着。写出来："目前最大的未知是 X，如果 X 不成立，这个方向就得放弃。所以我们建议第一步先验证 X。"这就是 open questions 的价值。
- **中文自然，语气果断**：用"我们选 I03"而不是"建议考虑选择 I03"。用"I01 做不了因为 X"而不是"I01 在可行性方面存在一定的挑战"。

## 工作流

### Step 1: 综合前序分析

读取 idea pool 与 evaluation，形成判断：
- 主选方案是什么？为什么不是其他候选？
- 备选方案保留哪个？什么情况下需要切到备选？
- 哪些 idea 明确不推进？原因一句话说清。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查推荐逻辑：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea recommendation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    Evaluation: {00-01-idea-evaluation.md 内容摘要}
    执行计划: 综合前序分析，选出主选与备选，输出可直接进入 story 的 framing

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 3: 形成推荐结论

按以下结构输出。**这是内容指引，不是模板——用叙事段落写，不要分条罗列**：

```
# Idea Recommendation

## 决策总览

[一段话：我们选什么、为什么、备选是什么、放弃什么。读者读完这段就应该知道结论。]

## 为什么选 [主选 idea]

[2-4 段叙述。不是重复 evaluation 里的评分——是综合所有信息之后做出的判断。覆盖：]
- 这个 idea 的核心吸引力是什么（novelty + 理论洞察 + 可验证性）
- 与备选和其他候选相比，为什么它胜出
- 理论→模拟闭环的可行性：什么可以推导、什么可以用数值实验验证、闭环是否完整
- 最大的风险和我们的应对策略

## 备选：[备选 idea]

[1-2 段。什么情况下需要回到备选？备选保留了主选没有覆盖的什么可能性？]

## 不推进

[一段话或一个简短列表。每个被淘汰的 idea 一句话说清原因。不用展开——读者不会关心为什么不选 I07。]

## Story Framing

[这是最重要的输出——直接决定了 01-story.md 的质量。用 3-5 段的叙事把以下问题讲清楚：]

### 核心研究问题

我们到底要回答什么问题？边界在哪？不回答什么？

这不是"研究目标"或"contribution statement"——是让读者（和你自己）一眼看清这个 paper 的 intellectual core。

### 为什么值得做

不写"填补空白"。写清楚：如果我们做成了，我们对这个问题的理解会发生什么变化？目前大家卡在哪？我们的切入为什么可能打破僵局？

### 怎么做

从哪个角度切入？核心方法路径是什么？有哪几个关键探索步骤？它们的优先级和依赖关系是什么？

这里不是详细的实验计划——是让读者（和后续阶段的自己）理解"先试什么、再试什么、每一步验证什么假设"的路线图。

## Next Step

- `/01-paper-init`：将 framing 固化为 story
```

要求：
- 不是简单选最高分——综合 novelty、可做性、实验成本、venue fit、叙事完整度做决策
- 对计算/理论/数值模拟导向，优先选"理论机制明确 + 数值模拟可验证"的方案
- 主选方案的关键不确定性必须明确写入（如果需要，同时生成 `00-02-idea-open-questions.md`）
- Framing 必须具体到可以直接喂给 `/01-paper-init`——不要留"需要进一步明确"的尾巴

### Step 4: 记录关键歧义（如需要）

如果存在影响主线决策的关键歧义，在 `00-02-idea-open-questions.md` 中记录：
- 歧义是什么
- 系统采取的默认选择
- 该选择的影响范围
- 对后续 story / venue / experiments 的后果

不生成 open questions 文件是正常的——大部分情况下默认决策就够了。只在歧义真正影响决策时才生成。

### Step 5: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查推荐质量：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea recommendation 是否合理：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}
    Recommendation: {00-02-idea-recommendation.md}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
    额外检查：推荐是否果断清晰？Framing 是否具体到能直接用于写 story？读起来像决策文件还是像自动生成的模板？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 修改 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况。

### Step 6: 输出确认

输出：
- `00-02-idea-recommendation.md` 已生成
- 若存在关键歧义，输出 `00-02-idea-open-questions.md` 并说明系统默认决策
- 用一段话总结推荐结论和下一步
- 提示下一步：`/01-paper-init`
