"""A research prototype's closed internal outcomes."""

from typing import Dict, Iterable, Literal

Outcome = Literal["ok", "error", "unsupported"]


def classify(outcome: Outcome) -> str:
    if outcome == "error":
        return "failed"
    return "passed"


def summarize(outcomes: Iterable[Outcome]) -> Dict[str, int]:
    counts = {"passed": 0, "failed": 0, "unsupported": 0}
    for outcome in outcomes:
        counts[classify(outcome)] += 1
    return counts
