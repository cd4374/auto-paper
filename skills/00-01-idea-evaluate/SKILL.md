---
name: "00-01-idea-evaluate"
description: "对候选 idea 池做结构化评估，并对 top-k 想法做 novelty 与 paperability 风险审查。"
allowed-tools: Read, Write, mcp__kimi-code__kimi_web_search, mcp__kimi-code__kimi_fetch_url, mcp__MiniMax__web_search, WebSearch, WebFetch, mcp__codex__codex
---

# 00-01-idea-evaluate

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

对 `00-00-idea-pool.md` 做结构化评分，并生成 `00-01-idea-evaluation.md`。

## 输入

- `00-00-idea-pool.md`
- 可选：用户补充偏好（偏快出结果、偏计算/理论/数值模拟、偏顶会、偏低算力）

## 输出

`00-01-idea-evaluation.md` -- 主要语言用中文，专业术语保留英文。

## 写作风格（重要）

评估报告必须**读起来像一个有经验的研究者在做判断**，而不是在填评分表。具体要求：

- **用讨论代替打分**：不生成评分矩阵。对于每个 idea，用一段话给出你的判断——它好在哪、弱在哪、你担心什么、你觉得值得赌吗。判断可以是一个综合结论，不需要拆成 8 个维度各写一句。
- **思考过程透明化**：写出你形成判断的推理链。例如："I03 的 novelty 看起来不错，但我查了一圈发现 XX 等人去年已经做了非常接近的事，所以真正的 delta 可能是 YY，这比最初想的要小。不过换个 framing 也许还能救。"这种推理本身比结论更有价值。
- **比较才有意义**：评估不是每个 idea 独立打分然后排序。要把几个 idea 放在一起比较——"I01 和 I04 都在做 XX 方向，但 I01 的方法路径更清晰，I04 虽然更 ambitious 但第一个实验设计就不太对"。
- **宁可尖锐不要平庸**：如果你觉得某个 idea 就是不行，直接说为什么不行，不要用"具有一定的局限性""建议进一步探索"这种话缓冲。如果你觉得某个 idea 非常值得做，也直接说。
- **中文自然流畅**：和 brainstorm 阶段一样，用口语化的中文写。短句，直接，像在讨论而不是在汇报。
- **篇幅由内容决定**：一个 idea 的评估可以 80 字也可以 400 字。关键是信息密度，不是均匀分布。

## 工作流

### Step 1: 阅读 idea pool

读取 `00-00-idea-pool.md`，理解每个 idea 的核心问题和关键 claim。后续评估围绕这些展开，不需要重新摘要一遍。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查评估计划：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea evaluation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    执行计划: 对全部候选做叙述性评估（不生成评分表），选出 top-k 做 novelty 深查

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 3: 叙述性评估所有候选

对全部候选做评估。**不生成评分表**——用自然段落给出判断。

输出结构：

```
## 评估总览

[一段话概括这批 idea 的整体质量、主要亮点、共性问题。读者读完应该知道这批 idea 大概在什么水平。]

## 各 idea 评估

### I01: [标题]
[1-3 段叙述性评估，覆盖：novelty 判断、可做性、实验成本、理论潜力、模拟可复现性、paperability。不是每个维度都要写——重点写这个 idea 最突出和最成问题的维度。结论方向明确：推进 / 观望 / 放弃。]

### I02: [标题]
[同上]

...
```

评估要点：
- 不要只看"听起来新不新"——要看能不能形成可验证的 claim
- 对计算/理论/数值模拟导向，默认重视理论潜力和模拟可复现性
- 明显不成立或不适合当前约束的 idea 直接标记"放弃"并写清原因
- 把相关的 idea 放在一起比较，指出它们之间的差异和相对优劣

### Step 4: 深度审查 top-k

选出最值得推进的 top-k（默认 3 个）idea，做更深入的新颖性审查：

- 提炼每个 idea 最需要成立的 2-4 个核心 claim
- 按优先级检索最近相关工作：`mcp__kimi-code__kimi_web_search` → `mcp__MiniMax__web_search` → `WebSearch`；仅当前一工具不可用时才降级
- 抓取页面细节：`mcp__kimi-code__kimi_fetch_url` → `WebFetch`
- 记录 closest prior work、true delta、reviewer attack points

每个 deep review 输出：

```
### Ixx 深度审查

[一段话综述这个 idea 的 novelty 处境]

**最接近的工作：**
- [工作 1]：[简述 + 与我们的差异]
- [工作 2]：[简述 + 与我们的差异]

**真正的增量在哪：**
[一段话分析——去掉已有工作之后，我们还剩下什么新的东西]

**Reviewer 会攻击什么：**
[从最致命到最轻微的 2-4 个潜在攻击点，以及是否可以提前防御]

**结论：**
[novelty 是否成立？如果不成立但值得做，原因是什么？]
```

要求：
- novelty 深查只覆盖 top-k，不要对所有 idea 做
- 如果轻量评估阶段已能明确淘汰多数候选，deep review 可收缩到 1-3 个
- 如果发现"其实不新"，诚实记录，同时分析是否通过 framing 或 finding 差异仍有 paperability

### Step 5: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查评估质量：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea evaluation 是否合理：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
    额外检查：评估读起来是否像一个有经验的研究者的真实判断，还是像自动生成的评分报告？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 修改 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况。

### Step 6: 输出确认

输出：
- `00-01-idea-evaluation.md` 已生成
- 用一段话总结：主推什么、淘汰了什么、关键理由
- 提示下一步：`/00-02-idea-recommend`
