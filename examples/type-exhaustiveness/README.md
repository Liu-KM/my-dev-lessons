# Checking for missing branches when categories are added: examples

English | [中文](README.zh.md)

This example checks the [lesson](../../lessons/type-exhaustiveness.md): reproduce a default branch misclassifying a new category, confirm that typechecking detects the omission, then test repaired return values and counts. The cases use constructed data, not a real inference service or GPU experiment.

## Run

At the repository root, use an isolated Python 3.9 or newer environment:

```sh
python -m pip install -r examples/type-exhaustiveness/requirements.txt
python -m unittest discover -s examples/type-exhaustiveness -p 'test_*.py' -v
```

Files in this directory specify dependency versions and mypy configuration. Documentation checks do not need these dependencies; a separate CI step installs them and runs the same test command.

## Classifying cancellation

| Step | Change | Expected result |
| --- | --- | --- |
| Reproduce the error | A default branch treats cancellation as length truncation | Typechecking passes, classification and counts are wrong |
| Add an exhaustiveness check | Handle the original two categories | Typechecking passes |
| Check detection of omissions | Add only cancellation without changing the handler | mypy reports unhandled cancellation |
| Repair | Add the cancellation branch | Typechecking passes, return values and counts are correct |

The fixtures directory retains teaching versions from before repair, not business implementations. Tests add categories in temporary copies, keep the checker configuration unchanged, and require diagnostics identifying the omitted category and argument-type error. The suite passes only after verifying these expected failures.

Other tests check that unexpected values bypassing typechecking fail at runtime, and that extensible events reach the plugin handler rather than being rejected as invalid categories.

## Another agent's use of the lesson

Kernel-test outcomes include correct execution, execution failure, and unsupported input. The old code counts every non-failure as success, including inputs never executed. The task requires correct counts and a type error when a future category is added without its branch.

Before the trial, the author saved a Chinese lesson draft, task, broken example, and mypy configuration, defined four checks, and recorded material hashes. A GPT-6.1 Sol / medium agent received neither author conversation history nor repaired code. Its task restricted reading to those materials and allowed repairing the example and recording results. This was an instruction-based reading limit, not operating-system file-access isolation.

The author's predeclared checks found two failures in the old code: unsupported input counted as success, and adding a category caused no type error. The agent's repair passed all four checks, with hashes of three read-only materials unchanged. This directory retains code before and after repair; three regression tests recheck incorrect counts, repaired results, and the diagnostic for a future category. These tests rerun existing code without calling an agent.

The agent used the draft saved before the trial and was not run again after this wording revision. There was no comparison without the lesson, so this confirms one successful independent use, not whether the lesson improves problem-solving ability. It is a trial, not a mandatory step for all lessons.

## Verification status

Nine case tests and four independent checks passed locally. Remote CI has not run. Passing typechecking and correct branch meanings need separate verification; these constructed data do not represent real performance or paper conclusions.
