# QCD5 source adjudication

QCD5 is qualified through existing accepted claims, not accepted wholesale.
Native execution passes all seven source predicates, but that tally does not
validate the headline because the decisive source check substitutes equation
count for constraint rank.

The exact retained content is the standard fundamental SU3 half-trace metric,
the shared Riesz force exponent `2s-d-1`, the conditional specialization
`s=1 -> d=3`, the fixed-`s` uniqueness inside that supplied family, and the
useful counterexample `s=3/4 -> d=5/2`. These are accepted composition of
C-LIE-003, C-NVP-002, C-KRN-001, and C-KRN-002.

The alleged three-sector overdetermination does not survive. QCD5 constructs
all simultaneous equations by calling the same `force_exp_shared` function.
At fixed `s=1`, the coefficient matrix is `[[1],[1],[1]]` with equal right-hand
side, coefficient and augmented rank one, and two row dependencies. One row
already gives the same unique conditional solution `d=3`. With both `d` and
`s` free, the matrix has three copies of `[1,-2]`, rank one, nullity one, and
solution family `d=2s+1`. C-LIN-001 therefore classifies the system as
overdetermined by count only; the named sectors do not add constraint
directions or independent provenance.

The color amplitudes do not repair this. QCD5 has three labels but only two
amplitude values, and no amplitude enters a constraint row. Its fabricated
`kappa(d)` guard differentiates `log G` with respect to `d`; a nonzero
dimension-dependent amplitude changes that sensitivity but leaves the radial
potential and force exponents unchanged. A radial factor such as `r**alpha`
does change the exponent and is the relevant contrast. The source supplies no
sector-specific operator, measurement, geometry, dimension-changing map, or
independent endpoint selection.

The retroactive D3S annotation receives no authority. Accepted C-KRN-002 and
the qualified D3S record preserve the endpoint-selection ceiling; QCD5 itself
hard-codes `no_sg_derivation_of_s = True`. Pending MD1 remains individually
queued and cannot inherit `d=3` authority from QCD5. OD and duplicate AS4 use
actual explicit matrix rank and nullity machinery and need no QCD5 headline.

Decision: qualify QCD5 through C-LIE-003, C-NVP-002, C-KRN-001, C-KRN-002,
and C-LIN-001 without a new claim, API, or release. Retain its exact shared
formula and supplied-input substitutions. Do not promote independent
three-sector constraints, overdetermination of dimension, endpoint selection,
geometry, dimensional lift, gauge-sector realization, or substrate mechanism.

The primary, fresh independent, and frozen-graph routes pass 32, 14, and 20
checks; 46 focused accepted-API tests pass. The graph distinguishes 91 lexical
check sites from 99 runtime executions across eight hash-pinned units. QCD5 is
native; immutable YM2 and QCD2 use compatibility aliases backed only by
`np.trapezoid`. No canonical code changes, and campaign debt is empty at the
no-release boundary.
