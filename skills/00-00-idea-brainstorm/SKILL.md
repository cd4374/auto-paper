---
name: "00-00-idea-brainstorm"
description: "围绕研究方向进行头脑风暴，生成结构化候选 idea 池。"
allowed-tools: Read, Write, mcp__codex__codex
---

# 00-00-idea-brainstorm

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

围绕用户给定的研究方向、约束与偏好，生成 `00-00-idea-pool.md`。

## 输入

- 用户描述的研究方向/主题
- 可选约束：
  - 算力/时间预算
  - 偏计算 / 偏理论 / 偏数值模拟（或偏实验）
  - 目标 venue
  - 已有数据、代码、实验资产

## 输出

`00-00-idea-pool.md` -- （主要语言要用中文，名词等专业用语可以保留英文）

## 工作流

### Step 1: Pre-review

调用 `mcp__codex__codex` 检查生成计划是否合理：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea brainstorming 计划是否合理：

    研究方向: {用户描述的研究方向}
    约束条件: {算力/时间/偏好等约束}
    执行计划: 生成 6-12 个候选 idea，每个包含 problem/motivation/insight/method/contribution/risks

    检查：要点见 codex-review-template.md
```

### Step 2: 生成候选 idea 池

参考 `skills/shared/idea-pool-template.md`，生成 6-12 个候选 idea。

每个 idea 至少包含：
- problem
- motivation
- core insight
- minimal method
- expected contribution
- required experiments
- likely venue
- main risks

要求：
- 候选之间要有清晰差异，不要只做措辞改写
- 默认优先生成“计算/理论/数值模拟”导向的 idea（可形成 theory → simulation 的最小闭环）
- 每个 idea 都必须能落到最小实验包（优先数值模拟可验证）
- 对明显依赖大规模数据采集或重工程实现、且缺少理论增量的方向，降权并写明原因
- 若某个 idea 明显依赖不存在的数据、算力或理论前提，要直接写入风险

### Step 3: Post-review（迭代循环，最多 10 轮）

调用 `mcp__codex__codex` 检查 idea pool 质量：

```
mcp__codex__codex:
  model: gpt-5.5
  prompt: |
    请检查以下 idea pool 是否适合作为论文前置 brainstorming 输出：

    {idea pool 内容}

    检查：要点见 codex-review-template.md

    若有问题，明确指出并给出修改建议。
```

迭代逻辑：
- 若 review 指出问题 → 按 review 建议修改 idea pool → 继续 review（round++）
- 若 review 通过或达到轮数上限 → 结束

**每轮情况汇总**：review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...

### Step 4: 输出确认

输出：
- `00-00-idea-pool.md` 已生成
- 总结最值得评估的 3-5 个 idea
- 提示下一步：`/00-01-idea-evaluate`
