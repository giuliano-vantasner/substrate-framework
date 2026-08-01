---
description: Independent review of C-SG-012
author: vantasner-review
created: '2026-08-02T00:22:00Z'
updated: '2026-08-02T00:29:00Z'
tags:
- substrate-framework
- claim-review
- sine-gordon
- stress-tensor
category: decisions
confidence: working
status: archived
---
# Review of C-SG-012

## Claim Under Review

The claim gives the exact canonical covariant and contravariant stress tensors
of the normalized real sine-Gordon field, factorizes their Cartesian
divergences by the field-equation residual, transforms the covariant tensor to
the declared half-normalized light-cone coordinates, and proves both null
balance laws, the trace relation, and spatial-parity covariance. It explicitly
separates a distinct potentialless massless model from the small-amplitude
limit and excludes any derived physical anomaly, handed-sector selection, or
V-A interaction.

## Sourced Inputs

The review read `v0.43.0`, `C-SG-001`, `C-SG-011`, P049's frozen proposal and
attempts, the canonical APIs and tests, the 37-check primary verifier, the
seven-check independent Noether review, and hash-pinned NC2 at SHA-256
`6854fafe...a2e2`. NC2's canonical-component labels, energy bridge,
small-amplitude inference, anomaly language, pending W1/W7 dependencies, and
physical weak-sector interpretation remain outside the proposed claim delta.

## Independence

The primary route constructs the tensor from the declared scalar Lagrangian,
raises indices, differentiates off shell, and transforms it with the explicit
coordinate Jacobian. The review route starts from a general potential
`U(phi)`, derives energy and momentum continuity directly, and independently
performs the null Jacobian transformation. It does not call the new stress,
divergence, null-component, balance, trace, or potential APIs.

## Verification Status

The maximum status is `symbolic_verified`. SymPy proves the tensor,
off-shell residual factorization, coordinate transformation, balance laws,
trace identity, parity map, exact kink pressure, constant-vacuum limits, and
potentialless countermodel. No unresolved numerical, simulation, or empirical
predicate remains, so numerical agreement would add regression coverage but
not a stronger verdict.

## Sensitivity and Counterexamples

Replacing the coordinate-Jacobian factor one half by one or one quarter fails;
replacing the raised mixed-component sign minus one by zero or plus one fails;
and changing the canonical mixed null coefficient one half to zero, one, or
minus one half fails. Reversing or deleting a balance sign fails. Replacing
NC2's required conversion factor two by one or four fails. Constant vacua give
zero stress, the exact kink has zero pressure, and spatial parity exchanges the
two null components while leaving the mixed component even. Deleting the
potential yields a different massless model; linearizing the accepted fixed
sine-Gordon model retains its mass term and is a counterexample to NC2's
small-amplitude reading.

## Framework Compatibility

The result is native to the accepted normalized sine-Gordon action, signature
`(+,-)`, and C-SG-011 light-cone convention. It introduces no improvement
parameter, fitted constant, empirical comparator, weak-sector dependency, or
new physical ontology. Smoothness and boundary qualifications distinguish
local conservation from integrated conserved charges, and tensor index
placement and coordinate normalization are explicit.

## Dependency and Consumer Replay

Graph impact is low: direct consumers of the canonical module are the package
export surface and `u1_charge`, with quartic-Q-ball and fluctuation consumers
at depths two and three and no affected indexed execution flow. The targeted
81-test replay passes, as do P001 and P048 with status zero. The only edit to an
existing function replaces `1-cos(phi)` by the identical canonical potential
helper. No scientific or consumer debt remains.

## Competing Candidate Audit

Candidates A, B, and C and structural selection criteria were frozen before
the full NC2 script was opened. Candidate A is selected because the canonical
tensor closes every exact obligation off shell with no free parameter.
Candidate B's improvement freedom is unnecessary, while Candidate C is
rejected by exact parity covariance and missing accepted weak-interaction
dependencies, not by numerical comparison.

## Four-Axis Decision

The four axes record an exact native mathematical claim while qualifying the
source's normalization and physical narrative.

- Verification: symbolic_verified
- Review: accepted
- Compatibility: native
- Epistemic: active
- Relationship: depends on C-SG-001 and C-SG-011; challenges and supersedes none

## Promotion Transaction

Promotion adds the canonical potential, Lagrangian, Cartesian tensor,
divergence, light-cone, balance, and trace APIs; exact tests; immutable P049
record; claim registry entry; qualified NC2 mapping; v0.44 release manifest;
generated docs; and synchronized accepted memory. The source's uniformly
half-scaled balances remain mapped as evidence, while its incorrect energy
bridge and physical inferences remain explicitly excluded.

## Continuation if Not Accepted

If the canonical tensor or coordinate transform failed, Candidate B would be
considered only after identifying a concrete unresolved invariant and
governing its improvement freedom. A physical chiral narrative could not
repair an exact tensor or normalization failure.

## Done Gate

The exact positive object, closed dependencies, independent derivation,
sensitive mutations, limiting cases, consumer replay, canonical transaction,
qualified source mapping, empty debt ledger, and the single 346-test repository
promotion gate all pass.

## Cross-References

See P049, NC2, `C-SG-001`, `C-SG-011`, the canonical sine-Gordon module, P049's
source adjudication and impact review, and the active corpus-migration effort.
