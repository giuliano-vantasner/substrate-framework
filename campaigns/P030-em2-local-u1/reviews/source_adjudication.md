# Source adjudication: EM2 local U1

## Decision

EM2 is qualified. Its local-covariance and finite-energy winding algebra support
corrected `C-GAU-001`. Its identification of the polar current with EM1 has the
opposite sign from accepted `C-U1-001`; its half-flux minus-one phase is not a
consequence of integer winding; and no gauge kinetic dynamics or physical
electromagnetism is derived.

## Check-family audit

Checks 1, 2, and 9 correctly show that `D_mu=partial_mu-i*e*A_mu` transforms
covariantly under `Psi'=exp(i*e*chi)Psi`, `A_mu'=A_mu+partial_mu chi`, and that
the covariant kinetic term is invariant. P030 upgrades the one-component polar
calculation to arbitrary fields in both 1+1 components, mutates all three linked
signs, and checks a phase-independent potential separately.

Check 3's raw bare-derivative residual is correct. However, for
`Psi=f*exp(i*theta)`, accepted `C-U1-001` gives
`j_mu=-2*f^2*partial_mu theta`, not the source's positive expression. In the
accepted convention the residual is `-e*j_mu*partial_mu chi` plus the quadratic
term.

Check 4 likewise has the correct raw polar cross term but names the opposite
current. With `C-U1-001`, expansion of
`(D_mu Psi)^* D^mu Psi` yields `+e*A_mu*j^mu` plus
`e^2*A_mu*A^mu*|Psi|^2`. P030 fixes the claim and package API at this convention.
Check 10 is a numeric substitution into Check 3, useful regression coverage but
not independent evidence.

Check 5 correctly shows that, conditional on nonzero asymptotic amplitude,
integer phase winding, and the stated logarithmic angular-energy coefficient,
finite energy forces `e*integral A=2*pi*N`. It was imported by EM2; P030 derives
the conditional statement directly and matches the accepted radial-vortex
convention without importing a physical identity.

Check 6 directly evaluates phases for separately inserted integer and
half-integer flux. The finite-energy result uses integer winding, for which the
charge-`e` matter holonomy is always `+1`. A half flux gives `-1` algebraically
but is outside that integer-winding consequence and requires a separate defect,
charge, boundary, or topology premise.

Check 7 differentiates a constant with respect to momentum. Every constant
phase has zero momentum derivative, so this does not make `-1` unique. Check 8
correctly distinguishes zero and one enclosure after declaring half flux, but
it derives no wall, reflection process, or physical Aharonov-Bohm probe.

The displayed ceiling correctly computes zero curvature for a pure-gauge
connection. P030 also supplies a nonzero-curvature connection and proves
`[D_mu,D_nu]Psi=-i*e*F_mu_nu*Psi`. Local symmetry permits every coefficient of
a gauge-invariant `F^2` term, including zero, and therefore does not generate a
Maxwell action, field equation, propagating photon, or force.

## Exact qualification

Accepted content is limited to convention-closed local covariance, invariant
matter algebra, curvature and commutator identities, and conditional integer
winding flux. The source's current label/sign, half-flux derivation,
momentum-uniqueness claim, wall-probe interpretation, emergent electromagnetic
sector, and gauge-force slogan remain outside the claim delta.
