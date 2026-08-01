# Claim governance and framework fit

Use this reference whenever work may change a scientific claim, convention, invariant, dependency, release, or canonical module.

## Authority model

Authority flows from a pinned accepted release through accepted claims to their evidence. Campaign order records chronology only. Commit history establishes provenance only. Neither makes a claim true.

Every claim carries four independent status axes:

| Axis | States |
| --- | --- |
| Verification | `unverified`, `symbolic_verified`, `formal_verified`, `numeric_evidence`, `simulation_evidence` |
| Review | `unaudited`, `audited`, `accepted`, `rejected` |
| Compatibility | `unassessed`, `native`, `compatible_extension`, `conflict` |
| Epistemic | `proposed`, `active`, `qualified`, `superseded`, `refuted` |

Do not infer one axis from another. In particular, committed does not imply reviewed; verified does not imply framework-compatible; later does not imply superseding; and empirical agreement does not imply derived.

## Artifact roles

- `proposals/`: mutable candidate work before adjudication.
- `attempts/`: append-only records inside a proposal; never canonical.
- `campaigns/`: immutable adjudicated research events.
- `governance/claims.yaml`: machine-readable claim graph.
- `governance/releases/`: reproducible accepted claim sets.
- `src/substrate_framework/`: reusable implementation of accepted definitions and derivations.
- `docs/generated/`: canonical views rendered from accepted state.
- memory `efforts`/`proposals`/`attempts`: work state and recall pointers.
- memory `claims`/`releases`: generated or synchronized accepted-state summaries.

## Proposal admissibility

Before calculating, require a proposal manifest with:

- base release and source commit;
- exact question and positive completion object;
- accepted invariants and conventions;
- permitted imports and assumptions;
- at least two candidate concepts, unless uniqueness is proved;
- selection criteria fixed before comparator values are used;
- proposed claim delta and anticipated consumers;
- comparator-blinding point;
- validation and global replay plan.

A candidate cannot alter these fields retroactively without creating a recorded proposal revision and rerunning earlier gates.

## Natural-fit test

A candidate fits naturally when it:

- reuses accepted primitives without redefining them;
- preserves symmetries, topology, units, conventions, and known limits;
- reduces or leaves unchanged the assumption and parameter ledger;
- composes with other accepted sectors through explicit APIs;
- produces consequences without importing their desired values;
- requires no unrelated narrative rewrite to appear compatible.

Reject or reformulate a candidate that fails this test. Try another concept before changing the framework.

## Foundational revisions

Treat foundation changes as separate proposals. Require evidence of a pre-existing inconsistency that does not depend on the proposed replacement. Compare at least two repairs, identify the smallest coherent change, list every affected claim and consumer, obtain independent review, and replay the whole dependency closure.

Do not bundle foundation changes into a candidate campaign. That makes it impossible to tell whether the framework needed revision or the candidate merely needed rejection.

## Promotion transaction

Promote claims individually:

1. Freeze the proposal and its attempt history.
2. Audit the exact claim and verifier sensitivity.
3. Assign all four statuses.
4. Validate accepted dependency closure.
5. Extract reusable implementation and tests.
6. Replay consumers.
7. Add accepted claim and graph edges.
8. Pin a release.
9. Generate docs and accepted memory.
10. Commit the complete transaction together.

Before acceptance, a proposal may record `challenges`. Only an accepted claim may record `supersedes`.

## Success and continuation

Transparency about a failed route is good scientific practice, but it does not satisfy a positive objective. Store it as `failed_attempt`, extract the reusable mechanism, and continue with a repaired or different candidate. Never conceal contradictions or manufacture success; resolve them through better concepts, better methods, or separately governed foundation work.
