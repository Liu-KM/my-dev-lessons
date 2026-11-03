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

## Documentation checks

Run these checks from the repository root (Python 3.9 or later, without third-party dependencies):

```sh
python scripts/check_lessons.py
python scripts/check_lesson_pairs.py
python -m unittest discover -s scripts -p 'test_*.py'
```

The [workflow](../.github/workflows/docs.yml) runs these checks, basic Markdown formatting, and local file links and heading anchors on pushes, PRs, and manual dispatch. The [format configuration](../.markdownlint-cli2.jsonc) excludes the reference clone and CLAUDE.md, which links to AGENTS.md. Link checks run offline and do not validate external URLs.

The lesson structure check validates titles, fixed sections, case source links, verification status, and template placeholders. [Bilingual maintenance](bilingual-maintenance.md#check-coverage) defines the pairing check's coverage and limits. Current checks cannot establish that sources support conclusions, translations preserve meaning, or commands execute successfully. They do not type-check documentation examples or deploy a website. The first lesson's [case](../lessons/docs-example-typecheck.zh.md#案例) also serves as a structure and Chinese-anchor sample.

Remote success is established by the Actions records for the corresponding commit. Required checks and integration restrictions are covered by the [PR policy](pull-requests.md#automation-and-activation).
