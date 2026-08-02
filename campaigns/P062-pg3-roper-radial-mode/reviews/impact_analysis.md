# P062 Pre-Change Impact Analysis

The impact boundary was evaluated after refreshing the GitNexus index at
framework commit `d76ebb6` and before editing canonical source.

## Planned Surface

P062 adds a new `radial_modes.py` module and focused tests. It consumes the
existing `solve_ivp_evidence` and `trapezoid_integral` helpers but does not
change their signatures or implementations. No accepted canonical symbol is
renamed or reinterpreted.

## Shared Helper Blast Radius

GitNexus classifies `trapezoid_integral` as CRITICAL if modified: eleven direct
callers, seventeen total impacted symbols through depth three, and eight
affected execution-flow groups. Direct consumers include the Abelian-Higgs
vortex tension, radial harmonic observables, radial sine-Gordon energy and
moment diagnostics, one-dimensional driven evolution, and linearized l=2
energy/moment consumers. The helper is therefore left unchanged. It already
prefers `numpy.trapezoid` under the framework's installed NumPy 2.5.1 and uses
the legacy alias only to retain the declared NumPy 1.26 minimum dependency.

GitNexus classifies `solve_bvp_evidence` as LOW risk: two direct consumers,
`solve_vortex_bvp` and `solve_radial_harmonic_balance`, with two affected
flows. P062 ultimately uses the existing IVP evidence helper for its shooting
route and changes no shared solver helper.

## Decision

The implementation is additive and leaves every pre-existing direct and
transitive consumer unchanged. Targeted replay must cover the new module and
shared numerics tests; the final graph change detector and repository workflow
remain required before promotion.

## Post-Change Detection

After staging the complete promotion surface and refreshing the graph index,
GitNexus maps 206 new or changed symbols across 31 files and assigns MEDIUM
aggregate change risk. The three affected execution flows are all newly added
`solve_option_c_hedgehog` paths: its IVP integration route, its profile-to-
energy sampling route, and its call to the unchanged `trapezoid_integral`
helper. No pre-existing execution flow or canonical symbol is reported as an
affected consumer. This matches the planned additive boundary. The focused
replay covers the new radial API and shared numerics/action-scale consumers;
the full repository workflow remains the final promotion oracle.
