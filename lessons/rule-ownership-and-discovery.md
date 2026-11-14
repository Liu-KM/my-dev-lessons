# Rule maintenance and discovery

English | [中文](rule-ownership-and-discovery.zh.md)

## Problem

When the same rule appears in the project introduction, agent instructions, writing templates, and topic documents, every change requires finding all copies. Missed updates create contradictions, while accumulated explanations make entry documents longer.

Removing duplicates alone is insufficient: once a rule moves, people and agents may fail to find it and continue working from memory unless clear entry points exist. Duplicate maintenance and poor discoverability need to be addressed together.

## Lesson

Give each rule one primary maintenance location and link to it elsewhere. Provide task-based navigation and make reading the relevant rules part of the actual workflow. Maintain content centrally while allowing multiple entry points.

One location means one logical source; an English–Chinese pair can jointly serve as that source. Brief reminders may recur, but separate files must not independently define complete requirements or add exceptions.

## Method

1. Search distinctive phrases and related concepts, and assign one source according to responsibility. Replace complete copies elsewhere with brief reminders and direct links, repairing old references together. See [Deciding when to add or revise lessons and rules](lesson-and-rule-decisions.md) for consolidation decisions and preserving conditions.
2. Provide navigation from the current task to the relevant policy and read it before editing or reviewing. Multiple entry points lead to the same source of complete requirements.
3. Follow an actual task entry point to the rule. Check that links reach the right requirements, old locations contain no independent definitions, and affected templates and checkers agree with the rule.

For example, the documentation policy owns lesson-writing requirements, the contribution guide supplies task entry points, and the template provides a fillable structure linked to the policy. The checker implements that requirement without defining a separate policy.

Link checks establish that a target file or heading exists. Following the task path and reviewing changes are still needed to judge whether it is the right rule, definitions remain duplicated, or the rule is followed.

## Case

[DSH commit `aa36b3b36b`: establish documentation responsibilities and length checks](https://github.com/deepseek-ai/deepseek-harness/commit/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a)

- **Problem and design**: Repeated rules and appended explanations expand standing documents. The commit assigns responsibilities to documentation tiers and requires searching repeated phrases, keeping one home, and replacing other statements with links.
- **Evidence**: The [documentation standard at that revision](https://github.com/deepseek-ai/deepseek-harness/blob/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a/docs/AGENTS.md). The length checker introduced in the same commit and its limits are explained in the [case on adding and revising lessons and rules](lesson-and-rule-decisions.md#case).

[DSH commit `73dbbb751c`: organize review rules and entry points by the artifact being changed](https://github.com/deepseek-ai/deepseek-harness/commit/73dbbb751c2ad113cd65d40c99c1942d0c83dc06)

- **Organization**: Replace the existing rule page with a topic directory and navigation mapping changes to the relevant rules. Topic pages link to type definitions and explanations of their meaning instead of duplicating them.
- **Usage**: Update root instructions and the code review workflow to require locating and reading the relevant rules before reviewing changes; repair references and bilingual pairs together.
- **Evidence**: The [navigation page](https://github.com/deepseek-ai/deepseek-harness/blob/73dbbb751c2ad113cd65d40c99c1942d0c83dc06/docs/defensive-patterns/README.md) and [review workflow](https://github.com/deepseek-ai/deepseek-harness/blob/73dbbb751c2ad113cd65d40c99c1942d0c83dc06/.agents/skills/dsh-code-review/SKILL.md).

Verification status: We inspected both DSH commits and their rule and reference changes. We did not run the length checker or measure subsequent duplication or compliance. This project consolidated writing requirements and check instructions in the documentation policy, replaced full definitions in README and Agent instructions with links, and added task navigation to the contribution guide. As an actual rule update, the verification-status requirement now distinguishes source inspection, local execution, and remote CI in the policy; the templates link to that requirement instead of defining it independently. Local checks verified links and paths from six entry points to five policy destinations, and manual review checked both languages and the rule's remaining definitions. This does not establish long-term compliance; remote checks are recorded in the corresponding PR.

The project's current owners and maintenance procedure are defined in [documentation maintenance](../docs/documentation.md). The lesson explains the approach; that policy owns the operational requirements.
