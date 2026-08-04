# Source adjudication: CF2 fixed-area closure

## Decision

CF2 remains qualified through unchanged C-FLX-001. Uniform fixed-area Gauss
data, declared field-energy density, and declared endpoint force produce two
separate exact linear constructions. P168 adds no claim, API, or release
because C-FLX-001 already owns all scientifically supportable content.

CF2 does not establish the condition that equates its two slopes, a map from a
smooth vortex to an ideal uniform tube, a physical charge or chromoelectric
flux, a Riesz mechanism, a Wilson area law, QCD confinement, or a substrate
mechanism. Those statements remain interpretation or overreach rather than
accepted dependency closure.

## Reproduction and compatibility

The immutable source is unchanged at SHA-256
`e9651b9d4db9f23bb54d013a419c2f050725063347e63f253a968781598bfe6a`.
It imports only SymPy, exits cleanly, and passes all fifteen predicates under
the current environment. Its only assertion implements the local check
ledger. CF2 and canonical `flux_tube.py` contain no NumPy integration surface.

The direct six-node narrative graph replays EM3, EM7, QCD3, CF1, CF2, and CF5.
CF1's three and CF5's one immutable `np.trapz` references are isolated behind
aliases backed only by `np.trapezoid`; the sources are not edited. All four
compatibility references are version provenance and earn no scientific status.

## Work-energy distinction

Uniform cap data give `E=Phi/A`. With energy density `E^2/2`, volume
integration over length `L` gives
`U(L)=Phi^2*L/(2*A)` and energy slope `Phi^2/(2*A)`. With separately declared
endpoint force `qE`, distance integration gives
`V(L)=q*Phi*L/A` and force slope `q*Phi/A`.

The slopes agree if and only if `q=Phi/2`. At the superficially natural
assignment `q=Phi`, endpoint work and slope are twice field energy and its
slope. CF2 never consumes `q` in its executable tube-energy path, yet its
question and result call the energy slope the same force as `qE`. All fifteen
checks can therefore pass while the narrative equality remains unproved.

P168's primary route rejects one-half, area-power, charge, and fixed-geometry
mutations. Its fresh route imports neither source nor canonical tube module and
independently solves Gauss data and integrates both constructions. That route
recovers the same exact equality condition and factor-two counterexample.

## Geometry and interpretation boundaries

Fixed area is load-bearing. For
`A(x)=A0*(1+x/L0)`, field energy is
`Phi^2*L0*log(1+L/L0)/(2*A0)`, has nonzero curvature, and approaches the
constant-area expression as `L0` tends to infinity. Spherical spreading gives
`E=Phi/(4*pi*r^2)` and a curved Coulomb comparison decaying at infinity.

Those calculations distinguish conditional geometries; they do not name a
physical phase. Likewise, the `(s,d)=(1,1)` and `(1,3)` arithmetic is exact but
does not construct or import a Riesz operator. Unbounded ideal field energy is
not by itself a Wilson area law or nonperturbative confinement oracle.

The three forms `E^2*A/2`, `E*Phi/2`, and `Phi^2/(2*A)` are identical field
energy per length. They do not identify the result with C-VTX-001/002 tension.
Solving `A_eff=Phi^2/(2*sigma)` for a separately supplied tension reconstructs
that input and depends on it; no smooth vortex profile supplies a uniform
cross-section to CF2.

## Predicate adjudication

CF2.i-a and CF2.i-b are accepted through C-FLX-001 under explicit uniform-cap
and fixed-area premises. CF2.ii-a is accepted exactly. CF2.ii-b and CF2.ii-c
retain degree-one energy, constant energy slope, and zero curvature but lose
the physical confinement reading and any unconditional identity with `qE`.

CF2.iii-a is accepted as field-energy algebra. CF2.iii-b retains only
energy-per-length and slope equality; its CF1 “same object” wording is
rejected. CF2.iii-c correctly preserves scale deferral.

CF2.iv-a through CF2.iv-c retain only integer exponent arithmetic and power
matching. They do not establish dynamical realization. CF2.v-a through
CF2.v-d retain the spherical field, Coulomb curvature, and mathematical limits;
area-law, confinement, deconfinement, and quark language remain outside the
claim.

## Independent, graph, and consumer closure

The primary and fresh exact routes pass 39 and 19 checks. The six-node graph
passes 31 graph checks while replaying 66 lexical and 66 runtime predicates
plus eight assertions. CF2 executably imports none of the five narrative
neighbors.

Forty-three focused flux-tube, vortex, Maxwell, Wilson-loop, and source-audit
tests pass. P027's 22-check verifier, six-check independent review, passing
attempt, canonical module, and tests are byte-identical, so P168 reuses them
instead of ceremonially repeating settled exact evidence.

## Exact qualification

Accepted content remains the conditional uniform fixed-area theorem, both
linear constructions, their distinct slopes and exact equality condition,
variable-area and spherical guards, and the effective-area reconstruction
ceiling. P168 completes current predicate, graph, compatibility, dependency,
and consumer evidence without altering C-FLX-001's four-axis state or
v0.127.0.
