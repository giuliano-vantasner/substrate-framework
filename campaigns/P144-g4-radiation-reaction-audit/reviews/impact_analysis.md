# P144 impact analysis

The change adds `generalized_dissipation.py`, its public exports, focused
tests, and campaign-only evidence. No existing canonical symbol is renamed or
given a new contract.

After refreshing the GitNexus index, upstream impact for
`metric_power_balance` is LOW: its only direct caller is the new
`scalar_power_balance_force`, with no affected execution process.
`rayleigh_dissipation` has no direct indexed caller outside the new validation
surface and is also LOW. The process registry contains only unrelated campaign
run-to-check flows.

`detect_changes(scope=all)` reports low risk and no affected process. It maps
the tracked `__all__` edit but does not enumerate untracked new files, so that
result is not treated as a complete oracle. Exact primary and independent
verifiers, the focused package suite, repository validation, and full pytest
cover the new files directly. The generated GitNexus Claude files and appended
AGENTS block were removed; only the refreshed index remains as tool state.

Direct consumers are the new scalar specialization, tests, and P144 verifier.
Indirect consumers are the package import surface and generated claim
documentation after promotion. No accepted numerical, formal, or scientific
consumer changes meaning.

Risk: LOW. The additive API is exact-input guarded, rejects ambiguous zero-rate
and non-positive-matrix domains, and states its physical ceiling in the module,
claim, tests, and campaign review.
