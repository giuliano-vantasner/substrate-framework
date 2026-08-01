# Source adjudication: CF4 dimensional transmutation

## Decision

CF4 is qualified. Its RGE solution, formal inverse-coupling zero, and total RG
invariance are duplicate evidence for `C-RGE-001`. Its single-scale dimensional
argument supports narrow `C-DIM-007`. Its conditional coefficient examples map
to `C-RGE-002`. The headline assertion that asymptotic freedom and confinement
are two limits of one perturbative running is rejected.

## Check-family audit

CF4.1 exactly integrates the declared one-loop ODE and is already the first
sentence of `C-RGE-001`. The alternative alpha parameterization is algebraic
rewriting, not a new claim.

CF4.2 exactly locates the zero of the one-loop inverse coupling and is already
accepted in `C-RGE-001`. Calling that formal boundary a dynamically generated
mass scale is acceptable only within the declared one-loop model; the
calculation does not control the coupling at the boundary.

CF4.3 correctly computes a zero *total* derivative when the reference coupling
runs. `C-RGE-001` already records both this result and the nonzero fixed-coupling
partial derivative. P025 additionally verifies that reversing the flow sign
destroys the cancellation.

CF4.4 has a valid but narrower content than its narrative suggests. Conditional
on an independently existing tension of mass dimension two and Lambda being
the only dimensionful mass scale, the unique monomial power is two:
`sigma=k*Lambda^2`. The dimensionless `k` is free and load-bearing. With another
independent mass scale `M`, the exponent family
`Lambda^(2-q)*M^q` is dimensionally allowed. Dimensional analysis derives
neither existence nor positivity of a tension and does not calculate `k`.

CF4.5 correctly finds the ultraviolet zero and divergence at the formal
one-loop boundary. Renaming the latter “confinement” is an invalid implication.
The running expression contains only the coupling, coefficient, and scale; it
has no Wilson loop, area law, flux tube, string tension, static potential, mass
gap, or other nonperturbative oracle. Both zero and positive tension assignments
are compatible with the identical checked one-loop equations.

CF4.6 correctly shows that changing the beta-coefficient sign moves the formal
zero from below to above the reference scale. It does not prove that the
positive-sign case confines or that every negative-sign theory lacks every
possible infrared mechanism. The accepted content is pole placement only.

The NumPy limit sweep is regression coverage because the exact rational limit
already fixes its output. It earns no independent evidence and is unnecessary
for promotion.

## Exact qualification

Accepted content is limited to duplicate `C-RGE-001`, conditional coefficient
composition with `C-RGE-002`, and the premise-explicit `C-DIM-007` exponent
theorem. Physical confinement, a nonzero string tension, a calculated
dimensionless prefactor, perturbative control at Lambda, and an absolute scale
remain outside the claim delta.
