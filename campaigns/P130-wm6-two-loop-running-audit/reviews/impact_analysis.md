# P130 Impact Analysis

The pre-edit graph was refreshed at freeze commit `2cf2bb5`. The proposed
`solve_three_factor_boundary_running` symbol did not exist. The accepted
`gauge_only_beta` surface had zero upstream callers and LOW risk, so the planned
change was additive rather than a symbol migration.

The implementation adds `gauge_running.py`, package exports, focused tests, and
campaign verifiers. It calls the accepted `GaugeCoefficientLedger` and shared
status-gated IVP helper; no existing canonical API is renamed or removed.

The source dependency replay covers WM3 and WM5 for 21 checks. Later WM8 and
WM10 replay 17 checks from pinned bytes. They remain pending, and their boundary,
composition, comparator, and physical conclusions are excluded from C-RGE-006.

Generated consumers are the claim index, accepted memory, release manifest, and
migration queue. They are regenerated only in the claim-level transaction. No
quadrature or NumPy integration alias is affected.

The post-edit graph was refreshed with the new module and campaign surfaces.
`solve_three_factor_boundary_running` has zero upstream callers, zero affected
processes, and LOW direct impact. The indexed change detector reports no hidden
consumer change. Promotion therefore adds a new API and generated consumers
without migrating or silently changing an accepted symbol.
