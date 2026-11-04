"""Intentionally wrong: a newly admitted category becomes length_limit."""

from typing import Literal

FinishReason = Literal["eos", "max_tokens", "cancelled"]


def classify(reason: FinishReason) -> str:
    if reason == "eos":
        return "generated"
    return "length_limit"
