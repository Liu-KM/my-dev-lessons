# my-dev-lessons

从 DeepSeek Harness（DSH）从零开始的开发历史中，学习开发技巧、工程决策和踩坑经验，并通过自己的实践，将它们整理成可复用的方法和工具。

这些 lessons 既是我学到的经验，也是教给我的 Agent 的课程：帮助我提升工程能力，让 Codex 等 Agent 更好地参与开发，减少 AI slop。

目前从学习和讨论开始，项目需求见 [MVP 需求分析草稿](MVP.md)。首批案例范围与具体组织方式待讨论。

写作与翻译参考[中英文术语约定](TERMINOLOGY.md)。

## 开发经验

- 文档：[让文档示例参与类型检查](lessons/docs-example-typecheck.md)

## 文档检查

[GitHub Actions](https://github.com/Liu-KM/my-dev-lessons/actions/workflows/docs.yml) 在 push、PR 和手动触发时执行 Markdown 基础格式检查及本地文件链接检查。检查排除 `ref/`；格式检查跳过链接到 `AGENTS.md` 的 `CLAUDE.md`，避免重复检查。

格式规则见 [.markdownlint-cli2.jsonc](.markdownlint-cli2.jsonc)，工作流见 [docs.yml](.github/workflows/docs.yml)。链接检查采用离线模式，不请求外部网站；当前不检查链接锚点、代码示例类型或术语语义，也不部署网站。
