# 贡献指南

[English](CONTRIBUTING.md) | 中文

你可以补充或纠正 lesson 的证据、改进内容说明，或完善仓库的维护工具。开始前请阅读[项目目标](MVP.md)，了解项目范围。

## 讨论问题

先查看[已有 Issue](https://github.com/Liu-KM/my-dev-lessons/issues)，确认是否已有对应问题。新问题使用 [Issue 模板](.github/ISSUE_TEMPLATE/change.yml)，说明哪里缺失或不正确，以及期望结果；有具体例子或来源时一并提供。

较大改动先讨论范围。Issue 关联和改动边界遵循[范围与追踪](docs/pull-requests.zh.md#范围与追踪)。

## 准备改动

使用分支开展修改。没有仓库写权限时，可以 fork 仓库并在 fork 中创建分支。按[提交与合入](docs/pull-requests.zh.md#提交与合入)保存和组织改动；存在依赖的工作按[并行与依赖 PR](docs/pull-requests.zh.md#并行与依赖-pr)协调。

贡献 lesson 时，使用[经验模板](templates/lesson.md)，参考[写作说明](README.md#开发经验)与[术语约定](TERMINOLOGY.md)。Agent 还应读取 [AGENTS.md](AGENTS.md)。

## 检查结果

按[文档检查](README.md#文档检查)运行本地检查。除了机器检查，还要审阅来源和结论：检查通过不能证明案例支持经验。如果文档已有另一语言版本，一并审阅两侧内容。

## 提交审阅

使用 [PR 模板](.github/pull_request_template.md)，说明问题、最终变化和实际验证。准备审阅时遵循[分类](docs/pull-requests.zh.md#分类)与[描述与验证](docs/pull-requests.zh.md#描述与验证)要求。没有标签权限的贡献者可以在描述中说明拟用标签，由维护者设置。

在同一分支处理审阅意见，方案变化时更新描述。合入条件见[提交与合入](docs/pull-requests.zh.md#提交与合入)。
