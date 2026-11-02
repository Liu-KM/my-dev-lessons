# Contributing

English | [中文](CONTRIBUTING.zh.md)

Contributions can improve the evidence behind a lesson, clarify its explanation, or improve the tools used to maintain this repository. Start with the [project goals](MVP.md) to understand its scope.

## Discuss the problem

Check [existing Issues](https://github.com/Liu-KM/my-dev-lessons/issues) for the problem you want to address. For a new problem, describe what is missing or incorrect and the expected outcome using the [Issue template](.github/ISSUE_TEMPLATE/change.yml). Include a concrete example or source when available.

Discuss the scope before substantial changes. Issue references and change boundaries follow [Scope and traceability](docs/pull-requests.md#scope-and-traceability).

## Prepare the change

Use a branch for the change. If you do not have repository write access, fork the repository and work on a branch there. Follow [Commits and integration](docs/pull-requests.md#commits-and-integration); coordinate dependent work using [Parallel and dependent PRs](docs/pull-requests.md#parallel-and-dependent-prs).

When contributing a lesson, use the [lesson template](templates/lesson.md) and consult the [writing guidance](README.md#开发经验) and [terminology](TERMINOLOGY.md). Agents should also read [AGENTS.md](AGENTS.md).

## Check the result

Follow the local instructions in [Documentation checks](README.md#文档检查). Review sources and conclusions as well as automated results: passing checks does not establish that a cited case supports the lesson. If the document has a second language version, review both versions together.

## Submit for review

Use the [PR template](.github/pull_request_template.md) to explain the problem, final changes, and actual verification. Follow [Classification](docs/pull-requests.md#classification) and [Description and verification](docs/pull-requests.md#description-and-verification) when preparing the PR for review. Contributors without label permissions can state their intended labels in the description for a maintainer to apply.

Address review feedback on the same branch and update the description when the proposal changes. Read [Commits and integration](docs/pull-requests.md#commits-and-integration) for the conditions for merging.
