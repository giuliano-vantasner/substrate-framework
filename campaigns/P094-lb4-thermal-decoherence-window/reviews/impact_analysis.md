# P094 impact analysis

P094 extends the existing coherence-gates module with exact conditional
Brownian-phase APIs and adds claim `C-COH-002`. It changes no accepted symbol,
existing function signature, numerical solver, or physical convention.

The direct accepted dependency is `C-COH-001`, which supplies the static
Gaussian phase characteristic and pair-coherence semantics. `C-DYN-001`
supplies only the declared deterministic coordinate-amplitude envelope used in
the explicitly conditional product. `C-SG-016` is replayed as a ceiling on
fixed-lifetime interpretation; its statement and implementation are unchanged.

Direct governed consumers are the extended pure module, focused tests, P094
primary verifier, independent stochastic review, claim registry, release
manifest, generated documentation, and synchronized memory. The P086
coherence verifier and damped-oscillator tests cover unchanged dependencies.

Hash-pinned coherence-array, lifetime, nucleation, DBD, and synthesis modules
are narrative or engineering consumers, not accepted authority. P094 does not
edit them. Their pair-factor, survival, accumulation, population, and event
interpretations remain noncanonical because they do not close the stochastic
or physical map.

The exact promoted work uses symbolic Gaussian and elementary integration. It
introduces no direct NumPy quadrature call, including neither `np.trapz` nor
the newer `np.trapezoid`. Existing sampled integration remains isolated behind
`substrate_framework.numerics.trapezoid_integral`.
