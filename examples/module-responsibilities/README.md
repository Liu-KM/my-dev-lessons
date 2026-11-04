# Replacing attention implementations with shared validation

English | [中文](README.zh.md)

This example practices [separating replaceable implementations from shared procedures](../../lessons/module-responsibilities.md), checking responsibilities and dense causal self-attention semantics.

## Run

From the repository root, with Python 3.9 or later:

```sh
python -m pip install -r examples/module-responsibilities/requirements.txt
python -m unittest discover -s examples/module-responsibilities -p 'test_*.py' -v
python examples/module-responsibilities/demo.py
```

The requirements file specifies the NumPy version. CI uses the same installation and test commands; see the checks on the corresponding PR commit for execution results.

## Responsibilities

| File | Responsibility | Change when adding an implementation |
| --- | --- | --- |
| [contract.py](contract.py) | Check input shape, dtype, and finite values | Change only when common requirements change |
| [kernels.py](kernels.py) | Full-matrix and query-chunked calculations, each respecting global causal positions | Add a calculation function without copying the shared experiment |
| [experiment.py](experiment.py) | Validate before calling, time computation, check output shape and dtype | Accept a function parameter without importing a particular kernel |
| [demo.py](demo.py) | Generate inputs, select implementations, compare results | Connect the second implementation here |
| [test_attention.py](test_attention.py) | Independent reference values, fault contrasts, and shared requirements | Apply the same checks to the new implementation |

The interface is the convention that a calculation function accepts Q, K, V and returns an output array, not another service. Calling kernels directly is an internal computation path; the example's public entry is `run_attention`. Implementations needing state, asynchronous execution, or different input shapes require reviewing that interface; this example does not cover them.

Both calculations receive identical float32 inputs of shape [2,4,128,64], seed=7, dropout=0. Queries are chunked by 32, with every chunk reading complete K/V; this remains dense causal attention. Both implementations are independently checked against a per-token float64 reference with fixed rtol=1e-5 and atol=1e-6, then compared with each other. Timing surrounds only the calculation, excluding generation and validation. Without warmup and repeated measurement, it does not establish a speedup.

## Reproducible fault and repair

1. **Original checks**: the [faulty mask](fixtures/block_local_mask.py) passes a reference check with only 32 tokens.
2. **Added scenario**: keep that implementation and tolerance unchanged while increasing input length to 128. Resetting query positions inside each block causes disagreement with the independent reference after a block boundary. The local maximum absolute error was 3.389124662.
3. **Repair**: the current chunked implementation uses global query positions; both implementations pass reference checks. Another input uses zero Q/K and position-valued V, requiring row i to equal the mean of 0..i at 31/32, 63/64, and the final row. A partial final block is checked too.
4. **Evolution of a shared requirement**: the [old validator](fixtures/validation_before.py) checks only shape and dtype, allowing NaN inputs that make both calculations return NaN. Tests temporarily reconnect that same old validator to reproduce the issue. Restoring current common validation rejects the input before either algorithm runs, without separately adding validation to the calculations.

Tests also cover mismatched K/V lengths, unchanged inputs, and shared output checks. Fault fixtures are used only by tests. They demonstrate why checks are needed, not that DSH had an attention defect.

## Verification status

Eight tests passed locally with Python 3.9.7 / NumPy 2.0.0; the demo's maximum absolute difference between outputs was about 5.36e-7. A Sol / medium agent who did not author the change checked the implementation, bilingual documents, and DSH sources, and independently reran the eight tests and documentation checks without finding a behavior blocker. The lesson records DSH sources and adoption differences; see the corresponding PR checks for remote execution results.
