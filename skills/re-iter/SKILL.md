---
name: "re-iter"
description: "通用迭代式工作流：需求→Plan→Review循环→实现→Review循环"
allowed-tools: Read, Write, Glob, Grep, Agent, mcp__codex__codex, mcp__MiniMax__understand_image
temporary-files: PLAN.md
---

# re-iter

通用迭代式工作流。分析需求 → 生成 Plan → 多轮 Review 改进 → 实现 → 多轮 Review 改进 → 完成。

## 参数

| 参数 | 说明 | 默认 |
|------|------|------|
| task | 任务描述 | 必填 |
| max_review_rounds | 最大 review 轮数 | 4 |
| output_prefix | 输出文件前缀 | `workflow/` |

## 工作流

### Phase 1: 需求分析

1. 读取用户任务描述，澄清范围与约束
2. 识别关键里程碑与验收标准
3. 估算工作量与风险

### Phase 2: Plan 生成与 Review 循环

**Step 2.1: 生成 Plan**

生成 `PLAN.md`，包含：
- 任务拆解（步骤清单）
- 资源/依赖
- 验收标准
- 风险点

**Step 2.2: Review Plan**

调用 Codex 审查 plan（最多 `max_review_rounds` 轮）：

```
mcp__codex__codex:
  model: kimi-k2.6
  prompt: |
    请审查以下 plan：

    任务: {task}
    计划: {plan}

    检查：
    1. 步骤是否完整、无遗漏
    2. 顺序是否合理
    3. 验收标准是否可操作
    4. 风险是否识别充分

    若有问题，明确指出并给出修改建议。
```

- 若有改进建议 → 更新 PLAN.md → 继续 review
- 若通过或达到轮数上限 → 进入 Phase 3

### Phase 3: 实现与 Review 循环

**Step 3.1: 按 Plan 执行**

按步骤执行，记录每个里程碑的输出。

**Step 3.2: Review 实现**

调用 Codex 审查实现（最多 `max_review_rounds` 轮）：

```
mcp__codex__codex:
  model: kimi-k2.6
  prompt: |
    请审查以下实现：

    任务: {task}
    计划: {plan}
    实际实现: {实现内容}

    检查：
    1. 是否忠实于 plan
    2. 质量是否达标
    3. 验收标准是否满足
    4. 有无遗漏或错误

    若有问题，明确指出并给出修改建议。
```

- 若有改进建议 → 按建议修改 → 继续 review
- 若通过或达到轮数上限 → 进入 Phase 4

### Phase 4: 输出

- 汇总实现结果
- 标注未解决的问题（如有）
- 提示后续步骤

## 输出文件

| 文件 | 说明 |
|------|------|
| `{output_prefix}PLAN.md` | 执行计划 |
| `{output_prefix}REPORT.md` | 最终报告 |

## 注意事项

- Review 是迭代的，每轮都要有实质改进才继续
- 若某轮无改进建议，直接通过
- 轮数上限是为了避免无限循环