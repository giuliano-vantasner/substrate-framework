# P075 Impact Analysis

P075 changes no accepted claim, canonical symbol, package API, release member,
formal theorem, or generated claim document. It adds one campaign consumer of
the existing exact linear-system and scale-constraint APIs and changes only
AS4's migration disposition plus the generated queue.

The direct reusable surfaces are `diagnose_linear_system`,
`diagnose_log_constraints`, and `generalized_least_squares`. Existing consumers
found by repository search are their focused tests, P022, P065, and later
scale-audit campaigns. P075 calls the APIs without modifying their signatures,
data classes, conventions, or return semantics. The 78 tests covering linear
systems, scale constraints, transmutation, and induced gravity pass unchanged.

The only generated consumer is `migration/source-claims.yaml`, regenerated
from `migration/dispositions.yaml`. Accepted claim docs and release memory must
remain byte-current under the unchanged `v0.68.0` registry. There are no Lean
consumers and no numerical or quadrature paths. The final replay therefore
includes both P075 exact routes, the affected focused tests, repository
governance/inventory tests, one integrated validation boundary, and a diff
check.
