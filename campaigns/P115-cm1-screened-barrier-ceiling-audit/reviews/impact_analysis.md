# P115 impact analysis

P115 adds the self-contained `screened_barrier` module and provisional
C-SCR-001. It changes no existing canonical symbol. GitNexus was refreshed
with `--index-only`; upstream impact for `inverse_sqrt_barrier_factor` at depth
three reports two direct callers inside the same new module, one affected
module, zero affected processes, and low risk. Change detection reports no
pre-existing canonical change.

The source graph has five direct pending consumers and no indirect consumer
after excluding cycle returns to CM1. CM3 uses a generic monotone surrogate and
incorrectly replaces the positive shifted floor by zero. CM7 algebraically
inverts the actual factor against a free dimensionless constant. CM6, GB6, and
WN7 use lexical presence or tagged citations. None receives a physical rate,
yield, material bound, or observation from C-SCR-001.

Direct canonical consumers are the module's enhancement and ledger functions,
the focused package tests, P115's primary verifier, governance, generated
documentation, and accepted memory. Promotion replay must cover these paths
and preserve every pending source disposition.
