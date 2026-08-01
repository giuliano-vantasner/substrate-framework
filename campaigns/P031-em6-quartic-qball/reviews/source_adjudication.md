# Source adjudication: EM6 quartic Q-ball

## Decision

EM6 is qualified. Its declared quartic stationary ODE has the exact positive
sech family, forced width and amplitude within that nonzero ansatz, and the
accepted-current charge curve recorded as `C-QBL-001`. The source does not
establish VK, spectral, orbital, or nonlinear stability, and it does not force
a complex substrate ontology.

## Check-family audit

Checks 1 through 3 correctly verify the sech residual and its two coefficient
balances. The ODE is not derived from an action in this unit: its provenance
section explicitly declares the small-amplitude quartic reduction and the
stationary ansatz. P031 therefore keeps the entire result conditional on that
dimensionless 1+1 equation. A first-integral rederivation independently fixes
the nonzero peak and recovers the same homoclinic profile.

Check 4's exact charge is correct in `C-U1-001`'s convention. Its numerical
quadrature evaluates an already exact integral and is regression coverage, not
independent evidence. Check 5's derivative is also exact. The charge vanishes
at both frequency endpoints, increases on `(0,1/2)`, reaches 24 at `1/2`, and
decreases on `(1/2,1/sqrt(2))`.

Checks 6 and 9 establish only those slope signs. The source states the VK
criterion but encodes no fluctuation operator, spectrum, negative-mode count,
functional setting, or theorem hypotheses. Sampling the sign cannot upgrade
the exact calculus statement to a stability theorem.

Check 7 is a valid counterprofile guard, though exact center residuals already
reject the Gaussian. Check 8 correctly distinguishes a real field's zero U1
current from the stationary complex field's nonzero density. A charge
definition does not prove that a charged excitation is stable, physically
realized, or the only possible stable object.

Check 10 integrates the same ODE from the exact analytic center data. Its
coarse and fine runs change only `t_eval` sample counts while retaining the
same adaptive DOP853 tolerances; the analytic profile is also used as the
comparison. This is useful solver regression coverage, not an independent
shooting existence result or convergence study.

Check 11 is a Boolean conjunction of zero real current, nonzero complex
current, and sampled negative slope. The load-bearing real-lump instability is
cited rather than checked, applies to `D>=2`, and does not directly adjudicate
the source's declared 1+1 profile. The conjunction consequently cannot force
complex ontology or a physical substrate sector.

## Exact qualification

The shared word “sech” does not identify EM1 and EM6 profiles. EM1 declares
unit amplitude and inverse width `sqrt(1-omega^2)`; EM6's ODE forces amplitude
`sqrt(24)*sqrt(1/2-omega^2)` and a different inverse width. P031 accepts only
the conditional EM6 family and its charge calculus. Stability, forced
ontology, electric charge, particle identity, an exact sine-Gordon solution,
and any substrate realization remain outside the claim delta.
