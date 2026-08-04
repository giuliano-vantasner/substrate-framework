# P142 impact analysis

P142 adds the pure `gordon_metric.py` module, root-package exports, and focused
tests. It changes no accepted optical, sine-Gordon, stress, curvature, numeric,
unit, or historical-campaign API. Imports execute no simulation and print no
output.

After refreshing the GitNexus index, upstream impact for
`gordon_metric_mostly_plus` is LOW: its only direct caller is the new
`transverse_profile_einstein` function, with one affected module and zero
execution processes. Upstream impact for `transverse_profile_einstein` is LOW
with zero preexisting callers, modules, or processes. The semantic query finds
the new P142 definitions as the exact Gordon matches; nearby accepted optical
and sine-Gordon stress definitions do not duplicate the metric or tensor.

The frozen source graph covers G2, its three declared dependencies, and all 28
direct reverse consumers, with C1 correctly counted once as both dependency and
consumer. All 31 hashes and 325 static predicates are pinned; the 74-check graph
replay passes. Fourteen qualified consumers retain independent closures,
twelve pending consumers gain no authority, and two duplicate consumers remain
duplicate evidence.

Eight immutable graph nodes have legacy NumPy integration shapes and retain
alias-only replay paths backed by `np.trapezoid`. G2 itself has no integration
compatibility event, and mutable P142 and framework code has no executable
`np.trapz` access.

Focused package tests pass 15 checks, the primary verifier passes 29, the fresh
independent tensor reconstruction passes 16, and the graph passes 74. Final
implementation risk is LOW; the remaining replay is the claim, release,
disposition, generated state, memory, and single integrated validation
transaction.
