# NY2 Source Adjudication

NY2 is duplicate evidence for C-SK-001's conditional scale expression. Its
coefficient-one nuclear yield, import elimination, generic event payload, and
derived engine replacement are not accepted.

The legacy executable exits zero with `ALL 10 CHECKS PASS`. It inserts the
measured electron rest energy, repeats `16*pi*E_e`, assigns
`Y_NUC_DERIVED_MEV=F_pi_over_e_MeV`, and only then opens the nuclear and engine
comparators. NY1 is already terminal duplicate evidence, and C-SK-001 excludes
physical numerical prediction. Free-symbol independence from the comparator
literals therefore proves only how the local expression was constructed; it
does not derive a nuclear event map or remove the empirical electron input.

For any positive energy unit `U`, dimensional consistency gives
`Q=kappa*U` and the inverse `kappa=Q/U`. It cannot select `kappa=1`. The source
comparators instead imply two distinct nonunit coordinates: approximately
0.928925 for 23.86 MeV and 0.934375 for 24 MeV. Its declared 0.85--1.15 band
contains infinitely many inequivalent choices, so band membership and 7--8%
residuals cannot identify the coefficient.

The missing dynamics are load bearing. Writing the uncomputed sector masses as
`M_2=a_2*U` and `M_4=a_4*U` gives
`Q=(2*a_2-a_4)*U`, which is positive, zero, or negative for allowed supplied
coefficients and realizes every positive factor even after exothermicity is
required. NY2 explicitly admits that no multi-Skyrmion solution or exact
coefficient exists. It supplies no mass functional, boundary conditions,
solver, refinement, state assignment, or corrections.

The physical channel is also incomplete. A one-body alpha final state cannot
carry positive release in the center-of-momentum frame. The measured process
is radiative `D+D -> 4He+gamma`; exact two-body kinematics partitions the mass
difference between photon energy and alpha recoil. Primary measurements make
this a channel with a very small branching ratio relative to the proton branch
at 20 keV. NY2 contains no photon, branching, cross section, or medium energy-
deposition model, and a D+D comparator cannot justify one common nonzero
payload for both H2 and D2 engine categories.

Consumer replay confirms that no migration occurred. The pinned C035 engine
still labels `Y_NUC_EV=24.0e6` as imported, and its parity program passes 108905
comparisons only while that literal remains unchanged. Separate predecessor
engineering code embeds 25.686 MeV. These inconsistent consumers are evidence,
not accepted framework authority, and modifying either would not repair the
missing reaction derivation.

Every NY2 predicate has an individual verdict in `evidence/source-audit.yaml`.
Primary and independent exact routes, coefficient mutations, source AST,
literature and consumer audits, candidate comparison, and dependency inventory
support the terminal duplicate disposition. No numerical quadrature or NumPy
integration alias is used, no canonical API or release changes, and all
unsupported physical objects are excluded rather than borrowed.
