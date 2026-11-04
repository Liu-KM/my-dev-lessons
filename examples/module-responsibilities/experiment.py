"""The common caller knows the callable interface, not a particular kernel."""

from dataclasses import dataclass
from time import perf_counter

import numpy as np

from contract import validate_inputs


@dataclass
class Result:
    output: np.ndarray
    kernel_seconds: float


def run_attention(implementation, q, k, v):
    validate_inputs(q, k, v)
    start = perf_counter()
    output = implementation(q, k, v)
    elapsed = perf_counter() - start
    if output.shape != q.shape or output.dtype != np.float32:
        raise ValueError("attention output must preserve Q shape and float32 dtype")
    return Result(output, elapsed)
