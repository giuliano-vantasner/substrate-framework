# P177 BX1 Source Adjudication

BX1 exits cleanly and all eight source checks run. Instrumentation also shows
all nine BVP and all 572 IVP calls report success with controlled residuals.
That validates execution of the source-defined finite-wall calculation; it
does not validate every sentence in its result prose.

## Accepted exact surface

For a real three-dimensional central radial mode, the substitution
`chi=r*g` exactly turns
`-g''-2g'/r+ell*(ell+1)g/r^2+Vg=E g` into
`-chi''+[ell*(ell+1)/r^2+V]chi=E chi`. It preserves the real radial norm,
`integral r^2 g^2 dr=integral chi^2 dr`, and maps regular
`g=O(r^ell)` to `chi=O(r^(ell+1))`.

On a regular Dirichlet ball of radius `R` with constant vacuum potential
`mu^2`, the modes are spherical Bessel functions and
`E_(ell,n)=mu^2+(z_(ell,n)/R)^2`. Hence the vacuum wall gap has exact
inverse-square scaling and the normalized profile depends on `r/R`; these are
finite-wall properties, not half-line localization. If
`W_ell=ell*(ell+1)/r^2+V-mu^2` is nonnegative almost everywhere and the
self-adjoint boundary form vanishes, the quadratic form gives `E>=mu^2`.
The implication is exact, but a finite sample of `W_ell` is not proof of its
premise.

Finally, a decay predicate evaluated after the endpoint or outer tail is
overwritten by zero is non-discriminating whenever the interior amplitude
clears the predicate's floor. This is an exact counterexample, not merely a
numerical warning. These statements form C-PDE-012.

## BX1 corrections

The native R=80 branch is above threshold and multi-node. The fixed-guess
wall scan wanders, but it does not track one fixed-index branch and therefore
does not prove that every branch has no limit. Robust zero filtering changes
several reported node counts by one; the high-overtone observation survives,
while claimed linear growth is never tested. BX1 also says 5 to 42 nodes and
an l=0 endpoint 0.4015 although its pinned execution prints 5 to 41 and
0.459073.

The lowest source-defined l=2 finite-wall level is well resolved and follows
the soluble vacuum ball. P054 had already established the stronger scoped
version on the accepted C-PDE-006 background: its R=40 averaged level is
1.020703693 above the unit threshold, about 0.249 of the transformed norm lies
in the outer quarter, and the level moves materially from wall 30 to 40.
That is finite-wall numeric evidence only.

BX1 samples `W_2` at 8,000 points and then calls positivity exact. P177 retains
the conditional Rayleigh theorem but not that global premise. The l=0 control
is an eigenpair of the source-defined time-averaged operator; C-PDE-009 forbids
calling it a genuine mode of the full periodic problem without a separate
Floquet construction. No scan of all angular channels supports the phrase
“only genuine internal mode.”

## Decision

Accept C-PDE-012 as a distinct exact native extension and qualify BX1 through
C-PDE-003, C-PDE-005, C-PDE-009, and C-PDE-012. Retain its finite-wall
diagnosis and pure-vacuum counterexample. Do not promote exact global
nonexistence for the sampled profile, every-branch nonconvergence, a genuine
full-periodic l=0 mode, a nonlinear deformation theorem, corpus-wide mechanism
closure, physical radiation, gravity, absolute scale, particle identity, or
substrate realization. SC2 and TX1–TX3 remain pending and receive no authority
from successful source replay.
