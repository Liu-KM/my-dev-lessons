# Documentation maintenance

English | [中文](documentation.zh.md)

This page owns documentation responsibilities, lesson writing requirements, and documentation check instructions. Use the [contribution guide](../CONTRIBUTING.md#find-rules-by-task) to select the rules for a task.

## Rule ownership

Each rule has one primary maintenance location; an existing bilingual pair forms one logical source. Other pages may retain essential short reminders, but link to the full requirements and do not introduce separate exceptions.

| Content | Maintained in | Responsibilities elsewhere |
| --- | --- | --- |
| Project goals and scope | [MVP](../MVP.md) | README introduces the project and links to it |
| Lesson writing and documentation responsibilities | This page | Templates provide fillable structure; the contribution guide provides task navigation |
| Bilingual pairing, confirmation, and records | [Bilingual maintenance](bilingual-maintenance.md) | Writing entry points and templates link to the workflow |
| Concepts, translations, and terms kept verbatim | [Terminology](../TERMINOLOGY.md) | Other documents use the conventions without copying the table |
| Issues, commits, PRs, and integration | [PR policy](pull-requests.md) | The contribution guide connects the steps; Agent instructions provide reminders |
| Agent startup and discussion agreements | [AGENTS.md](../AGENTS.md) | CLAUDE.md links to the same file |
| Engineering lessons and historical evidence | [Lessons](../README.md#开发经验) | Explain rationale and applicability; link project operations to the relevant policy |

Templates and checkers consume rules. When changing a rule, check whether they need corresponding updates. Resolve or explicitly discuss implementation discrepancies rather than treating two different requirements as current policy. Discussion drafts and local operation notes are not sources of current rules.

## Learning and adoption

For a selected DSH learning topic, default to the responsibilities, workflow, and checks used by the case to solve that problem. Verify the specific revision and sources before deciding how to integrate the mechanism here; unrelated DSH features remain outside the scope.

The person proposing a difference explains what problem the original mechanism prevents, whether that problem exists here, which verifiable constraint requires adaptation, and how the original protection will be retained and tested. Language, runtime, or an explicit user choice can provide grounds. Project size, simplicity, or a check's inability to solve a different problem alone do not justify omitting it. Reviewers assess whether the evidence is sufficient, not merely whether the difference is documented. Mark an unimplemented mechanism as a gap rather than an accepted tradeoff.

## Lesson writing

Start from the [Chinese template](../templates/lesson.zh.md) or [English template](../templates/lesson.md) and save the lesson under `lessons/`. Replace every `{{…}}` placeholder and follow [bilingual maintenance](bilingual-maintenance.md) to add the counterpart, language links, and record.

- Use a title that directly identifies the problem or application scenario.
- Use four nonempty second-level sections in order: Problem, Lesson, Method, and Case, with their Chinese equivalents. Use third-level headings for subdivisions. State a reusable insight first and support it with the case at the bottom, rather than only retelling commits.
- Distinguish DSH's actual practice, our inference, and this project's adopted approach without copying its entire current architecture or rules. A case may be a useful design or a failure and repair; DSH's adoption alone does not establish effectiveness.
- Link the case to a specific commit, naming the commit and change topic in the link label. Reference code, tests, or decisions at that revision when useful. Explain what they support without inventing undocumented motives.
- State separately what historical source inspection, local execution, and remote CI actually establish in the verification status. Identify what was not executed. Not every case needs reproduction; configuration or static reading cannot establish successful execution.

## Changing rules

Find the owner in the table, then search distinctive wording, related concepts, and incoming links for duplicates or conflicts. Update the owner and its existing translation; adjust templates, checkers, and content using the rule as needed. Entry points provide navigation without repeating full clauses.

Reference repository policies with relative Markdown links to their files or sections so readers can navigate and link checks can validate them. Repair incoming links when moving a rule; the old location may keep a link to the new one.

During review, follow an actual task from README, the contribution guide, or Agent instructions to confirm that the updated rule is discoverable. Check that old locations do not retain independent full definitions. A resolving link does not establish correct rule placement; semantic duplication and exceptions still need human review.

## Adding and consolidating content

Before adding or reviewing a lesson or project rule, the author reads related content through rule ownership and task navigation, then searches the topic, related concepts, and distinctive wording. Compare the problem, applicability, conclusion, and evidence. Similar wording is a clue, not proof of duplication.

| Comparison result | Action |
| --- | --- |
| Same conditions and conclusion, with another case | Add useful evidence to the existing lesson instead of creating an equivalent entry |
| Same problem, with additional conditions, exceptions, or explanation | Extend the existing content while preserving its conditions |
| Different scenarios lead to different conclusions | Explain the scenarios, preserve necessary distinctions, and cross-link |
| Conclusions conflict under the same conditions | Check the evidence and identify the correction or replacement; unresolved conclusions are not current requirements |
| Independent problem with a new reusable judgment | Add a lesson and explain how it differs from related content |
| Ordinary change history without a new lasting judgment | Use the PR description or existing operational documentation; do not create a lesson to fill a template |

A lesson does not automatically become a mandatory rule. When adopting it as project policy, explain the concrete project need, scope, responsible actor, and checking or review method, then update the primary owner in existing policy. The lesson retains the experience and evidence and links to the project's requirements.

When consolidating or replacing content, preserve useful unique rationale, exceptions, tradeoffs, and verification gaps. Partial replacement does not justify deleting content that remains valid. Delete redundant copies only after consolidation, updating translations, pairing records, and incoming links together. Historical cases continue to describe the facts at the time; a current policy change must not rewrite them into the opposite conclusion.

In the PR's change description, the author links related content and briefly explains the choice. The reviewer checks whether the comparison is sufficient, conditions were lost, or an experience was promoted into a universal requirement. Agent collaboration and user review follow [Collaboration review before committing](pull-requests.md#collaboration-review-before-committing). Passing mechanical checks does not establish the absence of semantic duplication or conflicts.

Content review and the budget check below jointly constrain growth; do not delete necessary conditions to meet a length metric. See [Deciding when to add or revise lessons and rules](../lessons/lesson-and-rule-decisions.md) for the rationale and cases.

## Documentation budgets

The [manifest](../scripts/doc-budgets.manifest.json) covers standing entry pages and operational policies. The [checker](../scripts/check_doc_budgets.py) validates each entry's file, metric, and ceiling without writing files. Missing files, invalid entries, and excess length fail; unlisted files have no ceiling. Update the manifest when moving or deleting a listed file, and have the reviewer confirm that protection was not unintentionally removed.

| Scope or parameter | Rationale |
| --- | --- |
| Root agent instructions, README, contribution guides, documentation maintenance, PR policy, and bilingual maintenance | Tasks can repeatedly add to these standing entry pages and operational rules; both sides of existing bilingual pages are listed |
| Lessons, terminology, templates, and the MVP draft are unlisted | They hold historical cases, reference entries, fillable structure, and undecided requirements respectively; a uniform entry-page budget would not replace content review. CLAUDE.md links to existing instructions and is not counted twice |
| `words` | English follows DSH's whitespace-word counting over the whole file, including code and Markdown syntax |
| `characters` | Chinese files count non-whitespace Unicode characters, including English fragments and markup. This is a stable length measure, not Chinese word segmentation or a model token count |
| `max` | This change sets fixed initial ceilings at the reviewed size plus at least 5% headroom, rounded up. Values live only in the manifest and never refresh automatically as files grow |

When editing or review reveals duplication, outdated content, or mixed responsibilities, tidy as needed without waiting for overflow. Leave content unchanged when no concrete problem is found. There is no cleanup schedule, reduction quota, or required output. Relocate content to its owner with a link, then condense redundancy while preserving necessary conditions.

After substantial length changes from cleanup, review whether to lower the ceiling in the same PR, retaining at least 5% headroom; minor wording edits need no reset. To raise it, explain why the content belongs here, why relocation or condensation is insufficient, and the new value's basis. Explain metric or scope changes too. The reviewer assesses the rationale; the user reviews before committing. The checker neither changes ceilings nor decides when cleanup is needed.

`python scripts/check_doc_budgets.py --list` reports usage and entry errors. Like DSH's observational mode, it succeeds even on overflow or missing entries and must not enforce CI; failure to read or parse the manifest itself still fails. Enforcement uses the entry point without `--list`.

This retains DSH's fixed manifest, failure checks, and adjustment review. Python reuses the existing environment. Passing cannot rule out duplication or conflicts; ceilings are not minimization targets.

## Documentation checks

Run the Python documentation checks from the repository root (Python 3.9 or later, without third-party dependencies):

<!-- doc-check-entry -->
```sh
python scripts/check_docs.py
```
<!-- /doc-check-entry -->

The [shared entry](../scripts/check_docs.py) runs wiring, structure, pairing, budget checks and regression tests, stopping on failure. The [wiring check](../scripts/check_doc_entry.py) validates this page's command block, CI steps and hook; see the [case](../lessons/documentation-check-entry.md) for scope and experiments.

Inspect `git config --get core.hooksPath`; integrate existing hooks, or, if unset, enable [pre-push checks](../.githooks/pre-push) with `git config core.hooksPath .githooks`.

The [workflow](../.github/workflows/docs.yml) runs these checks, basic Markdown formatting, and local file links and heading anchors on pushes, PRs, and manual dispatch. The [format configuration](../.markdownlint-cli2.jsonc) excludes the reference clone and CLAUDE.md, which links to AGENTS.md. Link checks run offline and do not validate external URLs.

The lesson structure check validates titles, fixed sections, case source links, verification status, and template placeholders. [Bilingual maintenance](bilingual-maintenance.md#check-coverage) defines the pairing check's coverage and limits. Current checks cannot establish that sources support conclusions, translations preserve meaning, or commands execute successfully. They do not type-check documentation examples or deploy a website. The first lesson's [case](../lessons/docs-example-typecheck.zh.md#案例) also serves as a structure and Chinese-anchor sample.

Remote success is established by the Actions records for the corresponding commit. Required checks and integration restrictions are covered by the [PR policy](pull-requests.md#automation-and-activation).
