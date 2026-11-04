"""Closed internal finish reasons: every category needs an explicit meaning."""

from typing import Dict, Iterable, Literal
from typing_extensions import assert_never

FinishReason = Literal["eos", "max_tokens", "cancelled"]


def classify(reason: FinishReason) -> str:
    if reason == "eos":
        return "generated"
    if reason == "max_tokens":
        return "length_limit"
    if reason == "cancelled":
        return "cancelled"
    assert_never(reason)


def summarize(reasons: Iterable[FinishReason]) -> Dict[str, int]:
    counts = {"generated": 0, "length_limit": 0, "cancelled": 0}
    for reason in reasons:
        counts[classify(reason)] += 1
    return counts
