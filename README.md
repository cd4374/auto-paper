# auto-paper

基于 Claude Code 的自动化论文生成工具。采用双层文档结构，确保叙事一致性。

## 目录结构

```
auto-paper/
├── README.md
├── skills/                          # Skills 目录（复制到 .claude/skills/）
│   ├── 01-paper-init/               # 生成 01-story.md
│   ├── 02-paper-journal/            # 推荐期刊
│   ├── 03-paper-structure/          # 生成 03-structure.md
│   ├── 04-00-experiment-design/     # 实验设计
│   ├── 04-01-experiment-implement/  # 实验代码实现
│   ├── 04-02-experiment-run/        # 运行实验并收集结果
│   ├── 05-paper-write/              # 撰写 LaTeX
│   ├── 06-paper-compile/            # 编译 PDF
│   └── shared/                      # 共享资源
│       ├── story-template.md
│       ├── structure-template.md
│       ├── codex-review-prompt.md
│       └── templates/               # 期刊模板
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
├── 04-00-experiments.md             # 生成：实验设计
├── 04-01-experiment-code/           # 生成：实验代码
├── 04-02-experiment-results.md      # 生成：实验结果
├── 04-02-experiment-results/        # 生成：原始输出、日志
├── 05-template/                     # 生成：当前项目 LaTeX
└── 06-output/                       # 生成：编译输出
    └── paper.pdf
```

## 工作流

```
/01-paper-init           → 生成 01-story.md
           ↓
/02-paper-journal        → 02-journal-recommendation.md + 02-journal-requirements.md
           ↓
/03-paper-structure      → 生成 03-structure.md
           ↓
/04-00-experiment-design → 生成 04-00-experiments.md
           ↓
/04-01-experiment-implement → 生成 04-01-experiment-code/
           ↓
/04-02-experiment-run    → 04-02-experiment-results.md + 04-02-experiment-results/
           ↓
/05-paper-write          → 填写 05-template/
           ↓
/06-paper-compile        → 06-output/paper.pdf
```

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
| ML期刊 | JMLR | 无限制 |
| 物理/复杂系统 | PRE, PRL, PRX, Chaos, NJP, JSTAT | 4-15页 |
| 数值计算 | JCP, CPC | 无限制 |
| 综合/跨学科 | Nature, Science | 8-10页 |

详见 `skills/shared/templates/venue-requirements.json`

设计注意：

1. **阶段命名规范**：项目是分阶段的，阶段有数字前缀（如 01、02、03），也有子阶段（如 04-00、04-01、04-02）。不止 skills，所生产的文件、文件夹都要有对应前缀，以便查看是哪个阶段。

2. **Skills 简洁性**：每个 skill 应保持简洁，不超过 150 行。