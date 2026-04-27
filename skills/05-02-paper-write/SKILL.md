---
name: "05-02-paper-write"
description: "按章节撰写论文 LaTeX"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, mcp__codex__codex
---

# 05-02-paper-write

按 `03-00-structure.md` 逐章撰写论文。

## 接口契约

```
Preconditions(required):
  - 05-template/ 目录存在
  - 04-03-experiment-analysis.md 含 Story Claim Coverage
Inputs(required):
  - 01-story.md
  - 02-journal-requirements.md
  - 03-00-structure.md
  - 03-01-related-work.md
  - 03-01-references.bib
  - 03-02-theory-analysis.md
  - 04-03-experiment-analysis.md
Inputs(optional):
  - 04-03-paper-assets/
Outputs: 05-template/sections/*.tex
Failure(阻塞): 回退到 03-02 或 04-03
Failure(非阻塞): 用户确认后继续
```

## Step 0: 进入条件检查

**必须满足以下条件**：
1. `04-03-experiment-analysis.md` 已存在且包含 `## Story Claim Coverage`
2. 所有核心 story claim 均有实验支撑，或已在 `04-03-story-gap.md` 记录并确认

若不满足，**阻塞并返回上游补齐**，不得跳过。

## Step 1: Pre-review

调用 Codex 检查撰写准备：
```
检查 Story、Structure、Related Work、Theory Analysis、Experiment Analysis、Journal Requirements
```

## Step 2: 逐章撰写

按 `03-00-structure.md` 章节顺序**串行**撰写。

**章节间跳转规则**：
- 章节顺序与章节集合以 `03-00-structure.md` 为唯一依据（该文件由 `/03-00-paper-structure` 基于 `venue-requirements.json` 生成）
- 不允许在 05-02 中硬编码通用顺序（如 Abstract → Introduction → Related Work → Method → Experiments → Conclusion）
- 若 `03-00-structure.md` 与当前写作目标不匹配，先回退更新 `03-00-structure.md`，再继续撰写
- 只有在前置章节完成后，才撰写依赖它的后续章节
- 不支持并行撰写：每章必须完成 Pre-review 后再进入下一章

**每章流程**：
1. 读取该章叙事内容
2. 相关工作优先用 `03-01-related-work.md`
3. 方法/理论/实验优先用 `03-02-theory-analysis.md`
4. 实验 claim 强度、limitations 必须以 `04-03-experiment-analysis.md` 为准
5. 只用 `04-03-experiment-analysis.md` 中标注"可直接用于论文"的图表
6. 撰写完整 LaTeX（非占位符）
7. 调用 Codex review（见 Step 3）

**写作原则**：
- 只写 structure 明确要求的内容
- "少而实"分节：1-2 段默认并入父节

**写作要点**：
- Abstract: what/why/how/evidence/result
- Introduction: hook + gap + approach + contributions
- Related Work: 按类别组织
- Method: 符号 + 公式 + 算法
- Experiments: setup → results → ablation → analysis
- Conclusion: 总结 + 局限 + 未来

## Step 3: 每章 Post-review（迭代最多 10 轮）

撰写完成后调用 Codex 审查章节内容。

**迭代逻辑**：
- 通过 → 进入下一章
- 问题 → 修改 → 继续 review（round++）
- 达到 10 轮上限仍未通过 → **阻塞**，记录问题到用户，回退上游补齐

**每轮情况汇总**：每章 review 循环结束后，打印每轮的简要情况：
- 第 1 轮：通过 / 问题数：N，问题摘要：...
- 第 2 轮：通过 / 问题数：N，问题摘要：...
- ...

## 输出

完成后提示：
```
所有章节已撰写。下一步：/05-03-paper-gate
```
