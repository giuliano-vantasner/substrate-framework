---
name: small-ratio-numerics
description: Deterministic, runner-independent numerical evidence for small-ratio regimes (soft modes, tiny splittings, weak forces). Use whenever a check compares numbers smaller than 1e-3 relative, reports lambda_min or near-zero crossings, subtracts nearly equal energies, or runs through multiple executors (.py, importlib, run_scipy, harness agents).
---

# Small-Ratio Numerics

Use this skill when the quantity of interest is a small difference, a soft eigenvalue, or a weak force extracted from a computation whose dominant scale is orders of magnitude larger. It encodes two layers of standard: an execution-determinism contract (a result must not depend on who ran it) and an evidence-discipline contract (a small ratio must not be trusted because one grid produced it).

The motivating failure, measured in this repository: the certified energy evaluator returns `56.22021310789286` with 1 BLAS thread and `56.22021310789277` with 2+ threads — bit-stable per setting, different across settings, purely from floating-point reduction order. Any pipeline that amplifies last-bit noise (root-finding on stiff residuals, eigenvalue sign calls, chained continuations) turns that 1.6e-15 relative difference into a different answer depending on whether the script was run directly or imported by a harness. A check that passes as `.py` and flips under `run_scipy` is not a flaky test; it is a check whose acceptance gate sits below the runner-noise floor.

## Layer 1 — determinism contract

Every numeric artifact must carry its execution context, and every load-bearing check must be shown runner-independent:

1. Pin and record the thread environment (`torch.set_num_threads`, `OMP_NUM_THREADS`/`MKL_NUM_THREADS`) at module level — never inside an `if __name__ == "__main__"` block, so imports see it too. Record the setting in the result file.
2. Seeds, constants, and dtype declarations go at module level for the same reason. No RNG may influence an accepted claim; if sampling is unavoidable, save and commit the sampled inputs.
3. Measure the runner-noise floor once per evaluator: run the same evaluation under at least two thread counts and both invocation paths (direct `.py` and importlib). The floor is the largest observed deviation. Quote it next to every acceptance tolerance.
4. Runner-equivalence gate: an acceptance tolerance must exceed the measured noise floor by at least two orders of magnitude, or the check must be made insensitive (see layer 2). A discrepancy beyond tolerance marks all dependent results gate-invalid — do not average, re-run until lucky, or silently keep the direct-run answer.
5. Iterative pipelines (continuation ladders, root-finding, bisection on eigenvalue signs) inherit the floor of every step. Their outputs are runner-dependent unless each step's residual convergence is driven well below the floor or the final result is re-validated independently of the chain.

## Layer 2 — evidence discipline in the small-ratio regime

Adapted from issue #155 (small ratios, soft modes, weak long-range forces); the ordering below is the labour-saving device:

1. Never extract a small quantity as the difference of large numbers without an independent handle on the cancellation error. State the subtraction's relative error budget before believing the result. Prefer formulations where the weak term appears directly (pairing of asymptotic moments over `E(R) - 2E_1`; component-wise second derivatives over two-radius matrix differences).
2. Treat a single-grid sign or magnitude as necessary, never sufficient: report `lambda_min` together with `lambda_2` (or the full relevant spectrum gap), the mesh/domain scaling of the value, and where the eigenvector lives (bulk mode versus boundary/mesh artifact).
3. Cross-validate on at least one axis the result does not control: independent quadrature, independent discretization, doubled nodes, or a second extraction method. Acceptance = reproduction within a tolerance tied to the measured noise floor and the operation's conditioning, not to aspiration.
4. Under-resolved solutions manufacture spurious stationary points that reproduce their own solving-grid values. Any root accepted into a ladder must survive re-evaluation on an independently chosen grid.
5. Monitors close claims: conservation or identity residuals (virial/Derrick-type, topological charge, exact algebraic identities) must close at the accuracy being claimed, or the claimed accuracy is withdrawn.
6. Classify honestly: results that fail these gates stay in the record labeled gate-invalid with the failing mechanism named. Failures become mechanisms; they never become quiet retractions or quiet promotions.

## Reporting format

Numerical-check records should state: question; evaluator and its certification status; execution context (thread pins, versions, invocation path); measured noise floor; acceptance tolerances and their rationale; cross-validation performed; verdict; and artifact paths. Use the `numerical-check` memory template for the durable record.

## Non-goals

This skill does not govern symbolic work (exact arithmetic has no noise floor), nor claim governance (promotion/review stays with the physics loop), nor performance engineering. It applies only where double precision meets small ratios.
