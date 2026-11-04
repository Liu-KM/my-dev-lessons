# Separating replaceable implementations from shared procedures

English | [中文](module-responsibilities.zh.md)

## Problem

When code owns both a shared procedure and one particular implementation, replacing an algorithm, storage backend, or model provider can also affect validation, error handling, and result organization. Copying the whole procedure instead creates multiple copies of common logic to keep synchronized.

These mixed responsibilities create coupling: parts that should change independently have to change together. As features accumulate, the affected code grows with each change.

For example, reading data in the same format from object storage instead of a local file becomes more involved when reading, parsing, and statistics share one function, making it harder to change only the reading mechanism.

## Lesson

**Divide responsibilities according to why they change, separating replaceable implementations from procedures that must remain consistent.** Implementations determine how the work is done; callers use them through a shared agreement. Replacing an implementation and revising the common procedure then have distinct places to change.

An interface here is the agreement on inputs, outputs, and error behavior that both sides follow, expressed through functions or types. This applies separation of concerns to capabilities that need different implementations.

## Method

Start with an actual change and distinguish code that varies by implementation from requirements that need shared maintenance:

| Part | Responsibility |
| --- | --- |
| Interface | Define the inputs, outputs, and error behavior the caller needs |
| Implementation | Perform the particular calculation, storage operation, or external-service call |
| Caller | Organize the task and use implementations through the interface |

Choose the split according to actual replacement needs. Test it with two changes: replace an implementation while the caller continues using the same agreement; revise a common requirement and have all implementations adopt it through the same entry point. When a new implementation exposes an incomplete agreement, update the interface, caller, and tests together.

## Case

[DSH commit 8b5a3ef730: separate the Bash interface, implementation, and tool caller](https://github.com/deepseek-ai/deepseek-harness/commit/8b5a3ef7300e5b100c66268f9c761c660172b298) separates execution conventions, local-process operations, and model-facing tools. Tools depend on the execution interface, which the local executor implements; the split follows independent replacement needs.

[DSH commit ab19fed77c: introduce two LLM adapters and complete error handling](https://github.com/deepseek-ai/deepseek-harness/commit/ab19fed77c4b744f4447d72de0dfd59dca7c82a3) also updates core handling and tests for errors reported within a stream while integrating the implementations, completing the shared agreement.

This repository's [attention example](../examples/module-responsibilities/README.md) replaces calculations through function arguments and maintains the shared procedure in Python modules: `run_attention` owns validation, timing, and output checks; two calculation functions implement their respective algorithms. Adding NaN rejection to shared validation stops both before execution while leaving calculation functions unchanged. Results are separately checked against independent reference values. Attention serves as a validation case for the general method.

Verification status: DSH evidence comes from reading historical source and tests. Eight CPU case tests passed with Python 3.9.7 / NumPy 2.0.0.
