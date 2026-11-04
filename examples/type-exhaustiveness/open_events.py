"""An open extension point delegates events outside its owned vocabulary."""

from typing import Callable


def route_event(kind: str, extension: Callable[[str], str]) -> str:
    if kind == "measurement":
        return "built-in measurement"
    # Extension-owned events are valid inputs; the caller supplies their handler.
    return extension(kind)
