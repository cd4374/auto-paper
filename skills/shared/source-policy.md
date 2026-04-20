# Source Policy

## 数据库优先级（Ladder）

1. **DBLP** — 首选：含 venue、pages、editors，覆盖 ML/AI、物理、数学等大多数领域
2. **CrossRef** — 备用：适用于有 DOI 的正式出版物及 arXiv preprint（DOI = `10.48550/arXiv.{id}`）
3. **IEEE Xplore** — 通信/信号处理/硬件领域首选
4. **ACM DL** — 系统/软件/网络领域首选
5. **arXiv** — 仅用于以下情况：
   - 过去 6 个月内的最新工作（尚未正式发表）
   - 某篇论文只有 preprint 可获取

## 来源标识规则

- 正式出版物：标注 venue、年份、页码
- arXiv preprint：标注 arXiv ID、年份，标注 `[preprint]`
- 若两者均存在，引用正式版本，不引用 preprint

## 时间窗口策略

未指定年份范围时，默认：
- **基础工作**（2022 前）：正式出版物
- **近期工作**（2022–2024）：正式出版物优先
- **最新工作**（2024+）：可接受高影响力 arXiv preprint

## BibTeX 获取链

对每篇论文按以下顺序尝试：

1. **DBLP**：`curl -s "https://dblp.org/search/publ/api?q=TITLE+AUTHOR&format=json&h=3"`，提取 key 后获取 `.bib`
2. **CrossRef**：`curl -sLH "Accept: application/x-bibtex" "https://doi.org/{doi}"`
3. **[VERIFY]**：两者均失败时加 `% [VERIFY]` 标记，记录到 open-questions，禁止编造

## Venue 分层

按论文领域选用对应的分层表（详见 `venue-tiering.md`）：
- 默认先找 Tier A，再扩展到 Tier B
- 只有用户明确要求时才将 Tier A 作为硬过滤条件
