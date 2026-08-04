# P140 impact analysis

P140 adds a pure `hls_reduction.py` module and root-package exports. It does
not change C-EFT-001 elimination machinery, C-CHI-001 coordinate identities,
C-SK-001 mass-formula algebra, numeric solvers, units, or any historical
campaign. The new APIs require exact inputs and perform no simulation or
output at import time.

After indexing the frozen working base, GitNexus reports LOW upstream impact
for `eliminate_quadratic_field`: one direct internal caller and no affected
execution process. The semantic query finds no preexisting HLS current-wedge
API. `detect-changes` reports LOW risk, one tracked `__all__` symbol, and no
affected process; direct git status remains authoritative for the new untracked
module and campaign records.

The frozen source graph covers S4, its pending B1 dependency, and eleven
reverse consumers. All thirteen hashes and all 123 static predicates are
pinned; the 31-check graph replay passes. S4 has no NumPy compatibility event.
B1's immutable dynamic/eager legacy-name shape remains classified for
alias-only replay backed by `np.trapezoid`; no mutable P140 code uses the
removed name.

Focused package tests pass 44 checks, the primary verifier passes 36, and the
fresh independent derivation passes 25. Four qualified consumers retain
independent accepted closures and seven pending consumers gain no authority.
Final risk is LOW; the remaining replay is the claim/release/disposition and
generated-state transaction followed by one integrated gate.
