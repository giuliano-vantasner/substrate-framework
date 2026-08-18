# C-GRV-002 Claim Review

## Claim Under Review
The claim is the exact necessary-and-sufficient total-sign map for the derived usable total coupling, with the additive-baseline provenance and the total Newton constant. Under C-IGR-004's condition `1/G_total = B + Delta`, `Delta = N*(1-6*xi)*Lambda^2*J(z)/(12*pi)`, `0 < J(z) <= 1` on the usable set, the attractive Newtonian sign `1/G_total > 0` holds: for `xi < 1/6` iff `B > -Delta` (uniform in mass iff `B >= 0`, with a unique critical mass for negative `B`); for `xi = 1/6` iff `B > 0` (the purely-induced reading lands exactly on the marginal locus `1/G_total = 0`); for `xi > 1/6` iff `B > N*(6*xi-1)*Lambda^2*J(z)/(12*pi) > 0`. The baseline `B` is a declared premise per C-GRV-001; the purely-induced reading `B = 0` is attractive iff `xi < 1/6`, and `G_total = 1/(B+Delta)` preserves sign, returning no constant at the marginal locus and a negative constant in the repulsive regime.

## Sourced Inputs
The review read accepted release v0.161.0, C-GRV-001 and C-IGR-004, the P231 proposal and formula freeze, the candidate comparison, dependency, consumer, and nonduplication audits, the four prior attempt manifests and the self-adversarial audit (findings F2/F7/F8 on the sign-map direction, half-line baselines, and the tuned boundary), the module `total_gravitational_coupling.py` (`attractive_sign_map`, `total_inverse_gravity_coupling`, `purely_induced_attractive_verdict`, `baseline_provenance`, `total_newton_constant`), its tests, and both verifier routes.

## Independence
An independent rederivation rebuilt the sign algebra from scratch with fresh SymPy, importing no `total_gravitational_coupling` symbol: solving `B + Delta = 0` for the attractive boundary `B* = -Delta`, confirming `Delta = 0` identically at `xi = 1/6`, deriving the uniform-in-mass threshold from the large-mass worst case `J -> 0` (confirmed by quadrature, not an unevaluated symbolic limit), and evaluating the purely-induced verdict `attractive iff 1-6*xi > 0` at `xi in {0, 1/12, 1/6, 1/5}`.

## Verification Status
The claim earns `symbolic_verified`. Each xi-case condition is an exact algebraic consequence of `1/G_total > 0` given the exact sign `sign(Delta) = sign(1-6*xi)` on the usable set (where `J(z) > 0`). The conformal marginal locus `1/G_total = 0` is exact. The module's three-tier decidability (exact SymPy, derived-structure including half-line-constrained symbolic baselines, then certified 70-digit numeric separation returning `None` inside the band) never guesses a sign.

## Sensitivity and Counterexamples
A baseline-sign mutation flips the attractive verdict (`B = -1/4` repulsive vs `B = 1/4` attractive at the same operator data); the super-conformal boundary `B* = 1/(12*pi)` is tested from both sides (above attractive, below repulsive). The Newton constant returns `None` at the marginal locus (never `zoo`/silent division), a finite negative value in the repulsive regime, and its purely-induced bracket ratio is exactly `R(z)`. Tiny `1e-60` totals resolve to finite constants while exact zeros return `None`, and the certified sign band was probed at its `1e-50` edge.

## Framework Compatibility
The claim is a compatible conditional extension built directly on C-IGR-004 and C-GRV-001's baseline ledger. It introduces no fitted constant, no observed-G comparator, no sourced geometry, and no radiative prediction; the baseline remains an external declared input and the total value stays scheme-bracketed by `R(z)`, so no unique numeric `G` is asserted.

## Dependency and Consumer Replay
The accepted dependencies are C-GRV-001 (baseline ledger) and C-IGR-004 (the composition object the sign map operates on), both current-accepted in v0.162.0. The consumers are the module's sign-map, provenance, and Newton-constant surfaces and their tests; the change is additive and the accepted P230 and C-GRV-001 consumer suites replay green.

## Competing Candidate Audit
The sign map is a consequence of the selected candidate A composition; no separate candidate set applies to the sign statement beyond A's usable-set derivation, and no empirical comparator was opened. The conformal point and the uniform-in-mass thresholds were derived from the exact worst-case structure, not fitted.

## Four-Axis Decision
Verification is `symbolic_verified`; review is `accepted`; compatibility is `compatible_extension`; epistemic status is `active`. The relationship is a new claim depending on C-GRV-001 and C-IGR-004, with no challenge or supersession edge.

## Promotion Transaction
The transaction materializes this review, the registry entry, release v0.162.0 and its `current.yaml` update, the shared campaign record and canonical module/tests, generated docs, and accepted memory, replayed once at the final boundary.

## Continuation if Not Accepted
Not applicable after acceptance. Any total value pinned to a unique number, any sourced field-equation solution, or any empirical confrontation requires a separate proposal and an input no accepted claim currently supplies.

## Done Gate
The claim is accepted together with the final status-zero campaign verifiers, full repository validation, generated-state checks, and an empty P231 debt ledger.

## Cross-References
See the P231 proposal, formula freeze, `verify.py`, `independent_total_coupling_review.py`, C-GRV-001, C-IGR-004, `total_gravitational_coupling.py`, `tests/test_total_gravitational_coupling.py`, base release v0.161.0, and accepted release v0.162.0.
