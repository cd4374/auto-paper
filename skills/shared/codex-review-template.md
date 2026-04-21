# Codex Review 模板

所有生成/修改文件的 skills 必须在关键步骤前后调用 Codex review，确保质量。

## Review 类型

| 类型 | 时机 | 目的 |
|------|------|------|
| Pre-review | 执行前 | 检查计划是否覆盖必要输入、是否符合上游约束 |
| Post-review | 执行后 | 检查输出是否自洽、是否与上游文件一致 |

## 统一格式（精简版）

### Pre-review

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    检查以下执行计划：{计划内容}
    要点：是否覆盖上游要求？是否有冲突/遗漏？输出范围是否合理？
```

### Post-review

```
mcp__codex__codex:
  model: gpt-5.4
  prompt: |
    检查以下输出：{输出内容}
    要点：是否覆盖上游要求？是否自洽？有无过度扩展？格式是否规范？
```

## 各 Skill Review 触发点

| Skill | Pre-review 触发点 | Post-review 触发点 |
|-------|-------------------|-------------------|
| 00-00-idea-brainstorm | 读取研究方向后，生成 idea 前 | 生成 00-00-idea-pool.md 后 |
| 00-01-idea-evaluate | 读取 idea pool 后，评估前 | 生成 00-01-idea-evaluation.md 后 |
| 00-02-idea-recommend | 读取 evaluation 后，推荐前 | 生成 00-02-idea-recommendation.md 后 |
| 01-paper-init | 读取 idea recommendation 后，生成 story 前 | 生成 01-story.md 后 |
| 02-paper-journal | 读取 story 后，推荐前 | 生成 02-journal-requirements.md 后 |
| 03-00-paper-structure | 读取 story + requirements 后，设计章节前 | 生成 03-00-structure.md 后 |
| 03-01-paper-bibliography | 读取 structure 后，检索前 | 生成 references.bib 后（related work 可单独 review） |
| 03-02-paper-theory-analysis | 读取 structure + related work 后，分析前 | 生成 03-02-theory-analysis.md 后 |
| 04-00-experiment-design | 读取 theory analysis 后，设计实验前 | 生成 04-00-experiments.md 后 |
| 04-01-experiment-implement | 读取 experiment design 后，实现前 | 实现完成后 |
| 04-02-experiment-run | 读取实现代码后，运行前 | 收集结果后 |
| 04-03-experiment-analysis | 读取结果后，分析前 | 生成 04-03-experiment-analysis.md + 图表后 |
| 05-paper-write | 每章撰写前读取 structure，撰写后 review（已有设计） | 同上 |
| 06-paper-review | 读取 05-template 后，审查前 | 生成 report.md 后 |
| 06-01-review-assess | 读取外部 review 后，评估前 | 生成 action-plan 后 |
| 06-02-review-apply | 读取 action-plan 后，修改前 | 修改完成后 |
| 07-paper-compile | 检查 LaTeX 完整性后，编译前 | 编译成功后检查 PDF |

## Review 结果处理

- 如果 Pre-review 发现问题：暂停执行，向用户确认或调整计划
- 如果 Post-review 发现问题：根据问题严重程度决定是否立即修正，或记录到 open-questions.md
- 所有 review 发现的问题必须在下一阶段前解决，不得遗留