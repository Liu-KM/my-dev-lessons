# Git 提交与 PR 协作

[English](commits-and-pr-integration.md) | 中文

## 问题

一个改动通常需要多轮实现、检查和讨论。如果每次保存进展都直接提交并推送到主线，尚未认可的方案就会成为主线的一部分。CI 通过只能证明配置的检查通过，不能替代对需求、内容和取舍的确认。

问题不在于开发途中有多个 commit，而在于把保存进展与接受成果当成了同一个动作。

## 经验

用分支上的 commit 保存阶段性进展，用 PR 组织一个完整改动的审阅与验证，确认后再合入主线。开发可以持续迭代，主线接收的是已经认可的成果。

## 方法

1. 围绕一个明确改动建立分支。讨论稿可以先留在工作区，需要保存或远程检查时再提交到该分支。
2. 通过同一个 PR 展示改动，尚在打磨时使用 Draft 状态。后续修正继续进入该分支，PR 描述随最终方案更新。
3. 合入前检查内容是否符合需求、相关 CI 是否通过，以及审阅是否完成。本项目由用户确认后合入，不把检查通过视为自动合并授权。
4. 按改动选择合并方式。小型独立任务可以 squash 成一个主线提交；需要保留有意义的分步历史时，也可以保留多个提交。

`commit` 是创建提交，`push` 是将提交发送到远程分支，PR 是审阅与讨论改动的入口，`merge` 才是合入目标分支。推送功能分支不等于推送主线。采用 PR 也不自动保证主线历史精简，是否压缩提交需要单独决定。

这条经验不要求每轮交流都提交，也不要求重写已经发布的历史。分支保护可以进一步强制 PR 和检查要求，但需要实际配置；流程约定本身不等于 GitHub 已禁止直接推送。

保存进展也应尽量形成逻辑独立、便于审阅和撤销的提交。主线历史的目标是解释清楚改动，而非单纯减少 commit 数量；多个独立问题不应仅为了“干净”而压成一个提交。

## 案例

[DSH 提交 `204c36ed76`：通过 PR #15 合入文档同步检查](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **解决的问题或设计目标**：将文档示例类型检查和事件表检查作为一组改动合入主线。
- **采取的办法**：改动在 `feat/rfc006-doc-sync` 分支推进，随后通过 PR 合入。分支先实现检查，再修正解析问题、补充本地 pre-push 接入；这些修改没有各自作为一次直接推送主线的操作。
- **可查看的证据**：[PR #15](https://github.com/deepseek-ai/deepseek-harness/pull/15)对应的合并提交保留了分支历史，其中包括[初始实现 `6a528be569`](https://github.com/deepseek-ai/deepseek-harness/commit/6a528be5695deb9b5207477948f0110d588c8c01)、[解析修复 `7a39616a06`](https://github.com/deepseek-ai/deepseek-harness/commit/7a39616a06731b6a61e861494e3169511d87a344)和[pre-push 接入 `fa7d1df6f2`](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828)。这是一笔保留分支历史的 merge commit，不是 squash merge。

### 补充参考

以下是我们学习时补充的参考：

- 《Pro Git》第 2 版：[5.2](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project) 解释逻辑独立的提交；[5.3](https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project) 介绍主题分支与集成方式。
- [MIT Missing Semester：Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/)：补充快照、提交历史与分支的概念基础。

Draft PR 与用户确认合并是本项目的流程选择。

验证状态：已检查本地 DSH 仓库的合并提交、父提交及分支内提交记录，并阅读上述书籍章节与课程讲义；未核对该 PR 当时的审批与 CI 结果。分支迭代后通过 PR 合入由历史支持；用户确认后合并及小型任务可采用 squash，是本项目选择的协作方式。此前本项目直接推送主线，尚未完成一次 PR 合入实践。
