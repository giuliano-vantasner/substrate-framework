# P099 impact analysis

P099 adds a conditional capillary constitutive surface to the existing radial
energy module. The new APIs expose the relative capillary barrier, declared
Frank/core line tension, declared quadratic area drive, composed radius and
barrier, monomial dimension family, exact identifiability ranks, constructive
drive-preserving rescalings, and state-dependent Frank/core sensitivities.
They are exported from the package root and covered by focused tests.

The existing `capillary_critical_radius` now returns the exact quotient without
an outer `simplify`; `capillary_barrier_height` follows the same representation.
This preserves additive constitutive subexpressions that SymPy would otherwise
rewrite as logarithms of symbolic powers. The mathematical value and domain do
not change. Repository search found direct consumers only in radial-energy
tests, P006, and the new P099 composition. P006's 28-check verifier and all
radial-energy tests replay successfully.

The accepted downstream transaction adds C-RG-002, release `v0.84.0`, generated
claim and release documentation, accepted memory, the qualified BD1 migration
disposition, and the immutable P099 campaign. No accepted formal theorem,
numeric solver, sampled integration, or material module changes.

Pinned predecessor consumers are recorded in `evidence/consumer-audit.yaml`.
The core source consumer reproduces 16 checks, but BD2-BD5, CM2, CM4, NY3, and
the engineering DBD pipeline remain pending, qualified, or noncanonical. They
cannot inherit a rate, population, material, temperature, isotope, nuclear, or
output-power claim from C-RG-002.

P099 is exact symbolic work and imports no NumPy. It introduces neither
`np.trapz` nor `np.trapezoid`; no quadrature compatibility decision is needed.
