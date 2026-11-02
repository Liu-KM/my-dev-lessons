# my-dev-lessons

从 DeepSeek Harness（DSH）从零开始的开发历史中，学习开发技巧、工程决策和踩坑经验，并通过自己的实践，将它们整理成可复用的方法和工具。

这些 lessons 既是我学到的经验，也是教给我的 Agent 的课程：帮助我提升工程能力，让 Codex 等 Agent 更好地参与开发，减少 AI slop。

目前从学习和讨论开始，项目需求见 [MVP 需求分析草稿](MVP.md)。首批案例范围与具体组织方式待讨论。

写作与翻译参考[中英文术语约定](TERMINOLOGY.md)。

参与项目请从[贡献指南](CONTRIBUTING.zh.md)（[English](CONTRIBUTING.md)）开始，按任务找到写作、检查和 PR 协作要求。

## 开发经验

- 文档：[文档代码示例类型检查](lessons/docs-example-typecheck.zh.md)（[English](lessons/docs-example-typecheck.md)）
- 协作：[Git 提交与 PR 协作](lessons/commits-and-pr-integration.zh.md)（[English](lessons/commits-and-pr-integration.md)）
- 文档：[中英双语文档一致性维护](lessons/bilingual-consistency-records.zh.md)（[English](lessons/bilingual-consistency-records.md)）

新经验使用[中文模板](templates/lesson.zh.md)或[英文模板](templates/lesson.md)，保存到 `lessons/`，替换所有 `{{…}}` 占位符及语言切换链接。正文按“问题 → 经验 → 方法 → 案例”及对应英文结构展开；案例放在底部，支持前面的归纳。固定四个二级章节，需要细分时使用三级标题。验证状态用正文说明实际做了什么，不要求每条经验都复现。双语更新、确认记录及检查范围见[Lesson 双语维护](docs/bilingual-maintenance.zh.md)。

## 文档检查

[GitHub Actions 配置](https://github.com/Liu-KM/my-dev-lessons/actions/workflows/docs.yml)在 push、PR 和手动触发时执行 Markdown 基础格式、本地文件链接与标题锚点、经验结构及双语一致性检查。检查排除 `ref/`；格式检查跳过链接到 `AGENTS.md` 的 `CLAUDE.md`，避免重复检查。每次 PR 的实际运行结果以对应提交的 Actions 记录为准。

格式规则见 [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc)，工作流见 [docs.yml](.github/workflows/docs.yml)。链接检查采用离线模式，不请求外部网站。经验结构检查要求一个标题、四个按顺序排列的非空章节、参考案例中的来源链接和非空验证状态，以及无遗留模板占位符；它不判断来源是否支持结论或实践是否有效。当前也不检查代码示例类型或术语语义，不部署网站。

本地运行经验结构检查及其失败场景测试（Python 3.9 及以上，无第三方依赖）：

```sh
python scripts/check_lessons.py
python scripts/check_lesson_pairs.py
python -m unittest discover -s scripts -p 'test_*.py'
```

第一条经验的[案例与验证状态](lessons/docs-example-typecheck.zh.md#案例)也是结构与中文锚点检查的样本。
