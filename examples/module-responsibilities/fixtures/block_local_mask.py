"""Injected fault: query positions restart at zero in every block."""

import numpy as np


def attention(q, k, v, chunk_size=32):
    output = np.empty_like(q)
    for start in range(0, q.shape[-2], chunk_size):
        end = min(start + chunk_size, q.shape[-2])
        scores = (q[..., start:end, :] @ k.swapaxes(-2, -1)) * np.float32(q.shape[-1] ** -0.5)
        # Wrong after the first block: missing the global start position.
        mask = np.arange(k.shape[-2]) > np.arange(end - start)[:, None]
        scores = np.where(mask, -np.inf, scores)
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights /= weights.sum(axis=-1, keepdims=True)
        output[..., start:end, :] = weights @ v
    return output
