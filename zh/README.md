# Remember Aaron Swartz — 中文版 /zh/

> 当前阶段：Phase 1 — 骨架建立（2026-05-16）

## 概述

这是 Remember Aaron Swartz 中文版的子站骨架，位于 `/zh/` 目录下。

- 英文原站保留在根目录，未作改动。
- 中文版采用相同的技术栈（Jekyll）与档案结构。

## 翻译原则

- 保持原始内容、作者、日期、链接和档案结构不变。
- 仅翻译面向读者的页面文字、导航、说明与正文。
- 文件名中的日期前缀、front matter 字段名与键值（`type`、`layout`、`link`、`date`）保持原样。
- 外部 URL、作者名、图片路径、RSS 技术字段、代码变量名保持原样。
- 人名保留英文，首次出现时可附加中文译名。

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
- [ ] Phase 2：分批翻译 363 篇 memories 与 3 篇 statements
- [ ] Phase 3：集成测试、构建验证与发布

## 文件结构

```
zh/
├── index.html          # 中文版首页（骨架）
├── archive.html        # 归档页（占位）
├── about.html          # 关于本站
├── newpost.html        # 贡献回忆说明
├── README.md           # 本文件
├── memories/_posts/    # 待填充（Phase 2）
└── statements/_posts/  # 待填充（Phase 2）
```

## 参与贡献

欢迎通过 <https://github.com/rememberaaronsw/rememberaaronsw> 提交 Issue 或 Pull Request。
