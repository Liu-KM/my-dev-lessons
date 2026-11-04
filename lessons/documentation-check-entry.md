# Keep check commands aligned with execution entries

English | [中文](documentation-check-entry.zh.md)

## Problem

When documentation, pre-push hooks, and CI list checks separately, additions or renames can miss one consumer. A successful exit does not establish that all promised checks ran. Even after implementation is repaired, a review skill can retain obsolete guidance.

## Lesson

Use one script to run checks in order, and invoke it locally and in CI. If a child check fails, the script must also exit unsuccessfully. Separately check whether documentation, hooks, and CI call that script, then deliberately introduce errors to confirm the checks run. Review claims about coverage against the implementation.

## Method

1. Identify the commands used for current operations and the checks each should run. Do not rewrite historical case commands to match the current script.
2. Keep ordering and failure exits in the same script. Document how to run it and invoke it from hooks and CI instead of maintaining separate child-command lists.
3. Mark the current operational command blocks and check that they call the shared script. CI must separately check calls from documentation, CI, and hooks, so replacing the shared script with a child check does not bypass that check as well.
4. In disposable copies, run the original code, deliberately broken code, and restored code; record exit codes and diagnostics. Require the diagnostic to identify the introduced error rather than an environment failure.

The project's operating policy is in [documentation checks](../docs/documentation.md#documentation-checks). The shared entry covers Python documentation checks only; CI retains its existing formatting and link steps. Calls are checked using the agreed fixed format; arbitrary shell or YAML is not parsed, and this does not establish that the workflow triggers. Deleting the checker and all its callers together also bypasses it. Reviewers still need to inspect coverage, prerequisites, and changes to the checker itself.

## Case

[DSH commit fa7d1df6f2: share doc-sync between local hooks and CI](https://github.com/deepseek-ai/deepseek-harness/commit/fa7d1df6f2c6dbbae32ecbaf0fb8275c407b8828) combined documentation code-block and event-name checks previously run only in CI into one script and connected it to pre-push. One definition avoids updating two check lists; earlier execution reduces failures found only after pushing. Typechecking still needs previously built declaration files; sharing a command does not generate missing files.

[DSH commit bcfff6f1ee: correct stale review-skill coverage](https://github.com/deepseek-ai/deepseek-harness/commit/bcfff6f1ee47990a1609d517280a18ea21f35fe1) explains that automated checks can still miss errors in prose: reviewers must inspect explanations of configuration, defaults, and error codes. This case did not automatically detect obsolete documentation commands across the repository.

This project reuses its Python environment for a shared script and uses `check_doc_entry.py` to check calls from documentation, CI, and hooks. It retains DSH's shared local-hook/CI script and nonzero exits on failure, and additionally checks two operational documentation blocks, CI steps, and hook content. These call checks were added by this project, not by the DSH case.

Fault experiments use disposable repository copies: a misspelled documentation command must fail validation of these calls; a missing required lesson section must fail the shared entry; replacing the CI entry with a child check must fail the separate check of these calls. Restore each original file and rerun the shared entry. The regression suite avoids recursively invoking itself; child processes still run the other existing tests.

All three experiments returned baseline 0, fault 1, and restored 0. The misspelled command reported the expected shared command; the missing section reported the affected lesson's structure error; CI bypass reported the missing unconditional shared-entry step. Repairs restored original bytes rather than weakening rules or refreshing pairing records to hide faults.

Verification status: DSH historical commits inspected; the local shared entry and 58 tests passed, including the three fault-and-repair experiments. Disabling the CI step and deleting a documentation marker were also rejected. A Git push dry-run against a temporary local repository triggered the real hook, passed all checks, and exited 0 without pushing. See [PR #10](https://github.com/Liu-KM/my-dev-lessons/pull/10) for remote checks and their corresponding commits; the hook is not permanently installed.
