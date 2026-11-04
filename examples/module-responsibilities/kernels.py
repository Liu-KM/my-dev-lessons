"""Two CPU calculations of the same dense causal self-attention."""

import numpy as np


def _softmax(scores):
    weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
    return weights / weights.sum(axis=-1, keepdims=True)


def dense_attention(q, k, v):
    scores = (q @ k.swapaxes(-2, -1)) * np.float32(q.shape[-1] ** -0.5)
    future = np.triu(np.ones((q.shape[-2], k.shape[-2]), dtype=bool), k=1)
    return _softmax(np.where(future, -np.inf, scores)) @ v


def chunked_attention(q, k, v, chunk_size=32):
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    output = np.empty_like(q)
    keys = k.swapaxes(-2, -1)
    key_positions = np.arange(k.shape[-2])
    for start in range(0, q.shape[-2], chunk_size):
        end = min(start + chunk_size, q.shape[-2])
        scores = (q[..., start:end, :] @ keys) * np.float32(q.shape[-1] ** -0.5)
        query_positions = np.arange(start, end)[:, None]
        scores = np.where(key_positions > query_positions, -np.inf, scores)
        output[..., start:end, :] = _softmax(scores) @ v
    return output
