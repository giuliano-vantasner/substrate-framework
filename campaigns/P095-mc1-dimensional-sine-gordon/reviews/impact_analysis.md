# P095 impact analysis

P095 adds two conditional exact claims and one pure symbolic module. It changes
no accepted symbol, existing function signature, numerical solver, normalized
sine-Gordon convention, or material identification.

`C-MED-003` depends on the general constant-multiplier principle in
`C-VAR-001` and the set-local dimension logic of `C-DIM-002`, while deriving
the field-density instance directly. `C-SG-017` depends on `C-MED-003` and the
accepted normalized field, energy, and action in `C-SG-001` through
`C-SG-003`. The new module imports only those normalized APIs and performs no
simulation, output, or numerical quadrature at import time.

Direct governed consumers are the new module, public package exports, focused
tests, P095 primary verifier, independent review, claim registry, release
manifest, generated documentation, and synchronized memory. Focused replay
also covers the normalized sine-Gordon, variational, action-scale, and
constitutive tests.

Hash-pinned MC2, MC3, MC4, engineering, MD, MK, and HE files remain
noncanonical pending units or consumers. P095 edits none of them. They cannot
broaden the conditional model into a material realization or remove the free
coefficient scale. In particular, consumers that use normalized `16*eta` in
physical energy formulas or treat dimensionless `w` as a frequency remain
outside the accepted claim.

P095 is exact symbolic work and introduces no direct NumPy integration call.
Neither the legacy `np.trapz` nor the newer `np.trapezoid` appears; sampled
integration elsewhere remains isolated behind
`substrate_framework.numerics.trapezoid_integral`.
