# auto-paper

基于 Claude Code 的自动化论文生成工具。采用双层文档结构，确保叙事一致性。

## 目录结构

```
auto-paper/
├── README.md
├── skills/                          # Skills 目录（复制到 .claude/skills/）
│   ├── 01-paper-init/               # 生成 01-story.md
│   ├── 02-paper-journal/            # 推荐期刊
│   ├── 03-00-paper-structure/       # 生成 03-structure.md
│   ├── 03-01-paper-bibliography/    # 检索文献并生成参考文献初稿
│   ├── 04-00-experiment-design/     # 实验设计
│   ├── 04-01-experiment-implement/  # 实验代码实现
│   ├── 04-02-experiment-run/        # 运行实验并收集结果
│   ├── 04-03-experiment-analysis/   # 复核实现与结果，分析并生成图表资产
│   ├── 05-paper-write/              # 撰写 LaTeX
│   ├── 06-paper-review/            # 内部论文审查
│   ├── 06-01-review-assess/        # 外部 review 意见评估
│   ├── 06-02-review-apply/         # 按 review 方案修改
│   ├── 07-paper-compile/           # 编译 PDF
│   ├── project-import/             # 独立导入工具
│   └── shared/                      # 共享资源
│       ├── story-template.md
│       ├── structure-template.md
│       ├── codex-review-prompt.md
│       └── templates/               # 期刊模板（部分 venue 仅提供配置，模板需另行下载）
│           ├── venue-requirements.json
│           ├── neurips/
│           ├── icml/
│           ├── iclr/
│           ├── aaai/
│           ├── aps/
│           ├── aip/
│           ├── iop/
│           ├── elsevier/
│           ├── nature/
│           └── science/
│
├── 01-story.md                      # 生成：叙事逻辑
├── 02-journal-recommendation.md     # 生成：期刊推荐
├── 02-journal-requirements.md       # 生成：期刊要求明细
├── 03-structure.md                  # 生成：文章结构
├── 03-01-related-work.md            # 生成：related work 笔记
├── 03-01-references.bib             # 生成：参考文献初稿
├── 04-00-experiments.md             # 生成：实验设计
├── 04-01-experiment-code/           # 生成：实验代码
├── 04-02-experiment-results.md      # 生成：实验结果
├── 04-02-experiment-results/        # 生成：原始输出、日志
├── 04-03-experiment-analysis.md     # 生成：实验分析与结论边界
├── 04-03-paper-assets/              # 生成：论文可直接引用的图表资产
├── 05-template/                     # 生成：当前项目 LaTeX
├── 06-paper-review/                 # 生成：内部审查报告 + 修订日志
│   ├── report.md
│   └── revision-log.md
├── 06-01-review-feedback.md            # 生成：外部 review 意见整理
├── 06-01-review-action-plan.md         # 生成：review 修改方案
├── 06-01-review-open-questions.md      # 可选：待确认问题
├── 06-02-review-resolution.md          # 生成：review 落实记录
└── 07-output/                       # 生成：编译输出
    └── paper.pdf
```

## 工作流

```
/01-paper-init           → 生成 01-story.md
           ↓
/02-paper-journal        → 02-journal-recommendation.md + 02-journal-requirements.md
           ↓
/03-00-paper-structure   → 生成 03-structure.md
           ↓
/03-01-paper-bibliography → 生成 03-01-related-work.md + 03-01-references.bib
           ↓
/04-00-experiment-design → 生成 04-00-experiments.md
           ↓
/04-01-experiment-implement → 生成 04-01-experiment-code/
           ↓
/04-02-experiment-run    → 04-02-experiment-results.md + 04-02-experiment-results/
           ↓
/04-03-experiment-analysis → 04-03-experiment-analysis.md + 04-03-paper-assets/
           ↓
/05-paper-write          → 填写 05-template/
           ↓
/06-paper-review         → 默认生成 06-paper-review/report.md（可选：按用户要求同时修订论文）
           ↓
[可选：收到外部 review 后]
/06-01-review-assess     → 06-01-review-feedback.md + 06-01-review-action-plan.md
           ↓
/06-02-review-apply      → 更新 01/03/04/05 + 06-02-review-resolution.md
           ↓
/06-paper-review         → 再审查修订结果
           ↓
/07-paper-compile        → 07-output/paper.pdf
```

## 独立技能

- `/project-import`：解析一个现有研究项目（代码、实验结果、论文草稿、笔记），并尽可能转化为 auto-paper 的标准格式
- 它不是 01–07 正式阶段的一部分，而是一个导入/迁移工具
- 导入完成后，可根据恢复程度继续主流程；若 `01/02/03/04` 已较完整，通常可直接进入 `/05-paper-write`

## 03-01 文献检索子阶段

- `/03-01-paper-bibliography`：基于 `01-story.md`、`02-journal-requirements.md` 与 `03-structure.md` 做定向文献检索，生成 `03-01-related-work.md` 与 `03-01-references.bib`
- 它负责为 `/05-paper-write` 提供 Related Work 的材料基础与 BibTeX 初稿，但不替代正文写作

## 04 实验分析子阶段

- `/04-03-experiment-analysis`：复核 `04-01` 实现是否忠实于 `04-00` 设计，检查 `04-02` 结果是否完整可信，输出 `04-03-experiment-analysis.md` 与论文可直接引用的 `04-03-paper-assets/`
- 它负责把“原始跑数结果”整理为“可写入论文的分析结论、图表和限制说明”，供 `/05-paper-write` 直接使用
- 对准备进入论文的关键 figures，会额外使用图片理解 MCP 做可读性与表达审查，避免 panel 布局、标注、色条或科学表达引发 reviewer 困惑

## review 子阶段

- `/06-paper-review`：内部一致性与质量审查（默认生成 `report.md`，并在自检时生成 `self-check.md`；若用户明确要求，也可同时修订论文并更新 `revision-log.md`）
- `/06-01-review-assess`：判断外部 review 意见是否成立，并生成 `06-01-review-action-plan.md`
- `/06-02-review-apply`：依据 action plan 修改 `01/03/04/05` 层内容，并生成 `06-02-review-resolution.md`

## 核心概念

### 双层文档结构

| 层级 | 文件 | 作用 |
|------|------|------|
| 叙事层 | 01-story.md | 定义论文的"故事"：是什么、为什么、怎么做 |
| 结构层 | 03-structure.md | 定义章节：每章叙事内容 + 需求（字数/图表）|

### 一致性保证

- **01-story.md 先行**：所有后续步骤以 story 为锚点
- **03-structure.md 锁定**：章节结构确定后，后续内容必须与之对齐
- **Codex review**：关键节点介入检查逻辑一致性
- **改稿规则**：先改 01/03，再同步内容

## 支持的期刊

| 领域 | 期刊 | 页数限制 |
|------|------|----------|
| ML会议 | NeurIPS, ICML, ICLR, AAAI | 7-10页 |
| 物理/复杂系统 | PRE, PRL, PRX, Chaos, NJP, JSTAT, JMP, Chaos, Solitons & Fractals | 4-15页或不限 |
| 数值计算 | JCP, CPC | 无限制 |
| 综合/跨学科 | Nature, Science | 8-10页 |

详见 `skills/shared/templates/venue-requirements.json`

设计注意：

1. **阶段命名规范**：项目是分阶段的，阶段有数字前缀（如 01、02、03），也有子阶段（如 04-00、04-01、04-02）。不止 skills，所生产的文件、文件夹都要有对应前缀，以便查看是哪个阶段。

2. **Skills 简洁性**：每个 skill 应保持简洁，不超过 150 行。