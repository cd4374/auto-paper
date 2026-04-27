---
name: "04-03-03-story-coverage"
description: "执行 Story Claim Coverage 门控，收敛 04-03 分析文档并给出进入 05 的判定。"
allowed-tools: Read, Write, Edit, mcp__codex__codex
---

# 04-03-03-story-coverage

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

执行 04-03 的 P0 门控，判断是否可以进入论文写作阶段。

## 输入
- `01-story.md`
- `04-03-experiment-analysis.md`（需已包含实验审计与 Figure Review）

## 输出
- 更新 `04-03-experiment-analysis.md`（补全 `## Story Claim Coverage`）
- `04-03-story-gap.md`（仅在门控触发时）

## 工作流

### Step 1: 生成 Story Claim Coverage（必填）
按表格填写：
- Story Claim
- 支撑实验
- 支撑程度（支撑/部分支撑/不支持/无实验）
- 论文处理方式（直接引用/加限定词/移至 future work）

### Step 2: 执行门控判定
触发条件：若 ≥2 个核心 claim 为“不支持”或“无实验”。

若触发：
1. 生成 `04-03-story-gap.md`
2. 阻塞进入 `/05-02-paper-write`
3. 提示用户在以下路径中选择：
   - 回退 `/01-paper-init` 或 `/03-02-paper-theory-analysis`
   - 回退 `/04-00-experiment-design`
   - 放弃当前项目

若未触发：允许进入 05 阶段。

### Step 3: 收敛分析文档
确保 `04-03-experiment-analysis.md` 至少包含：
- `## Summary`
- `## Story Claim Coverage`
- `## Experiment-by-Experiment Review`
- `## Theory vs Experiment`
- `## Figure Review`
- `## Writing Notes`

### Step 4: Post-review（最多 10 轮）
调用 `mcp__codex__codex` 检查 coverage 判定与文档边界是否合理；有问题则迭代修订。

## 约束
- 门控是 P0 强制项，不得跳过。
- 不把证据不足的 claim 写成已被证实。