# Source adjudication: HE4 action-variable bridge

## Decision

HE4 is qualified. Its classical action and Legendre identities map to accepted
`C-SG-003/004`. P011 adds the exact secant-scale classification `C-SG-006` and
the consequences of a separately imposed fixed action lattice as `C-SG-007`.
HE4 does not derive quantum discretization, a renormalized coupling map, charge
reciprocity, or a literature spectrum in the framework's conventions.

## Check-family audit

HE4.1 is duplicate period evidence for `C-SG-001`. HE4.2–HE4.5 reconstruct the
phase-space integrand and use high-precision quadrature to recover the canonical
action. `C-SG-003` already has an exact endpoint-fixed derivation and an
independent field phase-space construction, so HE4's numerical route is
regression evidence rather than a third independent oracle. HE4.6 and HE4.7
repeat the accepted action-angle derivative and inverse map.

HE4.8 substitutes the declared lattice `J=n*hbar_q` into the accepted inverse
map. The sine energy follows exactly and is retained conditionally in
`C-SG-007`. The declaration does not derive a quantum rule, a value of
`hbar_q`, or its identification with a renormalized coupling. HE4.9's finite
cutoff follows from `0<J<8*pi` once the same lattice is imposed.

HE4.10 correctly differentiates the continuous interpolation
`E(n)=16*sin(n*hbar_q/16)`, giving `dE/dn=hbar_q*cos(n*hbar_q/16)`. It calls
this derivative the level spacing, but the adjacent discrete gap is instead
`E_(n+1)-E_n = 32*sin(hbar_q/32)*cos((2*n+1)*hbar_q/32)`. `C-SG-007` records
both quantities and their distinction.

HE4.11–HE4.13 compare `E/omega` with the canonical action. `C-SG-006` replaces
the interpretive name `hbar_eff` with “secant action scale,” proves the ratio's
global monotonicity rather than sampling derivatives, and simplifies the
decisive rejection to `dE/d(E/omega)=omega^3`, not `omega`. The ratio tending
to one in the harmonic endpoint is exact; calling its departure “the
anharmonicity” is interpretation rather than an independently unique physical
measure.

HE4.14 and HE4.15 reproduce the exact Legendre identity already accepted as
`C-SG-004`. Their decimal anchor is regression coverage for the exact formula.

## Literature comparator audit

The [APS publisher record](https://journals.aps.org/prd/issues/11/12) confirms
that Dashen, Hasslacher, and Neveu's 1975 article is a semiclassical particle-
spectrum calculation for the sine-Gordon model. The
[1979 primary publisher record](https://doi.org/10.1016/0003-4916(79)90391-9)
states that the Zamolodchikovs construct an exact sine-Gordon soliton S-matrix.
Those records support the historical subject matter, but they do not close
HE4's convention map from the framework's normalized classical action quantum
to the papers' renormalized coupling. No such map is derived in HE4. Therefore
the claimed exact DHN convention match and exactness attribution remain
quarantined comparison statements, not accepted framework claims.

## Scope routing

Charge reciprocity is not computed by any HE4 check. It belongs to the distinct
pending unit HE3, whose declared dependencies include the complex-enriched
Noether charge EM1 and the secant construction HE1. It remains pending rather
than being silently accepted or rejected through HE4.

## Exact qualification

Accepted mappings are `C-SG-001`, `C-SG-003`, `C-SG-004`, `C-SG-006`, and
`C-SG-007`. HE4 is terminally qualified because its exact classical and
conditional algebra is represented, while physical quantization, coupling
identification, literature-spectrum equality, a universal Planck interpretation,
and charge reciprocity are not established by this source unit.
