"""Input rules shared by every self-attention implementation in this example."""

import numpy as np


def validate_inputs(q, k, v):
    for name, array in (("Q", q), ("K", k), ("V", v)):
        if array.ndim != 4 or array.dtype != np.float32:
            raise ValueError(f"{name} must be a rank-4 float32 array")
        if any(size <= 0 for size in array.shape):
            raise ValueError(f"{name} dimensions must be positive")
    if q.shape != k.shape or q.shape != v.shape:
        raise ValueError("Q, K and V must have the same self-attention shape")
    for name, array in (("Q", q), ("K", k), ("V", v)):
        if not np.isfinite(array).all():
            raise ValueError(f"{name} must contain only finite values")
