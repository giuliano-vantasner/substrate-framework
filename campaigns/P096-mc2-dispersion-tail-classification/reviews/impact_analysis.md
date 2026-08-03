# P096 impact analysis

P096 extends the existing dimensional sine-Gordon module without changing an
accepted symbol, equation, convention, coefficient definition, or prior claim.
The new APIs are pure exact-symbolic functions; imports execute no simulation
and print no tally.

The direct changed consumers are `src/substrate_framework/__init__.py`,
`tests/test_dimensional_sine_gordon.py`, the P096 primary verifier, and its
independent review. The accepted dependencies replayed are the normalized
sine-Gordon, lattice scalar, and radial harmonic-tail tests. C-MED-003 and
C-SG-017 remain unchanged: the former owns the physical coefficients and
scales, while the latter owns nonlinear breather existence and observables.

Indirect consumers MC3, MC4, MD1, MD2, `medium_omega0.py`,
`lifetime_kernel.py`, `seeding_kernel.py`, and `commensurate.py` were
hash-pinned and classified. They remain pending or noncanonical because they
add material maps, simulation assumptions, 3-D measures, cutoffs, quantum
premises, damping, deposition spectra, or design identifications. In
particular, an oscillatory branch is named `oscillatory` in the canonical API;
calling it radiative remains the responsibility of a consumer that supplies
and verifies an outgoing condition or directed flux.

The migration disposition changes only MC2 from pending to qualified and maps
it to C-SG-018. The release adds exactly C-SG-018. Generated documentation,
accepted memory, release memory, and the migration queue must be regenerated
from those authoritative records. No formal theorem, numerical solver,
generated source file, or accepted consumer requires a symbol migration.

The direct `np.trapz` calls found in the immutable external
`engineering/seeding_kernel.py` are recorded as evidence for that consumer's
future adjudication. P096's exact code has no NumPy dependency or trapezoidal
alias, so this observation creates no unresolved debt in C-SG-018.
