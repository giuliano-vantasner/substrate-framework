# P091 Impact Analysis

P091 adds one compatible qualified claim, `C-SG-016`, and exact pure breather
kinetic, damping-form-factor, phase-averaged trajectory, instantaneous-time,
and integrated-e-fold APIs. Existing sine-Gordon signatures are unchanged.

The claim depends on `C-SG-001`, `C-SG-002`, `C-SG-003`, and `C-SG-012`.
Direct governed consumers are `tests/test_sine_gordon.py`, the P091 primary and
independent verifiers, and the damped-PDE review using existing C-PDE-011-era
solver machinery. Generated consumers are claim and release documentation,
accepted memory, and migration inventory. LB1 changes from pending to qualified.

Hash-pinned LB2, LB3, LB4, `engineering/lifetime_kernel.py`,
`nucleation_efficiency_model.py`, and `engineering/dbd/pipeline.py` are not
edited. LB2's small-amplitude convention remains viable; all other assertions
in those pending or noncanonical consumers require their own adjudication.

Replay obligations are P091's three scientific verifiers, focused sine-Gordon
and governance tests, generated docs and memory synchronization, one integrated
repository validation boundary, full pytest, and `git diff --check`. Exact work
uses no quadrature, independent field evidence uses adaptive SciPy quadrature,
and sampled PDE ledgers use the shared `trapezoid_integral` compatibility helper
rather than a version-specific NumPy alias.
