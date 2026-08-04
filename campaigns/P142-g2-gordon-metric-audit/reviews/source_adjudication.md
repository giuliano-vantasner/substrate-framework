# G2 source adjudication

G2 is qualified, not accepted wholesale. Native execution exits cleanly and
prints all six checks passing; it has no NumPy integration compatibility event.
The scientific failure is instead a convention error hidden by internally
consistent matrix algebra.

The primary Gordon source that G2 invokes uses mostly-minus signature,
`u.u=+1`, and `g^ab=eta^ab+(n^2-1)u^a u^b`. G2 retains that plus coefficient
after changing to mostly-plus signature and `u.u=-1`. The consistent
mostly-plus form is
`g^ab=eta^ab+(1-n^2)u^a u^b`, with inverse
`g_ab=eta_ab+(1-1/n^2)u_a u_b`. Its determinants are `-n^2` and `-1/n^2`, so
it remains nondegenerate and Lorentzian for every positive index. G2's
`n=sqrt(2)` pole is spurious. At its `n=2` witness, the wrong-sign inverse
metric is positive definite, so `G_tt=5/6` is curvature of a Riemannian matrix,
not a Lorentzian Gordon analog spacetime.

C-GOR-001 is the corrected positive object. At rest its covariant metric is
`diag(-1/n^2,1,1,1)` and its null speed is `1/n`. For a constant z velocity and
transverse `n=n(x)`, define
`K=(n*n_xx-2*n_x^2)/n^2` and `gamma^2=1/(1-v^2)`. The only nonzero covariant
Einstein components are
`G_tt=-gamma^2*v^2*K`, `G_tz=gamma^2*v*K`, `G_yy=-K`, and
`G_zz=-gamma^2*K`; `G_xx=0` and `R=2*K`. A fresh direct Christoffel, Ricci,
Einstein reconstruction matches these expressions and the contracted Bianchi
identity vanishes componentwise. At `v=1/2`, `n=2+x`, `x=0`, the corrected
value is `G_tt=1/6`, while G2's component ratios happen to survive.

The constant-index limit is flat. Correct static Gordon remains outside the
accepted optical family, but for the right reason:
`-1/n^2=-1+2*epsilon+O(epsilon^2)` rather than G2's
`-1-2*epsilon+O(epsilon^2)`, while the optical entry is
`-1/n=-1+epsilon+O(epsilon^2)`.

Nonzero effective curvature is not an Einstein-source solution. G2 constructs
no executable Gordon stress tensor, action, componentwise tensor equality,
conservation match, coupling derivation, boundary data, or coupled medium
solution. Its cited breather is a one-plus-one field with no z dependence, so
`T_tz=0`; the nonflat half-boost Gordon tensor has `G_tz=-2*G_tt`, defeating
every scalar coupling whenever the claimed `G_tt` source is nonzero. Primary
literature also describes the Gordon geometry as an effective or fictitious
space for photon propagation, not automatically as dynamical gravity.

Decision: promote C-GOR-001 and qualify G2 through that exact effective-metric
surface only. Reject G2's copied-sign convention, sqrt-two material boundary,
five-sixths Lorentzian witness, breather source match, free-coupling argument,
dynamical gravity, physical gravity, and substrate interpretation. The exact
primary and independent derivations, coefficient and signature mutations,
component counterexample, frozen graph, native compatibility classification,
and physical-scope audit leave no hidden debt in the qualified result.
