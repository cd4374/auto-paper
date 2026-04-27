---
name: "04-03-experiment-analysis"
description: "复核实验实现与结果，分析结论边界并生成论文可用图表资产（主入口，编排 04-03-01/02/03 子阶段）。"
allowed-tools: Bash, Read, Write, Edit, Glob, mcp__codex__codex, mcp__kimi-code__kimi_read_media, mcp__MiniMax__understand_image
---

# 04-03-experiment-analysis

- REVIEWER_MODEL = `gpt-5.5` — Model used via Codex MCP.
- MAX_POST_REVIEW_ROUNDS = 10 — Post-review 迭代轮数上限。

04-03 主入口：按子阶段完成实验复核、图表资产整理与 story 覆盖门控。

## 输入

- `01-story.md`（必须读取，用于 claim 覆盖度核查）
- `04-00-experiments.md`
- `04-01-experiment-code/`
- `04-02-experiment-results.md`
- `04-02-experiment-results/`
- `03-00-structure.md`
- `03-02-theory-analysis.md`（如已生成，用于 theory vs experiment 对照）

## 输出

- `04-03-experiment-analysis.md`（主要语言要用中文，名词等专业用语可以保留英文）
- `04-03-paper-assets/`（论文可直接引用的图、表、整理后的中间文件）
- `04-03-paper-assets/latex_includes.tex`（所有图表的 LaTeX 嵌入代码）
- `04-03-story-gap.md`（仅在覆盖缺口触发阻塞时生成）

## 子阶段编排

**执行约束（强制）**：必须按 `Stage A → Stage B → Stage C` 串行执行，禁止跳步、并行或只执行子集。若某阶段阻塞，必须先解决阻塞再进入下一阶段。

### Stage A: `/04-03-01-experiment-audit`

目标：复核实现是否忠实于设计、结果是否完整可信，并提炼 claim/theory 对应关系。

完成后应至少产出：
- `04-03-experiment-analysis.md` 初稿中的 `Summary`、`Experiment-by-Experiment Review`、`Theory vs Experiment` 结构化内容。

### Stage B: `/04-03-02-paper-assets`

目标：生成最小必要论文图表资产，并完成关键图图片审查。

完成后应至少产出：
- `04-03-paper-assets/`
- `04-03-paper-assets/latex_includes.tex`
- `04-03-experiment-analysis.md` 中 `Figure Review` 的可追溯结论。

### Stage C: `/04-03-03-story-coverage`

目标：执行 P0 Story Claim Coverage 门控，收敛最终分析文档并做 Post-review。

完成后应保证：
- `04-03-experiment-analysis.md` 含完整 `## Story Claim Coverage`。
- 若触发门控条件，生成 `04-03-story-gap.md` 并阻塞进入 `/05-02-paper-write`。

## 统一约束

- 只分析当前 story/structure 直接需要的结论；不扩展新故事线。
- 只保留论文写作所需的最小必要资产；优先复用已有结果，不重跑无关实验。
- 结果不理想不等于实验失败；关注证据是否足以支撑/削弱 claim。
- 图片审查优先 Kimi，失败再降级 MiniMax，并显式记录降级原因。

## 失败处理

- 实现路径不清楚、结果来源无法回溯：先向用户确认，不要自行假设。
- Story 覆盖门控触发：阻塞并回退到 `/01-paper-init`、`/03-02-paper-theory-analysis` 或 `/04-00-experiment-design`。

## 输出确认

完成后提示：
- `04-03-experiment-analysis.md` 与 `04-03-paper-assets/` 已生成
- 若无阻塞项，下一步：`/05-01-paper-template` 或 `/05-02-paper-write`（取决于模板是否已就绪）
- 若有阻塞项，先处理 `04-03-story-gap.md`