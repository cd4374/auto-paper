---
name: "00-02-idea-recommend"
description: "基于 idea 池与评估结果推荐主选方向，并给出进入 story 的 framing。"
allowed-tools: Read, Write, Shell
---

# 00-02-idea-recommend

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex CLI.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

基于 `00-00-idea-pool.md` 与 `00-01-idea-evaluation.md`，生成 `00-02-idea-recommendation.md`。

## 输入

- `00-00-idea-pool.md`
- `00-01-idea-evaluation.md`

## 输出

- `00-02-idea-recommendation.md` -- 主要语言用中文，专业术语首次出现时用中文并括号标注英文原文。
- `00-02-idea-open-questions.md` -- 仅在存在关键歧义且影响主线决策时生成。

## 写作原则

推荐文件是**方向决策的终点**——精炼、果断、可直接驱动下一阶段。具体要求：

- **全文控制在 800-1500 字**：这是一个决策摘要，不是综述报告。
- **结论先行**：开篇一段话给出主选方案和决策逻辑。
- **Framing 是核心交付物**：Story Framing 必须足够具体，可直接作为 `/01-paper-init` 的输入。这是整份文件最有价值的部分。
- **不重复前序内容**：不要复述 idea pool 或 evaluation 中已有的分析。只写决策和 framing。
- **对关键不确定性显式记录**：若主选方案有决定性未知因素，写入 open questions。不生成 open questions 文件是正常的。

## 工作流

### Step 1: 综合前序分析

读取 idea pool 与 evaluation，形成判断：
- 主选方向是什么？为什么不是其他候选？
- 备选方向保留哪个？什么触发条件下切到备选？
- 哪些方向明确放弃？

### Step 2: Pre-review

调用 `codex exec` 检查推荐逻辑：

```bash
codex exec -c model="gpt-5.5" << 'EOF'
请检查以下 idea recommendation 计划是否合理：

Idea Pool: {00-00-idea-pool.md 内容摘要}
Evaluation: {00-01-idea-evaluation.md 内容摘要}
执行计划: 综合前序分析，选出主选与备选，输出精炼的决策文件和可直接进入 story 的 framing

检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
EOF
```

### Step 3: 形成推荐结论

输出结构（紧凑型）：

```
# Idea Recommendation

## 决策

[一段话：主选什么、备选什么、放弃什么、核心决策逻辑]

## 为什么

[1-2 段：选定主选方向的关键理由——不是重复 evaluation，而是综合权衡后的最终判断。覆盖：]
- 这个方向的核心吸引力（novelty 方向 + 理论洞察 + 可验证性）
- 与备选相比为什么胜出
- 最大风险和应对方向

## 备选

[1 段：备选方向是什么，什么情况下启用]

## 不推进

[一行一个，被淘汰的方向 + 一句话原因]

## Story Framing

[2-3 段紧凑叙述，直接可喂给 /01-paper-init：]

### 核心研究问题
[1 段：要回答什么问题，边界在哪。不展开背景。]

### 为什么值得做
[1 段：做成了会改变什么理解。不写"填补空白"。]

### 怎么做
[1 段：切入角度 + 关键探索步骤（2-3 步） + 每一步验证什么假设。不需要详细实验计划。]

## Next Step

- `/01-paper-init`
```

要求：
- 对计算/理论/数值模拟导向，优先选"理论机制明确 + 数值模拟可验证"的方向
- Framing 不留"需要进一步明确"的尾巴——所有关键决策必须在 00 阶段完成
- 主选方向的关键不确定性显式写出

### Step 4: 记录关键歧义（如需要）

如果存在影响主线决策的关键歧义，在 `00-02-idea-open-questions.md` 中记录：
- 歧义点
- 系统默认选择
- 对后续 stage 的影响

不生成此文件是正常的。

### Step 5: Post-review（迭代循环，最多 10 轮）

调用 `codex exec` 检查推荐质量：

```bash
codex exec -c model="gpt-5.5" << 'EOF'
请检查以下 idea recommendation：

Idea Pool: {00-00-idea-pool.md}
Evaluation: {00-01-idea-evaluation.md}
Recommendation: {00-02-idea-recommendation.md}

检查：是否覆盖上游要求？是否自洽？有无遗漏或过度扩展？
额外检查：文件是否精炼（800-1500 字）？决策是否果断？Framing 是否具体到能直接用于 story？是否只有方向性内容而非过度展开？

若有问题，明确指出并给出修改建议。
EOF
```

迭代逻辑：
- 若 review 指出问题 → 修改 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：打印每轮通过/问题数和问题摘要。

### Step 6: 输出确认

输出：
- `00-02-idea-recommendation.md` 已生成
- 若存在关键歧义，输出 `00-02-idea-open-questions.md`
- 一段话总结推荐结论
- 提示下一步：`/01-paper-init`
