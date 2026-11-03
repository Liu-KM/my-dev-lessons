# Issue and PR collaboration

English | [中文](pull-requests.zh.md)

## Scope and traceability

Split independent changes; review the documentation, implementation, tests, and CI needed for one outcome together. Issues record problems, scope, and acceptance criteria; PRs present concrete solutions. One Issue may have several PRs. Individual edits or conversations do not each require a new Issue.

Every ready PR must reference at least one Issue in this repository. Put `Refs #N` on its own body line for context, or `Fixes #N` to resolve the Issue, replacing the example number. PR numbers and references in code, quotations, or comments do not count. Drafts may lack information temporarily; complete it before marking ready.

## Commits and integration

Complete the change, relevant local checks, and collaboration review below in the working tree, then present a local PR summary to the user. Commit, push the feature branch, and create the remote PR only after user review and authorization. The pre-commit summary is not a published PR. Each commit should represent a logically coherent change; passing checks do not authorize an automatic commit or push.

After publication is authorized, use a Draft PR while refining the proposal. Mark it ready when its scope, description, and verification evidence are complete. Continue revisions on the same branch and describe the final proposal. Required remote checks must pass on the latest candidate commit. Before merging, recheck checks, unresolved review feedback, and the final diff, then obtain explicit user confirmation to merge. Missing, failed, or stale CI results prevent merging; green results do not authorize it automatically.

Choose the merge strategy for the change: squash incremental work on one outcome or retain meaningful steps. Do not combine independent problems merely to reduce commit count. See [Git commits and PR collaboration](../lessons/commits-and-pr-integration.md) for the rationale and case.

### Collaboration review before committing

When an agent prepares a change, complete the following workflow by default before handing it to the user for review. Proceed through ordinary checks, collaboration, and corrections without requesting confirmation for each step.

For routine reviews, the sub-agent defaults to `gpt-6.1-sol` with `medium` reasoning effort. Use focused follow-up on concrete findings; explain the reason when a different model or effort is needed.

1. **Author preparation**: Complete the change, relevant local checks, and PR description draft. Establish the review base and file scope, including untracked new files.
2. **Independent review**: Request a read-only review from an agent that did not author the change. Provide the requirements, base, change locations, sources, and verification records. The reviewer reads the diff, related files, and evidence independently rather than checking only the author's summary. Check requirement coverage, details, and source support, and assess evidence for differences from DSH under [Learning and adoption](documentation.md#learning-and-adoption). Report finding locations, evidence, impact, and unverified items.
3. **Corrections and follow-up**: The author addresses findings and requests focused follow-up from the same reviewer when needed. Retain unresolved disagreements, choices that would change requirements, and incomplete verification for user judgment. Do not repeat reviews merely to obtain approval.
4. **User review**: Provide the inspectable change and one concise explanation of what is complete, files and sources both agents reviewed, how DSH handles the problem and how and why this project differs, check results, findings and their disposition, and open decisions. Maintain only one Chinese local summary for the user. An English publication body may remain internal; avoid multiple user-facing review drafts.

This workflow is this project's collaboration choice, not a claim that DSH uses the same pre-commit process, and CI does not trigger it automatically. If an independent agent is unavailable, report the gap; do not label author self-review as independent review. Passing review does not authorize commits, pushes, or merges; user authorization still follows this section. After subsequent edits, recheck only affected content and checks.

## Classification

Choose one dominant `kind/*` and at least one materially affected `area/*` for each PR. The inventory lives in [pr-labels.json](../.github/pr-labels.json).

| Kind | Intent |
| --- | --- |
| `kind/feature` | Adds or intentionally changes behavior |
| `kind/bug-fix` | Corrects incorrect behavior |
| `kind/doc` | Documentation is the dominant intent |
| `kind/testing` | Tests or test infrastructure without product behavior changes |
| `kind/cleanup` | Maintenance without behavior changes |
| `kind/dependency` | Dependency update without another dominant intent |

Initial areas are `area/lessons`, `area/docs`, `area/ci`, and `area/workflow`: engineering lessons and cases, project documentation, automated checks, and development collaboration respectively. Accompanying tests do not make a feature PR a testing PR; incidental file edits do not require extra area labels. Add new areas and their meanings to the inventory in the same PR.

## Description and verification

Use the [PR template](../.github/pull_request_template.md) with fixed headings `Motivation`, `Changes`, and `Testing`; body text may be Chinese. Explain the problem, final interface and behavior changes, and acceptance checks for each change. Update the description when scope changes. Report only executed checks as passing, distinguish local runs from CI, and identify unexecuted checks. Regression checks should demonstrate failure on a broken example and success after correction.

AI stage ratings, percentages, and badges remain undecided and are not required; factual, brief role descriptions may remain. CI cannot judge requirements, classification accuracy, or evidence sufficiency. Content review and user confirmation are still required before merging.

## Parallel and dependent PRs

