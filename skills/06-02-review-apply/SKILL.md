---
name: "06-02-review-apply"
description: "依据 review action plan 修改项目内容，并记录修改落实情况。"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 06-02-review-apply

- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 3 — Post-review 迭代轮数上限。

根据 `06-01-review-action-plan.md` 执行已经确认的修改，并记录落实情况。

## 输入

- `06-01-review-action-plan.md`
- 当前项目文件：
  - `01-story.md`
  - `03-00-structure.md`
  - `03-02-theory-analysis.md`
  - `04-00-experiments.md`
  - `04-01-experiment-code/`（涉及实现修改时参考）
  - `04-02-experiment-results.md`
  - `04-03-experiment-analysis.md`
  - `05-template/`
- `06-01-review-open-questions.md`（如存在，且已由用户确认）

## 输出

- 更新后的项目文件
- `06-02-review-resolution.md` — 每条 review 意见的最终落实记录（主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: 读取 action plan

读取 `06-01-review-action-plan.md`，只处理：
- `accept`
- `partial`

默认不处理：
- `reject`
- `defer`
- `confirm`（除非用户已明确确认）


### Step 2: Pre-review

调用 `mcp__codex__codex` 检查修改计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下修改计划是否合理：

    Action Plan: {06-01-review-action-plan.md accept/partial 项}
    项目文件: {01/03-00/03-02/04/05 文件列表}

    检查：要点见 codex-review-template.md
```

### Step 3: 按源头优先顺序修改

修改顺序：
1. `01-story.md`
2. `03-00-structure.md`
3. `03-02-theory-analysis.md`
4. `04-00-experiments.md`
5. `04-01-experiment-code/`（如涉及实现修改）
6. `04-02-experiment-results.md`
7. `04-03-experiment-analysis.md`
8. `05-template/`

只按 action plan 做外科手术式修改；不要顺手扩写正文、重组结构，或新增本轮未批准的实验与结论。

要求：
- 先改源头文件，再改 LaTeX
- 不要只在 `05-template/` 里头痛医头
- 如果 review 影响核心主张，必须先改 `01-story.md`
- 如果 review 影响章节组织，必须先改 `03-00-structure.md`
- 如果 review 指向理论假设、证明力度、理论表述边界或 theory–experiment mismatch，优先更新 `03-02-theory-analysis.md`，必要时再同步 `04-*` 与 `05-template/`
- 如果 review 指向实验不足，应先更新 `04-*` 再决定是否修改正文
- 如果 review 指向结果解释不充分、图表不足或 claim 证据边界不清，优先更新 `04-03-experiment-analysis.md`，不要直接改 `05-template/`
- 每条实际改动都应能回溯到某条 review item

### Step 4: 记录落实情况

生成 `06-02-review-resolution.md`：

```markdown
# Review Resolution Log

## Applied
- R1: 已修改，位置 ...

## Partially Applied
- R2: 仅修改了 ...

## Rejected
- R3: 未修改，原因 ...

## Pending
- R4: 待确认 ...
```

要求：
- 每条意见都要能在 resolution 中找到归宿
- 说明改动落到了哪些文件
- 若只部分落实，要说明为什么没有全部采用

### Step 5: Post-review（迭代循环，最多 3 轮）

调用 `mcp__codex__codex` 检查修改是否与 action plan 一致：

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    请检查以下修改是否严格遵循 review action plan：

    Action Plan: {06-01-review-action-plan.md}
    Updated Story/Structure/Theory/Experiments/Results: {updated files}
    Updated LaTeX: {05-template changes}
    Resolution Log: {06-02-review-resolution.md}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

### Step 6: 输出下一步建议

最后总结：
- 哪些意见已落实
- 哪些意见仅部分落实
- 哪些问题仍待用户确认

**如涉及实验修改/补实验**：
修改后需要重新运行实验：
```
/04-01-experiment-implement → /04-02-experiment-run → /04-03-experiment-analysis → /05-paper-write
```

**如涉及论文内容修改**：
```
/06-paper-review → /07-paper-compile
```
