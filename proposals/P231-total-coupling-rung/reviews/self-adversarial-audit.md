# P231 self-adversarial audit (author's own, pre-review)

Audited against issue #88's four composition obligations and the AGENTS.md
success gates, not against the author's own test list.

## Obligation-by-obligation audit

**Selection derivation.** The three legs are exact: L1 positivity and the
squeeze 0 < J(z) <= 1 come from the defining integrals (positive integrands,
positive operator spectrum); L2 monotone decoupling comes from
dJ/dz = -(tau^-1 class) with the tau^-1 class itself a positive-integrand
integral (exact squeeze 0 < E1(z) <= exp(-z)/z; K_0 by its standard
representation); L3 is C-GRV-001's own cutoff ontology. The usable set
{sharp, smooth} and the exclusion of the power-subtracted family (exact roots
exp(1-EulerGamma) and exp(-EulerGamma)) are outputs, not choices. Candidates
B (point scheme) and C (subtraction scale) fail the preregistered criteria
and are recorded as rejected with reasons; D exceeds the accepted
local-coefficient ceiling.

**Additive-baseline provenance.** B is a declared premise per C-GRV-001;
the B=0 reading is itself a declared premise with the exact consequence
structure (attractive iff xi < 1/6, independent of N, m^2, Lambda, scheme;
G_total = 12*pi/(N*(1-6*xi)*J(z)*Lambda^2) for xi < 1/6; conformal marginal
locus 1/G_total = 0 exactly) and the exact downstream ceiling (scheme
bracket R(z) in [1, inf) with the exact unit-mass value).

**Total-sign map.** Necessary and sufficient in each xi case, including the
exact-mass corrections through J(z), the conformal point, and the
uniform-in-mass thresholds with correct direction (finding F2 repaired and
boundary-tested from both sides).

**Control ledger.** The tau^-1 class is exactly -dJ/dz per scheme, its log
divergence at m^2=0 is declared with the z_min domain (finding F5), the
tau^-3 vacuum sector is exhibited from the accepted families, and the
nonlocal remainder is bounded by the declared derivative-expansion
parameter rather than silently omitted.

## Defects found by the audit and repaired

F1-F6 in attempts/0001/manifest.yaml. Two were module-side physics/boundary
defects (F1 NaN at the massless point; F2 backwards uniform-in-mass
threshold), two were oracle-honesty issues (F4 sign decidability tiers; F5
silent divergence), one was a completeness gap against the issue text
(F6 baseline provenance surface), one was a test-side wrong expected value
(F3).

## Known limits stated honestly

- The spread R(z) is unbounded, so no unique numeric normalization is
  derived; the ceiling is quoted exactly. This is the issue's comparator-
  blinding boundary, not a hidden failure.
- The nonlocal bound is a declared derivative-expansion bound, not a
  derived constant; the domain is predeclared.
- Sign classification uses a certified numeric tier only for symbol-free
  inputs and returns None (never a guess) inside the separation band.


## Addendum (attempt 0002): session crash recovery and finding F7

The working session crashed while rewriting the test file after the F1-F6
repairs; the on-disk test file was truncated to zero bytes and the restored
kernel snapshot held the pre-repair 23-test version. Reconstruction from
the snapshot plus the attempt-0001 evidence recovered the file; the F2/F3
repair deltas were re-applied, and the defining-integral oracles were
re-stated in a form SymPy can actually decide (closed-form derivative
identities, one-sided limits, and 50-digit mpmath quadrature agreement)
because unevaluated Integral differences do not simplify.

**F7_symbolic_half_line_baseline_undecidable.** The F4 three-tier
classifier could not certify `B >= 0` symbolic baselines: a baseline
constrained to the same closed half-line as the strictly signed shift
cannot cancel it, yet the total returned None. This contradicted both the
F2 uniform threshold (`B >= 0` attractive for every mass, sub-conformal)
and the F4 repair statement ("decidable whenever the baseline sign does not
oppose the weight"). Repair: a half-line leg in the derived-structure tier
(`baseline.is_nonnegative` with weight +1, symmetrically nonpositive with
weight -1), locked by boundary tests on both sides (positive symbol,
nonnegative symbol decided; unconstrained symbol still None).
