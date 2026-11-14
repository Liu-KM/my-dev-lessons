# Git commits and PR collaboration

English | [中文](commits-and-pr-integration.zh.md)

## Problem

A change usually takes several rounds of implementation, checking, and discussion. If every saved increment is committed and pushed directly to the main branch, proposals that have not been accepted become part of it. Passing CI proves only that the configured checks passed; it cannot replace confirmation of requirements, content, and tradeoffs.

The problem is not having several commits during development. It is treating saving progress and accepting results as the same action.

## Lesson

Use commits on a branch to save intermediate progress, and a PR to organize review and validation of a complete change before integrating it into the main branch. Development can continue to iterate while the main branch receives accepted work.

## Method

1. Keep work that is still being refined on a feature branch and review the complete result through one PR. Saving or pushing branch progress does not mean accepting the result.
2. Assess check results and review conclusions separately before deciding to merge. Checks establish whether configured conditions are met; review judges whether the requirements, content, and tradeoffs are acceptable.
3. Organize history so changes can be understood and reverted: squash incremental progress toward one result when useful, retain meaningful steps, and keep independent problems separate regardless of commit count.

The project's [commit and integration policy](../docs/pull-requests.md#commits-and-integration) owns commit timing, Draft PRs, and user-confirmation requirements. Branch protection requires actual configuration; see [automation and activation](../docs/pull-requests.md#automation-and-activation). This method does not require committing after every exchange or rewriting published history.

## Case

[DSH commit `204c36ed76`: integrate documentation synchronization checks through PR #15](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **Problem or design goal**: Integrate documentation example type checks and event table checks into the main branch as one set of changes.
- **Solution**: Develop the changes on `feat/rfc006-doc-sync`, then merge through a PR. The branch first implemented the checks, then fixed parsing and added local pre-push integration; these were not separate direct pushes to the main branch.
- **Evidence to inspect**: The merge commit for [PR #15](https://github.com/deepseek-ai/deepseek-harness/pull/15) preserves the branch history, including [initial implementation `6a528be569`](https://github.com/deepseek-ai/deepseek-harness/commit/6a528be5695deb9b5207477948f0110d588c8c01), [parsing fix `7a39616a06`](https://github.com/deepseek-ai/deepseek-harness/commit/7a39616a06731b6a61e861494e3169511d87a344), and [pre-push integration `fa7d1df6f2`](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828). This is a merge commit preserving branch history, not a squash merge.

We inspected the merge commit, its parents, and branch commits in the local DSH repository. They support branch iteration followed by PR integration; we did not verify that PR's historical approvals or CI results. Draft PRs, user confirmation, and optional squashing are this project's workflow choices.

In [PR #1](https://github.com/Liu-KM/my-dev-lessons/pull/1), this project updated the feature branch, passed documentation CI, and squash-merged after user confirmation. The [merge commit](https://github.com/Liu-KM/my-dev-lessons/commit/83a377de6b956bea346e18ddd07e67e105bdc23a) records the integrated result. This practice does not establish that branch protection or the PR policy workflow has been enabled.

Further reading: Pro Git [5.2](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project) and [5.3](https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project); [MIT Missing Semester: Git](https://missing.csail.mit.edu/2020/version-control/).
