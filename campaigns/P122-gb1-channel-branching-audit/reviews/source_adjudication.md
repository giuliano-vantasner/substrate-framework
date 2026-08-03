# GB1 Source Adjudication

GB1 is qualified through new claim C-BRN-001. Its eighteen predicates
reproduce, and its exact two-channel normalization becomes a reusable,
domain-complete theorem. Its physical rate, exhaustive-channel, weight,
dependency, and barrier-free readings remain outside accepted closure.

For exact nonnegative common-dimension inputs `A` and `B` with `A+B>0`, the
canonical fractions `A/(A+B)` and `B/(A+B)` lie in the closed unit interval and
sum to one. Either zero endpoint is valid; the double-zero point is undefined
and rejected. On the positive interior, the odds equal `A/B`, the first share
increases with `A`, decreases with `B`, and tends from zero to one. Common
positive scaling cancels, while changing one channel normalization changes the
fractions. These statements are C-BRN-001.

GB1's specialization is exact under explicit premises. With
`A=r_s*w*N`, `B=r_gamma`, and `rho=r_gamma/r_s`, positive `r_s` gives
`B_soft=w*N/(w*N+rho)` and `B_gamma=rho/(w*N+rho)`. If `r_s` and `r_gamma`
share an inverse-time dimension and `w` and `N` are dimensionless, both inputs
share that dimension and the fractions are dimensionless. C-BRN-001's
canonical specialization strengthens the source by requiring a positive
integer population and rejecting invalid signs, floats, zero weight, and a
zero total.

The relative-odds result `w*N/w1` is also exact only with its hidden domain
made visible: both comparison odds require positive comparison rates, the
same positive channel normalizations must be used at the two points, and the
baseline weight `w1` must be nonzero. The result still depends on free `w`,
`N`, and `w1`; it predicts no enhancement. For any target fraction strictly
between zero and one, a positive `rho=w*N*(1-q)/q` fits it exactly.

Several source checks are materially weaker. The first predicate computes
`r_gamma/r_s-rho.subs(rho,r_gamma/r_s)`, which is zero after substituting the
desired answer and contains no `rho`; it does not test an independently
supplied ratio. The executable uses `w` as an independent symbol. Although
`n`, `Omega`, and `omega_ph` are declared and whitelisted, none enters a rate,
fraction, or enhancement. Thus no PN2 subdivision law or function `w(n)` is
implemented.

The shared `K_loss`, `G_coh`, `Wc`, and `W_nuc` factors appear only in prose
and comments. One genuinely common positive factor would cancel, but unequal
channel gates change the first fraction by
`A*B*(C_s-C_g)/((A+B)*(C_s*A+C_g*B))`. A zero interaction can remove both
physical rates entirely. The source neither constructs the claimed common
factors nor tests their equality.

The barrier-free check is finite syntax only. Its helper reports any SymPy
power with exponent one half, so benign `sqrt(w)` is a false positive. A
non-square-root barrier-shaped factor, an opaque imported symbol, a precomputed
constant, an alias, or semantics hidden inside `w` evades it. The free-symbol
whitelist similarly checks only locally constructed expressions and not data
flow or imported meaning. No physical independence from screening,
tunnelling, barriers, or empirical inputs is established.

The cited candidate dependencies supply no missing rate premise. PN2 has no
accepted claim. C-SPN-002 proves normalized ladder coefficients and explicitly
states that their squares are not rates. C-CMP-001's conditional composition
retains a matrix-element dimension and establishes no transition rate or
physical channel. Source edges and cycles add no authority.

Forty-two primary and twenty-six independent exact checks plus fifteen focused
package tests close the allocation, endpoint, odds, derivative, limit, scale,
dimension, specialization, enhancement, arbitrary-target, unequal-gate,
source-predicate, scan, and physical-ceiling ledgers. Four direct and ten
transitive consumers replay 576 checks from pinned hashes. No sampled
integration or NumPy compatibility event occurs.

C-BRN-001 accepts only conditional allocation algebra. GB1 does not establish
a physical excited state, exhaustive soft or gamma channels, coherent
preparation, interaction, subdivision weight, nuclear transition, rate
magnitude, material branching fraction, enhancement prediction, yield, heat,
or observation.
