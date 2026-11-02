# Type checking for documentation code examples

English | [中文](docs-example-typecheck.zh.md)

## Problem

API examples in documentation are code, but ordinary CI usually compiles only designated source and test files. It does not automatically extract code blocks from Markdown. After an interface changes, calls in the source may be fixed while documentation examples still use the old interface.

“Remember to update the docs when changing code” relies on contributors finding every affected example. As documentation becomes more scattered, memory alone becomes less reliable.

## Lesson

Include compilable documentation examples that depend on project APIs in type checking, and run it continuously in CI so that incompatible interfaces produce failures pointing to the affected examples.

## Method

1. Extract explicitly marked code examples from Markdown and check them against the project's current packages and types.
2. Map errors back to document locations so developers know which examples need attention.
3. Use the same check entry point locally and in CI to prevent the two implementations from drifting apart.
4. Supply necessary imports and helper declarations for partial examples. Explicitly skip illustrative pseudocode and review whether each exclusion is justified.

Prioritize examples that readers will copy and that depend on project APIs. This type checking produces no release artifacts and does not fix documentation automatically. It checks type compatibility; runtime behavior requires executing examples or tests. Explanations and recommended usage still need review.

## Case

[DSH commit `204c36ed76`: integrate documentation example type checks and event table checks into CI](https://github.com/deepseek-ai/deepseek-harness/commit/204c36ed7631c482a0d3843029dced160b417099)

- **Problem**: TypeScript examples in documentation were outside type checking, leaving reviewers to detect incompatibilities caused by API changes.
- **Solution**: Add `doc-typecheck` to extract Markdown `ts` code blocks and check them with `tsc --noEmit`; supply necessary imports and helper declarations, and connect the checks to local pre-push and CI through `doc-sync`.
- **Evidence to inspect**: The [check script](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/scripts/doc-typecheck.ts) implements extraction, compilation, and error reporting; the [decision record](https://github.com/deepseek-ai/deepseek-harness/blob/204c36ed7631c482a0d3843029dced160b417099/docs/adr/0014-doc-sync-enforcement.md) explains scope and tradeoffs.

Related case: [Commit `2b447625fa`](https://github.com/deepseek-ai/deepseek-harness/commit/2b447625fa0d7d04aa97095dbb2fa42e82f3aa9b) corrected an inaccurate README description of `registerAdapter([])` and replaced `args: any` in a tool example with type inference through `defineTool`. These discrepancies also show the limits of automated checks: inline code in tables is outside extraction, and explicit `any` may not produce a type error. Review remains necessary.

Verification status: We read DSH's historical fixes, decision record, and check implementation, but did not run the historical checks or measure their effectiveness. This project has not implemented documentation example type checking; its bilingual consistency checks do not validate example types either.
