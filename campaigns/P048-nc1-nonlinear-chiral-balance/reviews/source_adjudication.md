# NC1 Source Adjudication

NC1 is qualified. Its exact characteristic-current sources, off-shell
topological-current identity, boundary charge, and kink/antikink parity map are
supportable and map to proposed `C-SG-011`. Its conclusion that these facts
derive a nonlinear weak-sector V-A or physical parity-violation mechanism does
not follow.

## Reproduction

The hash-pinned source exits with status zero and `ALL 8 CHECKS PASS` in 0.90
seconds under Python 3.12 and SymPy 1.14.0. The executable correctly obtains
both full-coordinate sources as `-sin(phi)`, both light-cone sources as
`-sin(phi)/2`, the current components
`(j0,j1)=(phi_x,-phi_t)/(2*pi)`, zero divergence, opposite boundary charges,
and unit charges for an explicit kink and its parity image. Reproduction shows
that these checks run as written; it does not validate the final physical
interpretation printed after them.

## Characteristic Balance

With `J_plus=phi_t+phi_x` and `J_minus=phi_t-phi_x`, direct differentiation
gives the same off-shell defect in both channels:

`d_t J_plus-d_x J_plus = d_t J_minus+d_x J_minus = phi_tt-phi_xx`.

On `phi_tt-phi_xx+sin(phi)=0`, both therefore equal `-sin(phi)`. Under the
declared half-normalized light-cone derivatives, the two corresponding sources
are `-sin(phi)/2`. P048 derives these expressions through the canonical API,
rejects coefficients zero, plus one, and minus two, and independently recovers
the half factors in coordinates `u=t+x`, `v=t-x`.

The source repeatedly calls the small-field regime a free chiral limit in
which the split becomes exact. That is not the linearized limit of normalized
sine-Gordon. For `phi=epsilon*f`, division by `epsilon` and
`epsilon->0` gives the massive Klein-Gordon equation
`f_tt-f_xx+f=0`, and each characteristic source approaches `-f`, not zero.
The independent chiral split belongs to the massless wave equation or to
special configurations with zero potential derivative; it is not the generic
linearized sine-Gordon dynamics.

## Topological Current and Charge

For orientation `epsilon^(01)=+1`, the exact current is
`j^mu=epsilon^(mu nu) partial_nu phi/(2*pi)`, hence
`j0=phi_x/(2*pi)` and `j1=-phi_t/(2*pi)`. Its divergence is the antisymmetric
contraction of the symmetric Hessian and vanishes for every sufficiently smooth
field without using any equation of motion. The sign on `j1` is load-bearing;
zero or plus-one replacements fail the divergence predicate.

This identity is topological and off shell, not a nonlinear dynamical current
created or selected by sine-Gordon. Integrated charge exists when the spatial
limits exist and equals
`[phi(+infinity)-phi(-infinity)]/(2*pi)`. It is conserved in time when the
asymptotic flux difference vanishes. If both limits are sine-Gordon vacua
`2*pi*n`, the charge is the integer difference `n_plus-n_minus`. Without these
boundary hypotheses, local divergence zero alone does not grant an integer or
a conserved whole-line integral.

## Parity and the Physical-Inference Failure

Treating `phi` as a scalar under spatial parity gives
`phi_P(t,x)=phi(t,-x)`. The topological current transforms axially:
`j0[phi_P](t,x)=-j0[phi](t,-x)` while
`j1[phi_P](t,x)=j1[phi](t,-x)`. Consequently the whole-line winding changes
sign. The unit kink `4*atan(exp(x))` and its parity image are exact normalized
sine-Gordon solutions with charges plus and minus one by both boundary limits
and direct density integration.

The same calculation proves that the field equation is invariant under this
parity transformation. A symmetry that maps a kink sector to a degenerate
antikink sector is not a parity violation. Selecting only one sector would be
an additional boundary, state, interaction, or coupling premise. NC1 provides
none. Moreover, its current is identically conserved for arbitrary smooth
fields and contains no chiral coupling, weak charge, vector-minus-axial
vertex, or interaction that distinguishes left from right. Calling an axial
current “parity-odd” describes its transformation law; it does not prove that
the theory violates parity.

## Dependency Audit

NC1 declares W1, W3, and W7 as dependencies for its weak-sector reading, but
all three remain pending source units and none is an accepted framework claim.
The exact mathematical content closes from the accepted normalized
sine-Gordon convention plus smoothness and explicit boundary hypotheses. The
physical V-A conclusion has no accepted dependency closure and cannot be
promoted through chronology or narrative inheritance.

## Terminal Disposition

NC1 maps its exact nonlinear characteristic balance, normalized topological
current, integer vacuum-boundary charge, and parity-sector exchange to
`C-SG-011`. It remains qualified for calling the small-field sine-Gordon limit
a massless free chiral theory; treating the EOM-independent topological current
as a nonlinear dynamical replacement; and inferring intrinsic parity
violation, weak-force chirality, a V-A interaction, a selected topological
sector, bosonization closure, particle identity, or substrate ontology. Later
NC units may import only `C-SG-011`'s exact identities and explicit ceilings.
