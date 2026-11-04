"""Compose two implementations with the same experimental procedure."""

import numpy as np

from experiment import run_attention
from kernels import chunked_attention, dense_attention


def main():
    rng = np.random.default_rng(7)
    q, k, v = [rng.standard_normal((2, 4, 128, 64)).astype(np.float32)
               for _ in range(3)]
    dense = run_attention(dense_attention, q, k, v)
    chunked = run_attention(chunked_attention, q, k, v)
    np.testing.assert_allclose(chunked.output, dense.output, rtol=1e-5, atol=1e-6)
    print("shape:", q.shape, "dtype:", q.dtype, "chunk_size: 32, dropout: 0")
    print("max absolute difference:", float(np.max(np.abs(dense.output - chunked.output))))
    print("kernel-only seconds:", dense.kernel_seconds, chunked.kernel_seconds)
    print("CPU teaching example; these timings do not establish a speedup.")


if __name__ == "__main__":
    main()
