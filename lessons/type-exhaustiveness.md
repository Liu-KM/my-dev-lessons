# Checking for missing branches when categories are added

English | [中文](type-exhaustiveness.zh.md)

## Problem

When a new result requires different handling, an old function may still run while assigning it to an existing category. For example, an experiment report needs to distinguish cancellation from reaching the generation length limit. If old code counts every unsuccessful result as length truncation, adding cancellation produces incorrect counts, while tests of the old categories miss the omission.

## Lesson

First establish which results require different handling, then express that requirement in types and add an exhaustiveness check: a check that every possible category has been handled. Adding a type without updating its handler should identify the omission; completing the branch restores success. Deliberately omitting a branch verifies the check, while actual requirements establish whether the category is needed.

First determine whether plugins may extend the categories. Exhaustiveness checks suit sets defined by the module that must be handled individually. If an interface permits plugins to add categories, handle unknown categories according to that interface. Typechecking detects omissions, not whether each branch returns the correct value.

## Method

1. **Establish the requirement**: trace results from production through handling to report output. Identify why each category needs different handling and who maintains its type definition and handler. A closed set requires individual handling; an extensible interface also needs an agreed recipient for unknown categories.
2. **Express the requirement**: list valid results, handle each explicitly, and finish with an exhaustiveness assertion. TypeScript's `assertNever` accepts `never`; Python can use `assert_never` with a static checker. Any remaining valid category does not match the assertion's parameter type, producing a type error. Executing the program or throwing a generic exception does not replace this static check.
3. **Expose and close the gap**: keep the checker configuration unchanged and confirm the old categories pass. Add only a category justified by the requirement, leaving the handler unchanged, and require a diagnostic identifying the missing category. Complete the branch and require success. This deliberately creates a handling omission; an import or syntax error does not meet the acceptance condition.
4. **Verify behavior**: check return values, displayed text, and counts separately, since complete branches can still behave incorrectly. Delegate or ignore plugin-added categories according to the interface and test that path. Run the same command locally and in CI, preserving omission rejection and repaired acceptance in temporary copies; the suite itself exits successfully.

The Python example lists allowed categories with `Literal`, combining strict mypy checks with `typing_extensions.assert_never` to detect omissions after a category addition. A runtime assertion reports unexpected values that bypass typechecking; it does not replace external input validation.

## Case

[DSH commit 370b5d3aab: add exhaustiveness assertions and distinguish closed from extensible types](https://github.com/deepseek-ai/deepseek-harness/commit/370b5d3aab7dd751b95c9988661464d83421579a) adds an exhaustiveness assertion to the stream-chunk assembler. Adding a chunk category without handling it causes a type error. The commit also requires plugin-added categories to follow the extension contract rather than being rejected, and tests runtime diagnostics for values that bypass typechecking.

This repository's [example](../examples/type-exhaustiveness/README.md) starts from the requirement to count cancellation separately from length truncation. The old default branch misclassifies cancellation, and tests of the old categories miss the omission. The example first establishes exhaustiveness for the old categories, then adds only cancellation, making mypy report the missing branch. Completing that branch restores success; behavior tests check classification and counts, with extensible events as a contrast. This is the reproducible sequence of this repository's experiment, not a claim about the DSH author's development order.

Another agent received neither the author's conversation history nor repaired code. Using the saved lesson draft, it fixed unsupported kernel inputs being counted as success and made future categories without branches cause type errors. All four predeclared checks passed, with task, draft, and configuration hashes unchanged; the example README describes the procedure. There was no comparison without the lesson, so this supports one successful independent use.

The DSH evidence comes from historical source and test inspection; its repository was not run. The original case passed nine tests and four independent checks locally with Python 3.9.7 and mypy 1.18.2. [PR #19's remote documentation checks](https://github.com/Liu-KM/my-dev-lessons/actions/runs/41767950683) passed on Linux / Python 3.12.15, including the nine case tests. The agent used the draft saved before its trial; it was not run again after this wording revision. Long-term effects in real research remain unverified.
