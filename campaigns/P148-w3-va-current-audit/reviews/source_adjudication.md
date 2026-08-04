# W3 source adjudication

W3 is qualified, not accepted wholesale. Native execution passes W3.1 through
W3.3 and then stops only at NumPy's removed `trapz` name. An isolated alias to
`np.trapezoid` reproduces all seven checks and the terminal tally without
editing the immutable source. That compatibility event is version-only; the
tally remains reproduction evidence rather than a headline oracle.

The first load-bearing sign is wrong. For
`phi=L(t+x)+R(t-x)`, direct differentiation gives
`phi_t=L'+R'` and `phi_x=L'-R'`. W3 assigns the negative spatial derivative.
Its own W3.3 calculation consequently finds the plus combination equal to
`2R'` and the minus combination equal to `2L'`, then separately asserts that
the desired plus channel is left. The correct massless identities are already
accepted under C-SG-011 and C-SG-012.

With signature `(+,−)` and `epsilon^(01)=+1`, define
`D^mu=partial^mu phi=(phi_t,-phi_x)` and
`T^mu=epsilon^(mu nu)partial_nu phi=(phi_x,-phi_t)`. Their divergences are
`Box phi` and zero, respectively. On normalized sine-Gordon solutions the
first is `-sin(phi)`; the second is the accepted topological-current identity.
W3 never computes these divergences. Instead it imports conservation of a
distinct complex-field U1 current and uses a finite potential displacement for
its axial reading. A genuinely real field has zero complex-Noether current.

Scalar parity transforms D as a vector, T as an axial vector, and exchanges
the null combinations D−T and D+T. That is a covariance statement. W3 supplies
no parity-breaking action, matter representation, selected coupling, spinor
bilinear, gauge connection, current vertex, anomaly calculation, or dynamics.
Calling one exchanged null derivative a maximally violating charged current
does not construct any of those objects.

W3.4 normalizes a Gaussian to area `-2*pi` before quadrature, assigns the
resulting integer comparison, and solves no boundary evolution. The accepted
half-line charge law still needs a boundary field change and vacuum data.
Moreover W2's SU2 ladder changes T3 by one, while its supplied basis labels
change from -1 to +1 and hence by two; W3 inherits rather than resolves that
event-label conflation.

W3.G1 chooses sine and cosine traces in quadrature, obtains a near-zero sign
correlation, and relabels it zero topological transfer. Exact countermodels
give nonzero correlation with zero transfer and zero correlation with nonzero
transfer, as C-SG-013 already requires. Parity-even laws also do not force each
state or outcome to be symmetric.

Decision: qualify W3 through C-SG-011, C-SG-012, C-SG-013, C-BND-001,
C-REP-002, and C-U1-001 without a new claim or release. Retain the corrected
derivative identities, epsilon-dual conservation, parity exchange, conditional
boundary trace, and field-type distinction under those ceilings. Do not
promote a physical V-A current, charged vertex, intrinsic parity violation,
charge-changing boundary event, real-scalar U1 current, axial anomaly, gauge
interaction, weak sector, or substrate realization.

The primary, fresh independent, and frozen-graph routes pass 47, 25, and 61
checks. The graph pins seventeen units, 184 source predicates, and sixteen
assertions. Mutable code uses exact integration or current NumPy APIs; immutable
legacy compatibility is alias-only evidence. Campaign debt is empty at the
no-release boundary.
