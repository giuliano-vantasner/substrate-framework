# P063 Pre-Change Impact Analysis

The impact boundary was evaluated at framework commit `756c264` after the
P063 candidate and convention contract was frozen and before opening PG4's
executable or editing canonical source.

## Existing Surface Search

GitNexus finds no existing canonical axial-current, PCAC, pion-pole, or
Goldberger--Treiman execution flow. Its semantic query returns only unrelated
Lorentz-kinematic, STF, WZW, and campaign symbols. P063 therefore requires an
additive module rather than a reinterpretation of an accepted current API.

## Nearby Convention Helpers

The nearest accepted helper is `leading_exponential_kinetic_metric`, whose
upstream impact is LOW: one direct caller,
`su2_trace_breaking_evidence`, and no indexed execution flow. The conditional
GMOR helper also has LOW impact with no direct caller or affected process.
P063 may read their conventions and ceilings but will not modify either
function, because neither a scalar kinetic metric nor a declared GMOR equation
is an axial-current form-factor theorem.

## Process Review and Decision

The indexed process list contains no axial-current flow. The implementation
boundary is additive: a new exact module, focused tests, and thin campaign
verifiers. Existing C-SYM/C-CHI/C-GMR symbols, generated consumers, and shared
verification helpers remain unchanged. A post-change graph refresh and
`detect_changes` result must confirm that only new Ward-identity flows and
their tests are affected before promotion.

## Post-Change Detection

After staging the complete promotion surface and refreshing the index,
GitNexus reports 196 new or changed indexed symbols across 29 files with
MEDIUM aggregate risk. The only four affected execution flows are new
`pion_pole_remainder_evidence` paths through
`generalized_axial_ward_evidence`, `on_shell_axial_divergence`, and the new
local validation helpers. No pre-existing canonical flow or accepted symbol
is an affected consumer. This matches the planned additive boundary; the
focused replay covers every new path and the repository workflow remains the
final promotion oracle.
