# 模板目录说明

本目录包含常用期刊/会议的 LaTeX 模板文件。采用**最小打包 + 按需下载**策略。

## 打包原则

只打包运行时必需且官方模板中不提供的文件：
- `.bst` 样式文件（官方bst通常需要从官方包安装）
- `.sty` 辅助宏包（若官方未提供独立版本）
- `main.tex` 示例入口（精简版，保留核心格式要求）

## 按需下载

当前仓库未为每个 venue 单独提供 `README.md`；如需下载清单，请参考本文件下方“文件清单”与对应官网说明。

## 通用下载命令

```bash
# NeurIPS 2026
wget https://neurips.cc/NeuralIPS2026/AuthorKit.tgz

# ICML 2025
wget https://icml.cc/2025/conference/papers/ICML2025_authorkit.tar.gz

# ICLR 2025
wget https://iclr.cc/ICLR2025/conference/papers/iclr2025.zip

# ACL/EMNLP 等
wget https://aclanthology.org/venues/{venue}/latex.zip

# APS 期刊（PRL/PRX/PRB/PRE）
tlmgr install revtex

# AIP 期刊（Chaos/JMP）
tlmgr install aip4

# Elsevier 期刊
tlmgr install elsarticle

# IOP 期刊（NJP/JSTAT）
tlmgr install iop
```

## 文件清单

| 目录 | 打包内容 | 需下载内容 | 状态 |
|------|---------|-----------|------|
| neurips/ | main.tex, neurips_2026.sty, checklist.tex | neurips_2026.pdf（官方指南）, natbst, 各年份样式文件 | 部分完整 |
| icml/ | main.tex, icml2025.sty, icml2025.bst, algorithm.sty, algorithmic.sty, example_paper.bib | icml2025.pdf（官方说明） | 部分完整 |
| iclr/ | main.tex, iclr2025_conference.sty, iclr2025_conference.bst, iclr2025_conference.bib, math_commands.tex | iclr2025_conference.pdf（官方说明） | 部分完整 |
| aaai/ | main.tex, aaai2026.sty, aaai2026.bst, aaai2026.bib | aaai2026.pdf（官方指南） | 部分完整 |
| aps/ | main.tex, apssamp.bib | revtex4-2.cls, apsrev4-2.bst（通过 tlmgr install revtex） | 需下载 |
| aip/ | main.tex, aip4-1.rtx, aipnum4-1.bst, revtex4-1.cls, ltxdocext.sty, ltxfront.sty, ltxgrid.sty, ltxutil.sty, revsymb4-1.sty | — | ✅ 完整 |
| elsevier/ | main.tex, elsarticle-harv.bst, example.bib | elsarticle.cls（通过 tlmgr install elsarticle） | 需下载 |
| iop/ | main.tex, iopjournal.cls | ioparts.bst, iopfmtnum.sty 等（通过 tlmgr install iop） | 需下载 |
| nature/ | main.tex, sn-jnl.cls, sn-*.bst | 更多 .cls 变体、sn-apacite.sty（SN官网下载） | 部分完整 |
| science/ | main.tex, scicite.sty, sciencemag.bst, science_template.bib, example_figure.* | AAAS 官方完整包 | 部分完整 |
