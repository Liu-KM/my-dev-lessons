# Keep check commands aligned with execution entries

English | [中文](documentation-check-entry.zh.md)

## Problem

When documentation, pre-push hooks, and CI list checks separately, additions or renames can miss one consumer. A successful exit does not establish that all promised checks ran. Even after implementation is repaired, a review skill can retain obsolete guidance.

## Lesson

Let one executable entry own the check sequence and have local checks and CI invoke it, propagating failure. Check the documentation and CI connections explicitly, then inject faults to verify the real entry. Review descriptions of coverage against implementation.

## Method

1. Identify the operational commands and coverage in scope; do not rewrite historical case commands to match current entries.
2. Let the shared entry own ordering and failure exits. Document that command and invoke it from hooks and CI instead of maintaining separate child-command lists.
3. Mark the current operational command blocks and compare them with the shared entry. Run the wiring check independently in CI so replacing the shared entry does not also bypass its own check.
4. Record baseline, fault, and restored results in disposable copies. Assert the specific diagnostic so an environment error cannot count as detecting the intended fault.

The project's operating policy is in [documentation checks](../docs/documentation.md#documentation-checks). The shared entry covers Python documentation checks only; CI retains its existing formatting and link steps. Wiring checks use a fixed format, not a general shell or YAML analyzer. They do not establish that the workflow triggers or prevent simultaneous deletion of the checker and all its callers. Review must still inspect coverage, prerequisites, and changes to the enforcement mechanism itself.

## Case

[DSH commit fa7d1df6f2: share doc-sync between local hooks and CI](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828) combined documentation code-block and event-name checks previously run only in CI into one script and connected it to pre-push. One definition avoids updating two check lists; earlier execution reduces failures found only after pushing. Built declarations remain a type-check prerequisite: sharing a command does not eliminate environment differences.

[DSH commit bcfff6f1ee: correct stale review-skill coverage](https://github.com/deepseek-ai/deepseek-harness/commit/bcfff6f1ee47990a1609d517280a18ea21f35fe1) explains that existing checks do not protect all documentation semantics: reviewers still inspect prose about configuration, defaults, and error codes. This case did not implement repository-wide command drift detection.

This project reuses its Python environment for a shared entry and fixed wiring checks, preserving shared local-hook/CI execution and failure exits. It additionally checks two operational documentation blocks, CI steps, and hook content. These wiring checks are this project's application, not a DSH mechanism.

Fault experiments use disposable repository copies: a misspelled documentation command must fail wiring validation; a missing required lesson section must fail the shared entry; replacing the CI entry with a child check must fail independent wiring validation. Restore each original file and rerun the shared entry. The regression suite avoids recursively invoking itself; child processes still run the other existing tests.

All three experiments returned baseline 0, fault 1, and restored 0. The misspelled command reported the expected shared command; the missing section reported the affected lesson's structure error; CI bypass reported the missing unconditional shared-entry step. Repairs restored original bytes rather than weakening rules or refreshing pairing records to hide faults.

Verification status: DSH historical commits inspected; the local shared entry and 58 tests passed, including the three fault-and-repair experiments. Disabling the CI step and deleting a documentation marker were also rejected. A Git push dry-run against a temporary local repository triggered the real hook, passed all checks, and exited 0 without pushing. See [PR #10](https://github.com/Liu-KM/my-dev-lessons/pull/10) for remote checks and their corresponding commits; the hook is not permanently installed.
