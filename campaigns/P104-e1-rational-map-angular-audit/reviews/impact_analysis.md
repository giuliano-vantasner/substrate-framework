# P104 Impact Analysis

## Change Surface

P104 adds `rational_maps.py`, additive package exports, focused tests, and
campaign/governance artifacts. It renames or changes no accepted canonical
symbol and alters no accepted equation. The new APIs operate only on explicitly
supplied rational-map polynomial coefficients and declared quadrature orders.

## Graph Analysis

The GitNexus index was refreshed after the implementation was present. Upstream
impact for both `exact_rational_map_degree` and
`rational_map_sphere_integrals` is LOW: zero pre-existing impacted symbols,
zero affected modules, and zero affected execution flows. Worktree detection
identifies the existing package `__all__` as the only changed baseline symbol,
with zero affected processes and LOW risk. After staging the complete
promotion, final change detection resolves sixty-seven changed graph symbols
across forty indexed files, zero affected existing symbols, zero affected
processes, and LOW risk.

## Scientific Consumers

The governed consumers are the pure module, additive exports, eleven focused
tests, and the two P104 verifiers. Accepted B=1 radial, mass-cancellation,
winding, and dimensional claims are compatibility ceilings rather than callers.
Pinned later source files duplicate the old integral instead of importing the
new API and remain pending evidence.

## Quadrature Compatibility

Canonical cubature is tensor Gauss-Legendre and contains neither `np.trapz` nor
a direct `np.trapezoid` dependency. E1 executes its current `np.trapezoid`
branch and does not suffer a version-only abort. No new mutable script uses the
removed alias.

## Risk and Replay

Code risk is LOW and additive. Interpretation risk is material because map
degree, global minimization, radial energy, topological charge, nuclear identity,
and yield are distinct obligations. Promotion therefore requires exact and
independent verifier replay, focused tests, structured-evidence validation, one
integrated repository workflow, regenerated state, and final change detection.
