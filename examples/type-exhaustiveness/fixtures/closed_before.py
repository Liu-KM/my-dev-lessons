"""Protected baseline before the third internal category is introduced."""

from typing import Literal
from typing_extensions import assert_never

FinishReason = Literal["eos", "max_tokens"]


def classify(reason: FinishReason) -> str:
    if reason == "eos":
        return "generated"
    if reason == "max_tokens":
        return "length_limit"
    assert_never(reason)
