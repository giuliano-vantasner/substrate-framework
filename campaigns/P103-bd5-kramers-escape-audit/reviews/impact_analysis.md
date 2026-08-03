# P103 Impact Analysis

## Change Surface

P103 adds `first_passage.py`, additive package exports, focused tests, and
campaign/governance artifacts. It does not rename or alter an accepted
canonical equation. The stochastic process remains an explicit conditional
input rather than a modification of the radial, collective, thermal, or
coherence sectors.

## Graph Analysis

The GitNexus index was refreshed at preregistration commit `9e56fc5` before the
result was trusted. Upstream impact for `reflected_absorbing_mfpt` is LOW: zero
pre-existing impacted symbols, zero affected modules, and zero affected
execution flows. Worktree change detection identifies only the existing
package `__all__` symbol because the new module and tests have no baseline
graph identity; it reports zero affected processes and LOW risk. The repository
process inventory contains no first-passage execution flow. After staging the
complete promotion, final change detection resolves ninety-four changed graph
symbols across forty files, zero affected existing symbols, zero affected
processes, and LOW risk.

## Scientific Consumers

The direct governed consumers are the additive package exports, fourteen
focused tests, and the two P103 verifiers. Accepted radial, collective,
thermal, coherence, and probability claims are compatibility anchors rather
than callers. Pinned BD5 and legacy scripts are immutable predecessor or
narrative evidence; none imports the new API.

## Quadrature Compatibility

The canonical exact route uses SciPy adaptive quadrature and has no sampled
NumPy integration call. The only sampled legacy MFPT consumer already uses
`np.trapezoid`. No mutable or immutable consumer aborts on `np.trapz`, so no
version-only compatibility failure is misclassified as scientific evidence.

## Risk and Replay

The code risk is LOW and additive. The interpretation risk is material because
inverse MFPT, completed-only inverse time, restricted mean, hazard, and
asymptotic rate are different objects. The promotion gate therefore replays
the exact and independent verifiers, focused dependency tests, structured
evidence validation, one integrated repository workflow, generated state, and
final worktree impact detection.
