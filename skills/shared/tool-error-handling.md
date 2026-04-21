# Tool Error Handling

所有外部工具失败的标准 fallback 方案。不可跳过的记录要求。

## BibTeX 获取链

| 工具 | 失败场景 | Fallback | 产出要求 |
|------|---------|---------|---------|
| DBLP API | 限流/超时/无结果 | CrossRef → Semantic Scholar → `[VERIFY]` | 每步记录，失败加 `[VERIFY]` 标记 |
| CrossRef | 无DOI/超时 | arXiv search → `[VERIFY]` | 同上 |
| Semantic Scholar | 超时 | `[VERIFY]` | 只记录不尝试更多 |
| `curl` 执行失败 | 网络不可达 | 降级到 WebSearch/WebFetch | 标注数据来源 |

## 图片审查

| 工具 | 失败场景 | Fallback | 产出要求 |
|------|---------|---------|---------|
| `mcp__MiniMax__understand_image` | 调用失败/超时 | 跳过，生成占位结论 | 明确标注 `⚠️ 待人工审查` |
| 图片文件不存在 | 路径错误 | 报错，列出缺失文件 | 不继续 |

## Codex Review

| 工具 | 失败场景 | Fallback | 产出要求 |
|------|---------|---------|---------|
| `mcp__codex__codex` | 无响应/超时 | 跳过该步，记录跳原因，继续执行 | 标注 `⚠️ Codex review 已跳过` |
| 连续 2 次失败 | 服务不可用 | 阻塞，提示用户 | 不得自动降级 |

## LaTeX 编译

| 工具 | 失败场景 | Fallback | 产出要求 |
|------|---------|---------|---------|
| `pdflatex` | 工具缺失 | 报错："请安装 MacTeX" | 阻塞，不尝试修复 |
| `bibtex` | 工具缺失 | 同上 | 同上 |
| `latexmk` | 工具缺失 | 降级到手写编译链（最多3次循环） | 标注 `⚠️ 使用 fallback 编译` |
| `pdfinfo` | 工具缺失 | 跳过页数检查，标注 | 不阻塞 |

## 通用原则

1. **记录优先**：任何 fallback 都要记录原因和降级路径
2. **不静默跳过**：Codex review 跳过最多 1 次，连续失败必须报告用户
3. **不自动修复**：工具缺失类错误直接报错，不尝试安装
4. **不降级到不可信来源**：BibTeX 获取链所有来源失败后，标记 `[VERIFY]` 而非用 WebSearch 凑合

## 各 Skill 环境检查入口

在每个 skill 的 Step 1（Pre-review）之前执行：

```
### Step 0: 环境检查
检查所需工具是否可用：
- 编译类：which pdflatex && which bibtex
- BibTeX获取：curl --version
- 图片审查：mcp__MiniMax__understand_image 自检
- Codex：mcp__codex__codex 自检

若不可用，阻塞并说明缺失工具和修复方法。
```
