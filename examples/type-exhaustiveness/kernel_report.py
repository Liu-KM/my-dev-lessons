"""A research prototype's closed internal outcomes."""

from typing import Dict, Iterable, Literal

from typing_extensions import assert_never

Outcome = Literal["ok", "error", "unsupported"]


def classify(outcome: Outcome) -> str:
    if outcome == "ok":
        return "passed"
    if outcome == "error":
        return "failed"
    if outcome == "unsupported":
        return "unsupported"
    assert_never(outcome)


def summarize(outcomes: Iterable[Outcome]) -> Dict[str, int]:
    counts = {"passed": 0, "failed": 0, "unsupported": 0}
    for outcome in outcomes:
        counts[classify(outcome)] += 1
    return counts
