---
name: "project-import"
description: "解析现有研究项目并转化为 auto-paper 标准格式。"
allowed-tools: Bash, Read, Glob, Grep, Write, WebSearch, WebFetch, mcp__codex__codex
---

# project-import
- REVIEWER_MODEL = `gpt-5.4` — Model used via Codex MCP.

解析一个现有研究项目（代码、实验结果、论文草稿、笔记），并尽可能转化为 auto-paper 的标准产物。

## 输入

- 一个现有项目目录
- 可能包含：
  - 代码：`src/`, `code/`, `scripts/`, `train*`, `eval*`, `run*`
  - 结果：`results/`, `outputs/`, `logs/`, `figures/`, `tables/`
  - 论文：`*.tex`, `*.md`, `paper*`, `draft*`, `abstract*`
  - 配置/元数据：`README*`, `requirements.txt`, `environment.yml`, `pyproject.toml`, `*.yaml`, `*.json`

## 输出

尽可能生成：
- `01-story.md`
- `02-journal-recommendation.md`
- `02-journal-requirements.md`
- `03-structure.md`
- `04-00-experiments.md`
- `04-02-experiment-results.md`（仅在结果证据充足时）

如果信息不足，必须明确标注“待确认/缺失”，不要编造内容。

## 工作流

### Step 1: 项目普查
扫描并归类证据：
- narrative sources：abstract、introduction、conclusion、README、研究说明
- method sources：方法代码、模块命名、配置文件、算法说明
- experiment sources：训练/评测脚本、实验配置、命令行入口
- result sources：结果表、日志、图表、CSV/JSON 指标
- venue/template clues：LaTeX 模板、class/sty/bst、草稿中的会议信息

对每类证据标记：`high confidence` / `medium confidence` / `missing`。

### Step 2: 提炼 story
从现有项目恢复三问：
- **是什么**：解决什么问题？核心贡献是什么？
- **为什么**：为什么重要？已有方法有什么不足？
- **怎么做**：方法、系统或实验方案的核心思路是什么？

证据优先级：
1. 现有草稿中的 abstract / introduction / conclusion
2. README 或项目说明
3. 方法代码命名 / 配置命名
4. 图表标题 / 结果表格 / 日志摘要

必须区分“材料直接支持的结论”和“仅为合理推断的表述”。

### Step 3: 生成 `01-story.md`
参考 `../shared/story-template.md` 生成 `01-story.md`。

要求：
- 中文为主，保留必要英文术语
- 三问完整
- 不得把没有证据的推断写成既成事实

生成后调用 `mcp__codex__codex` 审查：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {"model_reasoning_effort": "xhigh"}
  prompt: |
    请检查以下导入得到的 story 是否严格基于现有项目证据：

    项目证据摘要: {evidence summary}
    Story: {story 内容}

    检查要点：
    1. 三问是否完整？
    2. 哪些表述有明确证据支持？
    3. 哪些表述只是合理推断？
    4. 是否存在超出原项目材料的编造式概括？
```

### Step 4: 推断或推荐 venue
优先从已有项目识别 venue：
- LaTeX 模板 marker
- class/sty/bst 文件
- 草稿文本中的会议/期刊痕迹

若不能识别，则根据 `../shared/templates/venue-requirements.json` 推荐 1-2 个候选。

生成：
- `02-journal-recommendation.md`
- `02-journal-requirements.md`

### Step 5: 生成 `03-structure.md`
参考 `../shared/structure-template.md` 生成 `03-structure.md`。

规则：
- 若已有论文草稿结构较完整，优先保留其章节框架
- 若没有现成结构，则回退到标准 5 章结构
- 每章叙事内容要能映射回 story
- 字数/图表/公式需求要考虑 venue 要求和现有材料量

### Step 6: 恢复 04 阶段材料
#### 6.1 生成 `04-00-experiments.md`
从训练/评测脚本、YAML/JSON 配置、日志、结果表格、图表 caption、草稿实验段中恢复：
- 实验名称
- 支撑的 claim
- 数据集
- baseline
- 指标
- ablation / robustness / generalization 检查

每个实验都应能追溯到现有文件证据；否则标为“推测/待确认”。

#### 6.2 条件性生成 `04-02-experiment-results.md`
只有在已有项目里存在清晰结果产物时才生成：CSV/JSON、图表、关键日志、草稿结果描述。证据不足则不要生成。

#### 6.3 不默认重建 `04-01-experiment-code/`
已有项目通常已包含代码，导入阶段只做映射和解释，不做代码重写。

### Step 7: 最终一致性检查
调用 `mcp__codex__codex` 检查导入结果是否超出原项目证据：

```
mcp__codex__codex:
  model: gpt-5.4
  config: {“model_reasoning_effort”: “xhigh”}
  prompt: |
    请检查以下导入结果是否超出原项目证据：
    导入结果摘要: {导入生成的内容}
    原项目证据: {evidence summary}
    检查要点：
    1. 每个主要 claim 是否有证据支撑？
    2. 每个实验是否能定位到脚本、配置或结果？
    3. 哪些内容应标记为”待确认”？
    4. 是否存在 silently fabricated content？
```

### Step 8: 输出导入总结
最后总结：
- 已生成哪些标准文件
- 哪些内容是 high confidence / medium confidence / missing
- 哪些 claim 或实验仍需用户确认
- 导入完成后建议从哪个阶段继续；若 `01/02/03/04` 恢复充分，通常可继续 `/05-paper-write`
