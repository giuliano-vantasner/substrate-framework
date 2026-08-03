# CM7 Source Adjudication

CM7 is qualified through C-XOV-001 and C-SCR-001 with no registry, release, or
package API delta. Its twenty-seven predicates reproduce, and its complete
surviving exact mathematics is already accepted. The source's numerical and
physical readings require narrower qualification.

For real `E>=0`, `G>0`, and `U>0`, the declared factor
`P(E)=exp(-sqrt(G/(E+U)))` rises strictly from the attained floor
`p0=exp(-sqrt(G/U))` to the unattained limit one. A unique positive crossing
exists exactly for `p0<c<1` and is `E_x=G/log(c)^2-U`. The floor crosses at
zero, `c=1` only in the infinite-input limit, and other real levels do not
cross. When `U=0`, the floor is zero and the inverse loses the subtraction
term. These statements, including the branch conditions, are C-XOV-001.

The squared logarithm cannot relax the level domain. For `c=2`, the algebraic
expression evaluates the factor to one half rather than two. SymPy returning
one expression is therefore an algebraic reproduction, not a complete real
range proof. The source's admissibility check verifies a rational identity,
and its derivative-sign checks use selected points. P121 supplies the global
branch proof and confirms
`partial_c E_x=-2G/(c log(c)^3)>0`,
`partial_G E_x=1/log(c)^2>0`, and `partial_U E_x=-1` throughout the interior.

The common energy-scale law is exact: rescaling `G` and `U` together rescales
the crossing and any energy threshold. Barrier and shift elasticities sum to
one, while all relevant relative sensitivities diverge at the zero-crossing
floor. More importantly, every positive target `E_T` can be fitted by choosing
`c=P(E_T)`. A free horizontal level therefore does not predict a crossover.
Independent normalizations of two putative channels change that level and the
crossing even though the dimensionless factor equation remains exact.

CM7's one-eV statement is a conditional measure calculation. The threshold
level is `c_T=exp(-sqrt(G/(U+E_T)))`. Under a specifically uniform log-c
measure, the fraction of the admissible log window below that threshold is
`1-sqrt(U/(U+E_T))`. Uniform c gives a different exact fraction, and point
masses above or below the threshold give probabilities zero or one. The
reported 1.84 percent is therefore a selected window length, not a probability
over materials, experiments, levels, or operating states.

The selected source inputs are also bounded. The pinned screening module gives
the d+d value `G=985.7655246160418 keV` and assigns one conduction electron per
atom to Ni, Pd, Ti, and Zr. Ni is the maximum of those four assigned models at
`26.367367161568605 eV`. The material record has no uncertainty or universal-
ceiling field. Changing Ni's assigned conduction count from one to sixty-four
doubles the screening energy under the declared one-sixth-power model. Thus the
maximum is reproducible parameter evidence, not a universal material result.

The source bisection agrees with the exact inverse for its six selected levels,
but it always uses `[0,1e9] keV` and never checks bracketing. For the admissible
level `c=0.9999`, the exact root lies above `1e9 keV`; the routine returns its
upper boundary and fails the defining residual. Its three hundred iterations
also continue long after float64 saturation for bracketed examples. Numerical
agreement is regression only because the exact inverse is already available.

Likewise, the seeded random scan is finite. It samples
`rng.uniform(ln_floor*0.999,-1e-6,size=500)`, excluding both endpoints and the
bottom 0.1 percent of the log interval. Its passing residuals do not establish
arbitrary-level validity or a physical distribution.

Forty-four primary and thirty-four independent checks close the exact domain,
endpoint, inverse, derivative, elasticity, scale, identifiability, measure,
material-provenance, bracket, random-scan, mutation, and nonduplication ledgers.
Three direct and two transitive source consumers replay 131 checks. No sampled
integration or NumPy compatibility route is involved.

C-XOV-001 and C-SCR-001 remain unchanged and are mapped individually to CM7.
No predicted coherent rate, common observable, channel dominance, universal
screening maximum, one-eV operating probability, nuclear or coherent
mechanism, material selection, yield, heat, or observation is accepted.
