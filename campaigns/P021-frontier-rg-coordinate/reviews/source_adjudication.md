# Source adjudication: EL4 frontier RG coordinate

## Decision

EL4 is qualified. Its declared one-loop flow supports `C-RGE-001`, and its
premise-explicit scale/mass composition supports `C-DIM-005`. It does not derive
the beta function, select a reference scale or coupling, establish its soliton
coefficient to the required numerical standard, fix the free hadronic offset,
or predict an electron mass.

## Check-family audit

EL4.1 reproduces a stable shooting estimate for the source's declared hedgehog
ODE. It does not gate solver success, separate origin/domain/tolerance errors,
report a residual norm, or compare an independent discretization or method.
The simultaneous domain and tolerance change cannot attribute the observed
difference. This remains numerical attempt evidence and neither `b(1)` nor its
physical use is promoted by P021.

EL4.2 verifies the arithmetic identity
`48*pi^3=(12*pi^2)*(4*pi)`. Factorability cannot show that the original
coefficient was derived or contains no free premise; arbitrary numbers admit
factorizations. The physical meanings assigned to the two factors come from
pending or conditional source chains.

EL4.3 contains the exact conditional core accepted as `C-RGE-001`. The declared
flow integrates to
`1/g(mu)^2=1/g0^2+b0*log(mu/mu0)/(8*pi^2)`, with zero
`Lambda=mu0*exp(-8*pi^2/(b0*g0^2))`. The scale is invariant under the total
derivative along that flow. At fixed `g0`, its partial derivative with respect
to `mu0` is `Lambda/mu0`, not zero. P021 makes this semantic boundary explicit.

EL4.4 and EL4.5 give correct conditional orientation and limits: for positive
`b0` and coupling, `Lambda/mu0` lies below one and the reciprocal length ratio
lies above one; reversing the coefficient sign reverses the orientation. The
identifications `mu0=S*c0/a`, `g0^2=beta^2`, and the physical QCD or granularity
readings remain premises.

EL4.6 has the exact generic content accepted as `C-DIM-005`: if
`m*c0^2=q*Lambda` and `mu0=S*c0/a`, then
`N_m=m*c0*a/S=q*exp(-8*pi^2/(b0*beta^2))`. In EL4,
`q=kappa_h/(48*pi^3*b)`. The source explicitly leaves `kappa_h` unpinned and
P021 does not accept `b`; thus `q` is not a derived number. The units check only
establishes that `S*c0/a` is an energy. It cannot establish a particle identity
or choose the dimensionless prefactor.

EL4.7 correctly extracts a coefficient row conditional on the assembled form.
An identical left-hand row adds no new coefficient direction, but consistency
depends on the right-hand offsets. With an unpinned `q`, the source can absorb
any positive target coordinate, so the electron is not an output.

EL4.8 correctly observes that negating one matrix column preserves rank and
nullity. That does not preserve augmented-system consistency, fitted offsets,
or physical solutions unless their transformations are also specified. It
therefore cannot certify all earlier sign-dependent conclusions.

EL4.9 contradicts its narrative with its own matrix: the fabricated
five-by-three system has rank three and nullity zero. It is still full-column-
rank and has more rows than unknowns. The check proves that a column was added,
not that over-determination was destroyed.

EL4.10 is a functioning scanner for a short list of literal values and names.
It is provenance regression evidence, not a semantic dependency inventory and
not evidence that equivalent comparator information or free offsets are absent.

## Exact qualification

Accepted content is limited to the declared one-loop flow solution, its total-
derivative invariant and orientation, and the conditional mass-coordinate
composition with all three dimensionless inputs explicit. EL4 does not derive
QCD's beta function or coefficient, a granularity identification, `b(1)`,
`kappa_h`, an over-determination prediction, an electron mass, or an electron
identity.
