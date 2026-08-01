# Claim Review and Promotion Template

Use one instance per claim. Review raw artifacts against frozen criteria; do not accept a campaign wholesale or inherit the proposing agent's preferred narrative.

```md
---
description: Independent review of <claim-id>
author: <reviewer-id>
created: '<ISO-8601>'
updated: '<ISO-8601>'
tags:
- substrate-framework
- claim-review
category: decisions
confidence: working
status: active
---

## Claim Under Review
Quote the exact statement, quantifiers, regime, conventions, proposed graph relationship, and positive framework role.

## Sourced Inputs
List the base release, dependencies, proposal, derivation, verifier, attempt history, and consumer map read directly.

## Independence
State what was independently rederived or implemented and what code, constants, or reasoning were intentionally not shared with the proposal path.

## Verification Status
Assign one status and justify the maximum verdict earned. Confirm the assertions test the headline rather than copied literals or invariants unrelated to its values.

## Sensitivity and Counterexamples
Record input mutations, wrong conventions, counterexamples, convergence/limit tests, and whether each relevant check failed when it should.

## Framework Compatibility
Assess invariants, assumptions, imports, parameters, units, conventions, limits, and cross-sector composition. If the concept does not fit, reject or return it for a different candidate; do not retrofit unrelated claims.

## Dependency and Consumer Replay
List direct/indirect consumers and exact replay results. Record any debt created by the claim.

## Competing Candidate Audit
Confirm plausible alternatives and selection criteria were registered before comparator inspection. Explain the structural reason for selection independently of numerical closeness.

## Four-Axis Decision
Record verification, review, compatibility, and epistemic status separately. Before acceptance, use `challenges`; only accepted replacements may use `supersedes`.

- Verification:
- Review:
- Compatibility:
- Epistemic:
- Relationship:

## Promotion Transaction
List registry edit, importable implementation/tests, immutable campaign record, release manifest, generated docs, accepted-memory synchronization, and validation commands.

## Continuation if Not Accepted
Non-acceptance is not campaign success. Name the repair or next candidate and leave the parent effort active. If a foundation issue is independently demonstrated, link the separate revision proposal.

## Done Gate
Accept only when the positive claim and every success gate in `AGENTS.md` pass with an empty debt ledger.

## Cross-References
Link proposal, claim, dependencies, evidence, consumers, release, and parent research arc.
```
