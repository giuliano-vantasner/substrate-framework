---
description: Independent review of C-EFT-001 conditional quadratic heavy-field elimination
author: vantasner-review
created: '2026-08-02T12:09:06Z'
updated: '2026-08-02T12:09:06Z'
tags:
- substrate-framework
- claim-review
- effective-action
category: decisions
confidence: established
status: archived
---
# C-EFT-001 Claim Review

## Claim Under Review

C-EFT-001 states an exact conditional finite-dimensional action theorem. For
a real column field with a nonempty symmetric invertible quadratic kernel and
a declared plus-source convention, it fixes the stationary field and Schur
complement. A declared even/odd source split fixes the inherited odd cross
term. A finite low-momentum Neumann expansion retains its exact multiplication
residual. Stationary chain-rule reduction preserves supplied explicit
variation and cannot create or normalize a missing anomaly. The claim excludes
all physical HLS, WZW, vector-meson, coefficient, baryon, `N_c`, scale, and
substrate interpretations.

## Sourced Inputs

The review reads base release `v0.52.0`, P059's frozen proposal, four append-only
attempts, the SHA-256-pinned WZ4 source and native reproduction, the
check-by-check source audit, primary HLS provenance, both exact verifiers, the
new canonical module and tests, impact analysis, and WZ4's regenerated
migration entry. C-LIE-001, C-WZW-001, C-WZW-002, and C-TOP-002 were audited as
scope ceilings but are not needed to prove the matrix theorem. Pending G2, G3,
S3, and S4 supply no premise. WZ4 is pinned at
`fca6b9c1d95bdf49e99b863470c7e800880e493b3f716159aa2341f8cf963d2b`.

## Independence

The independent review imports no canonical effective-action helper. It
differentiates a general symmetric two-component action, solves with the
adjugate, substitutes directly, and completes the square. It separately
expands even and odd sources, derives noncommuting left and right Neumann
residuals, computes the anomaly-map rank and nullity, and constructs arbitrary-
and zero-contact counterexamples to WZ4. Its comparison objects were derived
before use; no physical comparator or WZ4 target coefficient selected them.

## Verification Status

The maximum verdict is `symbolic_verified`. The canonical module's seven tests
and the independent verifier's 23 checks use exact SymPy expressions, actual
component derivatives, matrix residuals, and direct substitution. The first
focused test rejected an algebraically identical factored scalar series because
it compared expression trees; the repair compares the exact simplified
difference to zero and changes no tolerance or expected formula. No numerical
claim is promoted.

## Sensitivity and Counterexamples

Opposite and doubled stationary fields fail the equation of motion. Removing
the quadratic one-half changes the equation and rejects the canonical
stationary point. Removing either source kills the odd cross term, while odd
parity reverses only that cross term. Nonsymmetric, singular, empty, and
wrong-shaped inputs are rejected. A finite inverse series multiplies to the
identity only through the declared order and retains nonzero exact next-order
residuals for a noncommuting matrix example.

Assigning anomaly variation to a purported homogeneous term fails the
invariance predicate. With zero starting inhomogeneous level, stationary
elimination leaves zero. Replacing WZ4's imported WZW coefficient by arbitrary
`C` makes its zero-momentum and heavy-mass checks return `C`; setting `C=0`
makes its displayed amplitude zero. Physical pion parity also defeats the
source's four-polar-vector interpretation.

## Framework Compatibility

The theorem uses only approved exact matrix algebra and explicit assumptions.
It introduces no fitted parameter and has no accepted-claim dependency. The
declared four-dimensional dimension example is consistent but is not required
for the abstract theorem. Candidate B is a compatible extension. Candidate D
supplies the exact interpretation ceiling. Candidate A fails as a positive HLS
route; Candidate C confirms externally that the four homogeneous coefficients
are free rather than deriving a framework HLS sector.

## Dependency and Consumer Replay

The accepted dependency list is empty. GitNexus found no pre-existing symbol
or process for the additive module. Later WZ/HLS consumers remain pending and
cannot reinterpret this matrix theorem as a physical vector construction.
Focused tests and campaign verifiers exercise the new surface; the registry,
release, generated outputs, migration inventory, and every repository test are
part of the promotion replay. No canonical symbol is removed or renamed.

## Competing Candidate Audit

Candidates A through D and structural criteria were frozen before WZ4's
executable internals were opened. B and D are selected because they deliver an
exact positive action theorem and its precise anomaly ceiling with fewer
premises. A's clean tally is rejected as a selection oracle because it never
constructs the advertised objects. C is retained as audited external theory
evidence; its free coefficients require an additional UV or phenomenological
selection premise. No numerical closeness or phenomenological value selected
the claim.

## Four-Axis Decision

The axes are assigned independently and without a supersession relationship.

- Verification: `symbolic_verified`
- Review: `accepted`
- Compatibility: `compatible_extension`
- Epistemic: `active`
- Relationship: new dependency-free conditional theorem

## Promotion Transaction

Promotion adds the pure effective-action module and tests, C-EFT-001 in the
registry, release `v0.53.0`, immutable P059 records, a qualified WZ4
disposition, regenerated source claims, rendered canonical docs and accepted
memory, and a separate effort synchronization commit. Both exact verifiers,
focused tests, pre-commit impact analysis, the full workflow gate, the
explicitly required pytest replay, memory validation, and `git diff --check`
must pass before the transaction is sealed.

## Continuation if Not Accepted

This clause is inactive because the exact conditional theorem is accepted.
WZ4's physical HLS and WZW-generation narrative remains historical attempt
evidence. A future positive HLS claim requires a separately governed field
content, transformations, action, operator basis, coefficient-selection
premise, Ward identities, and accepted physical map.

## Done Gate

The claim-level mathematical debt is empty after exact and independent review.
The parent corpus migration remains active because later queue units remain
pending.

## Cross-References

See P059, WZ4, `effective_actions.py`, `test_effective_actions.py`, the two
audited HLS primary sources, and release v0.53.0.
