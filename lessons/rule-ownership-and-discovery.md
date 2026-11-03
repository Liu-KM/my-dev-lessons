# Rule maintenance and discovery

English | [中文](rule-ownership-and-discovery.zh.md)

## Problem

When the same rule appears in the project introduction, agent instructions, writing templates, and topic documents, every change requires finding all copies. Missed updates create contradictions, while accumulated explanations make entry documents longer.

Removing duplicates alone is insufficient: once a rule moves, people and agents may fail to find it and continue working from memory unless clear entry points exist. Duplicate maintenance and poor discoverability need to be addressed together.

## Lesson

Give each rule one primary maintenance location and link to it elsewhere. Provide task-based navigation and make reading the relevant rules part of the actual workflow. Maintain content centrally while allowing multiple entry points.

One location means one logical source; an English–Chinese pair can jointly serve as that source. Brief reminders may recur, but separate files must not independently define complete requirements or add exceptions.

## Method

1. Inventory existing rules. Search distinctive phrases and related concepts to find repeated or conflicting statements; text search identifies candidates, while semantic duplication still requires judgment.
2. Assign ownership by responsibility: documentation standards own writing requirements, the terminology table owns wording, and PR policy owns collaboration. Consolidate requirements while preserving conditions and necessary exceptions; do not present undecided designs as current rules.
3. Replace complete copies elsewhere with brief reminders and direct links. Repair old references in the same change so old and new rules do not coexist.
4. Provide navigation from the current task to the relevant standard. Agent instructions or review workflows should require reading it before editing or judging content, rather than relying solely on memory or repository-wide search.
5. Check that links resolve, task entry points lead to the requirements, and old locations no longer duplicate definitions. Targeted length limits can constrain repeatedly expanding entry documents; limits cannot replace content review.

For example, the documentation standard owns complete lesson-writing requirements, the README links from a writing task, and the template provides a fillable structure with a link to the standard. Update the owner and affected templates and checkers when a rule changes, rather than rewriting it at every entry point. A checker implements a rule; it is not a separate policy source.

Link checks establish that paths or anchors resolve, not that they lead to the correct rule. Length checks detect excess, not all semantic duplication. Compliance still needs behavior-specific checks and review. This method aims to reduce duplication and discovery failures; it does not automatically guarantee enforcement.

## Case

[DSH commit `aa36b3b36b`: establish documentation responsibilities and length checks](https://github.com/deepseek-ai/deepseek-harness/commit/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a)

- **Problem and design**: Repeated rules and appended explanations expand standing documents. The commit assigns responsibilities to documentation tiers and requires searching repeated phrases, keeping one home, and replacing other statements with links.
- **Executable constraint**: Add a length checker and manifest to the documentation checks; excess length or a missing listed file fails. This constrains growth in selected documents, rather than deduplicating semantics across the repository.
- **Evidence**: The [documentation standard at that revision](https://github.com/deepseek-ai/deepseek-harness/blob/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a/docs/AGENTS.md) and [checker](https://github.com/deepseek-ai/deepseek-harness/blob/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a/scripts/verify-doc-budgets.ts).

[DSH commit `73dbbb751c`: organize review rules and entry points by the artifact being changed](https://github.com/deepseek-ai/deepseek-harness/commit/73dbbb751c2ad113cd65d40c99c1942d0c83dc06)

- **Organization**: Replace the existing rule page with a topic directory and navigation mapping changes to the relevant rules. Topic pages link to type definitions and semantics instead of duplicating them.
- **Usage**: Update root instructions and the code review workflow to require locating and reading the relevant rules before reviewing changes; repair references and bilingual pairs together.
- **Evidence**: The [navigation page](https://github.com/deepseek-ai/deepseek-harness/blob/73dbbb751c2ad113cd65d40c99c1942d0c83dc06/docs/defensive-patterns/README.md) and [review workflow](https://github.com/deepseek-ai/deepseek-harness/blob/73dbbb751c2ad113cd65d40c99c1942d0c83dc06/.agents/skills/dsh-code-review/SKILL.md).

Verification status: We inspected both DSH commits and their rule and reference changes. We did not run the length checker or measure subsequent duplication or compliance. This project consolidated writing requirements and check instructions in the documentation policy, replaced full definitions in README and Agent instructions with links, and added task navigation to the contribution guide. As an actual rule update, the verification-status requirement now distinguishes source inspection, local execution, and remote CI in the policy; the templates link to that requirement instead of defining it independently. Local checks verified links and paths from six entry points to five policy destinations, and manual review checked both languages and the rule's remaining definitions. This does not establish long-term compliance; remote checks are recorded in the corresponding PR.

The project's current owners and maintenance procedure are defined in [documentation maintenance](../docs/documentation.md). The lesson explains the approach; that policy owns the operational requirements.
