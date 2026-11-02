# Git commits and PR collaboration

English | [中文](commits-and-pr-integration.zh.md)

## Problem

A change usually takes several rounds of implementation, checking, and discussion. If every saved increment is committed and pushed directly to the main branch, proposals that have not been accepted become part of it. Passing CI proves only that the configured checks passed; it cannot replace confirmation of requirements, content, and tradeoffs.

The problem is not having several commits during development. It is treating saving progress and accepting results as the same action.

## Lesson

Use commits on a branch to save intermediate progress, and a PR to organize review and validation of a complete change before integrating it into the main branch. Development can continue to iterate while the main branch receives accepted work.

## Method

1. Create a branch for a clearly defined change. Discussion drafts can remain in the working tree; commit them to the branch when saving progress or running remote checks is needed.
2. Present the change through one PR, using Draft status while it is still being refined. Continue pushing revisions to that branch and update the PR description to reflect the final proposal.
3. Before merging, check that the content meets the requirements, relevant CI passes, and review is complete. This project requires user confirmation before merging; passing checks do not authorize an automatic merge.
4. Choose the merge strategy for the change. A small independent task may be squashed into one mainline commit; multiple commits may be retained when their steps form meaningful history.

`commit` creates a commit, `push` sends commits to a remote branch, a PR provides a place to review and discuss changes, and `merge` integrates them into the target branch. Pushing a feature branch is different from pushing the main branch. PRs do not automatically produce concise mainline history; squashing is a separate decision.

This lesson does not require committing after every exchange or rewriting published history. Branch protection can further enforce PR and check requirements, but it must actually be configured; a written workflow does not mean GitHub blocks direct pushes.

Even progress commits should aim to be logically independent and easy to review and revert. Mainline history should explain changes clearly, rather than merely minimize commit counts; independent problems should not be squashed together just to make history look clean.

## Case

[DSH commit `204c36ed76`: integrate documentation synchronization checks through PR #15](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **Problem or design goal**: Integrate documentation example type checks and event table checks into the main branch as one set of changes.
- **Solution**: Develop the changes on `feat/rfc006-doc-sync`, then merge through a PR. The branch first implemented the checks, then fixed parsing and added local pre-push integration; these were not separate direct pushes to the main branch.
- **Evidence to inspect**: The merge commit for [PR #15](https://github.com/deepseek-ai/deepseek-harness/pull/15) preserves the branch history, including [initial implementation `6a528be569`](https://github.com/deepseek-ai/deepseek-harness/commit/6a528be5695deb9b5207477948f0110d588c8c01), [parsing fix `7a39616a06`](https://github.com/deepseek-ai/deepseek-harness/commit/7a39616a06731b6a61e861494e3169511d87a344), and [pre-push integration `fa7d1df6f2`](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828). This is a merge commit preserving branch history, not a squash merge.

### Further reading

These references supplement our study:

- Pro Git, second edition: [5.2](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project) explains logically separate commits; [5.3](https://git-scm.com/book/en/v2/Distributed-Git-Maintaining-a-Project) covers topic branches and integration strategies.
- [MIT Missing Semester: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/): Background on snapshots, commit history, and branches.

Draft PRs and user confirmation before merging are this project's workflow choices.

Verification status: We inspected the merge commit, its parents, and commits within the branch in the local DSH repository, and read the cited book chapters and lecture notes; we did not verify the PR's historical approvals or CI results. The history supports branch iteration followed by PR integration. User confirmation before merging and optional squashing for small tasks are this project's choices. This project practiced that workflow in [PR #1](https://github.com/Liu-KM/my-dev-lessons/pull/1): the branch was updated, documentation CI passed, and the user confirmed a squash merge into the main branch. The [merge commit](https://github.com/Liu-KM/my-dev-lessons/commit/83a377de6b956bea346e18ddd07e67e105bdc23a) records the integrated result; this does not establish that branch protection or the new PR policy workflow has been enabled.
