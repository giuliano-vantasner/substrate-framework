# PN4 source adjudication

PN4 reproduces twenty-seven runtime predicates from twenty-two static check
sites at the pinned source hash. It uses NumPy and SciPy for finite matrices and
time propagation but no sampled integration, so no `np.trapz` compatibility
event occurs.

Its central finite-matrix identity is correct under its declared
specialization. For intermediate energies `+Delta-i*Gamma/2` and
`-Delta-i*Gamma/2`, equal coupling product `c`, spectral energy `E=0`, and the
convention `H_PP+H_PQ*(E*I-H_QQ)^-1*H_QP`, one pair contributes
`-i*c*Gamma/(Delta^2+Gamma^2/4)`. The exact energy-dependent expression is
`2*c*(E+i*Gamma/2)/((E+i*Gamma/2)^2-Delta^2)`.

The cancellation is conditional. At zero loss but nonzero `E`, the pair is
`2*c*E/(E^2-Delta^2)`. At `E=0`, unequal complex coupling products leave
`(c_minus-c_plus)/Delta`. Positive loss does not produce a monotone opening:
the magnitude vanishes at both zero and infinite loss and peaks at
`Gamma=2*abs(Delta)`.

The source's `L=3` to `L=6` comparison adds intermediate states while keeping
each state coupling fixed. It is model enlargement, not mesh, domain,
timestep, or tolerance refinement. A fixed-total product convention produces
no pair-count growth.

The time-domain prose is stronger than its predicate and its own output. The
source reports nonzero zero-loss peak `|B|^2 = 2.629e-3`. Independently, the
lossless full Hamiltonian has `(H^2)_BA=2*L*g^2`, hence a nonzero second-order
short-time transfer amplitude even though the `E=0` effective element
cancels. Under positive loss, `exp(-iHt)` is nonunitary and the raw component
`|B|^2` is not a normalized conditional or trace-preserving probability.

H5a is a correct two-by-two basis-rotation identity, but it derives no
composite or nuclear map. H5b checks a Boolean import marker. H7 scans three
constructed literals and self-tests that scanner; it cannot close scientific
provenance or derivation. The named arXiv v2 record does not explicitly retract
the earlier claim, so PN4's stronger retraction wording is not retained.

PN4 is therefore qualified. C-RES-001 receives only the exact declared finite
complex resolvent theorem. It establishes no microscopic loss, Lindblad
dynamics, physical channel, population, probability, rate, nuclear or phonon
mechanism, material realization, magnitude, or observation. Eight direct and
sixteen indirect pending consumers inherit only this ceiling. The PN4-PN5
candidate cycle supplies no authority.
