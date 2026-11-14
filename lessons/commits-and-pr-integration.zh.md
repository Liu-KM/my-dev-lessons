# Git 提交与 PR 协作

[English](commits-and-pr-integration.md) | 中文

## 问题

一个改动通常需要多轮实现、检查和讨论。如果每次保存进展都直接提交并推送到主线，尚未认可的方案就会成为主线的一部分。CI 通过只能证明配置的检查通过，不能替代对需求、内容和取舍的确认。

问题不在于开发途中有多个 commit，而在于把保存进展与接受成果当成了同一个动作。

## 经验

用分支上的 commit 保存阶段性进展，用 PR 组织一个完整改动的审阅与验证，确认后再合入主线。开发可以持续迭代，主线接收的是已经认可的成果。

## 方法

1. 将尚在迭代的改动留在功能分支，通过同一个 PR 审阅完整成果；保存或推送分支进展不等于接受成果。
2. 分别核对检查结果与审阅结论，再决定是否合入。检查回答配置的条件是否满足，审阅判断需求、内容和取舍是否可接受。
3. 按解释改动和撤销的需要组织历史：同一成果的零散进展可以 squash，有意义的分步提交可以保留，独立问题不为减少提交数而合并。

本项目的提交时机、Draft PR 与用户确认要求由[提交与合入规范](../docs/pull-requests.zh.md#提交与合入)维护；分支保护须实际配置，见[自动检查与启用](../docs/pull-requests.zh.md#自动检查与启用)。本方法不要求每轮交流都提交或重写已发布历史。

## 案例

[DSH 提交 `204c36ed76`：通过 PR #15 合入文档同步检查](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **解决的问题或设计目标**：将文档示例类型检查和事件表检查作为一组改动合入主线。
- **采取的办法**：改动在 `feat/rfc006-doc-sync` 分支推进，随后通过 PR 合入。分支先实现检查，再修正解析问题、补充本地 pre-push 接入；这些修改没有各自作为一次直接推送主线的操作。
- **可查看的证据**：[PR #15](https://github.com/deepseek-ai/deepseek-harness/pull/15)对应的合并提交保留了分支历史，其中包括[初始实现 `6a528be569`](https://github.com/deepseek-ai/deepseek-harness/commit/6a528be5695deb9b5207477948f0110d588c8c01)、[解析修复 `7a39616a06`](https://github.com/deepseek-ai/deepseek-harness/commit/7a39616a06731b6a61e861494e3169511d87a344)和[pre-push 接入 `fa7d1df6f2`](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828)。这是一笔保留分支历史的 merge commit，不是 squash merge。

已检查本地 DSH 仓库的合并提交、父提交及分支内记录，支持“分支迭代后通过 PR 合入”；未核对该 PR 当时的审批与 CI 结果。Draft PR、用户确认和可选择 squash 是本项目的流程选择。

本项目在 [PR #1](https://github.com/Liu-KM/my-dev-lessons/pull/1) 中更新功能分支，文档 CI 通过后经用户确认 squash 合入；[合并提交](https://github.com/Liu-KM/my-dev-lessons/commit/83a377de6b956bea346e18ddd07e67e105bdc23a)记录了集成结果。这次实践不证明分支保护或 PR 策略工作流已启用。

补充阅读：《Pro Git》[5.2](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)、[5.3](https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project)；[MIT Missing Semester：Git](https://missing.csail.mit.edu/2020/version-control/)。
