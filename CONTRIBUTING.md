# Contributing

English | [中文](CONTRIBUTING.zh.md)

Contributions can improve the evidence behind a lesson, clarify its explanation, or improve the tools used to maintain this repository. Start with the [project goals](MVP.md) to understand its scope.

## Find rules by task

Before editing or reviewing, read the policy for the current task. The linked page owns the full requirements.

| Task | Read |
| --- | --- |
| Write or review a lesson | [Writing requirements](docs/documentation.md#lesson-writing) and their template links |
| Decide whether to add, consolidate, or replace content | [Adding and consolidating content](docs/documentation.md#adding-and-consolidating-content) |
| Synchronize English and Chinese | [Bilingual maintenance](docs/bilingual-maintenance.md) and [terminology](TERMINOLOGY.md) |
| Run documentation checks | [Documentation checks](docs/documentation.md#documentation-checks) |
| Prepare or review a PR | [PR policy](docs/pull-requests.md) |
| Change project rules | [Rule ownership and changes](docs/documentation.md#rule-ownership) |

## Discuss the problem

Check [existing Issues](https://github.com/Liu-KM/my-dev-lessons/issues) for the problem you want to address. For a new problem, describe what is missing or incorrect and the expected outcome using the [Issue template](.github/ISSUE_TEMPLATE/change.yml). Include a concrete example or source when available.

Discuss the scope before substantial changes. Issue references and change boundaries follow [Scope and traceability](docs/pull-requests.md#scope-and-traceability).

## Prepare the change

Use a branch for the change. If you do not have repository write access, fork the repository and work on a branch there. Follow [Commits and integration](docs/pull-requests.md#commits-and-integration); coordinate dependent work using [Parallel and dependent PRs](docs/pull-requests.md#parallel-and-dependent-prs).

When contributing a lesson, use the task navigation above to read the writing and bilingual policies. Agents should also read [AGENTS.md](AGENTS.md).

## Check the result

Follow the local instructions in [Documentation checks](docs/documentation.md#documentation-checks). Review sources and conclusions as well as automated results: passing checks does not establish that a cited case supports the lesson. If the document has a second language version, review both versions together.

## Submit for review

Use the [PR template](.github/pull_request_template.md) to explain the problem, final changes, and actual verification. Follow [Classification](docs/pull-requests.md#classification) and [Description and verification](docs/pull-requests.md#description-and-verification) when preparing the PR for review. Contributors without label permissions can state their intended labels in the description for a maintainer to apply.

Address review feedback on the same branch and update the description when the proposal changes. Read [Commits and integration](docs/pull-requests.md#commits-and-integration) for the conditions for merging.
