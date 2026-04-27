# Report: 整合 structure-template.md 到 venue-requirements.json

## 任务完成

将 `structure-template.md` 的章节叙事模板内容整合到 `venue-requirements.json` 中。

## 完成的修改

### 1. venue-requirements.json 扩展

为 17 个 venue 的每个 section 添加：
- `narrative_points`: 关键叙事要点（数组）
- `requirements`: 结构化需求对象（word_count, figures, tables, equations, notes）

**覆盖的 venue**:
- AI conferences: NeurIPS, ICML, ICLR, AAAI
- Nature family: Nature, Science
- APS journals: PRE, PRX, PRB, PRL
- AIP journals: Chaos, JMP
- Elsevier journals: CN, JCP, CPC
- IOP journals: NJP, JSTAT

### 2. 03-00-paper-structure skill 修改

- 移除对 `structure-template.md` 的引用
- 新增读取 `venue-requirements.json` 的 Step 2
- 基于 venue 配置的 section_structure 生成章节

### 3. project-import skill 修改

- 更新 Step 5 说明，引用 `venue-requirements.json` 而非 `structure-template.md`

### 4. README.md 更新

- 移除 `structure-template.md` 的目录引用

### 5. 文件删除

- 删除 `structure-template.md`

## 验证

- JSON 格式验证通过
- 所有 17 个 venue 均已配置 section_structure
- skills 不再依赖已删除的模板文件
