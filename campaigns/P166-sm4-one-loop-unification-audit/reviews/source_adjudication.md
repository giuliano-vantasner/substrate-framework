# SM4 Source Adjudication

SM4's exact conditional core survives through accepted composition, but its
source tally overstates provenance and several guard semantics. C-RGE-004
applied to the supplied exactized intercepts and source coefficients gives
coefficient rank two, augmented rank three, a nonzero left-null residual, and
three strictly ordered exact crossings. C-RGE-005 supplies the coefficient
vector only under its separately declared normalized representation table.

## Individual Predicate Verdicts

SM4.1 gives the correct conditional `b0=7`, `b3=-7`, and derivative sign, but
the script does not reuse QCD3 executable code. It imports only `math`, NumPy,
and SymPy and locally repeats the formula, `C_A`, `T_F`, and `n_f`. SM4.2's
vector and signs are exact under C-RGE-005, while the script hard-codes `b1`
and `b2` rather than deriving them from a matter table.

SM4.3 exactly transforms four supplied decimal inputs; it does not derive
those inputs, their uncertainties, a weak-angle scheme, or the `3/5`
coordinate normalization. SM4.4's monotonicities follow exactly from the
constant derivatives, so its 200-point sweep is regression coverage. SM4.5's
rounded crossing table is the numerical evaluation of three exact C-RGE-004
crossings.

SM4.6 contains a correct nonintersection result and a 3.979055-decade supplied-
data spread. Calling spread greater than three a near miss is a declared
classifier. The same predicate also requires the externally cited MSSM scale
to lie inside the SM crossing envelope; that stand-in is unrelated to whether
the three SM lines intersect. SM4.7 correctly reverses the strong derivative
under `b3 -> +7`, but its sampled `L=40` endpoint has negative inverse strong
coupling and lies outside the positive physical domain. SM4.8 correctly tests
parallel-disjoint lines for its unequal intercepts; it omits the equal-slope,
equal-intercept coincident branch.

## Exact Positive Object

The source decimals treated as supplied rationals give inverse coordinates
`295096203/5000000`, `29584599/1000000`, and `10000/1181`. With coefficients
`41/10`, `-19/6`, and `-7`, the exact crossing coordinates
`log(mu/MZ)/(2*pi)` are `55189953/13625000`,
`298508615743/65545500000`, and `74818234257/13581500000`. Evaluating their
scales gives 13.013127, 14.387275, and 16.992183 in `log10(GeV)`. They cannot
be one common intersection because the augmented rank is three.

This is already the object accepted in C-RGE-004, specialized with the
conditional coefficient vector in C-RGE-005 and the SU3 specialization in
C-RGE-002. A new fixed-reference wrapper would duplicate those APIs and embed
noncanonical comparator data. P166 therefore adds no claim, package API, or
release.

## Assumption and Counterfamily Ceiling

Every absolute crossing scale retains the supplied `MZ`; common reference
rescaling moves all scales while preserving their spread. Paired Abelian
coordinate rescaling preserves the electromagnetic row but not unqualified
cross-factor equality. Independent sector matching offsets can realize any
desired common affine point. The source supplies no threshold spectrum,
matching theorem, scheme conversion, uncertainty propagation, perturbative-
domain proof, simple-group embedding, preferred U1 normalization, physical
unification boundary, observed-running likelihood, or substrate mechanism.

## Verification and Consumer Replay

The primary route passes 37 checks through the accepted API and exact SymPy
mutations. A fresh matrix derivation passes 24 checks without importing the
canonical running code. The direct source graph passes 33 checks over SM4 and
four executable consumers, totaling 50 lexical checks, 50 runtime predicates,
and five assertions. All five nodes run natively without legacy NumPy
integration. Sixty accepted renormalization, gauge-beta, and gauge-running
tests pass. One comment-sensitive primary provenance probe failed before its
narrow AST-backed repair and remains preserved as attempt 0003.

## Terminal Decision

SM4 is qualified through C-RGE-002, C-RGE-004, and C-RGE-005. Its exact
supplied-data nonintersection and pairwise crossings survive; its executable-
reuse wording, derived-input reading, undefined convergence-region prose,
arbitrary near-miss threshold, unrelated MSSM stand-in, unrestricted sign-flip
interpretation, complete equal-slope implication, physical Standard Model
unification test, and substrate significance do not. No accepted claim is
challenged or superseded.
