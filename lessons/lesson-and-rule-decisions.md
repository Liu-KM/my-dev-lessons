# Deciding when to add or revise lessons and rules

English | [中文](lesson-and-rule-decisions.zh.md)

## Problem

Appending a lesson or rule after every change repeats conclusions and can leave old conclusions and new exceptions presented as current requirements. Having a primary maintenance location identifies where content belongs, but not whether it deserves to be added.

Merging or deleting content merely to reduce length is also risky: similar statements may apply to different scenarios, and old records may contain useful rationale or describe what remains unverified; deleting them can lose both.

## Lesson

New content should add a reusable judgment or necessary evidence. Compare its problem, conditions, and conclusion with existing content before choosing to extend, add, consolidate, or replace it. Adopting a lesson as project policy also requires a concrete application need and an execution method.

Automated checks can detect missing sections or excessive length. People or agents must review whether content is needed, rules conflict, or merging passages loses applicable conditions. Meeting a length ceiling does not establish that the content is correct.

## Method

Start the comparison at the primary owners of related content. Another case supporting the same conclusion usually extends existing evidence; an independent problem may need a new entry. Preserve conclusions that apply under different conditions. For conflicting conclusions under the same conditions, check the sources and identify the correction or replacement. See [Rule ownership and discovery](rule-ownership-and-discovery.md) for placement and navigation.

Make the comparison part of editing and review: the author links related content and explains the choice; the reviewer checks necessity and preservation of conditions. When consolidating, preserve useful rationale, tradeoffs, and what remains unverified, and repair references. Do not assume Git history replaces current explanations readers still need.

For entry pages that receive frequent additions, check the length of named files and require review when they exceed their ceilings. First decide whether the new content belongs elsewhere, then condense it; justify any increase still needed. The ceiling, measurement, and adjustment rationale also need review: passing after changing the configuration does not establish that the new ceiling is appropriate. English whitespace-based word counts do not directly measure Chinese text length.

[Adding and consolidating content](../docs/documentation.md#adding-and-consolidating-content) owns this project's steps and responsibilities. This lesson explains the experience rather than defining a second project policy.

## Case

[DSH commit `aa36b3b36b`: assign standing-document responsibilities and enforce word ceilings](https://github.com/deepseek-ai/deepseek-harness/commit/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a)

- **Problem**: the commit reports that root instructions reached 8,130 words through 50 commits in two and a half weeks. Existing writing rules did not prevent repeated requirements and incident explanations.
- **Approach**: identify the document that maintains each kind of content and set length ceilings in a small manifest of growth-prone files. The check joins documentation checks and CI, failing on excess length or missing listed files. It cannot decide whether rules contradict each other.
- **Evidence**: the [decision record](https://github.com/deepseek-ai/deepseek-harness/blob/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a/docs/rfc/implemented/process/2026-07-04-doc-tiers-and-budgets.md) and [checker](https://github.com/deepseek-ai/deepseek-harness/blob/aa36b3b36bcb46ef3c9d37b23c3145439fd7bf1a/scripts/verify-doc-budgets.ts).

The later [commit `c60eb87860`](https://github.com/deepseek-ai/deepseek-harness/commit/c60eb878601f54ee5a9d32496c7e2237a49643b0) clarifies the response to overflow: relocate, condense, and only then justify raising the ceiling, while retaining at least 5% working headroom. This evolved from the initial approach of freezing ceilings at current sizes.

[DSH commit `3feb05fef8`: consolidate fully superseded decision records](https://github.com/deepseek-ai/deepseek-harness/commit/3feb05fef83a956e73b0a28057c8cd13bebf3dfd)

- **Approach**: allow consolidation of fully superseded records while preserving unique rationale, alternatives, consequences, and what remains unverified. Repair references as part of the consolidation. Partial replacement retains both records and their relationship. The [record policy at that revision](https://github.com/deepseek-ai/deepseek-harness/blob/3feb05fef83a956e73b0a28057c8cd13bebf3dfd/.agents/notes/README.md#when-to-write-one) owns these requirements; word counting does not decide them.

[DSH commit `730bcc7c85`: require lasting decision value before writing a record](https://github.com/deepseek-ai/deepseek-harness/commit/730bcc7c856141e09566c35c835b1109dd6c90a6)

- **Approach**: replace the requirement to record every nontrivial change with a requirement to record only lasting maintenance rationale absent from existing code, tests, and documentation. Extend the existing record for the same decision; keep ordinary changes in the PR or existing documentation. The commit also forbids inventing alternatives to fill a template. This is DSH's decision-record policy; applying it to lesson creation is this project's adaptation.

This project compared the following passages. The judgments came from review, not from an automated checker:

| Comparison sample | Judgment and action |
| --- | --- |
| Ownership, navigation, and word ceilings in this case versus the existing rule-ownership lesson | The existing lesson covers these mechanisms, so Method links to it; this case retains the background needed to explain addition and replacement decisions |
| This lesson's creation criteria versus the previous lesson's maintenance location | They are complementary topics; keep them distinct and add only one owner for project operations in the documentation policy |
| Documentation example type checking versus bilingual consistency | Both validate documentation, but one checks code types and the other checks structure, literal code, and confirmation records; do not merge them into a claim that passing checks proves documentation correct |
| A hypothetical rule allowing automatic merge after checks pass versus the current user-confirmation requirement | They conflict in the same integration scenario; the hypothetical rule was not adopted, and PR policy remains the owner of integration conditions |

This project also follows DSH's approach of setting document length ceilings: the [file manifest](../scripts/doc-budgets.manifest.json) owns fixed ceilings, and the [checker](../scripts/check_doc_budgets.py) runs through `python scripts/check_doc_budgets.py` in [documentation CI](../.github/workflows/docs.yml). The initial manifest covers ten standing entry pages and operational policy files; reviewers still decide whether rules conflict.

The implementation uses the existing Python checking environment. English counts whitespace-separated words; Chinese counts non-whitespace characters so a paragraph is not treated as one word. [Documentation budgets](../docs/documentation.md#documentation-budgets) owns the scope, at least 5% headroom, and adjustment order. Despite the language and counting changes, this retains fixed manifests, failure on excess length or missing files, and review of ceiling adjustments. Neither project size nor the inability to detect rule conflicts automatically was used to omit length checks.

An experiment used the unchanged DSH `ce7073d512` checker with temporary files and a manifest limiting one example file to 10 words. Ordinary short text passed; 11 words and a missing file each failed with exit code 1. Short English text requiring review both always and never still passed. These samples check what the length checker detects and misses; they are not historical DSH incidents.

Verification status: inspected the historical commits above and the policies, skills, checker, and CI call path in local DSH `ce7073d512`. Direct execution of the word-budget checker with Node 24.22.1 passed for seven listed files; the temporary-file experiment verified the four outcomes above. Full DSH documentation checks and its remote CI were not run, and long-term reduction in duplication or conflicts was not measured. This project completed the manual comparisons in the table and implemented the budget check with regression tests that invoke the checker through its command line. The PR verification description supplies actual check results and remote CI status for this change. These manual comparisons do not establish that review detects every conflict.
