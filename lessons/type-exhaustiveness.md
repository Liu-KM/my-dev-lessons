# Checking for missing branches when categories are added

English | [中文](type-exhaustiveness.zh.md)

## Problem

Adding an event or result category can leave an old handler runnable while it treats the new category as an existing one. For example, cancellation may be counted as reaching the generation length limit. Tests covering only the original categories miss this error.

## Lesson

If a handler must distinguish every valid result, list all result types, give each an explicit branch, and add an exhaustiveness check: a check that every possible category has been handled. Adding a type without its branch then causes a type error.

First determine whether plugins may extend the categories. Exhaustiveness checks suit sets defined by the module that must be handled individually. If an interface permits plugins to add categories, handle unknown categories according to that interface. Typechecking detects omissions, not whether each branch returns the correct value.

## Method

1. Find the type definition and its handlers. Identify categories that require individual handling and those that plugins may extend. Do not ban valid plugin categories just to obtain a passing check.
2. Handle each category explicitly, then call an exhaustiveness assertion. TypeScript's `assertNever` accepts `never`; Python can use `assert_never` with a static checker. If a valid category remains unhandled, its value does not match the assertion's parameter type and checking fails. Annotations alone, executing the program, or throwing a generic exception at the end does not replace this static check.
3. Keep the checker configuration unchanged. Check that the original categories pass; add only a category without changing the handler and require a diagnostic identifying it; then add the branch and require success. An import or syntax failure does not count as detecting an omission.
4. Test each category's return value, displayed text, and counts. Complete branches can still return each other's values by mistake.
5. For extensible interfaces, identify who handles unknown categories. Delegate or ignore them according to the interface, and test that valid extensions take that path.
6. Run the same test command locally and in CI. Add categories in temporary copies and require typechecking to fail because a branch is missing; the test suite itself should succeed. Do not change the checker configuration to hide omissions.

The Python example lists allowed categories with `Literal`, combining strict mypy checks with `typing_extensions.assert_never` to detect omissions after a category addition. A runtime assertion reports unexpected values that bypass typechecking; it does not replace external input validation.

## Case

[DSH commit 370b5d3aab: add exhaustiveness assertions and distinguish closed from extensible types](https://github.com/deepseek-ai/deepseek-harness/commit/370b5d3aab7dd751b95c9988661464d83421579a) adds an exhaustiveness assertion to the stream-chunk assembler. Adding a chunk category without handling it causes a type error. The commit also requires plugin-added categories to follow the extension contract rather than being rejected, and tests runtime diagnostics for values that bypass typechecking.

This repository's [example](../examples/type-exhaustiveness/README.md) first reproduces cancellation being counted as length truncation. It then verifies that the original categories pass, adding only a category fails, and adding its branch restores success. Separate behavior tests check classification and counts, with extensible events as a contrast.

Another agent received neither the author's conversation history nor repaired code. Using the saved lesson draft, it fixed unsupported kernel inputs being counted as success and made future categories without branches cause type errors. All four predeclared checks passed, with task, draft, and configuration hashes unchanged; the example README describes the procedure. There was no comparison without the lesson, so this supports one successful independent use.

Verification status: DSH's historical source and tests were inspected, but its repository was not run. Nine case tests and four independent checks passed locally with Python 3.9.7 and mypy 1.18.2. [PR #19's remote documentation checks](https://github.com/Liu-KM/my-dev-lessons/actions/runs/41767950683) passed on Linux / Python 3.12.15, including the nine case tests. The agent used the draft saved before its trial; it was not run again after this wording revision. Long-term effects in real research remain unverified.
