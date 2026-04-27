# Plan: 整合 structure-template.md 到 venue-requirements.json

## 任务

将 `structure-template.md` 的内容整合到 `venue-requirements.json` 中，删除旧文件，修改 skill 基于配置生成结构。

## 步骤

### Step 1: 扩展 venue-requirements.json

为每个 venue 的 section 补充：
- `narrative_points`: 关键叙事要点（1-4 条）
- `requirements`: 结构化需求

### Step 2: 修改 03-00-paper-structure skill

1. 读取 `02-journal-requirements.md` 的 `venue_key`
2. 从 `venue-requirements.json` 读取 `section_structure`
3. 基于配置生成 `03-00-structure.md`
4. 移除对 `structure-template.md` 的引用

### Step 3: 修改其他引用 skill

- `05-01-paper-template`: 应用相同解析规则
- `project-import`: 应用相同解析规则

### Step 4: 清理文档

- 修改 README.md 移除模板引用
- 删除 `structure-template.md`

## 验收标准

- [x] venue-requirements.json 完整覆盖所有 venue
- [x] skill 不再依赖 structure-template.md
- [x] JSON 格式验证通过
