# Remember Aaron Swartz — 中文版 /zh/

> 当前阶段：Phase 2A — 样本翻译与流水线设计（2026-05-16）

## 概述

这是 Remember Aaron Swartz 中文版的子站，位于 `/zh/` 目录下。

- 英文原站保留在根目录，未作改动。
- 中文版采用相同的技术栈（Jekyll）与档案结构。
- 当前已完成 3 篇样本翻译，全量翻译将在后续批次中逐步完成。

## 翻译原则

- 保持原始内容、作者、日期、链接和档案结构不变。
- 仅翻译面向读者的页面文字、导航、说明与正文。
- 文件名中的日期前缀、front matter 字段名与键值（`type`、`layout`、`link`、`date`）保持原样。
- 外部 URL、作者名、图片路径、RSS 技术字段、代码变量名保持原样。
- 人名保留英文，首次出现时可附加中文译名。
- Aaron Swartz 首次出现译为"亚伦·斯沃茨（Aaron Swartz）"，后续可用"亚伦"或"斯沃茨"。
- 引用类内容必须忠实原文，不扩写、不鸡汤化。

## 不要翻译的规则

| 类别 | 处理方式 |
|------|----------|
| 文件名 | 保持原文件名（含日期前缀） |
| Front matter 字段名 | 不翻译键名 |
| Front matter 值（type/layout/link/date） | 保持原值 |
| 外部 URL | 保留原始链接 |
| 作者名 | 保持原始拼写 |
| 图片路径/URL | 保持原路径 |
| RSS 技术字段 | 保持英文 |
| CSS/JS 类名 | 保持英文 |
| 许可证法律文本 | 保留英文原文，可附加中文说明 |

## 当前进度

- [x] Phase 1：建立 `/zh/` 骨架、模板、导航与说明页
- [x] Phase 2A：生成全量清单、翻译 3 篇样本、建立验证流水线
- [ ] Phase 2B：审查样本质量，commit + push 样本分支
- [ ] Phase 2C：小批量试翻译（最多 20 篇）
- [ ] Phase 3：集成测试、构建验证与发布

## Phase 2A 样本

| 日期 | 标题 | 类型 | 作者 | 路径 |
|------|------|------|------|------|
| 2013-01-12 | 他如此炽热地闪耀（He was so fiercely brilliant） | post | Patrick Schmitt | `zh/memories/_posts/2013-01-12-he-was-so-fiercely-brilliant.md` |
| 2013-01-12 | Cory Doctorow 悼念亚伦·斯沃茨 | quote | Cory Doctorow | `zh/memories/_posts/2013-01-12-cory-doctorow-aaron.md` |
| 2013-01-12 | 2012年5月21日，亚伦·斯沃茨在 Freedom to Connect 2012 大会主旨演讲后 | image | Family and friends of Aaron | `zh/memories/_posts/2013-01-12-freedom-to-connect.md` |

## 文件结构

```
zh/
├── index.html              # 中文版首页（含样本列表）
├── archive.html            # 归档页（含 3 篇样本）
├── about.html              # 关于本站
├── newpost.html            # 贡献回忆说明
├── README.md               # 本文件
├── data/
│   └── translation_inventory.json  # 全量翻译清单
├── memories/_posts/        # 中文 memories（3 篇样本已放入）
└── statements/_posts/      # 待填充（Phase 2C+）
```

## 参与贡献

欢迎通过 <https://github.com/rememberaaronsw/rememberaaronsw> 提交 Issue 或 Pull Request。
