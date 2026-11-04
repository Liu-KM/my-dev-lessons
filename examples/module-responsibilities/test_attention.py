"""Check numerical semantics and a real change to the shared input rules."""

from pathlib import Path
import runpy
import unittest
from unittest.mock import Mock, patch

import numpy as np

import experiment
from kernels import chunked_attention, dense_attention

ROOT = Path(__file__).resolve().parent
IMPLEMENTATIONS = (dense_attention, chunked_attention)


def inputs(length=128):
    rng = np.random.default_rng(7)
    return tuple(rng.standard_normal((2, 4, length, 64)).astype(np.float32)
                 for _ in range(3))


def per_token_reference(q, k, v):
    # Different mask construction and higher precision than either kernel.
    q64, k64, v64 = (array.astype(np.float64) for array in (q, k, v))
    output = np.empty(q.shape, dtype=np.float64)
    for index in range(q.shape[-2]):
        scores = np.einsum("bhd,bhkd->bhk", q64[..., index, :], k64[..., :index + 1, :])
        scores /= q.shape[-1] ** 0.5
        weights = np.exp(scores - scores.max(axis=-1, keepdims=True))
        weights /= weights.sum(axis=-1, keepdims=True)
        output[..., index, :] = np.einsum("bhk,bhkd->bhd", weights, v64[..., :index + 1, :])
    return output


class AttentionTests(unittest.TestCase):
    def test_both_implementations_match_independent_reference(self):
        q, k, v = inputs()
        expected = per_token_reference(q, k, v)
        for implementation in IMPLEMENTATIONS:
            with self.subTest(implementation=implementation.__name__):
                actual = experiment.run_attention(implementation, q, k, v).output
                np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-6)

    def test_partial_last_block_matches_reference(self):
        q, k, v = inputs(length=65)
        actual = chunked_attention(q, k, v, chunk_size=31)
        np.testing.assert_allclose(actual, per_token_reference(q, k, v), rtol=1e-5, atol=1e-6)

    def test_injected_mask_fault_passes_one_block_but_fails_across_blocks(self):
        broken = runpy.run_path(str(ROOT / "fixtures" / "block_local_mask.py"))["attention"]
        q, k, v = inputs(length=32)
        np.testing.assert_allclose(broken(q, k, v), per_token_reference(q, k, v),
                                   rtol=1e-5, atol=1e-6)
        q, k, v = inputs()
        expected = per_token_reference(q, k, v)
        with self.assertRaises(AssertionError):
            np.testing.assert_allclose(broken(q, k, v), expected, rtol=1e-5, atol=1e-6)
        error = float(np.max(np.abs(broken(q, k, v) - expected)))
        print("Injected block-local mask: max absolute error", error)
        np.testing.assert_allclose(chunked_attention(q, k, v), expected, rtol=1e-5, atol=1e-6)

    def test_global_positions_at_block_boundaries(self):
        q = np.zeros((2, 4, 128, 64), dtype=np.float32)
        k = np.zeros_like(q)
        v = np.broadcast_to(np.arange(128, dtype=np.float32)[None, None, :, None], q.shape).copy()
        expected = np.broadcast_to((np.arange(128) / 2)[None, None, :, None], q.shape)
        for implementation in IMPLEMENTATIONS:
            actual = experiment.run_attention(implementation, q, k, v).output
            np.testing.assert_allclose(actual, expected, rtol=1e-5, atol=1e-6)
            for index in (31, 32, 63, 64, 127):
                self.assertAlmostEqual(float(actual[0, 0, index, 0]), index / 2, places=5)

    def test_mismatched_kv_lengths_rejected_by_common_caller(self):
        q, k, v = inputs()
        for implementation in IMPLEMENTATIONS:
            with self.subTest(implementation=implementation.__name__):
                with self.assertRaisesRegex(ValueError, "same self-attention shape"):
                    experiment.run_attention(implementation, q, k[..., :-1, :], v)
                with self.assertRaisesRegex(ValueError, "same self-attention shape"):
                    experiment.run_attention(implementation, q, k, v[..., :-1, :])

    def test_new_finite_rule_applies_before_both_kernels(self):
        old = runpy.run_path(str(ROOT / "fixtures" / "validation_before.py"))["validate_inputs"]
        q, k, v = inputs(length=8)
        q[0, 0, 0, 0] = np.nan
        for implementation in IMPLEMENTATIONS:
            with self.subTest(implementation=implementation.__name__):
                with patch.object(experiment, "validate_inputs", old):
                    before = experiment.run_attention(implementation, q, k, v)
                    self.assertTrue(np.isnan(before.output).any())
                spy = Mock(wraps=implementation)
                with self.assertRaisesRegex(ValueError, "Q must contain only finite values"):
                    experiment.run_attention(spy, q, k, v)
                spy.assert_not_called()

    def test_inputs_not_mutated(self):
        for implementation in IMPLEMENTATIONS:
            q, k, v = inputs(length=8)
            snapshots = tuple(array.copy() for array in (q, k, v))
            experiment.run_attention(implementation, q, k, v)
            for array, saved in zip((q, k, v), snapshots):
                np.testing.assert_array_equal(array, saved)

    def test_output_shape_and_dtype_checked_by_common_caller(self):
        q, k, v = inputs(length=8)
        for invalid in (lambda *args: q[..., :-1, :], lambda *args: q.astype(np.float64)):
            with self.assertRaisesRegex(ValueError, "output must preserve"):
                experiment.run_attention(invalid, q, k, v)


if __name__ == "__main__":
    unittest.main()
