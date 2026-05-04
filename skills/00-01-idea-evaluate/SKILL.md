---
name: "00-01-idea-evaluate"
description: "对候选 idea 池做方向性评估与 novelty 审查。"
allowed-tools: Read, Write, mcp__kimi-code__kimi_web_search, mcp__kimi-code__kimi_fetch_url, mcp__MiniMax__web_search, WebSearch, WebFetch, mcp__codex__codex
---

# 00-01-idea-evaluate

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

对 `00-00-idea-pool.md` 做方向性评估，生成 `00-01-idea-evaluation.md`。

## 输入

- `00-00-idea-pool.md`
- 可选：用户补充偏好

## 输出

`00-01-idea-evaluation.md` -- 主要语言用中文，专业术语首次出现时用中文并括号标注英文原文。

## 写作原则

评估是**方向筛选**而非详细审查——目标是从 6-12 个候选中快速识别 2-3 个值得推进的方向。具体要求：

- **每个 idea 评估 1-2 段（100-250 字）**：给出方向性判断——novelty 大致处于什么水平、可做性如何、是否值得推进。不逐维度展开，不生成评分矩阵。
- **判断必须有依据**：每个结论附带简要推理链——"I03 的 novelty 方向受限，XX 等人（2025）已覆盖核心 setting，剩余增量不足以支撑一篇独立 paper"——而非"novelty 中等"。
- **横向比较**：将方向相近的 idea 放在一起比较，指出相对优劣。
- **结论明确**：每个 idea 给出清晰方向——推进 / 观望 / 放弃。放弃的 idea 一句话说明原因即可。

## 工作流

### Step 1: 读取 idea pool

理解每个 idea 的核心方向和关键 claim。不需要重新摘要。

### Step 2: Pre-review

调用 `mcp__codex__codex` 检查评估计划：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea evaluation 计划是否合理：

    Idea Pool: {00-00-idea-pool.md 内容摘要}
    执行计划: 对全部候选做方向性评估（不生成评分表），选出 top-k 做 novelty 方向检索

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
```

### Step 3: 方向性评估

对全部候选做精炼评估。**不生成评分表**。

输出结构：

```
## 评估总览

[一段话：这批 idea 的整体方向质量，主要亮点和共性问题]

## 各 idea 评估

### I01: [标题]
[1-2 段：novelty 方向判断 + 可做性 + 理论/模拟闭环可行性 + 结论（推进/观望/放弃）]

### I02: [标题]
[同上]

...
```

要点：
- 重点评估能否形成可验证 claim 和 theory → simulation 闭环
- 明显不成立的直接标记"放弃"，不展开
- 方向相近的 idea 放在一起比较差异

### Step 4: Novelty 方向检索（仅 top-k）

对评估为"推进"的 top-k（默认 2-3 个）做方向性 novelty 检索：

- 按优先级检索：`mcp__kimi-code__kimi_web_search` → `mcp__MiniMax__web_search` → `WebSearch`
- 抓取细节：`mcp__kimi-code__kimi_fetch_url` → `WebFetch`
- 目的：确认大方向是否已被覆盖，不做详尽的 prior work 列表

输出（每个 top-k idea 1 段）：

```
### Ixx 方向验证

[1 段：最接近的已有工作方向 + 我们的方向增量在哪 + 是否成立]
```

- 如果发现方向已被充分覆盖，标记为"观望"或"放弃"并写明原因
- 如果方向成立但增量有限，诚实记录并分析通过 framing 调整是否有出路

### Step 5: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查评估质量：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea evaluation：

    Idea Pool: {00-00-idea-pool.md}
    Evaluation: {00-01-idea-evaluation.md}

    检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
    额外检查：评估是否精炼？判断是否有明确依据？是否只给了方向性结论而非过度展开？

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 修改 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：打印每轮通过/问题数和问题摘要。

### Step 6: 输出确认

输出：
- `00-01-idea-evaluation.md` 已生成
- 一段话总结：主推方向、淘汰方向、关键理由
- 提示下一步：`/00-02-idea-recommend`