Independent work starts from the main branch in separate branches and worktrees. Create a stack only when changes depend on another PR: the child's base targets the parent's branch, and its description and acceptance cover that layer alone. Fix problems in the PR that introduced them, propagate upward, and validate each layer.

Same-repository dependency chains use native GitHub stacks before becoming ready. First verify availability of the GitHub feature and official CLI extension; a branch dependency alone is not a registered stack. Existing same-author PRs may be linked with `gh stack link --base main <bottom-pr> <next-pr>`, followed by verification of server-side membership and order. Coordinate first for different authors. Never automatically dissolve or reorder an existing stack.

Refresh with merge-forward or `gh stack sync`; the latter can cascade-rebase and push, requiring inspection, validation, and renewed review of every affected layer. Protect rewritten pushes with leases; never use raw `--force`. Before landing, obtain fresh check and review states, get explicit user confirmation, and use `gh stack merge` for the confirmed range. CI does not create stacks, rewrite branches, or merge automatically.

If native stacks are unavailable or dependencies cross forks, do not present manual sequential merging as the same mechanism. Keep drafts and decide an alternative workflow. Independent parallel PRs are unaffected.

## Automation and activation

[PR policy](../.github/workflows/pr-policy.yml) runs read-only code from the default branch, fetches live PR metadata, and checks nonempty sections, real Issue references, labels, and native stack relationships for non-trunk bases. It never executes PR branch code. Missing API access or unreadable stack metadata fails rather than silently skipping verification. After stack metadata changes, manually dispatch the workflow with the PR number to recheck.

Maintainers manually run the [label initialization workflow](../.github/workflows/pr-labels.yml). It only creates missing inventory labels, never deleting or rewriting existing labels. Review policy documents and automated checks together.

### First activation

The default branch does not yet contain the checker when it is first introduced. The PR adding it cannot be required to have already run the new policy. Follow this sequence and record results and run links as each step is performed:

1. **Before merging**: Run `python scripts/check_lessons.py` and `python -m unittest discover -s scripts -p 'test_*.py'`, and inspect this PR's documentation CI. Manually review its Issue, label selection, description, and dependencies; record intended label names if they do not exist yet. Merge only after review and explicit user confirmation.
2. **Initialization**: Run `Initialize PR labels` on the default branch, verify label names and meanings, and label PRs that are still open. Confirm that `PR policy` appears in Actions.
3. **First live run**: Use the next open PR for actual development, complete its metadata, and mark it ready. Confirm that `PR policy` runs automatically and reports a result for that PR. Record the PR, head SHA, run link, and conclusion. For manual runs, provide `pr_number`; manual success is diagnostic and does not replace confirming that the check appears on the PR. Draft and closed PRs are skipped, so their green results do not verify enforcement.
4. **Merge requirements**: After confirming that `Issue, labels and stack` and `Documentation checks` actually appear on the PR, configure them as required checks. Inspect branch coverage, bypass permissions, and merge restrictions on failures. Until configuration is complete, do not claim GitHub enforces the policy.
5. **Dependent PRs**: On the first native stack, verify server-side order, parent and child branches, and checks on every layer. Manual runs can diagnose metadata-only stack changes; verify valid checks on the PR before merging. Passing an independent PR does not validate the stack path.

Keep the related Issue open and use `Refs #N` until activation has been verified; record the actual results before closing it. Do not create meaningless Issues or PRs to demonstrate failures. Local tests cover failure cases; real development verifies remote triggers and permissions.

### Verification scope

Local tests cover valid and invalid metadata, PR-event and manual-input entry paths, fetching the current PR, Draft/closed deferral, missing Issues, permission errors, transport failures, and parent and stack queries for dependent PRs. HTTP responses are mocked; these tests do not establish that GitHub Actions permissions, triggers, or branch protection work.

Record actual activation evidence in the relevant PR's verification section. Separately state the status of local tests, remote runs, labels, branch protection, and stack practice, marking unexecuted items as unverified.

## Sources

- [DSH collaboration rules](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/AGENTS.md): independent changes and fix ownership.
- [DSH label design](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/.agents/notes/implemented/process/2026-08-08-unified-github-label-taxonomy.md): separate intent from affected domains.
- [DSH PR description rules](https://github.com/deepseek-ai/deepseek-harness/blob/ce7073d512/.agents/skills/dsh-pr-description/SKILL.md): map changes to verification; this project defers quantified AI declarations.
- [Native GitHub stacks](https://docs.github.com/en/pull-requests/reference/stacked-pull-requests) and [CLI commands](https://docs.github.com/en/pull-requests/reference/stacked-prs-cli-commands): dependency-chain management.
- [GitHub workflow events](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) and [PR GraphQL fields](https://docs.github.com/en/graphql/reference/pulls#pullrequeststack): execution context and stack query references for the checker.

Deferring checks for Drafts, the label inventory, and read-only workflows are this project's implementation choices, not a claim to reproduce DSH's entire policy system.
