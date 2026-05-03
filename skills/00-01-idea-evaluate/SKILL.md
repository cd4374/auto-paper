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

评估报告必须以**连贯的分析性叙述**呈现，而非评分矩阵或条目罗列。核心要求：

- **用分析代替打分**：不生成评分矩阵。对每个 idea，用连贯段落给出综合判断——其优势、不足、风险、是否值得推进。判断应基于各维度的综合权衡，而非逐维打分后加总。
- **推理过程透明**：写出形成判断的完整推理链。例如，I03 的 novelty 初看有吸引力，但检索发现 XX 等人（2025）已完成高度接近的工作，因此真正的增量仅限于 YY 条件下的边界扩展。这种推理本身比结论更有价值——后续阶段需要依赖这些推理来调整方向。
- **横向比较**：评估不应是对每个 idea 的孤立分析。将相关 idea 放在一起比较，指出差异和相对优劣——"I01 和 I04 面向相似问题，但 I01 的方法路径更明确，I04 目标更野心但首个实验设计即存在逻辑缺陷"。
- **判断明确**：对每个 idea 给出清晰结论方向。不应使用"具有一定的局限性""建议进一步探索"等模糊措辞缓冲判断。
- **篇幅由信息量决定**：一个 idea 的评估可以 80 字也可以 400 字。关键在于信息密度，而非均匀分布。

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
    额外检查：评估的推理链是否逻辑完整、可追溯？判断是否有明确依据？还是读起来像自动生成的评分报告？

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
