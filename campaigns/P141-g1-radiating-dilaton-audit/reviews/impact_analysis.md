# P141 impact analysis

P141 adds the pure `retarded_wave.py` module, root-package exports, and focused
tests. It changes no accepted sine-Gordon, optical-geometry, Maxwell, numeric,
unit, or historical-campaign API. Imports perform no simulation or output.

After refreshing the GitNexus index, upstream impact for both new public
functions is LOW: zero preexisting callers, zero affected modules, and zero
affected execution processes. The repository process inventory contains eight
small verifier flows and none uses the new objects. `detect_changes` sees the
existing `__all__` symbol as the only tracked changed symbol and reports LOW
risk with no affected process; direct git status and `rg` remain authoritative
for the new untracked module, tests, and campaign records.

The semantic nonduplication query finds the new P141 objects as the only exact
retarded-action match. Nearby `sine_gordon_1d.py` and `maxwell.py` definitions
cover driven numerical evolution or static Maxwell point sources, not the
canonical scalar action-to-two-sided-retarded-flux ledger and same-equation
static countermodel.

The frozen source graph covers G1, G2, G3, T2A, and all 27 direct reverse
consumers. All 31 hashes and 339 static predicates are pinned; the 73-check
graph replay passes. Fourteen qualified consumers retain independent accepted
closures, eleven pending consumers gain no authority, and two duplicate units
remain duplicate evidence.

Seven immutable nodes have legacy NumPy integration shapes and retain
alias-only replay paths backed by `np.trapezoid`. Mutable P141 and framework
code has no executable `np.trapz` access. G1 itself passes all ten predicates
after compatibility replay, so its scientific rejection is not a version
failure.

Focused package tests pass 75 checks, the primary verifier passes 37, the fresh
independent derivation passes 29, and the graph passes 73. Final implementation
risk is LOW; the remaining replay is the claim, release, disposition, generated
state, memory, and single integrated validation transaction.
