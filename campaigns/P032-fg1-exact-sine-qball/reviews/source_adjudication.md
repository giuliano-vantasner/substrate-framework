# Source adjudication: FG1 exact-sine reconciliation

## Decision

FG1 is qualified. Its declared exact-sine stationary ODE supports the unique
implicit homoclinic family, accepted-current charge quadrature, and controlled
quartic limit promoted as `C-QBL-002`. It neither identifies EM1's envelope
with that family nor proves a VK-stable physical charged soliton.

## Check-family audit

The unmodified source passes A through E and then fails in F at removed
`np.trapz`. A compatibility-only alias lets all eight checks execute, but it
does not repair the scientific issues below and is not source reproduction.

Check A uses the exact peak relation and two genuine DOP853 maximum-step
budgets on a shared local interval. The agreement is useful solver regression,
but same initial data and local ODE uniqueness do not independently establish
global existence. P032 instead proves that
`(1-cos(f))/f^2` decreases from one-half to zero on `(0,2*pi)`, giving a unique
first peak, positive orbit square below it, and an exact inverse quadrature.

Check B correctly derives the quartic truncation. Check C fits one frequency;
P032 replaces that point fit with the scaled differential equation, scaled
peak balance, and shrinking peak/charge ratios. The exact result is a
controlled limit to `C-QBL-001`, not equality at finite amplitude.

Check D correctly rejects EM1's envelope width: it misses the quartic balance
by exactly one-half. The unit-amplitude EM1 envelope also fails the exact-sine
ODE. These facts contradict the headline assertion that EM1 and EM6 are the
same profile at two truncations. EM1 remains a declared parameterized envelope.

Check E is an exact ratio of two accepted conditional formulas. Calling that
ratio an amplitude deficit is algebraic bookkeeping between different widths
and amplitudes; it does not identify the fields, equations, or objects.

Check F is not promotable. Beyond the removed NumPy call, its long forward IVP
tracks a homoclinic separatrix from a floating-point peak. At `omega=0.6` the
trajectory eventually rebounds to another full peak and the source-domain
integral is three times the independently evaluated first-orbit charge
quadrature. The slope signs happen to agree on its samples, but the charge is
not the localized one and no fluctuation operator or VK theorem hypotheses are
encoded. Stability therefore remains unverified.

Check G is a valid counterprofile, though the exact residual already rejects
the Gaussian. Check H correctly reproduces the accepted sine-Gordon breather
envelope identity and `eta^2-kappa^2=1/2`; it is provenance and distinction
evidence rather than a reconciliation identity.

## Exact qualification

Accepted content is limited to the conditional exact first integral, unique
first positive peak, implicit localized branch, finite charge quadrature, and
quartic small-amplitude limit. Closed-form profile claims, EM1/EM6 object
identity, the source's numerical charge curve, VK or nonlinear stability,
electric charge, particle identity, and substrate ontology remain outside the
claim delta.
