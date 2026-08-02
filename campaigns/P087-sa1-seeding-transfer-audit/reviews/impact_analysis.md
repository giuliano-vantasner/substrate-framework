# P087 Impact Analysis

P087 adds no new dynamical symbol and changes no accepted convention. It adds
three pure sine-Gordon APIs: the fixed-position arctangent amplitude, the exact
fixed-position fundamental sine coefficient, and its core specialization.
Their only accepted dependency is C-SG-001's normalized rest breather.

Direct consumers are `tests/test_sine_gordon.py`, the P087 primary verifier,
and the C-SG-015 review. Package-root exports, the claim registry, release
manifest, generated claim index, accepted memory, migration queue, and parent
effort are indirect consumers. C-SG-009 and C-SG-010 remain unchanged because
they describe the even energy second moment rather than the breather field
trace.

The hash-pinned external `engineering/seeding_kernel.py` is audited, not
modified. Its replay fails under current NumPy at a direct `np.trapz` call, and
its scientific normalization remains unclosed. Rungs 174 and 175 retain their
inserted Michaelis triggers and do not import SA1. Consequently no external
engine, susceptibility, seeding population, breakdown law, or nuclear channel
enters C-SG-015's dependency closure.

Replay consists of both exact P087 routes, the focused sine-Gordon tests,
governance/source-inventory tests, generated-state validation, and one
integrated unchanged-boundary gate. The failed external replay is durable
negative consumer evidence rather than an accepted consumer obligation.
