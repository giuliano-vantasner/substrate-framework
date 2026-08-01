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
List the base release, dependencies, proposal, derivation, verifier, attempt history, and consumer map read directly. For migration, include the hash-pinned source unit and audit which of its subclaims remain outside the proposed claim delta.

## Independence
State what was independently rederived or implemented and what code, constants, or reasoning were intentionally not shared with the proposal path.

## Verification Status
Assign one status and justify the maximum verdict earned. Confirm the oracle fits the actual obligation and the assertions test the headline rather than copied literals or invariants unrelated to its values. An exact SymPy identity, an audited Lean theorem, SciPy numerical evidence, and a PDE simulation earn different maximum verdicts. Treat a numerical run whose input or outcome is already fixed by an exact result as regression coverage, not independent evidence; for example, exact parameter elimination plus local ODE uniqueness already decides same-data trajectory independence.

## Sensitivity and Counterexamples
Record input mutations, wrong conventions, counterexamples, convergence/limit tests, and whether each relevant check failed when it should. For numerical claims independently inspect solver status, precision, initial/boundary data, mesh/domain/time/tolerance refinement, residual or error norm, conservation/stability behavior, and an independent method or soluble limit.

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
List registry edit, importable implementation/tests, immutable campaign record, release manifest, generated docs, accepted-memory synchronization, source-unit disposition update, and validation commands. For terminal qualification, refutation, duplicate, or scope decisions, record the structured reason and durable evidence path; an unsupported label is not an adjudication.

## Continuation if Not Accepted
Non-acceptance is not campaign success. Name the repair or next candidate and leave the parent effort active. If a foundation issue is independently demonstrated, link the separate revision proposal.

## Done Gate
Accept only when the positive claim and every success gate in `AGENTS.md` pass with an empty debt ledger.

## Cross-References
Link proposal, claim, dependencies, evidence, consumers, release, and parent research arc.
```
