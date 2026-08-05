# P208 Impact Analysis

P208 adds three public symbols to `qball_fluctuations.py` and changes no
existing symbol, signature, convention, solver, or accepted equation. Direct
runtime consumers are the focused tests and P208 verifier.

The new APIs derive the curvature deficit from the existing canonical
potential and retain the separately supplied coupling normalization. They do
not execute simulations at import. Existing Q-ball, overlap, translated-well,
and exact-sine APIs remain unchanged.

The scientific impact is primarily on narrative consumers. GC2 through GC6
may import the accepted local conditional identity, but must not import the
rejected equivalence between pointwise `c(x)` and integrated `y_n`, the
quartic/exact-sine model mix, a no-shallow-bound-state theorem, the RMS
relocation diagnostic, a stability window, or a physical generation and
multisoliton interpretation.

Promotion touches C-QBL-005 in the claim registry, v0.151.0 and `current`, the
GC1 source disposition, generated claim/release/migration documentation,
framework claim/release memory, campaign decision memory, and the durable
migration effort. The 14-node source graph has 107 lexical check calls and 20
assertions, no executable legacy NumPy trapezoid access, and no formal
consumer.
