# PG4 Source Adjudication

PG4's four-check process exits cleanly and preserves a narrow conditional
zero-transfer residual, but its physical Goldberger--Treiman derivation,
mass-squared discrepancy derivation, parameter prediction, and guard do not
survive convention and data-flow audit.

## Reproduction Boundary

The audited unit is the SHA-256-pinned PG4 file at
`substrate@6d1f4e0`. Its native Python 3.12.2 process under NumPy 1.26.4,
SciPy 1.14.1, and SymPy 1.14.0 exits zero in 0.47 seconds with `ALL 4 CHECKS
PASS`. The source imports PCAC, its current decomposition, pion-pole
dominance, a nucleon state interpretation, a physical pion dictionary, and
all masses and couplings. Those imports are evidence context, not accepted
framework premises. No numerical comparator enters the executable checks.

## Current Convention and Divergence

With Minkowski metric `(+---)`, `q=p'-p`, and `Q^2=-q^2`, dimensionless
form factors use the bracket
`[gamma^mu G_A+q^mu G_P/(2M)] gamma5`. Equal-mass on-shell spinors give
`ubar qslash gamma5 u=2M ubar gamma5 u`, so the normalized divergence is
`G_A-Q^2 G_P/(4M^2)`. P063 derives this with exact on-shell algebra and an
explicit Breit-frame spinor representation, including the induced-term sign.

PG4 writes the `q_mu G_P` term without the `2M` denominator while using the
dimensionless pole formula `G_P=4 M F g/(m_pi^2-q^2)`. The two displayed
pieces belong to different form-factor conventions. PG4.1 then evaluates
only `q^2=0`, where the induced term vanishes, and checks that the remaining
expression has the same algebraic shape as a separately named GT residual.
Its complete mixed-convention matching does not vanish after imposing GT;
the corrected convention does.

## PCAC, Pole Dominance, and Remainders

The generalized normalized PCAC form-factor identity constrains
`G_A-Q^2 G_P/(4M^2)` to a declared pion-pole source. It does not separately
determine `G_A`, `G_P`, or `G_piNN`. The further pion-pole-dominance ansatz
reduces that identity to a GT-form residual. Adding a regular induced
remainder changes the identity away from zero by `-Q^2 R/(4M^2)` while
leaving the rational pole residue unchanged. The residue evaluates the
coupling at `Q^2=-m_pi^2`; it is not generally the zero-transfer coupling.
PG4 declares these inputs and never tests a regular remainder or the distinct
evaluation points.

## Chiral and Zero-Transfer Limits

PG4.2 assigns `R_residual=K*m_pi^2` and then verifies the declared factor and
limit. It does not derive the coefficient or the power. The PCAC pole kernel
`m_pi^2/(m_pi^2+Q^2)` has zero-transfer-then-chiral limit one,
chiral-then-zero-transfer limit zero, and proportional-path value
`1/(1+rho)`. Current conservation alone therefore does not license an
unqualified interchange of these limits.

A mass-squared GT discrepancy follows only after declaring a regular
pole-point coupling expansion. P063 derives its exact factor and leading
coefficient and supplies a square-root coupling counterexample for which the
discrepancy is not order `m_pi^2`. PG4's asserted scaling may survive as a
conditional analytic expansion, not as a consequence of its four checks.

## Identifiability and Effective-Model Alternative

PG4.3 solves the supplied monomial equation for `g_A` and substitutes it
back. The exponent constraint has rank one and a three-dimensional kernel;
three explicit continuous rescaling families preserve it. The solve-back is
bookkeeping, not a prediction of any parameter. The guard first assumes GT,
adds an undeclared unit offset to a source, and verifies the constructed
residual. It evaluates no current or pole.

An independently inspected minimal Yukawa-model route produces the relation
only with a fixed axial coefficient one. A generalized coefficient restores
an unconstrained residual. That candidate adds a new field ontology and does
not naturally derive the general physical relation, so it is not promoted.

## Disposition

PG4 is qualified. C-WID-001 may promote the convention-complete conditional
on-shell Ward, PCAC, pole, remainder, residue, and limit-order theorem.
C-GTR-001 may promote the conditional analytic discrepancy and parameter-
identifiability theorem. PG4 establishes no framework-derived QCD current,
PCAC identity, pion-pole dominance, physical pion or nucleon, coupling value,
Goldberger--Treiman prediction, discrepancy coefficient, effective action,
or substrate realization. S1 and S2 remain pending and supply no premise.
