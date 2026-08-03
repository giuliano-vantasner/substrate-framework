# P089 Impact Analysis

P089 adds one compatible, qualified numerical claim, `C-PDE-011`, and a pure
bulk-forced 1+1 sine-Gordon solver/classifier surface. The accepted release
advances from `v0.76.0` with 104 claims to `v0.77.0` with 105 claims.

Direct code consumers are the expanded `tests/test_sine_gordon_1d.py`, the P089
primary verifier, and its adaptive review. The package exports two bulk-source
evolvers, homogeneous-Dirichlet energy, exact Gaussian-source helpers, and
constrained temporal and phase-space breather fits. Existing periodic and
boundary-driven APIs retain their signatures and tests.

The claim depends on `C-SG-001`, `C-SG-002`, and `C-SG-012`; their closure and
consumers remain unchanged. Generated consumers are the claim documentation,
release documentation, and accepted memory. The source disposition changes SA3
from pending to qualified and regenerates the migration queue.

Hash-pinned external paths SA4, LB3, MC4, `engineering/seeding_kernel.py`, and
`engineering/dbd/pipeline.py` are not edited. SA4 and engineering do not import
SA3. LB3 and MC4 copy local stencils and plant exact initial states, so neither
consumes the promoted source-formation object. Their future migration must use
canonical APIs where relevant and cannot inherit SA3's rejected physical story.

Replay obligations are the P089 scientific verifiers, sine-Gordon and numerics
tests, claim/release/governance/source-inventory tests, generated docs and
memory synchronization, one integrated repository validation boundary, full
pytest, and `git diff --check`. The four-minute half-grid DOP853 route is
preserved as an explicit reproduction record and is not repeated by ordinary
repository validation; this avoids ceremony without weakening the evidence.
