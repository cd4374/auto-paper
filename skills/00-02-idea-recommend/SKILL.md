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

推荐报告是一个**决策文件**——必须清晰阐述选择方案、决策依据和下一步路径。核心要求：

- **结论先行**：开篇直接给出主选方案，不做冗长铺垫。
- **决策逻辑完整且可追溯**：写出完整的权衡过程——选定 I03 而非 I01 的具体原因，I01 的 novelty 优势为何在当前约束下不可行，I04 作为备选保留了哪些可能性。决策链的每一步推理都应明确可查。
- **Framing 具体可操作**：Story Framing 的输出必须足够精确，可直接作为 `/01-paper-init` 的输入。不应停留在"探索 XX 机制"的粒度——需明确切入角度、核心假设、第一优先级验证目标。
- **对不确定性精确记录**：主选方案的关键不确定性必须显式记录。若某个假设不成立将导致方向放弃，应直接写出。这类记录即是 open questions 的核心内容。

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
    额外检查：推荐决策的推理链是否完整可追溯？Framing 是否具体到能直接用于写 story？叙事是否逻辑连贯而非模板填充？

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
