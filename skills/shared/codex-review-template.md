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
  model: gpt-5.5
  prompt: |
    检查以下执行计划：{计划内容}
    要点：是否覆盖上游要求？是否有冲突/遗漏？输出范围是否合理？
```

### Post-review

```
mcp__codex__codex:
  model: gpt-5.5
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
| 04-01-experiment-implement | 读取 experiment design 后，实现前 | 先验证入口/参数/输出路径，再调用 Codex review 代码是否支撑实验设计 |
| 04-02-experiment-run | 读取实现代码后，运行前 | 先检查实验完成约定输出，再调用 Codex review 结果是否达到预期 |
| 04-03-experiment-analysis | 读取结果后，分析前 | 先检查分析文档/图表/审查结论可回溯，再调用 Codex review 分析是否合理 |
| 05-02-paper-write | 每章撰写前读取 structure，撰写后 review | 同上 |
| 06-paper-review | 读取 05-template 后，审查前 | 生成 report.md 后 |
| 06-01-review-assess | 读取外部 review 后，评估前 | 生成 action-plan 后 |
| 06-02-review-apply | 读取 action-plan 后，修改前 | 修改完成后，调用 Codex review 修改是否遵循 action plan |

## Review 结果处理

- 如果 Pre-review 发现问题：暂停执行，向用户确认或调整计划
- 如果 Post-review 发现问题：根据问题严重程度决定是否立即修正，或记录到 open-questions.md
- 所有 review 发现的问题必须在下一阶段前解决，不得遗留

## 工具错误处理规范

### Codex Review 失败处理

| 场景 | 处理 |
|------|------|
| 无响应/超时 | 跳过该步，记录原因，继续执行；标注 `⚠️ Codex review 已跳过` |
| 连续 2 次失败 | 阻塞，提示用户检查服务状态；不得自动降级 |

### LaTeX 编译失败处理

| 工具 | 场景 | 处理 |
|------|------|------|
| `pdflatex` | 工具缺失 | 报错："请安装 MacTeX" |
| `bibtex` | 工具缺失 | 同上 |
| `latexmk` | 工具缺失 | 降级到手写编译链（最多3次循环）；标注 `⚠️ 使用 fallback 编译` |
| `pdfinfo` | 工具缺失 | 跳过页数检查，不阻塞 |

### 图片审查失败处理

| 场景 | 处理 |
|------|------|
| `mcp__kimi-code__kimi_read_media` 调用失败/超时 | 降级到 `mcp__MiniMax__understand_image`；标注 `⚠️ 已降级到 MiniMax` |
| `mcp__MiniMax__understand_image` 调用失败/超时 | 跳过，生成占位结论；标注 `⚠️ 待人工审查` |
| 图片文件不存在 | 报错，列出缺失文件；不继续 |

### 通用原则

1. **记录优先**：任何 fallback 都要记录原因和降级路径
2. **不静默跳过**：Codex review 跳过最多 1 次，连续失败必须报告用户
3. **不自动修复**：工具缺失类错误直接报错，不尝试安装