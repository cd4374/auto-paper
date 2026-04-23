---
name: "05-paper-write"
description: "[DEPRECATED] 请使用 /05-01 → /05-02 → /05-03"
allowed-tools: Bash, Read, Write
---

# 05-paper-write（兼容入口）

本 skill 已拆分为三个子 skill。

## 编排顺序

1. `/05-01-paper-template` → 生成模板
2. `/05-02-paper-write` → 撰写章节
3. `/05-03-paper-gate` → 最终检查

## 失败传播

| 阶段 | 失败处理 |
|------|---------|
| 05-01 失败 | 提示用户确认后可继续 |
| 05-02 失败 | 显示失败章节 + 建议回退到对应上游补齐 |
| 05-03 失败 | 显示 check-failures.md + 建议回退到 05-02 修复 |

## 使用方式

**方式一**：按顺序执行三步
```
/05-01-paper-template
/05-02-paper-write
/05-03-paper-gate
```

**方式二**：直接执行本 skill，自动编排三步

## 原则

本 wrapper 只做编排，不复制子 skill 逻辑。
